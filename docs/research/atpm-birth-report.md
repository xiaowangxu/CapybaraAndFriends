---
layout: article
title: ATPM 从记忆操作到记忆动力学
description: 一份关于 Adaptive Transport–Proximal Memory 的设计报告：从四种记忆行为出发，构建具有 Read、Remember、Revise、Rewrite 能力的连续神经记忆系统。
type: 研究
topic: Neural Architecture
date: 2026-09-01
author: Capybara & Friends
status: Published
---

<script setup lang="ts">
import { computed, ref } from 'vue'

const lambda = ref(0.72)
const rho = ref(0.76)
const equationStep = ref(4)

const atlas = computed(() => {
  const highLambda = lambda.value >= 0.5
  const highRho = rho.value >= 0.5

  if (highLambda && highRho) {
    return {
      code: 'I',
      name: '定向重写',
      en: 'Directed Rewrite',
      tag: 'constrained read · directed write',
      copy: '查询被拉向写入锚点，同时允许目标地址偏离源地址。模型既知道“从哪里找到”，也能决定“写到哪里去”。',
      family: 'RCQP / CrossScan-like endpoint'
    }
  }

  if (!highLambda && highRho) {
    return {
      code: 'II',
      name: '自由检索 · 有向更新',
      en: 'Free Recall, Directed Update',
      tag: 'free read · directed write',
      copy: '读取保持内容驱动，但写入允许沿切空间迁移。适合“我能找到相关内容，但真正需要改动的位置并不是原位置”的情形。',
      family: 'content-addressed directed memory'
    }
  }

  if (highLambda && !highRho) {
    return {
      code: 'III',
      name: '稳定原址修订',
      en: 'Stable Revision',
      tag: 'constrained read · symmetric write',
      copy: '源地址与目标地址几乎重合，而查询被约束到同一锚点附近。它更像在原来的地方把已有事实修正得更准确。',
      family: 'in-place substitution'
    }
  }

  return {
    code: 'IV',
    name: '自由局部更新',
    en: 'Free Local Update',
    tag: 'free read · symmetric write',
    copy: '没有额外的 transport，也没有强制的 proximal recall。几何逐渐回到经典 delta-style memory 的端点。',
    family: 'GDN-like endpoint'
  }
})

const cursorStyle = computed(() => ({
  left: `${rho.value * 100}%`,
  top: `${(1 - lambda.value) * 100}%`
}))

const queryResidual = computed(() =>
  ((1 - lambda.value) * 100).toFixed(0)
)

const transportStrength = computed(() =>
  (rho.value * 100).toFixed(0)
)

const equationSteps = [
  {
    n: '01',
    title: 'Decay',
    formula: '\\bar E_t = \\alpha_t E_{t-1}',
    copy: '先决定多少旧状态应该自然延续。'
  },
  {
    n: '02',
    title: 'Predict & compare',
    formula: 'r_t = e_t - \\bar E_t^\\top s_t',
    copy: '从源地址读出旧实体，只更新“当前实体与旧预测之间的差”。'
  },
  {
    n: '03',
    title: 'Polarize',
    formula: '\\Omega_t = \\beta^K_t\\Pi_K + \\beta^V_t\\Pi_V',
    copy: 'Key 与 Value 属于同一实体，但可以以不同强度被修订。'
  },
  {
    n: '04',
    title: 'Transport',
    formula: 'd_t = s_t + \\rho_t\\tau_t',
    copy: '把“在哪里发现旧内容”与“在哪里写回新内容”分开。'
  },
  {
    n: '05',
    title: 'Substitute',
    formula: 'E_t = \\bar E_t + d_t(\\Omega_t r_t)^\\top',
    copy: '一次外积完成局部、可极化、可定向的替换。'
  },
  {
    n: '06',
    title: 'Recall',
    formula: 'q_t = q_t^0 + \\lambda_t(1-(q_t^0)^\\top a_t)a_t',
    copy: '读取查询可以保持自由，也可以被近端约束拉向更新后的锚点。'
  }
]

const activeEquation = computed(() =>
  equationSteps[Math.max(0, Math.min(equationSteps.length - 1, equationStep.value - 1))]
)
</script>

<div :class="$style.hero">
  <div :class="$style.eyebrow">CAPYBARA & FRIENDS · RESEARCH REPORT 001</div>

  <h1 :class="$style.heroTitle">
    ATPM 的诞生
    <span :class="$style.heroAccent">让记忆成为一种连续动力学</span>
  </h1>

  <p :class="$style.heroLead">
    从 <strong>Read · Remember · Revise · Rewrite</strong> 出发，
    我们试着回答一个很朴素的问题：
    <em>神经网络里的“记忆”，能不能不再只是一个被动保存过去的矩阵？</em>
  </p>

  <div :class="$style.heroMeta">
    <span>Adaptive Transport–Proximal Memory</span>
    <span>Architecture · Memory · Language Modeling</span>
    <span>September 2026</span>
  </div>
</div>

<div :class="$style.statusStrip">
  <div>
    <b>≈ 200M</b>
    <span>largest LM run</span>
  </div>
  <div>
    <b>≈ 20B</b>
    <span>FineWeb tokens</span>
  </div>
  <div>
    <b>1 state</b>
    <span>joint K/V entity memory</span>
  </div>
  <div>
    <b>O(T)</b>
    <span>recurrent sequence complexity</span>
  </div>
</div>

> **这不是一篇 SOTA 宣言。**
>
> 这份报告记录的是一个架构如何从问题本身长出来，以及它是否真的能离开合成任务，进入一个非平凡规模的语言模型。到目前为止，我们能比较有把握地说：**ATPM 是可训练的；它可以作为语言模型中的持续状态模块工作；它至少能够扩展到约 200M 参数、约 20B FineWeb tokens 的训练规模。**
>
> 更大的 scaling law、严格 compute-matched 的强基线比较，以及十亿参数以上的行为，我们还不知道。

---

# 1. 一切从“四个 R”开始 {#four-r}

最开始，我们并没有想设计一个新的 linear attention，也没有先写下一条 recurrence 再寻找解释。

问题反过来：

> **如果把“记忆”当成一个真正的认知动作，它到底应该会做什么？**

最小的答案似乎至少包含四件事。

<div :class="$style.fourR">
  <article>
    <span :class="$style.rIndex">01</span>
    <h3>Read</h3>
    <p>从过去留下的状态中，找到此刻真正相关的内容。</p>
  </article>

  <article>
    <span :class="$style.rIndex">02</span>
    <h3>Remember</h3>
    <p>当没有新证据推翻旧内容时，不要因为“每一步都必须更新”而把它破坏掉。</p>
  </article>

  <article>
    <span :class="$style.rIndex">03</span>
    <h3>Revise</h3>
    <p>新信息不是另起炉灶，而是对已有知识做小幅、局部、连续的纠正。</p>
  </article>

  <article>
    <span :class="$style.rIndex">04</span>
    <h3>Rewrite</h3>
    <p>当旧内容已经不再成立时，模型应该能够明确地替换它，而不是永远做指数平均。</p>
  </article>
</div>

传统 recurrent memory 很容易写成：

$$
M_t = \gamma_t M_{t-1} + \Delta M_t.
$$

它当然可以“记”。问题是，**记住并不等于拥有记忆行为**。

