import { useEffect, useMemo, useRef, useState } from 'react'
import { useSearchParams } from 'react-router'
import SmilesDrawer from 'smiles-drawer'
import { Pill, Droplets, FlaskConical, Sparkles, UtensilsCrossed, BookOpen, Lightbulb, Filter, Search, AlertTriangle, BookMarked } from 'lucide-react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Checkbox } from '@/components/ui/checkbox'
import { Input } from '@/components/ui/input'
import { VITAMINS, MEAL_PLANS, DIET_TAGS, VITAMIN_QUICK_REFERENCE, type Vitamin } from '@/data/vitamins'

/** 用 SMILES 在浏览器端离线绘制化学结构（数据来自 PubChem） */
function StructureView({ smiles, name, full }: { smiles: string; name: string; full: boolean }) {
  const hostRef = useRef<HTMLDivElement>(null)
  const [failed, setFailed] = useState(false)

  useEffect(() => {
    const host = hostRef.current
    if (!host) return
    host.innerHTML = ''
    setFailed(false)
    const id = 'vsvg-' + Math.random().toString(36).slice(2)
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg')
    svg.setAttribute('id', id)
    host.appendChild(svg)
    try {
      const opts: Record<string, unknown> = { width: 360, height: 280, padding: 12 }
      if (full) Object.assign(opts, { explicitHydrogens: true, terminalCarbons: true, compactDrawing: false })
      const drawer = new SmilesDrawer.SmiDrawer(opts)
      drawer.draw(smiles, '#' + id, 'light', null, () => setFailed(true))
    } catch {
      setFailed(true)
    }
  }, [smiles, full])

  if (failed) {
    return <div className="flex h-64 items-center justify-center rounded-lg bg-slate-100 text-sm text-slate-400">结构式渲染失败（{name}）</div>
  }
  return <div ref={hostRef} className="flex min-h-64 items-center justify-center overflow-hidden rounded-lg bg-white [&>svg]:max-w-full" />
}

function VitaminDetail({ v }: { v: Vitamin }) {
  const [full, setFull] = useState(false)
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex flex-wrap items-center gap-2">
          <span className="text-lg">{v.name}</span>
          <span className="text-sm font-normal text-slate-500">{v.commonName}</span>
          <span className="font-mono text-sm font-medium text-indigo-700">{v.formula}</span>
          <span className="ml-auto flex gap-1.5">
            <Badge className={v.essential ? 'bg-indigo-600' : 'bg-slate-400'}>{v.essential ? '必需维生素' : '非必需 / 类维生素'}</Badge>
            <Badge variant="secondary" className="font-normal">{v.solubilityType}</Badge>
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent className="grid gap-4 lg:grid-cols-[380px_1fr]">
        {/* 结构式 */}
        <div className="rounded-xl border bg-white p-2">
          <div className="mb-1 flex items-center justify-between px-1">
            <span className="text-xs font-medium text-slate-500">{full ? '完整结构式（显示全部原子）' : '键线式（骨架式）'}</span>
            <button
              onClick={() => setFull(!full)}
              className="rounded-md bg-indigo-50 px-2 py-1 text-xs font-medium text-indigo-700 hover:bg-indigo-100"
            >
              切换为{full ? '键线式' : '完整结构式'}
            </button>
          </div>
          <StructureView smiles={v.smiles} name={v.name} full={full} />
          <p className="px-1 pb-1 text-center text-[11px] text-slate-400">结构数据：PubChem · 浏览器端实时绘制</p>
        </div>
        {/* 信息 */}
        <div className="grid gap-2.5 text-sm leading-relaxed">
          <p className="flex gap-2"><Droplets className="mt-0.5 h-4 w-4 shrink-0 text-sky-600" /><span><b>溶解性（{v.solubilityType}）：</b>{v.solubilityReason}</span></p>
          <p className="flex gap-2"><FlaskConical className="mt-0.5 h-4 w-4 shrink-0 text-indigo-600" /><span><b>结构 / 官能团：</b>{v.structureFeatures}</span></p>
          <p className="flex gap-2"><Sparkles className="mt-0.5 h-4 w-4 shrink-0 text-amber-500" /><span><b>性质及理由：</b>{v.properties}</span></p>
          <p className="flex gap-2"><Pill className="mt-0.5 h-4 w-4 shrink-0 text-emerald-600" /><span><b>生理用途：</b>{v.role}</span></p>
          <p className="flex gap-2"><UtensilsCrossed className="mt-0.5 h-4 w-4 shrink-0 text-rose-500" /><span><b>摄入来源：</b>{v.sources}</span></p>
          <div className="mt-1 grid gap-2 rounded-lg bg-indigo-50/60 p-3 sm:grid-cols-2">
            <p><b className="text-indigo-800">每日摄入量：</b><span className="text-slate-700">{v.rni}</span></p>
            <p><b className="text-indigo-800">推荐饮食：</b><span className="text-slate-700">{v.diet}</span></p>
          </div>
          <p className="flex gap-2 rounded-lg bg-amber-50 p-3 text-amber-800"><Lightbulb className="mt-0.5 h-4 w-4 shrink-0" /><span><b>教学亮点：</b>{v.funFact}</span></p>
        </div>
      </CardContent>
    </Card>
  )
}

