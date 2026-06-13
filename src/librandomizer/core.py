"""OS-backed random value generation for the v1 public beta SDK."""

from __future__ import annotations

import base64
import datetime as _dt
import json
import math
import re
import secrets
import string as _string
import uuid
from pathlib import Path
from typing import Any, Callable


_ROOT = Path(__file__).resolve().parents[2]
_PACKAGE_DATA = Path(__file__).resolve().parent / "data"
_CATALOG_PATH = (
    _PACKAGE_DATA / "output-types.json"
    if (_PACKAGE_DATA / "output-types.json").exists()
    else _ROOT / "spec" / "beta" / "output-types.json"
)
_DATASET_PATH = (
    _PACKAGE_DATA / "datasets.json"
    if (_PACKAGE_DATA / "datasets.json").exists()
    else _ROOT / "datasets" / "catalog.json"
)
_PRINTABLE_ASCII_MIN = 32
_PRINTABLE_ASCII_MAX = 126
_MAX_SIZE = 10_000
_ALPHANUM = _string.ascii_letters + _string.digits
_URLSAFE = _ALPHANUM + "_-"
_HEX = "0123456789abcdef"


def _load_json(path: Path, fallback: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return fallback


_CATALOG = _load_json(_CATALOG_PATH, {"types": []})
_DATASETS = _load_json(
    _DATASET_PATH,
    {
        "safe_words": ["anchor", "beacon", "canvas", "harbor", "signal"],
        "adult_words": ["adult"],
    },
)


def _snake_name(camel: str) -> str:
    first = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", camel)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", first).lower()


def _api_name(entry: dict[str, Any]) -> str:
    return entry["api"].split("(", 1)[0]


