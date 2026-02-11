---
sidebar_position: 1
title: 네이티브 광고
---

## 광고 로드

```dart
void loadNative() async {
  NativeAd(
    slotCode: 'slot-code-xxxxxx',
    request: const AdRequest(),
    nativeTemplate: NativeTemplate(
      templateType: TemplateType.medium,
      cornerRadius: 8,
      mainBackgroundColor: Colors.white,
      primaryTextStyle: const NativeTextStyle(
        textColor: Colors.black,
        backgroundColor: Colors.white,
        style: NativeTextFontStyle.monospace,
        size: 16,
      ),
      secondaryTextStyle: const NativeTextStyle(
        textColor: Colors.black,
        backgroundColor: Colors.white,
        style: NativeTextFontStyle.monospace,
        size: 16,
      ),
      tertiaryTextStyle: const NativeTextStyle(
        textColor: Colors.black,
        backgroundColor: Colors.white,
        style: NativeTextFontStyle.monospace,
        size: 16,
      ),
      callToActionTextStyle: const NativeTextStyle(
        textColor: Colors.black,
        backgroundColor: Colors.white,
        style: NativeTextFontStyle.monospace,
        size: 16,
      ),
      callToActionBackgroundColor: Colors.blue,
    ),
    listener: NativeAdListener(
      onLoaded: (ad) {
        setState(() => _nativeAd = ad);
      },
      onFailed: (ad, errorCode) {
        if (errorCode == 'NO_FILL') {
          setState(() => _nativeAd = ad); // NO_FILL placeholder 표시
          return;
        }
        ad.dispose();
      },
      onOpened: (ad) {},
      onClosed: (ad) {},
      onImpression: (ad) {},
      onClicked: (ad) {},
      onWillDismissScreen: (ad) {},
    ),
  ).load();
}
```

## 광고 표시 (AdWidget)

```dart
if (_nativeAd != null)
  Align(
    alignment: Alignment.bottomCenter,
    child: SafeArea(
      child: SizedBox(
        width: _nativeAd!.size.width.toDouble(),
        height: _nativeAd!.size.height.toDouble(),
        child: AdWidget(ad: _nativeAd!),
      ),
    ),
  )
```

## 광고 해제

```dart
await _nativeAd?.dispose();
setState(() => _nativeAd = null);
```
