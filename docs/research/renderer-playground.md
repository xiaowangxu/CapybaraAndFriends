---
layout: article
title: Markdown 渲染器全能力测试场
description: 一篇用于压力测试 Markdown、MathJax、HTML 与 Vue 交互能力的复杂文档
type: 实验
topic: Frontend
date: 2026-09-01
author: SunWx
status: Published
---

<script setup lang="ts">
import { computed, ref } from 'vue'
import { withBase } from 'vitepress'

const count = ref(3)
const intensity = ref(64)
const selectedMode = ref('Markdown')
const modes = ['Markdown', 'Vue', 'MathJax']
const checks = ref([
  { label: '结构与排版', done: true },
  { label: '公式与代码', done: true },
  { label: '响应式交互', done: false }
])

const completedChecks = computed(() => checks.value.filter(item => item.done).length)
const signal = computed(() => Math.round((count.value * intensity.value) / 10))

function resetLab() {
  count.value = 3
  intensity.value = 64
  selectedMode.value = 'Markdown'
  checks.value.forEach((item, index) => { item.done = index < 2 })
}
</script>

这不是一篇普通文章，而是一份可以长期保留的 **renderer playground**。它把常见 Markdown、VitePress 扩展、MathJax、原生 HTML 与 Vue 响应式状态放在同一篇文档里，用来快速发现主题样式、语法解析和移动端布局的回归。

> 如果某次主题更新后，这篇文章仍然结构清晰、没有横向溢出，而且下面的控件都能响应，那么渲染链路大概率仍然健康。

# 第一层：基础排版与行内语义

