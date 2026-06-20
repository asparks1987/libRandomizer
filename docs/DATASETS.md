# libRandomizer Dataset And Type Policy

`libRandomizer` is currently centered on generated JSON-native input/output
training pairs, not large bundled real-world datasets. This policy describes how
types and optional dataset-backed values should behave.

## Default Type Generation

The primary schema helpers generate values from deterministic seeded algorithms:

- bounded integers;
- bounded numbers;
- booleans;
- fixed-length strings;
- arrays;
- objects;
- nulls;
- literals;
- finite choices;
- one-of unions.

These values are portable because they serialize naturally as JSON and can be
flattened into CSV when needed.

## Dataset-Backed Values

Future dataset-backed helpers, such as names, places, domain terms, or sample
text, must document:

- source name and URL or local origin;
- license and compatibility with MIT distribution;
- update policy;
- locale coverage;
- safety policy;
- fields and return shape used by SDKs;
- deterministic sampling behavior under a seed.

## Safe Defaults

Any human-readable corpus must be safe by default. Adult or profane values may
only appear through explicit opt-in options and must never be returned from
default training-data generation.

## Storage Format

Portable JSON is preferred for shared datasets so every SDK can consume the same
source data or generate equivalent native bundles.

Recommended layout for future datasets:

```text
datasets/
  text/
  people/
  location/
  internet/
  commerce/
  developer/
```

## Acceptance Gate

No dataset-backed helper should be documented as production-ready until its
source, license, safety mode, locale policy, and seeded selection behavior are
documented and tested.
