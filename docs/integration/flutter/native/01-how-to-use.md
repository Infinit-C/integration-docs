---
sidebar_position: 1
title: 네이티브 광고
---

### 광고 로드

```dart
void _load() async {
  NativeAd(
    // slotCode에 발급 받은 코드를 입력해야합니다.
    slotCode: "slot-code-xxxxxx",
    listener: NativeAdListener(
      onLoaded: (ad) {
        setState(() {
          _nativeAdIsLoaded = true;
        });
      },
      onFailed: (ad, errorCode) {
        debugPrint("Failed to load banner ad: $errorCode");
        ad.dispose();
      },
      onWillDismissScreen: (ad) {
      }
    ),
    nativeTemplate: NativeTemplate(
      templateType: TemplateType.medium, // TemplateType.medium or TemplateType.small
      cornerRadius: 8.0,
      mainBackgroundColor: Colors.white, 
      primaryTextStyle: NativeTextStyle(
        textColor: Colors.black,
        backgroundColor: Colors.white,
        style: NativeTextFontStyle.monospace,
        size: 16.0,
      ),
      secondaryTextStyle: NativeTextStyle(
        textColor: Colors.black,
        backgroundColor: Colors.white,
        style: NativeTextFontStyle.monospace,
        size: 16.0,
      ),
      tertiaryTextStyle: NativeTextStyle(
        textColor: Colors.black,
        backgroundColor: Colors.white,
        style: NativeTextFontStyle.monospace,
        size: 16.0,
      ),
      callToActionTextStyle: NativeTextStyle(
        textColor: Colors.black,
        backgroundColor: Colors.white,
        style: NativeTextFontStyle.monospace,
        size: 16.0,
      ),
      callToActionBackgroundColor: Colors.blue,
    ),
    request: AdRequest()
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

### 네이티브 광고 표시

`NativeAd`를 위젯으로 표시하려면 `load()`를 호출한 후 지원되는 광고를 사용하여 AdWidget을 인스턴스화해야 합니다.
`load()`를 호출하기 전에 위젯을 만들 수도 있지만 위젯 트리에 위젯을 추가하기 전에 `load()`를 호출해야 합니다.

`AdWidget`은 Flutter의 위젯 클래스에서 상속되며 다른 위젯처럼 사용할 수 있습니다. iOS에서는 지정된 너비와 높이를 바탕으로 컨테이너에 위젯을 배치해야 합니다. 그러지 않으면 광고가 게재되지 않을 수
있습니다.

```dart
if (_nativeAd != null) {
  Align(
    alignment: Alignment.bottomCenter,
    child: SafeArea(
      child: SizedBox(
        width: _nativeAd!.size.width.toDouble(),
        height: _nativeAd!.size.height.toDouble(),
        child: AdWidget(ad: _nativeAd!),
      ),
    )
  )
}
```
