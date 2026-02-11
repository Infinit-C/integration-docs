---
sidebar_position: 1
title: 배너 광고
---

## 광고 로드

```dart
void loadBanner() async {
  final size = await AdSize.getDefaultAdSize();

  BannerAd(
    slotCode: 'slot-code-xxxxxx',
    request: const AdRequest(),
    size: size,
    listener: AdListener(
      onLoaded: (ad) {
        setState(() => _bannerAd = ad);
      },
      onFailed: (ad, errorCode) {
        if (errorCode == 'NO_FILL') {
          setState(() => _bannerAd = ad); // NO_FILL placeholder 표시
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
if (_bannerAd != null)
  Align(
    alignment: Alignment.bottomCenter,
    child: SafeArea(
      child: SizedBox(
        width: _bannerAd!.size.width.toDouble(),
        height: _bannerAd!.size.height.toDouble(),
        child: AdWidget(ad: _bannerAd!),
      ),
    ),
  )
```

## 광고 해제

```dart
await _bannerAd?.dispose();
setState(() => _bannerAd = null);
```
