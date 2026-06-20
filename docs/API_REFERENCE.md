# libRandomizer API Reference

> Legacy compatibility note: this reference documents the older random primitive
> catalog. The primary SDK path is now `TrainingDataGenerator`, portable schemas,
> fixed counts, and deterministic input/output training pairs. Start with
> `../README.md`, `index.html`, and `../spec/training/README.md` for the current
> training-data API.

This legacy file is generated from `spec/beta/output-types.json`. Update the source catalog, then run:

```bash
python scripts/sync_beta_docs.py
```

Status values:

- `planned-beta`: Cemented in beta documentation as a target output type.
- `in-progress`: Implementation is underway but not release-gated.
- `implemented-python`: Python SDK and CLI pass shared conformance for this type.
- `implemented-all`: All 15 target SDKs pass shared conformance for this type.
- `deprecated`: Retained only for compatibility and not recommended.
- `available-v1`: Compatibility status from early v1 docs; new entries should use implemented-python or implemented-all.

Note: `implemented-all` in this generated reference file is the target state. In this beta release window, the actual deployment policy is that
all non-Python SDKs are treated as generated surfaces until parity is confirmed in
the language conformance matrix.

Shared option names:

- `min`: Inclusive lower bound where the output type supports ranges.
- `max`: Inclusive upper bound where the output type supports ranges.
- `length`: Number of characters or bytes to generate.
- `count`: Number of items to return.
- `locale`: Locale hint for dataset-backed values; default is en-US until broader locale support lands.
- `allowAdult`: Explicit opt-in for adult/profane corpus values; default is false.
- `format`: Return format selector for types with multiple common representations.
- `items`: Collection of values to select from.
- `weights`: Numeric weights aligned to items.

Text safety policy: safe corpora are the default; adult/profane terms require explicit opt-in.

## Core primitives

### Integer

- API: `randomInt()`
- Status: `implemented-all`
- Aliases: `getRandomInt()`
- Parameters: `min` (integer, default `0`), `max` (integer, default `99`)
- Returns: `integer` - Whole number with optional inclusive bounds.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid range: min must be less than or equal to max; Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomInt(0, 99)` -> `42`

### Float

- API: `randomFloat()`
- Status: `implemented-all`
- Aliases: `getRandomFloat()`
- Parameters: `min` (float, default `0.0`), `max` (float, default `1.0`)
- Returns: `float` - Floating-point number with optional bounds.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid range: min must be less than or equal to max; Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomFloat(0.0, 1.0)` -> `0.7319`

### Character

- API: `randomChar()`
- Status: `implemented-all`
- Aliases: `getRandomChar()`
- Parameters: `min` (character, default `A`), `max` (character, default `Z`)
- Returns: `character` - Printable ASCII character with optional bounds.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid range: min must be less than or equal to max; Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid character range: bounds must be single printable ASCII characters
- Example: `randomChar("A", "Z")` -> `"Q"`

### Boolean

- API: `randomBool()`
- Status: `implemented-all`
- Aliases: `getRandomBool()`
- Parameters: None
- Returns: `boolean` - True or false value.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomBool()` -> `<Boolean>`

### String

- API: `randomString()`
- Status: `implemented-all`
- Aliases: `getRandomString()`
- Parameters: `length` (integer, default `12`)
- Returns: `string` - String with configurable length and character set.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid size: length/count must be a non-negative integer within supported limits
- Example: `randomString(5)` -> `"aZ91q"`

### Bytes

- API: `randomBytes()`
- Status: `implemented-all`
- Aliases: `getRandomBytes()`
- Parameters: `length` (integer, default `16`), `format` (string, default `None`)
- Returns: `bytes` - Raw random byte sequence.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid size: length/count must be a non-negative integer within supported limits
- Example: `randomBytes()` -> `<Bytes>`

### Bit

- API: `randomBit()`
- Status: `implemented-all`
- Aliases: `getRandomBit()`
- Parameters: None
- Returns: `integer` - Single binary 0 or 1 value.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomBit()` -> `<Bit>`

### Binary String

- API: `randomBinaryString()`
- Status: `implemented-all`
- Aliases: `getRandomBinaryString()`
- Parameters: `length` (integer, default `16`)
- Returns: `string` - String of random 0 and 1 characters.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid size: length/count must be a non-negative integer within supported limits
- Example: `randomBinaryString()` -> `<Binary String>`

### Hex String

- API: `randomHex()`
- Status: `implemented-all`
- Aliases: `getRandomHex()`
- Parameters: `length` (integer, default `16`)
- Returns: `string` - Hexadecimal random string.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid size: length/count must be a non-negative integer within supported limits
- Example: `randomHex()` -> `<Hex String>`

### Base64 String

- API: `randomBase64()`
- Status: `implemented-all`
- Aliases: `getRandomBase64()`
- Parameters: `length` (integer, default `16`)
- Returns: `string` - Base64-encoded random bytes.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid size: length/count must be a non-negative integer within supported limits
- Example: `randomBase64()` -> `<Base64 String>`

## Identifiers

### UUID

- API: `randomUuid()`
- Status: `implemented-all`
- Aliases: `getRandomUuid()`
- Parameters: None
- Returns: `string` - UUID value.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomUuid()` -> `<UUID>`

### ULID

- API: `randomUlid()`
- Status: `implemented-all`
- Aliases: `getRandomUlid()`
- Parameters: None
- Returns: `string` - Sortable unique identifier.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomUlid()` -> `<ULID>`

