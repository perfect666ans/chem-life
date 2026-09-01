import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router'
import { Check, KeyRound, LogOut, Plus, ShieldCheck, UserRound } from 'lucide-react'
import {
  changePassword,
  closeInvite,
  getInvite,
  setInvite,
  updateProfile,
  useAuth,
  logout,
  type InviteState,
} from '../lib/auth'

const AVATARS = ['🧪', '⚗️', '🔬', '🧫', '🧬', '💊', '🧂', '🔥', '💧', '❄️', '⚡', '🌡️',
  '🍋', '🍇', '🥛', '🍯', '🧅', '🥕', '🌽', '🍞', '🧀', '🥚', '🧊', '🍵']

const PRESET_TAGS = [
  // 学科方向
  '化学课代表', '有机化学', '无机化学', '结构化学', '分析化学', '物理化学', '电化学', '热化学', '平衡移动', '高分子',
  // 学习风格
  '刷题机器', '错题本', '笔记控', '手写笔记', '思维导图', '番茄钟', '早起学习', '夜猫子', '考前突击', '稳步提升',
  // 实验
  '实验达人', '试管爱好者', '滴定之王', '焰色反应', '银镜反应', '铝热反应', '安全意识满分', '白大褂', '器材收藏', '家庭实验室',
  // 兴趣
  '分子模型', '晶体收藏', '科普阅读', '科幻迷', '游戏玩家', '动漫', '音乐', '运动', '摄影', '美食',
  // 性格
  '社牛', '社恐', '完美主义', '细节控', '拖延症', '行动派', '好奇心', '冷静', '热血', '佛系',
  // 身份
  '初中生', '高一', '高二', '高三', '竞赛党', '强基计划', '大学生', '老师', '家长', '自学党',
  // 目标
  '满分化学', '竞赛金牌', '高考加油', '逆袭中', '年级前十', '进步之星', '坚持打卡', '目标985', '目标211', '上岸',
  // 化学情怀
  '门捷列夫', '侯德榜', '居里夫人', '拉瓦锡', '勒夏特列', '碳基生物', '氟老大', '钠遇水', '王水', '酯化反应',
  // 状态
  '学习中', '摸鱼中', '冲刺中', '备考中', '咖啡续命', '奶茶爱好者', '图书馆常客', '网课达人', '酸碱中和', '氧化还原',
  // 未来方向
  '化学师范', '医学预备', '药学方向', '材料科学', '环境科学', '食品科学', '能源化学', '未来科学家', '工程师', '研究员',
]

const inputCls =
  'w-full rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100'

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-6">
      <h2 className="mb-4 text-base font-bold text-slate-900">{title}</h2>
      {children}
    </section>
  )
}

