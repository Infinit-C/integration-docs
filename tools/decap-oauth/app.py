#!/usr/bin/env python3
"""Decap CMS용 GitHub OAuth 중계 서버.

docs.infinit-c.com/admin (Decap CMS)의 GitHub 로그인을 처리한다.
GitHub Pages는 서버가 없으므로 이 중계가 code→access_token 교환을 대신한다.
studio VM에서 systemd(decap-oauth, :8110)로 돌고 nginx가
studio.infinit-c.com/decap-oauth/ 를 여기로 프록시한다.

환경변수(/etc/decap-oauth.env): GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET
"""
import json
import os
import secrets
import urllib.parse

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse

CLIENT_ID = os.environ["GITHUB_CLIENT_ID"]
CLIENT_SECRET = os.environ["GITHUB_CLIENT_SECRET"]
REDIRECT_URI = os.environ.get(
    "REDIRECT_URI", "https://studio.infinit-c.com/decap-oauth/callback")
# postMessage를 받을 CMS origin (보안: 다른 사이트로 토큰 전달 금지)
ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN", "https://docs.infinit-c.com")

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
_states: set[str] = set()


@app.get("/auth")
def auth():
    state = secrets.token_urlsafe(24)
    _states.add(state)
    if len(_states) > 500:  # 미완료 state 누적 방지
        _states.clear()
        _states.add(state)
    q = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "repo,user",
        "state": state,
    })
    return RedirectResponse(f"https://github.com/login/oauth/authorize?{q}")


@app.get("/callback")
async def callback(request: Request, code: str = "", state: str = ""):
    if not code or state not in _states:
        return HTMLResponse("인증 요청이 유효하지 않습니다. /admin에서 다시 시도하세요.", status_code=400)
    _states.discard(state)
    async with httpx.AsyncClient(timeout=15) as c:
        r = await c.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
                  "code": code, "redirect_uri": REDIRECT_URI},
        )
    token = r.json().get("access_token")
    if not token:
        return HTMLResponse("GitHub 토큰 교환에 실패했습니다.", status_code=502)
    payload = json.dumps({"token": token, "provider": "github"})
    # Decap 표준 postMessage 핸드셰이크: opener가 'authorizing:github'를 받으면
    # origin을 확인한 뒤 성공 메시지를 보낸다.
    html = f"""<!DOCTYPE html><html><body><script>
(function() {{
  var allowed = {json.dumps(ALLOWED_ORIGIN)};
  function receive(e) {{
    if (e.origin !== allowed) return;
    window.opener.postMessage(
      'authorization:github:success:{payload}', e.origin);
    window.removeEventListener('message', receive, false);
  }}
  window.addEventListener('message', receive, false);
  window.opener.postMessage('authorizing:github', allowed);
}})()
</script>로그인 처리 중… 이 창은 자동으로 닫힙니다.</body></html>"""
    return HTMLResponse(html)


@app.get("/health")
def health():
    return {"ok": True}
