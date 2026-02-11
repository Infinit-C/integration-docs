---
sidebar_position: 3
title: SDK 사용
---

## 초기화 / 해제

```swift
AdSynapse.initialize(debug: false)

let initialized = AdSynapse.instance.isInitilaized

AdSynapse.deinitialize()
```

## 배너 광고 (BannerView)

```swift
let bannerView = BannerView()
bannerView.slotCode = "slot-code-xxxxxx"
bannerView.adSize = AdSize.getDefaultAdSize()

bannerView.load { result in
    switch result {
    case .success:
        break
    case .failure(let error):
        print("banner load failed: \(error)")
    }
}
```

`BannerView`를 화면 하단 컨테이너에 붙여 사용하세요.

## 직접 호출 방식

```swift
let request = AdRequest()
request.slotCode = "slot-code-xxxxxx"
request.adType = .banner
request.adSize = AdSize.getDefaultAdSize()

AdSynapse.instance.loadAd(request: request) { result in
    switch result {
    case .success(let data):
        // JSON/HTML 응답 처리
        print(String(data: data, encoding: .utf8) ?? "")
    case .failure(let error):
        print(error)
    }
}
```

## 로그 정책

- 민감 로그는 `isRemoteDebug` 조건에서만 출력됩니다.
- `ISSApplicationKey`가 없으면 원격 디버그 로그는 비활성 상태입니다.
