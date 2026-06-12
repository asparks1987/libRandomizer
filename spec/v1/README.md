# libRandomizer v1 Contract

The v1 SDK contract exists so every native language package behaves the same
while still feeling natural to import and call.

## Functions

Every SDK must expose these operations as top-level functions or the closest
language-native equivalent:

- `randomInt()` returns an integer in the inclusive range `0..99`.
- `randomFloat()` returns a floating-point number in the range `0.0..1.0`.
- `randomChar()` returns a printable ASCII character in the inclusive range
  `"A".."Z"`.

Every SDK must also support optional bounds:

- `randomInt(min, max)`
- `randomFloat(min, max)`
- `randomChar(min, max)`

Languages whose naming conventions strongly prefer another casing should expose
idiomatic aliases while keeping a documented camelCase call where practical.

## Randomness

Every SDK must use the operating system cryptographic random number generator.
The SDK must not use time-based seeds or deterministic pseudo-random generators
for v1 values.

## Validation

- Bounds are inclusive for integers and characters.
- `min` must be less than or equal to `max`.
- `randomChar` bounds must be exactly one printable ASCII character.
- Equal boundaries must return that boundary.
- Invalid input must fail clearly using the language's standard error mechanism.

## JSON Examples

The CLI fallback continues to use compact JSON:

```json
{"type":"int","value":42}
```

```json
{"error":"Invalid range: min must be less than or equal to max"}
```
