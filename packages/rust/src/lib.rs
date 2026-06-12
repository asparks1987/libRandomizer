use rand::rngs::OsRng;
use rand::{Rng, RngCore};
use std::error::Error;
use std::fmt::{Display, Formatter};

const PRINTABLE_ASCII_MIN: u8 = 32;
const PRINTABLE_ASCII_MAX: u8 = 126;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RandomizerError {
    InvalidRange,
    InvalidChar,
}

impl Display for RandomizerError {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        match self {
            RandomizerError::InvalidRange => {
                write!(f, "Invalid range: min must be less than or equal to max")
            }
            RandomizerError::InvalidChar => write!(
                f,
                "Invalid character range: value must be one printable ASCII character"
            ),
        }
    }
}

impl Error for RandomizerError {}

pub fn random_int() -> i64 {
    random_int_range(0, 99).expect("default range is valid")
}

pub fn random_int_range(min: i64, max: i64) -> Result<i64, RandomizerError> {
    if min > max {
        return Err(RandomizerError::InvalidRange);
    }
    Ok(OsRng.gen_range(min..=max))
}

pub fn random_float() -> f64 {
    random_float_range(0.0, 1.0).expect("default range is valid")
}

pub fn random_float_range(min: f64, max: f64) -> Result<f64, RandomizerError> {
    if min > max {
        return Err(RandomizerError::InvalidRange);
    }
    if min == max {
        return Ok(min);
    }
    let value = OsRng.next_u64() >> 11;
    let unit = value as f64 / 9_007_199_254_740_992.0;
    Ok(min + unit * (max - min))
}

pub fn random_char() -> char {
    random_char_range('A', 'Z').expect("default range is valid")
}

pub fn random_char_range(min: char, max: char) -> Result<char, RandomizerError> {
    let min_code = validate_char(min)?;
    let max_code = validate_char(max)?;
    if min_code > max_code {
        return Err(RandomizerError::InvalidRange);
    }
    let code = OsRng.gen_range(min_code..=max_code);
    Ok(code as char)
}

fn validate_char(value: char) -> Result<u8, RandomizerError> {
    let code = value as u32;
    if code < PRINTABLE_ASCII_MIN as u32 || code > PRINTABLE_ASCII_MAX as u32 {
        return Err(RandomizerError::InvalidChar);
    }
    Ok(code as u8)
}
