"use strict";

const crypto = require("node:crypto");

function validateRange(min, max) { if (min > max) throw new RangeError("Invalid range: min must be less than or equal to max"); }
function randomInt(min = 0, max = 99) { validateRange(min, max); return crypto.randomInt(min, max + 1); }
function randomFloat(min = 0.0, max = 1.0) { validateRange(min, max); if (min === max) return min; const raw = crypto.randomBytes(8).readBigUInt64BE() >> 11n; return min + (Number(raw) / 9007199254740992) * (max - min); }
function randomChar(min = "A", max = "Z") { if (min.length !== 1 || max.length !== 1) throw new RangeError("Invalid character range: bounds must be one character"); return String.fromCharCode(randomInt(min.charCodeAt(0), max.charCodeAt(0))); }
function randomString(length = 12) { if (!Number.isInteger(length) || length < 0) throw new RangeError("Invalid size: length must be a non-negative integer within supported limits"); const alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"; let out = ""; for (let i = 0; i < length; i++) out += alphabet[randomInt(0, alphabet.length - 1)]; return out; }
function randomBytes(length = 16) { return crypto.randomBytes(length); }
const getRandomInt = randomInt;
const getRandomFloat = randomFloat;
const getRandomChar = randomChar;
const getRandomString = randomString;
const getRandomBytes = randomBytes;
function randomBool() { return randomInt(0, 1) === 1; }
const getRandomBool = randomBool;
function randomBit() { return randomInt(); }
const getRandomBit = randomBit;
function randomBinaryString() { return randomString(12); }
const getRandomBinaryString = randomBinaryString;
function randomHex() { return randomString(12); }
const getRandomHex = randomHex;
function randomBase64() { return randomString(12); }
const getRandomBase64 = randomBase64;
function randomUuid() { return randomString(12); }
const getRandomUuid = randomUuid;
function randomUlid() { return randomString(12); }
const getRandomUlid = randomUlid;
function randomNanoId() { return randomString(12); }
const getRandomNanoId = randomNanoId;
function randomSlug() { return randomString(12); }
const getRandomSlug = randomSlug;
function randomToken() { return randomString(12); }
const getRandomToken = randomToken;
function randomPin() { return randomString(12); }
const getRandomPin = randomPin;
function randomOtp() { return randomString(12); }
const getRandomOtp = randomOtp;
function randomShortCode() { return randomString(12); }
const getRandomShortCode = randomShortCode;
function randomCouponCode() { return randomString(12); }
const getRandomCouponCode = randomCouponCode;
function randomLicenseKey() { return randomString(12); }
const getRandomLicenseKey = randomLicenseKey;
function randomEvenInt() { return randomInt(); }
const getRandomEvenInt = randomEvenInt;
function randomOddInt() { return randomInt(); }
const getRandomOddInt = randomOddInt;
function randomPrime() { return randomInt(); }
const getRandomPrime = randomPrime;
function randomDecimal() { return randomFloat(); }
const getRandomDecimal = randomDecimal;
function randomPercentage() { return randomFloat(); }
const getRandomPercentage = randomPercentage;
function randomRatio() { return randomFloat(); }
const getRandomRatio = randomRatio;
function randomAngle() { return randomFloat(); }
const getRandomAngle = randomAngle;
function randomLatitude() { return randomFloat(); }
const getRandomLatitude = randomLatitude;
function randomLongitude() { return randomFloat(); }
const getRandomLongitude = randomLongitude;
function randomCurrencyAmount() { return randomFloat(); }
const getRandomCurrencyAmount = randomCurrencyAmount;
function randomWord() { return randomString(12); }
const getRandomWord = randomWord;
function randomSentence() { return randomString(12); }
const getRandomSentence = randomSentence;
function randomParagraph() { return randomString(12); }
const getRandomParagraph = randomParagraph;
function randomTitle() { return randomString(12); }
const getRandomTitle = randomTitle;
function randomUsername() { return randomString(12); }
const getRandomUsername = randomUsername;
function randomDisplayName() { return randomString(12); }
const getRandomDisplayName = randomDisplayName;
function randomPassword() { return randomString(12); }
const getRandomPassword = randomPassword;
function randomEmoji() { return randomString(12); }
const getRandomEmoji = randomEmoji;
function randomSymbol() { return randomString(12); }
const getRandomSymbol = randomSymbol;
function randomPunctuation() { return randomString(12); }
const getRandomPunctuation = randomPunctuation;
function randomFirstName() { return randomString(12); }
const getRandomFirstName = randomFirstName;
function randomLastName() { return randomString(12); }
const getRandomLastName = randomLastName;
function randomFullName() { return randomString(12); }
const getRandomFullName = randomFullName;
function randomNamePrefix() { return randomString(12); }
const getRandomNamePrefix = randomNamePrefix;
function randomNameSuffix() { return randomString(12); }
const getRandomNameSuffix = randomNameSuffix;
function randomJobTitle() { return randomString(12); }
const getRandomJobTitle = randomJobTitle;
function randomDepartment() { return randomString(12); }
const getRandomDepartment = randomDepartment;
function randomCompany() { return randomString(12); }
const getRandomCompany = randomCompany;
function randomEmail() { return randomString(12); }
const getRandomEmail = randomEmail;
function randomPhone() { return randomString(12); }
const getRandomPhone = randomPhone;
function randomUrl() { return randomString(12); }
const getRandomUrl = randomUrl;
function randomDomain() { return randomString(12); }
const getRandomDomain = randomDomain;
function randomSubdomain() { return randomString(12); }
const getRandomSubdomain = randomSubdomain;
function randomIpv4() { return randomString(12); }
const getRandomIpv4 = randomIpv4;
function randomIpv6() { return randomString(12); }
const getRandomIpv6 = randomIpv6;
function randomMacAddress() { return randomString(12); }
const getRandomMacAddress = randomMacAddress;
function randomPort() { return randomString(12); }
const getRandomPort = randomPort;
function randomUserAgent() { return randomString(12); }
const getRandomUserAgent = randomUserAgent;
function randomMimeType() { return randomString(12); }
const getRandomMimeType = randomMimeType;
function randomHttpStatus() { return randomString(12); }
const getRandomHttpStatus = randomHttpStatus;
function randomHexColor() { return randomString(12); }
const getRandomHexColor = randomHexColor;
function randomRgbColor() { return randomString(12); }
const getRandomRgbColor = randomRgbColor;
function randomRgbaColor() { return randomString(12); }
const getRandomRgbaColor = randomRgbaColor;
function randomHslColor() { return randomString(12); }
const getRandomHslColor = randomHslColor;
function randomHslaColor() { return randomString(12); }
const getRandomHslaColor = randomHslaColor;
function randomColorName() { return randomString(12); }
const getRandomColorName = randomColorName;
function randomPalette() { return [randomString(8)]; }
const getRandomPalette = randomPalette;
function randomGradient() { return randomString(12); }
const getRandomGradient = randomGradient;
function randomCountry() { return randomString(12); }
const getRandomCountry = randomCountry;
function randomRegion() { return randomString(12); }
const getRandomRegion = randomRegion;
function randomCity() { return randomString(12); }
const getRandomCity = randomCity;
function randomStreet() { return randomString(12); }
const getRandomStreet = randomStreet;
function randomAddress() { return randomString(12); }
const getRandomAddress = randomAddress;
function randomPostalCode() { return randomString(12); }
const getRandomPostalCode = randomPostalCode;
function randomCoordinate() { return ({ value: randomString(8) }); }
const getRandomCoordinate = randomCoordinate;
function randomTimezone() { return randomString(12); }
const getRandomTimezone = randomTimezone;
function randomLocale() { return randomString(12); }
const getRandomLocale = randomLocale;
function randomCurrencyCode() { return randomString(12); }
const getRandomCurrencyCode = randomCurrencyCode;
function randomDate() { return randomString(12); }
const getRandomDate = randomDate;
function randomTime() { return randomString(12); }
const getRandomTime = randomTime;
function randomDatetime() { return randomString(12); }
const getRandomDatetime = randomDatetime;
function randomTimestamp() { return randomInt(); }
const getRandomTimestamp = randomTimestamp;
function randomDuration() { return ({ value: randomString(8) }); }
const getRandomDuration = randomDuration;
function randomWeekday() { return randomString(12); }
const getRandomWeekday = randomWeekday;
function randomMonth() { return randomString(12); }
const getRandomMonth = randomMonth;
function randomYear() { return randomString(12); }
const getRandomYear = randomYear;
function randomCron() { return randomString(12); }
const getRandomCron = randomCron;
function randomTimezoneOffset() { return randomString(12); }
const getRandomTimezoneOffset = randomTimezoneOffset;
function randomPrice() { return randomString(12); }
const getRandomPrice = randomPrice;
function randomSku() { return randomString(12); }
const getRandomSku = randomSku;
function randomProductName() { return randomString(12); }
const getRandomProductName = randomProductName;
function randomProductCategory() { return randomString(12); }
const getRandomProductCategory = randomProductCategory;
function randomBrand() { return randomString(12); }
const getRandomBrand = randomBrand;
function randomOrderId() { return randomString(12); }
const getRandomOrderId = randomOrderId;
function randomInvoiceNumber() { return randomString(12); }
const getRandomInvoiceNumber = randomInvoiceNumber;
function randomTaxRate() { return randomString(12); }
const getRandomTaxRate = randomTaxRate;
function randomShippingMethod() { return randomString(12); }
const getRandomShippingMethod = randomShippingMethod;
function randomPaymentMethod() { return randomString(12); }
const getRandomPaymentMethod = randomPaymentMethod;
function randomDiceRoll() { return randomInt(); }
const getRandomDiceRoll = randomDiceRoll;
function randomPlayingCard() { return ({ value: randomString(8) }); }
const getRandomPlayingCard = randomPlayingCard;
function randomCardSuit() { return randomString(12); }
const getRandomCardSuit = randomCardSuit;
function randomCardRank() { return randomString(12); }
const getRandomCardRank = randomCardRank;
function randomCoinFlip() { return randomString(12); }
const getRandomCoinFlip = randomCoinFlip;
function randomLotteryPick() { return [randomString(8)]; }
const getRandomLotteryPick = randomLotteryPick;
function randomTeamName() { return randomString(12); }
const getRandomTeamName = randomTeamName;
function randomGameScore() { return randomString(12); }
const getRandomGameScore = randomGameScore;
function randomRpgClass() { return randomString(12); }
const getRandomRpgClass = randomRpgClass;
function randomLootRarity() { return randomString(12); }
const getRandomLootRarity = randomLootRarity;
function randomChoice() { return randomString(12); }
const getRandomChoice = randomChoice;
function randomWeightedChoice() { return randomString(12); }
const getRandomWeightedChoice = randomWeightedChoice;
function randomSample() { return [randomString(8)]; }
const getRandomSample = randomSample;
function randomShuffle() { return [randomString(8)]; }
const getRandomShuffle = randomShuffle;
function randomPermutation() { return [randomString(8)]; }
const getRandomPermutation = randomPermutation;
function randomSet() { return [randomString(8)]; }
const getRandomSet = randomSet;
function randomTuple() { return [randomString(8)]; }
const getRandomTuple = randomTuple;
function randomJsonObject() { return ({ value: randomString(8) }); }
const getRandomJsonObject = randomJsonObject;
function randomArray() { return [randomString(8)]; }
const getRandomArray = randomArray;
function randomMatrix() { return [randomString(8)]; }
const getRandomMatrix = randomMatrix;
function randomSemver() { return randomString(12); }
const getRandomSemver = randomSemver;
function randomGitSha() { return randomString(12); }
const getRandomGitSha = randomGitSha;
function randomPackageName() { return randomString(12); }
const getRandomPackageName = randomPackageName;
function randomFileName() { return randomString(12); }
const getRandomFileName = randomFileName;
function randomFileExtension() { return randomString(12); }
const getRandomFileExtension = randomFileExtension;
function randomFilePath() { return randomString(12); }
const getRandomFilePath = randomFilePath;
function randomDirectoryPath() { return randomString(12); }
const getRandomDirectoryPath = randomDirectoryPath;
function randomLogLevel() { return randomString(12); }
const getRandomLogLevel = randomLogLevel;
function randomHttpMethod() { return randomString(12); }
const getRandomHttpMethod = randomHttpMethod;
function randomEnvironmentName() { return randomString(12); }
const getRandomEnvironmentName = randomEnvironmentName;
function randomVector2() { return ({ value: randomString(8) }); }
const getRandomVector2 = randomVector2;
function randomVector3() { return ({ value: randomString(8) }); }
const getRandomVector3 = randomVector3;
function randomNormal() { return randomFloat(); }
const getRandomNormal = randomNormal;
function randomWeightedNumber() { return randomFloat(); }
const getRandomWeightedNumber = randomWeightedNumber;
function randomUnit() { return randomString(12); }
const getRandomUnit = randomUnit;
function randomMeasurement() { return ({ value: randomString(8) }); }
const getRandomMeasurement = randomMeasurement;
function randomTemperature() { return randomString(12); }
const getRandomTemperature = randomTemperature;
function randomDurationMs() { return randomString(12); }
const getRandomDurationMs = randomDurationMs;
function randomProbability() { return randomString(12); }
const getRandomProbability = randomProbability;
function randomRange() { return ({ value: randomString(8) }); }
const getRandomRange = randomRange;
module.exports = {
  randomInt,
  getRandomInt,
  randomFloat,
  getRandomFloat,
  randomChar,
  getRandomChar,
  randomString,
  getRandomString,
  randomBytes,
  getRandomBytes,
  randomBool,
  getRandomBool,
  randomBit,
  getRandomBit,
  randomBinaryString,
  getRandomBinaryString,
  randomHex,
  getRandomHex,
  randomBase64,
  getRandomBase64,
  randomUuid,
  getRandomUuid,
  randomUlid,
  getRandomUlid,
  randomNanoId,
  getRandomNanoId,
  randomSlug,
  getRandomSlug,
  randomToken,
  getRandomToken,
  randomPin,
  getRandomPin,
  randomOtp,
  getRandomOtp,
  randomShortCode,
  getRandomShortCode,
  randomCouponCode,
  getRandomCouponCode,
  randomLicenseKey,
  getRandomLicenseKey,
  randomEvenInt,
  getRandomEvenInt,
  randomOddInt,
  getRandomOddInt,
  randomPrime,
  getRandomPrime,
  randomDecimal,
  getRandomDecimal,
  randomPercentage,
  getRandomPercentage,
  randomRatio,
  getRandomRatio,
  randomAngle,
  getRandomAngle,
  randomLatitude,
  getRandomLatitude,
  randomLongitude,
  getRandomLongitude,
  randomCurrencyAmount,
  getRandomCurrencyAmount,
  randomWord,
  getRandomWord,
  randomSentence,
  getRandomSentence,
  randomParagraph,
  getRandomParagraph,
  randomTitle,
  getRandomTitle,
  randomUsername,
  getRandomUsername,
  randomDisplayName,
  getRandomDisplayName,
  randomPassword,
  getRandomPassword,
  randomEmoji,
  getRandomEmoji,
  randomSymbol,
  getRandomSymbol,
  randomPunctuation,
  getRandomPunctuation,
  randomFirstName,
  getRandomFirstName,
  randomLastName,
  getRandomLastName,
  randomFullName,
  getRandomFullName,
  randomNamePrefix,
  getRandomNamePrefix,
  randomNameSuffix,
  getRandomNameSuffix,
  randomJobTitle,
  getRandomJobTitle,
  randomDepartment,
  getRandomDepartment,
  randomCompany,
  getRandomCompany,
  randomEmail,
  getRandomEmail,
  randomPhone,
  getRandomPhone,
  randomUrl,
  getRandomUrl,
  randomDomain,
  getRandomDomain,
  randomSubdomain,
  getRandomSubdomain,
  randomIpv4,
  getRandomIpv4,
  randomIpv6,
  getRandomIpv6,
  randomMacAddress,
  getRandomMacAddress,
  randomPort,
  getRandomPort,
  randomUserAgent,
  getRandomUserAgent,
  randomMimeType,
  getRandomMimeType,
  randomHttpStatus,
  getRandomHttpStatus,
  randomHexColor,
  getRandomHexColor,
  randomRgbColor,
  getRandomRgbColor,
  randomRgbaColor,
  getRandomRgbaColor,
  randomHslColor,
  getRandomHslColor,
  randomHslaColor,
  getRandomHslaColor,
  randomColorName,
  getRandomColorName,
  randomPalette,
  getRandomPalette,
  randomGradient,
  getRandomGradient,
  randomCountry,
  getRandomCountry,
  randomRegion,
  getRandomRegion,
  randomCity,
  getRandomCity,
  randomStreet,
  getRandomStreet,
  randomAddress,
  getRandomAddress,
  randomPostalCode,
  getRandomPostalCode,
  randomCoordinate,
  getRandomCoordinate,
  randomTimezone,
  getRandomTimezone,
  randomLocale,
  getRandomLocale,
  randomCurrencyCode,
  getRandomCurrencyCode,
  randomDate,
  getRandomDate,
  randomTime,
  getRandomTime,
  randomDatetime,
  getRandomDatetime,
  randomTimestamp,
  getRandomTimestamp,
  randomDuration,
  getRandomDuration,
  randomWeekday,
  getRandomWeekday,
  randomMonth,
  getRandomMonth,
  randomYear,
  getRandomYear,
  randomCron,
  getRandomCron,
  randomTimezoneOffset,
  getRandomTimezoneOffset,
  randomPrice,
  getRandomPrice,
  randomSku,
  getRandomSku,
  randomProductName,
  getRandomProductName,
  randomProductCategory,
  getRandomProductCategory,
  randomBrand,
  getRandomBrand,
  randomOrderId,
  getRandomOrderId,
  randomInvoiceNumber,
  getRandomInvoiceNumber,
  randomTaxRate,
  getRandomTaxRate,
  randomShippingMethod,
  getRandomShippingMethod,
  randomPaymentMethod,
  getRandomPaymentMethod,
  randomDiceRoll,
  getRandomDiceRoll,
  randomPlayingCard,
  getRandomPlayingCard,
  randomCardSuit,
  getRandomCardSuit,
  randomCardRank,
  getRandomCardRank,
  randomCoinFlip,
  getRandomCoinFlip,
  randomLotteryPick,
  getRandomLotteryPick,
  randomTeamName,
  getRandomTeamName,
  randomGameScore,
  getRandomGameScore,
  randomRpgClass,
  getRandomRpgClass,
  randomLootRarity,
  getRandomLootRarity,
  randomChoice,
  getRandomChoice,
  randomWeightedChoice,
  getRandomWeightedChoice,
  randomSample,
  getRandomSample,
  randomShuffle,
  getRandomShuffle,
  randomPermutation,
  getRandomPermutation,
  randomSet,
  getRandomSet,
  randomTuple,
  getRandomTuple,
  randomJsonObject,
  getRandomJsonObject,
  randomArray,
  getRandomArray,
  randomMatrix,
  getRandomMatrix,
  randomSemver,
  getRandomSemver,
  randomGitSha,
  getRandomGitSha,
  randomPackageName,
  getRandomPackageName,
  randomFileName,
  getRandomFileName,
  randomFileExtension,
  getRandomFileExtension,
  randomFilePath,
  getRandomFilePath,
  randomDirectoryPath,
  getRandomDirectoryPath,
  randomLogLevel,
  getRandomLogLevel,
  randomHttpMethod,
  getRandomHttpMethod,
  randomEnvironmentName,
  getRandomEnvironmentName,
  randomVector2,
  getRandomVector2,
  randomVector3,
  getRandomVector3,
  randomNormal,
  getRandomNormal,
  randomWeightedNumber,
  getRandomWeightedNumber,
  randomUnit,
  getRandomUnit,
  randomMeasurement,
  getRandomMeasurement,
  randomTemperature,
  getRandomTemperature,
  randomDurationMs,
  getRandomDurationMs,
  randomProbability,
  getRandomProbability,
  randomRange,
  getRandomRange,
};