### Nano ID

- API: `randomNanoId()`
- Status: `implemented-all`
- Aliases: `getRandomNanoId()`
- Parameters: `length` (integer, default `16`)
- Returns: `string` - Compact URL-safe identifier.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid size: length/count must be a non-negative integer within supported limits
- Example: `randomNanoId()` -> `<Nano ID>`

### Slug

- API: `randomSlug()`
- Status: `implemented-all`
- Aliases: `getRandomSlug()`
- Parameters: `length` (integer, default `16`)
- Returns: `string` - URL-friendly text identifier.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid size: length/count must be a non-negative integer within supported limits
- Example: `randomSlug()` -> `<Slug>`

### Token

- API: `randomToken()`
- Status: `implemented-all`
- Aliases: `getRandomToken()`
- Parameters: `length` (integer, default `16`), `format` (string, default `None`)
- Returns: `string` - Random token string for non-auth demo data.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid size: length/count must be a non-negative integer within supported limits
- Example: `randomToken()` -> `<Token>`

### PIN

- API: `randomPin()`
- Status: `implemented-all`
- Aliases: `getRandomPin()`
- Parameters: `length` (integer, default `16`)
- Returns: `string` - Numeric personal identification style code.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid size: length/count must be a non-negative integer within supported limits
- Example: `randomPin()` -> `<PIN>`

### OTP

- API: `randomOtp()`
- Status: `implemented-all`
- Aliases: `getRandomOtp()`
- Parameters: `length` (integer, default `16`)
- Returns: `string` - One-time-code style numeric value for testing.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid size: length/count must be a non-negative integer within supported limits
- Example: `randomOtp()` -> `<OTP>`

### Short Code

- API: `randomShortCode()`
- Status: `implemented-all`
- Aliases: `getRandomShortCode()`
- Parameters: `length` (integer, default `16`)
- Returns: `string` - Short human-readable code.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid size: length/count must be a non-negative integer within supported limits
- Example: `randomShortCode()` -> `<Short Code>`

### Coupon Code

- API: `randomCouponCode()`
- Status: `implemented-all`
- Aliases: `getRandomCouponCode()`
- Parameters: `length` (integer, default `16`)
- Returns: `string` - Promotion-style alphanumeric code.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid size: length/count must be a non-negative integer within supported limits
- Example: `randomCouponCode()` -> `<Coupon Code>`

### License Key

- API: `randomLicenseKey()`
- Status: `implemented-all`
- Aliases: `getRandomLicenseKey()`
- Parameters: `length` (integer, default `16`)
- Returns: `string` - Segmented product-key style test value.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid size: length/count must be a non-negative integer within supported limits
- Example: `randomLicenseKey()` -> `<License Key>`

## Numbers

### Even Integer

- API: `randomEvenInt()`
- Status: `implemented-all`
- Aliases: `getRandomEvenInt()`
- Parameters: `min` (integer, default `0`), `max` (integer, default `99`)
- Returns: `integer` - Even whole number within bounds.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid range: min must be less than or equal to max; Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomEvenInt()` -> `<Even Integer>`

### Odd Integer

- API: `randomOddInt()`
- Status: `implemented-all`
- Aliases: `getRandomOddInt()`
- Parameters: `min` (integer, default `0`), `max` (integer, default `99`)
- Returns: `integer` - Odd whole number within bounds.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid range: min must be less than or equal to max; Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomOddInt()` -> `<Odd Integer>`

### Prime Number

- API: `randomPrime()`
- Status: `implemented-all`
- Aliases: `getRandomPrime()`
- Parameters: `min` (integer, default `0`), `max` (integer, default `99`)
- Returns: `integer` - Prime number within supported bounds.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid range: min must be less than or equal to max; Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomPrime()` -> `<Prime Number>`

### Decimal

- API: `randomDecimal()`
- Status: `implemented-all`
- Aliases: `getRandomDecimal()`
- Parameters: `min` (number, default `None`), `max` (number, default `None`)
- Returns: `decimal` - Fixed-precision decimal value.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid range: min must be less than or equal to max; Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomDecimal()` -> `<Decimal>`

### Percentage

- API: `randomPercentage()`
- Status: `implemented-all`
- Aliases: `getRandomPercentage()`
- Parameters: `min` (number, default `None`), `max` (number, default `None`)
- Returns: `float` - Percentage value.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid range: min must be less than or equal to max; Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomPercentage()` -> `<Percentage>`

### Ratio

- API: `randomRatio()`
- Status: `implemented-all`
- Aliases: `getRandomRatio()`
- Parameters: `min` (number, default `None`), `max` (number, default `None`)
- Returns: `float` - Ratio or normalized numeric value.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid range: min must be less than or equal to max; Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomRatio()` -> `<Ratio>`

### Angle

- API: `randomAngle()`
- Status: `implemented-all`
- Aliases: `getRandomAngle()`
- Parameters: `min` (number, default `None`), `max` (number, default `None`)
- Returns: `float` - Angle in degrees or radians.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid range: min must be less than or equal to max; Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomAngle()` -> `<Angle>`

### Latitude

- API: `randomLatitude()`
- Status: `implemented-all`
- Aliases: `getRandomLatitude()`
- Parameters: `min` (number, default `None`), `max` (number, default `None`)
- Returns: `float` - Latitude coordinate.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid range: min must be less than or equal to max; Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomLatitude()` -> `<Latitude>`

