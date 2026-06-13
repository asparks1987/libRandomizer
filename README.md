# libRandomizer

`libRandomizer` is a language-agnostic randomization SDK project. The goal is
simple: import the package in the language you are already using, call one
small function, and get an OS-backed random value.

```c
int thisINT = randomInt();
```

The current v1 implementation focuses on three primitive output types:
integers, floats, and printable ASCII characters. The beta documentation expands
the product roadmap with 138 planned output types so the SDK can grow toward
random data of almost any kind while keeping the same direct API style.

## Current Status

This repository is beta-ready for the v1 foundation:

- Python reference SDK with top-level functions, class compatibility, and CLI
- Native package targets for 15 languages under `packages/`
- Shared v1 behavior contract in `spec/v1`
- Beta output-type catalog in `spec/beta`
- GitHub-dark documentation site in `docs/`
- Unit tests, CLI tests, package layout checks, and beta catalog checks

Important distinction: v1 functions are implemented for the current primitive
scope. The beta catalog is documentation-first and marks the larger API surface
the SDK should implement over time.

## What Works Today

| Type | Default call | Default range | Bounded call |
| --- | --- | --- | --- |
| Integer | `randomInt()` | `0..99` | `randomInt(min, max)` |
| Float | `randomFloat()` | `0.0..1.0` | `randomFloat(min, max)` |
| Character | `randomChar()` | `"A".."Z"` | `randomChar(min, max)` |

Language-specific casing is supported where it is idiomatic. For example,
Python exposes `random_int()`, Go exposes `RandomInt()`, and C exposes
`random_int()`.

## Randomness Model

v1 uses operating-system cryptographic randomness through each platform's secure
random API. It does not seed from time and it does not use deterministic
pseudo-random generators for SDK values.

For this project, "true random" currently means practical OS-backed CSPRNG
randomness for local and server-side software. It does not require a hardware
random number generator or a hosted randomness service.

## Install The Python SDK

The Python package is the reference implementation and can be installed from the
repository root.

```bash
python -m pip install .
```

For local development, install it editable with test/build tools:

```bash
python -m pip install -e ".[dev]"
```

## Python Usage

Use top-level functions for the simplest API:

```python
from librandomizer import random_int, random_float, random_char

value = random_int()
score = random_int(10, 20)
ratio = random_float()
letter = random_char("A", "F")
```

Camel-case aliases are available when you want the cross-language shape:

```python
from librandomizer import randomInt, randomFloat, randomChar

value = randomInt()
ratio = randomFloat(0.25, 0.75)
letter = randomChar("A", "Z")
```

The older class-first API still works for compatibility:

```python
from libRandom import LibRandom

randomizer = LibRandom()
value = randomizer.random_int(min=0, max=99)
```

Legacy method aliases are also supported:

```python
value = LibRandom().get_random_int(0, 99)
```

## CLI Usage

The CLI is useful for shell scripts, smoke tests, or languages that do not yet
have a packaged SDK installed.

```bash
librandom int --min 0 --max 99
librandom float --min 0.0 --max 1.0
librandom char --min A --max Z
```

Successful output is compact JSON:

```json
{"type":"int","value":42}
```

Invalid input returns a non-zero exit code and writes JSON to stderr:

```json
{"error":"Invalid range: min must be less than or equal to max"}
```

## Validation Rules

All SDKs should follow the same v1 behavior:

- integer ranges are inclusive
- character ranges are inclusive
- float ranges use the platform's secure random float behavior within the
  requested bounds
- `min` must be less than or equal to `max`
- equal boundaries return that exact boundary
- characters must be single printable ASCII characters
- invalid input fails clearly using the language's normal error style

## 15 Language Targets

The monorepo contains native package targets for these languages. Some are
package-ready skeletons and examples, while the Python SDK is the reference
implementation used for the main package/build checks.

