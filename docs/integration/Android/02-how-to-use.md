---
sidebar_position: 3
title: SDK 사용
---

## 초기화

광고 호출 전에 앱 시작 시 1회 초기화합니다.

```kotlin
AdSynapseSdk.initialize(applicationContext)
```

초기화 상태 확인 및 해제:

```kotlin
val initialized = AdSynapseSdk.instance.isInitialized
AdSynapseSdk.deinitialize()
```

## 배너 광고 (AdView)

레이아웃 컨테이너:

```xml
<FrameLayout
    android:id="@+id/adViewContainer"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:layout_gravity="bottom" />
```

배너 생성 및 로드:

```kotlin
val adView = AdView(this).apply {
    slotCode = "slot-code-xxxxxx"
    adSize = AdSize.getDefaultAdSize(this@MainActivity)
    adListener = object : AdViewListener {
        override fun onClicked() {}
        override fun onClosed() {}
        override fun onFailed(code: Int) {}
        override fun onImpression() {}
        override fun onLoaded() {}
        override fun onOpened() {}
    }
}

findViewById<FrameLayout>(R.id.adViewContainer).apply {
    removeAllViews()
    addView(adView)
}

adView.load(AdRequest.Builder().build())
```

## 직접 호출 방식 (고급)

`AdRequest`를 직접 구성해 SDK에 전달할 수도 있습니다.

```kotlin
val request = AdRequest.Builder().build().apply {
    setSlotCode("slot-code-xxxxxx")
    setAdSize(AdSize.getDefaultAdSize(this@MainActivity))
    setAdType(AdType.BANNER) // 또는 AdType.NATIVE
}

val bannerJson = AdSynapseSdk.instance.loadBanner(request)
// val nativeJson = AdSynapseSdk.instance.loadNative(request)
```
