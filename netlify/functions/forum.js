// Netlify Function：交流论坛 + 游戏排行榜（Netlify Blobs 持久化）
// 路由：POST /api/forum  {action: ...}
// - list      {}                                  公开：帖子列表（新→旧）
// - get       {postId}                            公开：帖子详情+回复
// - post      {token, title, content, tag}        登录：发帖
// - reply     {token, postId, content}            登录：回复
// - like      {token, postId}                     登录：点赞/取消
// - del       {token, postId}                     登录：删帖（本人或管理员）
// - report    {token, game, score}                登录：上报成绩（只保留每人每游戏最高）
// - board     {game}                              公开：排行榜 Top 20
// 游戏标识：td=化学塔防(波) rpg=元素纪元(波) tree=知识挑战树(点亮节点数)

import { getStore } from '@netlify/blobs'
import crypto from 'node:crypto'

const mkStore = (name) => {
  const opts = { name, consistency: 'strong' }
  const token = process.env.BLOBS_TOKEN
  const siteID = process.env.SITE_ID || process.env.NETLIFY_SITE_ID
  if (!process.env.NETLIFY_BLOBS_CONTEXT && token && siteID) {
    opts.siteID = siteID
    opts.token = token
  }
  return getStore(opts)
}
const authStore = () => mkStore('chem-auth')
const forumStore = () => mkStore('chem-forum')

const now = () => Date.now()
const rand = (n = 8) => crypto.randomBytes(n).toString('hex')

async function getJSON(store, key) {
  return (await store.get(key, { type: 'json' })) ?? null
}

async function userByToken(token) {
  if (!token || typeof token !== 'string') return null
  const s = await getJSON(authStore(), 'session:' + token)
  if (!s || s.expiresAt < now()) return null
  const u = await getJSON(authStore(), 'user:' + s.username)
  return u || null
}

const ok = (data) => resp(200, { ok: true, ...data })
const fail = (message, code = 400) => resp(code, { ok: false, error: message })
const resp = (statusCode, obj) => ({
  statusCode,
  headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' },
  body: JSON.stringify(obj),
})

const TAGS = ['学习讨论', '题目求助', '页面反馈', '心得分享', '闲聊灌水']
const GAMES = ['td', 'rpg', 'tree']
const clip = (v, max) => String(v ?? '').slice(0, max).trim()

async function listPosts() {
  const { blobs } = await forumStore().list({ prefix: 'post:' })
  const posts = []
  for (const b of blobs) {
    const p = await getJSON(forumStore(), b.key)
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

export const handler = async (event) => {
  if (event.httpMethod !== 'POST') return fail('仅支持 POST', 405)
  let body
  try { body = JSON.parse(event.body || '{}') } catch { return fail('请求格式错误') }
  const { action } = body

  try {
    /* ---------- 公开读取 ---------- */
    if (action === 'list') {
      let posts = await listPosts()
      const q = clip(body.q, 40).toLowerCase()
      if (q) posts = posts.filter((p) =>
        p.title.toLowerCase().includes(q) || p.content.toLowerCase().includes(q))
      posts.sort((a, b) => ((!!b.pinned) - (!!a.pinned)) || (b.createdAt - a.createdAt))
      const offset = Math.max(0, Number(body.offset) || 0)
      return ok({
        posts: posts.slice(offset, offset + PAGE).map(brief),
        total: posts.length,
        hasMore: offset + PAGE < posts.length,
      })
    }
    if (action === 'get') {
      const p = await getJSON(forumStore(), 'post:' + clip(body.postId, 40))
      if (!p) return fail('帖子不存在', 404)
      return ok({ post: p })
    }
    if (action === 'board') {
      const game = clip(body.game, 10)
      if (!GAMES.includes(game)) return fail('未知游戏', 404)
      const board = (await getJSON(forumStore(), 'score:' + game)) || {}
      const rows = Object.values(board).sort((a, b) => b.score - a.score).slice(0, 20)
      // 可选登录：附带「我的排名」
      let me = null
      const u = await userByToken(body.token)
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

    /* ---------- 以下需登录 ---------- */
    const u = await userByToken(body.token)
    if (!u) return fail('请先登录', 401)

    if (action === 'post') {
      const title = clip(body.title, 60)
      const content = clip(body.content, 2000)
      const tag = TAGS.includes(body.tag) ? body.tag : TAGS[0]
      if (title.length < 2) return fail('标题至少 2 个字')
      if (content.length < 2) return fail('内容至少 2 个字')
      const posts = await listPosts()
      const mine = posts.find((p) => p.author.username === u.username)
      if (mine && now() - mine.createdAt < 30e3) return fail('发帖太频繁，请 30 秒后再试', 429)
      const p = {
        id: now().toString(36) + rand(4),
        title, content, tag,
        author: { username: u.username, nickname: u.nickname, avatar: u.avatar },
        createdAt: now(), likes: [], replies: [],
      }
      await forumStore().setJSON('post:' + p.id, p)
      return ok({ post: brief(p) })
    }

    if (action === 'reply') {
      const p = await getJSON(forumStore(), 'post:' + clip(body.postId, 40))
      if (!p) return fail('帖子不存在', 404)
      const content = clip(body.content, 1000)
      if (content.length < 1) return fail('回复不能为空')
      p.replies = [...(p.replies || []), {
        id: rand(6), content, createdAt: now(),
        author: { username: u.username, nickname: u.nickname, avatar: u.avatar },
      }].slice(-200)
      await forumStore().setJSON('post:' + p.id, p)
      return ok({ post: p })
    }

    if (action === 'like') {
      const p = await getJSON(forumStore(), 'post:' + clip(body.postId, 40))
      if (!p) return fail('帖子不存在', 404)
      p.likes = p.likes || []
      const i = p.likes.indexOf(u.username)
      if (i >= 0) p.likes.splice(i, 1); else p.likes.push(u.username)
      await forumStore().setJSON('post:' + p.id, p)
      return ok({ likes: p.likes.length, liked: i < 0 })
    }

    if (action === 'del') {
      const p = await getJSON(forumStore(), 'post:' + clip(body.postId, 40))
      if (!p) return fail('帖子不存在', 404)
      if (p.author.username !== u.username && !u.isAdmin) return fail('只能删除自己的帖子', 403)
      await forumStore().delete('post:' + p.id)
      return ok({})
    }

    if (action === 'pin') {
      if (!u.isAdmin) return fail('仅管理员可置顶', 403)
      const p = await getJSON(forumStore(), 'post:' + clip(body.postId, 40))
      if (!p) return fail('帖子不存在', 404)
      p.pinned = !p.pinned
      await forumStore().setJSON('post:' + p.id, p)
      return ok({ pinned: p.pinned })
    }

    if (action === 'report') {
      const game = clip(body.game, 10)
      const score = Math.floor(Number(body.score))
      if (!GAMES.includes(game)) return fail('未知游戏', 404)
      if (!Number.isFinite(score) || score < 0 || score > 100000) return fail('成绩不合法')
      const key = 'score:' + game
      const board = (await getJSON(forumStore(), key)) || {}
      const cur = board[u.username]
      if (!cur || score > cur.score) {
        board[u.username] = { username: u.username, nickname: u.nickname, avatar: u.avatar, score, at: now() }
        await forumStore().setJSON(key, board)
      }
      return ok({ best: board[u.username].score })
    }

    return fail('未知操作', 404)
  } catch (e) {
    return fail('服务器错误：' + String(e && e.message || e), 500)
  }
}
