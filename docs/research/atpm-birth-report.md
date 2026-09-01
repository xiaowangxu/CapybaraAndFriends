---
layout: article
title: ATPM 从记忆操作到记忆动力学
description: |-
  Adaptive Transport–Proximal Memory 设计报告
  构建具有 Read、Remember、Revise、Rewrite 能力的连续神经记忆系统。
type: 研究
topic: Neural Architecture
date: 2026-09-01
author: Capybara & Friends
status: Published
---
> 本文记录 ATPM 的设计过程和现有实验。当前证据表明：**ATPM 可以作为语言模型中的持续状态模块训练，并已在约 200M 参数、约 20B FineWeb tokens 的规模上完成验证。**
>
> 本文不讨论更大规模的 scaling law，也不声称已经完成严格 compute-matched 的强基线比较。十亿参数以上的行为仍待验证。

ATPM（Adaptive Transport–Proximal Memory）从 **Read、Remember、Revise、Rewrite** 四种记忆行为出发，讨论一个具体问题：神经网络里的记忆，能否不只是被动保存过去的矩阵，而是一套可以持续修订的内部状态？

| 已完成规模 | 训练数据 | 持久状态 | 序列复杂度 |
|---|---|---|---|
| 约 200M 参数 | 约 20B FineWeb tokens | n 个联合 K/V 实体状态 state | $O(T)$ |

# 1. 一切从“四个 R”开始 {#four-r}

最初的问题并不是如何设计一种新的 linear attention，也不是先写下一条 recurrence 再寻找解释，而是：**如果把“记忆”当成一个真正的认知动作，它到底应该会做什么？**

我认为至少需要四种基本行为：
1. **Read**：从过去的状态中找到当前相关的内容。
2. **Remember**：没有新证据时，尽量保留已有状态。
3. **Revise**：新信息到来时，对已有内容做局部、连续的修正。
4. **Rewrite**：旧内容失效时，允许模型明确替换它，而不是一直做指数平均。

传统 recurrent memory 很容易写成：

$$
M_t = \gamma_t M_{t-1} + \Delta M_t.
$$

但如果所有动作都被压成一个 `gate × update`，模型很容易退化为保守的平均器：该保留时仍在写入，该重写时又改得不够。Read、Remember、Revise、Rewrite 在数学上没有真正分开，最后只剩下一条连续但含义有限的衰减曲线。

> **设计原则：** 不为 4R 分别增加四个 operator，而让它们成为同一个动力系统在不同区域里的行为。

这条原则也限制了模型复杂度：遇到问题时，不能简单地再加一个 gate。

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

| 控制量 | 作用 |
|---|---|
| $\alpha_t$ | 保留多少旧状态 |
| $r_t$ | 当前实体与旧预测相差多少 |
| $\beta_t^K,\beta_t^V$ | 实体的哪一部分需要修改 |
| $d_t$ | 残差写到哪里 |

**Remember** 不再需要一个叫 `remember_gate` 的东西。

当 $\alpha_t$ 高、而 $\beta_t$ 小时，旧状态自然留下来。

**Revise** 也不需要单独的 operator。

当 residual 小、substitution strength 温和时，更新天然就是局部修订。

**Rewrite** 则是同一条更新在更强 substitution 下的另一端。

不过，PSM 仍然没有回答写入地址的问题。

# 3. Source 与 destination：读到的地方不一定是写回的地方 {#source-destination}

绝大多数 delta-style memory 都隐含了一个假设：

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

形式上只是替换了左侧向量，但它把读取地址和写入地址分开了，因此改变了 memory geometry。

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

由此可以得到不变量：

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

> **几何解释：** ATPM 保留 source 的约束，同时允许更新沿其 null / tangent space 偏转。

这也是为什么我们更愿意叫它 **transport**，而不是简单的 write offset。

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

## 为什么不用 hard normalize？

当 K/V binding 很弱时，强行把接近 0 的向量归一化到单位球面，会把低置信度变成高幅度的随机方向。soft sphere 则保留 proposal 本身的置信强度。

## 为什么使用 bilinear K×V？

Transport 不应只由地址或内容中的一方决定。它来自同一 entity 的两个坐标视图之间的交互：**写入的对象**与**对象当前表达的内容**共同决定偏转方向。

这里的 `transport_rank = R` 只是这个双线性映射的内部低秩维度。

它不是一个行为 gate，也不是给不同 head 手工分配 transport 配额的超参数。