export default function ProfilePage() {
  const { user, ready } = useAuth()
  const nav = useNavigate()
  const [msg, setMsg] = useState('')
  const [ok, setOk] = useState('')

  // 资料表单
  const [nickname, setNickname] = useState('')
  const [avatar, setAvatar] = useState('🧪')
  const [bio, setBio] = useState('')
  const [tags, setTags] = useState<string[]>([])
  const [customTag, setCustomTag] = useState('')
  const [showUsage, setShowUsage] = useState(false)
  const [showGameTime, setShowGameTime] = useState(false)

  // 改密
  const [oldPw, setOldPw] = useState('')
  const [newPw, setNewPw] = useState('')

  // 管理员邀请窗口
  const [inv, setInv] = useState<InviteState>(null)
  const [invCode, setInvCode] = useState('')
  const [invPw, setInvPw] = useState('')
  const [invMin, setInvMin] = useState(60)
  const [invMax, setInvMax] = useState(10)

  useEffect(() => {
    if (ready && !user) nav('/login', { replace: true })
  }, [ready, user, nav])

  useEffect(() => {
    if (!user) return
    setNickname(user.nickname)
    setAvatar(user.avatar)
    setBio(user.bio)
    setTags(user.tags)
    setShowUsage(user.showUsage)
    setShowGameTime(user.showGameTime)
    if (user.isAdmin) void getInvite().then((r) => r.ok && setInv(r.invite))
  }, [user])

  const flash = (okMsg: string, err?: string) => {
    setOk(err ? '' : okMsg)
    setMsg(err ?? '')
    setTimeout(() => {
      setOk('')
      setMsg('')
    }, 4000)
  }

  const saveProfile = async () => {
    const r = await updateProfile({ nickname, avatar, bio, tags, showUsage, showGameTime })
    flash('资料已保存', r.ok ? undefined : r.error)
  }
  const savePw = async () => {
    const r = await changePassword(oldPw, newPw)
    if (r.ok) {
      setOldPw('')
      setNewPw('')
      flash('密码已修改，之后请使用新密码登录')
    } else flash('', r.error)
  }
  const openInvite = async () => {
    const r = await setInvite(invCode, invPw, invMin, invMax)
    if (r.ok) setInv(r.invite)
    flash('登录权限已开放', r.ok ? undefined : r.error)
  }
  const shutInvite = async () => {
    const r = await closeInvite()
    if (r.ok) setInv(inv ? { ...inv, active: false } : inv)
    flash('已关闭开放', r.ok ? undefined : r.error)
  }

  const inviteLeft = useMemo(
    () => (inv ? inv.maxUsers - (inv.used || []).length : 0),
    [inv],
  )
  const inviteLive = !!(inv && inv.active && inv.expiresAt > Date.now() && inviteLeft > 0)

  if (!user) return null

  return (
    <main className="mx-auto max-w-3xl space-y-5 px-4 py-8">
      <div className="flex items-center gap-3">
        <span className="text-3xl">{user.avatar}</span>
        <div>
          <h1 className="text-xl font-bold text-slate-900">
            {user.nickname}
            <span className="ml-2 text-sm font-normal text-slate-400">@{user.username}</span>
          </h1>
          <p className="text-xs text-slate-500">
            {user.isAdmin ? '管理员 · 拥有登录权限管理' : '普通用户'}
          </p>
        </div>
        <button
          onClick={() => void logout().then(() => nav('/'))}
          className="ml-auto flex items-center gap-1.5 rounded-lg border border-slate-300 px-3 py-1.5 text-sm text-slate-600 hover:bg-slate-50"
        >
          <LogOut className="h-4 w-4" />
          退出登录
        </button>
      </div>

      {(msg || ok) && (
        <p className={`text-sm ${msg ? 'text-red-600' : 'text-emerald-600'}`}>{msg || ok}</p>
      )}

      {user.mustChangePw && (
        <p className="rounded-lg border border-amber-300 bg-amber-50 px-4 py-2.5 text-sm text-amber-700">
          你是首次登录：建议立即在下方「修改密码」设置自己的密码，之后可随时用新密码自由登录。
        </p>
      )}

      {/* 管理员：登录权限 */}
      {user.isAdmin && (
        <Section title="登录权限（仅管理员可见）">
          <div className="mb-4 rounded-lg bg-slate-50 px-4 py-3 text-sm text-slate-600">
            {inviteLive ? (
              <>
                状态：<span className="font-medium text-emerald-600">开放中</span> · 验证码{' '}
                <code className="rounded bg-white px-1.5 py-0.5 font-mono text-indigo-700">{inv!.code}</code>{' '}
                · 剩余名额 {inviteLeft}/{inv!.maxUsers} ·{' '}
                {new Date(inv!.expiresAt).toLocaleString('zh-CN')} 失效
                {!!(inv!.used || []).length && (
                  <div className="mt-1 text-xs text-slate-400">
                    已通过：{inv!.used.join('、')}
                  </div>
                )}
              </>
            ) : (
              <>状态：<span className="font-medium text-slate-500">未开放</span>（其他用户暂时无法注册）</>
            )}
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            <input
              className={inputCls}
              placeholder="数字验证码（4-12 位）"
              value={invCode}
              onChange={(e) => setInvCode(e.target.value.replace(/\D/g, ''))}
            />
            <input
              className={inputCls}
              placeholder="开放密码（他人首次注册用，≥6 位）"
              value={invPw}
              onChange={(e) => setInvPw(e.target.value)}
            />
            <label className="text-sm text-slate-600">
              起效时长（分钟）
              <input
                className={`${inputCls} mt-1`}
                type="number"
                min={1}
                value={invMin}
                onChange={(e) => setInvMin(Number(e.target.value))}
              />
            </label>
            <label className="text-sm text-slate-600">
              最大人数
              <input
                className={`${inputCls} mt-1`}
                type="number"
                min={1}
                value={invMax}
                onChange={(e) => setInvMax(Number(e.target.value))}
              />
            </label>
          </div>
          <div className="mt-4 flex gap-2">
            <button
              onClick={() => void openInvite()}
              className="flex items-center gap-1.5 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700"
            >
              <ShieldCheck className="h-4 w-4" />
              开启 / 重置开放
            </button>
            {inviteLive && (
              <button
                onClick={() => void shutInvite()}
                className="rounded-lg border border-red-300 px-4 py-2 text-sm text-red-600 hover:bg-red-50"
              >
                立即关闭
              </button>
            )}
          </div>
        </Section>
      )}

      {/* 个人信息 */}
      <Section title="个人信息">
        <div className="space-y-4">
          <div>
            <div className="mb-2 text-sm text-slate-600">头像</div>
            <div className="flex flex-wrap gap-1.5">
              {AVATARS.map((a) => (
                <button
                  key={a}
                  onClick={() => setAvatar(a)}
                  className={`flex h-9 w-9 items-center justify-center rounded-lg border text-lg ${
                    avatar === a ? 'border-indigo-500 bg-indigo-50' : 'border-slate-200 hover:bg-slate-50'
                  }`}
                >
                  {a}
                </button>
              ))}
            </div>
          </div>
          <label className="block text-sm text-slate-600">
            昵称
            <input className={`${inputCls} mt-1`} value={nickname} onChange={(e) => setNickname(e.target.value)} />
          </label>
          <label className="block text-sm text-slate-600">
            个人备注
            <textarea
              className={`${inputCls} mt-1 h-20 resize-none`}
              value={bio}
              onChange={(e) => setBio(e.target.value)}
              placeholder="写一句自我介绍…"
            />
          </label>
          <div className="flex gap-6">
            <label className="flex items-center gap-2 text-sm text-slate-600">
              <input type="checkbox" checked={showUsage} onChange={(e) => setShowUsage(e.target.checked)} />
              公开我的软件使用时长
            </label>
            <label className="flex items-center gap-2 text-sm text-slate-600">
              <input type="checkbox" checked={showGameTime} onChange={(e) => setShowGameTime(e.target.checked)} />
              公开我的游戏时长
            </label>
          </div>
        </div>
      </Section>

      {/* 标签 */}
      <Section title={`我的标签（已选 ${tags.length}/30）`}>
        <div className="mb-3 flex flex-wrap gap-1.5">
          {tags.map((t) => (
            <span
              key={t}
              className="flex items-center gap-1 rounded-full bg-indigo-50 px-2.5 py-1 text-xs text-indigo-700"
            >
              {t}
              <button onClick={() => setTags(tags.filter((x) => x !== t))} className="text-indigo-400 hover:text-indigo-700">
                ×
              </button>
            </span>
          ))}
          {!tags.length && <span className="text-xs text-slate-400">尚未选择标签</span>}
        </div>
        <div className="mb-3 flex gap-2">
          <input
            className={inputCls}
            placeholder="自定义标签（20 字以内，数据库里没有也可以加）"
            value={customTag}
            onChange={(e) => setCustomTag(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && customTag.trim()) {
                if (!tags.includes(customTag.trim())) setTags([...tags, customTag.trim()].slice(0, 30))
                setCustomTag('')
              }
            }}
          />
          <button
            onClick={() => {
              if (customTag.trim() && !tags.includes(customTag.trim()))
                setTags([...tags, customTag.trim()].slice(0, 30))
              setCustomTag('')
            }}
            className="flex shrink-0 items-center gap-1 rounded-lg border border-slate-300 px-3 text-sm text-slate-600 hover:bg-slate-50"
          >
            <Plus className="h-4 w-4" />
            添加
          </button>
        </div>
        <div className="flex max-h-56 flex-wrap gap-1.5 overflow-y-auto rounded-lg border border-slate-100 bg-slate-50 p-3">
          {PRESET_TAGS.map((t) => {
            const on = tags.includes(t)
            return (
              <button
                key={t}
                onClick={() => setTags(on ? tags.filter((x) => x !== t) : [...tags, t].slice(0, 30))}
                className={`flex items-center gap-1 rounded-full border px-2.5 py-1 text-xs transition ${
                  on
                    ? 'border-indigo-500 bg-indigo-100 text-indigo-700'
                    : 'border-slate-200 bg-white text-slate-600 hover:border-indigo-300'
                }`}
              >
                {on && <Check className="h-3 w-3" />}
                {t}
              </button>
            )
          })}
        </div>
        <button
          onClick={() => void saveProfile()}
          className="mt-4 flex items-center gap-1.5 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700"
        >
          <UserRound className="h-4 w-4" />
          保存资料
        </button>
      </Section>

      {/* 修改密码 */}
      <Section title="修改密码">
        <div className="grid gap-3 sm:grid-cols-2">
          <input
            className={inputCls}
            type="password"
            placeholder="当前密码"
            value={oldPw}
            onChange={(e) => setOldPw(e.target.value)}
          />
          <input
            className={inputCls}
            type="password"
            placeholder="新密码（至少 6 位）"
            value={newPw}
            onChange={(e) => setNewPw(e.target.value)}
          />
        </div>
        <button
          onClick={() => void savePw()}
          disabled={!oldPw || newPw.length < 6}
          className="mt-3 flex items-center gap-1.5 rounded-lg border border-slate-300 px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 disabled:opacity-50"
        >
          <KeyRound className="h-4 w-4" />
          确认修改
        </button>
      </Section>
    </main>
  )
}
