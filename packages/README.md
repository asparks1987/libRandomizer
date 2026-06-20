# libRandomizer SDK Packages

Each directory contains a native SDK target for the shared V1 public beta
catalog. Every package exposes the generated 138-function `randomX()` surface
plus natural `getRandomX()` aliases where the language supports them.

| Directory | Language | Primary call | Current beta completeness |
| --- | --- | --- | --- |
| `python` | Python | `random_int()` / `randomInt()` | Behavior-complete reference |
| `javascript` | JavaScript | `randomInt()` | Generated surface only |
| `typescript` | TypeScript | `randomInt()` | Generated surface only |
| `java` | Java | `LibRandomizer.randomInt()` | Generated surface only |
| `csharp` | C# | `Randomizer.RandomInt()` | Generated surface only |
| `c` | C | `librandom_random_int()` | Generated surface only |
| `cpp` | C++ | `librandom::randomInt()` | Generated surface only |
| `php` | PHP | `LibRandomizer\\randomInt()` | Generated surface only |
| `go` | Go | `RandomInt()` | Generated surface only |
| `rust` | Rust | `random_int()` | Generated surface only |
| `kotlin` | Kotlin | `randomInt()` | Generated surface only |
| `swift` | Swift | `LibRandomizer.randomInt()` | Generated surface only |
| `ruby` | Ruby | `LibRandomizer.randomInt()` | Generated surface only |
| `dart` | Dart | `randomInt()` | Generated surface only |
| `r` | R | `random_int()` | Generated surface only |
