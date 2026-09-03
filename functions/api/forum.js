// Cloudflare Pages Function：论坛 + 排行榜（KV）——由 Netlify 移植 + W-12 防刷榜
const now = () => Date.now()
const rand = (n = 8) =>
  [...crypto.getRandomValues(new Uint8Array(n))].map((b) => b.toString(16).padStart(2, '0')).join('')

async function getJSON(kv, key) {
  return (await kv.get(key, 'json')) ?? null
}
async function setJSON(kv, key, val) {
  await kv.put(key, JSON.stringify(val))
}

async function userByToken(env, token) {
  if (!token || typeof token !== 'string') return null
  const s = await getJSON(env.CHEM_AUTH, 'session:' + token)
  if (!s || s.expiresAt < now()) return null
  return (await getJSON(env.CHEM_AUTH, 'user:' + s.username)) || null
}

const json = (obj, status = 200) =>
  new Response(JSON.stringify(obj), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' },
  })
const ok = (data) => json({ ok: true, ...data })
const fail = (message, code = 400) => json({ ok: false, error: message }, code)

const TAGS = ['学习讨论', '题目求助', '页面反馈', '心得分享', '闲聊灌水']
const GAMES = ['td', 'rpg', 'tree']
const SCORE_CAP = { td: 20, rpg: 100, tree: 30 }
const REPORT_RATE = { windowMs: 60e3, max: 10 }
const clip = (v, max) => String(v ?? '').slice(0, max).trim()

async function listPosts(env) {
  const { keys } = await env.CHEM_FORUM.list({ prefix: 'post:' })
  const posts = []
  for (const k of keys) {
    const p = await getJSON(env.CHEM_FORUM, k.name)
    if (p) posts.push(p)
  }
  posts.sort((a, b) => b.createdAt - a.createdAt)
  return posts
}

const brief = (p) => ({
  id: p.id, title: p.title, tag: p.tag,
  author: p.author, createdAt: p.createdAt,
  content: p.content,
  likes: (p.likes || []).length,
  replies: (p.replies || []).length,
  pinned: !!p.pinned,
})

const PAGE = 20

