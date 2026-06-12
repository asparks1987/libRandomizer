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
