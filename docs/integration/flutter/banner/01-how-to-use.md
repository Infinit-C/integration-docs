---
sidebar_position: 1
title: 배너 광고
---

### 광고 로드

```dart
void _load() async {
  final size = await AdSize.getDefaultAdSize();
  
  BannerAd(
    // slotCode에 발급 받은 코드를 입력해야합니다.
    slotCode: "slot-code-xxxxxx",
    request: AdRequest(),
    size: size,
    listener: AdListener(
      onLoaded: (ad) {
        setState(() {
          _bannerAd = ad as BannerAd;
        });
      },
      onFailed: (ad, errorCode) {
        debugPrint("Failed to load banner ad: $errorCode");
        ad.dispose();
      }
    ) 
  ).load();
}
```

### 이벤트 조작

```dart
onOpened: (Ad ad) {
},
onClosed: (Ad ad) {
},
onImpression: (Ad ad) {
},
onClicked: (Ad ad) {
},
onWillDismissScreen: (Ad ad) {
},

```

### 배너 광고 표시

`BannerAd`를 위젯으로 표시하려면 `load()`를 호출한 후 지원되는 광고를 사용하여 AdWidget을 인스턴스화해야 합니다.
`load()`를 호출하기 전에 위젯을 만들 수도 있지만 위젯 트리에 위젯을 추가하기 전에 `load()`를 호출해야 합니다.

`AdWidget`은 Flutter의 위젯 클래스에서 상속되며 다른 위젯처럼 사용할 수 있습니다. iOS에서는 지정된 너비와 높이를 바탕으로 컨테이너에 위젯을 배치해야 합니다. 그러지 않으면 광고가 게재되지 않을 수
있습니다. `BannerAd`는 광고와 일치하는 크기의 컨테이너에 배치할 수 있습니다.

```dart
if (_bannerAd != null) {
  Align(
    alignment: Alignment.bottomCenter,
    child: SafeArea(
      child: SizedBox(
        width: _bannerAd!.size.width.toDouble(),
        height: _bannerAd!.size.height.toDouble(),
        child: AdWidget(ad: _bannerAd!),
      ),
    )
  )
}
```
