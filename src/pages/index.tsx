import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
      </div>
    </header>
  );
}

type ProductItem = {
  title: string;
  description: React.ReactNode;
  to: string;
  linkLabel: string;
};

const products: ProductItem[] = [
  {
    title: 'Claire',
    description: (
      <>
        AI 마케팅 어시스턴트. 미디어믹스 설계, 소재 성과 분석,
        광고 소재 제작을 대화형 대시보드에서 처리합니다.
      </>
    ),
    to: '/claire/intro',
    linkLabel: '사용 가이드 →',
  },
  {
    title: 'adsynapse SSP SDK',
    description: (
      <>
        개발자를 위한 광고 SDK 연동 문서. Flutter · Android · iOS · Web
        플랫폼별 연동 가이드와 RTB API 레퍼런스를 제공합니다.
      </>
    ),
    to: '/adsynapse/integration/intro',
    linkLabel: '연동 문서 →',
  },
];

function ProductCard({title, description, to, linkLabel}: ProductItem) {
  return (
    <div className="col col--5">
      <div className={clsx('card', styles.productCard)}>
        <div className="card__header">
          <Heading as="h2">{title}</Heading>
        </div>
        <div className="card__body">
          <p>{description}</p>
        </div>
        <div className="card__footer">
          <Link className="button button--primary button--block" to={to}>
            {linkLabel}
          </Link>
        </div>
      </div>
    </div>
  );
}

export default function Home(): React.ReactElement {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={siteConfig.title}
      description="INFINIT-C 제품 가이드 & 연동 문서">
      <HomepageHeader />
      <main>
        <div className="container padding-vert--xl">
          <div className={clsx('row', styles.productRow)}>
            {products.map((props) => (
              <ProductCard key={props.title} {...props} />
            ))}
          </div>
        </div>
      </main>
    </Layout>
  );
}
