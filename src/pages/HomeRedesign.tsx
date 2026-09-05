import { useEffect, useRef } from 'react'
import { Link } from 'react-router'
import '../home-fx.css'
import Reveal from '../components/fx/Reveal'
import Particles from '../components/fx/Particles'
import TiltCard from '../components/fx/TiltCard'
import HScroller from '../components/fx/HScroller'
import ThemeToggle from '../components/fx/ThemeToggle'
import useGlowTheme from '../components/fx/useGlowTheme'

import bgHero from '../assets/art/bg-hero.webp'
import titleArt from '../assets/art/title-shijie.webp'
import logoHua from '../assets/art/logo-hua.webp'
import worldStructure from '../assets/art/world-structure.webp'
import worldOrganic from '../assets/art/world-organic.webp'
import worldPrinciple from '../assets/art/world-principle.webp'
import worldRpg from '../assets/art/world-rpg.webp'
import worldTd from '../assets/art/world-td.webp'
import worldReview from '../assets/art/world-review.webp'
import portalLab from '../assets/art/portal-lab.webp'
import portalLife from '../assets/art/portal-life.webp'
import portalDb from '../assets/art/portal-db.webp'

/* ===== 数据（对齐《资产使用规范》第二节色板） ===== */
const MARQUEE = [
  ['晶格圣殿', '#5B8CFF'], ['熵增之海', '#3ECBFF'], ['配位场', '#C77DFF'],
  ['孤对星环', '#FFB84D'], ['轨道花园', '#B4FF5C'], ['阿伦尼乌斯回廊', '#FF9A3D'],
  ['勒夏特列之秤', '#FF5C5C'], ['元素周期神殿', '#8AB4FF'],
]

const WORLDS = [
  { img: worldStructure, color: '#3ECBFF', en: 'STRUCTURE', name: '晶脉回响', tags: '分子 · 晶体 · 电子排布', badge: '结构', to: '/teaching' },
  { img: worldOrganic, color: '#B4FF5C', en: 'ORGANIC', name: '有机迷林', tags: '命名 · 异构 · 机理', badge: '有机', to: '/teaching' },
  { img: worldPrinciple, color: '#FF9A3D', en: 'PRINCIPLE', name: '熔炉法则', tags: '能量 · 平衡 · 电化学', badge: '原理', to: '/teaching' },
  { img: worldRpg, color: '#C77DFF', en: 'RPG', name: '元素纪元', tags: '30 波元素兽 · 方程式施法', badge: 'RPG', to: '/teaching' },
  { img: worldTd, color: '#FF5C5C', en: 'ARCADE TD', name: '元素防线', tags: '沉淀塔 · 中和塔 · 15 波守卫战', badge: '塔防', to: '/teaching' },
  { img: worldReview, color: '#8AB4FF', en: 'REVIEW', name: '知识星河', tags: '知识地图 · 闪卡 · 技能树', badge: '复习', to: '/teaching' },
]

const PORTALS = [
  { img: portalLab, color: '#3ECBFF', code: 'LAB', name: '模拟实验室', badge: '16 实验室',
    desc: '晶体结构 · 有机机理 · 电化学 · 平衡速率，16 间互动实验室像真做实验一样学。', to: '/teaching' },
  { img: portalLife, color: '#B4FF5C', code: 'LIFE', name: '生活探究馆', badge: '持续更新',
    desc: '维生素与化学 · 氨基酸与化学 · 厨房里的反应，膳食指南宝塔即将上线。', to: '/vitamins' /* TODO: C-02 上线后改 /life */ },
  { img: portalDb, color: '#FFB84D', code: 'DB', name: '成分检索库', badge: '417 条目',
    desc: '417 条成分记录覆盖 12 类日常物品，俗名、化学式、用途一站式检索。', to: '/database' },
]

