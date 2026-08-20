# decap-oauth — docs CMS 로그인 중계

`docs.infinit-c.com/admin`(Decap CMS)의 GitHub 로그인을 처리하는 초소형 서버.
studio VM(:8110, systemd `decap-oauth`)에서 돌고, nginx가
`studio.infinit-c.com/decap-oauth/` → `127.0.0.1:8110/` 로 프록시한다.

## 선행: GitHub OAuth App (조직 관리자)

GitHub → Organization **Infinit-C** → Settings → Developer settings → OAuth Apps → New OAuth App

| 항목 | 값 |
|---|---|
| Application name | INFINIT-C Docs CMS |
| Homepage URL | `https://docs.infinit-c.com` |
| Authorization callback URL | `https://studio.infinit-c.com/decap-oauth/callback` |

생성 후 **Client ID**와 **Client Secret**(Generate a new client secret)을 발급.

## VM 설치

```bash
sudo mkdir -p /opt/decap-oauth && cd /opt/decap-oauth
# app.py 업로드 후:
python3 -m venv .venv && .venv/bin/pip install fastapi uvicorn httpx

# 시크릿 (root 600)
sudo tee /etc/decap-oauth.env >/dev/null <<'EOF'
GITHUB_CLIENT_ID=<발급받은 ID>
GITHUB_CLIENT_SECRET=<발급받은 Secret>
EOF
sudo chmod 600 /etc/decap-oauth.env

# systemd
sudo cp decap-oauth.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now decap-oauth
```

## nginx (studio.infinit-c.com server 블록에 추가)

```nginx
location /decap-oauth/ {
    proxy_pass http://127.0.0.1:8110/;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-Proto https;
}
```

```bash
sudo nginx -t && sudo systemctl reload nginx
curl -s https://studio.infinit-c.com/decap-oauth/health   # {"ok":true}
```

## 운영팀 온보딩

1. GitHub 계정 생성 → `Infinit-C/integration-docs` 리포에 **Write** 권한 초대
2. `docs.infinit-c.com/admin` 접속 → [GitHub으로 로그인] → 문서 수정 → 저장(=커밋) → 2~3분 후 자동 배포
