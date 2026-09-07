import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router'
import '../life-fx.css'
import ThemeToggle from '../components/fx/ThemeToggle'

/* ===== 宝塔五层（2022 版，主人核对后冻结） ===== */
const TIERS = [
  { name: '谷薯类', amt: '250–400 g/天', emj: '🍚🍠🌽🥣',
    foods: ['🍚 米饭', '🍞 全麦', '🍠 红薯', '🌽 玉米', '🥣 燕麦'],
    tip: '其中全谷物和杂豆类 50–150 g，薯类 50–100 g。精制碳水不可怕，关键在搭配。', mod: '碳水化合物' },
  { name: '蔬菜水果', amt: '菜300–500·果200–350 g', emj: '🥦🍅🍎🥝',
    foods: ['🥦 西兰花', '🍅 番茄', '🍎 苹果', '🥝 猕猴桃', '🥬 深绿叶菜'],
    tip: '深色蔬菜占一半以上；果汁不能代替鲜果——榨汁损失了膳食纤维。', mod: '维生素' },
  { name: '动物性食物', amt: '120–200 g/天', emj: '🐟🍗🥚🦐',
    foods: ['🐟 鱼虾', '🍗 禽肉', '🥚 鸡蛋', '🦐 贝类'],
    tip: '每周至少 2 次水产品，每天 1 个蛋；畜禽肉每周 300–500 g。', mod: '蛋白质' },
  { name: '奶类·大豆·坚果', amt: '奶300–500·豆坚25–35 g', emj: '🥛🫘🥜',
    foods: ['🥛 牛奶', '🫘 大豆', '🥜 坚果', '🍶 酸奶'],
    tip: '2022 版把奶类上调至 300–500 g；乳糖不耐受可选酸奶或舒化奶。', mod: '矿物质' },
  { name: '烹调油和盐', amt: '油25–30 g·盐<5 g', emj: '🧂🫒',
    foods: ['🧂 限盐勺', '🫒 植物油', '⚠️ 隐形盐'],
    tip: '盐 <5 g ≈ 一个啤酒瓶盖；酱油、咸菜里的隐形盐占 70% 以上。', mod: '矿物质' },
]

