import { useEffect } from 'react'

/**
 * 光晕呼吸：滚动到哪个板块，#homeRoot 的 --glow 变色（1.4s 流体过渡）
 * 挂在页面容器上，监听容器内所有 [data-glow] 板块
 */
export default function useGlowTheme(containerId = 'homeRoot') {
  useEffect(() => {
    const root = document.getElementById(containerId)
    if (!root || !('IntersectionObserver' in window)) return
    const secs = root.querySelectorAll<HTMLElement>('[data-glow]')
    const io = new IntersectionObserver((es) => {
      es.forEach((e) => {
        if (e.isIntersecting) root.style.setProperty('--glow', (e.target as HTMLElement).dataset.glow || '#2456d6')
      })
    }, { rootMargin: '-30% 0px -55% 0px' })
    secs.forEach((s) => io.observe(s))
    return () => io.disconnect()
  }, [containerId])
}
