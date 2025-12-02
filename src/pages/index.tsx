import React from 'react';
import clsx from 'clsx';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './index.module.css';

// 1. 상단 헤더 컴포넌트 (버튼 삭제됨)
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

// 2. 하단 RTB 정보 컴포넌트 (새로 추가됨)
function RtbInfoSection() {
  return (
    <div className="container padding-vert--xl">
      <div className="row">
        <div className="col col--8 col--offset-2">
          <Heading as="h2">RTB 프로토콜 지원 범위</Heading>
          <p>
            AdCore는 <strong>IAB OpenRTB API 2.6</strong> 규격에 기반한 AdCore RTB 프로토콜을 통해 RTB 입찰 요청과 응답을 처리하고 있으며, 
            다른 버전도 일부 지원하고 있습니다. 
          </p>
          <p>
            AdCore RTB API는 OpenRTB API 프로토콜 전체 범위를 지원하지는 않기에 이 문서에 포함되지 않은 내용은 지원이 보장되지 않으며, 
            OpenRTB API 와 AdCore RTB API에서 차이가 있을 시 <strong>AdCore RTB API를 우선합니다.</strong> </p>
           <p> 
            지원 프로토콜의 범위는 다양한 상황에 따라 변경될 수 있습니다.
          </p>
          <hr />
          <p>
            IAB는 온라인 마케팅 표준화 등을 진행하는 협회로 RTB 표준화를 위한 가이드 문서를 제공하고 있습니다.<br/>
            필요 시 아래 링크에서 OpenRTB API 문서 확인이 가능합니다.
          </p>
          <ul>
            <li>
              <a href="https://iabtechlab.com/standards/openrtb/" target="_blank" rel="noopener noreferrer">
                IAB OpenRTB API 2.6
              </a>
            </li>
            <li>
              <a href="https://iabtechlab.com/standards/openrtb-native/" target="_blank" rel="noopener noreferrer">
                IAB OpenRTB Dynamic Native Ads API 1.2
              </a>
            </li>
            <li>
              <a href="https://iabtechlab.com/standards/vast/" target="_blank" rel="noopener noreferrer">
                IAB Video Ad Serving Template(VAST) 3.0
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
// 3. 메인 페이지 레이아웃
export default function Home(): React.ReactElement {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="SDK Integration Guide">
      <HomepageHeader />
      <main>
        <RtbInfoSection />
      </main>
    </Layout>
  );
}