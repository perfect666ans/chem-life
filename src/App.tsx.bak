import { Suspense, lazy } from 'react'
import { Routes, Route } from 'react-router'
import SiteHeader from './components/SiteHeader'
import Home from './pages/Home'

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
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <SiteHeader />
      <Suspense fallback={<PageLoading />}>
        <Routes>
          <Route path="/" element={<Home />} />
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
      <footer className="border-t bg-white">
        <div className="mx-auto max-w-6xl px-4 py-6 text-center text-xs text-slate-400">
          生活中的化学 · 面向高中化学生活情境教学 · 内容为科普整理，涉及危险品操作请以产品说明与法规为准
        </div>
      </footer>
    </div>
  )
}
