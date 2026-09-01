import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router'
import { FlaskConical, KeyRound, LogIn, UserPlus } from 'lucide-react'
import { inviteStatus, login, register, useAuth } from '../lib/auth'

export default function LoginPage() {
  const { user, ready } = useAuth()
  const nav = useNavigate()
  const [tab, setTab] = useState<'login' | 'register'>('login')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [code, setCode] = useState('')
  const [msg, setMsg] = useState('')
  const [busy, setBusy] = useState(false)
  const [open, setOpen] = useState<{ open: boolean; left: number } | null>(null)

  useEffect(() => {
    void inviteStatus().then((r) => r.ok && setOpen({ open: r.open, left: r.left }))
  }, [])

  useEffect(() => {
    if (ready && user) nav('/', { replace: true })
  }, [ready, user, nav])

  const submit = async () => {
    setBusy(true)
    setMsg('')
    const r =
      tab === 'login'
        ? await login(username.trim(), password)
        : await register(username.trim(), password, code.trim())
    setBusy(false)
    if (!r.ok) {
      setMsg(r.error || '操作失败')
    } else {
      nav('/', { replace: true })
    }
  }

  const inputCls =
    'w-full rounded-lg border border-slate-300 px-3 py-2.5 text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100'

  return (
    <main className="mx-auto flex max-w-6xl justify-center px-4 py-14">
      <div className="w-full max-w-md rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <div className="mb-6 flex items-center gap-3">
          <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-600 text-white">
            <FlaskConical className="h-5 w-5" />
          </span>
          <div>
            <h1 className="text-xl font-bold text-slate-900">登录 · 生活中的化学</h1>
            <p className="text-xs text-slate-500">登录后可使用复习、游戏与社区功能</p>
          </div>
        </div>

        <div className="mb-5 grid grid-cols-2 rounded-lg bg-slate-100 p-1 text-sm">
          {(
            [
              ['login', '登录', LogIn],
              ['register', '注册', UserPlus],
            ] as const
          ).map(([k, label, Icon]) => (
            <button
              key={k}
              onClick={() => {
                setTab(k)
                setMsg('')
              }}
              className={`flex items-center justify-center gap-1.5 rounded-md py-2 transition ${
                tab === k ? 'bg-white font-medium text-indigo-700 shadow-sm' : 'text-slate-500'
              }`}
            >
              <Icon className="h-4 w-4" />
              {label}
            </button>
          ))}
        </div>

        <div className="space-y-3">
          <input
            className={inputCls}
            placeholder="账号（2-24 位字母/数字/中文）"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            className={inputCls}
            type="password"
            placeholder={tab === 'login' ? '密码' : '初始密码（管理员设置的开放密码）'}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && void submit()}
          />
          {tab === 'register' && (
            <>
              <input
                className={inputCls}
                placeholder="数字验证码（管理员在「登录权限」中设置）"
                value={code}
                onChange={(e) => setCode(e.target.value.replace(/\D/g, ''))}
                onKeyDown={(e) => e.key === 'Enter' && void submit()}
              />
              <p className={`text-xs ${open?.open ? 'text-emerald-600' : 'text-slate-400'}`}>
                {open === null
                  ? '正在查询注册开放状态…'
                  : open.open
                    ? `当前处于开放时段，剩余名额 ${open.left} 个`
                    : '当前未开放注册：需要管理员在「登录权限」中生成数字验证码并设定起效时长与人数'}
              </p>
            </>
          )}
        </div>

        {msg && <p className="mt-3 text-sm text-red-600">{msg}</p>}

        <button
          onClick={() => void submit()}
          disabled={busy || !username.trim() || !password}
          className="mt-5 flex w-full items-center justify-center gap-2 rounded-lg bg-indigo-600 py-2.5 text-sm font-medium text-white transition hover:bg-indigo-700 disabled:opacity-50"
        >
          <KeyRound className="h-4 w-4" />
          {busy ? '请稍候…' : tab === 'login' ? '登录' : '注册并登录'}
        </button>

        {tab === 'register' && (
          <p className="mt-3 text-center text-xs text-slate-400">
            首次登录后请立即前往「个人信息」修改为自己的密码，之后可随时自由登录
          </p>
        )}
        <p className="mt-4 text-center text-xs text-slate-400">
          <Link to="/" className="hover:text-indigo-600">
            ← 返回首页
          </Link>
        </p>
      </div>
    </main>
  )
}
