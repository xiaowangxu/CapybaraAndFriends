---
layout: article
title: 看到 Cordis，我想到了 Vue
description: 关于 DeepSeek Harness，可组合性，软件工程和 AGI
type: 随笔
topic: Frontend
date: 2026-08-14
author: SunWx
status: Published
---

DeepSeek Harness 背后的 Cordis 给自己提出了一个颇有理论色彩的目标：通过 **revertible effects**、**reactive coeffects** 和 **component calculus**，建立“时空可组合性（spatiotemporal composability）”。第一次读的时候，很容易产生一种 hallucination：我们是不是遇到了一种新的软件组件模型？

不过如果你恰好写过一点 Vue，尤其用过 `effectScope`（或者类似的signal/reactive系统），理解 Cordis 可以有一条轻松很多的路线。

# 从一个 `effectScope` 开始

Vue 里可以这样写：

```typescript
const services = reactive(new Map())
const scope = effectScope()

scope.run(() => {
  // effect
  watch(source, handler)

  // listener
  window.addEventListener("resize", onResize)

  // service
  services.set("foo", createService())

  // reactive dependency
  watchEffect((onCleanup) => {
    const foo = services.get("foo")
    if (!foo) return

    const child = effectScope()
    child.run(() => useService(foo))

    onCleanup(() => child.stop())
  })

  // arbitrary resource
  const timer = setInterval(work, 1000)

  // everything whose lifecycle is attached to this scope
  onScopeDispose(() => {
    window.removeEventListener("resize", onResize)
    services.delete("foo")
    clearInterval(timer)
  })
})

// unload plugin
scope.stop()
```

所以更准确地说，scope 管住了一组和自己生命周期绑定的东西：

```text
Scope
├── watcher
├── reactive effect
├── sub scope
├── reactive subscriptions
├── ...
└── cleanup
```

需要销毁这一整组逻辑的时候：

```typescript
scope.stop()
```

这些代码本身没什么特别。

如果我们对照着 Cordis 的 Plugin/Fiber，会发现虽然在复杂性和实现上会有差异，但表达的内涵是有一致性的：

```text
Plugin / Fiber
├── listeners
├── effects
├── service registrations
├── child plugins
└── disposers
```

插件被卸载，这些由它拥有的 runtime resource 随之清理。

于是运行中的 Cordis Plugin / Fiber，可以先用一个简略的方式理解：

$$
\boxed{Running\ Plugin/Fiber \approx Code + EffectScope + Context}
$$

当然，这只是一个理解模型，不是说 `effectScope()` 可以替代整个 Cordis，更不是说两边的实现结构是一一对应的。

## Effect

这就更熟悉了。

Cordis 允许一段 effect 在运行时返回 disposer。runtime 记住这个 disposer，等所属插件卸载的时候再执行。

如果从 Vue 的角度看，大概就是：

```typescript
scope.run(() => {
  acquireSomething()

  onScopeDispose(() => {
    releaseSomething()
  })
})
```

到了论文里，这叫 `Revertible Effect`

> 如果是前端工程师，可以感叹一下：哦，原来我们的 `clearInterval()` 已经离形式化软件理论这么近了。
> 当然，这样说多少有点刻薄。

论文真正做的是把这种 recovery / cleanup discipline 提升到一个统一的 context transformation 模型里，这本身可以是有价值的形式化。

但从实现直觉上说，我们确实仍然在处理那个非常古老的问题：

```text
创建了资源
↓
记得把它清掉
```

## Reactive Coeffect

Cordis 里我觉得比较有意思的一部分，是 service dependency。

假设组件 A 依赖一个 `llm` service。

很多启动期或者偏静态的 DI 模型，大致是在启动的时候：

```text
有 llm → 创建 A
没有 llm → 启动失败
```

Cordis 选择更进一步：如果运行过程中 `llm` provider 消失，A 可以被卸载；如果新的 provider 出现，A 又重新建立。

甚至 provider 从：`LLM_1` 换成 `LLM_2` consumer 也可以重新运行。