如果所有动作最终都被压成一个 `gate × update`，模型很容易学成一个安全的平均器：该保留的时候也写一点，该重写的时候也只写一点。Read、Remember、Revise、Rewrite 在数学上没有真正分开，所谓“四种行为”最后只剩下一条连续但语义贫乏的衰减曲线。

我们的目标因此变成了：

<div :class="$style.statement">
  <span>Design thesis</span>
  <p>
    不为 4R 分别设计四个 operator。<br/>
    让它们成为<strong>同一个动力系统在不同区域里的自然行为</strong>。
  </p>
</div>

这条约束后来非常重要。它迫使我们不断删掉那些“这里不行就再加一个 gate”的设计。

---

# 2. 第一个转折：记忆不是两个表，而是一个“实体” {#joint-entity}

早期设计中，一个反复出现的问题是 K/V 的角色。

如果把 Key memory 和 Value memory 完全拆成两个状态，精确控制会变得容易；但代价也很明显：模型似乎在维护两个彼此相关、却物理上独立的世界。

我们最终更喜欢另一种解释：

> **一条记忆首先是一个 entity；K 与 V 只是这个 entity 的两个坐标视图。**

于是每个 head 只有一个联合状态：

$$
E_t \in \mathbb{R}^{S \times (d_k + d_v)},
\qquad
e_t = [k_t;v_t].
$$

其中：

- $S$ 是 address / mode 维度；
- $d_k$ 与 $d_v$ 是实体内部两块固定坐标；
- $E_t$ 是唯一持久状态；
- K/V 的分离只发生在“修改哪一部分实体”时，而不是维护两份独立 memory。

这一步形成了 **PSM — Partial Substitution Memory** 的核心。

先衰减旧状态：

$$
\bar E_t = \alpha_t E_{t-1}.
$$

从源地址 $s_t$ 读取当前预测：

$$
\hat e_t = \bar E_t^\top s_t.
$$

只计算新实体与旧预测之间的残差：

$$
r_t = e_t - \hat e_t.
$$

再让 K/V 具有独立的 substitution strength：

$$
\Omega_t
=
\beta^K_t \Pi_K
+
\beta^V_t \Pi_V,
$$

其中 $\Pi_K,\Pi_V$ 是联合实体空间上的固定坐标投影。

最终更新：

$$
E_t
=
\bar E_t
+
d_t
\left(
\Omega_t r_t
\right)^\top.
$$

这条式子已经带来了一个我们很喜欢的性质：

<div :class="$style.formulaCallout">
  <div>
    <small>what to preserve</small>
    <b>$\alpha_t$</b>
  </div>
  <div>
    <small>what is wrong</small>
    <b>$r_t$</b>
  </div>
  <div>
    <small>which part to revise</small>
    <b>$\beta^K_t,\beta^V_t$</b>
  </div>
  <div>
    <small>where to write</small>
    <b>$d_t$</b>
  </div>
</div>

**Remember** 不再需要一个叫 `remember_gate` 的东西。

当 $\alpha_t$ 高、而 $\beta_t$ 小时，旧状态自然留下来。

**Revise** 也不需要单独的 operator。

当 residual 小、substitution strength 温和时，更新天然就是局部修订。

**Rewrite** 则是同一条更新在更强 substitution 下的另一端。

但是，PSM 仍然留下了一个更深的问题。

---

# 3. 真正让 ATPM 出现的问题：读到的地方，为什么一定是写回的地方？ {#source-destination}

绝大多数 delta-style memory 都隐含了一个很强的假设：

$$
\text{source address}
\approx
\text{destination address}.
$$

也就是说：

> 我在哪里找到旧内容，就在哪里修改它。

对很多任务，这完全合理。

但对我们关心的一类记忆行为，它不够。

想象模型读到：

> “Alice currently lives in Paris.”

随后又获得：

> “Alice moved to Berlin.”

模型首先需要通过旧内容找到 **Alice / location** 这条关系，但新的表示未必应该严格沿原来的地址方向写回。尤其当 memory space 本身承担了关系组织、冲突消解或实体绑定时：

$$
\text{where I found it}
\neq
\text{where the corrected state should live}.
$$

这就是 **Transport** 出现的原因。

我们开始显式区分：

- $s_t$：**source**，从哪里预测旧实体；
- $d_t$：**destination**，残差最终写到哪里。

于是最基本的 substitution 不再是：

$$
s_t r_t^\top,
$$

而是：

$$
d_t r_t^\top.
$$

这看起来只是把左边的一个向量换掉了。

实际上，它改变了整个 memory geometry。

---

# 4. Oblique write：不是“移动地址”，而是在切空间里改变写入方向 {#oblique-write}

如果 $d_t$ 可以任意偏离 $s_t$，系统很快会变得难以控制。

我们希望 transport 有方向自由度，但又不想丢掉一个关键事实：

> 这次更新仍然是由 source $s_t$ 找到的那条旧记忆所触发的。

因此 ATPM 不直接预测一个任意的 $d_t$。

它先产生一个 transport proposal $b_t$，再把它投影到 $s_t$ 的切空间：

$$
\tau_t
=
(I - s_t s_t^\top)b_t.
$$

由于 $s_t$ 已归一化：

$$
s_t^\top \tau_t = 0.
$$

随后仅沿这个正交方向移动：

$$
\boxed{
d_t = s_t + \rho_t \tau_t
}
$$

其中：

$$
\rho_t \in (0,1)
$$

由每个 token、每个 head 自适应预测。

这立刻给出一个非常有用的不变量：

$$
s_t^\top d_t
=
s_t^\top s_t
+
\rho_t s_t^\top\tau_t
=
1.
$$

因此：

$$
P_t = d_t s_t^\top
$$

满足：

$$
P_t^2
=
d_t(s_t^\top d_t)s_t^\top
=
d_t s_t^\top
=
P_t.
$$

也就是说，$d_ts_t^\top$ 是一个 **oblique projector**。

<div :class="$style.statement">
  <span>Geometric interpretation</span>
  <p>
    ATPM 没有把 source address “扔掉再重写”。<br/>
    它保留 source 的约束，同时允许更新沿其 null / tangent space 偏转。
  </p>
</div>

这也是为什么我们更愿意叫它 **transport**，而不是简单的 write offset。

---

# 5. Transport 从哪里来：让 K 与 V 共同决定“偏转方向” {#bilinear-transport}

接下来又出现一个设计问题：

> 谁来决定 $\tau_t$？

如果再加一个独立 routing network，模型当然能学，但整个结构又开始像“外挂控制器”。

最终 ATPM-v2 使用 entity 自己的 K/V 两个固定坐标块构造 transport。

先做无仿射 RMS normalization：

$$
\hat k_t = \operatorname{RMS0}(k_t),
\qquad
\hat v_t = \operatorname{RMS0}(v_t).
$$

映射到一个低秩 transport latent：

$$
u_t^K = A_K \hat k_t,
\qquad
u_t^V = A_V \hat v_t.
$$

做逐元素的双线性交互：

$$
z_t
=
u_t^K \odot u_t^V.
$$

再投回 address space：

$$
c_t
=
\frac{Cz_t}{\sqrt{R}},
$$

其中 $R$ 是 transport latent rank。

为了不让 proposal 的范数失控，我们不做硬单位归一化，而是压到 soft sphere：

$$
b_t
=
\frac{c_t}
{\sqrt{1+\|c_t\|^2}}.
$$

于是：

$$
\|b_t\| < 1.
$$

最后：

