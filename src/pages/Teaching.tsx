// 教学中心门户 —— 模仿 tk-chem.cc/nav.html 的讲座目录式设计
// 罗马数字分区 · 衬线标题 · 编号卡片 · 「进入 →」

type Card = {
  no: string
  name: string
  desc: string
  href?: string
  note?: string // 「建设中」等角标
}

type Section = {
  roman: string
  label: string
  title: string
  range: string
  cards: Card[]
}

const sections: Section[] = [
  {
    roman: 'Ⅰ',
    label: 'STRUCTURE · LAB 01–04',
    title: '结构专题',
    range: '微观结构可视化',
    cards: [
      {
        no: '01',
        name: 'VSEPR 分子构型实验室',
        desc: '184 种分子 3D 电子云：无机 / 离子团（正·负）/ 有机三大类，σ·π·孤对分色渲染。',
        href: '/teaching/chem_lab1.1.html',
      },
      {
        no: '02',
        name: '晶体结构深度实验室',
        desc: '31 种晶体：晶胞延展、立方体切割、比例模型、微粒显隐、四视角二维投影点阵。',
        href: '/teaching/chem_lab1.2.html',
      },
      {
        no: '03',
        name: '离子晶体晶胞专题',
        desc: 'NaCl、CsCl、ZnS、CaF₂、TiO₂ 等典型离子晶体晶胞对比（入口同晶体实验室·离子晶体）。',
        href: '/teaching/chem_lab1.2.html',
      },
      {
        no: '04',
        name: '核外电子排布实验室',
        desc: '118 元素点选：玻尔壳层动画、轨道方框图（泡利·洪特）、排布式三形态、常见离子切换、半径对比。',
        href: '/teaching/chem_lab1.3.html',
      },
    ],
  },
  {
    roman: 'Ⅱ',
    label: 'REVIEW',
    title: '复习板块',
    range: '记忆 · 连胜 · 复盘',
    cards: [
      {
        no: '01',
        name: '知识球 · 知识地图',
        desc: '52 个核心知识点力导向网络：五册教材分色、「前置→后续」学习路径箭头，每点配预习卡与母题方向，支持搜索与教材筛选。',
        href: '/teaching/chem_lab2.1.html',
      },
      {
        no: '02',
        name: '化学闪卡复习',
        desc: '高中化学 10 章 150 张精编闪卡：必修一二 + 选择性必修 1-3，Leitner 记忆盒追踪进度、识别薄弱、到期智能推荐。',
        href: '/teaching/chem_lab2.2.html',
      },
      {
        no: '03',
        name: '知识挑战树',
        desc: '10 条章节枝干 × 3 层共 30 个挑战节点：抽题自评闯关、点亮解锁上层，XP 等级、连胜纪录与 8 项成就本地持久化。',
        href: '/teaching/chem_lab2.3.html',
      },
    ],
  },
  {
    roman: 'Ⅲ',
    label: 'ORGANIC CHEMISTRY',
    title: '有机化学',
    range: '≡键 · R-OH · 酯化',
    cards: [
      {
        no: '01',
        name: '有机反应机理库',
        desc: '6 大核心机理分相动画：酯化 ¹⁸O 示踪、加成、消去、自由基取代、银镜、卤代烃双路径。',
        href: '/teaching/chem_lab3.1.html',
      },
      {
        no: '02',
        name: '有机系统命名中心',
        desc: '随机生成带支链烷烃键线式四选一闯关：最长链严格保证、最低位次组编号，连胜纪录 + 错题本。',
        href: '/teaching/chem_lab3.2.html',
      },
      {
        no: '03',
        name: '同分异构体闯关挑战',
        desc: '5 章 27 题：烷烃骨架、等效氢与卤代、烯炔、苯环定位、醇醚羧酸酯，题题带解析、80% 通关。',
        href: '/teaching/chem_lab3.3.html',
      },
    ],
  },
  {
    roman: 'Ⅳ',
    label: 'REACTION PRINCIPLES',
    title: '化学反应原理',
    range: 'ΔH · K · e⁻',
    cards: [
      {
        no: '01',
        name: '化学反应的热效应',
        desc: '键能法 ΔH 即时重算 + 能量进程图，8 个预设反应可自由改键清单；盖斯定律双路径拖动演示。',
        href: '/teaching/chem_lab4.1.html',
      },
      {
        no: '02',
        name: '化学反应速率与平衡',
        desc: '粒子碰撞沙盘：温度/浓度/压强滑块扰动，A⇌B 动态平衡互变动画 + 粒子数-时间曲线，勒夏特列实时判断。',
        href: '/teaching/chem_lab4.2.html',
      },
      {
        no: '03',
        name: '水溶液中的离子平衡',
        desc: 'pH 对数标尺联动浓度、三类滴定突跃曲线（含指示剂变色域与体积游标）、盐类水解速查表。',
        href: '/teaching/chem_lab4.3.html',
      },
      {
        no: '04',
        name: '化学反应与电能',
        desc: '原电池 / 电解池 / 电镀 / 吸氧腐蚀动画：电子流、气泡、离子迁移、电表与直流电源全联动。',
        href: '/teaching/chem_lab4.4.html',
      },
    ],
  },
  {
    roman: 'Ⅴ',
    label: 'GAMES',
    title: '游戏板块',
    range: 'XP · Boss · Combo',
    cards: [
      {
        no: '01',
        name: '元素纪元 RPG',
        desc: '回合制元素对战：答氧化还原题攻击、答错被反击，20 种元素精灵可削弱捕获进图鉴，等级成长与战绩本地保存。',
        href: '/teaching/chem_lab5.1.html',
      },
      {
        no: '02',
        name: '元素防线：化学塔防',
        desc: '用离子沉淀、酸碱中和与氧化还原布置防线，在攻防节奏中判断反应类型。',
        note: '建设中',
      },
      {
        no: '03',
        name: 'CBTI 化学人格鉴定',
        desc: '16 道题 × 4 维度测出你的物质人格：16 种结果卡（从钠到氦），可复制的分享文案。',
        href: '/teaching/chem_lab5.3.html',
      },
    ],
  },
  {
    roman: 'Ⅵ',
    label: 'COMMUNITY',
    title: '社区与排行',
    range: '登录系统上线后开放',
    cards: [
      {
        no: '01',
        name: '交流论坛',
        desc: '开贴讨论化学问题、反馈页面问题、分享学习心得。',
        note: '建设中',
      },
      {
        no: '02',
        name: '排行榜 / 统计',
        desc: '总排行与各模块积分榜，软件使用时长与游戏时长（可选公开）。',
        note: '建设中',
      },
    ],
  },
]

