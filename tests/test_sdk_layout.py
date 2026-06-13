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

    assert len(types) >= catalog["minimumCatalogSize"] >= 100
    assert len(ids) == len(set(ids))
    assert {"available-v1", "planned-beta"} >= statuses

    for entry in types:
        assert entry["id"]
        assert entry["name"]
        assert entry["category"]
        assert entry["api"].startswith("random")
        assert entry["description"]


def test_docs_beta_catalog_snapshot_matches_the_source_spec():
    source = json.loads((ROOT / "spec" / "beta" / "output-types.json").read_text())
    published = json.loads((ROOT / "docs" / "assets" / "beta-output-types.json").read_text())

    assert published == source
