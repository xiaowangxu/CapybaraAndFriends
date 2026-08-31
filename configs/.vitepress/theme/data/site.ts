export const siteText = {
  nav: {
    research: '研究',
    projects: '项目',
    about: '关于',
    search: '搜索',
    menu: '菜单'
  },
  home: {
    signal: '正在持续研究',
    latestLabel: '最近',
    latest: '最新研究',
    latestDescription: '从可复现的实验，到仍在形成中的问题。',
    recentCount: '篇近期文章',
    featured: '重点',
    areasLabel: '研究地图',
    areas: '我们关心的问题',
    projectsLabel: '项目档案',
    projects: '把想法变成可以继续工作的系统。',
    viewAll: '查看全部',
    readArticle: '阅读文章',
    explore: '探索研究',
    about: '了解机构',
    note: '独立、缓慢、可复现。'
  },
  research: {
    archive: '研究档案',
    title: '研究与文章',
    description: '研究、技术报告、实验与随笔。',
    search: '搜索标题、主题或类型…',
    all: '全部',
    results: '篇文章',
    noResults: '没有找到匹配的文章。',
    filter: '筛选主题',
    source: '内容来自 docs/research',
    filtered: '已筛选',
    clearFilters: '清除筛选'
  },
  article: {
    back: '返回研究列表',
    contents: '目录',
    related: '继续阅读',
    published: '发布于',
    by: '作者',
    reading: '阅读',
    noSections: '本文暂无小节目录。'
  },
  footer: {
    description: '探索本质，连接思想，创造影响。',
    note: '独立研究机构 · 研究、写作与开放实验。'
  }
} as const

export const routes = {
  home: '/',
  research: '/research/',
  projects: '/projects/',
  about: '/about/'
} as const
