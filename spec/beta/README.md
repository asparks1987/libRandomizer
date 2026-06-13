# libRandomizer Beta Output Catalog

The beta documentation cements the output-type vocabulary that libRandomizer
ships for the repo-ready V1 public beta.

The product goal is language agnostic: a developer should be able to import the
SDK in their language of choice and ask for a random value by type. The API
should remain small and predictable even as the type catalog grows.

## Current V1 Public Beta Types

The beta catalog contains 138 output types. The Python reference SDK and CLI
implement the full catalog; native package folders expose the generated beta
surface for all target languages.

The stable primitive calls remain:

- `randomInt()`
- `randomFloat()`
- `randomChar()`

The machine-readable catalog lives in `output-types.json`. It currently defines
138 output types across these categories:

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
- `status`: one of the catalog `allowedStatuses`
- `description`: short behavior summary
- `parameters`: shared option contract for implementation
- `returns`: expected return type and shape notes
- `errors`: required failure cases
- `examples`: example calls and representative return values
- `datasets`: dataset dependency, source, license, and locale requirements
- `contentSafety`: safe-default/adult-opt-in behavior
- `aliases`: supported `getRandomX` style aliases where practical

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

- `implemented-all` means the repo exposes the catalog function across all 15
  package targets.
- Python and CLI are the deepest reference implementation for option behavior.
- Type names should be stable once published in the beta catalog.
- Dataset-backed types such as names, places, words, brands, and user agents
  should document their source, size, locale support, and update policy.
