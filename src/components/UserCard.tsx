// 个人名片弹窗：论坛/排行榜点击昵称弹出
// 显示头像、昵称、备注、标签；本人公开时长/战绩时出现「详细信息」展开区；
// 管理员额外看到 禁言/解禁 按钮
import { useEffect, useState } from 'react'
import { Ban, ChevronDown, ChevronUp, ShieldOff, X } from 'lucide-react'
import { useAuth } from '../lib/auth'
import { banUser, getUserCard, GAMES, type UserCardData } from '../lib/forum'
import UserAvatar from './UserAvatar'

const MOD_LABELS: Record<string, string> = {
  home: '首页', teaching: '模拟实验室', life: '生活探究馆', database: '成分检索库',
  kitchen: '厨房化学', vitamins: '维生素与化学', amino: '氨基酸与化学',
  pubchem: '化合物查询', forum: '交流论坛', leaderboard: '排行榜', profile: '个人中心',
}
const GAME_NAMES: Record<string, string> = Object.fromEntries(GAMES.map((g) => [g.id, g.name]))

function fmtDur(sec: number) {
  if (sec < 60) return sec + ' 秒'
  if (sec < 3600) return Math.round(sec / 60) + ' 分钟'
  return (sec / 3600).toFixed(1) + ' 小时'
}

export default function UserCard({
  username,
  onClose,
}: {
  username: string
  onClose: () => void
}) {
  const { user } = useAuth()
  const [card, setCard] = useState<UserCardData | null>(null)
  const [err, setErr] = useState('')
  const [showDetail, setShowDetail] = useState(false)
  const [banBusy, setBanBusy] = useState(false)

  const load = async () => {
    const r = await getUserCard(username)
    if (r.ok && r.card) setCard(r.card)
    else setErr(r.error || '加载失败')
  }
  useEffect(() => {
    setCard(null)
    setErr('')
    setShowDetail(false)
    void load()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [username])

  const hasDetail = !!card && (card.usage !== null || card.games !== null)

  const toggleBan = async () => {
    if (!card || banBusy) return
    setBanBusy(true)
    const r = await banUser(card.username, !card.banned)
    setBanBusy(false)
    if (r.ok) void load()
    else setErr(r.error || '操作失败')
  }

  return (
    <div
      className="fixed inset-0 z-[70] flex items-center justify-center bg-black/40 p-4"
      onClick={onClose}
    >
      <div
        className="w-full max-w-sm rounded-2xl bg-white p-6 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {err && <p className="text-center text-sm text-rose-600">{err}</p>}
        {!card && !err && <p className="py-8 text-center text-sm text-slate-400">加载中…</p>}
        {card && (
          <>
            <div className="flex items-start gap-4">
              <UserAvatar
                value={card.avatar}
                className="text-4xl"
                imgClassName="h-16 w-16 border border-slate-200"
              />
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2">
                  <span className="truncate text-lg font-bold text-slate-900">{card.nickname}</span>
                  {card.banned && (
                    <span className="shrink-0 rounded-full bg-rose-100 px-2 py-0.5 text-xs text-rose-600">
                      禁言中
                    </span>
                  )}
                </div>
                <p className="text-xs text-slate-400">@{card.username}</p>
              </div>
              <button onClick={onClose} className="text-slate-400 hover:text-slate-600">
                <X className="h-5 w-5" />
              </button>
            </div>

            {card.bio ? (
              <p className="mt-4 whitespace-pre-wrap rounded-lg bg-slate-50 px-3 py-2 text-sm text-slate-600">
                {card.bio}
              </p>
            ) : (
              <p className="mt-4 text-sm text-slate-400">这个人很低调，还没写备注。</p>
            )}

            {card.tags.length > 0 && (
              <div className="mt-3 flex flex-wrap gap-1.5">
                {card.tags.map((t) => (
                  <span
                    key={t}
                    className="rounded-full bg-indigo-50 px-2.5 py-1 text-xs text-indigo-700"
                  >
                    {t}
                  </span>
                ))}
              </div>
            )}

            {hasDetail && (
              <>
                <button
                  onClick={() => setShowDetail(!showDetail)}
                  className="mt-4 flex w-full items-center justify-center gap-1 rounded-lg border border-slate-200 py-2 text-sm text-slate-600 hover:bg-slate-50"
                >
                  {showDetail ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                  详细信息
                </button>
                {showDetail && (
                  <div className="mt-3 space-y-4 rounded-lg border border-slate-100 bg-slate-50/60 p-4">
                    {card.usage && (
                      <div>
                        <h4 className="mb-2 text-xs font-bold text-slate-500">
                          使用时长（本人公开）· 总计 {fmtDur(card.usage.total)}
                        </h4>
                        <div className="space-y-1.5">
                          {Object.entries(card.usage.byModule)
                            .sort((a, b) => b[1] - a[1])
                            .map(([k, v]) => (
                              <div key={k} className="flex justify-between text-xs text-slate-600">
                                <span>{MOD_LABELS[k] || k}</span>
                                <span className="font-mono">{fmtDur(v)}</span>
                              </div>
                            ))}
                        </div>
                      </div>
                    )}
                    {card.games && (
                      <div>
                        <h4 className="mb-2 text-xs font-bold text-slate-500">游戏战绩（本人公开）</h4>
                        {card.games.length === 0 ? (
                          <p className="text-xs text-slate-400">还没有上榜记录。</p>
                        ) : (
                          <div className="space-y-1.5">
                            {card.games.map((g) => (
                              <div key={g.game} className="flex justify-between text-xs text-slate-600">
                                <span>{GAME_NAMES[g.game] || g.game}</span>
                                <span className="font-mono">
                                  #{g.rank} · {g.score} 分
                                </span>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                )}
              </>
            )}

            {user?.isAdmin && user.username !== card.username && (
              <button
                onClick={() => void toggleBan()}
                disabled={banBusy}
                className={`mt-4 flex w-full items-center justify-center gap-1.5 rounded-lg border px-3 py-2 text-sm disabled:opacity-50 ${
                  card.banned
                    ? 'border-emerald-300 text-emerald-600 hover:bg-emerald-50'
                    : 'border-rose-300 text-rose-600 hover:bg-rose-50'
                }`}
              >
                {card.banned ? <ShieldOff className="h-4 w-4" /> : <Ban className="h-4 w-4" />}
                {card.banned ? '解除禁言' : '一键禁言'}
              </button>
            )}
          </>
        )}
      </div>
    </div>
  )
}