$$
\tau_t
=
(I-s_ts_t^\top)b_t,
\qquad
d_t
=
s_t+\rho_t\tau_t.
$$

<div :class="$style.twoCol">
  <div>
    <h3>为什么不是 hard normalize？</h3>
    <p>
      当 K/V binding 很弱时，强行把一个接近 0 的向量归一化到单位球面，
      会把“低置信度”变成“高幅度随机方向”。
      soft sphere 保留了 proposal 自己的置信强度。
    </p>
  </div>
  <div>
    <h3>为什么是 bilinear K×V？</h3>
    <p>
      Transport 不是只由“地址”或只由“内容”决定。
      它来自同一 entity 的两个坐标视图之间的交互：
      <strong>什么东西</strong>与<strong>它当前表达了什么</strong>共同决定写入偏转。
    </p>
  </div>
</div>

这里的 `transport_rank = R` 只是这个双线性映射的内部低秩维度。

它不是一个行为 gate，也不是给不同 head 手工分配 transport 配额的超参数。

早期版本中我们尝试过全局 transport budget、per-head softmax 与额外的 $r_h$。最后这些都被删掉了。

最终式子回到了：

$$
\boxed{
d_t=s_t+\rho_t\tau_t
}
$$

没有额外的 head budget。

这是 ATPM 发展过程中一次很重要的“做减法”。

---

# 6. 第二个坐标：写到哪里，与怎么读回来，不应该是同一件事 {#proximal-recall}

有了 transport 之后，一个新的不对称出现了。

我们已经允许：

$$
s_t \neq d_t.
$$

但外部读取的 query $q_t^0$ 仍然可以完全自由。

于是模型可能成功地把状态写向一个新的 destination，却仍然用一个与该 destination 几乎无关的 query 去观察它。

最直接的方法，是让 query 直接等于 $d_t$。

但这又太强：它会把内容驱动的自由检索全部抹掉。

于是 ATPM 引入第二个连续坐标：

$$
\lambda_t\in(0,1).
$$

先定义 destination anchor：

$$
a_t
=
\frac{d_t}{\|d_t\|}.
$$

然后只修正 query 在 $a_t$ 方向上的 residual：

$$
\boxed{
q_t
=
q_t^0
+
\lambda_t
\left(
1-(q_t^0)^\top a_t
\right)a_t
}
$$

这条式子的好处是，它有一个极其干净的 residual law：

$$
1-q_t^\top a_t
=
(1-\lambda_t)
\left(
1-(q_t^0)^\top a_t
\right).
$$

因此：

- $\lambda_t=0$：保持自由 query；
- $0<\lambda_t<1$：只纠正一部分 query-anchor mismatch；
- $\lambda_t=1$：精确满足 $q_t^\top a_t=1$。

这里的 **Proximal** 不是指“再加一个相似度 loss”。

它表示：**读取不是被硬切换到 destination，而是沿最小的锚点方向修正逐渐靠近它。**

---

# 7. 两个坐标，四个极限：ATPM 的动态地图 {#atlas}

下面这张图不是四个离散模式。

拖动 $\lambda$ 与 $\rho$，你看到的是同一条动力学在二维控制空间里的不同区域。

<div :class="$style.atlasShell">
  <div :class="$style.atlasControls">
    <div :class="$style.controlRow">
      <div>
        <span>Proximal recall</span>
        <b>λ = {{ lambda.toFixed(2) }}</b>
      </div>
      <input
        v-model.number="lambda"
        type="range"
        min="0"
        max="1"
        step="0.01"
        aria-label="lambda proximal recall"
      />
      <small>query-anchor residual remains {{ queryResidual }}%</small>
    </div>
    <div :class="$style.controlRow">
      <div>
        <span>Directed transport</span>
        <b>ρ = {{ rho.toFixed(2) }}</b>
      </div>
      <input
        v-model.number="rho"
        type="range"
        min="0"
        max="1"
        step="0.01"
        aria-label="rho directed transport"
      />
      <small>transport coordinate {{ transportStrength }}%</small>
    </div>
  </div>
  <div :class="$style.atlasMain">
    <div :class="$style.quadrant">
      <div :class="[$style.qCell, $style.qTL]">
        <small>λ ↑ · ρ ↓</small>
        <b>Stable Revision</b>
        <span>原址修订</span>
      </div>
      <div :class="[$style.qCell, $style.qTR]">
        <small>λ ↑ · ρ ↑</small>
        <b>Directed Rewrite</b>
        <span>定向重写</span>
      </div>
      <div :class="[$style.qCell, $style.qBL]">
        <small>λ ↓ · ρ ↓</small>
        <b>Local Update</b>
        <span>GDN-like endpoint</span>
      </div>
      <div :class="[$style.qCell, $style.qBR]">
        <small>λ ↓ · ρ ↑</small>
        <b>Directed Update</b>
        <span>自由检索 · 有向写入</span>
      </div>
      <div :class="$style.axisY">λ · recall constraint</div>
      <div :class="$style.axisX">ρ · transport →</div>
      <div :class="$style.cursor" :style="cursorStyle">
        <span></span>
      </div>
    </div>
    <aside :class="$style.atlasReadout">
      <span :class="$style.readoutCode">{{ atlas.code }}</span>
      <small>{{ atlas.tag }}</small>
      <h3>{{ atlas.name }}</h3>
      <b>{{ atlas.en }}</b>
      <p>{{ atlas.copy }}</p>
      <div>{{ atlas.family }}</div>
    </aside>
  </div>
</div>

## 四个端点的形式化解释

| $\lambda$ | $\rho$ | 查询 | 写入 | 极限行为 |
|---:|---:|---|---|---|
| $1$ | $1$ | 地址约束查询 | 有向写入 | RCQP / CrossScan-like 精确召回端 |
| $0$ | $1$ | 自由查询 | 有向写入 | 内容反查 + directed memory |
| $1$ | $0$ | 地址约束查询 | 对称写入 | 稳定原址替换 / revision |
| $0$ | $0$ | 自由查询 | 对称写入 | GDN-like 局部 delta endpoint |

::: tip 一个重要的澄清
**这张四象限图不是 4R 的一一映射。**

$\lambda$ 与 $\rho$ 控制的是 **observation geometry** 和 **destination geometry**。

真正的 Remember / Revise / Rewrite 还同时受到 $\alpha_t$、$\beta_t^K$、$\beta_t^V$ 和 residual $r_t$ 的影响。  
ATPM 的目标恰恰不是把 4R 重新编码成四个手工 mode，而是让它们从一组连续坐标共同涌现。
:::

---

# 8. 到这里，4R 才真正闭合 {#four-r-closed}

现在可以重新回到最初的问题。

## Read

外部读取仍然只有一次：

$$
y_t = E_t^\top q_t.
$$

$q_t$ 可以保持内容驱动，也可以由 $\lambda_t$ 向 destination anchor 做 proximal correction。

## Remember

如果没有必要更新：

$$
\alpha_t \rightarrow 1,
\qquad
\beta_t^K,\beta_t^V \rightarrow 0,
$$

状态自然延续。

没有 `remember()` 分支。

## Revise

如果新实体与旧预测接近：

$$
\|r_t\|\ll 1,
$$

或者 substitution strength 较小：

$$
0<\beta_t^{K,V}\ll 1,
$$

同一条 recurrence 就表现为局部修订。

如果 $\rho_t\rightarrow 0$，这种修订还会稳定发生在原地址附近。

