// Cloudflare Pages Function：PubChem 中转代理
const BASE = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug'

export async function onRequest(context) {
  const { params } = context
  const path = String(params.path || '').replace(/^\/+/, '')
  const allowed = /^compound\/(name|cid|formula)\/[\w\-+[\](),.%/]+\/(cids|property\/[\w,]+|synonyms|PNG)(\/JSON)?$/i.test(path)
  if (!allowed) {
    return Response.json({ error: '不允许的查询路径', got: path }, { status: 400 })
  }
  try {
    const resp = await fetch(`${BASE}/${path}`, { headers: { 'User-Agent': 'chem-life-teaching-site' } })
    const isPng = path.endsWith('/PNG')
    if (isPng) {
      return new Response(await resp.arrayBuffer(), {
        status: resp.status,
        headers: { 'Content-Type': 'image/png', 'Cache-Control': 'public, max-age=86400' },
      })
    }
    return new Response(await resp.text(), {
      status: resp.status,
      headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'public, max-age=86400' },
    })
  } catch (e) {
    return Response.json({ error: 'PubChem 连接失败：' + String(e) }, { status: 502 })
  }
}
