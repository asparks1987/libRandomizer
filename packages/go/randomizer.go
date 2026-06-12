package librandomizer

import (
	"crypto/rand"
	"errors"
	"math"
	"math/big"
)

const (
	printableASCIIMin = 32
	printableASCIIMax = 126
)

func RandomInt() int {
	value, err := RandomIntRange(0, 99)
	if err != nil {
		panic(err)
	}
	return value
}

func RandomIntRange(min int, max int) (int, error) {
	if min > max {
		return 0, errors.New("invalid range: min must be less than or equal to max")
	}
	span := big.NewInt(int64(max - min + 1))
	value, err := rand.Int(rand.Reader, span)
	if err != nil {
		return 0, err
	}
	return int(value.Int64()) + min, nil
}

func RandomFloat() float64 {
	value, err := RandomFloatRange(0.0, 1.0)
	if err != nil {
		panic(err)
	}
	return value
}

func RandomFloatRange(min float64, max float64) (float64, error) {
	if min > max {
		return 0, errors.New("invalid range: min must be less than or equal to max")
	}
	if min == max {
		return min, nil
	}
	n, err := rand.Int(rand.Reader, big.NewInt(1<<53))
	if err != nil {
		return 0, err
	}
	unit := float64(n.Int64()) / math.Pow(2, 53)
	return min + unit*(max-min), nil
}

func RandomChar() rune {
	value, err := RandomCharRange('A', 'Z')
	if err != nil {
		panic(err)
	}
	return value
}

func RandomCharRange(min rune, max rune) (rune, error) {
	if min < printableASCIIMin || min > printableASCIIMax {
		return 0, errors.New("invalid character range: min must be printable ASCII")
	}
	if max < printableASCIIMin || max > printableASCIIMax {
		return 0, errors.New("invalid character range: max must be printable ASCII")
	}
	value, err := RandomIntRange(int(min), int(max))
	if err != nil {
		return 0, err
	}
	return rune(value), nil
}