const MODS: Record<string, { en: string; c: string; f: string; items: [string, string][] }> = {
  '蛋白质': { en: 'PROTEIN', c: '#e85d75', f: 'C、H、O、N（+S）｜氨基酸 → 肽键 —CO—NH—', items: [
    ['它是谁', '氨基酸经肽键缩合而成的高分子。20 种氨基酸中 8 种为必需氨基酸，人体不能合成、必须吃。'],
    ['化学视角', '四级结构决定功能：一级序列→氢键盘绕→疏水折叠→亚基组装。变性=空间结构破坏，肽键未断——煮熟的蛋照样消化。'],
    ['吃多少', '供能 4 kcal/g；成人约 0.8–1.2 g/kg 体重。'],
    ['来源', '蛋、奶、鱼虾、瘦肉、大豆；谷物缺赖氨酸、豆类缺蛋氨酸，混吃=蛋白互补。']] },
  '脂类': { en: 'LIPIDS', c: '#f5c76b', f: '甘油三酯 = 甘油 + 3 脂肪酸', items: [
    ['它是谁', '甘油三酯、磷脂、固醇三大类；疏水——所以维生素 A/D/E/K 必须随油脂吸收。'],
    ['化学视角', '饱和脂肪酸直链易堆积；不饱和脂肪酸的双键造成弯折。反式脂肪酸升高 LDL，配料表里的"人造奶油"要警惕。'],
    ['吃多少', '供能 9 kcal/g，是糖的两倍；烹调油 25–30 g/天足矣。'],
    ['来源', '深海鱼（EPA/DHA）、坚果、橄榄油；限制肥肉、奶油、油炸。']] },
  '碳水化合物': { en: 'CARBOHYDRATES', c: '#d98a3d', f: '(CH₂O)ₙ｜单糖 → 二糖 → 多糖', items: [
    ['它是谁', '人体首选能源。血糖生成指数（GI）：白米饭高、燕麦低。'],
    ['化学视角', '淀粉=α-1,4-糖苷键（可消化）；纤维素=β-1,4-糖苷键，人体缺切割它的酶——这就是纤维不能吸收的原因。'],
    ['吃多少', '供能 4 kcal/g，占总能量的 50–65%；全谷物替换 1/3 精米面是 2022 版核心建议。'],
    ['来源', '谷物、薯类、杂豆；限制含糖饮料（游离糖 <50 g/天，最好 <25 g）。']] },
  '维生素': { en: 'VITAMINS', c: '#5fb7ff', f: '13 种微量有机分子｜脂溶 A·D·E·K ｜水溶 B 族·C', items: [
    ['它是谁', '不供能、不构成身体，但每种都是关键酶的辅因子——缺一点，整条代谢链卡壳。'],
    ['化学视角', '维生素 C 是还原剂（抗氧化）；维生素 D 其实是类固醇激素前体（晒太阳皮肤合成）；B12 是唯一含钴的维生素。'],
    ['典型缺乏', '夜盲（A）、坏血病（C）、佝偻病（D）、巨幼贫（B12）……'],
    ['来源', '深色蔬果、肝脏、深海鱼、奶蛋；详见「维生素与化学」专页。']] },
  '矿物质': { en: 'MINERALS', c: '#8bc34a', f: '常量：钙磷钾钠镁｜微量：铁锌碘硒', items: [
    ['它是谁', '以离子形式存在：Ca²⁺ 骨骼、Fe²⁺ 血红蛋白、I⁻ 甲状腺激素、Zn²⁺ 上百种酶。'],
    ['化学视角', '补铁配维生素 C（Fe³⁺→Fe²⁺ 易吸收）；补钙配维生素 D；加碘盐是预防碘缺乏病最廉价手段。'],
    ['吃多少', '盐 <5 g/天 ≈ 钠 2000 mg；钙成人 800 mg，青少年 1000–1200 mg。'],
    ['来源', '奶类（钙）、红肉/动物血（铁）、海产品（碘锌硒）。']] },
  '水': { en: 'WATER', c: '#4dd0e1', f: 'H₂O｜占体重 60–70%', items: [
    ['它是谁', '含量最多、最不被重视的营养素：溶剂、运输介质、体温调节。'],
    ['化学视角', '比热容大（4.18 J/g·℃）所以能稳定体温；参与水解反应；汗液蒸发带走 2.4 kJ/g 汽化热。'],
    ['喝多少', '温和气候成人 1500–1700 ml/天（约 7–8 杯）。'],
    ['来源', '白开水、淡茶；含糖饮料不能替代饮水。']] },
  '膳食纤维': { en: 'DIETARY FIBER', c: '#9b59b6', f: '多糖但 β-糖苷键人切不开', items: [
    ['它是谁', '第七大营养素；不能被小肠吸收，却是肠道菌群的口粮。'],
    ['化学视角', '益生元纤维被菌群发酵产生短链脂肪酸（乙酸/丙酸/丁酸）——滋养肠上皮、调节免疫。吃纤维=养菌=养自己。'],
    ['吃多少', '成人 25–30 g/天；我国人均仅约 13 g，缺口巨大。'],
    ['来源', '全谷物、豆类、蔬果、菌菇；麸皮、菊粉、抗性淀粉都是好纤维。']] },
}

