import { useMemo, useState } from 'react'
import { useSearchParams } from 'react-router'
import { Dumbbell, HeartPulse, FlaskConical, Filter, UtensilsCrossed, CalendarDays, Repeat, BookOpen, Search, Beaker } from 'lucide-react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Checkbox } from '@/components/ui/checkbox'
import { Input } from '@/components/ui/input'
import { AMINO_ACIDS, PROTEIN_PRINCIPLES, GOAL_MODES, PROTEIN_TAGS, PROTEIN_RECIPES, WEEKLY_PLAN, MONTHLY_PLAN } from '@/data/aminoAcids'

function ModeCard({ mode }: { mode: 'health' | 'muscle' }) {
  const goal = GOAL_MODES.find((g) => g.key === mode) || GOAL_MODES[0]
  const Icon = mode === 'muscle' ? Dumbbell : HeartPulse
  return (
    <Card className="border-slate-200 bg-white">
      <CardContent className="grid gap-3 p-5 sm:grid-cols-[auto_1fr]">
        <span className={`flex h-12 w-12 items-center justify-center rounded-2xl ${mode === 'muscle' ? 'bg-amber-100 text-amber-700' : 'bg-emerald-100 text-emerald-700'}`}>
          <Icon className="h-6 w-6" />
        </span>
        <div>
          <div className="flex flex-wrap items-center gap-2">
            <h2 className="text-lg font-bold text-slate-900">{goal.label}</h2>
            <Badge variant="secondary">{goal.target}</Badge>
          </div>
          <p className="mt-2 text-sm leading-relaxed text-slate-600"><b>蛋白目标：</b>{goal.protein}</p>
          <ul className="mt-2 grid gap-1 text-sm leading-relaxed text-slate-600 sm:grid-cols-2">
            {goal.focus.map((f) => <li key={f}>· {f}</li>)}
          </ul>
        </div>
      </CardContent>
    </Card>
  )
}