所以从这个角度，可以把它理解成在维护一个随时间变化的 dependency graph：

$$
G_t
$$


如果继续戴着 Vue 眼镜看，它可以变得非常直观：

```typescript
watchEffect((onCleanup) => {
  const llm = services.get("llm")
  const tools = services.get("tools")

  if (!llm || !tools) return

  const dispose = mountAgent({
    llm,
    tools,
  })

  onCleanup(dispose)
})
```

`llm` 变了？ effect 重新运行。

依赖没了？ cleanup。

新的 dependency 出现？重新 mount。

从这个角度看，它像是把 reactive programming 从“值的变化”推广到了“服务图的变化”。当然，如果把 service 也看成一种值，这个说法本身也没那么神秘。

至于这种动态性到底多适合 Agent Harness，我个人还是保留一点意见。


# 给 Vue 加一个 Service Registry

前面的 `effectScope` 已经解决了一个问题：**一段代码创建出来的资源，应该跟着这段代码的生命周期一起消失。**

但 Cordis 还有另一部分很重要：**Service**。

我们可以继续用 Vue 做这个思想实验。

先从最简单的全局 Registry 开始：

```typescript
const services = shallowReactive(
  new Map<string, unknown>()
)
```

注册一个 service：

```typescript
services.set("shell", shell)
```

然后其他代码读取它：

```typescript
const shell = services.get("shell")
```

如果希望 service registration 也属于当前 `effectScope`，很自然可以写一个 `provide()`：

```typescript
function provide(name, value) {
  services.set(name, value)

  onScopeDispose(() => {
    // 当前 scope 销毁时，
    // 顺便撤销它注册的 service。
    if (services.get(name) === value) {
      services.delete(name)
    }
  })
}
```

于是：

```typescript
scope.run(() => {
  provide("shell", createShell())
})
```

已经有了一点 Cordis 的味道：

```text
scope alive
    ↓
shell registered

scope.stop()
    ↓
shell unregistered
```

Service 不再只是一个全局变量，而开始拥有一个明确的 owner。

## 但一个全局 Map 很快就不够用了

假设 Harness 同时运行两个 Agent：

```text
Host
├── Agent A
└── Agent B
```

Agent A 使用自己的 sandbox：`shell A`，Agent B 使用另一个：`shell B`

如果只有：

```typescript
services.set("shell", ...)
```

那马上会遇到一个很传统的问题：`"shell"` 到底是哪一个？

一种简单但是丑陋的方法是开始发明名字：

```typescript
services.set("agent-a:shell", shellA)
services.set("agent-b:shell", shellB)
```

然后再把 `agentId` 一路传下去。这条路大家应该都比较熟悉，也通常意味着事情正在往不太优雅的方向发展。

另一种办法是：**让每个 Agent 有自己的 Service Context。**

## Service Context 本质上就是一层作用域

可以先写一个很小的 Context：

```typescript
function createContext(parent = null) {
  const services = shallowReactive(
    new Map()
  )

  return {
    parent,
    services,

    provide(name, value) {
      services.set(name, value)

      onScopeDispose(() => {
        if (services.get(name) === value) {
          services.delete(name)
        }
      })
    },

    inject(name) {
      // 当前 Context 有，就使用当前的。
      if (services.has(name)) {
        return services.get(name)
      }

      // 否则向父 Context 继续查找。
      return parent?.inject(name)
    },
  }
}
```

现在先创建 Host：

```typescript
const host = createContext()
```

Host 可以提供一些所有 Agent 都能看到的公共 service：

```typescript
host.provide("logger", logger)
host.provide("storage", storage)
```

然后分别给两个 Agent 创建 child context：

```typescript
const agentA = createContext(host)
const agentB = createContext(host)
```

再分别提供自己的 shell：

```typescript
agentA.provide("shell", shellA)
agentB.provide("shell", shellB)
```

于是整个 service topology 变成：

```text
Host Context
├── logger
├── storage
│
├── Agent A Context
│   └── shell → shellA
│
└── Agent B Context
    └── shell → shellB
```

