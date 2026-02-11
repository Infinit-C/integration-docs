---
sidebar_position: 1
title: Android 시작하기
---

## 사전 확인 사항

- 연동 키: adsynapse 콘솔/관리자에게 발급받은 `app_key`
- 최소 버전: `minSdk 24` 이상
- 권장 빌드 환경: `compileSdk 36`, Java/Kotlin 17

## SDK 설치

`settings.gradle.kts`(또는 프로젝트 레벨 `repositories`)에 저장소를 추가합니다.

```kotlin
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
        maven(url = "https://nexus.infinit-c.com/repository/maven-public/")
    }
}

dependencyResolutionManagement {
    repositories {
        google()
        mavenCentral()
        maven(url = "https://nexus.infinit-c.com/repository/maven-public/")
    }
}
```

앱 모듈(`app/build.gradle.kts`)에 SDK를 추가합니다.

```kotlin
dependencies {
    implementation("com.infinitc.adsynapse:adsynapse-sdk:1.0.0")
}
```

다음 단계에서 `AndroidManifest.xml` 설정을 진행하세요.