## Rewrite

如果 residual 大、substitution 强，同时 $\rho_t$ 打开：

$$
\|r_t\| \uparrow,
\qquad
\beta_t \uparrow,
\qquad
\rho_t \uparrow,
$$

模型可以沿新的 destination direction 做强替换，而不是被限制为原地平均。

<div :class="$style.bigQuote">
  <p>
    4R 最后没有变成四个函数。<br/>
    它们变成了一个状态方程里的不同时间尺度、不同残差幅度与不同几何区域。
  </p>
</div>

---

# 9. 把 ATPM 压缩成六步 {#six-steps}

如果必须把整个模块压缩到一张白板上，我们现在会这样写。

<div :class="$style.equationExplorer">
  <div :class="$style.stepRail">
    <button
      v-for="step in equationSteps"
      :key="step.n"
      :class="[$style.stepButton, equationStep === Number(step.n) && $style.stepActive]"
      @click="equationStep = Number(step.n)"
    >
      <small>{{ step.n }}</small>
      <span>{{ step.title }}</span>
    </button>
  </div>

  <div :class="$style.stepStage">
    <small>STEP {{ activeEquation.n }}</small>
    <h3>{{ activeEquation.title }}</h3>
    <div :class="$style.liveFormula">\({{ activeEquation.formula }}\)</div>
    <p>{{ activeEquation.copy }}</p>
  </div>
</div>

完整形式为：

$$
\begin{aligned}
\bar E_t &= \alpha_t E_{t-1}, \\[4pt]
r_t &= e_t-\bar E_t^\top s_t, \\[4pt]
\Omega_t &= \beta_t^K\Pi_K+\beta_t^V\Pi_V, \\[4pt]
z_t &= (A_K\hat k_t)\odot(A_V\hat v_t), \\[4pt]
b_t &= \frac{Cz_t/\sqrt R}{\sqrt{1+\|Cz_t/\sqrt R\|^2}}, \\[4pt]
\tau_t &= (I-s_ts_t^\top)b_t, \\[4pt]
d_t &= s_t+\rho_t\tau_t, \\[4pt]
E_t &= \bar E_t+d_t(\Omega_t r_t)^\top, \\[4pt]
a_t &= \frac{d_t}{\|d_t\|}, \\[4pt]
q_t &= q_t^0+\lambda_t(1-(q_t^0)^\top a_t)a_t, \\[4pt]
y_t &= E_t^\top q_t.
\end{aligned}
$$

其中控制量：

$$
\alpha_t,\;
\beta_t^K,\;
\beta_t^V,\;
\rho_t,\;
\lambda_t
$$

全部由当前 token / hidden state 自适应产生。

<div :class="$style.invariantGrid">
  <div>
    <small>INVARIANT 01</small>
    <b>$s_t^\top d_t=1$</b>
    <p>transport 不破坏 source 对 update 的约束。</p>
  </div>
  <div>
    <small>INVARIANT 02</small>
    <b>$(d_ts_t^\top)^2=d_ts_t^\top$</b>
    <p>左侧 transport operator 是 oblique projector。</p>
  </div>
  <div>
    <small>LAW 03</small>
    <b>$\epsilon_q'=(1-\lambda)\epsilon_q$</b>
    <p>proximal recall residual 有精确的一阶收缩律。</p>
  </div>
</div>

---

# 10. 它仍然必须是一台“能训练的机器” {#parallelism}

到这里，ATPM 很容易变成一个漂亮但没法训练的递归系统。

因此有一个约束从 PSM 一直保留到了最终实现：

> **数学语义必须有 exact sequential reference，同时训练路径必须有等价的 chunk-parallel realization。**

单步 recurrence 可以写成：

$$
E_t
=
\alpha_tE_{t-1}
+
d_t
\left[
\Omega_t
\left(
e_t-\alpha_tE_{t-1}^\top s_t
\right)
\right]^\top.
$$

它仍然属于带 rank-1 / block-substitution 结构的线性状态更新。

实际实现保留：

- exact sequential reference，用来验证语义与数值；
- exact chunk-WY scan，用来做并行训练；
- 单个联合状态，而不是为 K/V 分别维护两套完整 memory；
- 每个 token 对外只产生一次 memory read；
- state 可以持续带到下一个 chunk / generation step。

<div :class="$style.flow">
  <div>
    <small>token $x_t$</small>
    <b>Projection</b>
    <span>$q^0,s,e,\alpha,\beta$</span>
  </div>
  <i>→</i>
  <div>
    <small>entity geometry</small>
    <b>Transport</b>
    <span>$K\times V\rightarrow\tau\rightarrow d$</span>
  </div>
  <i>→</i>
  <div>
    <small>persistent state</small>
    <b>Substitute</b>
    <span>$E_{t-1}\rightarrow E_t$</span>
  </div>
  <i>→</i>
  <div>
    <small>observation</small>
    <b>Proximal Recall</b>
    <span>$q^0\rightarrow q\rightarrow y_t$</span>
  </div>
</div>

::: details 关于 read-after-write
当前 ATPM-v2 的参考实现采用 **write-then-read / read-after-write** 语义：

1. 用当前 token 构造 source、destination 与 entity；
2. 更新 $E_{t-1}\rightarrow E_t$；
3. 当前 token 的外部 memory read 从更新后的 $E_t$ 中产生。

这使当前 observation 能立即看到本步 substitution 的结果。  
如果未来实验需要严格的 read-before-write causal memory，也可以把 observation 时序作为独立设计轴研究；它不是 ATPM 几何本身的必要条件。
:::

---

# 11. 为什么最终版反而比中间版本更简单 {#simplification}

ATPM 的开发过程里有过一个危险阶段：

每当某个任务表现不好，就很容易再加一个坐标。

我们曾经考虑或实现过：

- fixed rewrite radius；
- per-head transport radius $r_h$；
- global transport budget；
- head-wise softmax allocation；
- transport softness；
- 额外 routing / mode 参数；
- 显式 rewrite scale。

它们都“有道理”。

但放在一起以后，ATPM 开始失去最初最重要的东西：

> 一个自然、连续、可以解释的 memory dynamics。

因此最终版做了一个反方向的决定。

<div :class="$style.beforeAfter">
  <div>
    <small>INTERMEDIATE</small>
    <h3>分配 transport</h3>
    <p>$d=s+\rho\,r_h\,\tau$</p>
    <span>global budget → head softmax → radius → token gate</span>
  </div>
  <div :class="$style.after">
    <small>FINAL</small>
    <h3>让 token 自己决定</h3>
    <p>$d=s+\rho\tau$</p>
    <span>one token/head coordinate · no global allocation</span>
  </div>
</div>

最终的 $\rho$ 与 $\lambda$ 投影都从 **0 logit** 初始化：

$$
\rho_0=\lambda_0=0.5.
$$

这不是把模型预设到某个极端。

它从二维动力空间的中间开始，让训练自己决定往哪边走。

---

# 12. 从合成记忆到真实语言建模 {#language-modeling}

一个 memory operator 在精心设计的 synthetic task 上工作，并不能说明它真的适合作为语言模型的一部分。

我们真正关心的下一道门槛是：

> **当 ATPM 被放进一个正常的、端到端训练的语言模型里，它还能不能学？**

目前我们完成的最大规模验证大约是：

