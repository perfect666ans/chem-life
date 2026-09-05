import { useEffect, useRef, type ReactNode } from 'react'

/**
 * 滑窗式横滑条（C-01 定稿手感）：
 * - 区域内按住拖动：1:1 直接跟随，停哪算哪（任意小数位置）
 * - 快速甩动：惯性滑行（90% 衰减），到端点网球式弹簧回弹
 * - 底部细白条：拖 thumb / 点轨道，全部走同一惯性通道
 */
export default function HScroller({ children }: { children: ReactNode }) {
  const hs = useRef<HTMLDivElement>(null)
  const bar = useRef<HTMLDivElement>(null)
  const th = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const el = hs.current, track = bar.current, thumb = th.current
    if (!el || !track || !thumb) return
    const hsEl = el, trackEl = track, thumbEl = thumb
    let current = 0, vel = 0, dragging = false, tdragging = false, bounceEdge: number | null = null
    let sx = 0, scur = 0, lastX = 0, lastT = 0, tx = 0, tleft = 0, moved = 0, gt = 0

    const maxS = () => Math.max(0, hsEl.scrollWidth - hsEl.clientWidth)
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches

    function syncBar() {
      const m = maxS(), bw = track!.clientWidth
      const ratio = m > 0 ? hsEl.clientWidth / hsEl.scrollWidth : 1
      const tw = Math.max(30, bw * ratio)
      thumb!.style.width = `${tw}px`
      thumb!.style.left = `${m > 0 ? (current / m) * Math.max(0, bw - tw) : 0}px`
    }
    function glideTo(dest: number) {
      cancelAnimationFrame(gt)
      const step = () => {
        const d = dest - current
        if (Math.abs(d) < 0.5) { current = dest; return }
        current += d * 0.18; gt = requestAnimationFrame(step)
      }
      step()
    }

    function frame() {
      const m = maxS()
      if (!dragging && !tdragging) {
        if (bounceEdge !== null) {
          vel += -(current - bounceEdge) * 0.085 - vel * 0.085
          current += vel
          if (Math.abs(vel) < 0.25 && Math.abs(current - bounceEdge) < 0.4) { current = bounceEdge; vel = 0; bounceEdge = null }
        } else if (current < 0 || current > m) {
          bounceEdge = current < 0 ? 0 : m
          if (Math.abs(vel) < 1.5) vel = current < 0 ? -Math.min(4, (0 - current) * 0.06) : Math.min(4, (current - m) * 0.06)
        } else if (Math.abs(vel) > 0.3) {
          current += vel; vel *= 0.9
          if (current <= 0) { current = 0; bounceEdge = 0; if (Math.abs(vel) <= 2.5) vel = 0 }
          if (current >= m) { current = m; bounceEdge = m; if (Math.abs(vel) <= 2.5) vel = 0 }
        } else vel = 0
      }
      hsEl.scrollLeft = current
      syncBar()
      requestAnimationFrame(frame)
    }
    const raf = requestAnimationFrame(frame)

    const down = (e: PointerEvent) => {
      if (e.pointerType === 'mouse' && e.button !== 0) return
      dragging = true; vel = 0; moved = 0; sx = e.clientX; scur = current
      lastX = e.clientX; lastT = performance.now()
      try { hsEl.setPointerCapture(e.pointerId) } catch { /* noop */ }
      hsEl.style.cursor = 'grabbing'
    }
    const move = (e: PointerEvent) => {
      if (!dragging) return
      const dx = sx - e.clientX; moved = Math.max(moved, Math.abs(dx))
      const m = maxS()
      let next = scur + dx
      if (next < 0) next *= 0.35; else if (next > m) next = m + (next - m) * 0.35
      current = next
      const now = performance.now(), dt = Math.max(1, now - lastT)
      const v = ((lastX - e.clientX) / dt) * 16
      vel = vel * 0.5 + v * 0.5; lastX = e.clientX; lastT = now
    }
    const up = () => {
      if (!dragging) return
      dragging = false; hsEl.style.cursor = ''
      const m = maxS()
      if (current < 0 || current > m) { if (Math.abs(vel) < 2) vel = current < 0 ? -2.2 : 2.2; return }
      if (Math.abs(vel) < 3 || reduce) vel = 0
    }
    const suppressClick = (e: Event) => { if (moved > 6) { e.preventDefault(); e.stopPropagation() } }

    hsEl.addEventListener('pointerdown', down)
    hsEl.addEventListener('pointermove', move)
    hsEl.addEventListener('pointerup', up)
    hsEl.addEventListener('pointercancel', up)
    hsEl.addEventListener('click', suppressClick, true)

    const tdown = (e: PointerEvent) => {
      tdragging = true; tx = e.clientX; tleft = parseFloat(thumbEl.style.left || '0')
      try { thumbEl.setPointerCapture(e.pointerId) } catch { /* noop */ }
      e.preventDefault(); e.stopPropagation()
    }
    const tmove = (e: PointerEvent) => {
      if (!tdragging) return
      const bw = trackEl.clientWidth, tw = thumbEl.clientWidth, m = maxS()
      const nl = Math.min(Math.max(tleft + (e.clientX - tx), 0), bw - tw)
      if (m > 0 && bw > tw) current = (nl / (bw - tw)) * m
    }
    const tUp = () => { tdragging = false }
    const bdown = (e: PointerEvent) => {
      if (e.target === thumb) return
      const r = trackEl.getBoundingClientRect(), tw = thumbEl.clientWidth, bw = trackEl.clientWidth, m = maxS()
      const nl = Math.min(Math.max(e.clientX - r.left - tw / 2, 0), bw - tw)
      if (m > 0 && bw > tw) glideTo((nl / (bw - tw)) * m)
    }

    thumb.addEventListener('pointerdown', tdown)
    window.addEventListener('pointermove', tmove)
    window.addEventListener('pointerup', tUp)
    track.addEventListener('pointerdown', bdown)
    const onResize = () => { const m = maxS(); if (current > m) current = m }
    window.addEventListener('resize', onResize)

    return () => {
      cancelAnimationFrame(raf); cancelAnimationFrame(gt)
      hsEl.removeEventListener('pointerdown', down)
      hsEl.removeEventListener('pointermove', move)
      hsEl.removeEventListener('pointerup', up)
      hsEl.removeEventListener('pointercancel', up)
      hsEl.removeEventListener('click', suppressClick, true)
      thumb.removeEventListener('pointerdown', tdown)
      window.removeEventListener('pointermove', tmove)
      window.removeEventListener('pointerup', tUp)
      track.removeEventListener('pointerdown', bdown)
      window.removeEventListener('resize', onResize)
    }
  }, [])

  return (
    <>
      <div className="hr-hs" ref={hs}>{children}</div>
      <div className="hr-hsbar" ref={bar}><div className="th" ref={th} /></div>
    </>
  )
}
