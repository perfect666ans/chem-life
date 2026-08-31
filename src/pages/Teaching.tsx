import { Atom, FlaskConical, Gamepad2, GraduationCap, Layers, MessagesSquare, Sparkles, Trophy } from 'lucide-react'

type Card = {
  tag: string
  name: string
  desc: string
  href?: string
  accent: string // tailwind classes for left border + tag text
}

type Section = {
  label: string
  title: string
  icon: typeof Atom
  tags: string[]
  cards: Card[]
  cols: 2 | 3 | 4
}

const sections: Section[] = [
  {
    label: 'STRUCTURE TOPICS',
    title: '结构专题',
    icon: Atom,
    tags: ['e⁻', 'sp³', 'NaCl'],
    cols: 4,
    cards: [
      {
        tag: 'VSEPR',
        name: 'VSEPR 分子构型',
        desc: '3D 实时渲染。包含杂化轨道理论、孤电子对斥力演示，支持 CH₄、NH₃、H₂O、CO₂、BF₃、乙烷、乙烯模型。',
        href: '/teaching/chem_lab1.1.html',
        accent: 'border-l-blue-500 text-blue-600',
      },
      {
        tag: 'CELL',
        name: '晶体结构深度分析',
        desc: '全品类晶胞模型。支持金属、离子、共价晶体，可进行晶胞切割、配位数分析及空间利用率计算。',
        href: '/teaching/chem_lab1.2.html',
        accent: 'border-l-violet-500 text-violet-600',
      },
      {
        tag: 'NaCl',
        name: '离子晶体晶胞专题',
        desc: '聚焦 NaCl、CsCl、ZnS、CaF₂ 等典型离子晶体，按专题切换晶胞模型，适合课堂演示与对比学习。',
        accent: 'border-l-sky-400 text-sky-500',
      },
      {
        tag: 'e⁻',
        name: '核外电子排布',
        desc: '动态探索核外电子排布规律，联动原子半径、价层轨道与电子得失变化，适合课堂演示与自主学习。',
        accent: 'border-l-amber-400 text-amber-500',
      },
    ],
  },
  {
    label: 'REVIEW',
    title: '复习板块',
    icon: GraduationCap,
    tags: ['记忆', '连胜', '复盘'],
    cols: 3,
    cards: [
      {
        tag: 'MAP',
        name: '知识球 · 知识地图',
        desc: '必修 + 选必的 3D 知识网络：概念点串成「前置→后续」学习路径，每点配预习卡与真题母题。',
        accent: 'border-l-sky-500 text-sky-600',
      },
      {
        tag: 'CARD',
        name: '化学闪卡复习',
        desc: '高中化学 10 章 440+ 闪卡：必修一二 + 选择性必修 1-3，追踪进度、识别薄弱环节、智能推荐复习。',
        accent: 'border-l-orange-500 text-orange-600',
      },
      {
        tag: 'TREE',
        name: '知识挑战树',
        desc: '549 个知识点组成技能树，答题解锁节点，XP 等级系统、连胜奖励与成就等你挑战。',
        accent: 'border-l-emerald-500 text-emerald-600',
      },
    ],
  },
  {
    label: 'ORGANIC CHEMISTRY',
    title: '有机化学',
    icon: FlaskConical,
    tags: ['≡键', 'R-OH', '醚化'],
    cols: 3,
    cards: [
      {
        tag: 'ORG',
        name: '有机反应机理库',
        desc: '动态反应过程。可视化展示断键成键位置，涵盖取代、加成、消去、酯化等核心考点。',
        accent: 'border-l-green-500 text-green-600',
      },
      {
        tag: 'IUPAC',
        name: '有机系统命名中心',
        desc: '烷、烯、炔、卤代烃、醇醛酸、酯、芳香族命名闯关和生成器工具收进同一界面。',
        accent: 'border-l-green-500 text-green-600',
      },
      {
        tag: 'ISO',
        name: '同分异构体闯关挑战',
        desc: '按烷烃、烯烃、芳香烃、卤代烃、醇醛酸酯分章闯关，自动同步章节进度。',
        accent: 'border-l-green-500 text-green-600',
      },
    ],
  },
  {
    label: 'REACTION PRINCIPLES',
    title: '化学反应原理',
    icon: Layers,
    tags: ['ΔH', 'K', 'e⁻'],
    cols: 4,
    cards: [
      {
        tag: 'ΔH',
        name: '化学反应的热效应',
        desc: '断键吸能、成键放能与盖斯定律。拖动键能看 ΔH 即时重算，把能量变化变成能上手的阶梯图。',
        accent: 'border-l-purple-500 text-purple-600',
      },
      {
        tag: 'v/K',
        name: '化学反应速率与平衡',
        desc: '有效碰撞与能垒、动态平衡沙盘，以及勒夏特列原理「减弱而非抵消」的可视化演示。',
        accent: 'border-l-purple-400 text-purple-500',
      },
      {
        tag: 'pH',
        name: '水溶液中的离子平衡',
        desc: '电离与水解的动态平衡、pH 对数标尺、中和滴定突跃曲线与沉淀溶解平衡。',
        accent: 'border-l-purple-400 text-purple-500',
      },
      {
        tag: '⚡',
        name: '化学反应与电能',
        desc: '原电池双向、电解池阴阳极判断、盐桥与离子迁移，以及金属腐蚀微电池。',
        accent: 'border-l-purple-400 text-purple-500',
      },
    ],
  },
  {
    label: 'GAMES',
    title: '游戏板块',
    icon: Gamepad2,
    tags: ['XP', 'Boss', 'Combo'],
    cols: 3,
    cards: [
      {
        tag: 'RPG',
        name: '元素纪元 RPG',
        desc: '沉浸式化学对战。捕捉元素精灵，利用氧化还原反应战斗，含知识问答。',
        accent: 'border-l-red-500 text-red-600',
      },
      {
        tag: 'TD',
        name: '元素防线：化学塔防',
        desc: '利用离子沉淀、酸碱中和与氧化还原反应布置防线，在攻防节奏中判断反应类型。',
        accent: 'border-l-cyan-500 text-cyan-600',
      },
      {
        tag: 'CBTI',
        name: 'CBTI 化学人格鉴定',
        desc: '你是 H₂S 还是 NaOH？16 道选择题对应物质类型，结果配角色卡。',
        accent: 'border-l-rose-500 text-rose-600',
      },
    ],
  },
]

