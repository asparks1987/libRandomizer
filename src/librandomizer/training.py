"""Portable training-data generation for input/output pair datasets."""

from __future__ import annotations

import copy
import csv
import inspect
import json
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence


JSONValue = Any
SchemaLike = Any


class TrainingDataError(ValueError):
    """Raised when dataset generation or serialization fails."""


@dataclass(frozen=True)
class SchemaNode:
    """Serializable description of an input or output value."""

    kind: str
    params: dict[str, Any] = field(default_factory=dict)

    def to_spec(self) -> dict[str, Any]:
        return {"kind": self.kind, "params": _encode_json(self.params)}

    @classmethod
    def from_spec(cls, spec: Mapping[str, Any]) -> "SchemaNode":
        if not isinstance(spec, Mapping):
            raise TrainingDataError("Schema spec must be a mapping.")
        kind = spec.get("kind")
        if not isinstance(kind, str) or not kind:
            raise TrainingDataError("Schema spec requires a non-empty kind.")
        params = spec.get("params", {})
        if not isinstance(params, Mapping):
            raise TrainingDataError("Schema spec params must be a mapping.")
        return cls(kind=kind, params=_decode_json(dict(params)))

    def generate(self, rng: random.Random) -> JSONValue:
        kind = self.kind
        params = self.params

        if kind == "integer":
            low = int(params.get("min", 0))
            high = int(params.get("max", 99))
            _validate_range(low, high)
            return rng.randint(low, high)

        if kind == "number":
            low = float(params.get("min", 0.0))
            high = float(params.get("max", 1.0))
            precision = params.get("precision")
            _validate_range(low, high)
            value = low if low == high else rng.uniform(low, high)
            return round(value, int(precision)) if precision is not None else value

        if kind == "boolean":
            probability = float(params.get("probability", 0.5))
            if probability < 0.0 or probability > 1.0:
                raise TrainingDataError("Boolean probability must be between 0 and 1.")
            return rng.random() < probability

        if kind == "string":
            length = _validate_size("length", params.get("length", 12))
            alphabet = str(
                params.get("alphabet", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
            )
            if not alphabet:
                raise TrainingDataError("String alphabet must not be empty.")
            return "".join(rng.choice(alphabet) for _ in range(length))

        if kind == "choice":
            options = _validate_items(params.get("options"))
            return copy.deepcopy(rng.choice(options))

        if kind == "array":
            item_schema = ensure_schema(params.get("items"))
            length = params.get("length")
            min_length = params.get("min_length", 0)
            max_length = params.get("max_length", 3)
            if length is not None:
                size = _validate_size("length", length)
            else:
                _validate_range(min_length, max_length)
                size = rng.randint(int(min_length), int(max_length))
            return [item_schema.generate(rng) for _ in range(size)]

        if kind == "object":
            properties = params.get("properties", {})
            if not isinstance(properties, Mapping):
                raise TrainingDataError("Object schema properties must be a mapping.")
            return {name: ensure_schema(schema).generate(rng) for name, schema in properties.items()}

        if kind == "null":
            return None

        if kind == "literal":
            return copy.deepcopy(params.get("value"))

        if kind == "one_of":
            options = [ensure_schema(option) for option in _validate_items(params.get("options"))]
            return rng.choice(options).generate(rng)

        raise TrainingDataError(f"Unsupported schema kind: {kind}")

    def validate(self, value: JSONValue) -> None:
        _validate_against_schema(self, value)


@dataclass(frozen=True)
class TransformSpec:
    """Serializable description of a transform used to derive outputs."""

    name: str
    params: dict[str, Any] = field(default_factory=dict)

    def to_spec(self) -> dict[str, Any]:
        return {"name": self.name, "params": _encode_json(self.params)}

    @classmethod
    def from_spec(cls, spec: Mapping[str, Any]) -> "TransformSpec":
        if not isinstance(spec, Mapping):
            raise TrainingDataError("Transform spec must be a mapping.")
        name = spec.get("name")
        if not isinstance(name, str) or not name:
            raise TrainingDataError("Transform spec requires a non-empty name.")
        params = spec.get("params", {})
        if not isinstance(params, Mapping):
            raise TrainingDataError("Transform spec params must be a mapping.")
        return cls(name=name, params=_decode_json(dict(params)))


@dataclass(frozen=True)
class TrainingPair:
    """A generated input/output pair."""

    input: JSONValue
    output: JSONValue
    index: int

    def to_record(self) -> dict[str, JSONValue]:
        return {"input": self.input, "output": self.output}


class TrainingDataGenerator:
    """Generate reproducible training pairs from a portable schema."""

    def __init__(
        self,
        input_schema: SchemaLike,
        output_schema: SchemaLike | Callable[..., JSONValue],
        *,
        count: int | None = None,
        seed: int | str = 42,
        transform: Callable[..., JSONValue] | None = None,
        transform_spec: TransformSpec | Mapping[str, Any] | str | None = None,
    ) -> None:
        self.input_schema = ensure_schema(input_schema)
        self.transform = transform
        if callable(output_schema) and transform is None:
            self.output_schema = None
            self.transform = output_schema
        else:
            self.output_schema = ensure_schema(output_schema)
        self.count = _validate_size("count", count) if count is not None else None
        self.seed = seed
        self.transform_spec = _coerce_transform_spec(transform_spec)
        self._transform_mode = _detect_transform_mode(self.transform) if self.transform is not None else "schema"

    def generate(self, count: int | None = None) -> list[TrainingPair]:
        count = self._resolve_count(count)
        rng = random.Random(self.seed)
        pairs: list[TrainingPair] = []
        for index in range(count):
            input_value = self.input_schema.generate(rng)
            output_value = self._generate_output(input_value, rng)
            if self.output_schema is not None:
                self.output_schema.validate(output_value)
            pairs.append(TrainingPair(input=input_value, output=output_value, index=index))
        return pairs

    def iter_pairs(self, count: int | None = None) -> Iterable[TrainingPair]:
        return iter(self.generate(count))

    def to_spec(self) -> dict[str, Any]:
        return {
            "seed": _encode_json(self.seed),
            "count": self.count,
            "input_schema": self.input_schema.to_spec(),
            "output_schema": self.output_schema.to_spec() if self.output_schema is not None else None,
            "transform": self.transform_spec.to_spec() if self.transform_spec is not None else None,
        }

    @classmethod
    def from_spec(
        cls,
        spec: Mapping[str, Any],
        transform: Callable[..., JSONValue] | None = None,
    ) -> "TrainingDataGenerator":
        if not isinstance(spec, Mapping):
            raise TrainingDataError("Generator spec must be a mapping.")
        input_schema = spec.get("input_schema")
        if not isinstance(input_schema, Mapping):
            raise TrainingDataError("Generator spec requires an input_schema mapping.")
        output_schema = spec.get("output_schema")
        if output_schema:
            return cls(
                input_schema=SchemaNode.from_spec(input_schema),
                output_schema=SchemaNode.from_spec(output_schema),
                count=spec.get("count"),
                seed=spec.get("seed", 42),
                transform=transform,
                transform_spec=spec.get("transform"),
            )
        if transform is None:
            raise TrainingDataError("Generator spec requires an output_schema or transform.")
        return cls(
            input_schema=SchemaNode.from_spec(input_schema),
            output_schema=transform,
            count=spec.get("count"),
            seed=spec.get("seed", 42),
            transform_spec=spec.get("transform"),
        )

    def write_json(self, path: str | Path, count: int | None = None, *, indent: int = 2) -> Path:
        records = [pair.to_record() for pair in self.generate(count)]
        target = Path(path)
        target.write_text(json.dumps(records, indent=indent, ensure_ascii=False), encoding="utf-8")
        return target

    def write_jsonl(self, path: str | Path, count: int | None = None) -> Path:
        target = Path(path)
        with target.open("w", encoding="utf-8", newline="\n") as handle:
            for pair in self.generate(count):
                handle.write(json.dumps(pair.to_record(), ensure_ascii=False, separators=(",", ":")))
                handle.write("\n")
        return target

    def write_csv(self, path: str | Path, count: int | None = None) -> Path:
        records = self.generate(count)
        if not records:
            raise TrainingDataError("Cannot export an empty dataset to CSV.")

        flattened_rows = [_flatten_pair(pair) for pair in records]
        headers = list(flattened_rows[0].keys())
        for row in flattened_rows[1:]:
            if list(row.keys()) != headers:
                raise TrainingDataError("CSV export requires a stable record shape.")

        target = Path(path)
        with target.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=headers)
            writer.writeheader()
            for row in flattened_rows:
                writer.writerow({key: _csv_cell(value) for key, value in row.items()})
        return target

    def _resolve_count(self, count: int | None) -> int:
        if count is None:
            if self.count is None:
                raise TrainingDataError("Dataset count is required.")
            return self.count
        return _validate_size("count", count)

    def _generate_output(self, input_value: JSONValue, rng: random.Random) -> JSONValue:
        if self.transform is None:
            if self.output_schema is None:
                raise TrainingDataError("Output schema is required when no transform is provided.")
            return self.output_schema.generate(rng)
        if self._transform_mode == "rng_keyword":
            return self.transform(input_value, rng=rng)
        if self._transform_mode == "rng_positional":
            return self.transform(input_value, rng)
        return self.transform(input_value)


