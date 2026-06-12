# frozen_string_literal: true

require "securerandom"

module LibRandomizer
  module_function

  def random_int(min = 0, max = 99)
    validate_range(min, max)
    min + SecureRandom.random_number(max - min + 1)
  end

  def random_float(min = 0.0, max = 1.0)
    validate_range(min, max)
    return min.to_f if min == max

    raw = SecureRandom.random_bytes(8).unpack1("Q>") >> 11
    unit = raw.to_f / 9_007_199_254_740_992.0
    min + unit * (max - min)
  end

  def random_char(min = "A", max = "Z")
    min_code = validate_char("min", min)
    max_code = validate_char("max", max)
    validate_range(min_code, max_code)
    random_int(min_code, max_code).chr
  end

  def randomInt(min = 0, max = 99)
    random_int(min, max)
  end

  def randomFloat(min = 0.0, max = 1.0)
    random_float(min, max)
  end

  def randomChar(min = "A", max = "Z")
    random_char(min, max)
  end

  def validate_range(min, max)
    raise RangeError, "Invalid range: min must be less than or equal to max" if min > max
  end

  def validate_char(name, value)
    unless value.is_a?(String) && value.length == 1
      raise RangeError, "Invalid character range: #{name} must be one character"
    end

    code = value.ord
    unless code.between?(32, 126)
      raise RangeError, "Invalid character range: #{name} must be printable ASCII"
    end
    code
  end
end
