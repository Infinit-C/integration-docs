---
sidebar_position: 1
title: iOS 시작하기
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## 사전 확인 사항

adsynapse iOS SDK는 아래 사항이 충족해야됩니다.

- **연동 키 발급:** adsynapse 콘솔 또는 관리자에게 발급받은 키가 필요합니다.
- **개발 환경:** `Xcode 14.1` 버전 이상이 필요합니다.
- **타겟 버전:** iOS `11.0` 버전 이상이어야 합니다.

---

## SDK 설치 (Installation)

adsynapse iOS SDK는 **Swift Package Manager**를 통해 제공됩니다.

### 저장소 추가 (Project Level)

**Xcode 메뉴의 File → Add Packages...** 메뉴에서 아래 URL을 입력하여 패키지를 추가합니다.

  ```html
  https://github.com/Infinit-C/adsynapse-ios-sdk
  ```

사용할 adsynapse SDK 버전 혹은 **Up to Next Major Version**을 선택하는 것을 권장합니다.<br/>
추가가 완료되면 Xcode에서 자동으로 패키지를 다운로드하기 시작합니다.

**Swift Package Manager에 대해서 보다 자세한 사항은
Apple의 [Adding package dependencies to your app](https://developer.apple.com/documentation/xcode/adding-package-dependencies-to-your-app)
을 참고 하시기 바랍니다.**

## appCode, pubCode 설정

앱의 `Info.plist` 파일에 발급받은 식별자를 추가해야 합니다.
`pubCode`와 `appCode`를 각각 아래 항목에 입력하세요.

* **IADPubIdentifier**: Pub Code
* **IADAppIdentifier**: App Code

**XML 예시:**

```xml
<key>IADPubIdentifier</key>
<string>adsynapse-pc-xxxxxxxxxxxx-xxxxxxxxxxx</string>

<key>IADApplicationIdentifier</key>
<string>adsynapse-ac-xxxxxxxxxxxx-xxxxxxxxxxx</string>
```