function VitaminsTab() {
  const [params] = useSearchParams()
  const [filter, setFilter] = useState<'全部' | '必需' | '非必需'>('全部')
  const [query, setQuery] = useState('')
  const [selectedId, setSelectedId] = useState(params.get('v') || 'C')

  useEffect(() => {
    const id = params.get('v')
    if (id && VITAMINS.some((v) => v.id === id)) setSelectedId(id)
  }, [params])

  const list = useMemo(() => {
    const q = query.trim().toLowerCase()
    return VITAMINS.filter((v) => {
      const byFilter = filter === '全部' || (filter === '必需' ? v.essential : !v.essential)
      const byQuery =
        !q ||
        [v.name, v.commonName, v.formula, v.solubilityType].some((field) => field.toLowerCase().includes(q))
      return byFilter && byQuery
    })
  }, [filter, query])
  const selected = VITAMINS.find((v) => v.id === selectedId) || VITAMINS[0]

  return (
    <div>
      <div className="flex flex-wrap items-center gap-2">
        {(['全部', '必需', '非必需'] as const).map((f) => (
          <Badge
            key={f}
            onClick={() => setFilter(f)}
            className={`cursor-pointer ${filter === f ? 'bg-indigo-600' : 'bg-slate-200 text-slate-700 hover:bg-slate-300'}`}
          >
            {f}（{f === '全部' ? VITAMINS.length : VITAMINS.filter((v) => (f === '必需' ? v.essential : !v.essential)).length}）
          </Badge>
        ))}
        <span className="ml-auto text-xs text-slate-400">脂溶性：A / D / E / K · 其余为水溶性（硫辛酸两亲）</span>
      </div>

      <div className="relative mt-3 max-w-sm">
        <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
        <Input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="搜索维生素 / 化学名 / 分子式，如 C、叶酸、C₆H₈O₆"
          className="bg-white pl-9"
        />
      </div>

      <div className="mt-4 flex flex-wrap gap-2">
        {list.map((v) => (
          <button
            key={v.id}
            onClick={() => setSelectedId(v.id)}
            className={`rounded-lg border px-3 py-1.5 text-sm transition-colors ${
              selected.id === v.id
                ? 'border-indigo-600 bg-indigo-600 text-white'
                : 'border-slate-200 bg-white text-slate-700 hover:border-indigo-300 hover:text-indigo-700'
            }`}
          >
            {v.name}
          </button>
        ))}
      </div>

      <div className="mt-4">
        <VitaminDetail v={selected} />
      </div>

      <Card className="mt-6 border-indigo-100 bg-indigo-50/50">
        <CardContent className="flex items-start gap-2 p-4 text-sm leading-relaxed text-slate-700">
          <BookOpen className="mt-0.5 h-4 w-4 shrink-0 text-indigo-600" />
          <span>
            <b>授课动线建议：</b>以"溶解性"为总纲——为什么 B、C 族吃多了能随尿排出（水溶性）而 A、D 过量会中毒（脂溶性蓄积）？
            答案写在结构里：数羟基、看碳链。官能团 → 性质 → 用途，正是本模块每个条目都遵循的化学思维主线。
            摄入量数据参考《中国居民膳食营养素参考摄入量（2023 版）》，个体需求请遵医嘱。
          </span>
        </CardContent>
      </Card>
    </div>
  )
}

