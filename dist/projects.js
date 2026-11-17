const github = 'https://github.com/armaankhan2905';

export const projects = [
  {
    name: 'AirSync',
    category: 'Desktop & Systems',
    meta: 'Windows • Computer Vision',
    color: '#70a5ff',
    repo: github + '/AirSync',
    badge: 'CODE',
    download: { label: 'Download Source', url: github + '/AirSync/archive/HEAD.zip' },
    tagline: 'Touchless PowerPoint and Word control for Windows using hand gestures and facial authentication.',
    description: 'AirSync brings camera-based input to desktop presentations and document workflows. The Windows app combines hand gestures, air writing, slide annotations, face authentication, role-based access, and presence detection.',
    highlights: [
      'Uses hand gestures as a touchless input method for PowerPoint and Word.',
      'Supports air writing and on-slide annotations during presentations.',
      'Includes face authentication, presence detection, and role-based access.',
    ],
    tech: ['Python', 'Computer Vision', 'Windows', 'Microsoft Office'],
  },
  {
    name: 'ClaimSaathi',
    category: 'AI & Compliance',
    meta: 'Hackathon • Web Demo',
    color: '#6be6b7',
    repo: github + '/ClaimSaathi',
    live: 'https://armaankhan2905.github.io/ClaimSaathi/',
    tagline: 'An insurance companion prototype that helps Indian policyholders understand coverage and examine a rejected claim.',
    description: 'My team, OverCooked Brains, built this clickable demo for The Builder’s Theory 1.0. It walks through policy terms, plan comparisons, claim rejections and complaint drafting. It uses fictional sample cases and predefined results for the AI flows.',
    highlights: [
      'Browse policy coverage, exclusions, limits, and waiting periods in plain language.',
      'Compare policies against a scenario or review the evidence behind a sample rejection.',
      'Preview a complaint letter and the steps for escalating a dispute.',
      'Switch between English, Hindi, and Hinglish in the demo.',
    ],
    tech: ['HTML', 'CSS', 'JavaScript', 'RAG (planned)', 'OCR (planned)'],
  },
  {
    name: 'AgentSwarm',
    category: 'Full-Stack',
    meta: 'Python • Multi-agent AI',
    color: '#f6b660',
    repo: github + '/AgentSwarm',
    tagline: 'A multi-agent platform for researching topics, checking claims, and producing reports.',
    description: 'AgentSwarm divides research into jobs for specialized AI agents. Instead of doing every step in one pass, the workflow separates web research, academic paper analysis, fact-checking, and report generation.',
    highlights: [
      'Dedicated agents investigate web sources and academic papers.',
      'Fact-checking is a distinct step in the workflow.',
      'A report-generation stage brings the findings together.',
    ],
    tech: ['Python', 'Multi-agent AI', 'Web Research', 'Report Generation'],
  },
  {
    name: 'CTRL-ALT-TRUST',
    category: 'Full-Stack',
    meta: 'TypeScript • OT Security',
    color: '#ac83fc',
    repo: github + '/CTRL-ALT-TRUST',
    tagline: 'A zero-trust security project for a simulated SCADA water pipeline.',
    description: 'CTRL-ALT-TRUST uses a simulated water pipeline to explore how zero-trust security applies to an industrial control system. The repository contains the TypeScript project and provides a starting point for inspecting the simulation.',
    highlights: [
      'Explores zero-trust security in an operational technology setting.',
      'Uses a water pipeline simulation to model the SCADA environment.',
      'Provides the TypeScript source for inspection on GitHub.',
    ],
    tech: ['TypeScript', 'Zero Trust', 'SCADA', 'Operational Technology'],
  },
];

export const categories = ['All', ...new Set(projects.map(project => project.category))];
export const projectsIn = category => projects.filter(project => category === 'All' || project.category === category);