const colsClass: Record<Section['cols'], string> = {
  2: 'sm:grid-cols-2',
  3: 'sm:grid-cols-2 lg:grid-cols-3',
  4: 'sm:grid-cols-2 lg:grid-cols-4',
}

export default function TeachingPage() {
  return (
    <main className="mx-auto max-w-6xl px-4 py-8">
      {/* 头部 */}
      <section className="rounded-xl border border-slate-200 border-t-2 border-t-red-500 bg-white p-6 sm:p-8">
        <h1 className="text-3xl font-light leading-tight text-slate-900 sm:text-5xl">
          化学世界可视化教学中心
        </h1>
        <p className="mt-3 text-slate-500">高中化学可视化教学综合平台 · 教学展示模块</p>
        <div className="mt-5 flex flex-wrap gap-2">
          {['可视化实验', '互动闯关', '课堂投屏友好', '化学人格测试'].map((t) => (
            <span
              key={t}
              className="rounded-md border border-slate-300 bg-slate-100 px-3 py-1.5 text-sm text-slate-700"
            >
              {t}
            </span>
          ))}
        </div>
      </section>

      {/* 各板块 */}
      {sections.map((sec) => (
        <section
          key={sec.title}
          className="mt-10 rounded-xl border border-slate-200 bg-white p-6 sm:p-8"
        >
          <div className="mb-6 flex flex-wrap items-end justify-between gap-3">
            <div>
              <div className="flex items-center gap-2 text-xs tracking-widest text-slate-400">
                <sec.icon className="h-3.5 w-3.5" />
                {sec.label}
              </div>
              <h2 className="mt-1 text-3xl font-normal text-slate-900">{sec.title}</h2>
            </div>
            <div className="flex gap-1.5">
              {sec.tags.map((t) => (
                <span
                  key={t}
                  className="rounded border border-slate-300 bg-slate-100 px-2.5 py-1 text-xs text-slate-600"
                >
                  {t}
                </span>
              ))}
            </div>
          </div>
          <div className={`grid gap-3 ${colsClass[sec.cols]}`}>
            {sec.cards.map((card) => {
              const [borderCls, textCls] = card.accent.split(' ')
              const inner = (
                <>
                  <div className={`text-2xl font-bold ${textCls}`}>{card.tag}</div>
                  <div className="mt-2 text-lg text-slate-900">
                    {card.name}
                    {!card.href && (
                      <span className="ml-2 rounded bg-slate-200 px-1.5 py-0.5 text-xs text-slate-500">
                        建设中
                      </span>
                    )}
                  </div>
                  <p className="mt-2 min-h-16 text-sm leading-relaxed text-slate-500">
                    {card.desc}
                  </p>
                  <div className={`mt-3 text-sm ${card.href ? textCls : 'text-slate-400'}`}>
                    {card.href ? '进入实验室 →' : '敬请期待'}
                  </div>
                </>
              )
              const cls = `block rounded-lg border border-slate-200 border-l-4 ${borderCls} bg-slate-50 p-5 ${
                card.href ? 'transition-shadow hover:shadow-md' : 'opacity-80'
              }`
              return card.href ? (
                <a key={card.name} href={card.href} className={cls}>
                  {inner}
                </a>
              ) : (
                <div key={card.name} className={cls}>
                  {inner}
                </div>
              )
            })}
          </div>
        </section>
      ))}

      {/* 交流 + 排行榜占位 */}
      <section className="mt-10 grid gap-3 sm:grid-cols-2">
        <div className="rounded-lg border border-slate-200 border-l-4 border-l-red-500 bg-white p-5">
          <div className="flex items-center gap-2 text-lg text-slate-900">
            <MessagesSquare className="h-4 w-4 text-red-500" />
            交流论坛
            <span className="rounded bg-slate-200 px-1.5 py-0.5 text-xs text-slate-500">建设中</span>
          </div>
          <p className="mt-2 text-sm text-slate-500">
            开贴讨论化学问题、反馈页面问题、分享学习心得。
          </p>
        </div>
        <div className="rounded-lg border border-slate-200 border-l-4 border-l-amber-500 bg-white p-5">
          <div className="flex items-center gap-2 text-lg text-slate-900">
            <Trophy className="h-4 w-4 text-amber-500" />
            排行榜 / 统计
            <span className="rounded bg-slate-200 px-1.5 py-0.5 text-xs text-slate-500">建设中</span>
          </div>
          <p className="mt-2 text-sm text-slate-500">
            总排行与各模块积分榜，登录系统上线后开放。
          </p>
        </div>
      </section>

      <p className="mt-8 flex items-center gap-1.5 text-xs text-slate-400">
        <Sparkles className="h-3 w-3" />
        展示模块第一版：两个 3D 实验室已可用，其余板块将陆续接入。
      </p>
    </main>
  )
}
