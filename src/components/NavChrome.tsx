import { useEffect } from 'react'
import { Link, useLocation } from 'react-router'

/**
 * 全局导航辅助（挂在 App.tsx 的 Routes 之前，全站生效）：
 * 1. 路由切换自动滚到模块顶部
 * 2. 除首页外所有页面右下角悬浮"返回首页"按钮
 */
export default function NavChrome() {
  const { pathname } = useLocation()

  useEffect(() => {
    window.scrollTo(0, 0)
  }, [pathname])

  if (pathname === '/') return null

  return (
    <Link
      to="/"
      title="返回首页"
      style={{
        position: 'fixed', right: 20, bottom: 20, zIndex: 60,
        width: 44, height: 44, borderRadius: 999,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        background: 'rgba(15,23,42,.85)', color: '#fff',
        boxShadow: '0 8px 24px rgba(0,0,0,.35)', textDecoration: 'none',
        backdropFilter: 'blur(6px)', fontSize: 18,
      }}
    >⌂</Link>
  )
}
