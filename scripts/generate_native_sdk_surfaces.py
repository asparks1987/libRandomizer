from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "spec" / "beta" / "output-types.json").read_text(encoding="utf-8"))


def api(entry: dict) -> str:
    return entry["api"].split("(", 1)[0]


def pascal(name: str) -> str:
    return api({"api": name + "()"})[0].upper() + api({"api": name + "()"})[1:]


def snake(camel: str) -> str:
    first = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", camel)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", first).lower()


def ret(entry: dict) -> str:
    return entry["returns"]["type"]


def js_value(entry: dict) -> str:
    r = ret(entry)
    if entry["id"] == "int":
        return "randomInt()"
    if entry["id"] == "float":
        return "randomFloat()"
    if entry["id"] == "char":
        return "randomChar()"
    if r == "integer":
        return "randomInt()"
    if r in {"float", "decimal"}:
        return "randomFloat()"
    if r == "boolean":
        return "randomInt(0, 1) === 1"
    if r == "array":
        return "[randomString(8)]"
    if r == "object":
        return "({ value: randomString(8) })"
    if r == "bytes":
        return "randomBytes(16)"
    return "randomString(12)"


def generate_js() -> None:
    lines = [
        '"use strict";',
        "",
        'const crypto = require("node:crypto");',
        "",
        "function validateRange(min, max) { if (min > max) throw new RangeError(\"Invalid range: min must be less than or equal to max\"); }",
        "function randomInt(min = 0, max = 99) { validateRange(min, max); return crypto.randomInt(min, max + 1); }",
        "function randomFloat(min = 0.0, max = 1.0) { validateRange(min, max); if (min === max) return min; const raw = crypto.randomBytes(8).readBigUInt64BE() >> 11n; return min + (Number(raw) / 9007199254740992) * (max - min); }",
        "function randomChar(min = \"A\", max = \"Z\") { if (min.length !== 1 || max.length !== 1) throw new RangeError(\"Invalid character range: bounds must be one character\"); return String.fromCharCode(randomInt(min.charCodeAt(0), max.charCodeAt(0))); }",
        "function randomString(length = 12) { if (!Number.isInteger(length) || length < 0) throw new RangeError(\"Invalid size: length must be a non-negative integer within supported limits\"); const alphabet = \"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\"; let out = \"\"; for (let i = 0; i < length; i++) out += alphabet[randomInt(0, alphabet.length - 1)]; return out; }",
        "function randomBytes(length = 16) { return crypto.randomBytes(length); }",
        "const getRandomInt = randomInt;",
        "const getRandomFloat = randomFloat;",
        "const getRandomChar = randomChar;",
        "const getRandomString = randomString;",
        "const getRandomBytes = randomBytes;",
    ]
    exports = ["randomInt", "getRandomInt", "randomFloat", "getRandomFloat", "randomChar", "getRandomChar", "randomString", "getRandomString", "randomBytes", "getRandomBytes"]
    for entry in CATALOG["types"]:
        name = api(entry)
        if name in exports:
            continue
        lines.append(f"function {name}() {{ return {js_value(entry)}; }}")
        lines.append(f"const get{name[0].upper() + name[1:]} = {name};")
        exports.extend([name, f"get{name[0].upper() + name[1:]}"])
    lines.append("module.exports = {")
    lines.extend(f"  {name}," for name in exports)
    lines.append("};")
    (ROOT / "packages" / "javascript" / "src" / "index.js").write_text("\n".join(lines) + "\n", encoding="utf-8")

    dts = []
    for name in exports:
        if name.startswith("get") and name[3:4].isupper():
            dts.append(f"export function {name}(): unknown;")
        elif name == "randomInt":
            dts.append("export function randomInt(min?: number, max?: number): number;")
        elif name == "randomFloat":
            dts.append("export function randomFloat(min?: number, max?: number): number;")
        elif name == "randomChar":
            dts.append("export function randomChar(min?: string, max?: string): string;")
        elif name == "randomString":
            dts.append("export function randomString(length?: number): string;")
        elif name == "randomBytes":
            dts.append("export function randomBytes(length?: number): Buffer;")
        else:
            dts.append(f"export function {name}(): unknown;")
    (ROOT / "packages" / "javascript" / "src" / "index.d.ts").write_text("\n".join(dts) + "\n", encoding="utf-8")

    ts = [
        'import { randomBytes as nodeRandomBytes, randomInt as nodeRandomInt } from "node:crypto";',
        "",
        "function validateRange(min: number, max: number): void { if (min > max) throw new RangeError(\"Invalid range: min must be less than or equal to max\"); }",
        "export function randomInt(min = 0, max = 99): number { validateRange(min, max); return nodeRandomInt(min, max + 1); }",
        "export function randomFloat(min = 0.0, max = 1.0): number { validateRange(min, max); if (min === max) return min; const raw = nodeRandomBytes(8).readBigUInt64BE() >> 11n; return min + (Number(raw) / 9007199254740992) * (max - min); }",
        "export function randomChar(min = \"A\", max = \"Z\"): string { if (min.length !== 1 || max.length !== 1) throw new RangeError(\"Invalid character range: bounds must be one character\"); return String.fromCharCode(randomInt(min.charCodeAt(0), max.charCodeAt(0))); }",
        "export function randomString(length = 12): string { if (!Number.isInteger(length) || length < 0) throw new RangeError(\"Invalid size: length must be a non-negative integer within supported limits\"); const alphabet = \"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\"; let out = \"\"; for (let i = 0; i < length; i++) out += alphabet[randomInt(0, alphabet.length - 1)]; return out; }",
        "export function randomBytes(length = 16): Buffer { return nodeRandomBytes(length); }",
        "export const getRandomInt = randomInt;",
        "export const getRandomFloat = randomFloat;",
        "export const getRandomChar = randomChar;",
        "export const getRandomString = randomString;",
        "export const getRandomBytes = randomBytes;",
    ]
    seen = {"randomInt", "randomFloat", "randomChar", "randomString", "randomBytes"}
    for entry in CATALOG["types"]:
        name = api(entry)
        if name in seen:
            continue
        ts.append(f"export function {name}(): unknown {{ return {js_value(entry)}; }}")
        ts.append(f"export const get{name[0].upper() + name[1:]} = {name};")
        seen.add(name)
    (ROOT / "packages" / "typescript" / "src" / "index.ts").write_text("\n".join(ts) + "\n", encoding="utf-8")


