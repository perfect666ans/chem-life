import { useEffect, useRef } from 'react'

/** 弹簧星座粒子：鼠标挤压扩散、3-5 秒回弹重组（C-01 定稿参数） */
export default function Particles() {
  const ref = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const c = ref.current
    if (!c || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = c.getContext('2d')
    if (!ctx) return
    let W = 0, H = 0, raf = 0
    const dpr = Math.min(2, window.devicePixelRatio || 1)
    const pts: { x: number; y: number; hx: number; hy: number; vx: number; vy: number; r: number }[] = []
    let mx = -1e4, my = -1e4, vis = true

    function size() {
      const r = c!.parentElement!.getBoundingClientRect()
      W = r.width; H = r.height
      c!.width = W * dpr; c!.height = H * dpr
      ctx!.setTransform(dpr, 0, 0, dpr, 0, 0)
      pts.length = 0
      const n = Math.round(Math.min(80, (W * H) / 15000))
      for (let i = 0; i < n; i++) {
        const x = Math.random() * W, y = Math.random() * H
        pts.push({ x, y, hx: x, hy: y, vx: 0, vy: 0, r: Math.random() * 1.4 + 0.5 })
      }
    }
    size()
    window.addEventListener('resize', size)

    const parent = c.parentElement!
    const onMove = (e: MouseEvent) => { const r = c!.getBoundingClientRect(); mx = e.clientX - r.left; my = e.clientY - r.top }
    const onLeave = () => { mx = -1e4; my = -1e4 }
    parent.addEventListener('mousemove', onMove)
    parent.addEventListener('mouseleave', onLeave)

    const io = new IntersectionObserver((es) => { vis = es[0].isIntersecting })
    io.observe(c)

    const frame = () => {
      if (vis) {
        ctx!.clearRect(0, 0, W, H)
        for (const p of pts) {
          p.vx += (p.hx - p.x) * 0.0016; p.vy += (p.hy - p.y) * 0.0016
          const dx = p.x - mx, dy = p.y - my, d2 = dx * dx + dy * dy
          if (d2 < 20000) { const f = (20000 - d2) / 20000 * 0.9; p.vx += dx / Math.sqrt(d2 + 1) * f * 0.12; p.vy += dy / Math.sqrt(d2 + 1) * f * 0.12 }
          p.vx *= 0.96; p.vy *= 0.96; p.x += p.vx; p.y += p.vy
        }
        for (let i = 0; i < pts.length; i++) for (let j = i + 1; j < pts.length; j++) {
          const a = pts[i], b = pts[j], dx = a.x - b.x, dy = a.y - b.y, d = dx * dx + dy * dy
          if (d < 110 * 110) {
            ctx!.strokeStyle = `rgba(150,200,255,${(1 - Math.sqrt(d) / 110) * 0.22})`
            ctx!.beginPath(); ctx!.moveTo(a.x, a.y); ctx!.lineTo(b.x, b.y); ctx!.stroke()
          }
        }
        for (const p of pts) { ctx!.fillStyle = 'rgba(190,225,255,.85)'; ctx!.beginPath(); ctx!.arc(p.x, p.y, p.r, 0, 6.283); ctx!.fill() }
      }
      raf = requestAnimationFrame(frame)
    }
    raf = requestAnimationFrame(frame)

    return () => {
      cancelAnimationFrame(raf)
      window.removeEventListener('resize', size)
      parent.removeEventListener('mousemove', onMove)
      parent.removeEventListener('mouseleave', onLeave)
      io.disconnect()
    }
  }, [])

  return <canvas ref={ref} aria-hidden="true" />
}
