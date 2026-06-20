# libRandomizer Product Scope

This document defines the current product direction for `libRandomizer`.

## Product Goal

`libRandomizer` should let developers generate deterministic input/output
training pairs for simple prediction networks:

```text
input schema + output schema + count + seed => reproducible training pairs
```

The SDK is designed for demos, tests, tutorials, smoke training runs, and small
synthetic datasets where repeatability matters more than realism.

## Primary Workflow

Developers should be able to:

- define the datatype or schema for each generated input;
- define the datatype or schema for each generated output;
- choose an exact dataset size with `count`;
- choose a deterministic `seed`;
- optionally derive outputs from inputs with a transform callback;
- export the same dataset as JSON, JSONL, or CSV.

## V1 Reference Implementation

The Python package is the reference implementation for:

- schema validation;
- seeded record generation;
- input/output pair generation;
- transform result validation;
- deterministic JSON, JSONL, and CSV serialization;
- portable generator specs.

### Parity Policy (V1 Beta)

For this release, we are using a two-tier parity model:

- `Python + CLI`: behavior-complete reference implementation.
- all other SDKs: generated API surfaces, with behavior still in hardening and
  conformance status tracking.

Until a language passes shared conformance cases, it must not be presented as
behavior-parity complete, even if the full function surface is present.

Status terms in this repo mean:

- `implemented-python`: function is implemented with behavior parity in Python/CLI.
- `implemented-all`: all non-Python language SDKs have passing shared conformance
  for that behavior and are safe to treat as parity-complete.
- `planned-beta`: function remains on path but not yet fully covered yet.

The web and API docs must make this distinction visible so users know exactly what
is production-safe behavior for the chosen target language.

## Supported Portable Types

V1 focuses on JSON-native values that can map cleanly into many programming
languages:

- integers;
- numbers;
- booleans;
- strings;
- arrays;
- objects;
- nulls;
- literal values;
- finite choices;
- one-of schema unions.

## Cross-Language Direction

"Portable" means the shared contract is data-first. Schemas and generator specs
must be serializable, while each language target can expose idiomatic helpers
and native callback syntax.

The repo may keep generated surfaces for existing language targets, but the
Python implementation is the source of truth until parity work is complete.

## Out Of Scope For V1

V1 does not promise:

- arbitrary opaque host-language objects;
- realistic domain datasets for every industry;
- every possible programming language ecosystem;
- cryptographic randomness as the primary behavior;
- nondeterministic wall-clock or OS-random training runs by default;
- a full neural network training framework.

## Legacy Compatibility

The older random primitive catalog remains compatibility surface area. It should
not be the main documentation path for new users. New examples and product copy
should lead with `TrainingDataGenerator` and portable schemas.
