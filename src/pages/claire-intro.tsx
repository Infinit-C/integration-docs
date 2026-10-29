import React from 'react';
import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './claire-intro.module.css';

// 외부 피칭용 Claire 소개 페이지. 공개 경로(/claire-intro) — /claire 가이드 잠금과 별개.

const points = [
  {
    title: '설정은 한 번이면 끝',
    body: '매체 계정을 연결하고 목표(KPI)와 알림 기준을 한 번 정해 두면, 그 뒤의 성과 수집·추적·알림은 Claire가 알아서 합니다.',
  },
  {
    title: '채팅으로 묻고, 채팅으로 지시',
    body: '"이번 주 CPM 왜 올랐어?", "CTR 1% 밑으로 떨어지면 알려줘." 보고서를 뒤지는 대신 대화 한 줄이면 됩니다.',
  },
  {
    title: '확인은 줄이고, 운영에 집중',
    body: '이상이 있을 때만 알림이 오고, 정해진 시간에 요약이 Slack·이메일로 도착합니다. 매일 데이터를 열어 보는 시간이 사라집니다.',
  },
];

const chats = [
  {q: '이번 주 브랜드A 캠페인 성과 어때?', a: '노출 42만, 클릭 5,120건으로 CTR 1.22%입니다. 지난주보다 클릭이 18% 늘었고 CPC는 403원으로 목표(800원 이하) 안에 있습니다.'},
  {q: 'CPM이 9,000원 넘으면 Slack으로 알려줘', a: '"브랜드A" 그룹에 CPM 9,000원 초과 알림을 만들었습니다. 1시간마다 확인하고 운영 채널로 보냅니다.'},
  {q: '매주 월요일 아침에 지난주 요약 보내줘', a: '매주 월요일 09:00에 지난 7일 노출·클릭·비용 요약을 이메일로 보내도록 예약했습니다.'},
];

const before = ['매체 콘솔 4~5곳을 돌며 지표 확인', '엑셀에 옮겨 붙여 주간 보고서 작성', '이상 징후를 뒤늦게 발견', '지표 질문마다 담당자에게 요청'];
const after = ['연결된 캠페인 지표가 한 화면에 자동 수집', '정해진 시각에 요약이 Slack·이메일로 도착', '기준 이탈 시 즉시 알림', '궁금한 건 Claire에게 바로 질문'];

export default function ClaireIntro(): React.ReactElement {
  return (
    <Layout title="Claire 소개" description="캠페인 운영, 이제 물어보면 됩니다. 한 번 설정하면 성과 수집·알림·요약을 Claire가 맡고, 궁금한 건 채팅으로 묻습니다.">
      <header className={styles.hero}>
        <div className="container">
          <p className={styles.eyebrow}>CLAIRE · AI MARKETING ASSISTANT</p>
          <Heading as="h1" className={styles.heroTitle}>
            캠페인 운영,<br />이제 <span className={styles.gradientText}>물어보면</span> 됩니다
          </Heading>
          <p className={styles.heroSub}>
            매체 연결 한 번, 목표 설정 한 번. 그다음부터 성과 확인과 알림은 Claire가 맡고,
            궁금한 것은 채팅으로 묻고 지시하세요.
          </p>
          <div className={styles.videoWrap}>
            <video controls muted playsInline preload="metadata" poster="/img/claire/dashboard.png" src="/video/claire/claire-flow.mp4" />
            <p className={styles.videoCaption}>캠페인 연결부터 질문까지, 1분이면 충분합니다.</p>
          </div>
        </div>
      </header>

      <main>
        <section className={styles.section}>
          <div className="container">
            <Heading as="h2" className={styles.h2}>한 번 설정하면, 그다음은 Claire가 합니다</Heading>
            <div className={styles.grid3}>
              {points.map((p, i) => (
                <div key={p.title} className={styles.card}>
                  <span className={styles.num}>{i + 1}</span>
                  <Heading as="h3" className={styles.h3}>{p.title}</Heading>
                  <p>{p.body}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className={`${styles.section} ${styles.sectionAlt}`}>
          <div className="container">
            <Heading as="h2" className={styles.h2}>이런 대화로 운영합니다</Heading>
            <p className={styles.lead}>질문도, 알림·요약 설정도 같은 채팅창에서 끝납니다. Claire는 지금 보고 있는 캠페인의 실제 데이터를 알고 답합니다.</p>
            <div className={styles.chatList}>
              {chats.map((c) => (
                <div key={c.q} className={styles.chat}>
                  <p className={styles.user}>{c.q}</p>
                  <p className={styles.claire}><span className={styles.claireTag}>Claire</span>{c.a}</p>
                </div>
              ))}
            </div>
            <p className={styles.note}>예시 대화입니다. 실제 수치는 연결된 캠페인 데이터로 답합니다.</p>
          </div>
        </section>

        <section className={styles.section}>
          <div className="container">
            <Heading as="h2" className={styles.h2}>하루 운영이 이렇게 달라집니다</Heading>
            <div className={styles.compare}>
              <div className={styles.compareCol}>
                <p className={styles.compareLabel}>지금까지</p>
                <ul>{before.map((t) => <li key={t}>{t}</li>)}</ul>
              </div>
              <div className={`${styles.compareCol} ${styles.compareAfter}`}>
                <p className={styles.compareLabel}>Claire와 함께</p>
                <ul>{after.map((t) => <li key={t}>{t}</li>)}</ul>
              </div>
            </div>
          </div>
        </section>

        <section className={`${styles.section} ${styles.sectionAlt}`}>
          <div className="container">
            <Heading as="h2" className={styles.h2}>화면은 두 가지면 충분합니다</Heading>
            <div className={styles.shots}>
              <figure>
                <img src="/img/claire/dashboard.png" alt="Claire 대시보드: CTR·미디어 비용 카드와 일별 노출·클릭 차트" loading="lazy" />
                <figcaption>대시보드 — 조직이 함께 보는 성과 한 화면</figcaption>
              </figure>
              <figure>
                <img src="/img/claire/chat-panel.png" alt="캠페인 상세 화면에서 열린 Claire 채팅 패널" loading="lazy" />
                <figcaption>채팅 — 어느 화면에서든 열어서 묻고 지시</figcaption>
              </figure>
            </div>
          </div>
        </section>

        <section className={styles.cta}>
          <div className="container">
            <p className={styles.platforms}>DV360 · Google Ads · Meta · SA360 · Kakao Moment 지원</p>
            <Heading as="h2" className={styles.ctaTitle}>데이터를 확인하는 시간을, 캠페인을 키우는 시간으로.</Heading>
            <div className={styles.ctaRow}>
              <Link className="button button--primary button--lg" href="https://www.infinit-c.com">도입 문의</Link>
              <Link className="button button--outline button--lg" href="https://claire.infinit-c.com">Claire 바로가기</Link>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