<div :class="$style.scaleCard">
  <div>
    <small>MODEL SCALE</small>
    <strong>≈ 200M</strong>
    <span>parameters</span>
  </div>
  <div>
    <small>TRAINING DATA</small>
    <strong>≈ 20B</strong>
    <span>FineWeb tokens</span>
  </div>
  <div>
    <small>OBJECTIVE</small>
    <strong>LM</strong>
    <span>next-token prediction</span>
  </div>
  <div>
    <small>RESULT</small>
    <strong>✓</strong>
    <span>end-to-end trainable</span>
  </div>
</div>

这次实验对 ATPM 的意义不是“赢下 benchmark”。

它只回答一个更基础、也更重要的问题：

> 一个包含联合实体状态、K/V partial substitution、oblique transport、proximal recall 与 recurrent scan 的系统，到了真实语言建模规模，会不会因为优化、数值稳定性或动力学退化而直接失败？

至少在这个规模，我们观察到答案是：

**不会。**

ATPM 可以被端到端训练，并表现出正常的语言建模学习过程。

## Training traces

<div :class="$style.plotSlot">
  <div>
    <span>TRAINING CURVE SLOT</span>
    <h3>200M ATPM · FineWeb</h3>
    <p>
      在这里接入你的真实日志：train CE / validation CE / gradient norm / learning rate。
      第一版报告不要为了填满图表而生成任何模拟曲线。
    </p>
  </div>
  <code>&lt;TrainingCurve :runs="atpm200m" /&gt;</code>
</div>

::: warning 我们没有证明什么
目前的 200M / 20B run **不能**证明：

- ATPM 在 compute-matched 条件下优于 Transformer；
- ATPM 优于所有 DeltaNet / Gated DeltaNet / linear recurrent baselines；
- ATPM 已经具有更好的 scaling law；
- ATPM 在 1B、7B 或更大规模仍保持同样的性质；
- ATPM 的长期 state capacity 已经被充分刻画。

这些问题都应该留在开放问题里，而不是通过措辞绕过去。
:::

---

# 13. 我们认为已经学到的东西 {#what-we-learned}

即使不声称 SOTA，这条研究路径仍然留下了几个我们认为值得记录的结论。

## 13.1 Memory 更像动力学，而不是数据库

把 memory 想成一个 tensor cache 很自然：

$$
\text{write} \rightarrow M \rightarrow \text{read}.
$$

ATPM 更接近：

$$
\text{state}
\xrightarrow{\text{preserve / predict / correct / transport}}
\text{new state}.
$$

过去并不是被“存起来”。

过去持续参与对现在的预测，而新信息只以 residual 的形式改变它。

---

## 13.2 “从哪里读”与“往哪里写”是两个不同的问题

这是从 PSM 走到 ATPM 最关键的一步。

$$
s_t
\quad\text{asks}\quad
\text{where is the old relation?}
$$

而：

$$
d_t
\quad\text{asks}\quad
\text{where should the correction act?}
$$

两者相同，是一个重要特例。

但它不必是唯一情况。

---

## 13.3 K/V 分离不一定意味着两套 memory

我们最后保留的是：

$$
E=[K,V]
$$

而不是：

$$
(E^K,E^V).
$$

实体是统一的。

可塑性是分块的。

这让“Key 需要改，但 Value 应该保留”或者反过来的行为，可以发生在同一个 persistent object 上。

---

## 13.4 离散记忆动作可以来自连续坐标

ATPM 没有 `mode = REWRITE`。

它只有连续的：

$$
(\alpha,\beta_K,\beta_V,\rho,\lambda).
$$

但在不同区域中，我们仍然能看到非常不同的记忆行为。

这可能比“4R 本身”更重要：

> **行为类别不一定需要以离散类别存在于模型内部。**

---

# 14. ATPM 与它的几个边界情况 {#endpoints}

ATPM 不是为了让所有旧模型都消失。

相反，一个我们很在意的性质是：它应该拥有清晰的退化端点。

<div :class="$style.endpointList">
  <div>
    <span>ρ → 0</span>
    <p><strong>Transport 消失。</strong> destination 回到 source，写入重新变成对称的局部 substitution。</p>
  </div>
  <div>
    <span>λ → 0</span>
    <p><strong>Proximal recall 消失。</strong> query 保持其原本的内容驱动几何。</p>
  </div>
  <div>
    <span>βK = βV</span>
    <p><strong>K/V polarization 消失。</strong> 整个 entity 以同一强度更新。</p>
  </div>
  <div>
    <span>ρ → 0 · λ → 0 · βK = βV</span>
    <p><strong>走向 Gated DeltaNet-like endpoint。</strong> ATPM 的额外几何自由度全部关闭。</p>
  </div>
</div>

这件事对研究很有帮助。

它意味着 ATPM 更像是在一个已有、可理解的 memory dynamics 上增加了两个连续自由度，而不是另起一套无法比较的计算图。

---

# 15. 还不知道的事情，比已经知道的更多 {#open-questions}

这份报告是 ATPM 的出生记录，不是结案报告。

下一阶段真正值得回答的问题包括：

<div :class="$style.questionGrid">
  <article>
    <small>01 · SCALE</small>
    <h3>它会继续 scaling 吗？</h3>
    <p>200M 只是第一个真实门槛。1B 以上的 optimization 与 state capacity 仍然未知。</p>
  </article>

  <article>
    <small>02 · MECHANISM</small>
    <h3>ρ 与 λ 到底学出了什么？</h3>
    <p>平均值不够。更有意思的是 token、层、head、语义事件上的 trajectory 与 phase portrait。</p>
  </article>

  <article>
    <small>03 · CAPACITY</small>
    <h3>固定状态最终会忘掉什么？</h3>
    <p>ATPM 可以 revise，但 persistent state 的信息容量仍然有限。何时发生覆盖与干扰需要单独刻画。</p>
  </article>

  <article>
    <small>04 · ONLINE LEARNING</small>
    <h3>Memory 能不能继续“变成知识”？</h3>
    <p>如果生成时的持续状态进一步承担 latent learning，它可能连接到更广义的 test-time / online adaptation。</p>
  </article>

  <article>
    <small>05 · TRANSFER</small>
    <h3>记忆能独立于模型存在吗？</h3>
    <p>联合实体状态是否能在模型之间迁移，是比“更长上下文”更大胆也更长期的问题。</p>
  </article>

  <article>
    <small>06 · KERNEL</small>
    <h3>理论结构能否变成更快的 kernel？</h3>
    <p>exact chunk-WY 证明了可并行性，但工程上的吞吐、显存与硬件友好度仍有很大优化空间。</p>
  </article>
</div>

---

# 16. 结语：我们最后没有得到四个按钮 {#closing}

研究开始时，我们想要的是：

$$
\text{Read}
\quad
\text{Remember}
\quad
\text{Revise}
\quad
\text{Rewrite}.
$$

一种很自然的做法，是给每件事设计一个机制。

最后我们走到了相反的地方。

ATPM 只维护一个持续状态：

$$
E_t.
$$

只有一条 substitution recurrence：

$$
E_t
=
\alpha_tE_{t-1}
+
d_t
\left[
\Omega_t
\left(
e_t-\alpha_tE_{t-1}^\top s_t
\right)
\right]^\top.
$$

只是允许它拥有几个有明确几何含义的连续坐标：

$$
\alpha_t,\;
\beta_t^K,\;
\beta_t^V,\;
\rho_t,\;
\lambda_t.
$$

