---
sidebar_position: 1
title: Flutter 플러그인 시작하기
---

## 사전 확인 사항

- Flutter 3.25.0 이상
- Android Studio / Xcode 설치
- 플랫폼별 adsynapse 키 발급

## 플러그인 설치

배포 방식에 맞춰 `pubspec.yaml`에 추가합니다.

Git 의존성 예시:

```yaml
dependencies:
  adsynapse_flutter_sdk:
    git:
      url: https://github.com/Infinit-C/adsynapse-flutter-sdk.git
      ref: main
```

로컬 경로 예시:

```yaml
dependencies:
  adsynapse_flutter_sdk:
    path: ../adsynapse_flutter_sdk
```

## 플랫폼 설정

### Android (`android/app/src/main/AndroidManifest.xml`)

```xml
<meta-data
    android:name="com.infinitc.adsynapse.app_key"
    android:value="adsynapse-ac-xxxxxxxxxxxx-xxxxxxxxxxx" />

<meta-data
    android:name="com.infinitc.adsynapse.debug_mode"
    android:value="false" />
```

### iOS (`ios/Runner/Info.plist`)

```xml
<key>IADApplicationIdentifier</key>
<string>adsynapse-ac-xxxxxxxxxxxx-xxxxxxxxxxx</string>

<key>ISSApplicationKey</key>
<string>adsynapse-ss-xxxxxxxxxxxx-xxxxxxxxxxx</string>
```

## 초기화 / 상태 확인 / 해제

```dart
await AdsynapseFlutterSdkPlugin.initialize('YOUR_API_KEY');

final initialized = await AdsynapseFlutterSdkPlugin.isInitialized();

await AdsynapseFlutterSdkPlugin.deinitialize();
```

초기화 전에 `loadBanner`/`loadNative`를 호출하면 에러가 발생합니다.
