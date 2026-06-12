<?php

declare(strict_types=1);

namespace LibRandomizer;

function randomInt(int $min = 0, int $max = 99): int
{
    validateRange($min, $max);
    return random_int($min, $max);
}

function randomFloat(float $min = 0.0, float $max = 1.0): float
{
    validateRange($min, $max);
    if ($min === $max) {
        return $min;
    }

    $bytes = random_bytes(8);
    $parts = unpack('J', $bytes);
    $raw = $parts[1] >> 11;
    $unit = $raw / 9007199254740992.0;
    return $min + $unit * ($max - $min);
}

function randomChar(string $min = 'A', string $max = 'Z'): string
{
    $minCode = validateChar('min', $min);
    $maxCode = validateChar('max', $max);
    validateRange($minCode, $maxCode);
    return chr(randomInt($minCode, $maxCode));
}

function validateRange(int|float $min, int|float $max): void
{
    if ($min > $max) {
        throw new \InvalidArgumentException('Invalid range: min must be less than or equal to max');
    }
}

function validateChar(string $name, string $value): int
{
    if (strlen($value) !== 1) {
        throw new \InvalidArgumentException("Invalid character range: {$name} must be one character");
    }
    $code = ord($value);
    if ($code < 32 || $code > 126) {
        throw new \InvalidArgumentException("Invalid character range: {$name} must be printable ASCII");
    }
    return $code;
}
