plugins {
    kotlin("jvm") version "1.9.24"
    `maven-publish`
}

group = "io.github.librandomizer"
version = "0.1.0-beta.1"

kotlin {
    jvmToolchain(11)
}

publishing {
    publications {
        create<MavenPublication>("maven") {
            from(components["java"])
            pom {
                name.set("libRandomizer Kotlin SDK")
                description.set("Native Kotlin SDK for libRandomizer v1.")
                licenses {
                    license {
                        name.set("MIT License")
                        url.set("https://opensource.org/license/mit/")
                    }
                }
            }
        }
    }
}
