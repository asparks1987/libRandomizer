# libRandomizer Conformance

Conformance proves that every language package matches the shared catalog
contract.

## Required Coverage

Each SDK must prove:

- default calls return the documented type
- bounded calls stay within range
- equal boundaries return the boundary
- invalid ranges fail clearly
- invalid character inputs fail clearly
- size options reject unsupported negative or oversized values
- collection functions reject invalid item/weight combinations
- safe text mode is default
- adult/profane text appears only with explicit opt-in
- dataset-backed values use documented datasets or equivalent native bundles

## Language Targets

The production beta matrix includes:

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

## Test Shape

Each language should have:

- package build test
- local install/import smoke test
- call smoke test for every catalog API
- shared conformance cases generated from `spec/beta/output-types.json`
- negative tests for invalid options

## Status Rule

A catalog type can move to `implemented-python` when the Python SDK and CLI pass
the shared cases for that type.

A catalog type can move to `implemented-all` only when every language target
passes its conformance cases.
