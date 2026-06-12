import { randomBytes, randomInt as nodeRandomInt } from "node:crypto";

function validateRange(min: number, max: number): void {
  if (min > max) {
    throw new RangeError("Invalid range: min must be less than or equal to max");
  }
}

function validateChar(name: string, value: string): number {
  if (value.length !== 1) {
    throw new RangeError(`Invalid character range: ${name} must be one character`);
  }
  const code = value.charCodeAt(0);
  if (code < 32 || code > 126) {
    throw new RangeError(`Invalid character range: ${name} must be printable ASCII`);
  }
  return code;
}

function randomUnitFloat(): number {
  const bytes = randomBytes(8);
  const value = bytes.readBigUInt64BE() >> 11n;
  return Number(value) / 9007199254740992;
}

export function randomInt(min = 0, max = 99): number {
  validateRange(min, max);
  return nodeRandomInt(min, max + 1);
}

export function randomFloat(min = 0.0, max = 1.0): number {
  validateRange(min, max);
  if (min === max) {
    return min;
  }
  return min + randomUnitFloat() * (max - min);
}

export function randomChar(min = "A", max = "Z"): string {
  const minCode = validateChar("min", min);
  const maxCode = validateChar("max", max);
  validateRange(minCode, maxCode);
  return String.fromCharCode(randomInt(minCode, maxCode));
}
