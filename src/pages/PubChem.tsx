import { useState } from 'react'
import { Search, Loader2, ExternalLink, Atom, AlertCircle, Info } from 'lucide-react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

interface CompoundInfo {
  cid: number
  formula: string
  weight: string
  iupac: string
  xlogp?: string
  tpsa?: string
  hbd?: string
  hba?: string
  synonyms: string[]
}

const EXAMPLES = [
  { label: '水', q: 'water' },
  { label: '乙醇', q: 'ethanol' },
  { label: '葡萄糖', q: 'glucose' },
  { label: '氯化钠', q: 'sodium chloride' },
  { label: '咖啡因', q: 'caffeine' },
  { label: '醋酸', q: 'acetic acid' },
  { label: '碳酸钙', q: 'calcium carbonate' },
  { label: '维生素C', q: 'ascorbic acid' },
]

async function fetchCompound(query: string): Promise<CompoundInfo> {
  const q = encodeURIComponent(query.trim())
  // 第一步：名称 → CID
  const cidResp = await fetch(`/api/pubchem/compound/name/${q}/cids/JSON`)
  if (cidResp.status === 404) throw new Error('NOT_FOUND')
  if (!cidResp.ok) throw new Error('NETWORK')
  const cidData = await cidResp.json()
  const cid: number = cidData?.IdentifierList?.CID?.[0]
  if (!cid) throw new Error('NOT_FOUND')

  // 第二步：CID → 性质 + 同义词
  const props =
    'MolecularFormula,MolecularWeight,IUPACName,XLogP,TPSA,HBondDonorCount,HBondAcceptorCount'
  const [propResp, synResp] = await Promise.all([
    fetch(`/api/pubchem/compound/cid/${cid}/property/${props}/JSON`),
    fetch(`/api/pubchem/compound/cid/${cid}/synonyms/JSON`),
  ])
  if (!propResp.ok) throw new Error('NETWORK')
  const propData = await propResp.json()
  const p = propData?.PropertyTable?.Properties?.[0] || {}
  let synonyms: string[] = []
  if (synResp.ok) {
    const synData = await synResp.json()
    synonyms = (synData?.InformationList?.Information?.[0]?.Synonym || []).slice(0, 8)
  }
  return {
    cid,
    formula: p.MolecularFormula || '—',
    weight: p.MolecularWeight || '—',
    iupac: p.IUPACName || '—',
    xlogp: p.XLogP != null ? String(p.XLogP) : undefined,
    tpsa: p.TPSA != null ? String(p.TPSA) : undefined,
    hbd: p.HBondDonorCount != null ? String(p.HBondDonorCount) : undefined,
    hba: p.HBondAcceptorCount != null ? String(p.HBondAcceptorCount) : undefined,
    synonyms,
  }
}