class LibRandom:
    """Generate beta random values using the operating system CSPRNG."""

    def __init__(self) -> None:
        self._rng = secrets.SystemRandom()

    def random_int(self, min: int = 0, max: int = 99) -> int:
        self._validate_range(min, max)
        return self._rng.randrange(int(min), int(max) + 1)

    def random_float(self, min: float = 0.0, max: float = 1.0) -> float:
        self._validate_range(min, max)
        if min == max:
            return float(min)
        return self._rng.uniform(float(min), float(max))

    def random_char(self, min: str = "A", max: str = "Z") -> str:
        min_code = self._validate_printable_char("min", min)
        max_code = self._validate_printable_char("max", max)
        self._validate_range(min_code, max_code)
        return chr(self._rng.randrange(min_code, max_code + 1))

    def random_words(
        self, count: int = 1, locale: str = "en-US", allowAdult: bool = False
    ) -> str:
        del locale
        count = self._validate_size("count", count)
        words = [self.random_word(allowAdult=allowAdult) for _ in range(count)]
        return " ".join(words)

    def _generate(self, output_id: str, **options: Any) -> Any:
        method = getattr(self, f"_generate_{output_id.replace('-', '_')}", None)
        if method is not None:
            return method(**options)

        entry = _entry_by_id(output_id)
        dataset_value = self._dataset_value(output_id)
        if dataset_value is not None:
            return dataset_value
        return self._generic_value(entry["returns"]["type"], output_id, **options)

    @staticmethod
    def _validate_range(min_value: int | float, max_value: int | float) -> None:
        if min_value > max_value:
            raise ValueError("Invalid range: min must be less than or equal to max")

    @staticmethod
    def _validate_size(name: str, value: int | None, default: int = 1) -> int:
        if value is None:
            value = default
        if not isinstance(value, int) or value < 0 or value > _MAX_SIZE:
            raise ValueError(f"Invalid size: {name} must be a non-negative integer within supported limits")
        return value

    @staticmethod
    def _validate_items(items: list[Any] | None) -> list[Any]:
        if not isinstance(items, list) or not items:
            raise ValueError("Invalid items: items must be a non-empty array")
        return items

    @staticmethod
    def _validate_printable_char(name: str, value: str) -> int:
        if not isinstance(value, str) or len(value) != 1:
            raise ValueError(f"Invalid character range: {name} must be one character")
        code = ord(value)
        if code < _PRINTABLE_ASCII_MIN or code > _PRINTABLE_ASCII_MAX:
            raise ValueError(f"Invalid character range: {name} must be printable ASCII")
        return code

    @staticmethod
    def _coerce_char(value: str | int) -> str:
        if isinstance(value, int):
            return chr(value)
        return value

    def _choice(self, values: list[Any]) -> Any:
        return values[self._rng.randrange(0, len(values))]

    def _chars(self, alphabet: str, length: int) -> str:
        return "".join(self._choice(list(alphabet)) for _ in range(length))

    def _bytes(self, length: int) -> bytes:
        return secrets.token_bytes(length)

    def _words(self, allowAdult: bool = False) -> list[str]:
        words = list(_DATASETS.get("safe_words", []))
        if allowAdult:
            words.extend(_DATASETS.get("adult_words", []))
        return words or ["anchor"]

    def _dataset_value(self, output_id: str) -> Any:
        mapping = {
            "first-name": "first_names",
            "last-name": "last_names",
            "name-prefix": "name_prefixes",
            "name-suffix": "name_suffixes",
            "job-title": "job_titles",
            "department": "departments",
            "company": "companies",
            "country": "countries",
            "region": "regions",
            "city": "cities",
            "street": "streets",
            "timezone": "timezones",
            "locale": "locales",
            "currency-code": "currency_codes",
            "user-agent": "user_agents",
            "mime-type": "mime_types",
            "http-status": "http_statuses",
            "color-name": "color_names",
            "product-category": "product_categories",
            "brand": "brands",
            "shipping-method": "shipping_methods",
            "payment-method": "payment_methods",
            "card-suit": "card_suits",
            "card-rank": "card_ranks",
            "team-name": "team_terms",
            "rpg-class": "rpg_classes",
            "loot-rarity": "loot_rarities",
            "file-extension": "file_extensions",
            "log-level": "log_levels",
            "http-method": "http_methods",
            "environment-name": "environment_names",
            "unit": "units",
        }
        key = mapping.get(output_id)
        if key is None:
            return None
        return self._choice(list(_DATASETS.get(key, ["value"])))

    def _generic_value(self, return_type: str, output_id: str, **options: Any) -> Any:
        min_value = options.get("min")
        max_value = options.get("max")
        if min_value is not None and max_value is not None:
            self._validate_range(min_value, max_value)
        if return_type in {"integer"}:
            return self.random_int(int(min_value or 0), int(max_value if max_value is not None else 99))
        if return_type in {"float", "decimal"}:
            return round(self.random_float(float(min_value or 0), float(max_value if max_value is not None else 1)), 6)
        if return_type == "boolean":
            return bool(self.random_bit())
        if return_type == "array":
            count = self._validate_size("count", options.get("count"), default=1)
            return [self.random_word() for _ in range(count)]
        if return_type == "object":
            return {"type": output_id, "value": self.random_word()}
        if return_type == "bytes":
            length = self._validate_size("length", options.get("length"), default=16)
            return self._bytes(length)
        return f"{output_id}-{self._chars(_ALPHANUM.lower(), 8)}"

    def _generate_bool(self) -> bool:
        return bool(self.random_bit())

    def _generate_string(self, length: int = 12) -> str:
        return self._chars(_ALPHANUM, self._validate_size("length", length))

    def _generate_bytes(self, length: int = 16, format: str | None = None) -> bytes | str:
        raw = self._bytes(self._validate_size("length", length))
        if format == "hex":
            return raw.hex()
        if format == "base64":
            return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")
        if format in {None, "bytes"}:
            return raw
        raise ValueError("Invalid option: unsupported format")

    def _generate_bit(self) -> int:
        return self._rng.randrange(0, 2)

    def _generate_binary_string(self, length: int = 16) -> str:
        return self._chars("01", self._validate_size("length", length))

    def _generate_hex_string(self, length: int = 16) -> str:
        return self._chars(_HEX, self._validate_size("length", length))

    def _generate_base64_string(self, length: int = 16) -> str:
        raw = self._bytes(self._validate_size("length", length))
        return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")

    def _generate_uuid(self) -> str:
        return str(uuid.UUID(bytes=self._bytes(16), version=4))

    def _generate_ulid(self) -> str:
        alphabet = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
        timestamp_ms = int(_dt.datetime.now(tz=_dt.timezone.utc).timestamp() * 1000)
        value = timestamp_ms << 80 | int.from_bytes(self._bytes(10), "big")
        chars = []
        for _ in range(26):
            chars.append(alphabet[value & 31])
            value >>= 5
        return "".join(reversed(chars))

    def _generate_nanoid(self, length: int = 16) -> str:
        return self._chars(_URLSAFE, self._validate_size("length", length))

    def _generate_slug(self, length: int = 16) -> str:
        return self._chars(_string.ascii_lowercase + _string.digits + "-", self._validate_size("length", length)).strip("-") or "slug"

    def _generate_token(self, length: int = 16, format: str | None = None) -> str:
        length = self._validate_size("length", length)
        if format == "hex":
            return self._generate_hex_string(length)
        return self._chars(_URLSAFE, length)

    def _generate_pin(self, length: int = 16) -> str:
        return self._chars(_string.digits, self._validate_size("length", length))

    _generate_otp = _generate_pin

    def _generate_short_code(self, length: int = 16) -> str:
        return self._chars(_string.ascii_uppercase + _string.digits, self._validate_size("length", length))

    _generate_coupon_code = _generate_short_code
    _generate_license_key = _generate_short_code

    def _generate_even_int(self, min: int = 0, max: int = 99) -> int:
        self._validate_range(min, max)
        values = [value for value in range(int(min), int(max) + 1) if value % 2 == 0]
        if not values:
            raise ValueError("Invalid range: no even integer exists within bounds")
        return self._choice(values)

    def _generate_odd_int(self, min: int = 0, max: int = 99) -> int:
        self._validate_range(min, max)
        values = [value for value in range(int(min), int(max) + 1) if value % 2 != 0]
        if not values:
            raise ValueError("Invalid range: no odd integer exists within bounds")
        return self._choice(values)

    def _generate_prime(self, min: int = 0, max: int = 99) -> int:
        self._validate_range(min, max)
        values = [value for value in range(int(min), int(max) + 1) if _is_prime(value)]
        if not values:
            raise ValueError("Invalid range: no prime exists within bounds")
        return self._choice(values)

    def _generate_decimal(self, min: float | None = None, max: float | None = None) -> float:
        return round(self.random_float(float(min if min is not None else 0), float(max if max is not None else 1)), 2)

    _generate_currency_amount = _generate_decimal

    def _generate_percentage(self, min: float | None = None, max: float | None = None) -> float:
        return round(self.random_float(float(min if min is not None else 0), float(max if max is not None else 100)), 4)

    def _generate_ratio(self, min: float | None = None, max: float | None = None) -> float:
        return round(self.random_float(float(min if min is not None else 0), float(max if max is not None else 1)), 6)

    def _generate_angle(self, min: float | None = None, max: float | None = None) -> float:
        return round(self.random_float(float(min if min is not None else 0), float(max if max is not None else 360)), 6)

    def _generate_latitude(self, min: float | None = None, max: float | None = None) -> float:
        return round(self.random_float(float(min if min is not None else -90), float(max if max is not None else 90)), 6)

    def _generate_longitude(self, min: float | None = None, max: float | None = None) -> float:
        return round(self.random_float(float(min if min is not None else -180), float(max if max is not None else 180)), 6)

    def _generate_word(self, locale: str = "en-US", allowAdult: bool = False) -> str:
        del locale
        return self._choice(self._words(allowAdult=allowAdult))

    def _generate_sentence(self, locale: str = "en-US", allowAdult: bool = False) -> str:
        words = [self._generate_word(locale=locale, allowAdult=allowAdult) for _ in range(self.random_int(6, 12))]
        return " ".join(words).capitalize() + "."

    def _generate_paragraph(self, count: int = 1, locale: str = "en-US", allowAdult: bool = False) -> str:
        count = self._validate_size("count", count)
        return " ".join(self._generate_sentence(locale=locale, allowAdult=allowAdult) for _ in range(count))

    def _generate_title(self, locale: str = "en-US", allowAdult: bool = False) -> str:
        return " ".join(self._generate_word(locale=locale, allowAdult=allowAdult).capitalize() for _ in range(3))

    def _generate_username(self, locale: str = "en-US", allowAdult: bool = False) -> str:
        return f"{self._generate_word(locale, allowAdult)}{self.random_int(10, 9999)}"

    def _generate_display_name(self, locale: str = "en-US", allowAdult: bool = False) -> str:
        return f"{self._generate_word(locale, allowAdult).capitalize()} {self._generate_word(locale, allowAdult).capitalize()}"

    def _generate_password(
        self,
        length: int = 16,
        locale: str = "en-US",
        allowAdult: bool = False,
        format: str | None = None,
    ) -> str:
        del locale, allowAdult, format
        alphabet = _ALPHANUM + "!@#$%^&*"
        return self._chars(alphabet, self._validate_size("length", length))

    def _generate_emoji(self, locale: str = "en-US", allowAdult: bool = False) -> str:
        del locale, allowAdult
        return self._choice(["😀", "✨", "🚀", "🎲", "📦", "💡", "🌈", "✅"])

    def _generate_symbol(self, locale: str = "en-US", allowAdult: bool = False) -> str:
        del locale, allowAdult
        return self._choice(list("!@#$%^&*+-=?"))

    def _generate_punctuation(self, locale: str = "en-US", allowAdult: bool = False) -> str:
        del locale, allowAdult
        return self._choice(list(".,;:!?"))

    def _generate_full_name(self, locale: str = "en-US") -> str:
        del locale
        return f"{self._dataset_value('first-name')} {self._dataset_value('last-name')}"

    def _generate_email(self, locale: str = "en-US") -> str:
        del locale
        return f"{self._generate_username().lower()}@{self._generate_domain()}"

    def _generate_phone(self, locale: str = "en-US") -> str:
        del locale
        return f"+1-{self.random_int(200,999)}-{self.random_int(200,999)}-{self.random_int(1000,9999)}"

    def _generate_url(self, format: str | None = None) -> str:
        del format
        return f"https://{self._generate_domain()}/{self._generate_slug(8)}"

    def _generate_domain(self, format: str | None = None) -> str:
        del format
        return f"{self._generate_slug(8)}.example"

    def _generate_subdomain(self, format: str | None = None) -> str:
        del format
        return f"{self._generate_slug(6)}.{self._generate_domain()}"

    def _generate_ipv4(self, format: str | None = None) -> str:
        del format
        return ".".join(str(self.random_int(0, 255)) for _ in range(4))

    def _generate_ipv6(self, format: str | None = None) -> str:
        del format
        return ":".join(self._generate_hex_string(4) for _ in range(8))

    def _generate_mac_address(self, format: str | None = None) -> str:
        del format
        return ":".join(self._generate_hex_string(2) for _ in range(6))

    def _generate_port(self, min: int | None = None, max: int | None = None, format: str | None = None) -> int | str:
        value = self.random_int(int(min if min is not None else 1), int(max if max is not None else 65535))
        return str(value) if format == "string" else value

    def _generate_hex_color(self, format: str | None = None) -> str:
        del format
        return "#" + self._generate_hex_string(6)

    def _generate_rgb_color(self, format: str | None = None) -> str:
        values = [self.random_int(0, 255) for _ in range(3)]
        return values if format == "array" else f"rgb({values[0]}, {values[1]}, {values[2]})"

    def _generate_rgba_color(self, format: str | None = None) -> str:
        del format
        return f"rgba({self.random_int(0,255)}, {self.random_int(0,255)}, {self.random_int(0,255)}, {round(self.random_float(), 2)})"

    def _generate_hsl_color(self, format: str | None = None) -> str:
        del format
        return f"hsl({self.random_int(0,360)}, {self.random_int(0,100)}%, {self.random_int(0,100)}%)"

    def _generate_hsla_color(self, format: str | None = None) -> str:
        del format
        return f"hsla({self.random_int(0,360)}, {self.random_int(0,100)}%, {self.random_int(0,100)}%, {round(self.random_float(), 2)})"

    def _generate_palette(self, count: int = 1, format: str | None = None) -> list[str]:
        del format
        return [self._generate_hex_color() for _ in range(self._validate_size("count", count))]

    def _generate_gradient(self, count: int = 1, format: str | None = None) -> str:
        colors = self._generate_palette(max(2, self._validate_size("count", count)), format)
        return f"linear-gradient(90deg, {', '.join(colors)})"

    def _generate_address(self, locale: str = "en-US") -> str:
        del locale
        return f"{self.random_int(100, 9999)} {self._dataset_value('street')}, {self._dataset_value('city')}"

    def _generate_postal_code(self, locale: str = "en-US") -> str:
        del locale
        return str(self.random_int(10000, 99999))

    def _generate_coordinate(self, locale: str = "en-US") -> dict[str, float]:
        del locale
        return {"latitude": self._generate_latitude(), "longitude": self._generate_longitude()}

    def _generate_date(self, format: str | None = None) -> str:
        del format
        start = _dt.date(1970, 1, 1).toordinal()
        end = _dt.date(2100, 12, 31).toordinal()
        return _dt.date.fromordinal(self.random_int(start, end)).isoformat()

    def _generate_time(self, format: str | None = None) -> str:
        del format
        return f"{self.random_int(0,23):02}:{self.random_int(0,59):02}:{self.random_int(0,59):02}"

    def _generate_datetime(self, format: str | None = None) -> str:
        del format
        return f"{self._generate_date()}T{self._generate_time()}Z"

    def _generate_timestamp(self, format: str | None = None) -> int:
        del format
        return self.random_int(0, 4_102_444_800)

    def _generate_duration(self, format: str | None = None) -> dict[str, int]:
        del format
        seconds = self.random_int(1, 86_400)
        return {"seconds": seconds, "milliseconds": seconds * 1000}

    def _generate_weekday(self, format: str | None = None) -> str:
        del format
        return self._choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

    def _generate_month(self, format: str | None = None) -> str:
        del format
        return self._choice(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

    def _generate_year(self, min: int | None = None, max: int | None = None, format: str | None = None) -> int | str:
        value = self.random_int(int(min if min is not None else 1970), int(max if max is not None else 2100))
        return str(value) if format == "string" else value

    def _generate_cron(self, format: str | None = None) -> str:
        del format
        return f"{self.random_int(0,59)} {self.random_int(0,23)} * * {self.random_int(0,6)}"

    def _generate_timezone_offset(self, format: str | None = None) -> str:
        del format
        hour = self.random_int(-12, 14)
        return f"{hour:+03}:00"

    def _generate_price(self, min: float | None = None, max: float | None = None) -> str:
        return f"${self._generate_decimal(min if min is not None else 1, max if max is not None else 999):.2f}"

    def _generate_sku(self) -> str:
        return f"SKU-{self._generate_short_code(8)}"

    def _generate_product_name(self) -> str:
        return f"{self._dataset_value('brand')} {self._generate_title()}"

    def _generate_order_id(self) -> str:
        return f"ORD-{self._generate_short_code(10)}"

    def _generate_invoice_number(self) -> str:
        return f"INV-{self.random_int(100000, 999999)}"

    def _generate_tax_rate(self, min: float | None = None, max: float | None = None) -> str:
        return f"{self._generate_percentage(min if min is not None else 0, max if max is not None else 12):.2f}%"

    def _generate_dice_roll(self, min: int | None = None, max: int | None = None) -> int:
        return self.random_int(int(min if min is not None else 1), int(max if max is not None else 6))

    def _generate_playing_card(self) -> dict[str, str]:
        return {"rank": self._dataset_value("card-rank"), "suit": self._dataset_value("card-suit")}

    def _generate_coin_flip(self) -> str:
        return self._choice(["heads", "tails"])

    def _generate_lottery_pick(self, count: int = 1) -> list[int]:
        count = self._validate_size("count", count)
        return [self.random_int(1, 99) for _ in range(count)]

    def _generate_game_score(self, min: int | None = None, max: int | None = None) -> str:
        return str(self.random_int(int(min if min is not None else 0), int(max if max is not None else 999)))

    def _generate_choice(self, items: list[Any] | None = None) -> Any:
        return self._choice(self._validate_items(items))

    def _generate_weighted_choice(self, items: list[Any] | None = None, weights: list[int | float] | None = None) -> Any:
        items = self._validate_items(items)
        if not isinstance(weights, list) or len(weights) != len(items) or any(weight < 0 for weight in weights) or sum(weights) <= 0:
            raise ValueError("Invalid weights: weights must align with items and contain a positive total")
        target = self.random_float(0, float(sum(weights)))
        total = 0.0
        for item, weight in zip(items, weights):
            total += float(weight)
            if target <= total:
                return item
        return items[-1]

    def _generate_sample(self, count: int = 1, items: list[Any] | None = None) -> list[Any]:
        items = list(self._validate_items(items))
        count = self._validate_size("count", count)
        if count > len(items):
            raise ValueError("Invalid size: count must not exceed item count")
        self._rng.shuffle(items)
        return items[:count]

    def _generate_shuffle(self, count: int = 1, items: list[Any] | None = None) -> list[Any]:
        del count
        items = list(self._validate_items(items))
        self._rng.shuffle(items)
        return items

    _generate_permutation = _generate_shuffle

    def _generate_set(self, count: int = 1, items: list[Any] | None = None) -> list[Any]:
        return list(dict.fromkeys(self._generate_sample(count=count, items=items)))

    def _generate_tuple(self, count: int = 1, items: list[Any] | None = None) -> list[Any]:
        return self._generate_sample(count=count, items=items)

    def _generate_json_object(self, items: list[Any] | None = None) -> dict[str, Any]:
        if items:
            return {str(index): item for index, item in enumerate(items)}
        return {"id": self._generate_uuid(), "word": self._generate_word()}

    def _generate_array(self, count: int = 1, items: list[Any] | None = None) -> list[Any]:
        if items:
            return self._generate_sample(count=count, items=items)
        return [self._generate_word() for _ in range(self._validate_size("count", count))]

    def _generate_matrix(self, count: int = 1, items: list[Any] | None = None) -> list[list[Any]]:
        del items
        size = max(1, self._validate_size("count", count))
        return [[self.random_int() for _ in range(size)] for _ in range(size)]

    def _generate_semver(self) -> str:
        return f"{self.random_int(0, 9)}.{self.random_int(0, 20)}.{self.random_int(0, 99)}"

    def _generate_git_sha(self) -> str:
        return self._generate_hex_string(40)

    def _generate_package_name(self) -> str:
        return f"{self._generate_slug(6)}-{self._generate_slug(6)}"

    def _generate_file_name(self) -> str:
        return f"{self._generate_slug(10)}{self._dataset_value('file-extension')}"

    def _generate_file_path(self) -> str:
        return f"/tmp/{self._generate_file_name()}"

    def _generate_directory_path(self) -> str:
        return f"/tmp/{self._generate_slug(10)}"

    def _generate_vector2(self) -> dict[str, float]:
        return {"x": self._generate_ratio(), "y": self._generate_ratio()}

    def _generate_vector3(self) -> dict[str, float]:
        return {"x": self._generate_ratio(), "y": self._generate_ratio(), "z": self._generate_ratio()}

    def _generate_normal(self, min: float | None = None, max: float | None = None) -> float:
        value = self._rng.gauss(0, 1)
        if min is not None and max is not None:
            self._validate_range(min, max)
            value = max(float(min), min(float(max), value))
        return round(value, 6)

    def _generate_weighted_number(self, min: float | None = None, max: float | None = None, weights: list[int | float] | None = None) -> float:
        del weights
        return self._generate_decimal(min if min is not None else 0, max if max is not None else 1)

    def _generate_measurement(self) -> dict[str, Any]:
        return {"value": self._generate_decimal(0, 100), "unit": self._dataset_value("unit")}

    def _generate_temperature(self, min: float | None = None, max: float | None = None) -> str:
        return f"{self._generate_decimal(min if min is not None else -20, max if max is not None else 120):.2f}C"

    def _generate_duration_ms(self, min: int | None = None, max: int | None = None) -> str:
        return str(self.random_int(int(min if min is not None else 1), int(max if max is not None else 1_000_000)))

    def _generate_probability(self, min: float | None = None, max: float | None = None) -> str:
        return str(self._generate_ratio(min if min is not None else 0, max if max is not None else 1))

    def _generate_range(self, min: float | None = None, max: float | None = None) -> dict[str, float]:
        low = float(min if min is not None else 0)
        high = float(max if max is not None else 100)
        self._validate_range(low, high)
        a = self.random_float(low, high)
        b = self.random_float(a, high)
        return {"min": round(a, 6), "max": round(b, 6)}

    def get_random_int(self, low: int = 0, high: int = 99) -> int:
        return self.random_int(min=low, max=high)

    def get_random_float(self, low: float = 0.0, high: float = 1.0) -> float:
        return self.random_float(min=low, max=high)

    def get_random_char(self, low: str | int = "A", high: str | int = "Z") -> str:
        return self.random_char(min=self._coerce_char(low), max=self._coerce_char(high))


def _is_prime(value: int) -> bool:
    if value < 2:
        return False
    for candidate in range(2, int(math.sqrt(value)) + 1):
        if value % candidate == 0:
            return False
    return True


def _entry_by_id(output_id: str) -> dict[str, Any]:
    for entry in _CATALOG.get("types", []):
        if entry["id"] == output_id:
            return entry
    raise ValueError(f"Unsupported random type: {output_id}")


def _make_method(output_id: str) -> Callable[..., Any]:
    def method(self: LibRandom, *args: Any, **kwargs: Any) -> Any:
        if args:
            entry = _entry_by_id(output_id)
            names = [param["name"] for param in entry.get("parameters", [])]
            if len(args) > len(names):
                raise TypeError(f"Expected at most {len(names)} positional arguments")
            kwargs.update(dict(zip(names, args)))
        return self._generate(output_id, **kwargs)

    return method


_DEFAULT_RANDOMIZER = LibRandom()


def _make_function(output_id: str) -> Callable[..., Any]:
    def function(*args: Any, **kwargs: Any) -> Any:
        return getattr(_DEFAULT_RANDOMIZER, _snake_name(_api_name(_entry_by_id(output_id))))(*args, **kwargs)

    return function


def _json_safe(value: Any) -> Any:
    if isinstance(value, bytes):
        return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")
    return value


for _entry in _CATALOG.get("types", []):
    _camel = _api_name(_entry)
    _snake = _snake_name(_camel)
    _output_id = _entry["id"]
    if not hasattr(LibRandom, _snake):
        setattr(LibRandom, _snake, _make_method(_output_id))
    _alias = "get" + _camel[0].upper() + _camel[1:]
    _alias_snake = _snake_name(_alias)
    if not hasattr(LibRandom, _alias_snake):
        setattr(LibRandom, _alias_snake, _make_method(_output_id))
    globals()[_snake] = _make_function(_output_id)
    globals()[_camel] = globals()[_snake]
    globals()[_alias] = globals()[_snake]


randomWords = random_words = lambda count=1, locale="en-US", allowAdult=False: _DEFAULT_RANDOMIZER.random_words(count=count, locale=locale, allowAdult=allowAdult)
getRandomWords = randomWords


__all__ = ["LibRandom", "randomWords", "random_words", "getRandomWords"]
for _entry in _CATALOG.get("types", []):
    _camel = _api_name(_entry)
    _snake = _snake_name(_camel)
    _alias = "get" + _camel[0].upper() + _camel[1:]
    __all__.extend([_camel, _snake, _alias])
