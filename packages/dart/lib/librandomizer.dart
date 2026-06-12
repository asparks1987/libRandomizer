import 'dart:math';

final Random _rng = Random.secure();

int randomInt([int min = 0, int max = 99]) {
  _validateRange(min, max);
  return min + _rng.nextInt(max - min + 1);
}

double randomFloat([double min = 0.0, double max = 1.0]) {
  _validateRange(min, max);
  if (min == max) {
    return min;
  }
  return min + _rng.nextDouble() * (max - min);
}

String randomChar([String min = 'A', String max = 'Z']) {
  final minCode = _validateChar('min', min);
  final maxCode = _validateChar('max', max);
  _validateRange(minCode, maxCode);
  return String.fromCharCode(randomInt(minCode, maxCode));
}

void _validateRange(num min, num max) {
  if (min > max) {
    throw RangeError('Invalid range: min must be less than or equal to max');
  }
}

int _validateChar(String name, String value) {
  if (value.length != 1) {
    throw RangeError('Invalid character range: $name must be one character');
  }
  final code = value.codeUnitAt(0);
  if (code < 32 || code > 126) {
    throw RangeError('Invalid character range: $name must be printable ASCII');
  }
  return code;
}
