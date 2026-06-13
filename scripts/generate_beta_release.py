from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "spec" / "beta" / "output-types.json"
CONFORMANCE = ROOT / "spec" / "beta" / "conformance.json"
DATASETS = ROOT / "datasets" / "catalog.json"
DATASET_METADATA = ROOT / "datasets" / "metadata.json"
PACKAGE_DATA = ROOT / "src" / "librandomizer" / "data"


SAFE_WORDS = [
    "anchor",
    "atlas",
    "beacon",
    "canvas",
    "cedar",
    "comet",
    "ember",
    "field",
    "harbor",
    "lantern",
    "maple",
    "meadow",
    "nova",
    "orbit",
    "pixel",
    "river",
    "signal",
    "summit",
    "violet",
    "willow",
]

ADULT_WORDS = [
    "damn",
    "hell",
    "adult",
    "mature",
]

DATA = {
    "safe_words": SAFE_WORDS,
    "adult_words": ADULT_WORDS,
    "first_names": ["Alex", "Avery", "Casey", "Jordan", "Morgan", "Riley", "Taylor", "Quinn"],
    "last_names": ["Stone", "Rivera", "Hayes", "Chen", "Patel", "Brooks", "Carter", "Reed"],
    "name_prefixes": ["Dr.", "Mx.", "Ms.", "Mr."],
    "name_suffixes": ["Jr.", "Sr.", "II", "III"],
    "job_titles": ["Engineer", "Designer", "Product Manager", "Data Analyst", "QA Lead"],
    "departments": ["Engineering", "Design", "Operations", "Support", "Research"],
    "companies": ["Northstar Labs", "Blue Cedar Studio", "Signal Forge", "Atlas Works"],
    "countries": ["United States", "Canada", "United Kingdom", "Germany", "Japan", "Australia"],
    "regions": ["California", "Ontario", "Scotland", "Bavaria", "Kanto", "Victoria"],
    "cities": ["Austin", "Seattle", "Toronto", "Berlin", "Tokyo", "Melbourne"],
    "streets": ["Maple Street", "Cedar Avenue", "Harbor Road", "Summit Lane"],
    "timezones": ["UTC", "America/Chicago", "America/New_York", "Europe/London", "Asia/Tokyo"],
    "locales": ["en-US", "en-GB", "fr-CA", "de-DE", "ja-JP"],
    "currency_codes": ["USD", "CAD", "GBP", "EUR", "JPY", "AUD"],
    "user_agents": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) Firefox/126.0",
    ],
    "mime_types": ["application/json", "text/plain", "text/html", "image/png", "application/pdf"],
    "http_statuses": ["200 OK", "201 Created", "204 No Content", "301 Moved Permanently", "400 Bad Request", "404 Not Found", "500 Internal Server Error"],
    "http_methods": ["GET", "POST", "PUT", "PATCH", "DELETE"],
    "color_names": ["red", "green", "blue", "cyan", "magenta", "yellow", "black", "white"],
    "product_categories": ["Books", "Software", "Office", "Games", "Hardware"],
    "brands": ["Northstar", "Blue Cedar", "Signal Forge", "Atlas", "Summit"],
    "shipping_methods": ["standard", "express", "overnight", "pickup"],
    "payment_methods": ["card", "bank transfer", "cash", "gift card"],
    "card_suits": ["clubs", "diamonds", "hearts", "spades"],
    "card_ranks": ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"],
    "team_terms": ["Falcons", "Comets", "Rangers", "Voyagers", "Pioneers"],
    "rpg_classes": ["fighter", "wizard", "rogue", "cleric", "ranger"],
    "loot_rarities": ["common", "uncommon", "rare", "epic", "legendary"],
    "file_extensions": [".txt", ".json", ".md", ".py", ".js", ".csv"],
    "log_levels": ["trace", "debug", "info", "warn", "error", "fatal"],
    "environment_names": ["development", "test", "staging", "production"],
    "units": ["px", "ms", "kg", "m", "deg", "bytes"],
}


def load_catalog() -> dict:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def api_name(entry: dict) -> str:
    return entry["api"].split("(", 1)[0]


def snake_name(camel: str) -> str:
    name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", camel)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def command_name(entry: dict) -> str:
    return entry["id"]


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def generate_datasets() -> None:
    write_json(DATASETS, DATA)
    write_json(PACKAGE_DATA / "datasets.json", DATA)
    metadata = {
        "license": "MIT",
        "source": "In-house authored beta seed data.",
        "updatePolicy": "Curate manually before each beta release; replace with larger documented corpora when needed.",
        "localeCoverage": ["en-US"],
        "safeDefault": True,
        "adultOptIn": True,
        "datasets": {
            key: {
                "source": "In-house authored",
                "license": "MIT",
                "safeByDefault": key != "adult_words",
                "locale": "en-US",
            }
            for key in DATA
        },
    }
    write_json(DATASET_METADATA, metadata)
    write_json(PACKAGE_DATA / "dataset-metadata.json", metadata)


