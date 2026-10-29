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

const personas = [
  {who: '대행사 운영팀', need: '광고주·브랜드별로 캠페인을 묶어 두고, 각 담당자가 자기 그룹만 보며 운영합니다. 보고서는 정해진 시각에 자동으로 나갑니다.'},
  {who: '인하우스 마케터', need: 'DV360·Google Ads·Meta·SA360·Kakao Moment를 한 화면에서 보고, 매체마다 다른 지표 이름을 신경 쓰지 않아도 됩니다.'},
  {who: '마케팅 총괄 및 대행사 대표님', need: '대시보드를 열거나 "이번 달 비용 얼마 썼어?"라고 물으면 끝. 담당자에게 자료를 요청하고 기다릴 필요가 없습니다.'},
];

const features = [
  {t: 'KPI 목표 추적과 이상 알림', d: 'CTR 하한, CPC 상한처럼 목표를 정해 두면 달성 여부를 계속 확인하고, 기준을 벗어나면 Slack·이메일로 즉시 알립니다.'},
  {t: '미디어 플래닝', d: '기존 리포트들과 캠페인을 바탕으로 최적의 미디어 플랜을 제공합니다.'},
  {t: '캠페인 통합 관리', d: '5개 매체 캠페인을 광고주 단위 그룹으로 묶어 한 화면에서.'},
  {t: '정기 요약', d: '매일·매주 원하는 시각에 원하는 지표만 담아 자동 발송.'},
  {t: '대시보드·시각화', d: '필요한 차트를 골라 조직이 함께 보는 홈 화면 구성.'},
  {t: '리포트 내보내기', d: '기간·구분 기준·지표를 골라 CSV·Excel로 바로 다운로드.'},
];

const faqs = [
  {q: '어떤 매체를 지원하나요?', a: '마케터가 직접 운영·관리하는 매체들부터 제공합니다. 현재 DV360, Google Ads, Meta, SA360, Kakao Moment가 지원됩니다. 이후 원하시는 셀프서빙 매체를 알려주시면 추가 연동할 예정입니다.'},
  {q: '광고주별로 보는 사람을 나눌 수 있나요?', a: '광고주 캠페인 정보 보안이 걱정이시군요. 조직 내 접근 권한을 분류할 수 있습니다. 또한 누가 무엇을 바꿨는지는 이력과 감사 기록에 남습니다.'},
  {q: '알림과 요약은 어디로 오나요?', a: '이메일 그룹과 슬랙 채널을 등록하세요. 알림과 요약 리포트를 받으실 분들을 설정할 수 있습니다.'},
  {q: 'Claire의 답은 믿을 수 있나요?', a: 'Claire는 연결된 캠페인에서 실제로 수집한 지표로만 답합니다. 데이터가 없으면 없다고 말하고, 답에 쓴 기간과 수치를 함께 보여줍니다.'},
  {q: '우리 캠페인 정보가 다른 유저의 최적화를 위해 사용되나요?', a: '그렇지 않습니다. 인피니트씨에서 등록한 데이터 및 계정 소유자가 직접 올린 데이터만 최적화에 활용됩니다.'},
  {q: '기존 보고 체계와 같이 쓸 수 있나요?', a: '네. 리포트를 CSV·Excel로 내려받아 기존 양식에 넣거나, 정기 요약을 지금 쓰는 Slack 채널로 받으면 됩니다. 한국어·영어 화면을 모두 제공합니다.'},
];

const before = ['매체 콘솔 4~5곳을 돌며 지표 확인', '엑셀에 옮겨 붙여 주간 보고서 작성', '이상 징후를 뒤늦게 발견', '지표 질문마다 담당자에게 요청'];
const after = ['연결된 캠페인 지표가 한 화면에 자동 수집', '정해진 시각에 요약이 Slack·이메일로 도착', '기준 이탈 시 즉시 알림', '궁금한 건 Claire에게 바로 질문'];

export default function ClaireIntro(): React.ReactElement {
  return (
    <Layout title="Claire 소개" description="캠페인의 플래닝, 운영 최적화, 리포트까지 클레어의 AI가 모두 도와드립니다. 단 한 번의 매체 연결과 목표 설정으로 성과 관리와 알림까지 자동 세팅됩니다.">
      <header className={styles.hero}>
        <div className="container">
          <p className={styles.eyebrow}>CLAIRE · AI MARKETING ASSISTANT</p>
          <Heading as="h1" className={styles.heroTitle}>
            캠페인의 플래닝, 운영 최적화, 리포트까지<br /><span className={styles.gradientText}>클레어의 AI</span>가 모두 도와드립니다
          </Heading>
          <p className={styles.heroSub}>
            단 한 번의 매체 연결과 목표 설정으로, 성과 관리 및 알림까지 자동 세팅됩니다.<br />
            더욱 똑똑해진 클레어 AI와의 채팅으로 손쉽게 지시할 수 있어요.
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
            <Heading as="h2" className={styles.h2}>담당자는 단 한 번의 설정만, 그다음은 Claire가 합니다</Heading>
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
            <Heading as="h2" className={styles.h2}>이런 분들께 추천합니다</Heading>
            <div className={styles.grid3}>
              {personas.map((p) => (
                <div key={p.who} className={styles.card}>
                  <Heading as="h3" className={styles.h3}>{p.who}</Heading>
                  <p>{p.need}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className={styles.section}>
          <div className="container">
            <Heading as="h2" className={styles.h2}>일상 대화처럼 운영합니다</Heading>
            <p className={`${styles.lead} ${styles.leadOneLine}`}>질문도, 알림·요약 설정도 같은 채팅창에서 끝납니다. Claire는 지금 보고 있는 캠페인의 실제 데이터를 알고 답합니다.</p>
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

        <section className={`${styles.section} ${styles.sectionAlt}`}>
          <div className="container">
            <Heading as="h2" className={styles.h2}>마케터의 일과가 바뀝니다</Heading>
            <p className={styles.lead}>지식을 쌓고 의사결정하는 데 시간을 투자하세요.</p>
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

        <section className={styles.section}>
          <div className="container">
            <Heading as="h2" className={styles.h2}>대표 기능</Heading>
            <div className={styles.features}>
              {features.map((f) => (
                <div key={f.t} className={styles.feature}>
                  <Heading as="h3" className={styles.h3}>{f.t}</Heading>
                  <p>{f.d}</p>
                </div>
              ))}
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

        <section className={styles.section}>
          <div className="container">
            <Heading as="h2" className={styles.h2}>자주 묻는 질문</Heading>
            <div className={styles.faq}>
              {faqs.map((f) => (
                <details key={f.q}>
                  <summary>{f.q}</summary>
                  <p>{f.a}</p>
                </details>
              ))}
            </div>
          </div>
        </section>

        <section className={styles.cta}>
          <div className="container">
            <p className={styles.platforms}>DV360 · Google Ads · Meta · SA360 · Kakao Moment 지원</p>
            <Heading as="h2" className={styles.ctaTitle}><span className={styles.nowrap}>루틴한 업무는 클레어에 맡기시고,</span><br /><span className={styles.nowrap}>마케터의 역량을 개발하는 데 집중하세요.</span></Heading>
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
