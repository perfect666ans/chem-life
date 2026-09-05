import { useEffect, useState } from 'react'

const ORDER = ['dark', 'washi', 'shu'] as const
const LABEL: Record<string, string> = { dark: '暗色', washi: '和紙', shu: '朱砂' }
const KEY = 'huaxue-theme'

/** 三主题循环切换（暗色 / 和紙 / 朱砂），写入 #homeRoot 并记忆偏好 */
export default function ThemeToggle({ targetId = 'homeRoot' }: { targetId?: string }) {
  const [theme, setTheme] = useState<(typeof ORDER)[number]>('dark')

  useEffect(() => {
    let saved: string | null = null
    try { saved = localStorage.getItem(KEY) } catch { /* noop */ }
    const init = saved && (ORDER as readonly string[]).includes(saved) ? saved as (typeof ORDER)[number] : 'dark'
    setTheme(init)
    document.getElementById(targetId)?.setAttribute('data-theme', init)
  }, [targetId])

  const toggle = () => {
    const next = ORDER[(ORDER.indexOf(theme) + 1) % ORDER.length]
    setTheme(next)
    document.getElementById(targetId)?.setAttribute('data-theme', next)
    try { localStorage.setItem(KEY, next) } catch { /* noop */ }
  }

  return (
    <button className="hr-theme" onClick={toggle} title="切换主题">
      {LABEL[ORDER[(ORDER.indexOf(theme) + 1) % ORDER.length]]}
    </button>
  )
}