const LABS = [
  { to: '/vitamins', color: '#8bc34a', code: 'VITAMINS', name: '维生素与化学', glyph: '维',
    desc: '13 种维生素的分子结构、脂溶/水溶分类与缺乏症图谱。',
    bg: 'radial-gradient(120% 120% at 25% 20%,#2c4416,#101a08 60%),radial-gradient(55% 55% at 78% 82%,rgba(139,195,74,.35),transparent)' },
  { to: '/amino-acids', color: '#5fb7ff', code: 'AMINO ACIDS', name: '氨基酸与化学', glyph: '氨',
    desc: '20 种氨基酸的分类、必需氨基酸与肽键形成的分子机制。',
    bg: 'radial-gradient(120% 120% at 70% 25%,#17324a,#0b1622 60%),radial-gradient(55% 55% at 22% 80%,rgba(95,183,255,.32),transparent)' },
  { to: '/kitchen', color: '#f5a623', code: 'KITCHEN', name: '厨房化学', glyph: '厨',
    desc: '12 个厨房现象背后的化学原理：美拉德反应、发酵、胶体聚沉……',
    bg: 'radial-gradient(120% 120% at 30% 75%,#45300f,#150e04 60%),radial-gradient(55% 55% at 80% 22%,rgba(245,166,35,.32),transparent)' },
]

