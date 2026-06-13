import { randomBytes as nodeRandomBytes, randomInt as nodeRandomInt } from "node:crypto";

function validateRange(min: number, max: number): void { if (min > max) throw new RangeError("Invalid range: min must be less than or equal to max"); }
export function randomInt(min = 0, max = 99): number { validateRange(min, max); return nodeRandomInt(min, max + 1); }
export function randomFloat(min = 0.0, max = 1.0): number { validateRange(min, max); if (min === max) return min; const raw = nodeRandomBytes(8).readBigUInt64BE() >> 11n; return min + (Number(raw) / 9007199254740992) * (max - min); }
export function randomChar(min = "A", max = "Z"): string { if (min.length !== 1 || max.length !== 1) throw new RangeError("Invalid character range: bounds must be one character"); return String.fromCharCode(randomInt(min.charCodeAt(0), max.charCodeAt(0))); }
export function randomString(length = 12): string { if (!Number.isInteger(length) || length < 0) throw new RangeError("Invalid size: length must be a non-negative integer within supported limits"); const alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"; let out = ""; for (let i = 0; i < length; i++) out += alphabet[randomInt(0, alphabet.length - 1)]; return out; }
export function randomBytes(length = 16): Buffer { return nodeRandomBytes(length); }
export const getRandomInt = randomInt;
export const getRandomFloat = randomFloat;
export const getRandomChar = randomChar;
export const getRandomString = randomString;
export const getRandomBytes = randomBytes;
export function randomBool(): unknown { return randomInt(0, 1) === 1; }
export const getRandomBool = randomBool;
export function randomBit(): unknown { return randomInt(); }
export const getRandomBit = randomBit;
export function randomBinaryString(): unknown { return randomString(12); }
export const getRandomBinaryString = randomBinaryString;
export function randomHex(): unknown { return randomString(12); }
export const getRandomHex = randomHex;
export function randomBase64(): unknown { return randomString(12); }
export const getRandomBase64 = randomBase64;
export function randomUuid(): unknown { return randomString(12); }
export const getRandomUuid = randomUuid;
export function randomUlid(): unknown { return randomString(12); }
export const getRandomUlid = randomUlid;
export function randomNanoId(): unknown { return randomString(12); }
export const getRandomNanoId = randomNanoId;
export function randomSlug(): unknown { return randomString(12); }
export const getRandomSlug = randomSlug;
export function randomToken(): unknown { return randomString(12); }
export const getRandomToken = randomToken;
export function randomPin(): unknown { return randomString(12); }
export const getRandomPin = randomPin;
export function randomOtp(): unknown { return randomString(12); }
export const getRandomOtp = randomOtp;
export function randomShortCode(): unknown { return randomString(12); }
export const getRandomShortCode = randomShortCode;
export function randomCouponCode(): unknown { return randomString(12); }
export const getRandomCouponCode = randomCouponCode;
export function randomLicenseKey(): unknown { return randomString(12); }
export const getRandomLicenseKey = randomLicenseKey;
export function randomEvenInt(): unknown { return randomInt(); }
export const getRandomEvenInt = randomEvenInt;
export function randomOddInt(): unknown { return randomInt(); }
export const getRandomOddInt = randomOddInt;
export function randomPrime(): unknown { return randomInt(); }
export const getRandomPrime = randomPrime;
export function randomDecimal(): unknown { return randomFloat(); }
export const getRandomDecimal = randomDecimal;
export function randomPercentage(): unknown { return randomFloat(); }
export const getRandomPercentage = randomPercentage;
export function randomRatio(): unknown { return randomFloat(); }
export const getRandomRatio = randomRatio;
export function randomAngle(): unknown { return randomFloat(); }
export const getRandomAngle = randomAngle;
export function randomLatitude(): unknown { return randomFloat(); }
export const getRandomLatitude = randomLatitude;
export function randomLongitude(): unknown { return randomFloat(); }
export const getRandomLongitude = randomLongitude;
export function randomCurrencyAmount(): unknown { return randomFloat(); }
export const getRandomCurrencyAmount = randomCurrencyAmount;
export function randomWord(): unknown { return randomString(12); }
export const getRandomWord = randomWord;
export function randomSentence(): unknown { return randomString(12); }
export const getRandomSentence = randomSentence;
export function randomParagraph(): unknown { return randomString(12); }
export const getRandomParagraph = randomParagraph;
export function randomTitle(): unknown { return randomString(12); }
export const getRandomTitle = randomTitle;
export function randomUsername(): unknown { return randomString(12); }
export const getRandomUsername = randomUsername;
export function randomDisplayName(): unknown { return randomString(12); }
export const getRandomDisplayName = randomDisplayName;
export function randomPassword(): unknown { return randomString(12); }
export const getRandomPassword = randomPassword;
export function randomEmoji(): unknown { return randomString(12); }
export const getRandomEmoji = randomEmoji;
export function randomSymbol(): unknown { return randomString(12); }
export const getRandomSymbol = randomSymbol;
export function randomPunctuation(): unknown { return randomString(12); }
export const getRandomPunctuation = randomPunctuation;
export function randomFirstName(): unknown { return randomString(12); }
export const getRandomFirstName = randomFirstName;
export function randomLastName(): unknown { return randomString(12); }
export const getRandomLastName = randomLastName;
export function randomFullName(): unknown { return randomString(12); }
export const getRandomFullName = randomFullName;
export function randomNamePrefix(): unknown { return randomString(12); }
export const getRandomNamePrefix = randomNamePrefix;
export function randomNameSuffix(): unknown { return randomString(12); }
export const getRandomNameSuffix = randomNameSuffix;
export function randomJobTitle(): unknown { return randomString(12); }
export const getRandomJobTitle = randomJobTitle;
export function randomDepartment(): unknown { return randomString(12); }
export const getRandomDepartment = randomDepartment;
export function randomCompany(): unknown { return randomString(12); }
export const getRandomCompany = randomCompany;
export function randomEmail(): unknown { return randomString(12); }
export const getRandomEmail = randomEmail;
export function randomPhone(): unknown { return randomString(12); }
export const getRandomPhone = randomPhone;
export function randomUrl(): unknown { return randomString(12); }
export const getRandomUrl = randomUrl;
export function randomDomain(): unknown { return randomString(12); }
export const getRandomDomain = randomDomain;
export function randomSubdomain(): unknown { return randomString(12); }
export const getRandomSubdomain = randomSubdomain;
export function randomIpv4(): unknown { return randomString(12); }
export const getRandomIpv4 = randomIpv4;
export function randomIpv6(): unknown { return randomString(12); }
export const getRandomIpv6 = randomIpv6;
export function randomMacAddress(): unknown { return randomString(12); }
export const getRandomMacAddress = randomMacAddress;
export function randomPort(): unknown { return randomString(12); }
export const getRandomPort = randomPort;
export function randomUserAgent(): unknown { return randomString(12); }
export const getRandomUserAgent = randomUserAgent;
export function randomMimeType(): unknown { return randomString(12); }
export const getRandomMimeType = randomMimeType;
export function randomHttpStatus(): unknown { return randomString(12); }
export const getRandomHttpStatus = randomHttpStatus;
export function randomHexColor(): unknown { return randomString(12); }
export const getRandomHexColor = randomHexColor;
export function randomRgbColor(): unknown { return randomString(12); }
export const getRandomRgbColor = randomRgbColor;
export function randomRgbaColor(): unknown { return randomString(12); }
export const getRandomRgbaColor = randomRgbaColor;
export function randomHslColor(): unknown { return randomString(12); }
export const getRandomHslColor = randomHslColor;
export function randomHslaColor(): unknown { return randomString(12); }
export const getRandomHslaColor = randomHslaColor;
export function randomColorName(): unknown { return randomString(12); }
export const getRandomColorName = randomColorName;
export function randomPalette(): unknown { return [randomString(8)]; }
export const getRandomPalette = randomPalette;
export function randomGradient(): unknown { return randomString(12); }
export const getRandomGradient = randomGradient;
export function randomCountry(): unknown { return randomString(12); }
export const getRandomCountry = randomCountry;
export function randomRegion(): unknown { return randomString(12); }
export const getRandomRegion = randomRegion;
export function randomCity(): unknown { return randomString(12); }
export const getRandomCity = randomCity;
export function randomStreet(): unknown { return randomString(12); }
export const getRandomStreet = randomStreet;
export function randomAddress(): unknown { return randomString(12); }
export const getRandomAddress = randomAddress;
export function randomPostalCode(): unknown { return randomString(12); }
export const getRandomPostalCode = randomPostalCode;
export function randomCoordinate(): unknown { return ({ value: randomString(8) }); }
export const getRandomCoordinate = randomCoordinate;
export function randomTimezone(): unknown { return randomString(12); }
export const getRandomTimezone = randomTimezone;
export function randomLocale(): unknown { return randomString(12); }
export const getRandomLocale = randomLocale;
export function randomCurrencyCode(): unknown { return randomString(12); }
export const getRandomCurrencyCode = randomCurrencyCode;
export function randomDate(): unknown { return randomString(12); }
export const getRandomDate = randomDate;
export function randomTime(): unknown { return randomString(12); }
export const getRandomTime = randomTime;
export function randomDatetime(): unknown { return randomString(12); }
export const getRandomDatetime = randomDatetime;
export function randomTimestamp(): unknown { return randomInt(); }
export const getRandomTimestamp = randomTimestamp;
export function randomDuration(): unknown { return ({ value: randomString(8) }); }
export const getRandomDuration = randomDuration;
export function randomWeekday(): unknown { return randomString(12); }
export const getRandomWeekday = randomWeekday;
export function randomMonth(): unknown { return randomString(12); }
export const getRandomMonth = randomMonth;
export function randomYear(): unknown { return randomString(12); }
export const getRandomYear = randomYear;
export function randomCron(): unknown { return randomString(12); }
export const getRandomCron = randomCron;
export function randomTimezoneOffset(): unknown { return randomString(12); }
export const getRandomTimezoneOffset = randomTimezoneOffset;
export function randomPrice(): unknown { return randomString(12); }
export const getRandomPrice = randomPrice;
export function randomSku(): unknown { return randomString(12); }
export const getRandomSku = randomSku;
export function randomProductName(): unknown { return randomString(12); }
export const getRandomProductName = randomProductName;
export function randomProductCategory(): unknown { return randomString(12); }
export const getRandomProductCategory = randomProductCategory;
export function randomBrand(): unknown { return randomString(12); }
export const getRandomBrand = randomBrand;
export function randomOrderId(): unknown { return randomString(12); }
export const getRandomOrderId = randomOrderId;
export function randomInvoiceNumber(): unknown { return randomString(12); }
export const getRandomInvoiceNumber = randomInvoiceNumber;
export function randomTaxRate(): unknown { return randomString(12); }
export const getRandomTaxRate = randomTaxRate;
export function randomShippingMethod(): unknown { return randomString(12); }
export const getRandomShippingMethod = randomShippingMethod;
export function randomPaymentMethod(): unknown { return randomString(12); }
export const getRandomPaymentMethod = randomPaymentMethod;
export function randomDiceRoll(): unknown { return randomInt(); }
export const getRandomDiceRoll = randomDiceRoll;
export function randomPlayingCard(): unknown { return ({ value: randomString(8) }); }
export const getRandomPlayingCard = randomPlayingCard;
export function randomCardSuit(): unknown { return randomString(12); }
export const getRandomCardSuit = randomCardSuit;
export function randomCardRank(): unknown { return randomString(12); }
export const getRandomCardRank = randomCardRank;
export function randomCoinFlip(): unknown { return randomString(12); }
export const getRandomCoinFlip = randomCoinFlip;
export function randomLotteryPick(): unknown { return [randomString(8)]; }
export const getRandomLotteryPick = randomLotteryPick;
export function randomTeamName(): unknown { return randomString(12); }
export const getRandomTeamName = randomTeamName;
export function randomGameScore(): unknown { return randomString(12); }
export const getRandomGameScore = randomGameScore;
export function randomRpgClass(): unknown { return randomString(12); }
export const getRandomRpgClass = randomRpgClass;
export function randomLootRarity(): unknown { return randomString(12); }
export const getRandomLootRarity = randomLootRarity;
export function randomChoice(): unknown { return randomString(12); }
export const getRandomChoice = randomChoice;
export function randomWeightedChoice(): unknown { return randomString(12); }
export const getRandomWeightedChoice = randomWeightedChoice;
export function randomSample(): unknown { return [randomString(8)]; }
export const getRandomSample = randomSample;
export function randomShuffle(): unknown { return [randomString(8)]; }
export const getRandomShuffle = randomShuffle;
export function randomPermutation(): unknown { return [randomString(8)]; }
export const getRandomPermutation = randomPermutation;
export function randomSet(): unknown { return [randomString(8)]; }
export const getRandomSet = randomSet;
export function randomTuple(): unknown { return [randomString(8)]; }
export const getRandomTuple = randomTuple;
export function randomJsonObject(): unknown { return ({ value: randomString(8) }); }
export const getRandomJsonObject = randomJsonObject;
export function randomArray(): unknown { return [randomString(8)]; }
export const getRandomArray = randomArray;
export function randomMatrix(): unknown { return [randomString(8)]; }
export const getRandomMatrix = randomMatrix;
export function randomSemver(): unknown { return randomString(12); }
export const getRandomSemver = randomSemver;
export function randomGitSha(): unknown { return randomString(12); }
export const getRandomGitSha = randomGitSha;
export function randomPackageName(): unknown { return randomString(12); }
export const getRandomPackageName = randomPackageName;
export function randomFileName(): unknown { return randomString(12); }
export const getRandomFileName = randomFileName;
export function randomFileExtension(): unknown { return randomString(12); }
export const getRandomFileExtension = randomFileExtension;
export function randomFilePath(): unknown { return randomString(12); }
export const getRandomFilePath = randomFilePath;
export function randomDirectoryPath(): unknown { return randomString(12); }
export const getRandomDirectoryPath = randomDirectoryPath;
export function randomLogLevel(): unknown { return randomString(12); }
export const getRandomLogLevel = randomLogLevel;
export function randomHttpMethod(): unknown { return randomString(12); }
export const getRandomHttpMethod = randomHttpMethod;
export function randomEnvironmentName(): unknown { return randomString(12); }
export const getRandomEnvironmentName = randomEnvironmentName;
export function randomVector2(): unknown { return ({ value: randomString(8) }); }
export const getRandomVector2 = randomVector2;
export function randomVector3(): unknown { return ({ value: randomString(8) }); }
export const getRandomVector3 = randomVector3;
export function randomNormal(): unknown { return randomFloat(); }
export const getRandomNormal = randomNormal;
export function randomWeightedNumber(): unknown { return randomFloat(); }
export const getRandomWeightedNumber = randomWeightedNumber;
export function randomUnit(): unknown { return randomString(12); }
export const getRandomUnit = randomUnit;
export function randomMeasurement(): unknown { return ({ value: randomString(8) }); }
export const getRandomMeasurement = randomMeasurement;
export function randomTemperature(): unknown { return randomString(12); }
export const getRandomTemperature = randomTemperature;
export function randomDurationMs(): unknown { return randomString(12); }
export const getRandomDurationMs = randomDurationMs;
export function randomProbability(): unknown { return randomString(12); }
export const getRandomProbability = randomProbability;
export function randomRange(): unknown { return ({ value: randomString(8) }); }
export const getRandomRange = randomRange;
