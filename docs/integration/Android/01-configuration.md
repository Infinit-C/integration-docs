---
sidebar_position: 2
title: SDK 설정하기
---

## Manifest 메타데이터

`AndroidManifest.xml`의 `<application>`에 아래 메타데이터를 추가합니다.

- `com.infinitc.adsynapse.app_key` (필수)
- `com.infinitc.adsynapse.debug_mode` (선택, 원격 디버그 로그 활성화)

```xml
<manifest>
  <application>
    <meta-data
      android:name="com.infinitc.adsynapse.app_key"
      android:value="adsynapse-ac-xxxxxxxxxxxx-xxxxxxxxxxx" />

    <meta-data
      android:name="com.infinitc.adsynapse.debug_mode"
      android:value="false" />
  </application>
</manifest>
```

## 권한

```xml
<manifest>
  <uses-permission android:name="android.permission.INTERNET"/>
  <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
  <uses-permission android:name="com.google.android.gms.permission.AD_ID"/>
</manifest>
```
