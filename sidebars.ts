import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  integrationSidebar: [
    {
      type: 'doc',
      id: 'integration/intro',
      label: '들어가기 앞서',
    },
    {
      type: 'category',
      label: 'Flutter',
      items: [
        'integration/flutter/getting-started',
        {
          type: 'category',
          label: '광고',
          items: [
            'integration/flutter/banner/how-to-use',
            'integration/flutter/native/how-to-use',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Android',
      items: [
        'integration/Android/getting-started',
        'integration/Android/configuration',
        'integration/Android/how-to-use',
      ],
    },
    {
      type: 'category',
      label: 'iOS',
      items: [
        'integration/iOS/getting-started',
        'integration/iOS/how-to-use',
      ],
    },
  ],
};

export default sidebars;