### Longitude

- API: `randomLongitude()`
- Status: `implemented-all`
- Aliases: `getRandomLongitude()`
- Parameters: `min` (number, default `None`), `max` (number, default `None`)
- Returns: `float` - Longitude coordinate.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid range: min must be less than or equal to max; Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomLongitude()` -> `<Longitude>`

### Currency Amount

- API: `randomCurrencyAmount()`
- Status: `implemented-all`
- Aliases: `getRandomCurrencyAmount()`
- Parameters: `min` (number, default `None`), `max` (number, default `None`)
- Returns: `decimal` - Money-like decimal amount.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid range: min must be less than or equal to max; Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomCurrencyAmount()` -> `<Currency Amount>`

## Text

### Word

- API: `randomWord()`
- Status: `implemented-all`
- Aliases: `getRandomWord()`
- Parameters: `locale` (string, default `en-US`), `allowAdult` (boolean, default `False`)
- Returns: `string` - Single word from a configured or built-in corpus.
- Content safety: `safe-default-adult-opt-in`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomWord()` -> `"river"`

### Sentence

- API: `randomSentence()`
- Status: `implemented-all`
- Aliases: `getRandomSentence()`
- Parameters: `locale` (string, default `en-US`), `allowAdult` (boolean, default `False`)
- Returns: `string` - Generated sentence.
- Content safety: `safe-default-adult-opt-in`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomSentence()` -> `<Sentence>`

### Paragraph

- API: `randomParagraph()`
- Status: `implemented-all`
- Aliases: `getRandomParagraph()`
- Parameters: `count` (integer, default `1`), `locale` (string, default `en-US`), `allowAdult` (boolean, default `False`)
- Returns: `string` - Generated paragraph.
- Content safety: `safe-default-adult-opt-in`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid size: length/count must be a non-negative integer within supported limits
- Example: `randomParagraph(count=1)` -> `"A short generated paragraph."`

### Title

- API: `randomTitle()`
- Status: `implemented-all`
- Aliases: `getRandomTitle()`
- Parameters: `locale` (string, default `en-US`), `allowAdult` (boolean, default `False`)
- Returns: `string` - Title-style phrase.
- Content safety: `safe-default-adult-opt-in`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomTitle()` -> `<Title>`

### Username

- API: `randomUsername()`
- Status: `implemented-all`
- Aliases: `getRandomUsername()`
- Parameters: `locale` (string, default `en-US`), `allowAdult` (boolean, default `False`)
- Returns: `string` - Username-like handle.
- Content safety: `safe-default-adult-opt-in`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomUsername()` -> `<Username>`

### Display Name

- API: `randomDisplayName()`
- Status: `implemented-all`
- Aliases: `getRandomDisplayName()`
- Parameters: `locale` (string, default `en-US`), `allowAdult` (boolean, default `False`)
- Returns: `string` - Human-friendly display name.
- Content safety: `safe-default-adult-opt-in`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomDisplayName()` -> `<Display Name>`

### Password

- API: `randomPassword()`
- Status: `implemented-all`
- Aliases: `getRandomPassword()`
- Parameters: `length` (integer, default `16`), `locale` (string, default `en-US`), `allowAdult` (boolean, default `False`), `format` (string, default `None`)
- Returns: `string` - Configurable password-like random string.
- Content safety: `safe-default-adult-opt-in`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid size: length/count must be a non-negative integer within supported limits
- Example: `randomPassword()` -> `<Password>`

### Emoji

- API: `randomEmoji()`
- Status: `implemented-all`
- Aliases: `getRandomEmoji()`
- Parameters: `locale` (string, default `en-US`), `allowAdult` (boolean, default `False`)
- Returns: `string` - Emoji character or sequence.
- Content safety: `safe-default-adult-opt-in`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomEmoji()` -> `<Emoji>`

### Symbol

- API: `randomSymbol()`
- Status: `implemented-all`
- Aliases: `getRandomSymbol()`
- Parameters: `locale` (string, default `en-US`), `allowAdult` (boolean, default `False`)
- Returns: `string` - Symbol character.
- Content safety: `safe-default-adult-opt-in`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomSymbol()` -> `<Symbol>`

### Punctuation

- API: `randomPunctuation()`
- Status: `implemented-all`
- Aliases: `getRandomPunctuation()`
- Parameters: `locale` (string, default `en-US`), `allowAdult` (boolean, default `False`)
- Returns: `string` - Punctuation character.
- Content safety: `safe-default-adult-opt-in`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomPunctuation()` -> `<Punctuation>`

## People

### First Name

- API: `randomFirstName()`
- Status: `implemented-all`
- Aliases: `getRandomFirstName()`
- Parameters: `locale` (string, default `en-US`)
- Returns: `string` - Given name.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomFirstName()` -> `<First Name>`

### Last Name

- API: `randomLastName()`
- Status: `implemented-all`
- Aliases: `getRandomLastName()`
- Parameters: `locale` (string, default `en-US`)
- Returns: `string` - Family name.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomLastName()` -> `<Last Name>`

### Full Name

- API: `randomFullName()`
- Status: `implemented-all`
- Aliases: `getRandomFullName()`
- Parameters: `locale` (string, default `en-US`)
- Returns: `string` - Complete person name.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomFullName()` -> `<Full Name>`

### Name Prefix

- API: `randomNamePrefix()`
- Status: `implemented-all`
- Aliases: `getRandomNamePrefix()`
- Parameters: `locale` (string, default `en-US`)
- Returns: `string` - Name prefix such as Dr. or Ms.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomNamePrefix()` -> `<Name Prefix>`

