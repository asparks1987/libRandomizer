# SDK Parity Status (V1 Beta)

**Last updated:** 2026-06-19

This matrix tracks implementation confidence for the v1 beta milestone where
`TrainingDataGenerator` is the reference feature set.

## Status legend

- `reference-complete`: behavior-complete against the shared catalog and conformance fixtures.
- `surface-only`: generated API surface exists; behavior parity is not fully proven.
- `blocked`: language/toolchain unavailable locally or requires parity hardening.

## Current status

| Language | Package | SDK status | Notes |
| --- | --- | --- | --- |
| Python | `packages/python` | reference-complete | Primary source of truth |
| JavaScript | `packages/javascript` | surface-only | API surface generated; conformance hardening needed |
| TypeScript | `packages/typescript` | surface-only | API surface generated; conformance hardening needed |
| Go | `packages/go` | surface-only | API surface generated; conformance hardening needed |
| C# | `packages/csharp` | surface-only | API surface generated; conformance hardening needed |
| Java | `packages/java` | surface-only | API surface generated; conformance hardening needed |
| Rust | `packages/rust` | surface-only | API surface generated; conformance hardening needed |
| PHP | `packages/php` | surface-only | API surface generated; conformance hardening needed |
| Ruby | `packages/ruby` | surface-only | API surface generated; conformance hardening needed |
| Kotlin | `packages/kotlin` | surface-only | API surface generated; conformance hardening needed |
| Swift | `packages/swift` | surface-only | API surface generated; conformance hardening needed |
| Dart | `packages/dart` | surface-only | API surface generated; conformance hardening needed |
| R | `packages/r` | blocked | Toolchain not available in this environment; parity status pending |
| C | `packages/c` | blocked | Package generated/build artifacts exist; parity harness not yet run |
| C++ | `packages/cpp` | blocked | Package generated/build artifacts exist; parity harness not yet run |

## Next pass priority

1. JavaScript/TypeScript
2. Go
3. C#
4. Java
5. Rust
6. C/C++
7. PHP
8. Ruby
9. Kotlin
10. Swift
11. Dart
12. R

We will promote a language to `reference-complete` equivalent status only after:

- deterministic generator parity for supported schemas and options,
- invalid input/error behavior parity,
- JSON/JSONL/CSV export parity,
- and package/build verification with available toolchains.
