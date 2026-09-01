// 账号系统客户端：会话存 localStorage，接口走 /api/auth（Netlify Function + Blobs）
import { useEffect, useState } from 'react'

export type UserProfile = {
  username: string
  isAdmin: boolean
  nickname: string
  avatar: string
  bio: string
  tags: string[]
  showUsage: boolean
  showGameTime: boolean
  createdAt: number
  mustChangePw?: boolean
}

export type InviteState = {
  code: string
  openPassword: string
  active: boolean
  expiresAt: number
  maxUsers: number
  used: string[]
} | null

const KEY = 'chem-token'
let cache: UserProfile | null | undefined // undefined = 未初始化
const listeners = new Set<() => void>()
const emit = () => listeners.forEach((f) => f())

export function getToken() {
  return localStorage.getItem(KEY) || ''
}

async function api<T = Record<string, unknown>>(
  action: string,
  payload: Record<string, unknown> = {},
): Promise<T & { ok: boolean; error?: string }> {
  try {
    const r = await fetch('/api/auth', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action, token: getToken(), ...payload }),
    })
    return await r.json()
  } catch {
    return { ok: false, error: '网络异常，请稍后再试' } as T & { ok: false; error: string }
  }
}

export async function refresh() {
  if (!getToken()) {
    cache = null
    emit()
    return
  }
  const r = await api<{ user: UserProfile }>('me')
  cache = r.ok ? r.user : null
  if (!r.ok && r.error?.includes('过期')) localStorage.removeItem(KEY)
  emit()
}

export async function login(username: string, password: string) {
  const r = await api<{ token: string; user: UserProfile }>('login', { username, password })
  if (r.ok) {
    localStorage.setItem(KEY, r.token)
    cache = r.user
    emit()
  }
  return r
}

export async function register(username: string, password: string, code: string) {
  const r = await api<{ token: string; user: UserProfile }>('register', { username, password, code })
  if (r.ok) {
    localStorage.setItem(KEY, r.token)
    cache = r.user
    emit()
  }
  return r
}

export async function logout() {
  await api('logout')
  localStorage.removeItem(KEY)
  cache = null
  emit()
}

export async function updateProfile(patch: Partial<UserProfile>) {
  const r = await api<{ user: UserProfile }>('updateProfile', patch as Record<string, unknown>)
  if (r.ok) {
    cache = r.user
    emit()
  }
  return r
}

export const changePassword = (oldPassword: string, newPassword: string) =>
  api('changePassword', { oldPassword, newPassword })

export const inviteStatus = () => api<{ open: boolean; left: number }>('inviteStatus')

export const setInvite = (code: string, openPassword: string, durationMin: number, maxUsers: number) =>
  api<{ invite: InviteState }>('setInvite', { code, openPassword, durationMin, maxUsers })
export const getInvite = () => api<{ invite: InviteState }>('getInvite')
export const closeInvite = () => api('closeInvite')

export function useAuth() {
  const [user, setUser] = useState<UserProfile | null | undefined>(cache)
  useEffect(() => {
    const f = () => setUser(cache)
    listeners.add(f)
    if (cache === undefined) void refresh()
    return () => {
      listeners.delete(f)
    }
  }, [])
  return { user: user ?? null, ready: user !== undefined }
}