def integer(min: int = 0, max: int = 99) -> SchemaNode:
    _validate_range(min, max)
    return SchemaNode("integer", {"min": min, "max": max})


def number(min: float = 0.0, max: float = 1.0, precision: int | None = None) -> SchemaNode:
    _validate_range(min, max)
    params: dict[str, Any] = {"min": min, "max": max}
    if precision is not None:
        if precision < 0:
            raise TrainingDataError("Precision must be non-negative.")
        params["precision"] = precision
    return SchemaNode("number", params)


def boolean(probability: float = 0.5) -> SchemaNode:
    return SchemaNode("boolean", {"probability": probability})


def string(length: int = 12, alphabet: str | None = None) -> SchemaNode:
    params: dict[str, Any] = {"length": _validate_size("length", length)}
    if alphabet is not None:
        if not alphabet:
            raise TrainingDataError("String alphabet must not be empty.")
        params["alphabet"] = alphabet
    return SchemaNode("string", params)


def choice(options: Sequence[Any]) -> SchemaNode:
    return SchemaNode("choice", {"options": _validate_items(options)})


def array_schema(
    items: SchemaLike,
    *,
    length: int | None = 1,
    min_length: int = 0,
    max_length: int = 3,
) -> SchemaNode:
    params: dict[str, Any] = {"items": ensure_schema(items)}
    if length is not None:
        params["length"] = _validate_size("length", length)
    else:
        _validate_range(min_length, max_length)
        params["min_length"] = min_length
        params["max_length"] = max_length
    return SchemaNode("array", params)


