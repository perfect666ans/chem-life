// Cloudflare Pages Function：交流论坛 + 游戏排行榜（KV 持久化）
// 路由：POST /api/forum  {action: ...}
// 由 netlify/functions/forum.js 移植，接口契约完全一致，前端无需改动
// 环境变量/绑定：KV namespace 绑定为 CHEM_AUTH（读用户）与 CHEM_FORUM（帖子/榜单）
//
// - list      {q?, offset?}                    公开：帖子列表（置顶优先，新→旧，每页 20）
// - get       {postId}                        公开：帖子详情+回复
// - post      {token, title, content, tag}    登录：发帖
// - reply     {token, postId, content}        登录：回复
// - like      {token, postId}                 登录：点赞/取消
// - del       {token, postId}                 登录：删帖（本人或管理员）
// - pin       {token, postId}                 登录：置顶/取消（仅管理员）
// - report    {token, game, score}            登录：上报成绩（只保留每人每游戏最高，带服务端上限+限频）
// - board     {game, token?}                  公开：排行榜 Top 20（可选附带我的排名）
// - userCard  {username}                      公开：个人名片（昵称/头像/备注/标签 + 按本人开关公开时长与战绩）
// - ban       {token, username, banned}       管理员：一键禁言/解禁（禁言后无法发帖/回复/点赞/上报成绩）
// 游戏标识：td=化学塔防(波) rpg=元素纪元(波) tree=知识挑战树(点亮节点数)

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
const GAMES = ['td', 'rpg', 'tree', 'snake', 'merge', 'aufbau']
// 【W-12 防刷榜】每游戏成绩合理上限（td 目前 15 波可通关，留余量；tree 满节点 30）
const SCORE_CAP = { td: 20, rpg: 100, tree: 30, snake: 999999, merge: 9999999, aufbau: 59 }
// 【W-12 防刷榜】每用户每分钟最多上报次数
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

/* 读取时同步作者信息：帖子/榜单里存的是发帖当时的昵称头像，
   用户改资料后这里实时用 CHEM_AUTH 里的最新值覆盖展示（修「古早名字」） */
async function resolveAuthors(env, authors) {
  const names = [...new Set(authors.map((a) => a && a.username).filter(Boolean))]
  const cache = {}
  for (const n of names) {
    const u = await getJSON(env.CHEM_AUTH, 'user:' + n)
    if (u) cache[n] = { nickname: u.nickname || n, avatar: u.avatar || '🧪' }
  }
  for (const a of authors) {
    if (a && cache[a.username]) Object.assign(a, cache[a.username])
  }
}

