---
sidebar_position: 1
title: Android 시작하기
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## 사전 확인 사항

adsynapse Android SDK는 아래 사항이 충족해야됩니다.

- **연동 키 발급:** adsynapse 콘솔 또는 관리자에게 발급받은 키가 필요합니다.
- **최소 버전:** `minSdkVersion`은 **19** 혹은 이상이어야 합니다.
- **컴파일 버전:** `compileSdkVersion`은 **33** 혹은 이상이어야 합니다.

---

## SDK 설치 (Installation)

adsynapse Android SDK는 **Nexus Repository**를 통해 제공됩니다.

### 저장소 추가 (Project Level)

프로젝트 레벨의 `build.gradle` 파일에 아래와 같이 추가합니다.

```kotlin notebook
repositories {
   ...
   maven {  
      url = uri("https://mvn.infinit-c.com/repository/release")  
   }
   ...
}
```

### 의존성 추가 (App Level)

앱 모듈의 `build.gradle` 파일에 라이브러리를 추가합니다. version에는 연동키 발급 시 안내 받은 버전으로 넣습니다.

```kotlin notebook
dependencies {
   ...
   implementation "com.infinitc.adsynapse:adsynapse-sdk:${version}"
   ...
}
```

---
다음 단계는 adsynapse Android SDK 사용법을 확인해주세요.

:::tip 문의하기
본 가이드 관련해서 문의 사항이 있으실 경우 [dev@infinit-c.com](mailto:dev@infinit-c.com)로 문의 바랍니다.
:::