### Name Suffix

- API: `randomNameSuffix()`
- Status: `implemented-all`
- Aliases: `getRandomNameSuffix()`
- Parameters: `locale` (string, default `en-US`)
- Returns: `string` - Name suffix such as Jr. or III.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomNameSuffix()` -> `<Name Suffix>`

### Job Title

- API: `randomJobTitle()`
- Status: `implemented-all`
- Aliases: `getRandomJobTitle()`
- Parameters: `locale` (string, default `en-US`)
- Returns: `string` - Professional role title.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomJobTitle()` -> `<Job Title>`

### Department

- API: `randomDepartment()`
- Status: `implemented-all`
- Aliases: `getRandomDepartment()`
- Parameters: `locale` (string, default `en-US`)
- Returns: `string` - Company department name.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomDepartment()` -> `<Department>`

### Company

- API: `randomCompany()`
- Status: `implemented-all`
- Aliases: `getRandomCompany()`
- Parameters: `locale` (string, default `en-US`)
- Returns: `string` - Company or organization name.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomCompany()` -> `<Company>`

### Email

- API: `randomEmail()`
- Status: `implemented-all`
- Aliases: `getRandomEmail()`
- Parameters: `locale` (string, default `en-US`)
- Returns: `string` - Email-address shaped value.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomEmail()` -> `<Email>`

### Phone

- API: `randomPhone()`
- Status: `implemented-all`
- Aliases: `getRandomPhone()`
- Parameters: `locale` (string, default `en-US`)
- Returns: `string` - Phone-number shaped value.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomPhone()` -> `<Phone>`

## Internet

### URL

- API: `randomUrl()`
- Status: `implemented-all`
- Aliases: `getRandomUrl()`
- Parameters: `format` (string, default `None`)
- Returns: `string` - Web URL.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomUrl()` -> `<URL>`

### Domain

- API: `randomDomain()`
- Status: `implemented-all`
- Aliases: `getRandomDomain()`
- Parameters: `format` (string, default `None`)
- Returns: `string` - Domain name.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomDomain()` -> `<Domain>`

### Subdomain

- API: `randomSubdomain()`
- Status: `implemented-all`
- Aliases: `getRandomSubdomain()`
- Parameters: `format` (string, default `None`)
- Returns: `string` - Subdomain label.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomSubdomain()` -> `<Subdomain>`

### IPv4 Address

- API: `randomIpv4()`
- Status: `implemented-all`
- Aliases: `getRandomIpv4()`
- Parameters: `format` (string, default `None`)
- Returns: `string` - IPv4 address.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomIpv4()` -> `<IPv4 Address>`

### IPv6 Address

- API: `randomIpv6()`
- Status: `implemented-all`
- Aliases: `getRandomIpv6()`
- Parameters: `format` (string, default `None`)
- Returns: `string` - IPv6 address.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomIpv6()` -> `<IPv6 Address>`

### MAC Address

- API: `randomMacAddress()`
- Status: `implemented-all`
- Aliases: `getRandomMacAddress()`
- Parameters: `format` (string, default `None`)
- Returns: `string` - Network MAC address.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomMacAddress()` -> `<MAC Address>`

### Port

- API: `randomPort()`
- Status: `implemented-all`
- Aliases: `getRandomPort()`
- Parameters: `min` (number, default `None`), `max` (number, default `None`), `format` (string, default `None`)
- Returns: `string` - Network port number.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid range: min must be less than or equal to max; Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomPort()` -> `<Port>`

### User Agent

- API: `randomUserAgent()`
- Status: `implemented-all`
- Aliases: `getRandomUserAgent()`
- Parameters: `format` (string, default `None`)
- Returns: `string` - Browser or client user-agent string.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomUserAgent()` -> `<User Agent>`

### MIME Type

- API: `randomMimeType()`
- Status: `implemented-all`
- Aliases: `getRandomMimeType()`
- Parameters: `format` (string, default `None`)
- Returns: `string` - MIME media type.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomMimeType()` -> `<MIME Type>`

### HTTP Status

- API: `randomHttpStatus()`
- Status: `implemented-all`
- Aliases: `getRandomHttpStatus()`
- Parameters: `format` (string, default `None`)
- Returns: `string` - HTTP response status code.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomHttpStatus()` -> `<HTTP Status>`

## Color

### Hex Color

- API: `randomHexColor()`
- Status: `implemented-all`
- Aliases: `getRandomHexColor()`
- Parameters: `format` (string, default `None`)
- Returns: `string` - CSS hex color.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomHexColor()` -> `<Hex Color>`

### RGB Color

- API: `randomRgbColor()`
- Status: `implemented-all`
- Aliases: `getRandomRgbColor()`
- Parameters: `format` (string, default `None`)
- Returns: `string` - RGB color tuple.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomRgbColor()` -> `<RGB Color>`

### RGBA Color

- API: `randomRgbaColor()`
- Status: `implemented-all`
- Aliases: `getRandomRgbaColor()`
- Parameters: `format` (string, default `None`)
- Returns: `string` - RGBA color tuple.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomRgbaColor()` -> `<RGBA Color>`

### HSL Color

- API: `randomHslColor()`
- Status: `implemented-all`
- Aliases: `getRandomHslColor()`
- Parameters: `format` (string, default `None`)
- Returns: `string` - HSL color tuple.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomHslColor()` -> `<HSL Color>`

