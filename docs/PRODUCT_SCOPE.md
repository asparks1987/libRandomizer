# libRandomizer Product Scope

This document defines what "fully functional v1 beta production" means for
libRandomizer.

## Product Goal

libRandomizer should let developers import a native package in their language
of choice and call one small function to get an OS-backed random value.

```text
randomInt()
randomString(5)
randomWords(5)
randomColor()
randomWeightedChoice(items, weights)
```

The beta production goal is to implement the 138 output types currently listed
in `spec/beta/output-types.json` across all 15 SDK targets.

## Current Production Beta Target

Production beta requires:

- all 138 catalog entries have implementation contracts
- all 138 catalog entries are implemented in Python first
- all 138 catalog entries are implemented across all 15 language packages
- every implementation uses OS-backed cryptographic randomness
- every package has native install/import/call smoke tests
- every type has shared conformance cases
- datasets have documented source, license, safety, and locale policy
- docs clearly separate implemented features from planned work
- package metadata is ready for registry publishing dry runs

## Out Of Scope

The beta does not promise:

- an infinite catalog of every possible random data type
- hardware true random number generator requirements
- hosted network randomness
- cryptographic token suitability beyond documented secure-random primitives
- full locale coverage for every dataset-backed type
- deterministic seeding or reproducible random streams

## Randomness Meaning

"True random" means practical OS-backed cryptographic randomness. Each SDK must
use its platform's secure random source and must not seed from time.

## Text And Dataset Safety

Safe datasets are the default. Adult or profane text is allowed only through an
explicit opt-in option such as `allowAdult: true` or the closest idiom in the
target language.

`randomString(5)` means five characters. `randomWords(5)` means five words.

## Beta Limitations

Production beta is still prerelease software. It can change before `1.0.0`, but
it must be installable, tested, documented, honest about unfinished work, and
safe by default.
