// 论坛 + 排行榜客户端：接口走 /api/forum（Netlify Function + Blobs）
import { getToken } from './auth'

export type PostBrief = {
  id: string
  title: string
  tag: string
  author: { username: string; nickname: string; avatar: string }
  createdAt: number
  content: string
  likes: number
  replies: number
  pinned: boolean
}

export type Reply = {
  id: string
  content: string
  createdAt: number
  author: { username: string; nickname: string; avatar: string }
}

export type PostFull = Omit<PostBrief, 'likes' | 'replies'> & {
  likes: string[]
  replies: Reply[]
}

export type BoardRow = {
  username: string
  nickname: string
  avatar: string
  score: number
  at: number
}

export type BoardMe = { rank: number; score: number; total: number } | null

export const POST_TAGS = ['学习讨论', '题目求助', '页面反馈', '心得分享', '闲聊灌水']

export const GAMES = [
  { id: 'td', name: '元素防线 · 化学塔防', unit: '波' },
  { id: 'rpg', name: '元素纪元 RPG', unit: '波' },
  { id: 'tree', name: '知识挑战树', unit: '节点' },
] as const

async function api<T = Record<string, unknown>>(
  action: string,
  payload: Record<string, unknown> = {},
): Promise<T & { ok: boolean; error?: string }> {
  try {
    const r = await fetch('/api/forum', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action, token: getToken(), ...payload }),
    })
    return await r.json()
  } catch {
    return { ok: false, error: '网络异常，请稍后再试' } as T & { ok: false; error: string }
  }
}

export const listPosts = (q = '', offset = 0) =>
  api<{ posts: PostBrief[]; total: number; hasMore: boolean }>('list', { q, offset })
export const getPost = (postId: string) => api<{ post: PostFull }>('get', { postId })
export const createPost = (title: string, content: string, tag: string) =>
  api<{ post: PostBrief }>('post', { title, content, tag })
export const replyPost = (postId: string, content: string) =>
  api<{ post: PostFull }>('reply', { postId, content })
export const likePost = (postId: string) =>
  api<{ likes: number; liked: boolean }>('like', { postId })
export const delPost = (postId: string) => api('del', { postId })
export const pinPost = (postId: string) => api<{ pinned: boolean }>('pin', { postId })
export const getBoard = (game: string) =>
  api<{ rows: BoardRow[]; total: number; me: BoardMe }>('board', { game })

export const fmtTime = (t: number) => {
  const d = new Date(t)
  const p = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}`
}
