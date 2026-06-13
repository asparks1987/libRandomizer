import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_v1_spec_defines_required_function_contract():
    spec = json.loads((ROOT / "spec" / "v1" / "conformance.json").read_text())

    assert spec["randomness"] == "os-csprng"
    assert spec["functions"]["randomInt"]["defaultMin"] == 0
    assert spec["functions"]["randomInt"]["defaultMax"] == 99
    assert spec["functions"]["randomFloat"]["defaultMin"] == 0.0
    assert spec["functions"]["randomFloat"]["defaultMax"] == 1.0
    assert spec["functions"]["randomChar"]["defaultMin"] == "A"
    assert spec["functions"]["randomChar"]["defaultMax"] == "Z"


def test_top_15_sdk_package_directories_exist():
    expected = {
        "python",
        "javascript",
        "typescript",
        "java",
        "csharp",
        "c",
        "cpp",
        "php",
        "go",
        "rust",
        "kotlin",
        "swift",
        "ruby",
        "dart",
        "r",
    }

    actual = {path.name for path in (ROOT / "packages").iterdir() if path.is_dir()}

    assert expected <= actual


def test_beta_output_catalog_cements_at_least_100_unique_types():
    catalog = json.loads((ROOT / "spec" / "beta" / "output-types.json").read_text())
    types = catalog["types"]
    ids = [entry["id"] for entry in types]
    statuses = {entry["status"] for entry in types}
    allowed_statuses = set(catalog["allowedStatuses"])

    assert len(types) >= catalog["minimumCatalogSize"] >= 100
    assert len(ids) == len(set(ids))
    assert allowed_statuses >= statuses
    assert {
        "min",
        "max",
        "length",
        "count",
        "locale",
        "allowAdult",
        "format",
        "items",
        "weights",
    } <= set(catalog["sharedOptions"])

    for entry in types:
        assert entry["id"]
        assert entry["name"]
        assert entry["category"]
        assert entry["api"].startswith("random")
        assert entry["description"]
        assert isinstance(entry["parameters"], list)
        assert entry["returns"]["type"]
        assert entry["errors"]
        assert entry["examples"]
        assert "required" in entry["datasets"]
        assert entry["contentSafety"] in {
            "not-applicable",
            "safe-default",
            "safe-default-adult-opt-in",
        }
        assert all(alias.startswith("getRandom") for alias in entry["aliases"])


def test_docs_beta_catalog_snapshot_matches_the_source_spec():
    source = json.loads((ROOT / "spec" / "beta" / "output-types.json").read_text())
    published = json.loads((ROOT / "docs" / "assets" / "beta-output-types.json").read_text())

    assert published == source


def test_production_beta_docs_exist_and_reference_catalog_contract():
    required_docs = {
        "PRODUCT_SCOPE.md",
        "API_REFERENCE.md",
        "BETA_BURNDOWN.md",
        "DATASETS.md",
        "CONFORMANCE.md",
    }

    for filename in required_docs:
        text = (ROOT / "docs" / filename).read_text()
        assert "libRandomizer" in text

    api_reference = (ROOT / "docs" / "API_REFERENCE.md").read_text()
    catalog = json.loads((ROOT / "spec" / "beta" / "output-types.json").read_text())

    assert "safe corpora are the default" in api_reference
    for entry in catalog["types"]:
        assert f"### {entry['name']}" in api_reference
        assert f"`{entry['api']}`" in api_reference
