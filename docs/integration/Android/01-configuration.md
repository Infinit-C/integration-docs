---
sidebar_position: 2
title: SDK 설정하기
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## `appCode`, &nbsp;`pubCode` 설정
`AndroidManifest.xml` 파일에 `appCode`, `pubCode`를 `<meta-data>` 태그 이용하여 아래와 같이 추가합니다.

- `appCode`는 `com.infinit-c.adsynapse.app_key`로 입력
- `pubCode`는 `com.infinit-c.adsynapse.pub_code`로 입력

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

## 권한 추가
adsynapse Android SDK에서는 아래와 같은 권한이 필요합니다.

- `android.permission.INTERNET`: 네트워크 통신을 위해 사용
- `android.permission.ACCESS_NETWORK_STATE`: 인터넷 연결 상태를 확인을 위해 사용 
- `com.google.android.gms.permission.AD_ID`: 광고 ID를 얻기 위해 사용

```xml
<manifest>
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
    <uses-permission android:name="com.google.android.gms.permission.AD_ID"/>
</manifest>

```
