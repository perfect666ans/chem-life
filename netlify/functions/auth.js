// Netlify Function：账号系统（Netlify Blobs 持久化）
// 路由：POST /api/auth  {action: ...}
// - bootstrap        惰性创建管理员（18573854599 / 初始密码见管理员本人）
// - login            {username, password}
// - register         {username, password, code}   需要管理员开放的邀请窗口；password 须等于窗口密码
// - me               {token}
// - logout           {token}
// - updateProfile    {token, nickname, avatar, bio, tags, showUsage, showGameTime}
// - changePassword   {token, oldPassword, newPassword}
// - setInvite        {token, code, openPassword, durationMin, maxUsers}   仅管理员
// - getInvite        {token}                                             仅管理员
// - closeInvite      {token}                                             仅管理员
// - inviteStatus     {}              公开：当前是否开放注册（不泄露验证码/密码）

import { getStore } from '@netlify/blobs'
import crypto from 'node:crypto'

const ADMIN_NAME = '18573854599'
const ADMIN_INIT_PASSWORD = 'perfect2017' // 管理员初始密码（首次部署用，登录后请立即修改）

const store = () => getStore({ name: 'chem-auth', consistency: 'strong' })

const now = () => Date.now()
const sha = (s) => crypto.createHash('sha256').update(s).digest('hex')
const hashPw = (pw, salt) => sha(salt + '::' + pw)
const rand = (n = 32) => crypto.randomBytes(n).toString('hex')

async function getJSON(key) {
  const v = await store().get(key, { type: 'json' })
  return v ?? null
}
async function setJSON(key, val) {
  await store().setJSON(key, val)
}

async function bootstrap() {
  if (!(await getJSON('user:' + ADMIN_NAME))) {
    const salt = rand(16)
    await setJSON('user:' + ADMIN_NAME, {
      username: ADMIN_NAME,
      salt,
      hash: hashPw(ADMIN_INIT_PASSWORD, salt),
      isAdmin: true,
      nickname: '站长',
      avatar: '🧪',
      bio: '',
      tags: [],
      showUsage: false,
      showGameTime: false,
      createdAt: now(),
    })
  }
}

function publicUser(u) {
  const { salt, hash, ...rest } = u
  return rest
}

async function userByToken(token) {
  if (!token || typeof token !== 'string') return null
  const s = await getJSON('session:' + token)
  if (!s || s.expiresAt < now()) return null
  const u = await getJSON('user:' + s.username)
  return u || null
}

async function makeSession(username) {
  const token = rand(24)
  await setJSON('session:' + token, { username, expiresAt: now() + 30 * 86400e3 })
  return token
}

const ok = (data) => resp(200, { ok: true, ...data })
const fail = (message, code = 400) => resp(code, { ok: false, error: message })
const resp = (statusCode, obj) => ({
  statusCode,
  headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' },
  body: JSON.stringify(obj),
})

const validName = (s) => typeof s === 'string' && /^[\w一-龥-]{2,24}$/.test(s)

