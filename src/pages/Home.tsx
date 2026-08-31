import { Link } from 'react-router'
import { FlaskConical, Database, Gem, ShieldAlert, ArrowRight, Sparkles, BookOpen, Beaker, Atom, Pill, Dumbbell } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { MATERIALS, RARE_METALS, DANGERS, CATEGORIES } from '@/data/materials'
import { MEAL_PLANS } from '@/data/vitamins'
import { AMINO_ACIDS, PROTEIN_RECIPES } from '@/data/aminoAcids'

const rareCount = MATERIALS.filter((m) => m.rare.startsWith('是')).length
const dangerCount = MATERIALS.filter((m) => m.safety.startsWith('是')).length

const modules = [
  {
    title: '日常物品物质成分检索库',
    desc: `收录 ${MATERIALS.length} 条成分记录，覆盖 ${CATEGORIES.length} 类日常物品：俗名、化学名称、化学式、用途一站式检索`,
    icon: Database,
    to: '/database',
    status: '已上线',
    active: true,
  },
  {
    title: '稀有贵金属地图',
    desc: `${RARE_METALS.length} 种藏在身边的稀有与贵金属：金、银、铂族、稀土……它们各自藏在哪里`,
    icon: Gem,
    to: '/database?tab=rare',
    status: '已上线',
    active: true,
  },
  {
    title: '家庭化学安全警示',
    desc: `${DANGERS.length} 条家庭安全警示：84 消毒液为何不能混洁厕灵？锂电池鼓包怎么办`,
    icon: ShieldAlert,
    to: '/database?tab=safety',
    status: '已上线',
    active: true,
  },
  {
    title: '化合物实时查询（PubChem）',
    desc: '连接全球最大公开化学数据库 PubChem（NIH），输入名称/化学式实时查分子量、结构式、物性',
    icon: Atom,
    to: '/pubchem',
    status: '已上线',
    active: true,
  },
  {
    title: '厨房里的化学反应',
    desc: '12 个厨房现象背后的化学原理：美拉德反应、发酵、胶体聚沉……全部对齐课本知识点',
    icon: Beaker,
    to: '/kitchen',
    status: '已上线',
    active: true,
  },
  {
    title: '维生素与化学',
    desc: `13 种必需 + 6 种类维生素：结构式、溶解性与性质的结构解释、摄入量与忌口可筛选的 ${MEAL_PLANS.length} 种食谱`,
    icon: Pill,
    to: '/vitamins',
    status: '已上线',
    active: true,
  },
  {
    title: '氨基酸与健康 / 增肌',
    desc: `${AMINO_ACIDS.length} 种蛋白质氨基酸：必需/可合成路径、蛋白质合成原理、${PROTEIN_RECIPES.length} 种蛋白食谱与周/月训练饮食周期`,
    icon: Dumbbell,
    to: '/amino-acids',
    status: '已上线',
    active: true,
  },
  {
    title: '元素周期表 · 生活版',
    desc: '每种元素配一个生活实例，从 NaCl 到钕铁硼磁铁',
    icon: Atom,
    to: '',
    status: '规划中',
    active: false,
  },
  {
    title: '课堂实验素材集',
    desc: '可直接搬进课堂的家庭小实验与演示方案',
    icon: BookOpen,
    to: '',
    status: '规划中',
    active: false,
  },
]

const stats = [
  { label: '成分条目', value: MATERIALS.length },
  { label: '物品分类', value: CATEGORIES.length },
  { label: '含稀有/贵金属条目', value: rareCount },
  { label: '安全警示条目', value: dangerCount },
]

