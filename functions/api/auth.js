// Cloudflare Pages Function：账号系统（KV 持久化）
// 路由：POST /api/auth  {action: ...}
// 由 netlify/functions/auth.js 移植，接口契约完全一致，前端无需改动
// 环境变量/绑定：KV namespace 绑定为 CHEM_AUTH
//
// - bootstrap        惰性创建管理员（账号见 ADMIN_NAME；初始密码登录后请立即修改）
// - login            {username, password}
// - register         {username, password, code}   需要管理员开放的邀请窗口
// - me               {token}
// - logout           {token}
// - updateProfile    {token, nickname, avatar, bio, tags, showUsage, showGameTime}
// - changePassword   {token, oldPassword, newPassword}
// - setInvite        {token, code, openPassword, durationMin, maxUsers}   仅管理员
// - getInvite        {token}                                             仅管理员
// - closeInvite      {token}                                             仅管理员
// - inviteStatus     {}              公开：当前是否开放注册

const ADMIN_NAME = '18573854599'
// ⚠️ 部署后请第一时间登录并修改管理员密码（此初始密码已出现在公开仓库历史中）
const ADMIN_INIT_PASSWORD = 'perfect2017'

// --- Web Crypto 工具（Pages Functions 无 node:crypto） ---
const enc = new TextEncoder()
async function sha(s) {
  const buf = await crypto.subtle.digest('SHA-256', enc.encode(s))
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('')
}
const hashPw = (pw, salt) => sha(salt + '::' + pw)
const rand = (n = 32) =>
  [...crypto.getRandomValues(new Uint8Array(n))].map((b) => b.toString(16).padStart(2, '0')).join('')

const now = () => Date.now()

// --- KV 访问（替代 Netlify Blobs） ---
async function getJSON(env, key) {
  return (await env.CHEM_AUTH.get(key, 'json')) ?? null
}
async function setJSON(env, key, val) {
  await env.CHEM_AUTH.put(key, JSON.stringify(val))
}

