import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

import librandomizer


ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "spec" / "beta" / "output-types.json").read_text())
CONFORMANCE = json.loads((ROOT / "spec" / "beta" / "conformance.json").read_text())
PYTHONPATH = os.pathsep.join([str(ROOT / "src"), str(ROOT)])


def _sample_args(entry):
    args = {}
    for param in entry.get("parameters", []):
        name = param["name"]
        if entry["id"] == "char" and name == "min":
            args[name] = "A"
        elif entry["id"] == "char" and name == "max":
            args[name] = "C"
        elif name == "items":
            args[name] = ["alpha", "beta", "gamma"]
        elif name == "weights":
            args[name] = [1, 2, 3]
        elif name == "count":
            args[name] = 1
        elif name == "length":
            args[name] = 4
        elif name == "min":
            args[name] = 1
        elif name == "max":
            args[name] = 3
        elif name == "allowAdult":
            args[name] = False
    return args


@pytest.mark.parametrize("entry", CATALOG["types"], ids=lambda entry: entry["id"])
def test_every_catalog_api_is_importable_and_callable(entry):
    function_name = entry["api"].split("(", 1)[0]
    function = getattr(librandomizer, function_name)
    value = function(**_sample_args(entry))

    assert value is not None


@pytest.mark.parametrize("entry", CATALOG["types"], ids=lambda entry: entry["id"])
def test_every_catalog_get_random_alias_is_importable(entry):
    function_name = entry["api"].split("(", 1)[0]
    alias = f"get{function_name[0].upper()}{function_name[1:]}"

    assert hasattr(librandomizer, alias)


@pytest.mark.parametrize("entry", CATALOG["types"], ids=lambda entry: entry["id"])
def test_every_catalog_cli_command_outputs_json(entry):
    args = [entry["id"]]
    for param in entry.get("parameters", []):
        name = param["name"]
        if name == "items":
            args.extend([f"--{name}", json.dumps(["alpha", "beta", "gamma"])])
        elif name == "weights":
            args.extend([f"--{name}", json.dumps([1, 2, 3])])
        elif name == "count":
            args.extend([f"--{name}", "1"])
        elif name == "length":
            args.extend([f"--{name}", "4"])
        elif name == "min":
            args.extend([f"--{name}", "1"])
        elif name == "max":
            args.extend([f"--{name}", "3"])
        elif name == "allowAdult":
            args.extend([f"--{name}", "false"])

    env = os.environ.copy()
    env["PYTHONPATH"] = PYTHONPATH
    result = subprocess.run(
        [sys.executable, "-m", "librandomizer.cli", *args],
        check=False,
        capture_output=True,
        env=env,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["type"] == entry["id"]
    assert "value" in payload


def test_beta_release_artifacts_are_present_and_consistent():
    assert (ROOT / "spec" / "beta" / "output-types.schema.json").exists()
    assert (ROOT / "datasets" / "catalog.json").exists()
    assert (ROOT / "datasets" / "metadata.json").exists()
    assert (ROOT / "packages" / "api-manifest.json").exists()
    assert CONFORMANCE["caseCount"] == len(CATALOG["types"])
    assert {case["id"] for case in CONFORMANCE["cases"]} == {entry["id"] for entry in CATALOG["types"]}


def test_safe_words_do_not_include_adult_words_by_default():
    datasets = json.loads((ROOT / "datasets" / "catalog.json").read_text())
    safe_words = set(datasets["safe_words"])
    adult_words = set(datasets["adult_words"])

    assert safe_words.isdisjoint(adult_words)
    assert librandomizer.randomWords(3).count(" ") == 2
