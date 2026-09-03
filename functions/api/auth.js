// Cloudflare Pages Function：账号系统（KV 持久化）——由 Netlify 移植，接口契约不变
const ADMIN_NAME = '18573854599'
const ADMIN_INIT_PASSWORD = 'perfect2017'

const enc = new TextEncoder()
async function sha(s) {
  const buf = await crypto.subtle.digest('SHA-256', enc.encode(s))
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('')
}
const hashPw = (pw, salt) => sha(salt + '::' + pw)
const rand = (n = 32) =>
  [...crypto.getRandomValues(new Uint8Array(n))].map((b) => b.toString(16).padStart(2, '0')).join('')

const now = () => Date.now()

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

    if (action === 'login') {
      const { username, password } = body
      if (!validName(username) && username !== ADMIN_NAME) return fail('账号格式不正确')
      const u = await getJSON(env, 'user:' + username)
      if (!u) return fail('账号不存在。如需注册，请在开放时段使用验证码注册', 404)
      if (u.hash !== (await hashPw(String(password ?? ''), u.salt))) return fail('密码错误', 401)
      const token = await makeSession(env, username)
      return ok({ token, user: publicUser(u) })
    }

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

    if (action === 'me') {
      const u = await userByToken(env, body.token)
      if (!u) return fail('未登录或会话已过期', 401)
      return ok({ user: publicUser(u) })
    }
    if (action === 'logout') {
      if (body.token) await env.CHEM_AUTH.delete('session:' + body.token).catch(() => {})
      return ok({})
    }

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
