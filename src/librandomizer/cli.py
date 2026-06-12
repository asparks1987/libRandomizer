"""JSON command line interface for libRandomizer."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Sequence

from .core import LibRandom


class CliUsageError(ValueError):
    """Raised when command line arguments are invalid."""


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise CliUsageError(message)


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    try:
        args = parser.parse_args(argv)
        generator = LibRandom()
        value = _generate_value(generator, args)
    except (CliUsageError, ValueError) as exc:
        _write_json({"error": str(exc)}, stream=sys.stderr)
        return 1

    _write_json({"type": args.random_type, "value": value})
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = JsonArgumentParser(
        prog="librandom",
        description="Generate Alpha v1 random values as JSON.",
    )
    subparsers = parser.add_subparsers(
        dest="random_type",
        parser_class=JsonArgumentParser,
        required=True,
    )

    int_parser = subparsers.add_parser("int", help="Generate a random integer.")
    int_parser.add_argument("--min", type=int, default=0)
    int_parser.add_argument("--max", type=int, default=99)

    float_parser = subparsers.add_parser("float", help="Generate a random float.")
    float_parser.add_argument("--min", type=float, default=0.0)
    float_parser.add_argument("--max", type=float, default=1.0)

    char_parser = subparsers.add_parser("char", help="Generate a random character.")
    char_parser.add_argument("--min", default="A")
    char_parser.add_argument("--max", default="Z")

    return parser


def _generate_value(generator: LibRandom, args: argparse.Namespace) -> int | float | str:
    if args.random_type == "int":
        return generator.random_int(min=args.min, max=args.max)
    if args.random_type == "float":
        return generator.random_float(min=args.min, max=args.max)
    if args.random_type == "char":
        return generator.random_char(min=args.min, max=args.max)

    raise ValueError(f"Unsupported random type: {args.random_type}")


def _write_json(payload: dict[str, Any], stream: Any = sys.stdout) -> None:
    print(json.dumps(payload, separators=(",", ":")), file=stream)


if __name__ == "__main__":
    raise SystemExit(main())