### HSLA Color

- API: `randomHslaColor()`
- Status: `implemented-all`
- Aliases: `getRandomHslaColor()`
- Parameters: `format` (string, default `None`)
- Returns: `string` - HSLA color tuple.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomHslaColor()` -> `<HSLA Color>`

### Color Name

- API: `randomColorName()`
- Status: `implemented-all`
- Aliases: `getRandomColorName()`
- Parameters: `format` (string, default `None`)
- Returns: `string` - Human-readable color name.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomColorName()` -> `<Color Name>`

### Palette

- API: `randomPalette()`
- Status: `implemented-all`
- Aliases: `getRandomPalette()`
- Parameters: `count` (integer, default `1`), `format` (string, default `None`)
- Returns: `array` - Set of compatible colors.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid size: length/count must be a non-negative integer within supported limits
- Example: `randomPalette()` -> `<Palette>`

### Gradient

- API: `randomGradient()`
- Status: `implemented-all`
- Aliases: `getRandomGradient()`
- Parameters: `count` (integer, default `1`), `format` (string, default `None`)
- Returns: `string` - CSS-style gradient definition.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid size: length/count must be a non-negative integer within supported limits
- Example: `randomGradient()` -> `<Gradient>`

## Location

### Country

- API: `randomCountry()`
- Status: `implemented-all`
- Aliases: `getRandomCountry()`
- Parameters: `locale` (string, default `en-US`)
- Returns: `string` - Country name or code.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomCountry()` -> `<Country>`

### Region

- API: `randomRegion()`
- Status: `implemented-all`
- Aliases: `getRandomRegion()`
- Parameters: `locale` (string, default `en-US`)
- Returns: `string` - State, province, or region.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomRegion()` -> `<Region>`

### City

- API: `randomCity()`
- Status: `implemented-all`
- Aliases: `getRandomCity()`
- Parameters: `locale` (string, default `en-US`)
- Returns: `string` - City name.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomCity()` -> `<City>`

### Street

- API: `randomStreet()`
- Status: `implemented-all`
- Aliases: `getRandomStreet()`
- Parameters: `locale` (string, default `en-US`)
- Returns: `string` - Street name.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomStreet()` -> `<Street>`

### Address

- API: `randomAddress()`
- Status: `implemented-all`
- Aliases: `getRandomAddress()`
- Parameters: `locale` (string, default `en-US`)
- Returns: `string` - Full mailing-address shaped value.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomAddress()` -> `<Address>`

### Postal Code

- API: `randomPostalCode()`
- Status: `implemented-all`
- Aliases: `getRandomPostalCode()`
- Parameters: `locale` (string, default `en-US`)
- Returns: `string` - ZIP or postal code.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomPostalCode()` -> `<Postal Code>`

### Coordinate

- API: `randomCoordinate()`
- Status: `implemented-all`
- Aliases: `getRandomCoordinate()`
- Parameters: `locale` (string, default `en-US`)
- Returns: `object` - Latitude and longitude pair.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomCoordinate()` -> `<Coordinate>`

### Time Zone

- API: `randomTimezone()`
- Status: `implemented-all`
- Aliases: `getRandomTimezone()`
- Parameters: `locale` (string, default `en-US`)
- Returns: `string` - IANA-style time zone.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomTimezone()` -> `<Time Zone>`

### Locale

- API: `randomLocale()`
- Status: `implemented-all`
- Aliases: `getRandomLocale()`
- Parameters: `locale` (string, default `en-US`)
- Returns: `string` - Locale identifier.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomLocale()` -> `<Locale>`

### Currency Code

- API: `randomCurrencyCode()`
- Status: `implemented-all`
- Aliases: `getRandomCurrencyCode()`
- Parameters: `locale` (string, default `en-US`)
- Returns: `string` - ISO-style currency code.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomCurrencyCode()` -> `<Currency Code>`

## Date and time

### Date

- API: `randomDate()`
- Status: `implemented-all`
- Aliases: `getRandomDate()`
- Parameters: `format` (string, default `None`)
- Returns: `string` - Calendar date.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomDate()` -> `<Date>`

### Time

- API: `randomTime()`
- Status: `implemented-all`
- Aliases: `getRandomTime()`
- Parameters: `format` (string, default `None`)
- Returns: `string` - Clock time.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomTime()` -> `<Time>`

### Datetime

- API: `randomDatetime()`
- Status: `implemented-all`
- Aliases: `getRandomDatetime()`
- Parameters: `format` (string, default `None`)
- Returns: `datetime` - Date and time value.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomDatetime()` -> `<Datetime>`

### Timestamp

- API: `randomTimestamp()`
- Status: `implemented-all`
- Aliases: `getRandomTimestamp()`
- Parameters: `format` (string, default `None`)
- Returns: `integer` - Unix-style timestamp.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomTimestamp()` -> `<Timestamp>`

### Duration

- API: `randomDuration()`
- Status: `implemented-all`
- Aliases: `getRandomDuration()`
- Parameters: `format` (string, default `None`)
- Returns: `object` - Time interval.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomDuration()` -> `<Duration>`

### Weekday

- API: `randomWeekday()`
- Status: `implemented-all`
- Aliases: `getRandomWeekday()`
- Parameters: `format` (string, default `None`)
- Returns: `string` - Day of week.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomWeekday()` -> `<Weekday>`

