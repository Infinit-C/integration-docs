---
sidebar_position: 3
title: SDK 사용
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## adsynapse Android SDK 초기화

광고를 로드하기 전에 `SynapseSdk.initialze`를 호출해야 합니다.

이 작업은 앱 실행 시 한 번만 처리하면 됩니다.

<Tabs groupId="install-method">
    <TabItem value="java" label="Java" default>
        ```java
        SynapseSdk.initialize(this);
        ```
    </TabItem>
    <TabItem value="kotlin" label="Kotlin">
        ```kotlin
        SynapseSdk.initialize(this)
        ```
    </TabItem>
</Tabs>

## 광고 뷰 정의
배너 광고의 컨테이너 역할을 하는 뷰를 XML 레이아웃에 추가합니다.

```xml
<FrameLayout
        android:id="@+id/ad_view_container"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_centerInParent="true"
        android:layout_alignParentBottom="true"/>
```

## 광고 크기 설정

<Tabs groupId="install-method">
    <TabItem value="java" label="Java" default>
        ```java
        adView.setAdSize(AdSize.getDefaultAdSize(this));
        ```
    </TabItem>
    <TabItem value="kotlin" label="Kotlin">
        ```kotlin
        adView.setAdSize(AdSize.getDefaultAdSize(this))
        ```
    </TabItem>
</Tabs>

## 레이아웃에 AdView 추가
광고 크기를 사용하여 앱의 레이아웃에 추가할 `AdView`를 만듭니다.
```kotlin
val adView = AdView(this)
adView.slotCode = "adsynapse-slot_code-xxxxxx"
adView.setAdSize(AdSize.getDefaultAdSize(this))
this.adView = adView

binding.adViewContainer.removeAllViews()
binding.adViewContainer.addView(adView)
```

## AdView에 광고 호출
```kotlin
adView.load()
```

## 광고뷰에 대한 이벤트 리스너
<Tabs groupId="install-method">
<TabItem value="java" label="Java" default>
    ```java
    adView.setAdListener(new AdViewListener() {
        @Override
        public void onClicked() {}
    
        @Override
        public void onClosed() {}
    
        @Override
        public void onFailed(Integer code) {}
    
        @Override
        public void onImpression() {}
    
        @Override
        public void onLoaded() {}
    
        @Override
        public void onOpened() {}
    });
    ```
</TabItem>
<TabItem value="kotlin" label="Kotlin">
    ```kotlin
    adView.adListener = object : AdViewListener() {
        override fun onClicked() {}
    
        override fun onClosed() {}
    
        override fun onFailed(code: Int) {}
    
        override fun onImpression() {}
    
        override fun onLoaded() {}
    
        override fun onOpened() {}
    }
    ```
</TabItem>
</Tabs>