export async function onRequestPost(context) {
  const { request, env } = context
  let body
  try {
    body = await request.json()
  } catch {
    return fail('请求格式错误')
  }
  const { action } = body

  try {
    if (action === 'list') {
      let posts = await listPosts(env)
      const q = clip(body.q, 40).toLowerCase()
      if (q) posts = posts.filter((p) =>
        p.title.toLowerCase().includes(q) || p.content.toLowerCase().includes(q))
      posts.sort((a, b) => Number(!!b.pinned) - Number(!!a.pinned) || b.createdAt - a.createdAt)
      const offset = Math.max(0, Number(body.offset) || 0)
      return ok({
        posts: posts.slice(offset, offset + PAGE).map(brief),
        total: posts.length,
        hasMore: offset + PAGE < posts.length,
      })
    }
    if (action === 'get') {
      const p = await getJSON(env.CHEM_FORUM, 'post:' + clip(body.postId, 40))
      if (!p) return fail('帖子不存在', 404)
      return ok({ post: p })
    }
    if (action === 'board') {
      const game = clip(body.game, 10)
      if (!GAMES.includes(game)) return fail('未知游戏', 404)
      const board = (await getJSON(env.CHEM_FORUM, 'score:' + game)) || {}
      const rows = Object.values(board).sort((a, b) => b.score - a.score).slice(0, 20)
      let me = null
      const u = await userByToken(env, body.token)
      if (u && board[u.username]) {
        const all = Object.values(board).sort((a, b) => b.score - a.score)
        me = {
          rank: all.findIndex((r) => r.username === u.username) + 1,
          score: board[u.username].score,
          total: all.length,
        }
      }
      return ok({ rows, total: Object.keys(board).length, me })
    }

    const u = await userByToken(env, body.token)
    if (!u) return fail('请先登录', 401)

    if (action === 'post') {
      const title = clip(body.title, 60)
      const content = clip(body.content, 2000)
      const tag = TAGS.includes(body.tag) ? body.tag : TAGS[0]
      if (title.length < 2) return fail('标题至少 2 个字')
      if (content.length < 2) return fail('内容至少 2 个字')
      const posts = await listPosts(env)
      const mine = posts.find((p) => p.author.username === u.username)
      if (mine && now() - mine.createdAt < 30e3) return fail('发帖太频繁，请 30 秒后再试', 429)
      const p = {
        id: now().toString(36) + rand(4),
        title, content, tag,
        author: { username: u.username, nickname: u.nickname, avatar: u.avatar },
        createdAt: now(), likes: [], replies: [],
      }
      await setJSON(env.CHEM_FORUM, 'post:' + p.id, p)
      return ok({ post: brief(p) })
    }

    if (action === 'reply') {
      const p = await getJSON(env.CHEM_FORUM, 'post:' + clip(body.postId, 40))
      if (!p) return fail('帖子不存在', 404)
      const content = clip(body.content, 1000)
      if (content.length < 1) return fail('回复不能为空')
      p.replies = [...(p.replies || []), {
        id: rand(6), content, createdAt: now(),
        author: { username: u.username, nickname: u.nickname, avatar: u.avatar },
      }].slice(-200)
      await setJSON(env.CHEM_FORUM, 'post:' + p.id, p)
      return ok({ post: p })
    }

    if (action === 'like') {
      const p = await getJSON(env.CHEM_FORUM, 'post:' + clip(body.postId, 40))
      if (!p) return fail('帖子不存在', 404)
      p.likes = p.likes || []
      const i = p.likes.indexOf(u.username)
      if (i >= 0) p.likes.splice(i, 1); else p.likes.push(u.username)
      await setJSON(env.CHEM_FORUM, 'post:' + p.id, p)
      return ok({ likes: p.likes.length, liked: i < 0 })
    }

    if (action === 'del') {
      const p = await getJSON(env.CHEM_FORUM, 'post:' + clip(body.postId, 40))
      if (!p) return fail('帖子不存在', 404)
      if (p.author.username !== u.username && !u.isAdmin) return fail('只能删除自己的帖子', 403)
      await env.CHEM_FORUM.delete('post:' + p.id)
      return ok({})
    }

    if (action === 'pin') {
      if (!u.isAdmin) return fail('仅管理员可置顶', 403)
      const p = await getJSON(env.CHEM_FORUM, 'post:' + clip(body.postId, 40))
      if (!p) return fail('帖子不存在', 404)
      p.pinned = !p.pinned
      await setJSON(env.CHEM_FORUM, 'post:' + p.id, p)
      return ok({ pinned: p.pinned })
    }

    if (action === 'report') {
      const game = clip(body.game, 10)
      const score = Math.floor(Number(body.score))
      if (!GAMES.includes(game)) return fail('未知游戏', 404)
      if (!Number.isFinite(score) || score < 0 || score > 100000) return fail('成绩不合法')
      if (score > SCORE_CAP[game]) return fail('成绩超出上限（' + game + ' 最高 ' + SCORE_CAP[game] + '）', 422)
      const rlKey = 'rl:report:' + u.username
      const rl = (await getJSON(env.CHEM_FORUM, rlKey)) || { count: 0, resetAt: now() + REPORT_RATE.windowMs }
      if (now() > rl.resetAt) { rl.count = 0; rl.resetAt = now() + REPORT_RATE.windowMs }
      rl.count += 1
      await setJSON(env.CHEM_FORUM, rlKey, rl)
      if (rl.count > REPORT_RATE.max) return fail('上报太频繁，请稍后再试', 429)

      const key = 'score:' + game
      const board = (await getJSON(env.CHEM_FORUM, key)) || {}
      const cur = board[u.username]
      if (!cur || score > cur.score) {
        board[u.username] = { username: u.username, nickname: u.nickname, avatar: u.avatar, score, at: now() }
        await setJSON(env.CHEM_FORUM, key, board)
      }
      return ok({ best: board[u.username].score })
    }

    return fail('未知操作', 404)
  } catch (e) {
    return fail('服务器错误：' + String((e && e.message) || e), 500)
  }
}
