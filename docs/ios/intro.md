---
sidebar_position: 1
title: iOS SDK 연동
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# 매체 연동 가이드 - iOS SDK


## 1. 시작하기 (Getting Started)

### 사전 준비 사항

1.  **연동 키 발급:** adsynapse 콘솔 또는 관리자에게 발급받은 키가 필요합니다.
2.  **개발 환경:** `Xcode 14.1` 버전 이상이 필요합니다.
3.  **타겟 버전:** iOS `11.0` 버전 이상이어야 합니다.

---

## 2. SDK 설치 (Installation)

사용하는 패키지 매니저에 따라 설치 방법을 선택하세요.

<Tabs groupId="install-method">
  <TabItem value="spm" label="Swift Package Manager" default>

  **File > Xcode 메뉴의 File → Add Packages...** 메뉴에서 아래 URL을 입력하여 패키지를 추가합니다.

  ```html
  https://github.com/Infinit-C/adsynapse-ios-sdk
  ```

  사용할 adsynapse SDK 버전 혹은 **Up to Next Major Version**을 선택하는 것을 권장합니다.<br/>
  추가가 완료되면 Xcode에서 자동으로 패키지를 다운로드하기 시작합니다. 

  **Swift Package Manager에 대해서 보다 자세한 사항은 Apple의 [Adding package dependencies to your app](https://developer.apple.com/documentation/xcode/adding-package-dependencies-to-your-app)을 참고 하시기 바랍니다.**

  </TabItem>
  <TabItem value="cocoapods" label="CocoaPods">

  프로젝트의 `Podfile`에 아래 코드를 추가한 후 `pod install`을 실행하세요.

  ```ruby
  # Podfile
  pod 'adsynapse-SDK', git: "https://github.com/Infinit-C/adsynapse-ios-sdk.git", :branch => 'stable'
  ```

  터미널에서 업데이트 명령어를 실행합니다.

  ```bash
  pod install --repo-update
  ```

**CocoaPods의 사용 방법 등 자세한 사항은 [공식 문서](https://guides.cocoapods.org/using/using-cocoapods)를 확인해주세요**

  </TabItem>
</Tabs>

---

## 3. 프로젝트 설정 (Info.plist)

앱의 `Info.plist` 파일에 발급받은 식별자를 추가해야 합니다.
`publisher` 키와 `media` 키를 각각 아래 항목에 입력하세요.

* **IADPublisherIdentifier**: Publisher Key
* **IADApplicationIdentifier**: Media Key

**XML 예시:**

```xml
<key>IADPublisherIdentifier</key>
<string>i8-adc-pub-126412831823-45789723847</string>

<key>IADApplicationIdentifier</key>
<string>i8-adc-app-1239070457-92812739813</string>
```

다음 단계는 adsynapse iOS SDK 사용법을 확인해주세요.

:::tip 문의하기
본 가이드 관련해서 문의 사항이 있으실 경우 [dev@infinit-c.com](mailto:dev@infinit-c.com)로 문의 바랍니다.
:::