def generate_python_package_readme() -> None:
    text = "# libRandomizer Python SDK\n\nV1 public beta exposes all catalog `randomX()` functions from `librandomizer`.\n\n```python\nfrom librandomizer import randomInt, randomString, randomColorName\n\nprint(randomInt())\nprint(randomString(5))\nprint(randomColorName())\n```\n"
    (ROOT / "packages" / "python" / "README.md").write_text(text, encoding="utf-8")


def generate_ruby() -> None:
    names = [api(entry) for entry in CATALOG["types"]]
    lines = [
        'require "securerandom"',
        "",
        "module LibRandomizer",
        "  ALPHABET = ('a'..'z').to_a + ('A'..'Z').to_a + ('0'..'9').to_a",
        "  def self.randomInt(min = 0, max = 99) = SecureRandom.random_number(max - min + 1) + min",
        "  def self.randomFloat(min = 0.0, max = 1.0) = min == max ? min : min + SecureRandom.random_number * (max - min)",
        "  def self.randomChar(min = 'A', max = 'Z') = randomInt(min.ord, max.ord).chr",
        "  def self.randomString(length = 12) = Array.new(length) { ALPHABET[SecureRandom.random_number(ALPHABET.length)] }.join",
        "  def self.getRandomInt = randomInt",
        "  def self.getRandomFloat = randomFloat",
        "  def self.getRandomChar = randomChar",
        "  def self.getRandomString = randomString",
    ]
    for name in names:
        if name in {"randomInt", "randomFloat", "randomChar", "randomString"}:
            continue
        lines.append(f"  def self.{name} = randomString(12)")
        lines.append(f"  def self.get{name[0].upper() + name[1:]} = {name}")
    lines.append("end")
    (ROOT / "packages" / "ruby" / "lib" / "librandomizer.rb").write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_php() -> None:
    lines = [
        "<?php",
        "declare(strict_types=1);",
        "namespace LibRandomizer;",
        "function randomInt(int $min = 0, int $max = 99): int { if ($min > $max) { throw new \\InvalidArgumentException('Invalid range: min must be less than or equal to max'); } return random_int($min, $max); }",
        "function randomFloat(float $min = 0.0, float $max = 1.0): float { if ($min > $max) { throw new \\InvalidArgumentException('Invalid range: min must be less than or equal to max'); } if ($min === $max) { return $min; } return $min + (random_int(0, PHP_INT_MAX) / PHP_INT_MAX) * ($max - $min); }",
        "function randomChar(string $min = 'A', string $max = 'Z'): string { return chr(randomInt(ord($min), ord($max))); }",
        "function randomString(int $length = 12): string { $alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'; $out = ''; for ($i = 0; $i < $length; $i++) { $out .= $alphabet[randomInt(0, strlen($alphabet) - 1)]; } return $out; }",
        "function getRandomInt(): int { return randomInt(); }",
        "function getRandomFloat(): float { return randomFloat(); }",
        "function getRandomChar(): string { return randomChar(); }",
        "function getRandomString(): string { return randomString(); }",
    ]
    for entry in CATALOG["types"]:
        name = api(entry)
        if name in {"randomInt", "randomFloat", "randomChar", "randomString"}:
            continue
        lines.append(f"function {name}(): mixed {{ return randomString(12); }}")
        lines.append(f"function get{name[0].upper() + name[1:]}(): mixed {{ return {name}(); }}")
    (ROOT / "packages" / "php" / "src" / "functions.php").write_text("\n".join(lines) + "\n", encoding="utf-8")


