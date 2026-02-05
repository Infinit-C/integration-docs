---
sidebar_position: 1
title: Flutter 플러그인 시작하기
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## 사전 확인 사항

adsynapse Flutter SDK는 아래 사항이 충족해야됩니다.

- Flutter 3.25.0 이상
- **연동 키 발급:** adsynapse 콘솔 또는 관리자에게 발급받은 키가 필요합니다.
- Android: **최신 버전**의 Android 스튜디오
- iOS: **Xcode 14.1** 버전 이상이 필요합니다.

---

## SDK 설치 (Installation)

- Flutter 프로젝트에 [Adsynapse Flutter Plugin](https://mvn.infinit-c.com/repository/flutter/)을 포함합니다.

## 플랫폼별 설정

<Tabs groupId="install-method">
<TabItem value="android" label="Android" default>
    ```xml
    <manifest>
        <application>
            <meta-data
                    android:name="com.infinit-c.adsynapse.app_key"
                    android:value="adsynapse-ac-xxxxxxxxxxxx-xxxxxxxxxxx"/>
            <meta-data
                    android:name="com.infinit-c.adsynapse.pub_code"
                    android:value="adsynapse-pc-xxxxxxxxxxxx-xxxxxxxxxxx"/>
        </application>
    </manifest>
    ```
</TabItem>
<TabItem value="ios" label="iOS">
    **Info.plist** 변경
    
    앱의 ios/Runner/Info.plist 파일에 아래와 같이 adsynapse 연동 키를 추가합니다.
    ```xml
    <key>IADPubIdentifier</key>
    <string>adsynapse-pc-xxxxxxxxxxxx-xxxxxxxxxxx</string>
    
    <key>IADApplicationIdentifier</key>
    <string>adsynapse-ac-xxxxxxxxxxxx-xxxxxxxxxxx</string>
    ```
</TabItem>
</Tabs>

## 플러그인 초기화
광고를 로드하기 전에 앱에서 `SynapseSdk.instance.initialize()`를 호출하여 플러그인을 초기화해야합니다.
```dart
SynapseSdk.instance.initialize()
```
