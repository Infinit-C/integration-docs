import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  claireSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: 'Claire 소개',
    },
    {
      type: 'doc',
      id: 'getting-started',
      label: '시작하기',
    },
    {
      type: 'doc',
      id: 'campaigns',
      label: '캠페인 연결',
    },
    {
      type: 'doc',
      id: 'performance',
      label: '성과 확인',
    },
    {
      type: 'doc',
      id: 'chat',
      label: 'Claire와 대화하기',
    },
    {
      type: 'doc',
      id: 'targets',
      label: '지표와 KPI 규칙',
    },
    {
      type: 'doc',
      id: 'settings',
      label: '조직 설정',
    },
  ],
};

export default sidebars;