def java_value(entry: dict) -> str:
    r = ret(entry)
    if entry["id"] == "int":
        return "randomInt()"
    if entry["id"] == "float":
        return "randomFloat()"
    if entry["id"] == "char":
        return "String.valueOf(randomChar())"
    if r == "integer":
        return "randomInt()"
    if r in {"float", "decimal"}:
        return "randomFloat()"
    if r == "boolean":
        return "randomInt(0, 1) == 1"
    if r == "array":
        return "java.util.List.of(randomString())"
    if r == "object":
        return "java.util.Map.of(\"value\", randomString())"
    return "randomString()"


def generate_java() -> None:
    lines = [
        "package io.github.librandomizer;",
        "",
        "import java.security.SecureRandom;",
        "",
        "public final class LibRandomizer {",
        "    private static final SecureRandom RNG = new SecureRandom();",
        "    private static final String ALPHABET = \"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\";",
        "    private LibRandomizer() {}",
        "    public static int randomInt() { return randomInt(0, 99); }",
        "    public static int randomInt(int min, int max) { if (min > max) throw new IllegalArgumentException(\"Invalid range: min must be less than or equal to max\"); return RNG.nextInt((max - min) + 1) + min; }",
        "    public static double randomFloat() { return randomFloat(0.0, 1.0); }",
        "    public static double randomFloat(double min, double max) { if (min > max) throw new IllegalArgumentException(\"Invalid range: min must be less than or equal to max\"); if (min == max) return min; return min + RNG.nextDouble() * (max - min); }",
        "    public static char randomChar() { return randomChar('A', 'Z'); }",
        "    public static char randomChar(char min, char max) { return (char) randomInt((int) min, (int) max); }",
        "    public static String randomString() { return randomString(12); }",
        "    public static String randomString(int length) { StringBuilder out = new StringBuilder(); for (int i = 0; i < length; i++) out.append(ALPHABET.charAt(randomInt(0, ALPHABET.length() - 1))); return out.toString(); }",
        "    public static int getRandomInt() { return randomInt(); }",
        "    public static double getRandomFloat() { return randomFloat(); }",
        "    public static char getRandomChar() { return randomChar(); }",
        "    public static String getRandomString() { return randomString(); }",
    ]
    for entry in CATALOG["types"]:
        name = api(entry)
        if name in {"randomInt", "randomFloat", "randomChar", "randomString"}:
            continue
        lines.append(f"    public static Object {name}() {{ return {java_value(entry)}; }}")
        lines.append(f"    public static Object get{name[0].upper() + name[1:]}() {{ return {name}(); }}")
    lines.append("}")
    (ROOT / "packages" / "java" / "src" / "main" / "java" / "io" / "github" / "librandomizer" / "LibRandomizer.java").write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_csharp() -> None:
    lines = [
        "using System;",
        "using System.Security.Cryptography;",
        "namespace LibRandomizer { public static class Randomizer {",
        "private const string Alphabet = \"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\";",
        "public static int RandomInt(int min = 0, int max = 99) { if (min > max) throw new ArgumentOutOfRangeException(nameof(min), \"Invalid range: min must be less than or equal to max\"); return RandomNumberGenerator.GetInt32(min, max + 1); }",
        "public static double RandomFloat(double min = 0.0, double max = 1.0) { if (min > max) throw new ArgumentOutOfRangeException(nameof(min)); if (min == max) return min; Span<byte> bytes = stackalloc byte[8]; RandomNumberGenerator.Fill(bytes); ulong raw = BitConverter.ToUInt64(bytes); double unit = (raw >> 11) / (double)(1UL << 53); return min + unit * (max - min); }",
        "public static char RandomChar(char min = 'A', char max = 'Z') => (char)RandomInt(min, max);",
        "public static string RandomString(int length = 12) { var chars = new char[length]; for (int i = 0; i < length; i++) chars[i] = Alphabet[RandomInt(0, Alphabet.Length - 1)]; return new string(chars); }",
        "public static int GetRandomInt() => RandomInt();",
        "public static double GetRandomFloat() => RandomFloat();",
        "public static char GetRandomChar() => RandomChar();",
        "public static string GetRandomString() => RandomString();",
    ]
    for entry in CATALOG["types"]:
        name = pascal(api(entry))
        if name in {"RandomInt", "RandomFloat", "RandomChar", "RandomString"}:
            continue
        lines.append(f"public static object {name}() => RandomString();")
        lines.append(f"public static object Get{name}() => {name}();")
    lines.append("} }")
    (ROOT / "packages" / "csharp" / "LibRandomizer.cs").write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_go() -> None:
    lines = [
        "package librandomizer",
        'import ("crypto/rand"; "math/big")',
        "const alphabet = \"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\"",
        "func RandomIntRange(min int, max int) (int, error) { if min > max { return 0, nil }; n, err := rand.Int(rand.Reader, big.NewInt(int64(max-min+1))); if err != nil { return 0, err }; return int(n.Int64()) + min, nil }",
        "func RandomInt() int { v, _ := RandomIntRange(0, 99); return v }",
        "func RandomFloat() float64 { v, _ := RandomIntRange(0, 900719925); return float64(v) / 900719925.0 }",
        "func RandomChar() rune { v, _ := RandomIntRange(int('A'), int('Z')); return rune(v) }",
        "func RandomString() string { out := make([]byte, 12); for i := range out { v, _ := RandomIntRange(0, len(alphabet)-1); out[i] = alphabet[v] }; return string(out) }",
        "func GetRandomInt() int { return RandomInt() }",
        "func GetRandomFloat() float64 { return RandomFloat() }",
        "func GetRandomChar() rune { return RandomChar() }",
        "func GetRandomString() string { return RandomString() }",
    ]
    for entry in CATALOG["types"]:
        name = pascal(api(entry))
        if name in {"RandomInt", "RandomFloat", "RandomChar", "RandomString"}:
            continue
        lines.append(f"func {name}() any {{ return RandomString() }}")
        lines.append(f"func Get{name}() any {{ return {name}() }}")
    (ROOT / "packages" / "go" / "randomizer.go").write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_rust() -> None:
    lines = [
        "use rand::rngs::OsRng;",
        "use rand::Rng;",
        "const ALPHABET: &[u8] = b\"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\";",
        "pub fn random_int() -> i64 { OsRng.gen_range(0..=99) }",
        "pub fn random_float() -> f64 { OsRng.gen_range(0.0..=1.0) }",
        "pub fn random_char() -> char { OsRng.gen_range(b'A'..=b'Z') as char }",
        "pub fn random_string() -> String { (0..12).map(|_| ALPHABET[OsRng.gen_range(0..ALPHABET.len())] as char).collect() }",
        "pub fn get_random_int() -> i64 { random_int() }",
        "pub fn get_random_float() -> f64 { random_float() }",
        "pub fn get_random_char() -> char { random_char() }",
        "pub fn get_random_string() -> String { random_string() }",
    ]
    for entry in CATALOG["types"]:
        name = snake(api(entry))
        if name in {"random_int", "random_float", "random_char", "random_string"}:
            continue
        lines.append(f"pub fn {name}() -> String {{ random_string() }}")
        lines.append(f"pub fn get_{name}() -> String {{ {name}() }}")
    (ROOT / "packages" / "rust" / "src" / "lib.rs").write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_kotlin() -> None:
    lines = [
        "package io.github.librandomizer",
        "import java.security.SecureRandom",
        "object LibRandomizer {",
        "private val rng = SecureRandom()",
        "private const val alphabet = \"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\"",
        "fun randomInt(min: Int = 0, max: Int = 99): Int { require(min <= max); return rng.nextInt(max - min + 1) + min }",
        "fun randomFloat(min: Double = 0.0, max: Double = 1.0): Double { require(min <= max); return if (min == max) min else min + rng.nextDouble() * (max - min) }",
        "fun randomChar(min: Char = 'A', max: Char = 'Z'): Char = randomInt(min.code, max.code).toChar()",
        "fun randomString(length: Int = 12): String = (0 until length).map { alphabet[randomInt(0, alphabet.length - 1)] }.joinToString(\"\")",
        "fun getRandomInt(): Int = randomInt()",
        "fun getRandomFloat(): Double = randomFloat()",
        "fun getRandomChar(): Char = randomChar()",
        "fun getRandomString(): String = randomString()",
    ]
    for entry in CATALOG["types"]:
        name = api(entry)
        if name in {"randomInt", "randomFloat", "randomChar", "randomString"}:
            continue
        lines.append(f"fun {name}(): Any = randomString()")
        lines.append(f"fun get{name[0].upper() + name[1:]}(): Any = {name}()")
    lines.append("}")
    (ROOT / "packages" / "kotlin" / "src" / "main" / "kotlin" / "io" / "github" / "librandomizer" / "LibRandomizer.kt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_swift() -> None:
    lines = [
        "import Foundation",
        "public enum LibRandomizer {",
        "static let alphabet = Array(\"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\")",
        "public static func randomInt(min: Int = 0, max: Int = 99) -> Int { Int.random(in: min...max) }",
        "public static func randomFloat(min: Double = 0.0, max: Double = 1.0) -> Double { Double.random(in: min...max) }",
        "public static func randomChar(min: Character = \"A\", max: Character = \"Z\") -> Character { alphabet[randomInt(min: 0, max: alphabet.count - 1)] }",
        "public static func randomString(length: Int = 12) -> String { String((0..<length).map { _ in alphabet[randomInt(min: 0, max: alphabet.count - 1)] }) }",
        "public static func getRandomInt() -> Int { randomInt() }",
        "public static func getRandomFloat() -> Double { randomFloat() }",
        "public static func getRandomChar() -> Character { randomChar() }",
        "public static func getRandomString() -> String { randomString() }",
    ]
    for entry in CATALOG["types"]:
        name = api(entry)
        if name in {"randomInt", "randomFloat", "randomChar", "randomString"}:
            continue
        lines.append(f"public static func {name}() -> Any {{ randomString() }}")
        lines.append(f"public static func get{name[0].upper() + name[1:]}() -> Any {{ {name}() }}")
    lines.append("}")
    (ROOT / "packages" / "swift" / "Sources" / "LibRandomizer" / "LibRandomizer.swift").write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_dart() -> None:
    lines = [
        "import 'dart:math';",
        "final _rng = Random.secure();",
        "const _alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';",
        "int randomInt([int min = 0, int max = 99]) => min + _rng.nextInt(max - min + 1);",
        "double randomFloat([double min = 0.0, double max = 1.0]) => min == max ? min : min + _rng.nextDouble() * (max - min);",
        "String randomChar([String min = 'A', String max = 'Z']) => String.fromCharCode(randomInt(min.codeUnitAt(0), max.codeUnitAt(0)));",
        "String randomString([int length = 12]) => List.generate(length, (_) => _alphabet[randomInt(0, _alphabet.length - 1)]).join();",
        "int getRandomInt() => randomInt();",
        "double getRandomFloat() => randomFloat();",
        "String getRandomChar() => randomChar();",
        "String getRandomString() => randomString();",
    ]
    for entry in CATALOG["types"]:
        name = api(entry)
        if name in {"randomInt", "randomFloat", "randomChar", "randomString"}:
            continue
        lines.append(f"Object {name}() => randomString();")
        lines.append(f"Object get{name[0].upper() + name[1:]}() => {name}();")
    (ROOT / "packages" / "dart" / "lib" / "librandomizer.dart").write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_r() -> None:
    lines = [
        "random_int <- function(min = 0, max = 99) sample(seq(min, max), 1)",
        "random_float <- function(min = 0.0, max = 1.0) runif(1, min, max)",
        "random_char <- function(min = 'A', max = 'Z') intToUtf8(random_int(utf8ToInt(min), utf8ToInt(max)))",
        "random_string <- function(length = 12) paste(sample(c(letters, LETTERS, 0:9), length, replace = TRUE), collapse = '')",
    ]
    lines.extend([
        "get_random_int <- function() random_int()",
        "get_random_float <- function() random_float()",
        "get_random_char <- function() random_char()",
        "get_random_string <- function() random_string()",
    ])
    exports = ["random_int", "get_random_int", "random_float", "get_random_float", "random_char", "get_random_char", "random_string", "get_random_string"]
    for entry in CATALOG["types"]:
        name = snake(api(entry))
        if name in exports:
            continue
        lines.append(f"{name} <- function() random_string()")
        lines.append(f"get_{name} <- function() {name}()")
        exports.extend([name, f"get_{name}"])
    (ROOT / "packages" / "r" / "R" / "librandomizer.R").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (ROOT / "packages" / "r" / "NAMESPACE").write_text("\n".join(f"export({name})" for name in exports) + "\n", encoding="utf-8")


def generate_c_cpp() -> None:
    c_header = [
        "#pragma once",
        "#ifdef __cplusplus",
        'extern "C" {',
        "#endif",
        "int librandom_random_int(void);",
        "double librandom_random_float(void);",
        "char librandom_random_char(void);",
        "int librandom_get_random_int(void);",
        "double librandom_get_random_float(void);",
        "char librandom_get_random_char(void);",
    ]
    c_source = [
        '#include "librandom.h"',
        "#include <stdint.h>",
        "#ifdef _WIN32",
        "#include <windows.h>",
        "#include <bcrypt.h>",
        "#else",
        "#include <fcntl.h>",
        "#include <unistd.h>",
        "#endif",
        "static uint32_t librandom_u32(void) { uint32_t value = 0;",
        "#ifdef _WIN32",
        "BCryptGenRandom(NULL, (PUCHAR)&value, sizeof(value), BCRYPT_USE_SYSTEM_PREFERRED_RNG);",
        "#else",
        "int fd = open(\"/dev/urandom\", O_RDONLY); if (fd >= 0) { (void)read(fd, &value, sizeof(value)); close(fd); }",
        "#endif",
        "return value; }",
        "int librandom_random_int(void) { return (int)(librandom_u32() % 100u); }",
        "double librandom_random_float(void) { return (double)librandom_u32() / 4294967295.0; }",
        "char librandom_random_char(void) { return (char)('A' + librandom_random_int() % 26); }",
        "int librandom_get_random_int(void) { return librandom_random_int(); }",
        "double librandom_get_random_float(void) { return librandom_random_float(); }",
        "char librandom_get_random_char(void) { return librandom_random_char(); }",
    ]
    for entry in CATALOG["types"]:
        fn = "librandom_" + snake(api(entry))
        if fn in {"librandom_random_int", "librandom_random_float", "librandom_random_char"}:
            continue
        c_header.append(f"const char* {fn}(void);")
        c_source.append(f"const char* {fn}(void) {{ return \"beta\"; }}")
    c_header.extend(["#ifdef __cplusplus", "}", "#endif"])
    (ROOT / "packages" / "c" / "include" / "librandom.h").write_text("\n".join(c_header) + "\n", encoding="utf-8")
    (ROOT / "packages" / "c" / "src" / "librandom.c").write_text("\n".join(c_source) + "\n", encoding="utf-8")

    cpp = [
        "#pragma once",
        "#include <random>",
        "#include <string>",
        "namespace librandom {",
        "inline int randomInt(int min = 0, int max = 99) { static std::random_device rd; std::uniform_int_distribution<int> dist(min, max); return dist(rd); }",
        "inline double randomFloat(double min = 0.0, double max = 1.0) { static std::random_device rd; std::uniform_real_distribution<double> dist(min, max); return dist(rd); }",
        "inline char randomChar(char min = 'A', char max = 'Z') { return static_cast<char>(randomInt(min, max)); }",
        "inline std::string randomString(int length = 12) { const std::string alphabet = \"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\"; std::string out; for (int i = 0; i < length; ++i) out += alphabet[randomInt(0, (int)alphabet.size() - 1)]; return out; }",
        "inline int getRandomInt() { return randomInt(); }",
        "inline double getRandomFloat() { return randomFloat(); }",
        "inline char getRandomChar() { return randomChar(); }",
        "inline std::string getRandomString() { return randomString(); }",
    ]
    for entry in CATALOG["types"]:
        name = api(entry)
        if name in {"randomInt", "randomFloat", "randomChar", "randomString"}:
            continue
        cpp.append(f"inline std::string {name}() {{ return randomString(); }}")
        cpp.append(f"inline std::string get{name[0].upper() + name[1:]}() {{ return {name}(); }}")
    cpp.append("}")
    (ROOT / "packages" / "cpp" / "include" / "librandom" / "random.hpp").write_text("\n".join(cpp) + "\n", encoding="utf-8")


def main() -> None:
    generate_js()
    generate_python_package_readme()
    generate_ruby()
    generate_php()
    generate_java()
    generate_csharp()
    generate_go()
    generate_rust()
    generate_kotlin()
    generate_swift()
    generate_dart()
    generate_r()
    generate_c_cpp()


if __name__ == "__main__":
    main()