export default function LifeHall() {
  const [picked, setPicked] = useState(-1)
  const [chip, setChip] = useState<{ show: boolean; text: string; x: number; y: number }>({ show: false, text: '', x: 0, y: 0 })
  const [activeMod, setActiveMod] = useState<string | null>(null)
  const svgRef = useRef<SVGSVGElement>(null)
  const stageRef = useRef<HTMLDivElement>(null)

  /* 建塔：五层镂空悬浮 + 光点 */
  useEffect(() => {
    const svg = svgRef.current
    if (!svg) return
    const NS = 'http://www.w3.org/2000/svg'
    const H = 372, CX = 200, BASE = 168, TOPY = 26, N = TIERS.length, GAP = 13
    const half = (t: number) => BASE * t
    for (let i = 0; i < 16; i++) {
      const c = document.createElementNS(NS, 'circle')
      c.setAttribute('class', 'dot')
      c.setAttribute('cx', (60 + Math.random() * 280).toFixed(0))
      c.setAttribute('cy', (40 + Math.random() * 320).toFixed(0))
      c.setAttribute('r', (0.7 + Math.random() * 1.3).toFixed(1))
      c.setAttribute('fill', '#b9cede')
      c.style.cssText = `--dx:${(Math.random() * 30 - 15).toFixed(0)}px;--dy:${(-20 - Math.random() * 30).toFixed(0)}px;--dur:${(6 + Math.random() * 6).toFixed(1)}s;animation-delay:${(-Math.random() * 8).toFixed(1)}s`
      svg.appendChild(c)
    }
    for (let k = 0; k < N; k++) {
      const T = TIERS[k]
      const t1 = k / N, t2 = (k + 1) / N
      const y1 = TOPY + t1 * (H - TOPY), y2 = TOPY + t2 * (H - TOPY) - GAP
      const pts = [[CX - half(t1), y1], [CX + half(t1), y1], [CX + half(t2), y2], [CX - half(t2), y2]]
      const g = document.createElementNS(NS, 'g')
      g.setAttribute('class', 'tier'); g.dataset.i = String(k)
      g.style.animationDelay = `${k * 0.75}s`
      const tilt = document.createElementNS(NS, 'g')
      tilt.setAttribute('class', 'tilt')
      const body = document.createElementNS(NS, 'path')
      body.setAttribute('class', 'body')
      body.setAttribute('d', roundedPath(pts, 9))
      body.setAttribute('fill', '#0f1a28')
      body.setAttribute('fill-opacity', '.92')
      body.setAttribute('stroke', 'url(#metalLin)')
      body.setAttribute('stroke-width', '.9')
      body.style.filter = 'drop-shadow(0 8px 18px rgba(0,0,0,.35))'
      tilt.appendChild(body)
      const shade = document.createElementNS(NS, 'path')
      shade.setAttribute('class', 'shade')
      shade.setAttribute('d', roundedPath(pts, 9))
      shade.setAttribute('fill', '#08141f')
      shade.setAttribute('opacity', '.28')
      tilt.appendChild(shade)
      if (k > 0) {
        const tN = document.createElementNS(NS, 'text')
        tN.setAttribute('x', String(CX)); tN.setAttribute('y', String((y1 + y2) / 2 - 1))
        tN.setAttribute('text-anchor', 'middle')
        tN.setAttribute('style', `font-family:var(--mono);font-weight:500;font-size:${k === 1 ? 10.5 : 12}px;fill:#a9bdd0;letter-spacing:.22em;paint-order:stroke;stroke:rgba(4,14,22,.7);stroke-width:2.5px`)
        tN.textContent = T.name
        const tA = document.createElementNS(NS, 'text')
        tA.setAttribute('x', String(CX)); tA.setAttribute('y', String((y1 + y2) / 2 + 15))
        tA.setAttribute('text-anchor', 'middle')
        tA.setAttribute('style', `font-family:var(--mono);font-weight:400;font-size:${k === 1 ? 8 : 9.5}px;fill:#8ba2b6;letter-spacing:.1em;paint-order:stroke;stroke:rgba(4,14,22,.7);stroke-width:2px`)
        tA.textContent = T.amt
        tilt.appendChild(tN); tilt.appendChild(tA)
      } else {
        const tA0 = document.createElementNS(NS, 'text')
        tA0.setAttribute('x', String(CX)); tA0.setAttribute('y', String((y1 + y2) / 2 + 4))
        tA0.setAttribute('text-anchor', 'middle')
        tA0.setAttribute('style', 'font-family:var(--mono);font-weight:400;font-size:8px;fill:#8ba2b6;letter-spacing:.08em;paint-order:stroke;stroke:rgba(4,14,22,.7);stroke-width:2px')
        tA0.textContent = T.amt
        tilt.appendChild(tA0)
      }
      g.appendChild(tilt)
      svg.appendChild(g)
    }
    function roundedPath(pts: number[][], r: number) {
      let d = '', n = pts.length
      for (let i = 0; i < n; i++) {
        const p0 = pts[(i - 1 + n) % n], p1 = pts[i], p2 = pts[(i + 1) % n]
        const v1x = p0[0] - p1[0], v1y = p0[1] - p1[1], v2x = p2[0] - p1[0], v2y = p2[1] - p1[1]
        const l1 = Math.hypot(v1x, v1y) || 1, l2 = Math.hypot(v2x, v2y) || 1
        const rr = Math.min(r, l1 / 2.6, l2 / 2.6)
        d += (i === 0 ? 'M' : 'L') + (p1[0] + v1x / l1 * rr).toFixed(1) + ',' + (p1[1] + v1y / l1 * rr).toFixed(1)
          + ' Q' + p1[0].toFixed(1) + ',' + p1[1].toFixed(1) + ' ' + (p1[0] + v2x / l2 * rr).toFixed(1) + ',' + (p1[1] + v2y / l2 * rr).toFixed(1)
      }
      return d + 'Z'
    }
  }, [])

  /* 涟漪：石破湖面（微风档参数） */
  useEffect(() => {
    const stage = stageRef.current
    const cv = document.getElementById('ripple') as HTMLCanvasElement | null
    if (!stage || !cv) return
    const W = 200, H = 230
    cv.width = W; cv.height = H
    const ctx = cv.getContext('2d')
    if (!ctx) return
    let buf1 = new Float32Array(W * H), buf2 = new Float32Array(W * H)
    const img = ctx.createImageData(W, H), px = img.data
    let raf = 0
    const drop = (x: number, y: number, p: number) => {
      x |= 0; y |= 0; if (x < 2 || x > W - 3 || y < 2 || y > H - 3) return
      const i = y * W + x
      buf1[i] += p; buf1[i + 1] += p * 0.4; buf1[i - 1] += p * 0.4; buf1[i + W] += p * 0.4; buf1[i - W] += p * 0.4
    }
    const onMove = (e: MouseEvent) => {
      const r = stage.getBoundingClientRect()
      drop((e.clientX - r.left) / r.width * W, (e.clientY - r.top) / r.height * H, 90)
    }
    const onClick = (e: MouseEvent) => {
      const r = stage.getBoundingClientRect()
      drop((e.clientX - r.left) / r.width * W, (e.clientY - r.top) / r.height * H, 430)
    }
    stage.addEventListener('mousemove', onMove)
    stage.addEventListener('click', onClick)
    const step = () => {
      for (let y = 1; y < H - 1; y++) {
        const row = y * W
        for (let x = 1; x < W - 1; x++) {
          const i = row + x
          buf2[i] = ((buf1[i - 1] + buf1[i + 1] + buf1[i - W] + buf1[i + W]) / 2 - buf2[i]) * 0.982
        }
      }
      for (let i = 0; i < W * H; i++) {
        const v = buf2[i], j = i * 4
        px[j] = 186; px[j + 1] = 224; px[j + 2] = 255
        px[j + 3] = v > 1.6 ? Math.min(22, v * 0.3) : 0
      }
      ctx.putImageData(img, 0, 0)
      const t = buf1; buf1 = buf2; buf2 = t
      raf = requestAnimationFrame(step)
    }
    raf = requestAnimationFrame(step)
    return () => {
      cancelAnimationFrame(raf)
      stage.removeEventListener('mousemove', onMove)
      stage.removeEventListener('click', onClick)
    }
  }, [])

  /* 塔层交互（事件委托，SVG 为命令式构建） */
  useEffect(() => {
    const svg = svgRef.current
    const stage = stageRef.current
    if (!svg || !stage) return
    const tiers = svg.querySelectorAll<SVGGElement>('g.tier')
    const onEnter = (k: number) => (e: Event) => {
      if (picked >= 0) return
      const g = e.currentTarget as SVGGElement
      const r = g.getBoundingClientRect(), pr = stage.getBoundingClientRect()
      setChip({ show: true, text: `第${k + 1}层 · ${TIERS[k].name} · ${TIERS[k].amt}`, x: r.left - pr.left + r.width / 2, y: r.top - pr.top - 4 })
    }
    const onLeave = () => setChip((c) => ({ ...c, show: false }))
    const onClick = (k: number) => (e: Event) => { e.stopPropagation(); setPicked((p) => (p === k ? -1 : k)) }
    tiers.forEach((g, k) => {
      g.addEventListener('mouseenter', onEnter(k))
      g.addEventListener('mouseleave', onLeave)
      g.addEventListener('click', onClick(k))
    })
    return () => {
      tiers.forEach((g, k) => {
        g.removeEventListener('mouseenter', onEnter(k))
        g.removeEventListener('mouseleave', onLeave)
        g.removeEventListener('click', onClick(k))
      })
    }
  }, [picked])

  /* 点任意处 / 双击 / Esc 关弹窗 */
  useEffect(() => {
    const close = (e: MouseEvent) => {
      if (picked >= 0 && !(e.target as HTMLElement).closest('#life-pop') && !(e.target as HTMLElement).closest('#pagoda')) setPicked(-1)
    }
    const dbl = () => setPicked(-1)
    const esc = (e: KeyboardEvent) => { if (e.key === 'Escape') setPicked(-1) }
    document.addEventListener('click', close)
    document.addEventListener('dblclick', dbl)
    document.addEventListener('keydown', esc)
    return () => {
      document.removeEventListener('click', close)
      document.removeEventListener('dblclick', dbl)
      document.removeEventListener('keydown', esc)
    }
  }, [picked])

  /* 选中层高亮 */
  useEffect(() => {
    const tiers = svgRef.current?.querySelectorAll<SVGGElement>('g.tier')
    tiers?.forEach((g, i) => g.classList.toggle('lit', i === picked))
  }, [picked])

  useEffect(() => { document.title = '生活探究馆 · 化学视界' }, [])

  const T = picked >= 0 ? TIERS[picked] : null
  const M = activeMod ? MODS[activeMod] : null

  return (
    <div id="lifeRoot" data-theme="dark">
      <div className="wrap">
        <div className="top">
          <h1>生活探究馆</h1><span className="tag">NUTRITION · CHEMISTRY</span>
          <Link to="/" style={{ marginLeft: 'auto', fontFamily: 'var(--mono)', fontSize: 11, letterSpacing: '.08em', color: 'var(--ink-2)', textDecoration: 'none', border: '1px solid var(--line-2)', padding: '6px 12px', borderRadius: 999 }}>← 返回首页</Link>
          <ThemeToggle targetId="lifeRoot" />
        </div>
        <p className="sub">中国居民膳食指南（2022）· 悬停宝塔任一层看摄入量，点击查看详情</p>

        <div className="layout">
          <div className="stage" ref={stageRef}>
            <div className="cap">中国居民膳食指南 · 2022</div>
            <svg id="pagoda" ref={svgRef} viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg" />
            <canvas id="ripple" />
            <div className="callout">⑤ 烹调油和盐 · 油 25–30 g · 盐 &lt;5 g</div>
            <div className="water-note">水 1500–1700 ml/天 ｜ 每天活动 6000 步</div>
            <div className={chip.show ? 'chip show' : 'chip'} style={{ left: chip.x, top: chip.y }}>{chip.text}</div>
            <div id="life-pop" className={picked >= 0 ? 'pop show' : 'pop'}>
              {T && (<>
                <button className="x" onClick={() => setPicked(-1)}>✕</button>
                <h4>第{picked + 1}层 · {T.name} <span className="amt">{T.amt}</span></h4>
                <div className="foods">{T.foods.map((f) => <span key={f}>{f}</span>)}</div>
                <div className="tip">{T.tip}</div>
                <button className="more" onClick={() => { setActiveMod(T.mod); setPicked(-1); document.getElementById('mods')?.scrollIntoView({ behavior: 'smooth', block: 'center' }) }}>
                  看「{T.mod}」的化学视角 →
                </button>
              </>)}
            </div>
          </div>

          <div>
            <div className="sec-t">00 · 专页学习模块</div>
            <div className="labs">
              {LABS.map((L) => (
                <Link className="labcard" key={L.code} to={L.to} style={{ ['--lc' as string]: L.color }}>
                  <div className="art" style={{ background: L.bg }}><span className="glyph">{L.glyph}</span></div>
                  <div className="body">
                    <h3>{L.name} <span className="code">{L.code}</span></h3>
                    <p>{L.desc}</p>
                    <span className="go">进入专页 →</span>
                  </div>
                </Link>
              ))}
            </div>

            <div className="sec-t">01 · 七大营养素 — 点我看化学视角</div>
            <div className="mods" id="mods">
              {Object.entries(MODS).map(([k, v]) => (
                <div key={k} className={activeMod === k ? 'mod on' : 'mod'}
                  style={{ ['--mc' as string]: v.c }}
                  onClick={() => setActiveMod((cur) => (cur === k ? null : k))}>
                  <b>{k}</b><span>{v.en}</span><em>{v.f.split('｜')[0]}</em>
                </div>
              ))}
            </div>

            {M && activeMod && (
              <div className="detail" style={{ ['--mc' as string]: M.c }}>
                <h3>{activeMod} <span className="en">{M.en}</span></h3>
                <div className="formula">{M.f}</div>
                <div className="d-grid">
                  {M.items.map(([t, d]) => (<div className="d-item" key={t}><b>{t}</b><p>{d}</p></div>))}
                </div>
                <button className="back" onClick={() => setActiveMod(null)}>← 收起详情</button>
              </div>
            )}

            <div className="footnote">数据来源：《中国居民膳食指南（2022 版）》中国营养学会。摄入量为成年人一般推荐量，特殊人群另需个体化调整。正式上线前由站主逐项核对原文。</div>
          </div>
        </div>
      </div>
    </div>
  )
}