### Month

- API: `randomMonth()`
- Status: `implemented-all`
- Aliases: `getRandomMonth()`
- Parameters: `format` (string, default `None`)
- Returns: `string` - Month name or number.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomMonth()` -> `<Month>`

### Year

- API: `randomYear()`
- Status: `implemented-all`
- Aliases: `getRandomYear()`
- Parameters: `min` (number, default `None`), `max` (number, default `None`), `format` (string, default `None`)
- Returns: `string` - Year value.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid range: min must be less than or equal to max; Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomYear()` -> `<Year>`

### Cron Expression

- API: `randomCron()`
- Status: `implemented-all`
- Aliases: `getRandomCron()`
- Parameters: `format` (string, default `None`)
- Returns: `string` - Cron-like schedule expression.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomCron()` -> `<Cron Expression>`

### Time Zone Offset

- API: `randomTimezoneOffset()`
- Status: `implemented-all`
- Aliases: `getRandomTimezoneOffset()`
- Parameters: `format` (string, default `None`)
- Returns: `string` - UTC offset value.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomTimezoneOffset()` -> `<Time Zone Offset>`

## Commerce

### Price

- API: `randomPrice()`
- Status: `implemented-all`
- Aliases: `getRandomPrice()`
- Parameters: `min` (number, default `None`), `max` (number, default `None`)
- Returns: `string` - Price-like amount.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid range: min must be less than or equal to max; Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomPrice()` -> `<Price>`

### SKU

- API: `randomSku()`
- Status: `implemented-all`
- Aliases: `getRandomSku()`
- Parameters: None
- Returns: `string` - Stock keeping unit.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomSku()` -> `<SKU>`

### Product Name

- API: `randomProductName()`
- Status: `implemented-all`
- Aliases: `getRandomProductName()`
- Parameters: None
- Returns: `string` - Product name.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomProductName()` -> `<Product Name>`

### Product Category

- API: `randomProductCategory()`
- Status: `implemented-all`
- Aliases: `getRandomProductCategory()`
- Parameters: None
- Returns: `string` - Commerce category.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomProductCategory()` -> `<Product Category>`

### Brand

- API: `randomBrand()`
- Status: `implemented-all`
- Aliases: `getRandomBrand()`
- Parameters: None
- Returns: `string` - Brand name.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomBrand()` -> `<Brand>`

### Order ID

- API: `randomOrderId()`
- Status: `implemented-all`
- Aliases: `getRandomOrderId()`
- Parameters: None
- Returns: `string` - Order identifier.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomOrderId()` -> `<Order ID>`

### Invoice Number

- API: `randomInvoiceNumber()`
- Status: `implemented-all`
- Aliases: `getRandomInvoiceNumber()`
- Parameters: None
- Returns: `string` - Invoice-like identifier.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomInvoiceNumber()` -> `<Invoice Number>`

### Tax Rate

- API: `randomTaxRate()`
- Status: `implemented-all`
- Aliases: `getRandomTaxRate()`
- Parameters: `min` (number, default `None`), `max` (number, default `None`)
- Returns: `string` - Tax percentage.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid range: min must be less than or equal to max; Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomTaxRate()` -> `<Tax Rate>`

### Shipping Method

- API: `randomShippingMethod()`
- Status: `implemented-all`
- Aliases: `getRandomShippingMethod()`
- Parameters: None
- Returns: `string` - Shipping method label.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomShippingMethod()` -> `<Shipping Method>`

### Payment Method

- API: `randomPaymentMethod()`
- Status: `implemented-all`
- Aliases: `getRandomPaymentMethod()`
- Parameters: None
- Returns: `string` - Payment method label for test data.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomPaymentMethod()` -> `<Payment Method>`

## Games

### Dice Roll

- API: `randomDiceRoll()`
- Status: `implemented-all`
- Aliases: `getRandomDiceRoll()`
- Parameters: `min` (number, default `None`), `max` (number, default `None`)
- Returns: `integer` - Dice result with configurable sides.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid range: min must be less than or equal to max; Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomDiceRoll()` -> `<Dice Roll>`

### Playing Card

- API: `randomPlayingCard()`
- Status: `implemented-all`
- Aliases: `getRandomPlayingCard()`
- Parameters: None
- Returns: `object` - Card rank and suit.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomPlayingCard()` -> `<Playing Card>`

### Card Suit

- API: `randomCardSuit()`
- Status: `implemented-all`
- Aliases: `getRandomCardSuit()`
- Parameters: None
- Returns: `string` - Playing-card suit.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomCardSuit()` -> `<Card Suit>`

### Card Rank

- API: `randomCardRank()`
- Status: `implemented-all`
- Aliases: `getRandomCardRank()`
- Parameters: None
- Returns: `string` - Playing-card rank.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomCardRank()` -> `<Card Rank>`

### Coin Flip

