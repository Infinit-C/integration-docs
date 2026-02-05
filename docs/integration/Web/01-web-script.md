---
sidebar_position: 1
title: Banner 스크립트
---

# 매체 연동 가이드 - Banner 스크립트

## 준비 사항 
본 가이드는 웹(Web) 환경에서 스크립트 태그를 사용하여 배너 광고를 연동하는 방법을 설명합니다.<br/>
연동을 위해서는 adsynapse 콘솔에서 발급 혹은 관리자에게 발급 받은 키가 필요합니다. 

---

## 스크립트 설치 (Integration)
발급받은 광고 스크립트를 HTML의 `<body>` 태그 내부, 광고를 노출하고 싶은 위치에 삽입합니다.

```html
<script src="https://{domain}/pub.js"></script>
```
삽입된 스크립트 후에 init 함수 호출 후 banner(..)를 호출하면 광고 지면이 초기화되면서 광고 노출이 시작됩니다.

### 함수
| 함수명 | 설명 | 파라미터 |
|-|-|-|
| `init` | 스크립트를 초기화하는 함수 | |
| `banner` | 광고를 호출하는 함수 | Banner 형태 혹은 Banner의 배열 |

### 함수 파라미터
#### init
| Parameter | 설명 | 예시 | 필수 |
|-|-|-|-|
| `pub_code` | 퍼블리셔 코드 |  | ○ |
| `media_code` | 매체 코드 | | ○ |

#### Banner
| Parameter | 설명 | 예시 | 필수 |
|-|-|-|:-:|
| `canvasId` | 광고를 구현할 위치의 컨테이너 | div#id | ○ |
| `width` | 광고 가로 사이즈 | 240px, 100% | ○ |
| `height` | 광고 세로 사이즈 | 50px, auto | X |
| `type` | 광고 유형 |  | X |
| `affiliationId` | 하위 매체 구분자 | subpub-1234 | X |

---

### 예시
```html
<html>
  <head></head>
  <body>
    (... contents ...)

    <script src="https://{domain}/pub.js?pc={pub_code}&ac={area_code}"></script>
    <script>
      $(document).ready(function() {
        ID8.init({
          pub_code: "",
          media_code: ""
        });

        ID8.banner([
          {canvasId: 'div#id', width: '240px', height: '50px', affiliationId: '하위 매체 구분자'},
          {canvasId: 'div#id2', width: '240px', height: '50px', affiliationId: '하위 매체 구분자'}
          ...
        ]);
        // or
        ID8.banner({canvasId: 'div#id', width: '240px', height: '50px', affiliationId: '하위 매체 구분자'});
      });
    </script>
  </body>
</html>
```

---
:::tip 문의하기
본 가이드 관련해서 문의 사항이 있으실 경우 [dev@infinit-c.com](mailto:dev@infinit-c.com)로 문의 바랍니다.
:::