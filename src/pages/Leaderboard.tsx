import { useEffect, useState } from 'react'
import { Link } from 'react-router'
import { Trophy } from 'lucide-react'
import { GAMES, fmtTime, getBoard, type BoardRow } from '../lib/forum'

const MEDAL = ['🥇', '🥈', '🥉']

export default function LeaderboardPage() {
  const [game, setGame] = useState<string>(GAMES[0].id)
  const [rows, setRows] = useState<BoardRow[]>([])
  const [total, setTotal] = useState(0)
  const [err, setErr] = useState('')

  useEffect(() => {
    setErr('')
    void (async () => {
      const r = await getBoard(game)
      if (r.ok) { setRows(r.rows); setTotal(r.total) }
      else setErr(r.error || '加载失败')
    })()
  }, [game])

  const g = GAMES.find((x) => x.id === game)!

  return (
    <div className="mx-auto max-w-3xl px-4 py-8">
      <div className="mb-6 flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="flex items-center gap-2 text-2xl font-bold text-slate-900">
            <Trophy className="h-6 w-6 text-amber-500" /> 排行榜 / 统计
          </h1>
          <p className="mt-1 text-sm text-slate-500">
            游戏板块各模块最好成绩榜。登录后玩游戏，成绩会自动上报（只保留每人最高纪录）。
          </p>
        </div>
        <Link to="/forum" className="rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-600 hover:bg-slate-50">
          前往论坛 →
        </Link>
      </div>

      <div className="mb-5 flex flex-wrap gap-2">
        {GAMES.map((x) => (
          <button key={x.id} onClick={() => setGame(x.id)}
            className={`rounded-full px-4 py-1.5 text-sm ${game === x.id ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}`}>
            {x.name}
          </button>
        ))}
      </div>

      {err && <div className="mb-4 rounded-lg bg-rose-50 px-4 py-2 text-sm text-rose-700">{err}</div>}

      <div className="overflow-hidden rounded-xl border border-slate-200 bg-white">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b bg-slate-50 text-left text-xs text-slate-500">
              <th className="px-4 py-3 font-medium">名次</th>
              <th className="px-4 py-3 font-medium">玩家</th>
              <th className="px-4 py-3 font-medium">最好成绩</th>
              <th className="px-4 py-3 font-medium">达成时间</th>
            </tr>
          </thead>
          <tbody>
            {rows.length === 0 && (
              <tr><td colSpan={4} className="px-4 py-10 text-center text-slate-400">
                还没有人上榜。去<a className="text-indigo-600 hover:underline" href="/teaching">教学实验室</a>的游戏板块冲个纪录吧！
              </td></tr>
            )}
            {rows.map((r, i) => (
              <tr key={r.username} className="border-b last:border-0">
                <td className="px-4 py-3">{MEDAL[i] || i + 1}</td>
                <td className="px-4 py-3">
                  <span className="mr-2">{r.avatar}</span>
                  <span className="font-medium text-slate-800">{r.nickname}</span>
                </td>
                <td className="px-4 py-3 font-mono font-bold text-indigo-700">
                  {r.score} <span className="text-xs font-normal text-slate-400">{g.unit}</span>
                </td>
                <td className="px-4 py-3 text-xs text-slate-400">{fmtTime(r.at)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="mt-3 text-xs text-slate-400">共 {total} 位玩家上榜 · 榜单展示前 20 名 · 使用时长与游戏时长可在「个人信息」中自主选择是否公开（即将上线）。</p>
    </div>
  )
}
