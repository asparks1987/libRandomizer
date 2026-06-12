random_int <- function(min = 0L, max = 99L) {
  validate_range(min, max)
  span <- as.numeric(max - min + 1L)
  repeat {
    value <- raw_to_uint32(secure_raw(4))
    limit <- floor(2^32 / span) * span
    if (value < limit) {
      return(as.integer(min + (value %% span)))
    }
  }
}

random_float <- function(min = 0.0, max = 1.0) {
  validate_range(min, max)
  if (min == max) {
    return(as.numeric(min))
  }
  raw <- raw_to_uint48(secure_raw(6))
  unit <- raw / 2^48
  min + unit * (max - min)
}

random_char <- function(min = "A", max = "Z") {
  min_code <- validate_char("min", min)
  max_code <- validate_char("max", max)
  validate_range(min_code, max_code)
  intToUtf8(random_int(min_code, max_code))
}

randomInt <- random_int
randomFloat <- random_float
randomChar <- random_char

secure_raw <- function(n) {
  if (.Platform$OS.type == "windows") {
    command <- paste0(
      "$b = New-Object byte[] ", n, "; ",
      "[System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($b); ",
      "($b | ForEach-Object { $_.ToString('X2') }) -join ''"
    )
    hex <- system2("powershell", c("-NoProfile", "-Command", command), stdout = TRUE, stderr = FALSE)
    if (length(hex) == 0 || nchar(hex[1]) != n * 2) {
      stop("OS random source failed", call. = FALSE)
    }
    return(as.raw(strtoi(substring(hex[1], seq(1, nchar(hex[1]), 2), seq(2, nchar(hex[1]), 2)), 16L)))
  }

  con <- file("/dev/urandom", "rb")
  on.exit(close(con), add = TRUE)
  readBin(con, what = "raw", n = n)
}

raw_to_uint32 <- function(bytes) {
  bytes <- as.integer(bytes)
  sum(bytes * 256^(0:3))
}

raw_to_uint48 <- function(bytes) {
  bytes <- as.integer(bytes)
  sum(bytes * 256^(0:5))
}

validate_range <- function(min, max) {
  if (min > max) {
    stop("Invalid range: min must be less than or equal to max", call. = FALSE)
  }
}

validate_char <- function(name, value) {
  if (!is.character(value) || length(value) != 1 || nchar(value, type = "bytes") != 1) {
    stop(sprintf("Invalid character range: %s must be one character", name), call. = FALSE)
  }
  code <- utf8ToInt(value)
  if (code < 32 || code > 126) {
    stop(sprintf("Invalid character range: %s must be printable ASCII", name), call. = FALSE)
  }
  code
}