普通段落可以同时包含 **粗体**、*斜体*、***粗斜体***、~~删除线~~、`inline code`、<mark>高亮文本</mark>、H<sub>2</sub>O、x<sup>2</sup>，以及一个指向 [VitePress 官方文档](https://vitepress.dev/) 的外部链接。

中文标点、English words、`camelCaseIdentifier` 与一段很长的不可分割文本 <code :class="$style['breakable-code']">renderer_pipeline_should_remain_readable_even_when_identifiers_become_uncomfortably_long</code> 也被故意混合在这里，用于观察换行策略。

## 第二层：标题层级

这一节会一直下钻到六级标题，用来确认字号、间距、锚点和右侧目录的层级表现。

### 第三层：组件模型

标题里也可以放置 `code`，例如 `useRenderer()`。

#### 第四层：状态边界

四级标题通常不会进入当前文章目录，但仍应保留正确的视觉层级。

##### 第五层：实现注记

这一级适合承载更细的技术说明。

###### 第六层：最小标题

六级标题应该足够克制，但不能与普通段落混淆。

# 列表、引用与多层嵌套

1. 第一层有序列表
   - 第二层无序列表
     - 第三层无序列表
       1. 第四层有序列表
       2. 同一层中的第二项，包含 **粗体** 和 `code`
   - 第二个分支包含一段引用：

     > 引用可以出现在列表项内部。
     >
     > - 引用中还能继续放列表
     > - 也能包含行内公式：<br>$a^2 + b^2 = c^2$

2. 第二个一级列表项包含代码：

   ```ts
   interface RenderNode {
     type: 'heading' | 'paragraph' | 'interactive'
     children?: RenderNode[]
   }
   ```

3. 最后一项用于确认列表之后能正常回到正文流。

任务列表可以表达另一种状态：

- [x] Markdown 已解析
- [x] MathJax 已挂载
- [ ] 在真实手机上做一次触摸测试
- [ ] 在极端内容长度下继续扩展样例

> 一级引用用于强调结论。
>
> > 二级引用用于补充上下文。
> >
> > > 三级引用不常见，但渲染器仍然需要保持边界和缩进。

# 表格与对齐

| 能力 | 输入示例 | 预期输出 | 状态 |
| :--- | :---: | ---: | :---: |
| 行内语义 | `**strong**` | 粗体文本 | ✅ |
| 公式 | `$E = mc^2$` | 行内 MathJax | ✅ |
| 代码 | 三反引号 | 高亮代码块 | ✅ |
| 图片 | `![alt](url)` | 响应式图片 | ✅ |
| Vue | `@click` / `v-model` | 响应式状态 | ✅ |

表格单元格还可以包含 **强调文本**、`const value = 42` 与较长说明；在移动端，表格应保持可读并允许必要的横向滚动，而不是撑破整个页面。

# 公式：从行内到矩阵

行内公式 $E = mc^2$ 应该和中文基线自然对齐。概率密度也可以写成 <span :class="$style['inline-math-lock']">$p(x \mid \mu, \sigma^2)$。</span>

下面是一个块级积分：

<div :class="$style['formula-scroll']">

$$
\int_{-\infty}^{\infty} e^{-x^2}\,dx = \sqrt{\pi}
$$

</div>

再放入一个带分段条件、求和与矩阵的组合：

<div :class="$style['formula-scroll']">

$$
f(x) =
\begin{cases}
\displaystyle \sum_{i=1}^{n} w_i x_i, & x \ge 0 \\
\displaystyle \frac{1}{1 + e^{-x}}, & x < 0
\end{cases}
\qquad
A =
\begin{bmatrix}
1 & 2 & 3 \\
4 & 5 & 6 \\
7 & 8 & 9
\end{bmatrix}
$$

</div>

::: tip 公式测试提示
如果公式比正文宽，容器应该允许局部滚动，不应导致整页出现横向滚动条。
:::

# 代码、高亮与代码组

普通代码块支持行号高亮、聚焦行和语言标签：

```ts {3,6-8}
import { computed, ref } from 'vue'

const source = ref(21)
const doubled = computed(() => source.value * 2)

function update(next: number) {
  source.value = next
  return doubled.value
}
```

代码组可以在不同实现之间切换：

::: code-group
```ts [TypeScript]
type Result<T> = {
  data: T
  updatedAt: Date
}

export function wrap<T>(data: T): Result<T> {
  return { data, updatedAt: new Date() }
}
```

```js [JavaScript]
export function wrap(data) {
  return {
    data,
    updatedAt: new Date()
  }
}
```

```vue [Vue SFC]
<script setup>
import { ref } from 'vue'
const count = ref(0)
</script>

<template>
  <button @click="count++">{{ count }}</button>
</template>
```
:::

::: warning 边界条件
代码块中的 `<template>`、<code v-pre>{{ interpolation }}</code> 和 `@click` 都必须被当作示例代码，而不能被外层 Vue 编译器执行。
:::

::: details 点击展开隐藏内容
这里是 VitePress 的 details 容器。

- 可以包含 Markdown 列表
- 可以包含 `inline code`
- 也可以包含公式 $\phi = \frac{1 + \sqrt{5}}{2}$
:::

# 图片、说明文字与原生 HTML

下面这张图片使用标准 Markdown 图片语法，并带有 title：

![水豚与朋友站点横幅](/assets/banner.png "Markdown 图片语法渲染的站点横幅")

下面则是一个原生 HTML `figure`，图片地址通过 VitePress 的 `withBase()` 动态绑定：

<figure :class="$style['html-figure']">
  <img :src="withBase('/assets/capybara.png')" alt="正在工作的水豚图标">
  <figcaption>
    <strong>图 1：</strong>原生 HTML、Vue 属性绑定与语义化 <code>figcaption</code> 的组合。
  </figcaption>
</figure>

<details :class="$style['native-details']">
  <summary>原生 HTML details：点击查看诊断信息</summary>
  <div :class="$style['native-details__body']">
    <p><strong>渲染模式：</strong>HTML5 disclosure widget</p>
    <p><strong>键盘支持：</strong>聚焦后可用 Enter 或 Space 切换。</p>
    <p><strong>嵌套元素：</strong><kbd>Ctrl</kbd> + <kbd>K</kbd>、<mark>mark</mark>、<code>code</code></p>
  </div>
</details>

# Vue 交互实验台

下面这块不是静态示意图。它直接使用本 Markdown 文件顶部 `<script setup>` 中的响应式状态，刷新页面后会恢复初始值。

<section :class="$style['vue-lab']" aria-labelledby="vue-lab-title">
  <div :class="$style['vue-lab__heading']">
    <div>
      <p :class="$style['vue-lab__eyebrow']">LIVE VUE STATE</p>
      <h2 id="vue-lab-title">渲染信号控制台</h2>
    </div>
    <button type="button" :class="$style['vue-lab__reset']" @click="resetLab">重置</button>
  </div>

  <div :class="$style['vue-lab__grid']">
    <section :class="$style['vue-lab__panel']" aria-label="计数器">
      <span :class="$style['vue-lab__label']">节点数量</span>
      <div :class="$style.counter">
        <button type="button" aria-label="减少节点数量" @click="count = Math.max(0, count - 1)">−</button>
        <output aria-live="polite">{{ count }}</output>
        <button type="button" aria-label="增加节点数量" @click="count++">＋</button>
      </div>
    </section>
    <section :class="$style['vue-lab__panel']" aria-label="渲染强度">
      <label :class="$style['vue-lab__label']" for="render-intensity">渲染强度：{{ intensity }}%</label>
      <input id="render-intensity" v-model.number="intensity" type="range" min="0" max="100" step="1">
      <progress :value="intensity" max="100">{{ intensity }}%</progress>
    </section>
  </div>

  <fieldset :class="$style['mode-picker']">
    <legend>选择当前观察模式</legend>
    <label v-for="mode in modes" :key="mode" :class="{ [$style['is-active']]: selectedMode === mode }">
      <input v-model="selectedMode" type="radio" name="renderer-mode" :value="mode">
      {{ mode }}
    </label>
  </fieldset>

  <div :class="$style['check-grid']">
    <label v-for="item in checks" :key="item.label" :class="{ [$style['is-done']]: item.done }">
      <input v-model="item.done" type="checkbox">
      <span>{{ item.label }}</span>
    </label>
  </div>

  <div :class="$style['vue-lab__result']" role="status" aria-live="polite">
    <span>模式 <strong>{{ selectedMode }}</strong></span>
    <span>信号 <strong>{{ signal }}</strong></span>
    <span>检查 <strong>{{ completedChecks }}/{{ checks.length }}</strong></span>
  </div>
</section>

交互结果也可以回到普通 Markdown 中：当前模式是 **{{ selectedMode }}**，节点数量是 **{{ count }}**，计算信号为 $S = n \times i / 10$，页面中的实时结果是 **{{ signal }}**。

# 综合边界测试

::: danger 故意复杂的组合
下面的内容将多个语法放到同一区域，用来观察相邻元素的 margin collapse、颜色继承与溢出行为。

1. 一个带 `code` 的有序项
   - 嵌套项包含 **粗体**、*斜体* 与 $\alpha + \beta$
   - 另一个嵌套项包含链接：[回到交互实验台](#vue-交互实验台)
2. 一个超长路径：<code :class="$style['breakable-code']">C:\workspace\renderer\packages\markdown\src\plugins\deeply-nested\experimental\index.ts</code>

> 容器里的引用仍需保持清晰的视觉边界。
:::

---

最后一条水平分隔线之后，放置一段普通文字和一个手动换行。  
这一行应紧跟在上一行之后，而不是开始新的段落。

<style module>
code.breakable-code {
  overflow-wrap: anywhere;
  word-break: break-word;
  white-space: normal;
}

.inline-math-lock {
  white-space: nowrap;
}

.formula-scroll {
  display: block;
  max-width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
  scrollbar-width: thin;
  -webkit-overflow-scrolling: touch;
}

.formula-scroll :global(mjx-container.MathJax[display='true']) {
  display: grid !important;
  width: max-content;
  min-width: 100%;
  max-width: none;
  place-items: center;
  margin: 1em 0 !important;
  text-align: center;
}

.formula-scroll :global(mjx-container.MathJax[display='true'] > svg) {
  display: block;
  max-width: none;
}

.html-figure {
  margin: 2rem 0;
  overflow: hidden;
  border: 1px solid var(--cf-border);
  border-radius: 1.25rem;
  background: var(--cf-surface);
}

.html-figure img {
  display: block;
  width: min(12rem, 55%);
  margin: 2rem auto 1rem;
}

.html-figure figcaption {
  padding: 1rem 1.25rem;
  border-top: 1px solid var(--cf-border);
  color: #5f5f5f;
  font-size: .9rem;
  text-align: center;
}

.native-details {
  margin: 1.5rem 0 2.5rem;
  overflow: hidden;
  border: 1px solid var(--cf-border);
  border-radius: 1rem;
  background: var(--cf-surface);
}

.native-details summary {
  padding: .85rem 1rem;
  cursor: pointer;
  font-weight: 600;
}

.native-details__body {
  padding: .25rem 1rem 1rem;
  border-top: 1px solid var(--cf-border);
}

.vue-lab {
  --lab-accent: #d99a00;
  margin: 2rem 0 3rem;
  padding: 1.25rem;
  border: 1px solid #d8d5cf;
  border-radius: 1.5rem;
  background:
    radial-gradient(circle at 100% 0, rgba(255, 190, 48, .16), transparent 35%),
    #fff;
  box-shadow: 0 18px 45px rgba(25, 20, 10, .07);
}

.vue-lab__heading,
.vue-lab__result,
.counter,
.mode-picker,
.mode-picker label,
.check-grid label {
  display: flex;
  align-items: center;
}

.vue-lab__heading {
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
}

.vue-lab__heading h2 {
  margin: 0;
  font-size: 1.35rem;
}

.vue-lab__eyebrow {
  margin: 0 0 .2rem;
  color: #9a6d00;
  font-size: .7rem;
  font-weight: 750;
  letter-spacing: .14em;
}

.vue-lab button {
  border: 1px solid #d6d1c8;
  background: #fff;
  cursor: pointer;
}

.vue-lab button:hover {
  border-color: #aaa296;
  background: #faf8f3;
}

.vue-lab__reset {
  padding: .45rem .8rem;
  border-radius: 999px;
  font-size: .8rem;
}

.vue-lab__grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: .75rem;
}

.vue-lab__panel {
  min-width: 0;
  padding: 1rem;
  border: 1px solid #ebe7df;
  border-radius: 1rem;
  background: rgba(250, 249, 246, .82);
}

.vue-lab__label {
  display: block;
  margin-bottom: .7rem;
  color: #655f55;
  font-size: .78rem;
  font-weight: 650;
}

.counter {
  gap: .75rem;
}

.counter button {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: .7rem;
  font-size: 1.2rem;
}

.counter output {
  min-width: 2.5rem;
  font-size: 1.35rem;
  font-weight: 700;
  text-align: center;
}

.vue-lab input[type='range'],
.vue-lab progress {
  width: 100%;
  accent-color: var(--lab-accent);
}

.vue-lab progress {
  display: block;
  height: .5rem;
  margin-top: .75rem;
}

.mode-picker {
  flex-wrap: wrap;
  gap: .5rem;
  margin: 1rem 0;
  padding: 0;
  border: 0;
}

.mode-picker legend {
  width: 100%;
  margin-bottom: .5rem;
  color: #655f55;
  font-size: .78rem;
  font-weight: 650;
}

.mode-picker label {
  gap: .4rem;
  padding: .45rem .7rem;
  border: 1px solid #ded9cf;
  border-radius: 999px;
  cursor: pointer;
  font-size: .82rem;
}

.mode-picker label.is-active {
  border-color: #e2a20c;
  background: #fff4d2;
}

.check-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: .5rem;
}

.check-grid label {
  gap: .5rem;
  min-width: 0;
  padding: .7rem;
  border-radius: .75rem;
  background: #f4f3f0;
  color: #6c675f;
  font-size: .8rem;
}

.check-grid label.is-done {
  background: #eef6e9;
  color: #315426;
}

.vue-lab__result {
  flex-wrap: wrap;
  gap: .6rem 1rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px dashed #d8d2c8;
  color: #6d665b;
  font-size: .82rem;
}

.vue-lab__result strong {
  color: #26221d;
}

@media (max-width: 640px) {
  .vue-lab {
    padding: 1rem;
    border-radius: 1.15rem;
  }

  .vue-lab__grid,
  .check-grid {
    grid-template-columns: 1fr;
  }

  .vue-lab__heading {
    align-items: flex-start;
  }
}
</style>