早期版本中我们尝试过全局 transport budget、per-head softmax 与额外的 $r_h$。最后这些都被删掉了。

最终式子回到了：

$$
\boxed{
d_t=s_t+\rho_t\tau_t
}
$$

最终版本不再需要额外的 head budget。

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

它对应以下 residual law：

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

# 7. 两个坐标，四个极限：ATPM 的动态地图 {#atlas}

$\lambda$ 与 $\rho$ 定义了一个二维控制空间。下面列出四个端点；它们是同一套动力学的极限情况，不是四个离散模式。

四个端点的形式化解释：

| 控制坐标 $(\lambda,\rho)$ | 查询几何 | 写入几何 | 对应端点 |
|:---:|---|---|---|
| $(1,1)$ | 地址约束 | 有向写入 | RCQP / CrossScan-like |
| $(0,1)$ | 自由查询 | 有向写入 | Directed memory |
| $(1,0)$ | 地址约束 | 对称写入 | Stable revision |
| $(0,0)$ | 自由查询 | 对称写入 | GDN-like |


> **这张四象限图不是 4R 的一一映射。**
> 
> $\lambda$ 与 $\rho$ 控制的是 **observation geometry** 和 **destination geometry**。
> 
> Remember / Revise / Rewrite 还同时受到 $\alpha_t$、$\beta_t^K$、$\beta_t^V$ 和 residual $r_t$ 的影响。4R 不是四个手工 mode，而是多组连续坐标共同作用的结果。


# 8. 4R 在状态方程中的对应关系 {#four-r-closed}

我进一步逐项说明 4R 的实现方式。

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

> 4R 没有被实现为四个函数，而是对应同一状态方程中的不同时间尺度、残差幅度和几何区域。

# 9. 把 ATPM 压缩成六步 {#six-steps}

整个模块可以整理为六步：

1. **Decay**：$\bar E_t = \alpha_t E_{t-1}$。先决定旧状态保留多少。
2. **Predict & compare**：$r_t = e_t - \bar E_t^\top s_t$。从源地址读出旧实体，只更新当前实体与旧预测的差。
3. **Polarize**：$\Omega_t = \beta^K_t\Pi_K + \beta^V_t\Pi_V$。Key 与 Value 属于同一实体，但可以使用不同的修订强度。
4. **Transport**：$d_t = s_t + \rho_t\tau_t$。分离“在哪里发现旧内容”和“在哪里写回新内容”。
5. **Substitute**：$E_t = \bar E_t + d_t(\Omega_t r_t)^\top$。通过一次外积完成局部、可极化、可定向的替换。
6. **Recall**：$q_t = q_t^0 + \lambda_t(1-(q_t^0)^\top a_t)a_t$。查询既可以保持自由，也可以被近端约束拉向更新后的锚点。

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

| 性质 | 形式 | 含义 |
|---|---|---|
| Transport invariant | $s_t^\top d_t=1$ | transport 不破坏 source 对 update 的约束 |
| Oblique projection | $(d_ts_t^\top)^2=d_ts_t^\top$ | 左侧 transport operator 是 oblique projector |
| Recall residual law | $\epsilon_q'=(1-\lambda)\epsilon_q$ | proximal recall residual 具有精确的一阶收缩律 |

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

训练路径可以概括为：

$$
x_t
\xrightarrow{\text{Projection}}
(q^0,s,e,\alpha,\beta)
\xrightarrow{\text{Transport}}
d
\xrightarrow{\text{Substitute}}
E_t
\xrightarrow{\text{Proximal Recall}}
y_t.
$$


> 当前 ATPM-v2 的参考实现采用 **write-then-read / read-after-write** 语义：
> 
> 1. 用当前 token 构造 source、destination 与 entity；
> 2. 更新 $E_{t-1}\rightarrow E_t$；
> 3. 当前 token 的外部 memory read 从更新后的 $E_t$ 中产生。
> 
> 这使当前 observation 能立即看到本步 substitution 的结果。  
> 如果未来实验需要严格的 read-before-write causal memory，也可以把 observation 时序作为独立设计轴研究；它不是 ATPM 几何本身的必要条件。

# 11. 从合成记忆到真实语言建模 {#language-modeling}

一个 memory operator 在精心设计的 synthetic task 上工作，并不能说明它真的适合作为语言模型的一部分。

目前我们完成的最大规模验证大约是：

