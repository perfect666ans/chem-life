import { useEffect, useRef, useState, type CSSProperties } from 'react'
import { Link, useLocation } from 'react-router'
import { getToken, heartbeat } from '../lib/auth'

/**
 * 全局导航辅助（挂在 App.tsx 的 Routes 之前）：
 * 1. 路由切换自动滚到模块顶部
 * 2. 除首页外所有页面右下角悬浮"返回首页"按钮
 * 3. 使用时长心跳（W-06）：页面可见时每 20s 上报当前模块停留秒数
 * 4. 面包屑（首页 › 模块 › 子模块）：滚动超过 240px 后出现在左上角，
 *    悬浮覆盖式、不改动任何页面布局
 */
const MODS: [RegExp, string][] = [
  [/^\/teaching/, 'teaching'], [/^\/life/, 'life'], [/^\/database/, 'database'],
  [/^\/kitchen/, 'kitchen'], [/^\/vitamins/, 'vitamins'], [/^\/amino/, 'amino'],
  [/^\/pubchem/, 'pubchem'], [/^\/forum/, 'forum'], [/^\/leaderboard/, 'leaderboard'],
  [/^\/profile/, 'profile'], [/^\/$/, 'home'], [/.*/, 'home'],
]
function modOf(path: string) {
  for (const [re, name] of MODS) if (re.test(path)) return name
  return 'home'
}

/* 面包屑层级：每段 [文字, 链接]（最后一段为当前页，无链接） */
const CRUMBS: [RegExp, [string, string?][]][] = [
  [/^\/database/, [['首页', '/'], ['成分检索库']]],
  [/^\/pubchem/, [['首页', '/'], ['化合物查询']]],
  [/^\/kitchen/, [['首页', '/'], ['生活探究馆', '/life'], ['厨房化学']]],
  [/^\/vitamins/, [['首页', '/'], ['生活探究馆', '/life'], ['维生素与化学']]],
  [/^\/amino-acids/, [['首页', '/'], ['生活探究馆', '/life'], ['氨基酸与健康']]],
  [/^\/life/, [['首页', '/'], ['生活探究馆']]],
  [/^\/teaching/, [['首页', '/'], ['可视化教学中心']]],
  [/^\/forum/, [['首页', '/'], ['交流论坛']]],
  [/^\/leaderboard/, [['首页', '/'], ['排行榜']]],
  [/^\/profile/, [['首页', '/'], ['我的']]],
  [/^\/login/, [['首页', '/'], ['登录']]],
]
function crumbsOf(path: string): [string, string?][] | null {
  for (const [re, c] of CRUMBS) if (re.test(path)) return c
  return null
}

export default function NavChrome() {
  const { pathname } = useLocation()
  const tracker = useRef({ mod: '', since: Date.now() })
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    window.scrollTo(0, 0)
    setScrolled(false)
  }, [pathname])

  /* 滚动超过 240px 才显示面包屑，避免盖住页面顶部标题 */
  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 240)
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  /* 使用时长心跳 */
  useEffect(() => {
    const flush = () => {
      const now = Date.now()
      const secs = Math.round((now - tracker.current.since) / 1000)
      tracker.current.since = now
      if (secs < 3) return
      const token = getToken()
      if (!token) return
      if (document.visibilityState !== 'visible') return
      void heartbeat(tracker.current.mod, secs).catch(() => {})
    }
    const onHide = () => {
      /* 切后台时结算本段 */
      const now = Date.now()
      const secs = Math.round((now - tracker.current.since) / 1000)
      tracker.current.since = now
      if (secs >= 3 && getToken()) void heartbeat(tracker.current.mod, secs).catch(() => {})
    }
    tracker.current = { mod: modOf(pathname), since: Date.now() }
    const timer = setInterval(flush, 20000)
    document.addEventListener('visibilitychange', onHide)
    return () => {
      clearInterval(timer)
      document.removeEventListener('visibilitychange', onHide)
      onHide()
    }
  }, [pathname])

  if (pathname === '/') return null

  const crumbs = crumbsOf(pathname)
  const pill: CSSProperties = {
    background: 'rgba(15,23,42,.85)', color: '#fff',
    boxShadow: '0 8px 24px rgba(0,0,0,.35)', backdropFilter: 'blur(6px)',
  }

  return (
    <>
      {scrolled && crumbs && (
        <nav
          aria-label="面包屑"
          style={{
            position: 'fixed', left: 16, top: 16, zIndex: 60,
            display: 'flex', alignItems: 'center', gap: 6,
            ...pill, borderRadius: 999, padding: '8px 14px',
            fontSize: 13, fontFamily: 'sans-serif', whiteSpace: 'nowrap',
          }}
        >
          {crumbs.map(([text, to], i) => (
            <span key={i} style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              {i > 0 && <span style={{ opacity: 0.45 }}>›</span>}
              {to ? (
                <Link to={to} style={{ color: '#fff', textDecoration: 'none', opacity: 0.92 }}>{text}</Link>
              ) : (
                <span style={{ color: '#7fd4ff' }}>{text}</span>
              )}
            </span>
          ))}
        </nav>
      )}
      <Link
        to="/"
        title="返回首页"
        style={{
          position: 'fixed', right: 20, bottom: 20, zIndex: 60,
          width: 44, height: 44, borderRadius: 999,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          ...pill, textDecoration: 'none', fontSize: 18,
        }}
      >⌂</Link>
    </>
  )
}
