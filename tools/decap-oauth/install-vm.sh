#!/usr/bin/env bash
# decap-oauth를 studio VM에 설치한다. 로컬 맥에서 실행:
#   cd tools/decap-oauth && bash install-vm.sh
# Client ID/Secret은 프롬프트로 입력받아 VM의 /etc/decap-oauth.env에만 저장된다.
set -euo pipefail

VM_IP="${VM_IP:-34.64.110.133}"
VM_HOST="${VM_HOST:-yoonjaehyon@$VM_IP}"
SSH_KEY="${SSH_KEY:-$HOME/.ssh/google_compute_engine}"
SSH=(ssh -i "$SSH_KEY" -t "$VM_HOST")
HERE="$(cd "$(dirname "$0")" && pwd)"

read -rp "GitHub Client ID: " CLIENT_ID
read -rsp "GitHub Client Secret (입력 안 보임): " CLIENT_SECRET; echo
[[ -n "$CLIENT_ID" && -n "$CLIENT_SECRET" ]] || { echo "❌ 값이 비어 있습니다"; exit 1; }

echo "→ 파일 업로드"
scp -i "$SSH_KEY" "$HERE/app.py" "$HERE/decap-oauth.service" "$VM_HOST:/tmp/"

echo "→ VM 설치 (sudo 비밀번호를 물을 수 있습니다)"
"${SSH[@]}" "CLIENT_ID='$CLIENT_ID' CLIENT_SECRET='$CLIENT_SECRET' bash -s" <<'REMOTE'
set -euo pipefail

# 앱 + venv
sudo mkdir -p /opt/decap-oauth
sudo cp /tmp/app.py /opt/decap-oauth/
if [[ ! -x /opt/decap-oauth/.venv/bin/uvicorn ]]; then
  sudo python3 -m venv /opt/decap-oauth/.venv
  sudo /opt/decap-oauth/.venv/bin/pip install -q fastapi uvicorn httpx
fi
sudo chown -R www-data:www-data /opt/decap-oauth

# 시크릿 (root 600)
sudo install -m 600 /dev/null /etc/decap-oauth.env
printf 'GITHUB_CLIENT_ID=%s\nGITHUB_CLIENT_SECRET=%s\n' "$CLIENT_ID" "$CLIENT_SECRET" \
  | sudo tee /etc/decap-oauth.env >/dev/null

# systemd
sudo cp /tmp/decap-oauth.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now decap-oauth
sudo systemctl restart decap-oauth
rm -f /tmp/app.py /tmp/decap-oauth.service

# nginx: studio 서버 블록에 location 삽입 (이미 있으면 건너뜀)
CONF=$(sudo grep -l 'studio\.infinit-c\.com' /etc/nginx/sites-enabled/* | head -1)
[[ -n "$CONF" ]] || { echo "❌ studio nginx 설정을 못 찾음"; exit 1; }
if ! sudo grep -q 'decap-oauth' "$CONF"; then
  sudo cp "$CONF" "$CONF.bak-decap"
  sudo awk '
    /server_name[ \t].*studio\.infinit-c\.com/ && !done {
      print
      print "    location /decap-oauth/ {"
      print "        proxy_pass http://127.0.0.1:8110/;"
      print "        proxy_set_header Host $host;"
      print "        proxy_set_header X-Forwarded-Proto https;"
      print "    }"
      done=1; next
    }
    { print }
  ' "$CONF" | sudo tee "$CONF.new" >/dev/null
  sudo mv "$CONF.new" "$CONF"
  if sudo nginx -t; then
    sudo systemctl reload nginx
  else
    echo "❌ nginx 설정 오류 — 원복합니다"
    sudo mv "$CONF.bak-decap" "$CONF"
    exit 1
  fi
fi

sleep 1
echo "— 상태 확인 —"
systemctl is-active decap-oauth
curl -s http://127.0.0.1:8110/health
echo
REMOTE

echo "→ 외부 확인"
curl -s https://studio.infinit-c.com/decap-oauth/health && echo " ✅ 완료"
