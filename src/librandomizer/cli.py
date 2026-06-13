"""JSON command line interface for libRandomizer."""

from __future__ import annotations

import argparse
import base64
import json
import sys
from typing import Any, Sequence

from .core import LibRandom, _CATALOG, _api_name, _snake_name


class CliUsageError(ValueError):
    """Raised when command line arguments are invalid."""


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise CliUsageError(message)


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    try:
        args = parser.parse_args(argv)
        generator = LibRandom()
        value = _generate_value(generator, args)
    except (CliUsageError, ValueError, TypeError) as exc:
        _write_json({"error": str(exc)}, stream=sys.stderr)
        return 1

    _write_json({"type": args.random_type, "value": _json_safe(value)})
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = JsonArgumentParser(
        prog="librandom",
        description="Generate v1 public beta random values as JSON.",
    )
    subparsers = parser.add_subparsers(
        dest="random_type",
        parser_class=JsonArgumentParser,
        required=True,
    )

    for entry in _CATALOG.get("types", []):
        subparser = subparsers.add_parser(entry["id"], help=entry["description"])
        for param in entry.get("parameters", []):
            arg_type = _arg_type(param["type"])
            default = param.get("default")
            subparser.add_argument(
                f"--{param['name']}",
                type=arg_type,
                default=default,
                required=bool(param.get("required") and default is None),
            )

    return parser


def _arg_type(type_name: str) -> Any:
    if type_name in {"integer"}:
        return int
    if type_name in {"float", "number", "decimal"}:
        return float
    if type_name == "boolean":
        return _bool_arg
    if type_name == "array":
        return json.loads
    return str


def _bool_arg(value: str) -> bool:
    lowered = value.lower()
    if lowered in {"1", "true", "yes", "on"}:
        return True
    if lowered in {"0", "false", "no", "off"}:
        return False
    raise CliUsageError(f"invalid boolean value: {value!r}")


def _generate_value(generator: LibRandom, args: argparse.Namespace) -> Any:
    entry = next((item for item in _CATALOG.get("types", []) if item["id"] == args.random_type), None)
    if entry is None:
        raise ValueError(f"Unsupported random type: {args.random_type}")
    options = {
        param["name"]: getattr(args, param["name"])
        for param in entry.get("parameters", [])
        if hasattr(args, param["name"])
    }
    return getattr(generator, _snake_name(_api_name(entry)))(**options)


def _json_safe(value: Any) -> Any:
    if isinstance(value, bytes):
        return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")
    return value


def _write_json(payload: dict[str, Any], stream: Any = sys.stdout) -> None:
    print(json.dumps(payload, separators=(",", ":")), file=stream)


if __name__ == "__main__":
    raise SystemExit(main())