| Language | Location | Example call |
| --- | --- | --- |
| Python | `packages/python` | `random_int()` / `randomInt()` |
| JavaScript | `packages/javascript` | `randomInt()` |
| TypeScript | `packages/typescript` | `randomInt()` |
| Java | `packages/java` | `LibRandomizer.randomInt()` |
| C# | `packages/csharp` | `Randomizer.RandomInt()` |
| C | `packages/c` | `random_int()` |
| C++ | `packages/cpp` | `librandom::randomInt()` |
| PHP | `packages/php` | `LibRandomizer\randomInt()` |
| Go | `packages/go` | `RandomInt()` |
| Rust | `packages/rust` | `random_int()` |
| Kotlin | `packages/kotlin` | `randomInt()` |
| Swift | `packages/swift` | `LibRandomizer.randomInt()` |
| Ruby | `packages/ruby` | `LibRandomizer.random_int()` |
| Dart | `packages/dart` | `randomInt()` |
| R | `packages/r` | `random_int()` / `randomInt()` |

## Quick Examples By Language

Python:

```python
from librandomizer import random_int

value = random_int()
```

JavaScript:

```javascript
const { randomInt } = require("@librandomizer/javascript");

const value = randomInt();
```

TypeScript:

```typescript
import { randomInt } from "@librandomizer/typescript";

const value = randomInt();
```

Java:

```java
import static io.github.librandomizer.LibRandomizer.randomInt;

int value = randomInt();
```

C#:

```csharp
using static LibRandomizer.Randomizer;

int value = RandomInt();
```

C:

```c
#include "librandom.h"

int value = random_int();
```

C++:

```cpp
#include <librandom/random.hpp>

int value = librandom::randomInt();
```

PHP:

```php
use function LibRandomizer\randomInt;

$value = randomInt();
```

Go:

```go
import "github.com/asparks1987/librandomizer/packages/go"

value := librandomizer.RandomInt()
```

Rust:

```rust
use librandomizer::random_int;

let value = random_int();
```

Kotlin:

```kotlin
import io.github.librandomizer.LibRandomizer.randomInt

val value = randomInt()
```

Swift:

```swift
import LibRandomizer

let value = LibRandomizer.randomInt()
```

Ruby:

```ruby
require "librandomizer"

value = LibRandomizer.random_int
```

Dart:

```dart
import 'package:librandomizer/librandomizer.dart';

final value = randomInt();
```

R:

```r
library(librandomizer)

value <- random_int()
```

## Beta Output Catalog

The beta catalog in `spec/beta/output-types.json` currently defines 138 output
types across 14 categories:

- Core primitives
- Identifiers
- Numbers
- Text
- People
- Internet
- Color
- Location
- Date and time
- Commerce
- Games
- Collections
- Developer data
- Science and math

Each catalog item includes a stable id, display name, category, proposed API,
status, and behavior description. The docs site publishes a synchronized copy at
`docs/assets/beta-output-types.json` so the website can render the catalog as a
static site.

Implemented v1 catalog items are marked `available-v1`. Future targets are
marked `planned-beta`.

## Repository Map

```text
src/                 Python reference SDK and CLI
packages/            Native SDK targets for 15 languages
spec/v1/             Shared v1 behavior contract
spec/beta/           Beta random-output catalog
docs/                Static documentation/marketing site
tests/               Python, CLI, layout, and catalog tests
```

## Development

Run the test suite:

```bash
python -m pytest
```

Build the Python package:

```bash
python -m build
```

Serve the documentation site from the repository root so the static assets load
the same way they will in production:

```bash
python -m http.server 8001
```

Then open:

```text
http://localhost:8001/docs/index.html
```

## Release Direction

The current release line is `0.1.x` for the v1 primitive foundation. The path to
`1.0.0` is:

- keep the v1 contract stable for ints, floats, and chars
- complete packaging and conformance checks for each language target
- promote beta catalog items from `planned-beta` to implemented status as they
  land
- keep all SDKs aligned to one semantic version once publishing begins

## License

This project is licensed under the MIT License. See `LICENSE` for the
authoritative license text.