def object_schema(properties: Mapping[str, SchemaLike]) -> SchemaNode:
    if not isinstance(properties, Mapping):
        raise TrainingDataError("Object schema properties must be a mapping.")
    return SchemaNode("object", {"properties": {name: ensure_schema(schema) for name, schema in properties.items()}})


def null() -> SchemaNode:
    return SchemaNode("null")


def literal(value: Any) -> SchemaNode:
    _ensure_json_native(value)
    return SchemaNode("literal", {"value": value})


def one_of(options: Sequence[SchemaLike]) -> SchemaNode:
    return SchemaNode("one_of", {"options": [ensure_schema(option) for option in options]})


def transform_spec(name: str, **params: Any) -> TransformSpec:
    return TransformSpec(name=name, params=params)


def ensure_schema(value: SchemaLike | None) -> SchemaNode:
    if isinstance(value, SchemaNode):
        return value
    if isinstance(value, Mapping) and set(value.keys()) <= {"kind", "params"} and "kind" in value:
        return SchemaNode.from_spec(value)
    if isinstance(value, Mapping):
        return object_schema(value)
    raise TrainingDataError("Schema value must be a SchemaNode or mapping.")


def _coerce_transform_spec(
    value: TransformSpec | Mapping[str, Any] | str | None,
) -> TransformSpec | None:
    if value is None:
        return None
    if isinstance(value, TransformSpec):
        return value
    if isinstance(value, str):
        return TransformSpec(name=value)
    if isinstance(value, Mapping):
        if "name" not in value:
            raise TrainingDataError("Transform spec mappings require a name field.")
        params = value.get("params", {})
        if not isinstance(params, Mapping):
            raise TrainingDataError("Transform spec params must be a mapping.")
        return TransformSpec(name=str(value["name"]), params=_decode_json(dict(params)))
    raise TrainingDataError("Unsupported transform spec value.")


def _detect_transform_mode(transform: Callable[..., JSONValue]) -> str:
    try:
        signature = inspect.signature(transform)
    except (TypeError, ValueError):
        return "single"

    params = list(signature.parameters.values())
    positional_count = sum(
        1
        for param in params
        if param.kind in {inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD}
    )
    has_rng_keyword = any(param.name == "rng" for param in params)
    has_var_positional = any(param.kind == inspect.Parameter.VAR_POSITIONAL for param in params)
    has_var_keyword = any(param.kind == inspect.Parameter.VAR_KEYWORD for param in params)

    if has_rng_keyword or has_var_keyword:
        return "rng_keyword"
    if positional_count >= 2 or has_var_positional:
        return "rng_positional"
    return "single"


def _flatten_pair(pair: TrainingPair) -> dict[str, Any]:
    flattened: dict[str, Any] = {}
    _flatten_value(pair.input, "input", flattened)
    _flatten_value(pair.output, "output", flattened)
    return flattened


def _flatten_value(value: Any, prefix: str, target: dict[str, Any]) -> None:
    _ensure_json_native(value)
    if isinstance(value, Mapping):
        if not value:
            target[prefix] = {}
            return
        for key, nested in value.items():
            child_prefix = f"{prefix}.{key}" if prefix else str(key)
            _flatten_value(nested, child_prefix, target)
        return
    if isinstance(value, list):
        if not value:
            target[prefix] = []
            return
        for index, nested in enumerate(value):
            child_prefix = f"{prefix}[{index}]"
            _flatten_value(nested, child_prefix, target)
        return
    target[prefix] = value