<div :class="$style.closingCard">
  <small>ATPM · ADAPTIVE TRANSPORT–PROXIMAL MEMORY</small>
  <p>
    记忆不是“把过去放进一个矩阵”。<br/>
    它是一个系统持续决定：
    <strong>什么应该留下，什么应该被修正，修正发生在哪里，以及之后应该怎样重新读回它。</strong>
  </p>
</div>

我们现在已经知道，这套动力学不只存在于白板上。

它能够进入真实语言模型，并至少在约 200M 参数、约 20B FineWeb tokens 的尺度上完成训练。

接下来还剩很多不知道的事情。

这很好。

因为 ATPM 一开始就不是为了给“记忆”下一个最终定义。

它只是试图让这个问题变得更具体一点：

> **如果模型真的拥有持续的内部状态，那么“改变自己的过去”究竟应该是一种什么样的计算？**

---

# Appendix A · Symbols {#symbols}

| Symbol | Meaning |
|---|---|
| $E_t$ | per-head joint persistent entity state, $S\times(d_k+d_v)$ |
| $e_t=[k_t;v_t]$ | current entity written into memory |
| $s_t$ | normalized source address |
| $d_t$ | transport-aware destination address |
| $q_t^0$ | unconstrained external recall query |
| $q_t$ | proximal-corrected recall query |
| $\alpha_t$ | state retention / decay coordinate |
| $\beta_t^K,\beta_t^V$ | independent K/V substitution strengths |
| $\Pi_K,\Pi_V$ | fixed K/V coordinate projectors |
| $\rho_t$ | adaptive directed-transport coordinate |
| $\lambda_t$ | adaptive proximal-recall coordinate |
| $\tau_t$ | source-orthogonal transport tangent |
| $R$ | low-rank bilinear transport latent dimension |

# Appendix B · Implementation invariants worth testing {#implementation-checks}

如果你复现 ATPM，比对最终 loss 之前，先检查这些结构性不变量：

```text
1. source s must be unit-normalized
2. tau must be orthogonal to s
3. sᵀ d ≈ 1
4. ||b|| < 1 because of the soft-sphere map
5. rho, lambda ∈ (0, 1)
6. lambda residual law:
      1 - qᵀa = (1 - lambda)(1 - q0ᵀa)
7. sequential reference ≈ chunk-WY parallel path
8. K/V are fixed slices of one entity state, not two independent memories
9. rho/lambda controllers begin from the neutral 0.5 point
10. no global per-head transport budget is required in the final geometry
```

# Appendix C · Suggested evidence for the public release {#release-checklist}

这不是“还要重新训练一堆模型”的清单。

尽量只从已经存在的 checkpoint / log 中抽取：

- [ ] 200M run 的 train loss 曲线
- [ ] validation loss / PPL（如果已有）
- [ ] learning rate 与 gradient norm
- [ ] $\rho$ 的 layer/head 分布
- [ ] $\lambda$ 的 layer/head 分布
- [ ] $\beta_K-\beta_V$ 的 polarization 分布
- [ ] source-destination cosine / displacement
- [ ] sequential vs parallel numerical error
- [ ] 1–2 个最能展示 revise / rewrite 的 synthetic case
- [ ] 参数量、state size、训练 token 数与训练配置表

**没有现成数据的项，不为了报告而补跑。**

第一份 ATPM report 的任务是把架构、几何、已完成的可行性证据和开放问题说清楚。

<style module>
.hero {
  position: relative;
  overflow: hidden;
  margin: 1rem 0 1.5rem;
  padding: clamp(2rem, 6vw, 5rem);
  border: 1px solid var(--vp-c-divider);
  border-radius: 30px;
  background:
    radial-gradient(circle at 88% 12%, rgba(98, 196, 168, .28), transparent 24%),
    radial-gradient(circle at 72% 78%, rgba(114, 154, 232, .24), transparent 27%),
    radial-gradient(circle at 16% 88%, rgba(247, 179, 85, .28), transparent 28%),
    var(--vp-c-bg-soft);
}

.hero::after {
  content: '';
  position: absolute;
  width: 220px;
  height: 220px;
  right: -64px;
  bottom: -96px;
  border: 2px solid rgba(34, 34, 34, .18);
  border-radius: 48% 52% 62% 38% / 44% 36% 64% 56%;
  transform: rotate(-12deg);
}

.eyebrow {
  margin-bottom: 1.25rem;
  font-size: .72rem;
  font-weight: 750;
  letter-spacing: .14em;
  color: var(--vp-c-text-2);
}

.heroTitle {
  max-width: 900px;
  margin: 0 !important;
  border: 0 !important;
  font-size: clamp(2.8rem, 7vw, 6.4rem) !important;
  line-height: .96 !important;
  letter-spacing: -.055em;
}

.heroAccent {
  display: block;
  margin-top: .25em;
  font-size: .48em;
  font-weight: 540;
  letter-spacing: -.035em;
  color: var(--vp-c-text-2);
}

.heroLead {
  max-width: 760px;
  margin: 2rem 0 0;
  font-size: clamp(1.05rem, 1.8vw, 1.3rem);
  line-height: 1.8;
  color: var(--vp-c-text-2);
}

.heroMeta {
  display: flex;
  flex-wrap: wrap;
  gap: .55rem;
  margin-top: 2rem;
}

.heroMeta span {
  padding: .4rem .7rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  background: color-mix(in srgb, var(--vp-c-bg) 78%, transparent);
  font-size: .74rem;
  color: var(--vp-c-text-2);
}

.statusStrip {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1px;
  overflow: hidden;
  margin: 1.5rem 0 3rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 18px;
  background: var(--vp-c-divider);
}

.statusStrip > div {
  display: flex;
  min-height: 112px;
  padding: 1.15rem;
  flex-direction: column;
  justify-content: space-between;
  background: var(--vp-c-bg);
}

.statusStrip b {
  font-size: 1.65rem;
  letter-spacing: -.04em;
}

.statusStrip span {
  font-size: .76rem;
  color: var(--vp-c-text-2);
}

.fourR {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin: 1.7rem 0 2.2rem;
}

.fourR article {
  min-height: 190px;
  padding: 1.3rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 20px;
  background: var(--vp-c-bg-soft);
}

.fourR article:nth-child(1) {
  background:
    radial-gradient(circle at 100% 0, rgba(112, 159, 236, .20), transparent 45%),
    var(--vp-c-bg-soft);
}

.fourR article:nth-child(2) {
  background:
    radial-gradient(circle at 100% 0, rgba(100, 194, 154, .20), transparent 45%),
    var(--vp-c-bg-soft);
}

.fourR article:nth-child(3) {
  background:
    radial-gradient(circle at 100% 0, rgba(246, 175, 78, .22), transparent 45%),
    var(--vp-c-bg-soft);
}

.fourR article:nth-child(4) {
  background:
    radial-gradient(circle at 100% 0, rgba(181, 124, 226, .18), transparent 45%),
    var(--vp-c-bg-soft);
}

.fourR h3 {
  margin: 1rem 0 .5rem;
  font-size: 1.35rem;
}

.fourR p {
  margin: 0;
  color: var(--vp-c-text-2);
}

.rIndex {
  font: 700 .72rem/1 monospace;
  color: var(--vp-c-text-3);
}

.statement {
  margin: 2rem 0;
  padding: 1.5rem 1.7rem;
  border-left: 4px solid var(--vp-c-text-1);
  border-radius: 0 18px 18px 0;
  background: var(--vp-c-bg-soft);
}

