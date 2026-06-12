# libRandomizer

`libRandomizer` is a native SDK family for getting OS-backed random values with
the smallest practical API in each language.

The goal is simple:

```c
int thisINT = randomInt();
```

Every supported language should feel that direct: import the package, call a
function, get a random value.

## Alpha v1 Scope

Alpha v1 supports:

- `randomInt()` with default range `0..99`
- `randomFloat()` with default range `0.0..1.0`
- `randomChar()` with default range `"A".."Z"`

All functions also support explicit bounds where the language allows it:

- `randomInt(min, max)`
- `randomFloat(min, max)`
- `randomChar(min, max)`

## Supported SDK Targets

The v1 monorepo is organized around 15 SDK-friendly languages:

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

See `packages/` for language-specific implementations and examples.

## Randomness Model

Alpha v1 uses each platform's operating system cryptographic random number
generator. It does not seed from time and it does not use deterministic
pseudo-random generators for SDK values.

For v1, "true random" means OS-backed cryptographic randomness that is practical
for local and server-side software. It does not require a hardware true random
number generator or an external network randomness service.

## Python Reference SDK

The Python SDK is the reference implementation and remains installable from the
repository root.

```bash
python -m pip install .
```

```python
from librandomizer import random_int, random_float, random_char

value = random_int()
ratio = random_float(0.0, 1.0)
letter = random_char("A", "Z")
```

Camel-case aliases are also available:

```python
from librandomizer import randomInt

value = randomInt()
```

The older class-first import is still supported:

```python
from libRandom import LibRandom

value = LibRandom().random_int()
```

## CLI Fallback

The CLI remains available for environments that do not yet have a native
package.

```bash
librandom int --min 0 --max 99
librandom float --min 0.0 --max 1.0
librandom char --min A --max Z
```

Example output:

```json
{"type":"int","value":42}
```

## Shared Contract

The shared SDK behavior is defined in `spec/v1`.

Core rules:

- integer and character ranges are inclusive
- `min` must be less than or equal to `max`
- characters must be printable ASCII
- equal boundaries return that boundary
- invalid inputs fail clearly in the language's normal error style

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

Package-specific metadata and examples live under `packages/<language>`.

## Roadmap

Future versions should add richer random domains while keeping the API direct:

- strings and symbols
- colors
- words
- names
- places
- lists and selections
- weighted choices
- dates and times
- structured random objects

## License

This project is licensed under the MIT License. See `LICENSE` for the
authoritative license text.
