import React, {useEffect, useState} from 'react';
import {useLocation} from '@docusaurus/router';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

// Claire 가이드(/claire, /en/claire)는 접근 코드를 입력해야 보인다.
// 정적 사이트(GitHub Pages)라 서버 인증은 없다: 빌드 HTML에는 본문이 들어가지 않고(SSR에서 잠금 화면만 렌더),
// 코드 해시만 번들에 포함된다. 코드는 빌드 시 CLAIRE_GUIDE_CODE_HASH(SHA-256 hex)로 바꾼다.
const GATED = /^\/(en\/)?claire(\/|$)/;
const STORAGE_KEY = 'claire-guide-access';

async function sha256Hex(text: string): Promise<string> {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return Array.from(new Uint8Array(buf)).map((b) => b.toString(16).padStart(2, '0')).join('');
}

function Gate({hash, onUnlock}: {hash: string; onUnlock: () => void}) {
  const [code, setCode] = useState('');
  const [error, setError] = useState(false);
  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    const h = await sha256Hex(code.trim().toUpperCase());
    if (h === hash) {
      try { localStorage.setItem(STORAGE_KEY, h); } catch {}
      onUnlock();
    } else {
      setError(true);
    }
  };
  return (
    <main style={{minHeight: '70vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2rem'}}>
      <form onSubmit={submit} style={{width: '100%', maxWidth: 360, textAlign: 'center'}}>
        <h1 style={{fontSize: '1.4rem', marginBottom: '.5rem'}}>Claire 가이드</h1>
        <p style={{color: 'var(--ifm-color-emphasis-700)'}}>이 문서는 접근 코드가 있어야 볼 수 있습니다.</p>
        <label htmlFor="claire-access-code" style={{display: 'block', textAlign: 'left', fontWeight: 600, margin: '1rem 0 .25rem'}}>접근 코드</label>
        <input
          id="claire-access-code"
          type="password"
          autoComplete="off"
          autoFocus
          value={code}
          onChange={(e) => { setCode(e.target.value); setError(false); }}
          aria-invalid={error}
          style={{width: '100%', padding: '.6rem .75rem', fontSize: '1rem', border: `1px solid ${error ? 'var(--ifm-color-danger)' : 'var(--ifm-color-emphasis-300)'}`, borderRadius: 8}}
        />
        {error && <p role="alert" style={{color: 'var(--ifm-color-danger)', margin: '.5rem 0 0'}}>코드가 맞지 않습니다.</p>}
        <button type="submit" className="button button--primary button--block" style={{marginTop: '1rem'}} disabled={!code.trim()}>
          열기
        </button>
        <Link to="/" className="button button--secondary button--outline button--block" style={{marginTop: '.5rem'}}>
          돌아가기
        </Link>
      </form>
    </main>
  );
}

export default function Root({children}: {children: React.ReactNode}) {
  const {pathname} = useLocation();
  const {siteConfig} = useDocusaurusContext();
  const hash = String(siteConfig.customFields?.claireGuideCodeHash ?? '');
  const gated = GATED.test(pathname) && hash !== '';
  const [unlocked, setUnlocked] = useState(false);
  useEffect(() => {
    try { setUnlocked(localStorage.getItem(STORAGE_KEY) === hash); } catch { setUnlocked(false); }
  }, [hash]);
  if (gated && !unlocked) {
    return <Gate hash={hash} onUnlock={() => setUnlocked(true)} />;
  }
  return <>{children}</>;
}
