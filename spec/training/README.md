# Training Data Schema Contract

`libRandomizer`'s training-data layer is built around a portable schema,
deterministic generation, and input/output records for supervised learning.

## Core Concepts

- `input_schema`: a serializable schema that describes the generated input
  value for each pair.
- `output_schema`: a serializable schema that describes the generated output
  value for each pair.
- `count`: the fixed number of training pairs to generate.
- `seed`: a deterministic seed for reproducible record generation.
- `transform`: an optional host-language callback that derives one output from
  one generated input. When present, the output is still validated against
  `output_schema`.

Schema-only generation is the default workflow: both input and output values are
generated from their schemas. Transforms are for labels, scores, decisions, or
other outputs that should be reproducible functions of the input.

## Supported Schema Kinds

- `integer`
- `number`
- `boolean`
- `string`
- `choice`
- `array`
- `object`
- `null`
- `literal`
- `one_of`

## Serialized Shape

Schemas are exported as JSON objects like:

```json
{
  "kind": "object",
  "params": {
    "properties": {
      "age": {
        "kind": "integer",
        "params": {
          "min": 18,
          "max": 65
        }
      }
    }
  }
}
```

Generator specs are exported as JSON objects like:

```json
{
  "seed": 42,
  "count": 100,
  "input_schema": {
    "kind": "integer",
    "params": {
      "min": 0,
      "max": 99
    }
  },
  "output_schema": {
    "kind": "choice",
    "params": {
      "values": ["low", "medium", "high"]
    }
  },
  "transform": null
}
```

Host-language callback code is not serialized. Portable transform behavior
should be represented by named metadata in `transform_spec` and bound to native
code in each SDK.

## Record Shape

Generated records are language-neutral input/output pairs:

```json
{
  "input": 81,
  "output": "low"
}
```

## Conformance Expectations

Compatible implementations should prove:

- same seed, count, input schema, and output schema produce identical datasets;
- different seeds change generated inputs while preserving schema validity;
- transforms are deterministic for the same generated inputs;
- generated outputs validate against `output_schema`;
- JSON, JSONL, and CSV serialization are deterministic;
- nested arrays and objects round-trip through supported exports where possible.

The Python reference SDK produces the schema and serialization rules. Other
languages can implement the same portable contract using their local callback
style and native serializers.
