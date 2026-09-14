// 右下角「反馈」悬浮按钮 + 留言弹窗（全站挂载，主题色）
// 留言进后端留言箱，仅本人（登录时）与管理员可见，不公开
import { useState } from 'react'
import { MessageSquareText, Send, X } from 'lucide-react'
import { sendFeedback } from '../lib/forum'

export default function FeedbackWidget() {
  const [open, setOpen] = useState(false)
  const [content, setContent] = useState('')
  const [contact, setContact] = useState('')
  const [busy, setBusy] = useState(false)
  const [tip, setTip] = useState<{ text: string; ok: boolean } | null>(null)

  const submit = async () => {
    if (busy) return
    if (content.trim().length < 2) {
      setTip({ text: '留言至少写 2 个字哦', ok: false })
      return
    }
    setBusy(true)
    const r = await sendFeedback(content.trim(), contact.trim(), location.pathname)
    setBusy(false)
    if (r.ok) {
      setTip({ text: '已收到你的留言，感谢反馈 ✓', ok: true })
      setContent('')
      setContact('')
      setTimeout(() => {
        setOpen(false)
        setTip(null)
      }, 1000)
    } else {
      setTip({ text: r.error || '提交失败，请稍后再试', ok: false })
    }
  }

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        title="意见反馈"
        style={{
          position: 'fixed', right: 20, bottom: 76, zIndex: 60,
          padding: '10px 14px', borderRadius: 999, border: 'none', cursor: 'pointer',
          display: 'flex', alignItems: 'center', gap: 6,
          background: '#4f46e5', color: '#fff', fontSize: 13, fontWeight: 500,
          boxShadow: '0 8px 24px rgba(79,70,229,.4)',
          transition: 'transform .1s',
        }}
        onMouseDown={(e) => (e.currentTarget.style.transform = 'scale(.93)')}
        onMouseUp={(e) => (e.currentTarget.style.transform = 'scale(1)')}
      >
        <MessageSquareText style={{ width: 16, height: 16 }} />
        反馈
      </button>

      {open && (
        <div
          className="fixed inset-0 z-[80] flex items-end justify-center bg-black/40 p-4 sm:items-center"
          onClick={() => setOpen(false)}
        >
          <div
            className="w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between">
              <h3 className="flex items-center gap-2 text-base font-bold text-slate-900">
                <MessageSquareText className="h-5 w-5 text-indigo-600" />
                给我们留言
              </h3>
              <button onClick={() => setOpen(false)} className="text-slate-400 hover:text-slate-600">
                <X className="h-5 w-5" />
              </button>
            </div>
            <p className="mt-2 text-xs leading-5 text-slate-500">
              遇到问题、有建议，或者想吐槽某个页面，都可以写下来。留言只有你自己和管理员能看到，不会公开显示。
            </p>
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="想说的话…（2-500 字）"
              className="mt-4 h-28 w-full resize-none rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100"
            />
            <input
              value={contact}
              onChange={(e) => setContact(e.target.value)}
              placeholder="联系方式（选填，方便我们回复你）"
              className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100"
            />
            {tip && (
              <p className={`mt-2 text-sm ${tip.ok ? 'text-emerald-600' : 'text-rose-600'}`}>{tip.text}</p>
            )}
            <button
              onClick={() => void submit()}
              disabled={busy}
              className="mt-4 flex w-full items-center justify-center gap-1.5 rounded-lg bg-indigo-600 py-2.5 text-sm font-medium text-white transition hover:bg-indigo-700 active:scale-95 disabled:opacity-50"
            >
              <Send className="h-4 w-4" />
              {busy ? '提交中…' : '提交留言'}
            </button>
          </div>
        </div>
      )}
    </>
  )
}
