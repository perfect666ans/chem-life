// Netlify Function（ESM）：PubChem 中转代理
// 浏览器只访问本站 /api/pubchem/*，由此函数在 Netlify 服务器端转发到 PubChem，绕开网络限制

const BASE = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug'
const PREFIX = '/.netlify/functions/pubchem'

export const handler = async (event) => {
  // 从重写后的路径中取出 PubChem 查询路径
  let path = ''
  if (event.path && event.path.startsWith(PREFIX)) {
    path = event.path.slice(PREFIX.length).replace(/^\//, '')
  } else if (event.rawUrl) {
    path = new URL(event.rawUrl).pathname.replace(/^\/api\/pubchem\/?/, '')
  }
  // 白名单校验，防止被当作通用代理滥用
  const ok = /^compound\/(name|cid|formula)\/[\w\-+[\](),.%/]+\/(cids|property\/[\w,]+|synonyms|PNG)(\/JSON)?$/i.test(path)
  if (!ok) {
    return { statusCode: 400, body: JSON.stringify({ error: '不允许的查询路径', got: path }) }
  }
  try {
    const url = `${BASE}/${path}`
    const resp = await fetch(url, { headers: { 'User-Agent': 'chem-life-teaching-site' } })
    const isPng = path.endsWith('/PNG')
    const body = isPng
      ? Buffer.from(await resp.arrayBuffer()).toString('base64')
      : await resp.text()
    return {
      statusCode: resp.status,
      headers: {
        'Content-Type': isPng ? 'image/png' : 'application/json; charset=utf-8',
        'Cache-Control': 'public, max-age=86400',
      },
      body,
      isBase64Encoded: isPng,
    }
  } catch (e) {
    return { statusCode: 502, body: JSON.stringify({ error: 'PubChem 连接失败：' + String(e) }) }
  }
}