export default function Home() {
  return (
    <div className="min-h-screen bg-slate-50">
      {/* Hero */}
      <section className="border-b bg-white">
        <div className="mx-auto max-w-6xl px-4 py-12 sm:py-16">
          <div className="relative overflow-hidden rounded-3xl border border-slate-200 bg-[linear-gradient(135deg,#f8fafc_0%,#eef6f4_48%,#f7f8ff_100%)] p-8 sm:p-12">
            <svg aria-hidden="true" className="pointer-events-none absolute -right-10 -top-12 h-64 w-64 text-slate-200" viewBox="0 0 200 200" fill="none">
              <circle cx="70" cy="70" r="7" stroke="currentColor" strokeWidth="3" />
              <circle cx="132" cy="54" r="10" stroke="currentColor" strokeWidth="3" />
              <circle cx="152" cy="118" r="8" stroke="currentColor" strokeWidth="3" />
              <circle cx="86" cy="142" r="12" stroke="currentColor" strokeWidth="3" />
              <path d="M76 68 122 56M139 62l9 48M143 120l-48 17M78 137 73 78" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
            </svg>
            <Badge className="mb-4 border border-teal-200 bg-teal-50 text-teal-700 hover:bg-teal-50">高中化学 · 生活情境教学</Badge>
            <h1 className="max-w-3xl text-3xl font-bold leading-tight text-slate-950 sm:text-5xl">
              把化学课本，
              <br className="sm:hidden" />
              搬进日常生活
            </h1>
            <p className="mt-4 max-w-2xl text-sm leading-relaxed text-slate-600 sm:text-base">
              从一部手机的 60 种元素，到一杯奶茶杯上的 PET——这里是面向化学教学的
              「生活物质成分百科」。任何设备、任何时间，打开即用。
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Button asChild size="lg" className="bg-slate-900 text-white hover:bg-slate-800">
                <Link to="/database">
                  进入检索库 <ArrowRight className="ml-1 h-4 w-4" />
                </Link>
              </Button>
              <Button asChild size="lg" variant="outline" className="border-slate-300 bg-white/80 text-slate-700 hover:bg-white">
                <Link to="/database?tab=safety">查看安全警示</Link>
              </Button>
            </div>
            <div className="mt-10 grid grid-cols-2 gap-4 sm:grid-cols-4">
              {stats.map((s) => (
                <div key={s.label} className="rounded-2xl border border-white/70 bg-white/75 p-4 shadow-sm backdrop-blur">
                  <div className="text-2xl font-bold text-slate-900 sm:text-3xl">{s.value}</div>
                  <div className="mt-1 text-xs text-slate-500">{s.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* 模块导航 */}
      <section className="mx-auto max-w-6xl px-4 py-12">
        <div className="mb-6 flex items-center gap-2">
          <Sparkles className="h-5 w-5 text-indigo-600" />
          <h2 className="text-xl font-bold text-slate-900">教学模块</h2>
        </div>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {modules.map((m) => {
            const Icon = m.icon
            const inner = (
              <Card className={`h-full transition-shadow ${m.active ? 'hover:shadow-md' : 'opacity-70'}`}>
                <CardHeader className="pb-2">
                  <div className="flex items-center justify-between">
                    <span className={`flex h-10 w-10 items-center justify-center rounded-lg ${m.active ? 'bg-indigo-100 text-indigo-700' : 'bg-slate-100 text-slate-400'}`}>
                      <Icon className="h-5 w-5" />
                    </span>
                    <Badge variant={m.active ? 'default' : 'secondary'} className={m.active ? 'bg-indigo-600' : ''}>
                      {m.status}
                    </Badge>
                  </div>
                  <CardTitle className="mt-3 text-base">{m.title}</CardTitle>
                  <CardDescription className="text-xs leading-relaxed">{m.desc}</CardDescription>
                </CardHeader>
                {m.active && (
                  <CardContent className="pt-0">
                    <span className="inline-flex items-center text-sm font-medium text-indigo-600">
                      进入模块 <ArrowRight className="ml-1 h-3.5 w-3.5" />
                    </span>
                  </CardContent>
                )}
              </Card>
            )
            return m.active ? (
              <Link key={m.title} to={m.to}>{inner}</Link>
            ) : (
              <div key={m.title}>{inner}</div>
            )
          })}
        </div>
      </section>

      {/* 教学提示 */}
      <section className="mx-auto max-w-6xl px-4 pb-16">
        <Card className="border-indigo-100 bg-indigo-50/50">
          <CardContent className="flex flex-col gap-3 p-6 sm:flex-row sm:items-center">
            <FlaskConical className="h-8 w-8 shrink-0 text-indigo-600" />
            <div>
              <p className="font-medium text-slate-900">给老师的使用建议</p>
              <p className="mt-1 text-sm leading-relaxed text-slate-600">
                课堂上讲到某一物质时，直接在检索库中搜索（如讲「硅」时搜"芯片"、讲「原电池」时搜"电池"），
                即可调出学生身边物品的真实成分，把抽象的化学式与具体生活情境一一对应。后续新模块会持续添加到此站点。
              </p>
            </div>
          </CardContent>
        </Card>
      </section>
    </div>
  )
}