现在：

```typescript
agentA.inject("shell")
// → shellA

agentB.inject("shell")
// → shellB
```

但：

```typescript
agentA.inject("logger")
// → host.logger

agentB.inject("logger")
// → host.logger
```

这就形成了一个非常普通的 **hierarchical service resolution**：

子 Context 可以继承父 Context 的 capability，同时用同名 service 覆盖它。

这和 Vue Component Tree 中 `provide / inject` 的“最近 Provider 优先”其实已经非常接近了。

这里只是为了把 service resolution 的直觉讲清楚。Cordis 实际的 Context / Fiber 关系当然比一棵简单的 parent Map 复杂得多，我不是在这里复刻它的实现。

如果觉得：`ctx.inject("shell")`太啰嗦，完全可以在 Context 外面再套一层 Proxy：

```typescript
function asServiceContext(ctx) {
  return new Proxy(ctx, {
    get(target, key) {
      if (key in target) {
        return target[key]
      }

      return target.inject(key)
    },
  })
}
```

于是：

```typescript
const ctxA = asServiceContext(agentA)
const ctxB = asServiceContext(agentB)
```

就可以直接访问了：

```typescript
ctxA.shell
ctxB.shell
```

# 关于软件工程

到目前为止，一切都很漂亮。

- 每个 effect 有 disposer。
- 每个 service 有 owner。
- 每个 dependency 可以 reactive。
- 每个 plugin 在生命周期层面可以比较干净地 mount 和 unmount。

如果软件世界停在这一层，我们可能真的已经接近 composability 的理想国了。

遗憾的是，软件工程从来不是这么美好的。

比如一个 plugin 做了：

```typescript
sendEmail()
```

另一个做了：

```typescript
POST("/payment")
```

第三个：

```typescript
gitPush()
```

这时候我们就会发现：

```typescript
return () => undoEverything()
```

多少有一点乐观。

一个 listener 可以 unregister，但它已经处理过的事件不会跟着 listener 一起从历史里消失。

所以一个很朴素、但很重要的区别是：

$$
\boxed{
Registration\ Reversibility
\neq
Behavior\ Reversibility
}
$$

Cordis 对 lifecycle-scoped effect 的撤销和清理处理得很整齐。

但 effect 已经对外部世界造成的结果能不能撤回，是另一回事。这个问题不会因为 runtime 记住了 disposer 就自动消失。

## 共享状态

假设插件 A：

$$
x:3\rightarrow4
$$

然后插件 B：

$$
x:4\rightarrow7
$$

现在 A 卸载。它的 disposer 如果非常忠诚地：$x \rightarrow 3$

我们并没有成功恢复世界，还顺手把 B 的修改一起干掉了。

这些问题很难仅靠一个统一的 Plugin abstraction 消除。

因为它们不是生命周期语法的问题，而是不同代码之间共享语义的问题。

## “Everything is Plugin”的陷阱

“Everything is Plugin” 这类表达确实很有吸引力。

但从很多大型软件系统的历史来看，统一通常有一个很有趣的规律。

一开始： **Everything is X**

所有东西终于拥有同一种抽象，架构图一下变得很干净。

然后现实问题开始出现：

> 有些 Plugin 是全局的，有些属于 session，有些属于 agent。

于是加入：`scope / lifetime / ownership`

接着：

> 两个 Plugin 都提供同一个 service 怎么办？

于是加入：`namespace / priority / shadowing / isolation`

然后：

> A 依赖 B，但只兼容某个版本；B 在运行时消失了又怎么办？

于是加入：`version / dependency constraints / readiness / reload semantics / failure propagation`

再往后，权限、迁移、超时、恢复、配置、可观测性...。

复杂性并没有因为所有东西都叫 Plugin 而消失。

它只是从：

$$
\boxed{\text{不同类型的组件}}
$$

搬到了：

$$
\boxed{\text{组件之间的协议}}
$$

或者换句话说：

