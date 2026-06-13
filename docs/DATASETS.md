# libRandomizer Dataset Policy

Dataset-backed random types include words, names, places, user agents, MIME
types, commerce values, game terms, locale labels, time zones, and similar
human-readable outputs.

## Requirements

Every bundled dataset must document:

- source name and URL or local origin
- license and compatibility with MIT distribution
- update policy
- locale coverage
- whether it is safe by default
- whether adult/profane entries exist
- fields and return shape used by SDKs

## Safe Defaults

Safe corpora are loaded by default. Adult/profane values must never appear from
default calls such as `randomWord()` or `randomWords(5)`.

Adult/profane values require explicit opt-in:

```text
randomWord(allowAdult=true)
randomWords(5, allowAdult=true)
```

Language packages may use idiomatic option syntax, but the behavior must match
the shared catalog contract.

## Dataset Storage

Datasets should use portable JSON so every SDK can consume the same source data
or generate equivalent native bundles.

Recommended layout:

```text
datasets/
  text/
    words.safe.en-US.json
    words.adult.en-US.json
  people/
  location/
  internet/
  commerce/
  games/
```

## Minimum Beta Dataset Set

Production beta needs documented datasets for:

- safe words and adult/profane opt-in words
- first names, last names, prefixes, suffixes, job titles, departments
- countries, regions, cities, streets, locales, time zones, currency codes
- user agents, MIME types, HTTP statuses, HTTP methods
- color names and palette seed data
- commerce brands, product categories, shipping methods, payment methods
- games: suits, ranks, RPG classes, loot rarities, team-name terms
- developer data: file extensions, log levels, environment names

## Acceptance Gate

No dataset-backed type can be marked `implemented-all` until its source,
license, safety mode, and locale policy are documented.
