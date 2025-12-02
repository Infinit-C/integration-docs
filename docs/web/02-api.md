---
sidebar_position: 2
title: Banner API
---

# 매체 연동 가이드 - Banner API
본 가이드는 S2S 또는 클라이언트에서 직접 API를 호출하여 배너 광고를 요청하는 방법을 설명합니다.<br/>
연동을 위해선 AdCore 콘솔에서 발급 혹은 관리자에게 발급 받은 키가 필요합니다.

---

## 1. API 요청 (Request)

## 배너 광고 요청
HTTP GET 방식으로 아래 정의된 파마리터와 함께 호출합니다.

```http request
GET https://{domain}/ads.banner?version=&publisher=&media=
```

### 요청 파라미터

#### 기본 정보

| 필드          | 유형      | 필수 | 설명                      |
|-------------|---------|:--:|-------------------------|
| `version`   | integer | Y  | 1 ; 고정값                 |
| `publisher` | string  | Y  | 매체 코드                   |
| `media`     | string  | Y  | 미디어 코드                  |
| `section`   | string  | Y  | 지면 코드                   |
| `requestId` | string  | N  | UUID 혹은 nonce. 권장사항입니다. |
| `bWidth`    | string  | Y  | 광고가 노출된 영역 넓이           |
| `bHeight`   | string  | Y  | 광고가 노출될 영역 높이           |

#### 디바이스 정보

| 필드           | 유형      | 필수 | 설명                         |
|--------------|---------|:--:|----------------------------|
| `appName`    | string  | Y  | App 이름 (Web일 경우 브라우저 이름)   |
| `appCode`    | string  | Y  | App 코드명 (Web일 경우 브라우저 코드명) |
| `appVersion` | string  | Y  | App 버전 (Web일 경우 브라우저 버전)   |
| `os`         | integer | Y  | 1: Web, 2: iOS, 3: AOS     |
| `osVersion`  | string  | N  | OS 버전 (권장)                 |
| `lang`       | string  | N  | 언어 코드 (권장)                 |
| `ua`         | string  | N  | User Agent (권장)            |
| `sw`         | integer | N  | 화면 가로사이즈 (권장)              |
| `sh`         | integer | N  | 화면 세로사이즈 (권장)              |


### 요청 예시

#### Web

```shell
curl \
  -X GET \
  https://{domain}/ads.banner?version=1 \
  &publisher={publisher_code}&media={media_code}&section={section_code} \
  &requestId=263ad457-b56b-4664-bb29-3868a9189e5f \
  &bWidth=320px&bHeight=50px \
  &appName=Netscape&appCode=Mozilla&appVersion=5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F119.0.0.0%20Safari%2F537.36 \
  &os=1&osVersion=Mac%20OS%20X%2010_15_7 \
  &ua=Mozilla%2F5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F119.0.0.0%20Safari%2F537.36 \
  &lang=ko-KR&sw=1200&sh=700
```
---

## 2. API 응답 (Response)

아래 정의된 형태로 JSON 형식으로 응답합니다.

#### 광고 응답 정보

| 필드             | 유형      | 필수 | 설명                               |
|----------------|---------|:--:|----------------------------------|
| `version`      | string  | Y  | 1 ; 광고 버전                        |
| `errorCode`    | string  | Y  | [에러 코드](#error_code) 정의를 확인해주세요. |
| `rotateTime`   | string  | Y  | 광고 재요청 시간(초)                     |
| `requestId`    | string  | Y  | 요청 고유 코드. 요청 시 전달한 requestId     |
| `adType`       | string  | Y  | 광고 유형                            |
| `productType`  | string  | Y  | 광고 상품 구분                         |
| `productAttrs` | string  | Y  | 광고 상품 타입                         |
| `count`        | integer | Y  | 전달한 광고 갯수                        |
| `ads`          | object  | Y  | [광고](#ad). array 형태              |

#### 광고

<div id="ad"></div>

| 필드            | 유형     | 필수 | 설명                |
|---------------|--------|:--:|-------------------|
| `campCode`    | string | Y  | 캠페인 코드            |
| `adGroupCode` | string | Y  | 애드 그룹 코드          |
| `adCode`      | string | Y  | 애드 코드             |
| `imagePath`   | string | Y  | 이미지 소재 URL        |
| `imageName`   | string | Y  | 이미지 소재 파일명        |
| `clickOption` | string | Y  | 클릭 옵션             |
| `clickAction` | string | Y  | 클릭 액션 유형을 참고 해주세요 |
| `landingUrl`  | string | Y  | 광고주 랜딩 정보         |
| `bgColor`     | string | Y  | 배경화면 색상표          |
| `width`       | string | Y  | 광고 소재 이미지 넓이      |
| `height`      | string | Y  | 광고 소재 이미지 높이      |
| `endDt`       | string | Y  | 광고 송출 가능 시간       |
| `impAPI`      | string | Y  | 노출 트래킹 API        |
| `clickAPI`    | string | Y  | 클릭 API            |
| `trackingAPI` | string | Y  | 클릭 트래킹 API        |
| `html`        | string | Y  | HTML 광고 소재        |

#### 에러 코드

<div id="error_code"></div>

| 코드 | 설명             |
|----|----------------|
| 0  | 정상             |
| 1  | 광고 서버 에러       |
| 2  | 잘못된 광고 요청      |
| 3  | 잘못된 파라미터 정보 전달 |
| 4  | 광고 없음          |

> :warning: 에러의 경우 HTTP Status 코드는 성공(200)으로 응답됩니다.

### 응답 예시

```json
{
  "version": 1,
  "errorCode": 0,
  "rotateTime": "1000",
  "requestId": "263ad457-b56b-4664-bb29-3868a9189e5f",
  "adType": "banner",
  "productType": "ecpm",
  "productAttrs": "",
  "count": 1,
  "ads": [
    {
      "campCode": "1",
      "adGroupCode": "1",
      "adCode": "1",
      "imagePath": "https://id8.co.kr",
      "imageName": "",
      "clickOption": "",
      "clickAction": "",
      "landingUrl": "",
      "bgColor": "ffffff",
      "width": "320px",
      "height": "50px",
      "endDt": "1704121199000",
      "impAPI": "",
      "clickAPI": "",
      "trackingAPI": "",
      "html": ""
    }
  ]
}
```

----
:::tip 문의하기
본 가이드 관련해서 문의 사항이 있으실 경우 [dev@infinit-c.com](mailto:dev@infinit-c.com)로 문의 바랍니다.
:::