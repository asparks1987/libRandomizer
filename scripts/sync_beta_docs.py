"""Synchronize beta catalog-derived documentation artifacts."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "spec" / "beta" / "output-types.json"
DOCS_CATALOG_PATH = ROOT / "docs" / "assets" / "beta-output-types.json"
API_REFERENCE_PATH = ROOT / "docs" / "API_REFERENCE.md"


def main() -> int:
    catalog = json.loads(CATALOG_PATH.read_text())
    DOCS_CATALOG_PATH.write_text(json.dumps(catalog, indent=2) + "\n")
    API_REFERENCE_PATH.write_text(render_api_reference(catalog))
    return 0


def render_api_reference(catalog: dict) -> str:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for entry in catalog["types"]:
        grouped[entry["category"]].append(entry)

    lines = [
        "# libRandomizer API Reference",
        "",
        "This file is generated from `spec/beta/output-types.json`. Update the source catalog, then run:",
        "",
        "```bash",
        "python scripts/sync_beta_docs.py",
        "```",
        "",
        "Status values:",
        "",
    ]

    for status, description in catalog["statusLegend"].items():
        lines.append(f"- `{status}`: {description}")

    lines.extend(
        [
            "",
            "Shared option names:",
            "",
        ]
    )

    for option, description in catalog["sharedOptions"].items():
        lines.append(f"- `{option}`: {description}")

    lines.extend(
        [
            "",
            "Text safety policy: safe corpora are the default; adult/profane terms require explicit opt-in.",
            "",
        ]
    )

    for category in grouped:
        lines.extend([f"## {category}", ""])
        for entry in grouped[category]:
            lines.extend(render_entry(entry))

    return "\n".join(lines).rstrip() + "\n"


def render_entry(entry: dict) -> list[str]:
    aliases = ", ".join(f"`{alias}`" for alias in entry.get("aliases", [])) or "None"
    parameters = entry.get("parameters", [])
    parameter_text = ", ".join(format_parameter(parameter) for parameter in parameters) or "None"
    examples = entry.get("examples", [])
    example = examples[0] if examples else {"call": entry["api"], "returns": "<value>"}
    dataset = entry.get("datasets", {})

    return [
        f"### {entry['name']}",
        "",
        f"- API: `{entry['api']}`",
        f"- Status: `{entry['status']}`",
        f"- Aliases: {aliases}",
        f"- Parameters: {parameter_text}",
        f"- Returns: `{entry['returns']['type']}` - {entry['returns']['description']}",
        f"- Content safety: `{entry.get('contentSafety', 'not-applicable')}`",
        f"- Dataset: `{dataset.get('source', 'none')}`",
        f"- Errors: {'; '.join(entry.get('errors', []))}",
        f"- Example: `{example['call']}` -> `{example['returns']}`",
        "",
    ]


def format_parameter(parameter: dict) -> str:
    default = parameter.get("default")
    default_text = "required" if parameter.get("required") else f"default `{default}`"
    return f"`{parameter['name']}` ({parameter['type']}, {default_text})"


if __name__ == "__main__":
    raise SystemExit(main())
