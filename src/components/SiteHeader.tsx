import { Link, NavLink } from 'react-router'
import { FlaskConical } from 'lucide-react'

const nav = [
  { to: '/', label: '首页' },
  { to: '/database', label: '物质成分检索库' },
  { to: '/pubchem', label: '化合物实时查询' },
  { to: '/kitchen', label: '厨房化学' },
  { to: '/vitamins', label: '维生素与化学' },
  { to: '/amino-acids', label: '氨基酸与健康' },
]

export default function SiteHeader() {
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
        </nav>
      </div>
    </header>
  )
}
