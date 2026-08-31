# Capybara & Friends

Capybara & Friends 是一个中文独立研究机构网站，站点内容由 `docs/` 下的 Markdown 文件驱动。

## 目录结构

```text
configs/.vitepress/
├── config.mts                         VitePress 配置
├── data/content.data.mts              构建期扫描 docs 的内容数据
└── theme/
    ├── Layout.vue                     根据 frontmatter 选择页面壳
    ├── data/                          内容查询与站点固定文案
    └── components/
        ├── layout/                    站点头部与底部
        ├── pages/                     首页、研究列表、文章页
        ├── content/                   文章卡片等内容组件
        ├── research/                   Markdown 研究组件
        └── ui/                        可复用的基础控件

docs/
├── index.md                           首页内容与首页模块数据
├── about/index.md                     机构介绍
├── projects/index.md                 项目数据与项目说明
├── research/index.md                 研究列表页配置
└── research/*.md                     研究文章
```

## 开发

```bash
npm run docs:dev
npm run docs:build
npm run docs:preview
```

## 添加文章

在 `docs/research/` 新建 Markdown 文件，使用 `layout: article`，并填写标题、摘要、主题和日期等 frontmatter。内容加载器会自动将文章加入首页和研究列表，不需要修改 TypeScript 的文章数组。