> 当所有东西终于被统一成同一种抽象以后，我们往往还得再发明一整套系统，来解释这些“相同的东西”究竟有什么不同。

# 从 Vue 回到 Cordis

所以最后再回到最开始那个 `effectScope`。

```typescript
const scope = effectScope()

scope.run(() => {
  // code
})
```

我们已经可以相当自然地走到 Cordis 的核心模型。

至于这些机制是用工程语言描述成 lifecycle / reactive dependency，还是用：

- Revertible Effects
- Reactive Coeffects
- Spatiotemporal Composability

来描述，我觉得更像是两套观察语言。前者更接近日常实现，后者试图给它一套统一的语义。

软件工程师可能会继续写：

```typescript
onScopeDispose(cleanup)
```

然后突然发现，自己刚刚完成了一次 temporal composition。

# 关于自进化与 AGI

在一些讨论里，确实有人会进一步联想：**如果 Agent 能动态创建、替换甚至修改 Plugin，是不是就意味着它开始具备“自我进化”的基础？**

我对这个联想比较困惑，因为从工程上看，Cordis 解决的是一个很具体且传统的软件问题：**一段新代码如何被装入当前系统，并获得清晰的依赖、作用域和生命周期。**

## “能增加能力”是一件很古老的事

如果只把“运行时获得新能力”看成自进化，那么很多已有系统其实早就具备这种性质。

浏览器可以安装 Extension：

```text
Browser
├── Ad Blocker
├── Password Manager
└── Developer Tools
```

微信可以运行小程序：

```text
WeChat
├── Shopping
├── Maps
└── Games
```

操作系统更是如此：

```text
OS
├── Applications
├── Services
├── Drivers
└── Daemons
```

Agent 把一段代码包装成 Cordis Plugin，和它写一个 Python 程序、启动一个进程、安装一个浏览器扩展，至少在“运行时获得外部新能力”这一层，属于同一类事情。

## AGI 真的需要建立在这样一个 Plugin Runtime 上吗？

假设一个足够强的 Agent 已经能够使用：

```text
Shell
Filesystem
Browser
Network
Programming Language
Package Manager
Process / Container
```

那么它实际上已经站在一个极其通用的软件环境上。
如果 Harness 本身不够用，理论上甚至可以直接修改 Harness。

所以从能力空间看，**通用计算环境**本身已经比某一种 Plugin API 更泛用。

Cordis 可以让这些能力更容易组织、加载、替换和回收，这很有工程价值。但“组织能力的方式变好了”和“智能本身的能力边界被扩展了”，我觉得还是两件事。

## 一个我个人很喜欢的 React 小玩笑

这里会让我想到 React Hooks 经常被提到的一个优点：**Hooks 可以帮助我们复用逻辑，但是xxx不行。（xxx一般是class component）**

我第一次看到类似表述时，脑子里冒出一句：**那函数是干什么用的？**

当然，这只是一个玩笑，也许有人会说我在虚空打靶，我在这道歉，并不是说 Hooks 没有意义。Hooks 解决的是**带 React 状态和生命周期的逻辑组合与复用**，普通函数并不能直接替代它。

真正容易混淆的，是把一种组织能力的方式，强调成了能力本身。

# 关于学术

形式化当然不是问题。

旧的工程经验被严格形式化，也完全可能产生很有价值的研究。反过来说，“这东西在 Vue 里也能找到类似物”，也并不能说明 Cordis 的形式化没有价值。

真正值得问的是：**形式化以后，我们多得到了什么？**

好的形式化往往能做到：

$$
Many\ Phenomena
\rightarrow
Few\ Irreducible\ Structures.
$$

也就是把很多看起来不同的现象映射到少数几个真正不可约的结构上，然后再推出一些只靠工程直觉不太容易得到的结论。

所以我对 Cordis 的保留，不是因为它的 primitive 看起来熟悉。熟悉完全没关系。

我更希望这套 **revertible effects / reactive coeffects / spatiotemporal composability** 最后能不能给出一些超出“自动生命周期和依赖管理”之外的东西。
