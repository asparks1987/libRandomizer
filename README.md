# libRandomizer

`libRandomizer` is a portable training-data generator for simple prediction
networks. You define the datatype or schema for the input, define the datatype
or schema for the output, choose a fixed record count, and set a seed. The SDK
then produces a reproducible list of input/output training pairs.

The Python package is the reference implementation. Its schema contract is
JSON-native so the same dataset definition can be carried across language
targets without depending on opaque Python objects.

## Install

```bash
python -m pip install .
```

## Quickstart

```python
from librandomizer import TrainingDataGenerator, choice, integer

generator = TrainingDataGenerator(
    input_schema=integer(0, 99),
    output_schema=choice(["low", "medium", "high"]),
    count=100,
    seed=42,
)

pairs = generator.generate()
```

Each generated record has the same language-neutral shape:

```json
{
  "input": 81,
  "output": "low"
}
```

Calling the same generator again with the same schema, count, and seed produces
the same records in the same order.

## Derived Outputs

Most datasets can be generated from separate input and output schemas. When a
target should be calculated from the input, pass a transform callback and keep
an `output_schema` so the result can be validated and serialized consistently.

```python
from librandomizer import TrainingDataGenerator, integer, number

generator = TrainingDataGenerator(
    input_schema=integer(0, 10),
    output_schema=number(0, 20),
    count=100,
    seed=42,
    transform=lambda value: value * 2,
)

pairs = generator.generate()
```

This is useful for labels, thresholds, regression targets, boolean decisions,
and other predictable outputs for supervised learning examples.

## Schema Helpers

The v1 schema layer focuses on portable JSON-native datatypes:

| Helper | Purpose |
| --- | --- |
| `integer(min, max)` | Bounded integer values |
| `number(min, max, precision=None)` | Bounded floating point values |
| `boolean()` | `true` or `false` values |
| `string(length=8, alphabet=None)` | Fixed-length strings |
| `choice(values)` | One value from a finite set |
| `array_schema(items, length)` | Fixed-length arrays |
| `object_schema(properties)` | Nested JSON objects |
| `null()` | Explicit `null` values |
| `literal(value)` | A fixed serializable value |
| `one_of(schemas)` | A deterministic choice among schema variants |

Schemas can be nested:

```python
from librandomizer import boolean, integer, object_schema, string

input_schema = object_schema({
    "profile": object_schema({
        "age": integer(18, 65),
        "active": boolean(),
    }),
    "plan": string(length=6),
})
```

## Generator API

```python
TrainingDataGenerator(
    input_schema,
    output_schema,
    *,
    count=None,
    seed=42,
    transform=None,
    transform_spec=None,
)
```

- `input_schema` describes the generated input side of each pair.
- `output_schema` describes the generated output side, or validates transform
  results when a transform is supplied.
- `count` is the default number of pairs produced by `generate()` and export
  methods.
- `seed` controls deterministic generation.
- `transform` is optional and receives one generated input value.
- `transform_spec` is optional serializable metadata for cross-language specs.

## Exports

```python
generator.write_json("train.json")
generator.write_jsonl("train.jsonl")
generator.write_csv("train.csv")
```

JSON preserves the full nested record structure. JSONL is convenient for
streaming and line-oriented tooling. CSV flattens nested records into stable
columns such as `input.profile.age`, `input.features[0]`, and `output.score`.

## Portable Specs

Generators can be serialized as a spec:

```python
spec = generator.to_spec()
restored = TrainingDataGenerator.from_spec(spec)
```

Specs include the seed, count, input schema, output schema, and optional
transform metadata. Host-language callback code is intentionally not serialized;
portable transforms should be represented by a named `transform_spec` and bound
to native code in each SDK.

## Reproducibility Guarantees

The same implementation must produce identical datasets for the same:

- input schema
- output schema
- seed
- count
- transform behavior, when a transform is used

Different seeds should change generated inputs while preserving schema validity.
Exports are deterministic so generated JSON, JSONL, and CSV files can be used
in tests, demos, examples, and repeatable training experiments.

## Legacy Compatibility

The original OS-backed random primitive APIs remain available as compatibility
shims while the training-data generator becomes the primary product. New code
should use `TrainingDataGenerator` and the portable schema helpers.

## Documentation

The GitHub Pages site lives in `docs/`. Start with `docs/index.html` for the
developer-facing overview, then see `spec/training/README.md` for the portable
schema contract.

## Tests

```bash
python -m unittest discover tests
```