/* 个人名片数据：基础信息 + 按本人公开开关附带时长/战绩（W-系「个人名片」钩子） */
async function buildUserCard(env, username) {
  const u = await getJSON(env.CHEM_AUTH, 'user:' + username)
  if (!u) return null
  const card = {
    username: u.username,
    nickname: u.nickname || u.username,
    avatar: u.avatar || '🧪',
    bio: u.bio || '',
    tags: u.tags || [],
    banned: !!u.banned,
    showUsage: !!u.showUsage,
    showGameTime: !!u.showGameTime,
    usage: null,
    games: null,
  }
  if (card.showUsage) {
    const usage = (await getJSON(env.CHEM_AUTH, 'usage:' + u.username)) || {}
    card.usage = { byModule: usage, total: Object.values(usage).reduce((a, b) => a + b, 0) }
  }
  if (card.showGameTime) {
    const games = []
    for (const g of GAMES) {
      const board = (await getJSON(env.CHEM_FORUM, 'score:' + g)) || {}
      const all = Object.values(board).sort((a, b) => b.score - a.score)
      const mine = board[u.username]
      if (mine) games.push({ game: g, score: mine.score, rank: all.findIndex((r) => r.username === u.username) + 1, players: all.length })
    }
    card.games = games
  }
  return card
}

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
    /* ---------- 公开读取 ---------- */
    if (action === 'list') {
      let posts = await listPosts(env)
      const q = clip(body.q, 40).toLowerCase()
      if (q) posts = posts.filter((p) =>
        p.title.toLowerCase().includes(q) || p.content.toLowerCase().includes(q))
      posts.sort((a, b) => Number(!!b.pinned) - Number(!!a.pinned) || b.createdAt - a.createdAt)
      const offset = Math.max(0, Number(body.offset) || 0)
      const page = posts.slice(offset, offset + PAGE)
      await resolveAuthors(env, page.map((p) => p.author))
      return ok({
        posts: page.map(brief),
        total: posts.length,
        hasMore: offset + PAGE < posts.length,
      })
    }
    if (action === 'get') {
      const p = await getJSON(env.CHEM_FORUM, 'post:' + clip(body.postId, 40))
      if (!p) return fail('帖子不存在', 404)
      await resolveAuthors(env, [p.author, ...(p.replies || []).map((r) => r.author)])
      return ok({ post: p })
    }
    if (action === 'board') {
      const game = clip(body.game, 10)
      if (!GAMES.includes(game)) return fail('未知游戏', 404)
      const board = (await getJSON(env.CHEM_FORUM, 'score:' + game)) || {}
      const rows = Object.values(board).sort((a, b) => b.score - a.score).slice(0, 20)
      await resolveAuthors(env, rows)
      // 可选登录：附带「我的排名」
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

    /* 公开个人名片：论坛/排行榜点击昵称弹出 */
    if (action === 'userCard') {
      const username = clip(body.username, 40)
      if (!username) return fail('缺少用户名')
      const card = await buildUserCard(env, username)
      if (!card) return fail('用户不存在', 404)
      return ok({ card })
    }

    /* 使用时长榜：仅统计选择公开的用户（W-06 后半句） */
    if (action === 'usageBoard') {
      // 注意：心跳数据存在 CHEM_AUTH（usage: 前缀），此前误读 CHEM_FORUM 导致榜单恒空
      const users = await env.CHEM_AUTH.list({ prefix: 'user:' })
      const rows = []
      for (const k of users.keys) {
        const uname = k.name.slice(5)
        const u = await getJSON(env.CHEM_AUTH, k.name)
        if (!u || !u.showUsage) continue
        const uu = (await getJSON(env.CHEM_AUTH, 'usage:' + uname)) || {}
        const total = Object.values(uu).reduce((a, b) => a + b, 0)
        if (total > 0) rows.push({ username: uname, nickname: u.nickname || uname, avatar: u.avatar || '🧪', total })
      }
      rows.sort((a, b) => b.total - a.total)
      return ok({ rows: rows.slice(0, 20) })
    }

    /* ---------- 以下需登录 ---------- */
    const u = await userByToken(env, body.token)
    if (!u) return fail('请先登录', 401)

    /* 管理员：一键禁言/解禁（被禁言者无法发帖/回复/点赞/上报成绩，历史内容保留） */
    if (action === 'ban') {
      if (!u.isAdmin) return fail('仅管理员可禁言', 403)
      const target = await getJSON(env.CHEM_AUTH, 'user:' + clip(body.username, 40))
      if (!target) return fail('用户不存在', 404)
      if (target.isAdmin) return fail('不能禁言管理员', 403)
      target.banned = !!body.banned
      await setJSON(env.CHEM_AUTH, 'user:' + target.username, target)
      return ok({ username: target.username, banned: target.banned })
    }

    /* 管理员：禁言名单（个人中心集中管理） */
    if (action === 'banList') {
      if (!u.isAdmin) return fail('仅管理员可查看', 403)
      const all = await env.CHEM_AUTH.list({ prefix: 'user:' })
      const banned = []
      for (const k of all.keys) {
        const t = await getJSON(env.CHEM_AUTH, k.name)
        if (t && t.banned) banned.push({ username: t.username, nickname: t.nickname || t.username, avatar: t.avatar || '🧪' })
      }
      return ok({ banned })
    }

    // 禁言检查：ban 动作本身在上面已处理，其余写操作一律拦截
    if (u.banned) return fail('你已被禁言，暂时无法发言或上榜，如有疑问请联系站长', 403)

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
      // 【W-12】超过游戏理论上限直接拒绝
      if (score > SCORE_CAP[game]) return fail(`成绩超出上限（${game} 最高 ${SCORE_CAP[game]}）`, 422)
      // 【W-12】限频：每分钟最多 REPORT_RATE.max 次
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