.statement span {
  font-size: .7rem;
  font-weight: 760;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--vp-c-text-3);
}

.statement p {
  margin: .6rem 0 0;
  font-size: 1.18rem;
  line-height: 1.7;
}

.formulaCallout {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: .65rem;
  margin: 1.5rem 0 2.2rem;
}

.formulaCallout > div {
  padding: 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 16px;
  background: var(--vp-c-bg-soft);
}

.formulaCallout small {
  display: block;
  min-height: 2.2em;
  margin-bottom: .55rem;
  color: var(--vp-c-text-3);
}

.formulaCallout b {
  font-size: 1.05rem;
}

.twoCol {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin: 1.5rem 0 2rem;
}

.twoCol > div {
  padding: 1.35rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 18px;
}

.twoCol h3 {
  margin: 0 0 .6rem;
}

.twoCol p {
  margin: 0;
  color: var(--vp-c-text-2);
}

.atlasShell {
  margin: 2rem 0 2.5rem;
  overflow: hidden;
  border: 1px solid var(--vp-c-divider);
  border-radius: 26px;
  background: var(--vp-c-bg-soft);
}

.atlasControls {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1px;
  border-bottom: 1px solid var(--vp-c-divider);
  background: var(--vp-c-divider);
}

.controlRow {
  padding: 1rem 1.2rem 1.15rem;
  background: var(--vp-c-bg);
}

.controlRow > div {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 1rem;
}

.controlRow span,
.controlRow small {
  color: var(--vp-c-text-2);
}

.controlRow b {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: .9rem;
}

.controlRow input {
  width: 100%;
  margin: .8rem 0 .3rem;
  accent-color: var(--vp-c-text-1);
}

.controlRow small {
  display: block;
  font-size: .7rem;
}

.atlasMain {
  display: grid;
  grid-template-columns: minmax(0, 1.4fr) minmax(240px, .6fr);
}

.quadrant {
  position: relative;
  display: grid;
  min-height: 520px;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  border-right: 1px solid var(--vp-c-divider);
}

.qCell {
  display: flex;
  padding: 1.2rem;
  flex-direction: column;
  justify-content: flex-end;
}

.qCell small {
  margin-bottom: .2rem;
  font: 650 .68rem/1.2 ui-monospace, SFMono-Regular, Menlo, monospace;
  color: rgba(20, 20, 20, .55);
}

.qCell b {
  font-size: 1.02rem;
  color: rgba(20, 20, 20, .88);
}

.qCell span {
  margin-top: .15rem;
  font-size: .75rem;
  color: rgba(20, 20, 20, .58);
}

.qTL {
  border-right: 1px dashed rgba(0, 0, 0, .12);
  border-bottom: 1px dashed rgba(0, 0, 0, .12);
  background: rgba(104, 184, 148, .52);
}

.qTR {
  border-bottom: 1px dashed rgba(0, 0, 0, .12);
  background: rgba(241, 166, 72, .55);
}

.qBL {
  border-right: 1px dashed rgba(0, 0, 0, .12);
  background: rgba(110, 158, 230, .48);
}

.qBR {
  background: rgba(178, 125, 221, .44);
}

.axisY,
.axisX {
  position: absolute;
  z-index: 2;
  padding: .25rem .4rem;
  border-radius: 6px;
  background: rgba(255,255,255,.72);
  color: rgba(0,0,0,.58);
  font: 650 .65rem/1 ui-monospace, SFMono-Regular, Menlo, monospace;
  pointer-events: none;
}

.axisY {
  top: 50%;
  left: .5rem;
  transform: rotate(-90deg) translateX(-50%);
  transform-origin: 0 0;
}

.axisX {
  right: .6rem;
  bottom: .5rem;
}

.cursor {
  position: absolute;
  z-index: 5;
  width: 22px;
  height: 22px;
  margin: -11px 0 0 -11px;
  border: 2px solid #111;
  border-radius: 50%;
  background: rgba(255,255,255,.9);
  box-shadow: 0 4px 18px rgba(0,0,0,.22);
  transition: left .12s ease, top .12s ease;
  pointer-events: none;
}

.cursor span {
  position: absolute;
  inset: 6px;
  border-radius: 50%;
  background: #111;
}

.atlasReadout {
  display: flex;
  padding: clamp(1.2rem, 3vw, 2rem);
  flex-direction: column;
  justify-content: center;
  background: var(--vp-c-bg);
}

.readoutCode {
  display: grid;
  width: 2.4rem;
  height: 2.4rem;
  place-items: center;
  margin-bottom: 1.4rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 50%;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
}

.atlasReadout > small {
  text-transform: uppercase;
  letter-spacing: .08em;
  color: var(--vp-c-text-3);
}

.atlasReadout h3 {
  margin: .45rem 0 .05rem;
  font-size: 1.45rem;
}

.atlasReadout > b {
  color: var(--vp-c-text-2);
}

.atlasReadout p {
  margin: 1.15rem 0;
  color: var(--vp-c-text-2);
}

.atlasReadout > div {
  width: fit-content;
  padding: .35rem .55rem;
  border-radius: 7px;
  background: var(--vp-c-bg-soft);
  font: 600 .7rem/1.2 ui-monospace, SFMono-Regular, Menlo, monospace;
  color: var(--vp-c-text-2);
}

.bigQuote {
  margin: 2.5rem 0;
  padding: clamp(1.5rem, 4vw, 3rem);
  border-radius: 24px;
  background:
    radial-gradient(circle at 15% 10%, rgba(248, 176, 77, .25), transparent 35%),
    radial-gradient(circle at 90% 90%, rgba(95, 179, 148, .22), transparent 35%),
    var(--vp-c-bg-soft);
}

.bigQuote p {
  margin: 0;
  font-size: clamp(1.35rem, 3vw, 2.1rem);
  font-weight: 620;
  line-height: 1.45;
  letter-spacing: -.025em;
}

.equationExplorer {
  display: grid;
  grid-template-columns: 230px 1fr;
  overflow: hidden;
  margin: 1.8rem 0 2.4rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 22px;
}

.stepRail {
  display: flex;
  padding: .55rem;
  flex-direction: column;
  gap: .25rem;
  border-right: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg-soft);
}

.stepButton {
  display: grid;
  grid-template-columns: 2.2rem 1fr;
  gap: .4rem;
  width: 100%;
  padding: .7rem;
  border: 0;
  border-radius: 10px;
  background: transparent;
  text-align: left;
  color: var(--vp-c-text-2);
  cursor: pointer;
}

.stepButton:hover {
  background: var(--vp-c-bg);
}

.stepButton small {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  color: var(--vp-c-text-3);
}

.stepActive {
  background: var(--vp-c-bg) !important;
  color: var(--vp-c-text-1);
  box-shadow: inset 0 0 0 1px var(--vp-c-divider);
}

.stepStage {
  display: flex;
  min-height: 360px;
  padding: clamp(1.5rem, 5vw, 3.5rem);
  flex-direction: column;
  justify-content: center;
  background:
    radial-gradient(circle at 90% 15%, rgba(105, 160, 230, .14), transparent 26%),
    var(--vp-c-bg);
}

.stepStage > small {
  letter-spacing: .12em;
  color: var(--vp-c-text-3);
}

