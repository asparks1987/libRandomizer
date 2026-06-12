package io.github.librandomizer

import java.security.SecureRandom

object LibRandomizer {
    private val rng = SecureRandom()

    @JvmStatic
    fun randomInt(min: Int = 0, max: Int = 99): Int {
        require(min <= max) { "Invalid range: min must be less than or equal to max" }
        return rng.nextInt((max - min) + 1) + min
    }

    @JvmStatic
    fun randomFloat(min: Double = 0.0, max: Double = 1.0): Double {
        require(min <= max) { "Invalid range: min must be less than or equal to max" }
        if (min == max) return min
        return min + rng.nextDouble() * (max - min)
    }

    @JvmStatic
    fun randomChar(min: Char = 'A', max: Char = 'Z'): Char {
        require(min.code in 32..126) { "Invalid character range: min must be printable ASCII" }
        require(max.code in 32..126) { "Invalid character range: max must be printable ASCII" }
        return randomInt(min.code, max.code).toChar()
    }
}
