import { useRef, type ReactNode, type CSSProperties } from 'react'
import { Link } from 'react-router'

/**
 * 3D tilt 百叶窗 + 探照灯（C-01 定稿参数：X±10° Y±12°，双层圆形光晕 140/480px）
 * 用法：内部需含 .ph 元素（探照灯跟随其定位）
 */
export default function TiltCard({ children, className = '', style, to = '#' }: { children: ReactNode; className?: string; style?: CSSProperties; to?: string }) {
  const ref = useRef<HTMLAnchorElement>(null)
  const raf = useRef(0)

  const onMove = (e: React.MouseEvent) => {
    const card = ref.current
    if (!card || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    if (!window.matchMedia('(hover:hover) and (pointer:fine)').matches) return
    const r = card.getBoundingClientRect()
    const px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height
    cancelAnimationFrame(raf.current)
    raf.current = requestAnimationFrame(() => {
      card.style.transition = 'transform .12s ease-out'
      card.style.transform = `rotateX(${((0.5 - py) * 10).toFixed(2)}deg) rotateY(${((px - 0.5) * 12).toFixed(2)}deg)`
    })
    const ph = card.querySelector<HTMLElement>('.ph')
    if (ph) {
      const ar = ph.getBoundingClientRect()
      ph.style.setProperty('--mx', `${((e.clientX - ar.left) / ar.width * 100).toFixed(1)}%`)
      ph.style.setProperty('--my', `${((e.clientY - ar.top) / ar.height * 100).toFixed(1)}%`)
    }
  }

  const onLeave = () => {
    const card = ref.current
    if (!card) return
    cancelAnimationFrame(raf.current)
    card.style.transition = 'transform .9s cubic-bezier(.16,1,.3,1)'
    card.style.transform = 'rotateX(0deg) rotateY(0deg)'
    setTimeout(() => { if (card) card.style.transition = '' }, 900)
  }

  return (
    <Link ref={ref} to={to} className={className} style={style} onMouseMove={onMove} onMouseLeave={onLeave}>
      {children}
    </Link>
  )
}