function PrincipleTab({ mode }: { mode: 'health' | 'muscle' }) {
  const [group, setGroup] = useState<'全部' | '必需' | '可合成'>('全部')
  const list = useMemo(() => AMINO_ACIDS.filter((a) => {
    if (group === '必需') return a.group === '必需氨基酸'
    if (group === '可合成') return a.group !== '必需氨基酸'
    return true
  }), [group])
  const essential = AMINO_ACIDS.filter((a) => a.group === '必需氨基酸')

  return (
    <div className="grid gap-4">
      <ModeCard mode={mode} />

      <div className="grid gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-base"><FlaskConical className="h-4 w-4 text-indigo-600" /> 人体如何利用氨基酸：从食物到自身蛋白质</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-3 sm:grid-cols-2">
            {PROTEIN_PRINCIPLES.map((p) => (
              <div key={p.title} className="rounded-xl border bg-white p-4">
                <p className="font-medium text-slate-900">{p.title}</p>
                <p className="mt-1 text-sm leading-relaxed text-slate-600">{p.detail}</p>
                <p className="mt-2 rounded-lg bg-indigo-50/70 p-2 text-xs leading-relaxed text-indigo-800">{p.point}</p>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-base"><Beaker className="h-4 w-4 text-teal-600" /> 能不能自身合成？</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-3 text-sm leading-relaxed text-slate-600">
            <p><b className="text-slate-900">不能自身合成（9 种必需）：</b>{essential.map((a) => a.name).join('、')}。必须从食物蛋白获取。</p>
            <p><b className="text-slate-900">可自身合成：</b>丙氨酸、天冬酰胺、天冬氨酸、谷氨酸、甘氨酸、脯氨酸、丝氨酸等，原料多来自糖代谢/三羧酸循环中间体。</p>
            <p><b className="text-slate-900">条件性必需：</b>精氨酸、半胱氨酸、谷氨酰胺、酪氨酸在婴幼儿、创伤、高强度训练或特殊疾病状态下可能不够。</p>
            <p className="rounded-lg bg-amber-50 p-3 text-amber-800">半胱氨酸虽能合成，但硫来自必需氨基酸甲硫氨酸；酪氨酸虽能合成，但原料苯丙氨酸仍是必需氨基酸——“能合成”不等于“原料免费”。</p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="flex flex-wrap items-center gap-2 text-base">
            <BookOpen className="h-4 w-4 text-indigo-600" /> 20 种蛋白质氨基酸速查
            <span className="ml-auto flex gap-2">
              {(['全部', '必需', '可合成'] as const).map((g) => (
                <Badge key={g} onClick={() => setGroup(g)} className={`cursor-pointer ${group === g ? 'bg-indigo-600' : 'bg-slate-200 text-slate-700 hover:bg-slate-300'}`}>{g}</Badge>
              ))}
            </span>
          </CardTitle>
        </CardHeader>
        <CardContent className="grid gap-3">
          {list.map((a) => (
            <div key={a.id} className="grid gap-2 rounded-xl border bg-white p-4 text-sm leading-relaxed lg:grid-cols-[190px_1fr_1fr_1.2fr] lg:gap-4">
              <div>
                <p className="font-medium text-slate-900">{a.name} <span className="font-mono text-xs text-slate-400">{a.abbr3}/{a.abbr1}</span></p>
                <div className="mt-1 flex flex-wrap gap-1">
                  <Badge className={a.group === '必需氨基酸' ? 'bg-indigo-600' : a.group === '条件性必需' ? 'bg-amber-500' : 'bg-slate-400'}>{a.group}</Badge>
                </div>
              </div>
              <p className="text-slate-600"><b className="text-slate-800">能否合成：</b>{a.canSynthesize}<br /><b className="text-slate-800">原料/路径：</b>{a.rawMaterials}</p>
              <p className="text-slate-600"><b className="text-slate-800">功能：</b>{a.role}<br /><b className="text-slate-800">食物来源：</b>{a.food}</p>
              <p className="rounded-lg bg-indigo-50/60 p-2 text-xs leading-relaxed text-indigo-800">{a.classPoint}</p>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  )
}

function RecipesTab({ mode }: { mode: 'health' | 'muscle' }) {
  const [avoid, setAvoid] = useState<string[]>([])
  const [meal, setMeal] = useState<'全部' | '早餐' | '午餐' | '晚餐' | '加餐' | '训练后'>('全部')
  const [query, setQuery] = useState('')
  const toggle = (t: string) => setAvoid((prev) => (prev.includes(t) ? prev.filter((x) => x !== t) : [...prev, t]))
  const goalLabel = mode === 'muscle' ? '增肌' : '健康'

  const matched = useMemo(() => {
    const q = query.trim().toLowerCase()
    return PROTEIN_RECIPES.filter((p) => {
      const byGoal = p.goal.includes(goalLabel as '健康' | '增肌')
      const byMeal = meal === '全部' || p.meal === meal
      const byTags = avoid.every((a) => p.tags.includes(a))
      const byQuery = !q || [p.name, p.ingredients, p.steps, p.meal].some((x) => x.toLowerCase().includes(q))
      return byGoal && byMeal && byTags && byQuery
    })
  }, [avoid, meal, query, goalLabel])

  return (
    <div className="grid gap-4">
      <Card className="border-indigo-100 bg-indigo-50/50">
        <CardContent className="p-4">
          <p className="flex items-center gap-2 font-medium text-slate-900"><Filter className="h-4 w-4 text-indigo-600" /> 当前模式：{goalLabel} · 勾选忌口/场景自动匹配</p>
          <div className="mt-3 flex flex-wrap gap-x-5 gap-y-2">
            {PROTEIN_TAGS.map((t) => (
              <label key={t} className="flex cursor-pointer items-center gap-2 text-sm text-slate-700">
                <Checkbox checked={avoid.includes(t)} onCheckedChange={() => toggle(t)} />
                {t}
              </label>
            ))}
          </div>
          <div className="mt-3 grid gap-2 sm:grid-cols-[220px_1fr]">
            <div className="flex flex-wrap gap-2">
              {(['全部', '早餐', '午餐', '晚餐', '加餐', '训练后'] as const).map((m) => (
                <Badge key={m} onClick={() => setMeal(m)} className={`cursor-pointer ${meal === m ? 'bg-slate-900' : 'bg-white text-slate-700 hover:bg-slate-100'}`}>{m}</Badge>
              ))}
            </div>
            <div className="relative">
              <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
              <Input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="搜索食材/菜名，如 鸡胸、豆腐、纯素、训练后" className="bg-white pl-9" />
            </div>
          </div>
        </CardContent>
      </Card>

      <p className="text-sm text-slate-500">匹配到 <b className="text-indigo-700">{matched.length}</b> / {PROTEIN_RECIPES.length} 种蛋白质食谱{avoid.length > 0 && <span>（已选：{avoid.join('、')}）</span>}</p>

      <div className="grid gap-4 lg:grid-cols-2">
        {matched.map((p) => (
          <Card key={p.name} className="transition-shadow hover:shadow-md">
            <CardHeader className="pb-2">
              <CardTitle className="flex flex-wrap items-center gap-2 text-base">
                <UtensilsCrossed className="h-4 w-4 text-indigo-600" /> {p.name}
                <Badge variant="secondary" className="font-normal">{p.meal}</Badge>
                <span className="ml-auto rounded-full bg-emerald-50 px-2 py-0.5 text-xs font-medium text-emerald-700">约 {p.protein} g 蛋白</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="grid gap-1.5 text-sm leading-relaxed text-slate-600">
              <p><b className="text-slate-800">食材：</b>{p.ingredients}</p>
              <p><b className="text-slate-800">做法：</b>{p.steps}</p>
              <div className="mt-1 flex flex-wrap gap-1">
                {p.tags.map((t) => <Badge key={t} variant="outline" className="font-normal">{t}</Badge>)}
                {p.goal.map((g) => <Badge key={g} className={g === '增肌' ? 'bg-amber-500' : 'bg-emerald-600'}>{g}</Badge>)}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {matched.length === 0 && <p className="py-10 text-center text-slate-400">当前条件暂无完全匹配，试着减少忌口或切换餐次</p>}
    </div>
  )
}

function PlanTab({ mode }: { mode: 'health' | 'muscle' }) {
  return (
    <div className="grid gap-4">
      <ModeCard mode={mode} />
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="flex items-center gap-2 text-base"><CalendarDays className="h-4 w-4 text-indigo-600" /> 每周训练 + 食物搭配</CardTitle>
        </CardHeader>
        <CardContent className="grid gap-3">
          {WEEKLY_PLAN.map((w) => (
            <div key={w.day} className="grid gap-2 rounded-xl border bg-white p-4 text-sm leading-relaxed md:grid-cols-[70px_1fr_1.2fr] md:gap-4">
              <Badge className="h-fit w-fit bg-slate-900">{w.day}</Badge>
              <p className="text-slate-600"><b className="text-slate-800">训练：</b>{w.training}</p>
              <p className="text-slate-600"><b className="text-slate-800">食物：</b>{w.food}</p>
            </div>
          ))}
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="flex items-center gap-2 text-base"><Repeat className="h-4 w-4 text-teal-600" /> 每月周期：渐进超负荷 + 恢复</CardTitle>
        </CardHeader>
        <CardContent className="grid gap-3 md:grid-cols-2">
          {MONTHLY_PLAN.map((m) => (
            <div key={m.week} className="rounded-xl border bg-white p-4">
              <p className="font-medium text-slate-900">{m.week} · {m.focus}</p>
              <p className="mt-1 text-sm leading-relaxed text-slate-600">{m.detail}</p>
            </div>
          ))}
        </CardContent>
      </Card>

      <Card className="border-amber-100 bg-amber-50/60">
        <CardContent className="p-4 text-sm leading-relaxed text-amber-800">
          <b>严谨提示：</b>“增肌”不是多吃氨基酸就行，而是训练刺激 + 足量总蛋白 + 每餐分配 + 睡眠恢复共同作用。肾功能异常、痛风、孕期/哺乳期、青少年生长期或有慢性病者，蛋白目标与运动强度请先咨询医生或注册营养师。
        </CardContent>
      </Card>
    </div>
  )
}

export default function AminoAcidsPage() {
  const [params, setParams] = useSearchParams()
  const mode: 'health' | 'muscle' = params.get('mode') === 'muscle' ? 'muscle' : 'health'
  const tab = params.get('tab') || 'principle'

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-6xl px-4 py-8">
        <div className="flex flex-wrap items-end gap-3">
          <div>
            <h1 className="flex items-center gap-2 text-2xl font-bold text-slate-900">
              <Dumbbell className="h-6 w-6 text-indigo-600" /> 氨基酸与健康 / 增肌
            </h1>
            <p className="mt-1 text-sm text-slate-500">
              20 种蛋白质氨基酸：必需/可合成路径、蛋白质合成与利用原理、{PROTEIN_RECIPES.length} 种可筛选蛋白食谱、周/月训练饮食周期
            </p>
          </div>
          <div className="ml-auto flex gap-2">
            {GOAL_MODES.map((g) => {
              const Icon = g.key === 'muscle' ? Dumbbell : HeartPulse
              return (
                <button
                  key={g.key}
                  onClick={() => setParams({ mode: g.key, tab })}
                  className={`flex items-center gap-1.5 rounded-xl border px-3 py-2 text-sm font-medium transition-colors ${mode === g.key ? 'border-slate-900 bg-slate-900 text-white' : 'border-slate-200 bg-white text-slate-600 hover:border-slate-300'}`}
                >
                  <Icon className="h-4 w-4" /> {g.label}
                </button>
              )
            })}
          </div>
        </div>

        <Tabs value={tab} onValueChange={(v) => setParams({ mode, tab: v })} className="mt-6">
          <TabsList>
            <TabsTrigger value="principle">原理与氨基酸</TabsTrigger>
            <TabsTrigger value="recipes">蛋白质食谱库</TabsTrigger>
            <TabsTrigger value="plan">周 / 月周期计划</TabsTrigger>
          </TabsList>
          <TabsContent value="principle" className="mt-4"><PrincipleTab mode={mode} /></TabsContent>
          <TabsContent value="recipes" className="mt-4"><RecipesTab mode={mode} /></TabsContent>
          <TabsContent value="plan" className="mt-4"><PlanTab mode={mode} /></TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
