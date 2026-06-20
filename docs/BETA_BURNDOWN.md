# Full Catalog v1 Beta Production Burndown

> Legacy planning note: this burndown tracks the older random primitive catalog.
> The current primary product is the portable training-data generator described
> in `PRODUCT_SCOPE.md`, `../README.md`, and `../spec/training/README.md`.

This is the master task list for taking libRandomizer to fully functional v1
beta production.

## 1. Spec And Catalog

- [x] Define beta production scope.
- [x] Keep the 138-type catalog in `spec/beta/output-types.json`.
- [x] Add implementation contract fields to every catalog entry.
- [x] Add allowed statuses: `planned-beta`, `in-progress`, `implemented-python`, `implemented-all`, `deprecated`, `available-v1`.
- [x] Define shared option names: `min`, `max`, `length`, `count`, `locale`, `allowAdult`, `format`, `items`, `weights`.
- [x] Replace `available-v1` with the final status model or document it as a compatibility status.
- [x] Add machine-readable conformance cases for every catalog type.
- [x] Add schema validation for catalog contracts.

## 2. Python Reference SDK And CLI

- [x] Keep current v1 primitives stable: `randomInt`, `randomFloat`, `randomChar`.
- [x] Implement all 138 catalog functions in Python.
- [x] Add `getRandomX` aliases for every Python `randomX` function.
- [x] Add helpers for secure bytes, range validation, choices, weighted choices, dataset loading, locale fallback, and content-safety selection.
- [x] Extend CLI to support all 138 catalog functions.
- [x] Add JSON output and JSON error output for every CLI function.

## 3. Datasets

- [x] Define dataset policy and safe-default behavior.
- [x] Add portable JSON dataset directory.
- [x] Add safe word corpus.
- [x] Add adult/profane opt-in corpus.
- [x] Add names, places, internet, commerce, games, developer-data, and color datasets.
- [x] Document source, license, update policy, locale coverage, and safety status for every dataset.

## 4. All 15 SDKs

- [x] Keep package directories for all 15 language targets.
- [x] Implement the 138-function surface in Python.
- [x] Implement the 138-function surface in JavaScript.
- [x] Implement the 138-function surface in TypeScript.
- [x] Implement the 138-function surface in Java.
- [x] Implement the 138-function surface in C#.
- [x] Implement the 138-function surface in C.
- [x] Implement the 138-function surface in C++.
- [x] Implement the 138-function surface in PHP.
- [x] Implement the 138-function surface in Go.
- [x] Implement the 138-function surface in Rust.
- [x] Implement the 138-function surface in Kotlin.
- [x] Implement the 138-function surface in Swift.
- [x] Implement the 138-function surface in Ruby.
- [x] Implement the 138-function surface in Dart.
- [x] Implement the 138-function surface in R.

## 5. Conformance And Tests

- [x] Keep Python unit, CLI, layout, and catalog tests green.
- [x] Add shared conformance fixtures generated from the catalog.
- [ ] Add install/import/call smoke tests for every language package.
- [x] Add per-type Python/CLI conformance tests for defaults, callability, JSON output, and safe text mode.
- [ ] Add CI matrix for Windows, macOS, and Linux where supported.
- [ ] Block `implemented-all` status unless every language passes.

## 6. Packaging And Release

- [x] Validate Python package metadata and build artifacts.
- [ ] Validate npm packages for JavaScript and TypeScript.
- [ ] Validate Maven/Gradle metadata for Java and Kotlin.
- [ ] Validate NuGet metadata for C#.
- [ ] Validate crates.io metadata for Rust.
- [ ] Validate Packagist metadata for PHP.
- [ ] Validate Go module metadata.
- [ ] Validate RubyGems metadata.
- [ ] Validate pub.dev metadata for Dart.
- [ ] Validate Swift Package Manager metadata.
- [ ] Validate R package metadata.
- [ ] Validate CMake plus vcpkg/Conan-ready metadata for C and C++.
- [ ] Add release dry-run scripts before any registry publishing.
- [x] Add changelog.
- [x] Add release checklist.

## 7. Docs And Website

- [x] Add product scope doc.
- [x] Add API reference generated from the beta catalog.
- [x] Add dataset policy doc.
- [x] Add conformance doc.
- [x] Add this burndown checklist.
- [x] Add generated website status table by type and language.
- [x] Add examples for primitives, strings, words, names, places, colors, dates, choices, weighted choices, and objects.
- [x] Add per-language install instructions for package managers.
- [ ] Add publishing dry-run instructions.

## Production Beta Exit Criteria

- [x] `python -m pytest` passes.
- [x] `python -m build` passes.
- [ ] Every language package builds with its native toolchain.
- [ ] Every language package has install/import/call smoke tests.
- [ ] Shared conformance suite passes for all 138 types across all 15 languages.
- [x] Docs catalog snapshot matches source catalog.
- [x] Website renders current capability status and full catalog honestly.
- [x] No bundled dataset has unclear license/source metadata.
- [x] Safe text mode is default.
- [x] Adult/profane output appears only when explicitly opted in.
- [x] Release checklist proves metadata, version alignment, license, changelog, and artifact generation.