const TK_STYLE = `
@import url('https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;500;700;800&family=Noto+Serif+SC:wght@400;500;700;900&family=Noto+Sans+SC:wght@300;400;500;700&family=JetBrains+Mono:wght@400;500;700&display=swap');
.tk-portal{
  --serif-cn:"Noto Serif SC","Source Han Serif SC","Songti SC",serif;
  --sans-cn:"Noto Sans SC","PingFang SC",sans-serif;
  --mono:"JetBrains Mono",monospace;
  --ink:#1a1817; --ink-dim:#5a5550; --ink-mute:#9a948a;
  --paper:#f7f4ec; --card:#fffdf8;
  --line:rgba(26,24,23,.14); --line-strong:rgba(26,24,23,.30);
  --accent:#c8102e; --accent-soft:rgba(200,16,46,.08);
  background:
    radial-gradient(1200px 500px at 15% -5%, rgba(200,16,46,.05), transparent 60%),
    var(--paper);
  color:var(--ink); font-family:var(--sans-cn);
  border-top:1px solid var(--line); border-bottom:1px solid var(--line);
}
.tk-hero{padding:clamp(36px,6vw,72px) 0 clamp(28px,4vw,48px);}
.tk-hero .kicker{font-family:var(--mono);font-size:11px;letter-spacing:3px;color:var(--accent);}
.tk-hero h1{
  font-family:var(--serif-cn);font-weight:900;letter-spacing:2px;
  font-size:clamp(30px,5vw,52px);line-height:1.25;margin-top:12px;
}
.tk-hero h1 em{font-style:normal;color:var(--accent);}
.tk-hero p{margin-top:14px;color:var(--ink-dim);font-size:14.5px;max-width:560px;line-height:1.9;}
.tk-hero .meta{
  margin-top:20px;display:flex;flex-wrap:wrap;gap:8px 22px;
  font-family:var(--mono);font-size:11px;letter-spacing:2px;color:var(--ink-mute);
}
.tk-sec{padding:clamp(22px,3.5vw,36px) 0;border-top:1px solid var(--line);}
.tk-sec-head{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap;margin-bottom:18px;}
.tk-roman{
  font-family:var(--serif-cn);font-weight:800;font-size:clamp(26px,3.5vw,38px);
  color:var(--accent);line-height:1;
}
.tk-sec-head h2{font-family:var(--serif-cn);font-weight:800;font-size:clamp(19px,2.4vw,26px);letter-spacing:2px;}
.tk-sec-head .range{font-family:var(--mono);font-size:10.5px;letter-spacing:2px;color:var(--ink-mute);margin-left:auto;}
.tk-cards{display:grid;gap:1px;background:var(--line);border:1px solid var(--line);}
.tk-cards.c2{grid-template-columns:repeat(auto-fit,minmax(260px,1fr));}
.tk-card{
  background:var(--card);padding:18px 20px 16px;display:block;text-decoration:none;color:inherit;
  transition:background .25s;position:relative;
}
a.tk-card:hover{background:var(--accent-soft);}
.tk-card .row1{display:flex;align-items:baseline;gap:12px;}
.tk-card .no{font-family:var(--mono);font-size:12px;color:var(--ink-mute);}
.tk-card .enter{
  font-family:var(--serif-cn);font-weight:700;font-size:15px;color:var(--accent);
  letter-spacing:1px;white-space:nowrap;
}
.tk-card .enter.off{color:var(--ink-mute);}
.tk-card h3{font-family:var(--serif-cn);font-weight:700;font-size:16.5px;letter-spacing:1px;margin-top:8px;}
.tk-card p{font-size:12.5px;color:var(--ink-dim);line-height:1.8;margin-top:6px;}
.tk-card .wip{
  position:absolute;top:14px;right:16px;font-family:var(--mono);font-size:10px;
  letter-spacing:2px;color:var(--ink-mute);border:1px solid var(--line);padding:2px 8px;border-radius:999px;
}
.tk-foot{padding:26px 0 40px;font-family:var(--mono);font-size:10.5px;letter-spacing:2px;color:var(--ink-mute);}
`