| 模型规模 | 训练数据 | 目标 | 结果 |
|---|---|---|---|
| 约 200M 参数 | 约 20B FineWeb tokens | next-token prediction | 可端到端训练 |

这次实验不用于比较 benchmark，而是回答一个可行性问题：

> 一个包含联合实体状态、K/V partial substitution、oblique transport、proximal recall 与 recurrent scan 的系统，到了真实语言建模规模，会不会因为优化、数值稳定性或动力学退化而直接失败？

至少在这个规模，我们观察到答案是：**不会。**

ATPM 可以被端到端训练，并表现出正常的语言建模学习过程。

## Training traces

::: info 待补充：200M ATPM · FineWeb
这里应接入真实训练日志，包括 train CE、validation CE、gradient norm 和 learning rate。在数据准备好之前，不使用模拟曲线占位。
:::

::: warning 我们没有证明什么
目前的 200M / 20B run **不能**证明：

- ATPM 在 compute-matched 条件下优于 Transformer；
- ATPM 优于所有 DeltaNet / Gated DeltaNet / linear recurrent baselines；
- ATPM 已经具有更好的 scaling law；
- ATPM 在 1B、7B 或更大规模仍保持同样的性质；
- ATPM 的长期 state capacity 已经被充分刻画。

这些问题都应该留在开放问题里，而不是通过措辞绕过去。
:::

# 12. ATPM 与它的几个边界情况 {#endpoints}

ATPM 保留了清晰的退化端点，因此可以与已有 memory dynamics 直接比较。

| 边界条件 | 结果 |
|---|---|
| $\rho\rightarrow 0$ | Transport 消失，destination 回到 source，写入退化为对称的局部 substitution |
| $\lambda\rightarrow 0$ | Proximal recall 消失，query 保持原本的内容驱动几何 |
| $\beta_K=\beta_V$ | K/V polarization 消失，整个 entity 使用相同强度更新 |
| $\rho\rightarrow 0,\ \lambda\rightarrow 0,\ \beta_K=\beta_V$ | ATPM 的额外几何自由度全部关闭，走向 Gated DeltaNet-like endpoint |

这意味着 ATPM 是在已有 memory dynamics 上增加两个连续自由度，而不是另起一套无法比较的计算图。

# 13. 开放问题 {#open-questions}

下一阶段需要回答的问题包括：

1. **Scaling**：200M 只是第一个真实门槛。1B 以上的 optimization 与 state capacity 仍然未知。
2. **Mechanism**：$\rho$ 与 $\lambda$ 的平均值不足以解释行为，还需要观察 token、层、head 和语义事件上的 trajectory 与 phase portrait。
3. **Capacity**：ATPM 可以 revise，但 persistent state 的容量仍然有限。覆盖与干扰在什么条件下发生，需要单独刻画。
4. **Online learning**：如果生成时的持续状态进一步承担 latent learning，它可能连接到更广义的 test-time / online adaptation。
5. **Transfer**：联合实体状态能否在模型之间迁移，目前没有答案。
6. **Kernel**：exact chunk-WY 说明该结构可以并行，但吞吐、显存和硬件友好度仍有优化空间。

# 14. 结语 {#closing}

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

ATPM 没有为每种行为分别设计一个机制，而是只维护一个持续状态：

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

这条 recurrence 由几个具有明确几何含义的连续坐标控制：

$$
\alpha_t,\;
\beta_t^K,\;
\beta_t^V,\;
\rho_t,\;
\lambda_t.
$$

> 这里的记忆不是简单地“把过去放进一个矩阵”，而是持续决定：什么应该保留，什么需要修正，修正写到哪里，以及之后如何读回。

现有实验表明，这套动力学可以进入真实语言模型，并在约 200M 参数、约 20B FineWeb tokens 的尺度上完成训练。

这些结果还不足以给“记忆”下一个最终定义，但可以把问题收窄到更具体的计算形式：

> **如果模型真的拥有持续的内部状态，那么“改变自己的过去”究竟应该是一种什么样的计算？**

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

1. source $s$ must be unit-normalized
2. $\tau$ must be orthogonal to $s$
3. $s^T d ≈ 1$
4. $||b|| < 1$ because of the soft-sphere map
5. $\rho, \lambda ∈ (0, 1)$
6. lambda residual law: $1 - q^Ta = (1 - \lambda)(1 - q_0^Ta)$
7. sequential reference $≈$ chunk-WY parallel path
8. $\rho/\lambda$ controllers begin from the neutral 0.5 point