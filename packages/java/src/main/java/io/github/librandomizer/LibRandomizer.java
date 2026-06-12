package io.github.librandomizer;

import java.security.SecureRandom;

public final class LibRandomizer {
    private static final SecureRandom RNG = new SecureRandom();
    private static final int PRINTABLE_ASCII_MIN = 32;
    private static final int PRINTABLE_ASCII_MAX = 126;

    private LibRandomizer() {
    }

    public static int randomInt() {
        return randomInt(0, 99);
    }

    public static int randomInt(int min, int max) {
        validateRange(min, max);
        return RNG.nextInt((max - min) + 1) + min;
    }

    public static double randomFloat() {
        return randomFloat(0.0, 1.0);
    }

    public static double randomFloat(double min, double max) {
        validateRange(min, max);
        if (min == max) {
            return min;
        }
        return min + RNG.nextDouble() * (max - min);
    }

    public static char randomChar() {
        return randomChar('A', 'Z');
    }

    public static char randomChar(char min, char max) {
        int minCode = validateChar("min", min);
        int maxCode = validateChar("max", max);
        validateRange(minCode, maxCode);
        return (char) randomInt(minCode, maxCode);
    }

    private static void validateRange(double min, double max) {
        if (min > max) {
            throw new IllegalArgumentException("Invalid range: min must be less than or equal to max");
        }
    }

    private static int validateChar(String name, char value) {
        int code = value;
        if (code < PRINTABLE_ASCII_MIN || code > PRINTABLE_ASCII_MAX) {
            throw new IllegalArgumentException("Invalid character range: " + name + " must be printable ASCII");
        }
        return code;
    }
}
