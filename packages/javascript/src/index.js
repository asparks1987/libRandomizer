"use strict";

const crypto = require("node:crypto");

function validateRange(min, max) {
  if (min > max) {
    throw new RangeError("Invalid range: min must be less than or equal to max");
  }
}

function validateChar(name, value) {
  if (typeof value !== "string" || value.length !== 1) {
    throw new RangeError(`Invalid character range: ${name} must be one character`);
  }
  const code = value.charCodeAt(0);
  if (code < 32 || code > 126) {
    throw new RangeError(`Invalid character range: ${name} must be printable ASCII`);
  }
  return code;
}

function randomUnitFloat() {
  const bytes = crypto.randomBytes(8);
  const value = bytes.readBigUInt64BE() >> 11n;
  return Number(value) / 9007199254740992;
}

function randomInt(min = 0, max = 99) {
  validateRange(min, max);
  return crypto.randomInt(min, max + 1);
}

function randomFloat(min = 0.0, max = 1.0) {
  validateRange(min, max);
  if (min === max) {
    return min;
  }
  return min + randomUnitFloat() * (max - min);
}

function randomChar(min = "A", max = "Z") {
  const minCode = validateChar("min", min);
  const maxCode = validateChar("max", max);
  validateRange(minCode, maxCode);
  return String.fromCharCode(randomInt(minCode, maxCode));
}

module.exports = {
  randomInt,
  randomFloat,
  randomChar,
};
