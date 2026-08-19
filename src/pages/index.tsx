import React from 'react';
import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './index.module.css';

function ClaireIcon() {
  return (
    <svg viewBox="0 0 106 106" role="img" aria-label="Claire">
      <rect x="0" y="0" width="106" height="106" rx="26" fill="#0D1B2A" />
      <rect x="22.2" y="44" width="6.5" height="34" rx="3.2" fill="#29B6D8" />
      <rect x="33.2" y="32" width="6.5" height="46" rx="3.2" fill="#29B6D8" />
      <rect x="44.2" y="38" width="6.5" height="40" rx="3.2" fill="#29B6D8" />
      <rect x="55.2" y="22" width="6.5" height="56" rx="3.2" fill="#E6187F" />
      <rect x="66.2" y="32" width="6.5" height="46" rx="3.2" fill="#29B6D8" />
      <rect x="77.2" y="46" width="6.5" height="32" rx="3.2" fill="#29B6D8" />
    </svg>
  );
}

function AdsynapseIcon() {
  return (
    <svg viewBox="0 0 106 106" role="img" aria-label="adsynapse">
      <rect x="0" y="0" width="106" height="106" rx="26" fill="#0D1B2A" />
      <path
        d="M40 36 L23 53 L40 70"
        stroke="#29B6D8" strokeWidth="7" fill="none"
        strokeLinecap="round" strokeLinejoin="round"
      />
      <path
        d="M66 36 L83 53 L66 70"
        stroke="#29B6D8" strokeWidth="7" fill="none"
        strokeLinecap="round" strokeLinejoin="round"
      />
      <path
        d="M59 31 L47 75"
        stroke="#E6187F" strokeWidth="7" strokeLinecap="round"
      />
    </svg>
  );
}

type ProductItem = {
  title: string;
  tag: string;
  description: string;
  to: string;
  cta: string;
  Icon: () => React.ReactElement;
};

const products: ProductItem[] = [
  {
    title: 'Claire',
    tag: 'AI Marketing Assistant',
    description:
      '미디어믹스 설계부터 소재 제작, 성과 분석까지 — 캠페인 운영의 모든 단계를 대화형 대시보드에서 처리합니다.',
    to: '/claire/intro',
    cta: '사용 가이드',
    Icon: ClaireIcon,
  },
  {
    title: 'adsynapse',
    tag: 'SSP SDK · RTB API',
    description:
      'Flutter · Android · iOS · Web 플랫폼별 광고 SDK 연동 가이드와 OpenRTB 기반 RTB API 레퍼런스를 제공합니다.',
    to: '/adsynapse/integration/intro',
    cta: '연동 문서',
    Icon: AdsynapseIcon,
  },
];

function ProductCard({title, tag, description, to, cta, Icon}: ProductItem) {
  return (
    <Link className={styles.card} to={to}>
      <span className={styles.cardIcon}>
        <Icon />
      </span>
      <span className={styles.cardTag}>{tag}</span>
      <Heading as="h2" className={styles.cardTitle}>
        {title}
      </Heading>
      <p className={styles.cardDesc}>{description}</p>
      <span className={styles.cardCta}>
        {cta} <span aria-hidden="true">→</span>
      </span>
    </Link>
  );
}

export default function Home(): React.ReactElement {
  return (
    <Layout title="INFINIT-C Docs" description="INFINIT-C 제품 가이드 & 연동 문서">
      <header className={styles.hero}>
        <div className="container">
          <p className={styles.eyebrow}>INFINIT-C</p>
          <Heading as="h1" className={styles.heroTitle}>
            제품 가이드 &{' '}
            <span className={styles.gradientText}>개발 문서</span>
          </Heading>
          <p className={styles.heroSub}>
            Claire 사용 가이드부터 adsynapse SDK 연동까지, 필요한 문서를 한곳에서.
          </p>
        </div>
      </header>
      <main className={styles.main}>
        <div className={styles.cards}>
          {products.map((props) => (
            <ProductCard key={props.title} {...props} />
          ))}
        </div>
      </main>
    </Layout>
  );
}
