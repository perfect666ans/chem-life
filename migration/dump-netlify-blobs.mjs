import { getStore } from '@netlify/blobs'
import { writeFileSync } from 'node:fs'

async function dump(name, file) {
  const store = getStore({
    name, consistency: 'strong',
    siteID: process.env.SITE_ID, token: process.env.BLOBS_TOKEN,
  })
  const { blobs } = await store.list()
  const out = []
  for (const b of blobs) {
    if (b.key.startsWith('session:')) continue  // 会话不搬，用户重新登录即可
    out.push({ key: b.key, value: await store.get(b.key) })
  }
  writeFileSync(file, JSON.stringify(out))
  console.log(name, '→', file, out.length, '条')
}
await dump('chem-auth', 'migration/kv-auth.json')
await dump('chem-forum', 'migration/kv-forum.json')
