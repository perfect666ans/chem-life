import { useMemo, useState } from 'react'
import { useSearchParams } from 'react-router'
import { Search, Gem, ShieldAlert, Database, RotateCcw } from 'lucide-react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Switch } from '@/components/ui/switch'
import { Label } from '@/components/ui/label'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { MATERIALS, RARE_METALS, DANGERS, CATEGORIES } from '@/data/materials'

function MaterialsTab() {
  const [q, setQ] = useState('')
  const [cat, setCat] = useState('全部')
  const [onlyRare, setOnlyRare] = useState(false)
  const [onlyDanger, setOnlyDanger] = useState(false)

  const filtered = useMemo(() => {
    const kw = q.trim().toLowerCase()
    return MATERIALS.filter((m) => {
      if (cat !== '全部' && m.category !== cat) return false
      if (onlyRare && !m.rare.startsWith('是')) return false
      if (onlyDanger && !m.safety.startsWith('是')) return false
      if (kw) {
        const hay = `${m.category}${m.item}${m.part}${m.common}${m.chemName}${m.formula}${m.use}`.toLowerCase()
        if (!hay.includes(kw)) return false
      }
      return true
    })
  }, [q, cat, onlyRare, onlyDanger])

  const reset = () => {
    setQ('')
    setCat('全部')
    setOnlyRare(false)
    setOnlyDanger(false)
  }

  return (
    <div>
      {/* 筛选区 */}
      <div className="sticky top-14 z-30 -mx-4 border-b bg-slate-50/95 px-4 py-3 backdrop-blur">
        <div className="mx-auto flex max-w-6xl flex-col gap-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <Input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="搜索物品、俗名、化学名称、化学式或用途，如：芯片 / NaCl / 干燥剂 / 金"
              className="bg-white pl-9"
            />
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <Badge
              onClick={() => setCat('全部')}
              className={`cursor-pointer ${cat === '全部' ? 'bg-indigo-600' : 'bg-slate-200 text-slate-700 hover:bg-slate-300'}`}
            >
              全部
            </Badge>
            {CATEGORIES.map((c) => (
              <Badge
                key={c}
                onClick={() => setCat(c)}
                className={`cursor-pointer ${cat === c ? 'bg-indigo-600' : 'bg-slate-200 text-slate-700 hover:bg-slate-300'}`}
              >
                {c}
              </Badge>
            ))}
          </div>
          <div className="flex flex-wrap items-center gap-x-6 gap-y-2 text-sm text-slate-600">
            <span className="flex items-center gap-2">
              <Switch id="rare" checked={onlyRare} onCheckedChange={setOnlyRare} />
              <Label htmlFor="rare" className="flex cursor-pointer items-center gap-1 text-sm">
                <Gem className="h-3.5 w-3.5 text-indigo-600" /> 仅看含稀有/贵金属
              </Label>
            </span>
            <span className="flex items-center gap-2">
              <Switch id="danger" checked={onlyDanger} onCheckedChange={setOnlyDanger} />
              <Label htmlFor="danger" className="flex cursor-pointer items-center gap-1 text-sm">
                <ShieldAlert className="h-3.5 w-3.5 text-amber-600" /> 仅看有安全风险
              </Label>
            </span>
            <span className="ml-auto flex items-center gap-3">
              <span>
                共 <b className="text-indigo-700">{filtered.length}</b> / {MATERIALS.length} 条
              </span>
              <Button variant="ghost" size="sm" onClick={reset} className="h-7 px-2 text-slate-500">
                <RotateCcw className="mr-1 h-3.5 w-3.5" /> 重置
              </Button>
            </span>
          </div>
        </div>
      </div>

      {/* 桌面端：表格 */}
      <div className="mt-4 hidden md:block">
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-20">分类</TableHead>
                <TableHead className="w-32">物品 / 部件</TableHead>
                <TableHead className="w-36">俗名 / 材料</TableHead>
                <TableHead className="w-40">化学名称</TableHead>
                <TableHead className="w-44">化学式</TableHead>
                <TableHead>用途功能</TableHead>
                <TableHead className="w-36">稀有/贵金属</TableHead>
                <TableHead className="w-44">安全提示</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filtered.map((m, i) => (
                <TableRow key={i}>
                  <TableCell>
                    <Badge variant="secondary" className="font-normal">{m.category}</Badge>
                  </TableCell>
                  <TableCell className="font-medium">
                    {m.item}
                    {m.part !== '整体' && <span className="block text-xs text-slate-400">{m.part}</span>}
                  </TableCell>
                  <TableCell className="text-slate-600">{m.common}</TableCell>
                  <TableCell className="text-slate-600">{m.chemName}</TableCell>
                  <TableCell className="font-mono text-indigo-700">{m.formula}</TableCell>
                  <TableCell className="text-slate-600">{m.use}</TableCell>
                  <TableCell>
                    {m.rare.startsWith('是') ? (
                      <span className="inline-flex items-center gap-1 text-xs font-medium text-indigo-700">
                        <Gem className="h-3.5 w-3.5" /> {m.rare.replace(/^是：?/, '')}
                      </span>
                    ) : (
                      <span className="text-xs text-slate-400">—</span>
                    )}
                  </TableCell>
                  <TableCell>
                    {m.safety.startsWith('是') ? (
                      <span className="inline-flex items-center gap-1 text-xs font-medium text-amber-700">
                        <ShieldAlert className="h-3.5 w-3.5" /> {m.safety.replace(/^是：?/, '')}
                      </span>
                    ) : (
                      <span className="text-xs text-slate-400">{m.safety}</span>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>
      </div>

      {/* 移动端：卡片 */}
      <div className="mt-4 grid gap-3 md:hidden">
        {filtered.map((m, i) => (
          <Card key={i}>
            <CardContent className="p-4">
              <div className="flex items-center justify-between gap-2">
                <div className="font-medium text-slate-900">
                  {m.item}
                  {m.part !== '整体' && <span className="ml-1 text-xs text-slate-400">· {m.part}</span>}
                </div>
                <Badge variant="secondary" className="shrink-0 font-normal">{m.category}</Badge>
              </div>
              <div className="mt-2 flex flex-wrap items-baseline gap-x-2">
                <span className="text-sm text-slate-600">{m.common}（{m.chemName}）</span>
                <span className="font-mono text-sm font-medium text-indigo-700">{m.formula}</span>
              </div>
              <p className="mt-1.5 text-sm leading-relaxed text-slate-600">{m.use}</p>
              <div className="mt-2 flex flex-wrap gap-2">
                {m.rare.startsWith('是') && (
                  <Badge className="bg-indigo-50 font-normal text-indigo-700 hover:bg-indigo-50">
                    <Gem className="mr-1 h-3 w-3" /> {m.rare.replace(/^是：?/, '')}
                  </Badge>
                )}
                {m.safety.startsWith('是') && (
                  <Badge className="bg-amber-50 font-normal text-amber-700 hover:bg-amber-50">
                    <ShieldAlert className="mr-1 h-3 w-3" /> {m.safety.replace(/^是：?/, '')}
                  </Badge>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filtered.length === 0 && (
        <div className="mt-16 text-center text-slate-400">
          <Database className="mx-auto mb-3 h-10 w-10" />
          <p>没有匹配的条目，换个关键词试试</p>
        </div>
      )}
    </div>
  )
}

function RareTab() {
  return (
    <div>
      <Card className="mb-4 border-indigo-100 bg-indigo-50/50">
        <CardContent className="p-4 text-sm leading-relaxed text-slate-700">
          💡 一部手机约含 <b>60 种元素</b>；1 吨废旧手机可提炼约 <b>150–400g 黄金</b>，品位远高于金矿——这就是国家推动电子废弃物回收的原因。
        </CardContent>
      </Card>
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {RARE_METALS.map((r) => (
          <Card key={r.symbol + r.element}>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-baseline gap-2">
                  <span className="text-lg font-bold text-slate-900">{r.element}</span>
                  <span className="font-mono text-sm text-indigo-700">{r.symbol}</span>
                </div>
                <Badge variant="secondary" className="font-normal">{r.kind}</Badge>
              </div>
              <p className="mt-2 text-sm text-slate-600"><span className="text-slate-400">藏身于：</span>{r.foundIn}</p>
              <p className="mt-1 text-sm text-slate-600"><span className="text-slate-400">作用：</span>{r.role}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

function SafetyTab() {
  return (
    <div className="grid gap-3 sm:grid-cols-2">
      {DANGERS.map((d) => (
        <Card key={d.name} className="border-amber-100">
          <CardContent className="p-4">
            <div className="flex items-center justify-between gap-2">
              <div className="flex items-center gap-2 font-medium text-slate-900">
                <ShieldAlert className="h-4 w-4 shrink-0 text-amber-600" />
                {d.name}
              </div>
              <span className="shrink-0 font-mono text-xs text-slate-400">{d.formula}</span>
            </div>
            <p className="mt-2 text-sm text-amber-700">{d.hazard}</p>
            <p className="mt-1 text-sm leading-relaxed text-slate-600">{d.advice}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}

export default function DatabasePage() {
  const [params, setParams] = useSearchParams()
  const tab = params.get('tab') || 'materials'

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-6xl px-4 py-8">
        <h1 className="text-2xl font-bold text-slate-900">日常物品物质成分检索库</h1>
        <p className="mt-1 text-sm text-slate-500">
          俗名 ↔ 化学名称 ↔ 化学式 ↔ 用途，一站式检索；支持按分类、稀有贵金属、安全风险过滤
        </p>
        <Tabs value={tab} onValueChange={(v) => setParams({ tab: v })} className="mt-6">
          <TabsList>
            <TabsTrigger value="materials">成分检索</TabsTrigger>
            <TabsTrigger value="rare">稀有贵金属</TabsTrigger>
            <TabsTrigger value="safety">安全警示</TabsTrigger>
          </TabsList>
          <TabsContent value="materials" className="mt-4"><MaterialsTab /></TabsContent>
          <TabsContent value="rare" className="mt-4"><RareTab /></TabsContent>
          <TabsContent value="safety" className="mt-4"><SafetyTab /></TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