export default function HomeRedesign() {
  const rootRef = useRef<HTMLDivElement>(null)
  useGlowTheme('homeRoot')

  useEffect(() => {
    document.title = '化学视界 · 生活中的化学'
  }, [])

  return (
    <div id="homeRoot" ref={rootRef} data-theme="dark">
      <div className="hr-page">
        <header className="hr-top">
          <div className="in">
            <Link className="hr-brand" to="/">
              <span className="mark"><img src={logoHua} alt="化" /></span>
              <span><b>化学视界</b><small>CHEM · IN · LIFE</small></span>
            </Link>
            <nav className="hr-nav">
              <Link to="/#worlds" className="active">趣味探索</Link>
              <Link to="/#portals">功能门户</Link>
              <Link to="/forum">论坛</Link>
              <Link to="/profile">我的</Link>
            </nav>
            <ThemeToggle />
          </div>
        </header>

        {/* Hero */}
        <section className="hr-hero" data-glow="#2456d6">
          <div className="hr-hero-art" style={{ backgroundImage: `url(${bgHero})` }} />
          <Particles />
          <div className="wrap">
            <Reveal><span className="hr-eyebrow">早晨老师的化学可视化趣味平台</span></Reveal>
            <Reveal delay={90}><h1 className="hr-title"><img src={titleArt} alt="化学视界" /></h1></Reveal>
            <Reveal delay={180}><div className="hr-sub">CHEMISTRY · IN · DAILY LIFE</div></Reveal>
            <Reveal delay={270}>
              <p className="hr-lede">从一部手机的 60 种元素，到奶茶杯上的 PET——把化学课本搬进日常生活。16 个互动实验室、成分百科、健康化学，像探索一样学习。</p>
            </Reveal>
            <Reveal delay={360}>
              <div className="hr-cta">
                <Link className="hr-btn hr-btn-ink" to="/teaching">进入模拟实验室 <span className="arr">→</span></Link>
                <Link className="hr-btn hr-btn-ink" to="/vitamins">进入生活探究馆 <span className="arr">→</span></Link>
                <Link className="hr-btn hr-btn-ink" to="/database">进入成分检索库 <span className="arr">→</span></Link>
              </div>
            </Reveal>
          </div>
        </section>

        {/* 滚动彩条 */}
        <div className="hr-marquee" aria-hidden="true">
          <div className="track">
            {[...MARQUEE, ...MARQUEE].map(([name, color], i) => (
              <span className="hr-mq-item" style={{ ['--mq-c' as string]: color }} key={i}><i />{name}</span>
            ))}
          </div>
        </div>

        {/* 01 趣味探索 */}
        <section className="hr-block" data-glow="#e85d75" id="worlds">
          <div className="wrap">
            <Reveal className="hr-sec-head">
              <span className="no">01 / WORLDS</span><h2>趣味探索</h2><p>像闯入一个个化学异世界</p>
            </Reveal>
            <div className="hr-grid">
              {WORLDS.map((w, i) => (
                <Reveal key={w.en} delay={i * 90}>
                  <TiltCard className="hr-zone" to={w.to} style={{ ['--zc' as string]: w.color }}>
                    <span className="badge on">{w.badge}</span>
                    <div className="art">
                      <div className="ph"><img src={w.img} alt={w.name} loading="lazy" /><div className="mask" /></div>
                      <div className="ov" />
                    </div>
                    <div className="zt">
                      <span className="en">{w.en}</span>
                      <h3>{w.name}</h3>
                      <p>{w.tags}</p>
                    </div>
                  </TiltCard>
                </Reveal>
              ))}
            </div>
          </div>
        </section>

        {/* 02 功能门户 */}
        <section className="hr-block" data-glow="#2456d6" id="portals">
          <div className="wrap">
            <Reveal className="hr-sec-head">
              <span className="no">02 / PORTALS</span><h2>功能门户</h2><p>封面速览 · 左右滑动 →</p>
            </Reveal>
            <Reveal><div className="hr-hint">DRAG / SWIPE</div></Reveal>
            <HScroller>
              {PORTALS.map((p) => (
                <TiltCard key={p.code} className="hr-portal" to={p.to} style={{ ['--pc' as string]: p.color }}>
                  <span className="badge on">{p.badge}</span>
                  <div className="frame">
                    <div className="art">
                      <div className="ph"><img src={p.img} alt={p.name} loading="lazy" /><div className="mask" /></div>
                    </div>
                    <div className="body">
                      <h3>{p.name} <span className="code">{p.code}</span></h3>
                      <p>{p.desc}</p>
                      <span className="go">进入模块 →</span>
                    </div>
                  </div>
                </TiltCard>
              ))}
            </HScroller>
          </div>
        </section>

        <footer className="hr-footer">
          <div className="mono">HUAXUE-SHENGHUO · CHEM IN LIFE</div>
          <p style={{ marginTop: 6 }}>化学视界 · 把化学课本搬进日常生活</p>
        </footer>
      </div>
    </div>
  )
}
