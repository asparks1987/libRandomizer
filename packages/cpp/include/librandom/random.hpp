#pragma once

#include <cstdint>
#include <limits>
#include <stdexcept>
#include <string>

#if defined(_WIN32)
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#include <bcrypt.h>
#elif defined(__APPLE__)
#include <stdlib.h>
#else
#include <cerrno>
#include <fcntl.h>
#include <sys/syscall.h>
#include <unistd.h>
#endif

namespace librandom {
namespace detail {

inline void secureBytes(void *buffer, std::size_t length) {
#if defined(_WIN32)
    if (BCryptGenRandom(nullptr, static_cast<PUCHAR>(buffer), static_cast<ULONG>(length), BCRYPT_USE_SYSTEM_PREFERRED_RNG) != 0) {
        throw std::runtime_error("OS random source failed");
    }
#elif defined(__APPLE__)
    arc4random_buf(buffer, length);
#else
    auto *cursor = static_cast<unsigned char *>(buffer);
    std::size_t remaining = length;
    while (remaining > 0) {
        ssize_t count = syscall(SYS_getrandom, cursor, remaining, 0);
        if (count < 0) {
            if (errno == EINTR) {
                continue;
            }
            int fd = open("/dev/urandom", O_RDONLY);
            if (fd < 0) {
                throw std::runtime_error("OS random source failed");
            }
            while (remaining > 0) {
                count = read(fd, cursor, remaining);
                if (count <= 0) {
                    close(fd);
                    throw std::runtime_error("OS random source failed");
                }
                cursor += count;
                remaining -= static_cast<std::size_t>(count);
            }
            close(fd);
            return;
        }
        cursor += count;
        remaining -= static_cast<std::size_t>(count);
    }
#endif
}

inline std::uint64_t randomU64() {
    std::uint64_t value = 0;
    secureBytes(&value, sizeof(value));
    return value;
}

}  // namespace detail

inline int randomInt(int min = 0, int max = 99) {
    if (min > max) {
        throw std::invalid_argument("Invalid range: min must be less than or equal to max");
    }

    auto span = static_cast<std::uint64_t>(static_cast<std::int64_t>(max) - static_cast<std::int64_t>(min)) + 1;
    auto limit = (std::numeric_limits<std::uint64_t>::max)() - ((std::numeric_limits<std::uint64_t>::max)() % span);
    std::uint64_t value = 0;
    do {
        value = detail::randomU64();
    } while (value >= limit);
    return min + static_cast<int>(value % span);
}

inline double randomFloat(double min = 0.0, double max = 1.0) {
    if (min > max) {
        throw std::invalid_argument("Invalid range: min must be less than or equal to max");
    }
    if (min == max) {
        return min;
    }
    auto unit = static_cast<double>(detail::randomU64() >> 11) / 9007199254740992.0;
    return min + unit * (max - min);
}

inline char randomChar(char min = 'A', char max = 'Z') {
    if (min < 32 || max > 126) {
        throw std::invalid_argument("Invalid character range: value must be printable ASCII");
    }
    return static_cast<char>(randomInt(static_cast<int>(min), static_cast<int>(max)));
}

}  // namespace librandom
