using System;
using System.Security.Cryptography;

namespace LibRandomizer
{
    public static class Randomizer
    {
        private const int PrintableAsciiMin = 32;
        private const int PrintableAsciiMax = 126;

        public static int RandomInt() => RandomInt(0, 99);

        public static int RandomInt(int min, int max)
        {
            ValidateRange(min, max);
            return RandomNumberGenerator.GetInt32(min, max + 1);
        }

        public static double RandomFloat() => RandomFloat(0.0, 1.0);

        public static double RandomFloat(double min, double max)
        {
            ValidateRange(min, max);
            if (min == max)
            {
                return min;
            }

            Span<byte> bytes = stackalloc byte[8];
            RandomNumberGenerator.Fill(bytes);
            ulong raw = BitConverter.ToUInt64(bytes);
            double unit = (raw >> 11) / (double)(1UL << 53);
            return min + unit * (max - min);
        }

        public static char RandomChar() => RandomChar('A', 'Z');

        public static char RandomChar(char min, char max)
        {
            int minCode = ValidateChar(nameof(min), min);
            int maxCode = ValidateChar(nameof(max), max);
            ValidateRange(minCode, maxCode);
            return (char)RandomInt(minCode, maxCode);
        }

        private static void ValidateRange(double min, double max)
        {
            if (min > max)
            {
                throw new ArgumentOutOfRangeException(nameof(min), "Invalid range: min must be less than or equal to max");
            }
        }

        private static int ValidateChar(string name, char value)
        {
            int code = value;
            if (code < PrintableAsciiMin || code > PrintableAsciiMax)
            {
                throw new ArgumentOutOfRangeException(name, "Invalid character range: value must be printable ASCII");
            }
            return code;
        }
    }
}
