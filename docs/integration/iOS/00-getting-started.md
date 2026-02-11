---
sidebar_position: 1
title: iOS 시작하기
---

## 사전 확인 사항

- 연동 키: adsynapse 콘솔/관리자에게 발급받은 키
- 최소 타겟: iOS 13.0 이상
- 개발 환경: Xcode 14.1 이상

## SDK 설치 (Swift Package Manager)

Xcode에서 `File > Add Packages...`를 선택하고 아래 URL을 추가합니다.

```text
https://github.com/Infinit-C/adsynapse-ios-sdk
```

## Info.plist 설정

`Info.plist`에 아래 키를 추가합니다.

- `IADApplicationIdentifier` (필수, 앱 키)
- `ISSApplicationKey` (선택, 원격 디버그/보안 키)

```xml
<key>IADApplicationIdentifier</key>
<string>adsynapse-ac-xxxxxxxxxxxx-xxxxxxxxxxx</string>

<key>ISSApplicationKey</key>
<string>adsynapse-ss-xxxxxxxxxxxx-xxxxxxxxxxx</string>
```

선택사항(ATT 사용 시):

```xml
<key>NSUserTrackingUsageDescription</key>
<string>광고 식별자를 사용하여 맞춤형 광고를 제공합니다.</string>
```