async function bootstrap(env) {
  if (!(await getJSON(env, 'user:' + ADMIN_NAME))) {
    const salt = rand(16)
    await setJSON(env, 'user:' + ADMIN_NAME, {
      username: ADMIN_NAME,
      salt,
      hash: await hashPw(ADMIN_INIT_PASSWORD, salt),
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

async function userByToken(env, token) {
  if (!token || typeof token !== 'string') return null
  const s = await getJSON(env, 'session:' + token)
  if (!s || s.expiresAt < now()) return null
  return (await getJSON(env, 'user:' + s.username)) || null
}

async function makeSession(env, username) {
  const token = rand(24)
  await setJSON(env, 'session:' + token, { username, expiresAt: now() + 30 * 86400e3 })
  return token
}

const json = (obj, status = 200) =>
  new Response(JSON.stringify(obj), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' },
  })
const ok = (data) => json({ ok: true, ...data })
const fail = (message, code = 400) => json({ ok: false, error: message }, code)

const validName = (s) => typeof s === 'string' && /^[\w一-龥-]{2,24}$/.test(s)

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
    await bootstrap(env)

    /* ---------- 登录 ---------- */
    if (action === 'login') {
      const { username, password } = body
      if (!validName(username) && username !== ADMIN_NAME) return fail('账号格式不正确')
      const u = await getJSON(env, 'user:' + username)
      if (!u) return fail('账号不存在。如需注册，请在开放时段使用验证码注册', 404)
      if (u.hash !== (await hashPw(String(password ?? ''), u.salt))) return fail('密码错误', 401)
      const token = await makeSession(env, username)
      return ok({ token, user: publicUser(u) })
    }

    /* ---------- 注册（邀请窗口） ---------- */
    if (action === 'register') {
      const { username, password, code } = body
      if (!validName(username)) return fail('账号需为 2-24 位字母/数字/中文/下划线')
      if (username === ADMIN_NAME) return fail('该账号已被占用')
      if (await getJSON(env, 'user:' + username)) return fail('该账号已被注册')
      const inv = await getJSON(env, 'invite')
      if (!inv || !inv.active || inv.expiresAt < now())
        return fail('当前未开放注册，请联系管理员开放登录权限', 403)
      if (String(code ?? '') !== String(inv.code)) return fail('数字验证码错误', 401)
      if (String(password ?? '') !== String(inv.openPassword))
        return fail('初始密码错误：首次注册需使用管理员设置的开放密码', 401)
      if ((inv.used || []).length >= inv.maxUsers) return fail('本次开放名额已满', 403)
      const salt = rand(16)
      const user = {
        username, salt, hash: await hashPw(String(password), salt), isAdmin: false,
        nickname: username, avatar: '⚗️', bio: '', tags: [],
        showUsage: false, showGameTime: false, createdAt: now(), mustChangePw: true,
      }
      await setJSON(env, 'user:' + username, user)
      inv.used = [...(inv.used || []), username]
      if (inv.used.length >= inv.maxUsers) inv.active = false
      await setJSON(env, 'invite', inv)
      const token = await makeSession(env, username)
      return ok({ token, user: publicUser(user) })
    }

    /* ---------- 会话 ---------- */
    if (action === 'me') {
      const u = await userByToken(env, body.token)
      if (!u) return fail('未登录或会话已过期', 401)
      return ok({ user: { ...publicUser(u), usage: (await getJSON(env, 'usage:' + u.username)) || {} } })
    }
    /* 使用时长心跳：前端每 ~20s 上报一次各模块停留秒数（W-06） */
    if (action === 'heartbeat') {
      const u = await userByToken(env, body.token)
      if (!u) return fail('未登录', 401)
      const mod = String(body.module || '').slice(0, 24)
      const secs = Math.min(Math.max(Number(body.seconds) || 0, 0), 120)
      if (mod && secs > 0) {
        const key = 'usage:' + u.username
        const usage = (await getJSON(env, key)) || {}
        usage[mod] = (usage[mod] || 0) + Math.round(secs)
        await setJSON(env, key, usage)
      }
      return ok({})
    }
    if (action === 'logout') {
      if (body.token) await env.CHEM_AUTH.delete('session:' + body.token).catch(() => {})
      return ok({})
    }

    /* ---------- 个人资料 ---------- */
    if (action === 'updateProfile') {
      const u = await userByToken(env, body.token)
      if (!u) return fail('未登录', 401)
      const pick = (v, max = 200) => (typeof v === 'string' ? v.slice(0, max) : undefined)
      if (body.nickname !== undefined) u.nickname = pick(body.nickname, 24) || u.username
      if (body.avatar !== undefined) u.avatar = pick(body.avatar, 8)
      if (body.bio !== undefined) u.bio = pick(body.bio, 300)
      if (Array.isArray(body.tags)) u.tags = [...new Set(body.tags.map((t) => String(t).slice(0, 20)))].slice(0, 30)
      if (body.showUsage !== undefined) u.showUsage = !!body.showUsage
      if (body.showGameTime !== undefined) u.showGameTime = !!body.showGameTime
      await setJSON(env, 'user:' + u.username, u)
      return ok({ user: publicUser(u) })
    }
    if (action === 'changePassword') {
      const u = await userByToken(env, body.token)
      if (!u) return fail('未登录', 401)
      if (u.hash !== (await hashPw(String(body.oldPassword ?? ''), u.salt))) return fail('原密码错误', 401)
      const np = String(body.newPassword ?? '')
      if (np.length < 6) return fail('新密码至少 6 位')
      u.salt = rand(16)
      u.hash = await hashPw(np, u.salt)
      u.mustChangePw = false
      await setJSON(env, 'user:' + u.username, u)
      return ok({})
    }

    if (action === 'bindPhone') {
      const u = await userByToken(env, body.token)
      if (!u) return fail('未登录', 401)
      const phone = String(body.phone || '').trim()
      if (!/^1\d{10}$/.test(phone)) return fail('手机号格式不正确（需 11 位大陆手机号）')
      const all = await env.CHEM_AUTH.list({ prefix: 'user:' })
      for (const k of all.keys) {
        const other = await getJSON(env, k.name)
        if (other && other.username !== u.username && other.phone === phone) return fail('该手机号已被其他账号绑定', 409)
      }
      u.phone = phone
      await setJSON(env, 'user:' + u.username, u)
      return ok({ user: { ...publicUser(u), usage: (await getJSON(env, 'usage:' + u.username)) || {} } })
    }
    if (action === 'resetPassword') {
      const u = await getJSON(env, 'user:' + String(body.username || '').trim())
      if (!u) return fail('账号不存在', 404)
      if (!u.phone) return fail('该账号未绑定手机号，请联系站长重置', 403)
      if (u.phone !== String(body.phone || '').trim()) return fail('手机号与账号绑定的不一致', 401)
      const np = String(body.newPassword || '')
      if (np.length < 6) return fail('新密码至少 6 位')
      u.salt = rand(16)
      u.hash = await hashPw(np, u.salt)
      u.mustChangePw = false
      await setJSON(env, 'user:' + u.username, u)
      return ok({})
    }

    /* ---------- 管理员：登录权限（邀请窗口） ---------- */
    if (action === 'setInvite') {
      const u = await userByToken(env, body.token)
      if (!u || !u.isAdmin) return fail('无权限', 403)
      const code = String(body.code ?? '').trim()
      const openPassword = String(body.openPassword ?? '')
      if (!/^\d{4,12}$/.test(code)) return fail('验证码需为 4-12 位数字')
      if (openPassword.length < 6) return fail('开放密码至少 6 位')
      const durationMin = Math.min(Math.max(Number(body.durationMin) || 60, 1), 7 * 24 * 60)
      const maxUsers = Math.min(Math.max(Number(body.maxUsers) || 10, 1), 500)
      await setJSON(env, 'invite', {
        code, openPassword, active: true,
        expiresAt: now() + durationMin * 60e3,
        maxUsers, used: [], createdAt: now(),
      })
      return ok({ invite: await getJSON(env, 'invite') })
    }
    if (action === 'getInvite') {
      const u = await userByToken(env, body.token)
      if (!u || !u.isAdmin) return fail('无权限', 403)
      const inv = await getJSON(env, 'invite')
      if (inv && inv.expiresAt < now()) inv.active = false
      return ok({ invite: inv || null })
    }
    if (action === 'closeInvite') {
      const u = await userByToken(env, body.token)
      if (!u || !u.isAdmin) return fail('无权限', 403)
      const inv = await getJSON(env, 'invite')
      if (inv) { inv.active = false; await setJSON(env, 'invite', inv) }
      return ok({})
    }
    if (action === 'inviteStatus') {
      const inv = await getJSON(env, 'invite')
      const open = !!(inv && inv.active && inv.expiresAt > now() && (inv.used || []).length < inv.maxUsers)
      return ok({ open, left: open ? inv.maxUsers - (inv.used || []).length : 0 })
    }
    return fail('未知操作', 404)
  } catch (e) {
    return fail('服务器错误：' + String((e && e.message) || e), 500)
  }
}
