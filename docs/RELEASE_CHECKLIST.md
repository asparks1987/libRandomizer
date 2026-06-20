# V1 Public Beta Release Checklist

> Legacy planning note: this checklist was written for the older random
> primitive catalog. The current release gates should prioritize
> `TrainingDataGenerator`, portable schemas, deterministic exports, and the
> documentation in `PRODUCT_SCOPE.md`.

Use this checklist before tagging a repo-ready public beta.

## Required Gates

- [ ] `python -m pytest`
- [ ] `python -m build`
- [ ] `node --check docs/site.js`
- [ ] `python scripts/generate_beta_release.py`
- [ ] `python scripts/generate_native_sdk_surfaces.py`
- [ ] `python scripts/sync_beta_docs.py`
- [ ] Confirm `spec/beta/output-types.json` matches `docs/assets/beta-output-types.json`.
- [ ] Confirm all package manifests use the same beta version.
- [ ] Confirm all package manifests use MIT licensing.
- [ ] Confirm `datasets/metadata.json` lists source, license, locale, update policy, and safety status.
- [ ] Confirm docs site shows current capability status and does not claim registry publishing.

## Local Package Smoke

- [ ] Python package builds.
- [ ] JavaScript package parses under Node.
- [ ] TypeScript package type-checks where dependencies are installed.
- [ ] Java package compiles with Maven where available.
- [ ] C# package builds with `dotnet` where available.
- [ ] Go module builds where Go is available.
- [ ] Rust crate builds where Cargo is available.
- [ ] C/C++ packages configure with CMake where available.
- [ ] PHP, Ruby, Dart, Swift, Kotlin, and R package metadata parses with native tools where available.

## Release Boundary

- [ ] Do not publish to registries for `0.1.0b1`.
- [ ] Create a GitHub prerelease/tag only after all required gates pass.
- [ ] Record known beta limitations in the release notes.