export default function TeachingPage() {
  return (
    <div className="tk-portal">
      <style>{TK_STYLE}</style>
      <main className="mx-auto max-w-6xl px-4">
        {/* 头部 */}
        <section className="tk-hero">
          <div className="kicker">TEACHING CENTER · 教学展示模块</div>
          <h1>
            化学世界<em>可视化</em>教学中心
          </h1>
          <p>
            模仿 tk-chem 的讲座式目录：按专题分区、编号进入。两个 3D 实验室已完整可用，
            其余板块陆续接入。
          </p>
          <div className="meta">
            <span>LAB ×2 已上线</span>
            <span>MODULE ×17 规划中</span>
            <span>和紙 · 墨朱 · 藍 三主题（实验室内切换）</span>
          </div>
        </section>

        {/* 各板块 */}
        {sections.map((sec) => (
          <section key={sec.title} className="tk-sec">
            <div className="tk-sec-head">
              <span className="tk-roman">{sec.roman}</span>
              <h2>{sec.title}</h2>
              <span className="range">
                {sec.label} · {sec.range}
              </span>
            </div>
            <div className="tk-cards c2">
              {sec.cards.map((card) => {
                const inner = (
                  <>
                    {card.note && <span className="wip">{card.note}</span>}
                    <div className="row1">
                      <span className="no">{card.no}</span>
                      <span className={`enter${card.href ? '' : ' off'}`}>
                        {card.href ? '进入 →' : '敬请期待'}
                      </span>
                    </div>
                    <h3>{card.name}</h3>
                    <p>{card.desc}</p>
                  </>
                )
                return card.href ? (
                  <a key={card.name} href={card.href} className="tk-card">
                    {inner}
                  </a>
                ) : (
                  <div key={card.name} className="tk-card">
                    {inner}
                  </div>
                )
              })}
            </div>
          </section>
        ))}

        <div className="tk-foot">
          CHEM-LIFE TEACHING PORTAL · 目录式设计灵感：tk-chem.cc/nav.html
        </div>
      </main>
    </div>
  )
}
