import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'adsynapse SSP SDK 가이드 ',
  tagline: '개발자를 위한 연동 문서입니다',
  favicon: 'img/adsynapse-colorful-favicon-16.ico',

  // 배포할 실제 URL로 변경하세요
  url: 'https://adsynapse.infinit-c.com',
  baseUrl: '/',

  // GitHub Pages 배포 설정 (필요 없으면 무시해도 됨)
  organizationName: 'Infinit-C',
  projectName: 'integration-docs',

  trailingSlash: false,

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'ko',
    locales: ['ko', 'en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts', // sidebars.ts 파일을 참조합니다
        },
        blog: false, // 블로그 기능이 필요 없으면 false, 필요하면 설정 유지
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
    // ▼▼▼ [Redocusaurus 플러그인 설정] ▼▼▼
    [
      'redocusaurus',
      {
        specs: [
          {
            spec: 'api-spec/openapi.yaml', // 파일 경로: 루트/api-spec/openapi.yaml
            route: '/api/',                // 웹 접속 주소: /api/
          },
        ],
        theme: {
          primaryColor: '#1890ff', // Redoc 테마 포인트 컬러
        },
      },
    ],
    // ▲▲▲
  ],

  themeConfig: {


    // ▼▼▼ [네비게이션 바 설정 (여기가 중요)] ▼▼▼
    navbar: {
      logo: {
        alt: 'Site Logo',
        src: 'img/adsynapse-colorful-large.png', // 로고 파일 경로
      },
      items: [
        // 1. Web 메뉴
        {
          type: 'docSidebar',
          sidebarId: 'webSidebar', // sidebars.ts에 정의된 ID
          position: 'left',
          label: 'Web',
        },
        // 2. Android 메뉴
        {
          type: 'docSidebar',
          sidebarId: 'androidSidebar', // sidebars.ts에 정의된 ID
          position: 'left',
          label: 'Android',
        },
        // 3. iOS 메뉴
        {
          type: 'docSidebar',
          sidebarId: 'iosSidebar', // sidebars.ts에 정의된 ID
          position: 'left',
          label: 'iOS',
        },
        // 4. API 명세서 (Redoc)
        {
          to: '/api/',
          label: 'API Reference',
          position: 'left',
        },
        // 5. 우측 GitHub 아이콘 (선택 사항)
        {
          href: 'https://github.com/Infinit-C/adsynapse',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    // ▲▲▲

    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            { label: 'Web Guide', to: '/docs/web/script' },
            { label: 'Android Guide', to: '/docs/android/intro' },
            { label: 'iOS Guide', to: '/docs/ios/intro' },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Infinit-C Co.,Ltd. All rights reserved.`,
    },

    // ▼▼▼ [코드 하이라이팅 언어 추가] ▼▼▼
    // ... 위쪽 코드 생략 ...

    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      // ▼▼▼ [여기 수정] 에러 해결을 위해 java와 scala를 꼭 넣어주세요 ▼▼▼
      additionalLanguages: [
        'java',       // Scala가 작동하려면 Java가 필수입니다.
        'scala',      // 에러가 나는 범인이므로 명시적으로 추가해줍니다.
        'swift',      // iOS
        'objectivec', // iOS
        'kotlin',     // Android
        'groovy',     // Gradle
        'ruby',       // CocoaPods
        'bash',       // 터미널 명령어
      ],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
