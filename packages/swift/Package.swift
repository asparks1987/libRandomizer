// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "LibRandomizer",
    products: [
        .library(name: "LibRandomizer", targets: ["LibRandomizer"])
    ],
    targets: [
        .target(name: "LibRandomizer")
    ]
)
