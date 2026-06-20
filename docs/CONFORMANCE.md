# libRandomizer Conformance

Conformance proves that an SDK generates the same portable training-data shape
for the same schema, seed, and count.

## Required Coverage

Each implementation should prove:

- valid input schemas generate values with the documented type and bounds;
- valid output schemas generate values with the documented type and bounds;
- invalid schemas fail clearly before generation;
- invalid `count` values fail clearly;
- the same seed, schemas, and count produce identical records;
- different seeds change generated values while preserving schema validity;
- optional transforms produce deterministic outputs for deterministic inputs;
- transform outputs are validated against `output_schema`;
- JSON, JSONL, and CSV exports are deterministic;
- nested arrays and objects are serialized consistently.

## Language Targets

The repo's long-term direction is a shared high-level concept across existing
language targets:

- Python
- JavaScript
- TypeScript
- Java
- C#
- C
- C++
- PHP
- Go
- Rust
- Kotlin
- Swift
- Ruby
- Dart
- R

The Python SDK is currently the reference implementation. Other languages should
match the same serialized schema/spec contract even when helper names or
callback syntax are idiomatic to that language.

## Test Shape

Each language should have:

- package build test;
- local install/import smoke test;
- schema construction smoke test;
- generator smoke test for schema-only pairs;
- generator smoke test for transform-derived outputs;
- shared conformance cases for primitive and nested schemas;
- export checks for every supported file format.

## Status Rule

A language surface can claim training-data parity only when it can generate and
serialize the same language-neutral record shapes for the same shared specs.

Legacy random primitive APIs have separate compatibility expectations and should
not be treated as the product's primary conformance target.