- API: `randomCoinFlip()`
- Status: `implemented-all`
- Aliases: `getRandomCoinFlip()`
- Parameters: None
- Returns: `string` - Heads or tails.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomCoinFlip()` -> `<Coin Flip>`

### Lottery Pick

- API: `randomLotteryPick()`
- Status: `implemented-all`
- Aliases: `getRandomLotteryPick()`
- Parameters: `count` (integer, default `1`)
- Returns: `array` - Lottery-style number set.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid size: length/count must be a non-negative integer within supported limits
- Example: `randomLotteryPick()` -> `<Lottery Pick>`

### Team Name

- API: `randomTeamName()`
- Status: `implemented-all`
- Aliases: `getRandomTeamName()`
- Parameters: None
- Returns: `string` - Team-style name.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomTeamName()` -> `<Team Name>`

### Game Score

- API: `randomGameScore()`
- Status: `implemented-all`
- Aliases: `getRandomGameScore()`
- Parameters: `min` (number, default `None`), `max` (number, default `None`)
- Returns: `string` - Score value or pair.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid range: min must be less than or equal to max; Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomGameScore()` -> `<Game Score>`

### RPG Class

- API: `randomRpgClass()`
- Status: `implemented-all`
- Aliases: `getRandomRpgClass()`
- Parameters: None
- Returns: `string` - Role-playing class label.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomRpgClass()` -> `<RPG Class>`

### Loot Rarity

- API: `randomLootRarity()`
- Status: `implemented-all`
- Aliases: `getRandomLootRarity()`
- Parameters: None
- Returns: `string` - Item rarity tier.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomLootRarity()` -> `<Loot Rarity>`

## Collections

### Choice

- API: `randomChoice()`
- Status: `implemented-all`
- Aliases: `getRandomChoice()`
- Parameters: `items` (array, required)
- Returns: `item` - One item selected from a list.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid collection: items must contain enough values for the requested operation
- Example: `randomChoice(["red", "blue"])` -> `"red"`

### Weighted Choice

- API: `randomWeightedChoice()`
- Status: `implemented-all`
- Aliases: `getRandomWeightedChoice()`
- Parameters: `items` (array, required), `weights` (array, required)
- Returns: `item` - One item selected using weights.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid collection: items must contain enough values for the requested operation
- Example: `randomWeightedChoice(["red", "blue"])` -> `"red"`

### Sample

- API: `randomSample()`
- Status: `implemented-all`
- Aliases: `getRandomSample()`
- Parameters: `count` (integer, default `1`), `items` (array, required)
- Returns: `array` - Subset selected from a list.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid size: length/count must be a non-negative integer within supported limits; Invalid collection: items must contain enough values for the requested operation
- Example: `randomSample()` -> `<Sample>`

### Shuffle

- API: `randomShuffle()`
- Status: `implemented-all`
- Aliases: `getRandomShuffle()`
- Parameters: `count` (integer, default `1`), `items` (array, required)
- Returns: `array` - Randomly ordered copy of a collection.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid size: length/count must be a non-negative integer within supported limits; Invalid collection: items must contain enough values for the requested operation
- Example: `randomShuffle()` -> `<Shuffle>`

### Permutation

- API: `randomPermutation()`
- Status: `implemented-all`
- Aliases: `getRandomPermutation()`
- Parameters: `count` (integer, default `1`), `items` (array, required)
- Returns: `array` - Permutation of values.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid size: length/count must be a non-negative integer within supported limits; Invalid collection: items must contain enough values for the requested operation
- Example: `randomPermutation()` -> `<Permutation>`

### Set

- API: `randomSet()`
- Status: `implemented-all`
- Aliases: `getRandomSet()`
- Parameters: `count` (integer, default `1`), `items` (array, default `None`)
- Returns: `array` - Unique random collection.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid size: length/count must be a non-negative integer within supported limits; Invalid collection: items must contain enough values for the requested operation
- Example: `randomSet()` -> `<Set>`

### Tuple

- API: `randomTuple()`
- Status: `implemented-all`
- Aliases: `getRandomTuple()`
- Parameters: `count` (integer, default `1`), `items` (array, default `None`)
- Returns: `array` - Fixed-length random grouped values.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid size: length/count must be a non-negative integer within supported limits; Invalid collection: items must contain enough values for the requested operation
- Example: `randomTuple()` -> `<Tuple>`

### JSON Object

- API: `randomJsonObject()`
- Status: `implemented-all`
- Aliases: `getRandomJsonObject()`
- Parameters: `items` (array, default `None`)
- Returns: `object` - Generated JSON object from a schema or profile.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid collection: items must contain enough values for the requested operation
- Example: `randomJsonObject()` -> `<JSON Object>`

### Array

- API: `randomArray()`
- Status: `implemented-all`
- Aliases: `getRandomArray()`
- Parameters: `count` (integer, default `1`), `items` (array, default `None`)
- Returns: `array` - Array of random values.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid size: length/count must be a non-negative integer within supported limits; Invalid collection: items must contain enough values for the requested operation
- Example: `randomArray()` -> `<Array>`

### Matrix

- API: `randomMatrix()`
- Status: `implemented-all`
- Aliases: `getRandomMatrix()`
- Parameters: `count` (integer, default `1`), `items` (array, default `None`)
- Returns: `array` - Two-dimensional numeric or boolean matrix.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type; Invalid size: length/count must be a non-negative integer within supported limits; Invalid collection: items must contain enough values for the requested operation
- Example: `randomMatrix()` -> `<Matrix>`

## Developer data

### Semantic Version

- API: `randomSemver()`
- Status: `implemented-all`
- Aliases: `getRandomSemver()`
- Parameters: None
- Returns: `string` - Semantic version string.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomSemver()` -> `<Semantic Version>`

