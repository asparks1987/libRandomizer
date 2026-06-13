# libRandomizer Beta Output Catalog

The beta documentation cements the output-type vocabulary that libRandomizer
should grow toward after the v1 alpha SDK foundation.

The product goal is language agnostic: a developer should be able to import the
SDK in their language of choice and ask for a random value by type. The API
should remain small and predictable even as the type catalog grows.

## Current v1 Types

These output types already exist in the v1 alpha contract:

- `randomInt()`
- `randomFloat()`
- `randomChar()`

## Beta Catalog

The machine-readable catalog lives in `output-types.json`. It currently defines
at least 100 output types across these categories:

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

Each catalog entry has:

- `id`: stable kebab-case identifier
- `name`: human-readable type name
- `category`: grouping for docs and implementation planning
- `api`: proposed public function name
- `status`: `available-v1` or `planned-beta`
- `description`: short behavior summary

## Beta API Direction

The preferred API shape remains direct:

```text
randomColor()
randomName()
randomDate()
randomChoice(items)
randomWeightedChoice(items)
```

Languages with different conventions should expose idiomatic aliases while
preserving clear documentation that maps back to the shared catalog.

## Implementation Notes

- Beta docs define the target vocabulary; they do not mean every listed type is
  implemented in every SDK yet.
- Type names should be stable once published in the beta catalog.
- New type implementations should add conformance cases before being marked
  implemented.
- Dataset-backed types such as names, places, words, brands, and user agents
  should document their source, size, locale support, and update policy.