def _csv_cell(value: Any) -> Any:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return value


def _validate_against_schema(schema: SchemaNode, value: Any) -> None:
    kind = schema.kind
    params = schema.params

    if kind == "integer":
        if isinstance(value, bool) or not isinstance(value, int):
            raise TrainingDataError("Value does not match integer schema.")
        return

    if kind == "number":
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TrainingDataError("Value does not match number schema.")
        return

    if kind == "boolean":
        if not isinstance(value, bool):
            raise TrainingDataError("Value does not match boolean schema.")
        return

    if kind == "string":
        if not isinstance(value, str):
            raise TrainingDataError("Value does not match string schema.")
        expected_length = params.get("length")
        if expected_length is not None and len(value) != int(expected_length):
            raise TrainingDataError("String value does not match expected length.")
        return

    if kind == "choice":
        if value not in params.get("options", []):
            raise TrainingDataError("Value is not one of the allowed choices.")
        return

    if kind == "array":
        if not isinstance(value, list):
            raise TrainingDataError("Value does not match array schema.")
        item_schema = ensure_schema(params["items"])
        expected_length = params.get("length")
        if expected_length is not None and len(value) != int(expected_length):
            raise TrainingDataError("Array value does not match expected length.")
        for item in value:
            item_schema.validate(item)
        return

    if kind == "object":
        if not isinstance(value, Mapping):
            raise TrainingDataError("Value does not match object schema.")
        properties = params.get("properties", {})
        if set(value.keys()) != set(properties.keys()):
            raise TrainingDataError("Object value does not match expected keys.")
        for key, sub_schema in properties.items():
            ensure_schema(sub_schema).validate(value[key])
        return

    if kind == "null":
        if value is not None:
            raise TrainingDataError("Value does not match null schema.")
        return

    if kind == "literal":
        if value != params.get("value"):
            raise TrainingDataError("Value does not match literal schema.")
        return

    if kind == "one_of":
        schemas = [ensure_schema(option) for option in params.get("options", [])]
        for option in schemas:
            try:
                option.validate(value)
                return
            except TrainingDataError:
                continue
        raise TrainingDataError("Value does not match any allowed schema option.")

    raise TrainingDataError(f"Unsupported schema kind: {kind}")


def _encode_json(value: Any) -> Any:
    if isinstance(value, SchemaNode):
        return value.to_spec()
    if isinstance(value, TransformSpec):
        return value.to_spec()
    if isinstance(value, Mapping):
        return {str(key): _encode_json(nested) for key, nested in value.items()}
    if isinstance(value, list):
        return [_encode_json(item) for item in value]
    _ensure_json_native(value)
    return value


def _decode_json(value: Any) -> Any:
    if isinstance(value, Mapping) and set(value.keys()) <= {"kind", "params"} and "kind" in value:
        return SchemaNode.from_spec(value)
    if isinstance(value, Mapping):
        return {str(key): _decode_json(nested) for key, nested in value.items()}
    if isinstance(value, list):
        return [_decode_json(item) for item in value]
    return value


def _ensure_json_native(value: Any) -> None:
    if value is None or isinstance(value, (str, int, float, bool)):
        return
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if not isinstance(key, str):
                raise TrainingDataError("JSON object keys must be strings.")
            _ensure_json_native(nested)
        return
    if isinstance(value, list):
        for nested in value:
            _ensure_json_native(nested)
        return
    raise TrainingDataError(f"Value is not JSON-native: {type(value).__name__}")


def _validate_range(min_value: Any, max_value: Any) -> None:
    if min_value > max_value:
        raise TrainingDataError("Invalid range: min must be less than or equal to max.")


def _validate_size(name: str, value: Any) -> int:
    if not isinstance(value, int) or value < 0:
        raise TrainingDataError(f"Invalid size: {name} must be a non-negative integer.")
    return value


def _validate_items(items: Sequence[Any] | None) -> list[Any]:
    if items is None:
        raise TrainingDataError("Items are required.")
    if not isinstance(items, Sequence) or isinstance(items, (str, bytes)) or not items:
        raise TrainingDataError("Items must be a non-empty sequence.")
    normalized = list(items)
    for item in normalized:
        _ensure_json_native(item)
    return normalized


__all__ = [
    "TrainingDataError",
    "SchemaNode",
    "TransformSpec",
    "TrainingPair",
    "TrainingDataGenerator",
    "integer",
    "number",
    "boolean",
    "string",
    "choice",
    "array_schema",
    "object_schema",
    "null",
    "literal",
    "one_of",
    "transform_spec",
    "ensure_schema",
]
