# libRandomizer

`libRandomizer` is a language-agnostic randomization SDK project. The goal is
simple: import the package in the language you are already using, call one
small function, and get an OS-backed random value.

```c
int thisINT = randomInt();
```

The V1 public beta exposes the full 138-type beta catalog from the Python
reference SDK and CLI, with generated native SDK surfaces for the 15 target
language packages. Python is the deepest reference implementation; the native
packages provide the beta `randomX()`/`getRandomX()` call surface and package
metadata for local build validation.

## Current Status

This repository is repo-ready for the V1 public beta:

- Python reference SDK with all 138 catalog functions, aliases, class
  compatibility, and CLI fallback
- Native package targets for 15 languages under `packages/`
- Shared beta behavior contract, schema, and generated conformance fixtures in
  `spec/beta`
- Portable in-house MIT seed datasets under `datasets/`
- GitHub-dark documentation site in `docs/`
- Unit tests, CLI tests, catalog checks, and beta release smoke coverage

Important distinction: Python and the CLI are the reference implementation for
the full catalog. The other native SDKs have the full public beta surface and
secure-random primitives, but deeper option parity and per-language conformance
expansion should continue after this repo-ready beta.

For the full production beta burndown, see:

- `docs/PRODUCT_SCOPE.md`
- `docs/API_REFERENCE.md`
- `docs/BETA_BURNDOWN.md`
- `docs/DATASETS.md`
- `docs/CONFORMANCE.md`

## What Works Today

| Type | Default call | Default range | Bounded call |
| --- | --- | --- | --- |
| Integer | `randomInt()` | `0..99` | `randomInt(min, max)` |
| Float | `randomFloat()` | `0.0..1.0` | `randomFloat(min, max)` |
| Character | `randomChar()` | `"A".."Z"` | `randomChar(min, max)` |

The full Python/CLI beta catalog also includes strings, bytes, UUIDs, colors,
words, names, places, internet values, dates, commerce values, games,
collections, developer data, and science/math helpers. See
`docs/API_REFERENCE.md` for the complete generated list.

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
from librandomizer import random_int, random_float, random_char, randomWords

value = random_int()
score = random_int(10, 20)
ratio = random_float()
letter = random_char("A", "F")
phrase = randomWords(5)
```

Camel-case aliases are available when you want the cross-language shape:

```python
from librandomizer import randomInt, randomFloat, randomChar, randomString, randomColorName

value = randomInt()
ratio = randomFloat(0.25, 0.75)
letter = randomChar("A", "Z")
token = randomString(5)
color = randomColorName()
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
librandom string --length 5
librandom color-name
librandom weighted-choice --items '["a","b"]' --weights '[1,3]'
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

Each catalog item includes a stable id, display name, category, public API,
status, behavior description, parameters, return shape, errors, examples,
dataset dependency, content-safety mode, and aliases. The docs site publishes a
synchronized copy at `docs/assets/beta-output-types.json` so the website can
render the catalog as a static site.

Repo-ready V1 public beta catalog items are marked `implemented-all`.
`available-v1` remains documented only as an early compatibility status.

## Repository Map

```text
src/                 Python reference SDK and CLI
packages/            Native SDK targets for 15 languages
spec/v1/             Original primitive behavior contract
spec/beta/           Beta random-output catalog, schema, and conformance fixtures
docs/                Static site plus product, API, dataset, conformance, and burndown docs
datasets/            Portable MIT seed datasets and metadata
tests/               Python, CLI, layout, catalog, and beta release tests
scripts/             Catalog, docs, conformance, and SDK generation helpers
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

Regenerate beta release artifacts after changing `spec/beta/output-types.json`:

```bash
python scripts/generate_beta_release.py
python scripts/generate_native_sdk_surfaces.py
python scripts/sync_beta_docs.py
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

The current release line is `0.1.0b1` for the repo-ready V1 public beta. The
path to `1.0.0` is:

- deepen per-language option parity beyond the generated beta surfaces
- expand native conformance runners for every package manager and toolchain
- replace beta seed datasets with larger documented corpora where useful
- publish packages from tagged releases once registry credentials and dry-runs
  are complete

## License

This project is licensed under the MIT License. See `LICENSE` for the
authoritative license text.
