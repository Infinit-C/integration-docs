---
title: 사용자·권한 관리
sidebar_position: 8
---

# 사용자·권한 관리

사이드바 **Security** 섹션은 조직 관리자를 위한 메뉴입니다. 누가 조직에
들어올 수 있는지(Users), 어떤 권한을 갖는지(User Groups·Policies),
그리고 외부 시스템이 API로 접근할 때 쓰는 열쇠(API Keys)를 관리합니다.

## Users — 사용자

조직 구성원 목록입니다. [Invite user]로 이메일 초대를 보내거나 [Add user]로
직접 계정을 추가하고, 상태(Active 여부)·마지막 로그인·소속 그룹을 확인합니다.

![Users](/img/claire/security-users.png)

## User Groups · Policies — 그룹과 권한 정책

- **User Groups** — 사용자를 팀·역할 단위로 묶습니다. 권한은 개인이 아니라
  그룹에 부여하는 것이 관리하기 쉽습니다.
- **Policies** — 접근 범위(Scope)를 정의하는 권한 정책입니다. 정책을
  사용자 그룹이나 API 키에 연결해 접근을 제한합니다.

## API Keys — 기계 연동 키

외부 시스템이 Claire API를 호출할 때 쓰는 조직 API 키를 발급합니다.

![API Keys](/img/claire/api-keys.png)

- [Generate API key]로 발급하며, 조직당 **최대 5개**까지 보유할 수 있습니다.
- 키마다 **정책(Policies)을 연결해 권한 범위를 제한**할 수 있습니다 —
  필요한 최소 권한만 부여하세요.
- 만료(Expires)·마지막 사용(Last used)이 표시되니 쓰지 않는 키는 정리하세요.

:::warning
API 키는 발급 시점에만 전체 값이 표시됩니다. 안전한 곳에 보관하고,
코드 저장소나 문서에 절대 남기지 마세요. 유출이 의심되면 즉시 폐기 후 재발급하세요.
:::