### Git SHA

- API: `randomGitSha()`
- Status: `implemented-all`
- Aliases: `getRandomGitSha()`
- Parameters: None
- Returns: `string` - Git commit hash-like value.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomGitSha()` -> `<Git SHA>`

### Package Name

- API: `randomPackageName()`
- Status: `implemented-all`
- Aliases: `getRandomPackageName()`
- Parameters: None
- Returns: `string` - Package or module name.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomPackageName()` -> `<Package Name>`

### File Name

- API: `randomFileName()`
- Status: `implemented-all`
- Aliases: `getRandomFileName()`
- Parameters: None
- Returns: `string` - File name.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomFileName()` -> `<File Name>`

### File Extension

- API: `randomFileExtension()`
- Status: `implemented-all`
- Aliases: `getRandomFileExtension()`
- Parameters: None
- Returns: `string` - File extension.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomFileExtension()` -> `<File Extension>`

### File Path

- API: `randomFilePath()`
- Status: `implemented-all`
- Aliases: `getRandomFilePath()`
- Parameters: None
- Returns: `string` - File path.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomFilePath()` -> `<File Path>`

### Directory Path

- API: `randomDirectoryPath()`
- Status: `implemented-all`
- Aliases: `getRandomDirectoryPath()`
- Parameters: None
- Returns: `string` - Directory path.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomDirectoryPath()` -> `<Directory Path>`

### Log Level

- API: `randomLogLevel()`
- Status: `implemented-all`
- Aliases: `getRandomLogLevel()`
- Parameters: None
- Returns: `string` - Logging severity.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomLogLevel()` -> `<Log Level>`

### HTTP Method

- API: `randomHttpMethod()`
- Status: `implemented-all`
- Aliases: `getRandomHttpMethod()`
- Parameters: None
- Returns: `string` - HTTP verb.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomHttpMethod()` -> `<HTTP Method>`

### Environment Name

- API: `randomEnvironmentName()`
- Status: `implemented-all`
- Aliases: `getRandomEnvironmentName()`
- Parameters: None
- Returns: `string` - Environment label such as dev or prod.
- Content safety: `safe-default`
- Dataset: `in-house-beta-json`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomEnvironmentName()` -> `<Environment Name>`

## Science and math

### 2D Vector

- API: `randomVector2()`
- Status: `implemented-all`
- Aliases: `getRandomVector2()`
- Parameters: None
- Returns: `object` - Two-dimensional vector.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomVector2()` -> `<2D Vector>`

### 3D Vector

- API: `randomVector3()`
- Status: `implemented-all`
- Aliases: `getRandomVector3()`
- Parameters: None
- Returns: `object` - Three-dimensional vector.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomVector3()` -> `<3D Vector>`

### Normal Distribution Value

- API: `randomNormal()`
- Status: `implemented-all`
- Aliases: `getRandomNormal()`
- Parameters: `min` (number, default `None`), `max` (number, default `None`)
- Returns: `float` - Value drawn from a normal distribution.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid range: min must be less than or equal to max; Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomNormal()` -> `<Normal Distribution Value>`

### Weighted Number

- API: `randomWeightedNumber()`
- Status: `implemented-all`
- Aliases: `getRandomWeightedNumber()`
- Parameters: `min` (number, default `None`), `max` (number, default `None`), `weights` (array, required)
- Returns: `float` - Number selected from weighted ranges.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid range: min must be less than or equal to max; Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomWeightedNumber()` -> `<Weighted Number>`

### Unit

- API: `randomUnit()`
- Status: `implemented-all`
- Aliases: `getRandomUnit()`
- Parameters: None
- Returns: `string` - Measurement unit label.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomUnit()` -> `<Unit>`

### Measurement

- API: `randomMeasurement()`
- Status: `implemented-all`
- Aliases: `getRandomMeasurement()`
- Parameters: None
- Returns: `object` - Numeric value with unit.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomMeasurement()` -> `<Measurement>`

### Temperature

- API: `randomTemperature()`
- Status: `implemented-all`
- Aliases: `getRandomTemperature()`
- Parameters: `min` (number, default `None`), `max` (number, default `None`)
- Returns: `string` - Temperature value.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid range: min must be less than or equal to max; Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomTemperature()` -> `<Temperature>`

### Duration Milliseconds

- API: `randomDurationMs()`
- Status: `implemented-all`
- Aliases: `getRandomDurationMs()`
- Parameters: `min` (number, default `None`), `max` (number, default `None`)
- Returns: `string` - Duration represented in milliseconds.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid range: min must be less than or equal to max; Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomDurationMs()` -> `<Duration Milliseconds>`

### Probability

- API: `randomProbability()`
- Status: `implemented-all`
- Aliases: `getRandomProbability()`
- Parameters: `min` (number, default `None`), `max` (number, default `None`)
- Returns: `string` - Probability from 0 to 1.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid range: min must be less than or equal to max; Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomProbability()` -> `<Probability>`

### Range

- API: `randomRange()`
- Status: `implemented-all`
- Aliases: `getRandomRange()`
- Parameters: `min` (number, default `None`), `max` (number, default `None`)
- Returns: `object` - Range with lower and upper bounds.
- Content safety: `not-applicable`
- Dataset: `none`
- Errors: Invalid range: min must be less than or equal to max; Invalid option: unsupported format, locale, corpus, or shape for this output type
- Example: `randomRange()` -> `<Range>`
