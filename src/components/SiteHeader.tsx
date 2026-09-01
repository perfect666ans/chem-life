import { Link, NavLink } from 'react-router'
import { FlaskConical, KeyRound, UserRound } from 'lucide-react'
import { useAuth } from '../lib/auth'

const nav = [
  { to: '/', label: '首页' },
  { to: '/database', label: '物质成分检索库' },
  { to: '/pubchem', label: '化合物实时查询' },
  { to: '/kitchen', label: '厨房化学' },
  { to: '/vitamins', label: '维生素与化学' },
  { to: '/amino-acids', label: '氨基酸与健康' },
  { to: '/teaching', label: '教学实验室' },
  { to: '/forum', label: '交流论坛' },
  { to: '/leaderboard', label: '排行榜' },
]

export default function SiteHeader() {
  const { user } = useAuth()
  return (
    <header className="sticky top-0 z-40 border-b bg-white/90 backdrop-blur">
      <div className="mx-auto flex min-h-14 flex-wrap items-center gap-x-4 gap-y-1 px-4 py-2 max-w-6xl">
        <Link to="/" className="flex items-center gap-2 font-bold text-slate-900">
          <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-indigo-600 text-white">
            <FlaskConical className="h-4 w-4" />
          </span>
          <span className="whitespace-nowrap text-base sm:text-lg">生活中的化学</span>
        </Link>
        <nav className="ml-auto flex flex-wrap items-center gap-1">
          {nav.map((n) => (
            <NavLink
              key={n.to}
              to={n.to}
              end={n.to === '/'}
              className={({ isActive }) =>
                `whitespace-nowrap rounded-md px-2 py-1.5 text-sm transition-colors sm:px-3 ${
                  isActive
                    ? 'bg-indigo-50 font-medium text-indigo-700'
                    : 'text-slate-600 hover:bg-slate-100'
                }`
              }
            >
              {n.label}
            </NavLink>
          ))}
          {user ? (
            <NavLink
              to="/profile"
              className={({ isActive }) =>
                `ml-1 flex items-center gap-1.5 whitespace-nowrap rounded-md border px-2.5 py-1.5 text-sm transition-colors ${
                  isActive
                    ? 'border-indigo-300 bg-indigo-50 font-medium text-indigo-700'
                    : 'border-slate-300 text-slate-600 hover:bg-slate-100'
                }`
              }
            >
              <span>{user.avatar}</span>
              {user.isAdmin ? (
                <>
                  <KeyRound className="h-3.5 w-3.5" />
                  登录权限
                </>
              ) : (
                <>
                  <UserRound className="h-3.5 w-3.5" />
                  个人信息
                </>
              )}
            </NavLink>
          ) : (
            <NavLink
              to="/login"
              className={({ isActive }) =>
                `ml-1 whitespace-nowrap rounded-md px-2.5 py-1.5 text-sm font-medium transition-colors ${
                  isActive ? 'bg-indigo-600 text-white' : 'bg-indigo-600/90 text-white hover:bg-indigo-600'
                }`
              }
            >
              登录
            </NavLink>
          )}
        </nav>
      </div>
    </header>
  )
}