.stepStage h3 {
  margin: .4rem 0 1.3rem;
  font-size: 1.7rem;
}

.liveFormula {
  overflow-x: auto;
  padding: 1rem 0;
  font-size: clamp(1.1rem, 2.5vw, 1.65rem);
}

.stepStage p {
  max-width: 600px;
  color: var(--vp-c-text-2);
}

.invariantGrid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: .8rem;
  margin: 1.5rem 0 2.2rem;
}

.invariantGrid > div {
  padding: 1.1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 16px;
}

.invariantGrid small {
  display: block;
  margin-bottom: .8rem;
  letter-spacing: .08em;
  color: var(--vp-c-text-3);
}

.invariantGrid b {
  display: block;
  font-size: 1.05rem;
}

.invariantGrid p {
  margin: .55rem 0 0;
  color: var(--vp-c-text-2);
}

.flow {
  display: grid;
  grid-template-columns: 1fr auto 1fr auto 1fr auto 1fr;
  align-items: stretch;
  gap: .55rem;
  margin: 1.6rem 0 2rem;
}

.flow > div {
  display: flex;
  min-width: 0;
  padding: 1rem;
  flex-direction: column;
  border: 1px solid var(--vp-c-divider);
  border-radius: 15px;
}

.flow small,
.flow span {
  color: var(--vp-c-text-3);
}

.flow b {
  margin: .35rem 0;
}

.flow i {
  align-self: center;
  color: var(--vp-c-text-3);
}

.beforeAfter {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin: 1.5rem 0 2.2rem;
}

.beforeAfter > div {
  padding: 1.4rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 18px;
}

.beforeAfter small {
  letter-spacing: .1em;
  color: var(--vp-c-text-3);
}

.beforeAfter h3 {
  margin: .4rem 0 .6rem;
}

.beforeAfter p {
  margin: 0 0 .5rem;
  font-size: 1.2rem;
}

.beforeAfter span {
  color: var(--vp-c-text-2);
}

.after {
  background:
    radial-gradient(circle at 100% 0, rgba(101, 191, 154, .20), transparent 42%),
    var(--vp-c-bg-soft);
}

.scaleCard {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1px;
  overflow: hidden;
  margin: 1.5rem 0 2rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 20px;
  background: var(--vp-c-divider);
}

.scaleCard > div {
  display: flex;
  min-height: 155px;
  padding: 1.1rem;
  flex-direction: column;
  justify-content: space-between;
  background: var(--vp-c-bg-soft);
}

.scaleCard small {
  letter-spacing: .08em;
  color: var(--vp-c-text-3);
}

.scaleCard strong {
  font-size: 2.1rem;
  letter-spacing: -.04em;
}

.scaleCard span {
  color: var(--vp-c-text-2);
}

.plotSlot {
  display: flex;
  min-height: 300px;
  margin: 1rem 0 2rem;
  padding: 1.4rem;
  align-items: center;
  justify-content: center;
  border: 1px dashed var(--vp-c-divider);
  border-radius: 20px;
  background:
    linear-gradient(to right, transparent 49.8%, var(--vp-c-divider) 50%, transparent 50.2%),
    linear-gradient(to bottom, transparent 49.8%, var(--vp-c-divider) 50%, transparent 50.2%),
    var(--vp-c-bg-soft);
  text-align: center;
}

.plotSlot > div {
  max-width: 540px;
  padding: 1rem;
  border-radius: 14px;
  background: color-mix(in srgb, var(--vp-c-bg) 92%, transparent);
}

.plotSlot > div span {
  font-size: .7rem;
  font-weight: 700;
  letter-spacing: .1em;
  color: var(--vp-c-text-3);
}

.plotSlot h3 {
  margin: .35rem 0;
}

.plotSlot p {
  margin: 0;
  color: var(--vp-c-text-2);
}

.plotSlot code {
  display: none;
}

.endpointList {
  margin: 1.4rem 0 2rem;
  border-top: 1px solid var(--vp-c-divider);
}

.endpointList > div {
  display: grid;
  grid-template-columns: 170px 1fr;
  gap: 1rem;
  padding: 1rem 0;
  border-bottom: 1px solid var(--vp-c-divider);
}

.endpointList span {
  font: 700 .82rem/1.5 ui-monospace, SFMono-Regular, Menlo, monospace;
}

.endpointList p {
  margin: 0;
  color: var(--vp-c-text-2);
}

.questionGrid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin: 1.5rem 0 2.4rem;
}

.questionGrid article {
  min-height: 180px;
  padding: 1.25rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 18px;
  background: var(--vp-c-bg-soft);
}

.questionGrid small {
  letter-spacing: .08em;
  color: var(--vp-c-text-3);
}

.questionGrid h3 {
  margin: .5rem 0 .55rem;
}

.questionGrid p {
  margin: 0;
  color: var(--vp-c-text-2);
}

.closingCard {
  margin: 2rem 0 3rem;
  padding: clamp(1.5rem, 5vw, 3.5rem);
  border: 1px solid var(--vp-c-divider);
  border-radius: 26px;
  background:
    radial-gradient(circle at 12% 20%, rgba(244, 173, 76, .26), transparent 32%),
    radial-gradient(circle at 88% 20%, rgba(104, 184, 148, .22), transparent 30%),
    radial-gradient(circle at 70% 92%, rgba(120, 158, 229, .20), transparent 28%),
    var(--vp-c-bg-soft);
}

.closingCard small {
  font-size: .7rem;
  font-weight: 700;
  letter-spacing: .12em;
  color: var(--vp-c-text-3);
}

.closingCard p {
  max-width: 820px;
  margin: 1.2rem 0 0;
  font-size: clamp(1.3rem, 3vw, 2rem);
  line-height: 1.55;
  letter-spacing: -.025em;
}

@media (max-width: 900px) {
  .statusStrip,
  .scaleCard {
    grid-template-columns: repeat(2, 1fr);
  }

  .formulaCallout,
  .invariantGrid {
    grid-template-columns: repeat(2, 1fr);
  }

  .atlasMain {
    grid-template-columns: 1fr;
  }

  .quadrant {
    min-height: 430px;
    border-right: 0;
    border-bottom: 1px solid var(--vp-c-divider);
  }

  .flow {
    grid-template-columns: 1fr;
  }

  .flow i {
    transform: rotate(90deg);
  }
}

@media (max-width: 680px) {
  .hero {
    padding: 1.6rem;
    border-radius: 22px;
  }

  .heroTitle {
    font-size: clamp(2.5rem, 15vw, 4rem) !important;
  }

  .fourR,
  .twoCol,
  .atlasControls,
  .beforeAfter,
  .questionGrid {
    grid-template-columns: 1fr;
  }

  .formulaCallout,
  .invariantGrid {
    grid-template-columns: 1fr;
  }

  .equationExplorer {
    grid-template-columns: 1fr;
  }

  .stepRail {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    border-right: 0;
    border-bottom: 1px solid var(--vp-c-divider);
  }

  .stepButton {
    grid-template-columns: 1fr;
  }

  .statusStrip,
  .scaleCard {
    grid-template-columns: 1fr 1fr;
  }

  .endpointList > div {
    grid-template-columns: 1fr;
    gap: .3rem;
  }

  .quadrant {
    min-height: 390px;
  }

  .qCell {
    padding: .75rem;
  }

  .qCell b {
    font-size: .85rem;
  }

  .qCell span {
    font-size: .68rem;
  }
}
</style>
