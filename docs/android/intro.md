---
sidebar_position: 1
title: Android SDK 연동
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# 매체 연동 가이드 - Android SDK

## 1. 시작하기 (Getting Started)

### 사전 준비 사항

1.  **연동 키 발급:** AdCore 콘솔 또는 관리자에게 발급받은 키가 필요합니다.
2.  **최소 버전:** `minSdkVersion`은 **19** 혹은 이상이어야 합니다.
3.  **컴파일 버전:** `compileSdkVersion`은 **33** 혹은 이상이어야 합니다.

---

## 2. SDK 설치 (Installation)

AdCore Android SDK는 **GitHub Packages**를 통해 제공됩니다.

### 1단계: 저장소 추가 (Project Level)

1. 프로젝트 레벨의 `build.gradle` 파일에 아래와 같이 추가합니다.

```groovy
repositories {
   ...
   maven {  
      url = uri("https://maven.pkg.github.com/id8-io/adcore-aos-sdk")  
   }
   ...
}
```

### 2단계: 의존성 추가 (App Level)

2. 앱 모듈의 `build.gradle` 파일에 라이브러리를 추가합니다.

```groovy
dependencies {
   ...
   implementation "io.id8:adcore-aos-sdk:x.y.z"
   ...
}
```

3. `AndroidManifest.xml` 파일에 `publisher`, `media` 키를 `<meta-data>` 태그 이용하여 아래와 같이 추가합니다.

`publisher`키는 `io.id8.android.adcore.PUBLISHER_ID`로 입력합니다.
`media`키는 `io.id8.android.adcore.APP_ID`로 입력합니다.

```xml
<manifest>
    <application>
        <meta-data
                android:name="io.id8.android.adcore.PUBLISHER_ID"
                android:value="i8-adc-pub-126412831823-45789723847"/>
        <meta-data
                android:name="io.id8.android.adcore.APP_ID"
                android:value="i8-adc-app-1239070457-92812739813"/>
    </application>
</manifest>
```
---
다음 단계는 AdCore Android SDK 사용법을 확인해주세요.

:::tip 문의하기
본 가이드 관련해서 문의 사항이 있으실 경우 [dev@infinit-c.com](mailto:dev@infinit-c.com)로 문의 바랍니다.
:::