export const handler = async (event) => {
  if (event.httpMethod !== 'POST') return fail('仅支持 POST', 405)
  let body
  try { body = JSON.parse(event.body || '{}') } catch { return fail('请求格式错误') }
  const { action } = body

  try {
    await bootstrap()

    /* ---------- 登录 ---------- */
    if (action === 'login') {
      const { username, password } = body
      if (!validName(username) && username !== ADMIN_NAME) return fail('账号格式不正确')
      const u = await getJSON('user:' + username)
      if (!u) return fail('账号不存在。如需注册，请在开放时段使用验证码注册', 404)
      if (u.hash !== hashPw(String(password ?? ''), u.salt)) return fail('密码错误', 401)
      const token = await makeSession(username)
      return ok({ token, user: publicUser(u) })
    }

    /* ---------- 注册（邀请窗口） ---------- */
    if (action === 'register') {
      const { username, password, code } = body
      if (!validName(username)) return fail('账号需为 2-24 位字母/数字/中文/下划线')
      if (username === ADMIN_NAME) return fail('该账号已被占用')
      if (await getJSON('user:' + username)) return fail('该账号已被注册')
      const inv = await getJSON('invite')
      if (!inv || !inv.active || inv.expiresAt < now())
        return fail('当前未开放注册，请联系管理员开放登录权限', 403)
      if (String(code ?? '') !== String(inv.code))
        return fail('数字验证码错误', 401)
      if (String(password ?? '') !== String(inv.openPassword))
        return fail('初始密码错误：首次注册需使用管理员设置的开放密码', 401)
      if ((inv.used || []).length >= inv.maxUsers)
        return fail('本次开放名额已满', 403)
      const salt = rand(16)
      const user = {
        username, salt, hash: hashPw(String(password), salt), isAdmin: false,
        nickname: username, avatar: '⚗️', bio: '', tags: [],
        showUsage: false, showGameTime: false, createdAt: now(), mustChangePw: true,
      }
      await setJSON('user:' + username, user)
      inv.used = [...(inv.used || []), username]
      if (inv.used.length >= inv.maxUsers) inv.active = false
      await setJSON('invite', inv)
      const token = await makeSession(username)
      return ok({ token, user: publicUser(user) })
    }

    /* ---------- 会话 ---------- */
    if (action === 'me') {
      const u = await userByToken(body.token)
      if (!u) return fail('未登录或会话已过期', 401)
      return ok({ user: publicUser(u) })
    }
    if (action === 'logout') {
      if (body.token) await store().delete('session:' + body.token).catch(() => {})
      return ok({})
    }

    /* ---------- 个人资料 ---------- */
    if (action === 'updateProfile') {
      const u = await userByToken(body.token)
      if (!u) return fail('未登录', 401)
      const pick = (v, max = 200) => (typeof v === 'string' ? v.slice(0, max) : undefined)
      if (body.nickname !== undefined) u.nickname = pick(body.nickname, 24) || u.username
      if (body.avatar !== undefined) u.avatar = pick(body.avatar, 8)
      if (body.bio !== undefined) u.bio = pick(body.bio, 300)
      if (Array.isArray(body.tags)) u.tags = [...new Set(body.tags.map((t) => String(t).slice(0, 20)))].slice(0, 30)
      if (body.showUsage !== undefined) u.showUsage = !!body.showUsage
      if (body.showGameTime !== undefined) u.showGameTime = !!body.showGameTime
      await setJSON('user:' + u.username, u)
      return ok({ user: publicUser(u) })
    }
    if (action === 'changePassword') {
      const u = await userByToken(body.token)
      if (!u) return fail('未登录', 401)
      if (u.hash !== hashPw(String(body.oldPassword ?? ''), u.salt)) return fail('原密码错误', 401)
      const np = String(body.newPassword ?? '')
      if (np.length < 6) return fail('新密码至少 6 位')
      u.salt = rand(16)
      u.hash = hashPw(np, u.salt)
      u.mustChangePw = false
      await setJSON('user:' + u.username, u)
      return ok({})
    }

    /* ---------- 管理员：登录权限（邀请窗口） ---------- */
    if (action === 'setInvite') {
      const u = await userByToken(body.token)
      if (!u || !u.isAdmin) return fail('无权限', 403)
      const code = String(body.code ?? '').trim()
      const openPassword = String(body.openPassword ?? '')
      if (!/^\d{4,12}$/.test(code)) return fail('验证码需为 4-12 位数字')
      if (openPassword.length < 6) return fail('开放密码至少 6 位')
      const durationMin = Math.min(Math.max(Number(body.durationMin) || 60, 1), 7 * 24 * 60)
      const maxUsers = Math.min(Math.max(Number(body.maxUsers) || 10, 1), 500)
      await setJSON('invite', {
        code, openPassword, active: true,
        expiresAt: now() + durationMin * 60e3,
        maxUsers, used: [], createdAt: now(),
      })
      return ok({ invite: await getJSON('invite') })
    }
    if (action === 'getInvite') {
      const u = await userByToken(body.token)
      if (!u || !u.isAdmin) return fail('无权限', 403)
      const inv = await getJSON('invite')
      if (inv && inv.expiresAt < now()) inv.active = false
      return ok({ invite: inv || null })
    }
    if (action === 'closeInvite') {
      const u = await userByToken(body.token)
      if (!u || !u.isAdmin) return fail('无权限', 403)
      const inv = await getJSON('invite')
      if (inv) { inv.active = false; await setJSON('invite', inv) }
      return ok({})
    }
    if (action === 'inviteStatus') {
      const inv = await getJSON('invite')
      const open = !!(inv && inv.active && inv.expiresAt > now() && (inv.used || []).length < inv.maxUsers)
      return ok({ open, left: open ? inv.maxUsers - (inv.used || []).length : 0 })
    }
    if (action === 'debugEnv') {
      // 仅返回环境变量名（不含值），用于诊断 Blobs 自动配置
      return ok({
        keys: Object.keys(process.env).filter((k) => /NETLIFY|BLOB|AWS|SITE/i.test(k)).sort(),
      })
    }

    return fail('未知操作', 404)
  } catch (e) {
    return fail('服务器错误：' + String(e && e.message || e), 500)
  }
}
