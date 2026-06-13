# libRandomizer SDK Packages

Each directory contains a native SDK target for the shared V1 public beta
catalog. Every package exposes the generated 138-function `randomX()` surface
plus natural `getRandomX()` aliases where the language supports them.

| Directory | Language | Primary call |
| --- | --- | --- |
| `python` | Python | `random_int()` / `randomInt()` |
| `javascript` | JavaScript | `randomInt()` |
| `typescript` | TypeScript | `randomInt()` |
| `java` | Java | `LibRandomizer.randomInt()` |
| `csharp` | C# | `Randomizer.RandomInt()` |
| `c` | C | `librandom_random_int()` |
| `cpp` | C++ | `librandom::randomInt()` |
| `php` | PHP | `LibRandomizer\\randomInt()` |
| `go` | Go | `RandomInt()` |
| `rust` | Rust | `random_int()` |
| `kotlin` | Kotlin | `randomInt()` |
| `swift` | Swift | `LibRandomizer.randomInt()` |
| `ruby` | Ruby | `LibRandomizer.randomInt()` |
| `dart` | Dart | `randomInt()` |
| `r` | R | `random_int()` |
