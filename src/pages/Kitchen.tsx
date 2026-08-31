import { useMemo, useState } from 'react'
import { ChefHat, FlaskConical, BookOpen, Lightbulb } from 'lucide-react'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { KITCHEN_REACTIONS, KITCHEN_TAGS } from '@/data/kitchen'

export default function KitchenPage() {
  const [tag, setTag] = useState('全部')

  const filtered = useMemo(
    () => (tag === '全部' ? KITCHEN_REACTIONS : KITCHEN_REACTIONS.filter((r) => r.tag === tag)),
    [tag]
  )

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-5xl px-4 py-8">
        <h1 className="flex items-center gap-2 text-2xl font-bold text-slate-900">
          <ChefHat className="h-6 w-6 text-indigo-600" /> 厨房里的化学反应
        </h1>
        <p className="mt-1 text-sm text-slate-500">
          每一道菜都是一堂化学课：从厨房现象出发，还原背后的反应原理，并对齐到课本知识点
        </p>

        <div className="mt-5 flex flex-wrap gap-2">
          {KITCHEN_TAGS.map((t) => (
            <Badge
              key={t}
              onClick={() => setTag(t)}
              className={`cursor-pointer ${tag === t ? 'bg-indigo-600' : 'bg-slate-200 text-slate-700 hover:bg-slate-300'}`}
            >
              {t}
            </Badge>
          ))}
          <span className="ml-auto self-center text-sm text-slate-500">
            共 <b className="text-indigo-700">{filtered.length}</b> 个反应
          </span>
        </div>

        <div className="mt-5 grid gap-4">
          {filtered.map((r) => (
            <Card key={r.title} className="transition-shadow hover:shadow-md">
              <CardHeader className="pb-2">
                <CardTitle className="flex flex-wrap items-center gap-2 text-base">
                  {r.title}
                  <Badge variant="secondary" className="font-normal">{r.tag}</Badge>
                </CardTitle>
              </CardHeader>
              <CardContent className="grid gap-3 text-sm leading-relaxed">
                <div className="flex items-start gap-2">
                  <ChefHat className="mt-0.5 h-4 w-4 shrink-0 text-slate-400" />
                  <p><span className="font-medium text-slate-900">厨房现象：</span><span className="text-slate-600">{r.scene}</span></p>
                </div>
                <div className="flex items-start gap-2">
                  <FlaskConical className="mt-0.5 h-4 w-4 shrink-0 text-indigo-500" />
                  <p><span className="font-medium text-slate-900">化学原理：</span><span className="text-slate-600">{r.principle}</span></p>
                </div>
                <div className="rounded-lg bg-slate-100 px-3 py-2 font-mono text-xs text-indigo-800 sm:text-sm">
                  {r.equation}
                </div>
                <div className="flex items-start gap-2">
                  <BookOpen className="mt-0.5 h-4 w-4 shrink-0 text-emerald-600" />
                  <p><span className="font-medium text-slate-900">课本衔接：</span><span className="text-slate-600">{r.knowledge}</span></p>
                </div>
                <div className="flex items-start gap-2">
                  <Lightbulb className="mt-0.5 h-4 w-4 shrink-0 text-amber-500" />
                  <p><span className="font-medium text-slate-900">课堂应用：</span><span className="text-slate-600">{r.tip}</span></p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  )
}
