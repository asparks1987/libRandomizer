import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
PYTHONPATH = os.pathsep.join([str(ROOT / "src"), str(ROOT)])


def run_cli(*args):
    env = os.environ.copy()
    env["PYTHONPATH"] = PYTHONPATH

    return subprocess.run(
        [sys.executable, "-m", "librandomizer.cli", *args],
        check=False,
        capture_output=True,
        env=env,
        text=True,
    )


def test_cli_int_outputs_json():
    result = run_cli("int", "--min", "5", "--max", "5")

    assert result.returncode == 0
    assert json.loads(result.stdout) == {"type": "int", "value": 5}


def test_cli_float_outputs_json():
    result = run_cli("float", "--min", "1.5", "--max", "1.5")

    assert result.returncode == 0
    assert json.loads(result.stdout) == {"type": "float", "value": 1.5}


def test_cli_char_outputs_json():
    result = run_cli("char", "--min", "Q", "--max", "Q")

    assert result.returncode == 0
    assert json.loads(result.stdout) == {"type": "char", "value": "Q"}


def test_cli_invalid_input_outputs_json_error_and_nonzero_exit():
    result = run_cli("int", "--min", "10", "--max", "1")

    assert result.returncode == 1
    assert result.stdout == ""
    assert json.loads(result.stderr) == {
        "error": "Invalid range: min must be less than or equal to max"
    }


def test_cli_parse_errors_output_json_error_and_nonzero_exit():
    result = run_cli("int", "--min", "not-an-int")

    assert result.returncode == 1
    assert result.stdout == ""
    assert json.loads(result.stderr) == {
        "error": "argument --min: invalid int value: 'not-an-int'"
    }
