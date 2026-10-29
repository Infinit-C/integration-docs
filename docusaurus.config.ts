import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'INFINIT-C Docs',
  tagline: 'INFINIT-C 제품 가이드 & 연동 문서',
  favicon: 'img/favicon.svg',

  url: 'https://docs.infinit-c.com',
  baseUrl: '/',

  organizationName: 'Infinit-C',
  projectName: 'integration-docs',

  trailingSlash: false,

  // Claire 가이드 접근 코드의 SHA-256(hex). 코드 변경: CLAIRE_GUIDE_CODE_HASH=$(printf '%s' 'NEWCODE' | shasum -a 256 | cut -d' ' -f1) npm run build
  // 빈 문자열이면 잠금 해제. 게이트 구현: src/theme/Root.tsx
  customFields: {
    claireGuideCodeHash: process.env.CLAIRE_GUIDE_CODE_HASH ?? 'bb9043dc348f9c375244f4af88cb6ffc9ffe2560ce33950e6a3ca206939eb9ab',
  },

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
        // adsynapse SSP SDK 문서 (기본 인스턴스, docs/ 폴더)
        docs: {
          routeBasePath: 'adsynapse',
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/Infinit-C/integration-docs/edit/main/',
        },
        blog: false,
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

  plugins: [
    // Claire 사용 가이드 (두 번째 문서 인스턴스, docs-claire/ 폴더)
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'claire',
        path: 'docs-claire',
        routeBasePath: 'claire',
        sidebarPath: './sidebars-claire.ts',
        editUrl: 'https://github.com/Infinit-C/integration-docs/edit/main/',
      },
    ],
  ],

  themeConfig: {
    colorMode: {
      respectPrefersColorScheme: true, // 첫 방문 시 OS 다크/라이트 설정을 따른다
    },
    navbar: {
      title: 'INFINIT-C Docs',
      logo: {
        alt: 'INFINIT-C',
        src: 'img/infinit-logo.png',
      },
      items: [
        {
          to: '/claire-intro',
          label: 'Claire 소개',
          position: 'left',
        },
        {
          type: 'docSidebar',
          sidebarId: 'claireSidebar',
          docsPluginId: 'claire',
          position: 'left',
          label: 'Claire 가이드',
        },
        {
          type: 'docSidebar',
          sidebarId: 'integrationSidebar',
          position: 'left',
          label: 'adsynapse SDK',
        },
        {
          to: '/api/',
          label: 'adsynapse API',
          position: 'left',
        },
      ],
    },

    footer: {
      style: 'dark',
      links: [
        {
          title: 'INFINIT-C',
          items: [
            { label: 'Website', href: 'https://www.infinit-c.com' },
          ],
        },
        {
          title: 'Claire',
          items: [
            { label: 'Website', href: 'https://claire.infinit-c.com' },
            { label: '소개', to: '/claire-intro' },
            { label: 'User Guide', to: '/claire/intro' },
          ],
        },
        {
          title: 'adsynapse',
          items: [
            { label: 'Console', href: 'https://console.infinit-c.com' },
            { label: 'Flutter Guide', to: '/adsynapse/integration/flutter/getting-started' },
            { label: 'Android Guide', to: '/adsynapse/integration/Android/getting-started' },
            { label: 'iOS Guide', to: '/adsynapse/integration/iOS/getting-started' },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Infinit-C Co.,Ltd. All rights reserved.`,
    },

    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: [
        'java',       // Scala가 작동하려면 Java가 필수입니다.
        'scala',
        'swift',      // iOS
        'objectivec', // iOS
        'kotlin',     // Android
        'groovy',     // Gradle
        'ruby',       // CocoaPods
        'bash',       // 터미널 명령어
        'dart',
      ],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
