#include "librandom.h"

#include <stdint.h>
#include <stdio.h>

#if defined(_WIN32)
#include <windows.h>
#include <bcrypt.h>
#elif defined(__APPLE__)
#include <stdlib.h>
#else
#include <errno.h>
#include <fcntl.h>
#include <sys/syscall.h>
#include <unistd.h>
#endif

#define PRINTABLE_ASCII_MIN 32
#define PRINTABLE_ASCII_MAX 126

static int secure_bytes(void *buffer, size_t length) {
#if defined(_WIN32)
    return BCryptGenRandom(NULL, (PUCHAR)buffer, (ULONG)length, BCRYPT_USE_SYSTEM_PREFERRED_RNG) == 0 ? 0 : -1;
#elif defined(__APPLE__)
    arc4random_buf(buffer, length);
    return 0;
#else
    unsigned char *cursor = (unsigned char *)buffer;
    size_t remaining = length;
    while (remaining > 0) {
        ssize_t read_count = syscall(SYS_getrandom, cursor, remaining, 0);
        if (read_count < 0) {
            if (errno == EINTR) {
                continue;
            }
            int fd = open("/dev/urandom", O_RDONLY);
            if (fd < 0) {
                return -1;
            }
            while (remaining > 0) {
                read_count = read(fd, cursor, remaining);
                if (read_count <= 0) {
                    close(fd);
                    return -1;
                }
                cursor += read_count;
                remaining -= (size_t)read_count;
            }
            close(fd);
            return 0;
        }
        cursor += read_count;
        remaining -= (size_t)read_count;
    }
    return 0;
#endif
}

static int random_uint64(uint64_t *out) {
    return secure_bytes(out, sizeof(*out));
}

int librandom_random_int(int min, int max, int *out) {
    if (out == NULL || min > max) {
        return -1;
    }

    uint64_t span = (uint64_t)((int64_t)max - (int64_t)min) + 1;
    uint64_t limit = UINT64_MAX - (UINT64_MAX % span);
    uint64_t value = 0;

    do {
        if (random_uint64(&value) != 0) {
            return -1;
        }
    } while (value >= limit);

    *out = min + (int)(value % span);
    return 0;
}

int librandom_random_float(double min, double max, double *out) {
    if (out == NULL || min > max) {
        return -1;
    }
    if (min == max) {
        *out = min;
        return 0;
    }

    uint64_t value = 0;
    if (random_uint64(&value) != 0) {
        return -1;
    }
    double unit = (double)(value >> 11) / 9007199254740992.0;
    *out = min + unit * (max - min);
    return 0;
}

int librandom_random_char(char min, char max, char *out) {
    if (out == NULL || min < PRINTABLE_ASCII_MIN || max > PRINTABLE_ASCII_MAX || min > max) {
        return -1;
    }

    int value = 0;
    if (librandom_random_int((int)min, (int)max, &value) != 0) {
        return -1;
    }
    *out = (char)value;
    return 0;
}

int random_int(void) {
    return random_int_range(0, 99);
}

int random_int_range(int min, int max) {
    int value = 0;
    return librandom_random_int(min, max, &value) == 0 ? value : 0;
}

double random_float(void) {
    return random_float_range(0.0, 1.0);
}

double random_float_range(double min, double max) {
    double value = 0.0;
    return librandom_random_float(min, max, &value) == 0 ? value : 0.0;
}

char random_char(void) {
    return random_char_range('A', 'Z');
}

char random_char_range(char min, char max) {
    char value = '\0';
    return librandom_random_char(min, max, &value) == 0 ? value : '\0';
}