function MealPlansTab() {
  const [avoid, setAvoid] = useState<string[]>([])

  const toggle = (t: string) =>
    setAvoid((prev) => (prev.includes(t) ? prev.filter((x) => x !== t) : [...prev, t]))

  const matched = useMemo(
    () => MEAL_PLANS.filter((p) => avoid.every((a) => p.tags.includes(a))),
    [avoid]
  )

  return (
    <div>
      <Card className="border-indigo-100 bg-indigo-50/50">
        <CardContent className="p-4">
          <p className="flex items-center gap-2 font-medium text-slate-900"><Filter className="h-4 w-4 text-indigo-600" /> 勾选你的忌口 / 习惯，自动匹配可执行的食谱组合</p>
          <div className="mt-3 flex flex-wrap gap-x-5 gap-y-2">
            {DIET_TAGS.map((t) => (
              <label key={t} className="flex cursor-pointer items-center gap-2 text-sm text-slate-700">
                <Checkbox checked={avoid.includes(t)} onCheckedChange={() => toggle(t)} />
                {t}
              </label>
            ))}
          </div>
        </CardContent>
      </Card>

      <p className="mt-4 text-sm text-slate-500">
        匹配到 <b className="text-indigo-700">{matched.length}</b> / {MEAL_PLANS.length} 种组合
        {avoid.length > 0 && <span>（已选：{avoid.join('、')}）</span>}
      </p>

      <div className="mt-3 grid gap-4 lg:grid-cols-2">
        {matched.map((p) => (
          <Card key={p.name} className="transition-shadow hover:shadow-md">
            <CardHeader className="pb-2">
              <CardTitle className="flex flex-wrap items-center gap-2 text-base">
                <UtensilsCrossed className="h-4 w-4 text-indigo-600" />
                {p.name}
                <span className="text-xs font-normal text-slate-400">{p.audience}</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="grid gap-1.5 text-sm leading-relaxed text-slate-600">
              <p><b className="text-slate-800">早餐：</b>{p.breakfast}</p>
              <p><b className="text-slate-800">午餐：</b>{p.lunch}</p>
              <p><b className="text-slate-800">晚餐：</b>{p.dinner}</p>
              <p><b className="text-slate-800">加餐：</b>{p.snack}</p>
              <p className="mt-1 rounded-lg bg-emerald-50 p-2.5 text-xs leading-relaxed text-emerald-800">
                <b>维生素覆盖：</b>{p.coverage}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {matched.length === 0 && (
        <p className="mt-10 text-center text-slate-400">当前忌口组合暂无完全匹配的食谱，试着减少一两个条件</p>
      )}
    </div>
  )
}

function ReferenceTab() {
  const [, setParams] = useSearchParams()
  return (
    <div className="grid gap-4">
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="flex items-center gap-2 text-base">
            <AlertTriangle className="h-4 w-4 text-amber-600" /> 必需维生素：缺乏 / 过量速查
          </CardTitle>
        </CardHeader>
        <CardContent className="grid gap-3">
          <div className="hidden grid-cols-[120px_1fr_1fr_1.2fr] gap-3 rounded-lg bg-slate-100 px-3 py-2 text-xs font-medium text-slate-500 md:grid">
            <span>维生素</span><span>典型缺乏表现</span><span>过量风险 / 注意</span><span>课堂追问（化学点）</span>
          </div>
          {VITAMIN_QUICK_REFERENCE.map((r) => {
            const v = VITAMINS.find((x) => x.id === r.id)
            if (!v) return null
            return (
              <div key={r.id} className="grid gap-2 rounded-xl border bg-white p-3 text-sm leading-relaxed md:grid-cols-[120px_1fr_1fr_1.2fr] md:gap-3">
                <div>
                  <button
                    onClick={() => setParams({ tab: 'vitamins', v: r.id })}
                    className="font-medium text-indigo-700 hover:underline"
                  >
                    {v.name}
                  </button>
                  <span className={`ml-2 rounded-full px-2 py-0.5 text-[11px] ${v.solubilityType === '脂溶性' ? 'bg-amber-100 text-amber-700' : 'bg-sky-100 text-sky-700'}`}>
                    {v.solubilityType}
                  </span>
                </div>
                <p className="text-slate-600"><b className="text-slate-800 md:hidden">缺乏：</b>{r.deficiency}</p>
                <p className="text-slate-600"><b className="text-slate-800 md:hidden">过量：</b>{r.overdose}</p>
                <p className="rounded-lg bg-indigo-50/70 p-2 text-xs leading-relaxed text-indigo-800">{r.classPoint}</p>
              </div>
            )
          })}
        </CardContent>
      </Card>

      <Card className="border-indigo-100 bg-indigo-50/50">
        <CardContent className="flex items-start gap-2 p-4 text-sm leading-relaxed text-slate-700">
          <BookMarked className="mt-0.5 h-4 w-4 shrink-0 text-indigo-600" />
          <span>
            <b>数据来源与使用边界：</b>结构绘制使用 PubChem ConnectivitySMILES 并在浏览器端离线渲染；摄入量主要参考
            《中国居民膳食营养素参考摄入量（2023 版）》。本模块用于高中化学情境教学，不构成医疗建议；孕期、慢性病、服药人群的补充剂使用请遵医嘱。
          </span>
        </CardContent>
      </Card>
    </div>
  )
}

export default function VitaminsPage() {
  const [params, setParams] = useSearchParams()
  const tab = params.get('tab') || 'vitamins'

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-6xl px-4 py-8">
        <h1 className="flex items-center gap-2 text-2xl font-bold text-slate-900">
          <Pill className="h-6 w-6 text-indigo-600" /> 维生素与化学
        </h1>
        <p className="mt-1 text-sm text-slate-500">
          13 种必需 + 6 种类维生素：结构式 / 键线式、溶解性与性质的结构解释、摄入量与 {MEAL_PLANS.length} 种可筛选食谱组合；附缺乏 / 过量速查
        </p>
        <Tabs value={tab} onValueChange={(v) => setParams({ tab: v })} className="mt-6">
          <TabsList>
            <TabsTrigger value="vitamins">维生素详解</TabsTrigger>
            <TabsTrigger value="meals">综合食谱推荐</TabsTrigger>
            <TabsTrigger value="reference">缺乏 / 过量速查</TabsTrigger>
          </TabsList>
          <TabsContent value="vitamins" className="mt-4"><VitaminsTab /></TabsContent>
          <TabsContent value="meals" className="mt-4"><MealPlansTab /></TabsContent>
          <TabsContent value="reference" className="mt-4"><ReferenceTab /></TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