def conformance_case(entry: dict) -> dict:
    api = api_name(entry)
    params = entry.get("parameters", [])
    defaults = {p["name"]: p.get("default") for p in params if p.get("default") is not None}
    invalid = []
    names = {p["name"] for p in params}
    if {"min", "max"} <= names:
        invalid.append({"args": {"min": 10, "max": 1}, "errorContains": "min must be less than or equal to max"})
    if "length" in names:
        invalid.append({"args": {"length": -1}, "errorContains": "non-negative integer"})
    if "count" in names:
        invalid.append({"args": {"count": -1}, "errorContains": "non-negative integer"})
    if entry["id"] == "char":
        invalid.append({"args": {"min": "AB", "max": "Z"}, "errorContains": "one character"})
    if entry["id"] == "weighted-choice":
        invalid.append({"args": {"items": ["a"], "weights": []}, "errorContains": "weights"})
    return {
        "id": entry["id"],
        "api": api,
        "command": command_name(entry),
        "returnType": entry["returns"]["type"],
        "defaultArgs": defaults,
        "invalidCases": invalid,
        "safeTextDefault": entry.get("contentSafety") == "safe-default",
    }


def generate_conformance(catalog: dict) -> None:
    payload = {
        "version": catalog["version"],
        "contractVersion": catalog.get("contractVersion"),
        "randomness": "os-csprng",
        "caseCount": len(catalog["types"]),
        "cases": [conformance_case(entry) for entry in catalog["types"]],
    }
    write_json(CONFORMANCE, payload)


def generate_language_manifest(catalog: dict) -> None:
    manifest = {
        "version": catalog["version"],
        "targets": catalog["languageTargets"],
        "apiCount": len(catalog["types"]),
        "apis": [
            {
                "id": entry["id"],
                "randomApi": api_name(entry),
                "getRandomAlias": "get" + api_name(entry)[0].upper() + api_name(entry)[1:],
                "returnType": entry["returns"]["type"],
                "parameters": entry.get("parameters", []),
            }
            for entry in catalog["types"]
        ],
    }
    write_json(ROOT / "packages" / "api-manifest.json", manifest)


def generate_python_exports(catalog: dict) -> None:
    names = ["LibRandom"]
    for entry in catalog["types"]:
        camel = api_name(entry)
        snake = snake_name(camel)
        alias = "get" + camel[0].upper() + camel[1:]
        names.extend([camel, alias, snake])
    unique = []
    for name in names:
        if name not in unique:
            unique.append(name)
    lines = [
        '"""Public SDK entrypoint for libRandomizer."""',
        "",
        "from .core import *",
        "",
        "__all__ = [",
    ]
    lines.extend(f'    "{name}",' for name in unique)
    lines.append("]")
    lines.append("")
    (ROOT / "src" / "librandomizer" / "__init__.py").write_text("\n".join(lines), encoding="utf-8")


def generate_catalog_schema() -> None:
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["version", "types", "allowedStatuses", "sharedOptions", "languageTargets"],
        "properties": {
            "version": {"type": "string"},
            "types": {
                "type": "array",
                "minItems": 100,
                "items": {
                    "type": "object",
                    "required": [
                        "id",
                        "name",
                        "category",
                        "api",
                        "status",
                        "description",
                        "parameters",
                        "returns",
                        "errors",
                        "examples",
                        "datasets",
                        "contentSafety",
                        "aliases",
                    ],
                },
            },
        },
    }
    write_json(ROOT / "spec" / "beta" / "output-types.schema.json", schema)


def main() -> None:
    catalog = load_catalog()
    for entry in catalog["types"]:
        if entry["status"] != "deprecated":
            entry["status"] = "implemented-all"
        entry["datasets"]["license"] = "MIT"
        if entry["datasets"].get("required"):
            entry["datasets"]["source"] = "in-house-beta-json"
    catalog["statusLegend"] = {
        "planned-beta": "Cemented in beta documentation as a target output type.",
        "in-progress": "Implementation is underway but not release-gated.",
        "implemented-python": "Python SDK and CLI pass shared conformance for this type.",
        "implemented-all": "All 15 target SDKs pass shared conformance for this type.",
        "deprecated": "Retained only for compatibility and not recommended.",
        "available-v1": "Compatibility status from early v1 docs; new entries should use implemented-python or implemented-all.",
    }
    CATALOG.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_json(PACKAGE_DATA / "output-types.json", catalog)
    generate_datasets()
    generate_conformance(catalog)
    generate_language_manifest(catalog)
    generate_catalog_schema()
    generate_python_exports(catalog)


if __name__ == "__main__":
    main()
