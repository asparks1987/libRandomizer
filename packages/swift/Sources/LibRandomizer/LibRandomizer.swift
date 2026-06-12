import Foundation

#if canImport(Security)
import Security
#elseif canImport(WinSDK)
import WinSDK
#elseif canImport(Glibc)
import Glibc
#endif

public enum LibRandomizer {
    public static func randomInt() -> Int {
        try! randomInt(0, 99)
    }

    public static func randomInt(_ min: Int, _ max: Int) throws -> Int {
        guard min <= max else {
            throw RandomizerError.invalidRange
        }
        let span = UInt64(max - min + 1)
        let value = try randomUInt64(below: span)
        return min + Int(value)
    }

    public static func randomFloat() -> Double {
        try! randomFloat(0.0, 1.0)
    }

    public static func randomFloat(_ min: Double, _ max: Double) throws -> Double {
        guard min <= max else {
            throw RandomizerError.invalidRange
        }
        if min == max {
            return min
        }
        let raw = try randomUInt64() >> 11
        let unit = Double(raw) / 9007199254740992.0
        return min + unit * (max - min)
    }

    public static func randomChar() -> Character {
        try! randomChar("A", "Z")
    }

    public static func randomChar(_ min: Character, _ max: Character) throws -> Character {
        let minCode = try validateChar(min)
        let maxCode = try validateChar(max)
        let code = try randomInt(Int(minCode), Int(maxCode))
        return Character(UnicodeScalar(code)!)
    }

    private static func validateChar(_ value: Character) throws -> UInt8 {
        let scalars = String(value).unicodeScalars
        guard scalars.count == 1, let scalar = scalars.first, scalar.value >= 32, scalar.value <= 126 else {
            throw RandomizerError.invalidChar
        }
        return UInt8(scalar.value)
    }

    private static func randomUInt64(below upperBound: UInt64) throws -> UInt64 {
        let limit = UInt64.max - (UInt64.max % upperBound)
        var value: UInt64 = 0
        repeat {
            value = try randomUInt64()
        } while value >= limit
        return value % upperBound
    }

    private static func randomUInt64() throws -> UInt64 {
        var value: UInt64 = 0
        try withUnsafeMutableBytes(of: &value) { buffer in
            try fillRandomBytes(buffer)
        }
        return value
    }

    private static func fillRandomBytes(_ buffer: UnsafeMutableRawBufferPointer) throws {
        guard let baseAddress = buffer.baseAddress else {
            return
        }

        #if canImport(Security)
        let status = SecRandomCopyBytes(kSecRandomDefault, buffer.count, baseAddress)
        guard status == errSecSuccess else {
            throw RandomizerError.randomSourceFailed
        }
        #elseif canImport(WinSDK)
        let status = BCryptGenRandom(
            nil,
            baseAddress.assumingMemoryBound(to: UInt8.self),
            ULONG(buffer.count),
            ULONG(BCRYPT_USE_SYSTEM_PREFERRED_RNG)
        )
        guard status == 0 else {
            throw RandomizerError.randomSourceFailed
        }
        #elseif canImport(Glibc)
        let fd = open("/dev/urandom", O_RDONLY)
        guard fd >= 0 else {
            throw RandomizerError.randomSourceFailed
        }
        defer { close(fd) }

        var offset = 0
        while offset < buffer.count {
            let readCount = read(fd, baseAddress.advanced(by: offset), buffer.count - offset)
            guard readCount > 0 else {
                throw RandomizerError.randomSourceFailed
            }
            offset += readCount
        }
        #else
        throw RandomizerError.randomSourceFailed
        #endif
    }
}

public enum RandomizerError: Error {
    case invalidRange
    case invalidChar
    case randomSourceFailed
}
