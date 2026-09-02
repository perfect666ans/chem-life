import { useEffect, useState } from 'react'
import { Link } from 'react-router'
import { Heart, MessageSquare, Pin, Search, Send, Trash2 } from 'lucide-react'
import { useAuth } from '../lib/auth'
import {
  createPost, delPost, fmtTime, getPost, likePost, listPosts, pinPost, replyPost,
  POST_TAGS, type PostBrief, type PostFull,
} from '../lib/forum'

const inputCls =
  'w-full rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100'

const TAG_COLOR: Record<string, string> = {
  学习讨论: 'bg-indigo-50 text-indigo-700',
  题目求助: 'bg-amber-50 text-amber-700',
  页面反馈: 'bg-rose-50 text-rose-700',
  心得分享: 'bg-emerald-50 text-emerald-700',
  闲聊灌水: 'bg-slate-100 text-slate-600',
}

export default function ForumPage() {
  const { user } = useAuth()
  const [posts, setPosts] = useState<PostBrief[]>([])
  const [open, setOpen] = useState<PostFull | null>(null)
  const [err, setErr] = useState('')
  const [filter, setFilter] = useState('')
  const [q, setQ] = useState('')
  const [total, setTotal] = useState(0)
  const [hasMore, setHasMore] = useState(false)

  // 发帖表单
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [tag, setTag] = useState(POST_TAGS[0])
  const [reply, setReply] = useState('')

  const load = async (offset = 0, append = false, kw = q) => {
    const r = await listPosts(kw, offset)
    if (r.ok) {
      setPosts((prev) => (append ? [...prev, ...r.posts] : r.posts))
      setTotal(r.total); setHasMore(r.hasMore)
    } else setErr(r.error || '加载失败')
  }
  const reload = () => load(0, false)
  useEffect(() => { void load(0, false, '') }, [])

  const openPost = async (id: string) => {
    const r = await getPost(id)
    if (r.ok) { setOpen(r.post); setReply('') }
  }

  const submitPost = async () => {
    setErr('')
    const r = await createPost(title, content, tag)
    if (!r.ok) return setErr(r.error || '发帖失败')
    setTitle(''); setContent('')
    void reload()
  }

  const submitReply = async () => {
    if (!open) return
    const r = await replyPost(open.id, reply)
    if (!r.ok) return setErr(r.error || '回复失败')
    setOpen(r.post); setReply('')
    void reload()
  }

  const shown = filter ? posts.filter((p) => p.tag === filter) : posts

  return (
    <div className="mx-auto max-w-4xl px-4 py-8">
      <div className="mb-6 flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">交流论坛</h1>
          <p className="mt-1 text-sm text-slate-500">讨论化学问题、反馈页面问题、分享学习心得。</p>
        </div>
        <Link to="/leaderboard" className="rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-600 hover:bg-slate-50">
          查看排行榜 →
        </Link>
      </div>

      {err && <div className="mb-4 rounded-lg bg-rose-50 px-4 py-2 text-sm text-rose-700">{err}</div>}

      {/* 发帖 */}
      {user ? (
        <section className="mb-6 rounded-xl border border-slate-200 bg-white p-5">
          <div className="mb-3 flex flex-wrap gap-2">
            {POST_TAGS.map((t) => (
              <button key={t} onClick={() => setTag(t)}
                className={`rounded-full px-3 py-1 text-xs ${tag === t ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}`}>
                {t}
              </button>
            ))}
          </div>
          <input className={inputCls} placeholder="标题（2-60 字）" value={title} onChange={(e) => setTitle(e.target.value)} />
          <textarea className={`${inputCls} mt-2 h-24 resize-y`} placeholder="内容（2-2000 字）" value={content} onChange={(e) => setContent(e.target.value)} />
          <button onClick={submitPost}
            className="mt-3 flex items-center gap-1.5 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700">
            <Send className="h-4 w-4" /> 发布
          </button>
        </section>
      ) : (
        <div className="mb-6 rounded-xl border border-dashed border-slate-300 bg-slate-50 px-5 py-4 text-sm text-slate-500">
          浏览无需登录；发帖和回复请先 <Link to="/login" className="text-indigo-600 hover:underline">登录</Link>。
        </div>
      )}

      {/* 搜索 + 筛选 */}
      <div className="mb-3 flex gap-2">
        <input className={inputCls} placeholder="搜索标题或内容…" value={q}
          onChange={(e) => setQ(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && load(0, false)} />
        <button onClick={() => load(0, false)}
          className="flex shrink-0 items-center gap-1.5 rounded-lg bg-slate-800 px-4 text-sm text-white hover:bg-slate-700">
          <Search className="h-4 w-4" /> 搜索
        </button>
      </div>
      <div className="mb-4 flex flex-wrap items-center gap-2 text-sm">
        <button onClick={() => setFilter('')}
          className={`rounded-full px-3 py-1 text-xs ${!filter ? 'bg-slate-800 text-white' : 'bg-slate-100 text-slate-600'}`}>全部</button>
        {POST_TAGS.map((t) => (
          <button key={t} onClick={() => setFilter(t)}
            className={`rounded-full px-3 py-1 text-xs ${filter === t ? 'bg-slate-800 text-white' : 'bg-slate-100 text-slate-600'}`}>{t}</button>
        ))}
        <span className="ml-auto text-xs text-slate-400">共 {total} 帖</span>
      </div>

      {/* 帖子列表 */}
      <div className="space-y-3">
        {shown.length === 0 && <div className="rounded-xl border border-slate-200 bg-white p-8 text-center text-sm text-slate-400">还没有帖子，来发第一帖吧。</div>}
        {shown.map((p) => (
          <article key={p.id} className="cursor-pointer rounded-xl border border-slate-200 bg-white p-5 transition-shadow hover:shadow-sm"
            onClick={() => openPost(p.id)}>
            <div className="flex items-center gap-2">
              <span className="text-lg">{p.author.avatar}</span>
              <span className="text-sm font-medium text-slate-800">{p.author.nickname}</span>
              {p.pinned && (
                <span className="flex items-center gap-0.5 rounded-full bg-amber-100 px-2 py-0.5 text-xs text-amber-700">
                  <Pin className="h-3 w-3" /> 置顶
                </span>
              )}
              <span className={`rounded-full px-2 py-0.5 text-xs ${TAG_COLOR[p.tag] || TAG_COLOR.闲聊灌水}`}>{p.tag}</span>
              <span className="ml-auto text-xs text-slate-400">{fmtTime(p.createdAt)}</span>
            </div>
            <h2 className="mt-2 text-base font-bold text-slate-900">{p.title}</h2>
            <p className="mt-1 line-clamp-2 text-sm text-slate-600">{p.content}</p>
            <div className="mt-2 flex items-center gap-4 text-xs text-slate-400">
              <span className="flex items-center gap-1"><Heart className="h-3.5 w-3.5" />{p.likes}</span>
              <span className="flex items-center gap-1"><MessageSquare className="h-3.5 w-3.5" />{p.replies}</span>
            </div>
          </article>
        ))}
      </div>
      {hasMore && !filter && (
        <button onClick={() => load(posts.length, true)}
          className="mt-4 w-full rounded-lg border border-slate-300 py-2.5 text-sm text-slate-600 hover:bg-slate-50">
          加载更多（已显示 {posts.length}/{total}）
        </button>
      )}

      {/* 详情抽屉 */}
      {open && (
        <div className="fixed inset-0 z-50 flex justify-end bg-black/30" onClick={() => setOpen(null)}>
          <div className="h-full w-full max-w-xl overflow-y-auto bg-white p-6 shadow-xl" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center gap-2">
              <span className="text-xl">{open.author.avatar}</span>
              <span className="font-medium text-slate-800">{open.author.nickname}</span>
              <span className={`rounded-full px-2 py-0.5 text-xs ${TAG_COLOR[open.tag] || TAG_COLOR.闲聊灌水}`}>{open.tag}</span>
              <span className="ml-auto text-xs text-slate-400">{fmtTime(open.createdAt)}</span>
            </div>
            <h2 className="mt-3 text-xl font-bold text-slate-900">{open.title}</h2>
            <p className="mt-3 whitespace-pre-wrap text-sm leading-7 text-slate-700">{open.content}</p>
            <div className="mt-4 flex items-center gap-3">
              <button
                onClick={async () => {
                  if (!user) return setErr('请先登录再点赞')
                  const r = await likePost(open.id)
                  if (r.ok) { void openPost(open.id); void reload() }
                }}
                className="flex items-center gap-1.5 rounded-lg border border-slate-300 px-3 py-1.5 text-sm text-slate-600 hover:border-rose-300 hover:text-rose-600">
                <Heart className="h-4 w-4" /> {(open.likes || []).length}
              </button>
              {user?.isAdmin && (
                <button
                  onClick={async () => {
                    const r = await pinPost(open.id)
                    if (r.ok) { void openPost(open.id); void reload() }
                  }}
                  className="flex items-center gap-1.5 rounded-lg border border-slate-300 px-3 py-1.5 text-sm text-slate-600 hover:border-amber-300 hover:text-amber-600">
                  <Pin className="h-4 w-4" /> {open.pinned ? '取消置顶' : '置顶'}
                </button>
              )}
              {user && (user.username === open.author.username || user.isAdmin) && (
                <button
                  onClick={async () => {
                    if (!confirm('删除此帖？')) return
                    const r = await delPost(open.id)
                    if (r.ok) { setOpen(null); void reload() }
                  }}
                  className="flex items-center gap-1.5 rounded-lg border border-slate-300 px-3 py-1.5 text-sm text-slate-600 hover:border-rose-300 hover:text-rose-600">
                  <Trash2 className="h-4 w-4" /> 删除
                </button>
              )}
              <button onClick={() => setOpen(null)} className="ml-auto text-sm text-slate-400 hover:text-slate-600">关闭 ✕</button>
            </div>

            <h3 className="mt-6 border-t pt-4 text-sm font-bold text-slate-900">回复（{open.replies.length}）</h3>
            <div className="mt-3 space-y-3">
              {open.replies.map((r) => (
                <div key={r.id} className="rounded-lg bg-slate-50 p-3">
                  <div className="flex items-center gap-2 text-xs text-slate-500">
                    <span>{r.author.avatar}</span><span className="font-medium text-slate-700">{r.author.nickname}</span>
                    <span className="ml-auto">{fmtTime(r.createdAt)}</span>
                  </div>
                  <p className="mt-1 whitespace-pre-wrap text-sm text-slate-700">{r.content}</p>
                </div>
              ))}
            </div>
            {user ? (
              <div className="mt-4 flex gap-2">
                <input className={inputCls} placeholder="写下你的回复…" value={reply} onChange={(e) => setReply(e.target.value)} />
                <button onClick={submitReply}
                  className="shrink-0 rounded-lg bg-indigo-600 px-4 text-sm font-medium text-white hover:bg-indigo-700">回复</button>
              </div>
            ) : (
              <p className="mt-4 text-sm text-slate-400">登录后可回复。</p>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
