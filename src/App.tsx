import { Suspense, lazy } from 'react'
import { Routes, Route, useLocation } from 'react-router'
import Home from './pages/HomeRedesign'
import NavChrome from './components/NavChrome'
import FeedbackWidget from './components/FeedbackWidget'
import LifeHall from './pages/LifeHall'

// 路由级代码分割：非首页按需加载，降低首屏体积
const DatabasePage = lazy(() => import('./pages/Database'))
const PubChemPage = lazy(() => import('./pages/PubChem'))
const KitchenPage = lazy(() => import('./pages/Kitchen'))
const VitaminsPage = lazy(() => import('./pages/Vitamins'))
const AminoAcidsPage = lazy(() => import('./pages/AminoAcids'))
const TeachingPage = lazy(() => import('./pages/Teaching'))
const LoginPage = lazy(() => import('./pages/Login'))
const ProfilePage = lazy(() => import('./pages/Profile'))
const ForumPage = lazy(() => import('./pages/Forum'))
const LeaderboardPage = lazy(() => import('./pages/Leaderboard'))

const PageLoading = () => (
  <div className="mx-auto max-w-6xl px-4 py-16 text-center text-sm text-slate-400">
    页面加载中…
  </div>
)

export default function App() {
  const { pathname } = useLocation()
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <Suspense fallback={<PageLoading />}>
        <NavChrome />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/life" element={<LifeHall />} />
          <Route path="/database" element={<DatabasePage />} />
          <Route path="/pubchem" element={<PubChemPage />} />
          <Route path="/kitchen" element={<KitchenPage />} />
          <Route path="/vitamins" element={<VitaminsPage />} />
          <Route path="/amino-acids" element={<AminoAcidsPage />} />
          <Route path="/teaching" element={<TeachingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/forum" element={<ForumPage />} />
          <Route path="/leaderboard" element={<LeaderboardPage />} />
        </Routes>
      </Suspense>
      <FeedbackWidget />
      <footer className="border-t bg-slate-50">
        <div className="mx-auto max-w-3xl px-4 py-10">
          {pathname === '/' && (
            <div className="rounded-2xl bg-slate-900 px-6 py-8 text-center shadow-lg">
              <div className="text-[11px] tracking-[0.3em] text-amber-400/90">COMMUNITY · 关注拾焰集</div>
              <div className="mt-3 text-sm leading-7 text-slate-200">微信视频号 · 公众号 搜索：【拾焰集】或【拾焰集手记】</div>
              <div className="mt-1 text-xs text-slate-400">公众号 ID：shiyanjishouji · 获取更多化学灵感与更新动态</div>
            </div>
          )}
          <div className="mt-6 flex flex-col items-center justify-between gap-2 text-xs text-slate-400 sm:flex-row">
            <span>© 2026 早晨. ALL RIGHTS RESERVED.</span>
            <a href="https://beian.miit.gov.cn" target="_blank" rel="noreferrer" className="hover:text-slate-600">湘ICP备2026039674号-1</a>
          </div>
        </div>
      </footer>
    </div>
  )
}