export default function PubChemPage() {
  const [q, setQ] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<CompoundInfo | null>(null)

  const search = async (query: string) => {
    if (!query.trim() || loading) return
    setQ(query)
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      setResult(await fetchCompound(query))
    } catch (e) {
      if (e instanceof Error && e.message === 'NOT_FOUND') {
        setError(`未找到"${query}"，请换用英文名称或标准化学式（如 glucose / NaCl / C₆H₁₂O₆ 写作 C6H12O6）`)
      } else {
        setError('无法连接 PubChem 数据库。本地预览暂无网络中转，部署到 Netlify 后此功能自动启用。')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-4xl px-4 py-8">
        <h1 className="flex items-center gap-2 text-2xl font-bold text-slate-900">
          <Atom className="h-6 w-6 text-indigo-600" /> 化合物实时查询
        </h1>
        <p className="mt-1 text-sm text-slate-500">
          数据实时来自全球最大的公开化学数据库 <b>PubChem</b>（美国国立卫生研究院 NIH），收录超过 1 亿种化合物
        </p>

        <Card className="mt-6 border-indigo-100 bg-indigo-50/50">
          <CardContent className="flex items-start gap-2 p-4 text-sm leading-relaxed text-slate-700">
            <Info className="mt-0.5 h-4 w-4 shrink-0 text-indigo-600" />
            <span>
              课堂用法：检索请输入<b>英文名称或化学式</b>（PubChem 为英文数据库），
              如 water、NaCl、C6H12O6。可查分子式、分子量、IUPAC 命名、结构式——讲到什么查什么。
            </span>
          </CardContent>
        </Card>

        <div className="mt-4 flex gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <Input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && search(q)}
              placeholder="输入英文名称或化学式，如 glucose / NaCl / caffeine"
              className="bg-white pl-9"
            />
          </div>
          <Button onClick={() => search(q)} disabled={loading} className="bg-indigo-600 hover:bg-indigo-700">
            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : '查询'}
          </Button>
        </div>

        <div className="mt-3 flex flex-wrap gap-2">
          {EXAMPLES.map((e) => (
            <Badge
              key={e.q}
              onClick={() => search(e.q)}
              className="cursor-pointer bg-slate-200 font-normal text-slate-700 hover:bg-indigo-100 hover:text-indigo-700"
            >
              {e.label} {e.q}
            </Badge>
          ))}
        </div>

        {error && (
          <Card className="mt-6 border-amber-200 bg-amber-50">
            <CardContent className="flex items-start gap-2 p-4 text-sm text-amber-800">
              <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
              {error}
            </CardContent>
          </Card>
        )}

        {result && (
          <Card className="mt-6">
            <CardHeader>
              <CardTitle className="flex flex-wrap items-center gap-3">
                <span className="font-mono text-xl text-indigo-700">{result.formula}</span>
                <span className="text-sm font-normal text-slate-500">CID: {result.cid}</span>
                <a
                  href={`https://pubchem.ncbi.nlm.nih.gov/compound/${result.cid}`}
                  target="_blank"
                  rel="noreferrer"
                  className="ml-auto inline-flex items-center gap-1 text-xs font-normal text-indigo-600 hover:underline"
                >
                  PubChem 原文 <ExternalLink className="h-3 w-3" />
                </a>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col gap-6 sm:flex-row">
                <img
                  src={`/api/pubchem/compound/cid/${result.cid}/PNG`}
                  alt={result.formula}
                  className="h-48 w-48 shrink-0 rounded-lg border bg-white object-contain"
                />
                <dl className="grid flex-1 grid-cols-1 gap-x-8 gap-y-2 text-sm sm:grid-cols-2">
                  <div><dt className="text-slate-400">分子量</dt><dd className="font-medium">{result.weight} g/mol</dd></div>
                  {result.xlogp && <div><dt className="text-slate-400">脂溶性 XLogP</dt><dd className="font-medium">{result.xlogp}</dd></div>}
                  {result.tpsa && <div><dt className="text-slate-400">极性表面积 TPSA</dt><dd className="font-medium">{result.tpsa} Å²</dd></div>}
                  {result.hbd && <div><dt className="text-slate-400">氢键供体数</dt><dd className="font-medium">{result.hbd}</dd></div>}
                  {result.hba && <div><dt className="text-slate-400">氢键受体数</dt><dd className="font-medium">{result.hba}</dd></div>}
                  <div className="sm:col-span-2"><dt className="text-slate-400">IUPAC 命名</dt><dd className="break-all font-mono text-xs">{result.iupac}</dd></div>
                </dl>
              </div>
              {result.synonyms.length > 0 && (
                <div className="mt-4 border-t pt-3">
                  <p className="text-xs text-slate-400">常见别名</p>
                  <div className="mt-1 flex flex-wrap gap-1.5">
                    {result.synonyms.map((s) => (
                      <Badge key={s} variant="secondary" className="font-normal">{s}</Badge>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        )}

        <p className="mt-8 text-center text-xs text-slate-400">
          数据来源：PubChem（NIH）· 通过本站服务器中转，国内课堂网络可稳定访问
        </p>
      </div>
    </div>
  )
}
