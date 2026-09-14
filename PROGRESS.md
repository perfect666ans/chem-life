# PROGRESS · 项目进展笔记

> 用途：双设备切换时恢复上下文。每次结束工作前更新本文件并 commit + push；
> 换设备后先 `git pull`，再让 Kimi 读这个文件即可无缝继续。

## 项目概况

- 名称：chem-life（化学生活网站）
- 技术栈：React 19 + TypeScript + Vite + Tailwind CSS + shadcn/ui
- 线上地址：https://huaxue-shenghuo.pages.dev/（互动社区）｜ https://zao-chem.com（正式主站，2026-09-09 上线）
- 仓库：https://github.com/perfect666ans/chem-life （**私有**，2026-08-31 由公开转为私密）
- 部署：Cloudflare Pages，`npm run build` → `dist/`；登录/论坛/化合物代理由 Cloudflare Pages Functions（`functions/api/`）+ KV 承载（2026-09-03 迁移完成，六项验收全过）；Netlify 已废弃，netlify/ 目录与 netlify.toml 已于 2026-09-14 删除（历史遗留）

## 页面结构（src/pages/）

| 页面 | 文件 | 说明 |
| --- | --- | --- |
| 首页 | Home.tsx | 已浅色化 |
| 厨房化学 | Kitchen.tsx | |
| 数据库 | Database.tsx | |
| 氨基酸 | AminoAcids.tsx | 含增肌模块 |
| 维生素速查 | Vitamins.tsx | |
| PubChem 查询 | PubChem.tsx | 走 /api/pubchem 代理 |
| 教学实验室 | Teaching.tsx | `/teaching` 展示门户；3D 实验室静态页在 `public/teaching/` |

## 最近完成

- 2026-08-31 修复同步：首页浅色化 + 氨基酸增肌模块 + 维生素速查（commit efd2173）
- 2026-08-31 双设备基础设施：删除项目内重复的 .ssh 私钥副本（真钥在 `~/.ssh/`）、`.gitignore` 加入 `.ssh/`、仓库转为私有
- 2026-08-31 教学模块 v1：新增 `/teaching` 展示门户页（Teaching.tsx）；两个 3D 实验室作为静态页放入 `public/teaching/`（chem_lab1.1.html=VSEPR 分子构型，chem_lab1.2.html=晶体结构），返回按钮指向 `/teaching`
- 2026-08-31 晚 实验室按 tk-chem.cc 设计系统重做：和紙/墨朱/藍三主题切换（localStorage `ch-theme-lab` 共享）、衬线标题、朱红点缀；顺带修复原版 bug——晶体实验室切换物质时信息卡不同步、碳原子 #333 在深色画布不可见（改 0x9aa0a6）。重组装脚本在工作区 `rebuild_labs.py`
- 2026-09-01 氨基酸页补充化学信息：20 种氨基酸均加 `en`/`formula`/`structure` 字段；键线式用 PubChem 2D 图（`/api/pubchem/compound/name/<en>/PNG` 代理优先，直连回退，再失败显示占位）
- 2026-09-01 晶体实验室重写完成（commit c219b5b）：31 种晶体（离子 11/金属 12/共价 4/分子 3/混合 1）；**修复重大 bug：生成器 `x % 1.0` 把分数坐标 1.0 折回 0，导致晶胞正半侧原子全丢**；晶胞延展滑块、真立方体切割（clipping planes，顶点 1/8）、真实比例模型（半径相切）、按种类微粒显隐（单一种自动隐藏）、二维投影点阵 4 视角（尊重显隐、弹层排版后再绘制）。生成脚本：工作区 `build_crystal_lab.py`（改数据后运行它重组装 chem_lab1.2.html）
- 2026-09-01 VSEPR 实验室重写完成（commit ed329e2）：184 种分子 = 无机 77 + 离子团 50（阳 14/阴 36）+ 有机 57；Python 几何引擎（VSEPR 模板 + 多中心递归布局：交错扭转、sp2 共轭对齐；苯/萘/环丙烷/环氧乙烷/环己烷椅式精确几何）；σ 云蓝 #6aa6dd / π 云红 #e06b6b / 孤对云紫 #b89ae8，云内悬浮光点严格采样在椭球内（×0.72）；双键 π 透镜、三键圆柱壳；窄屏右栏变抽屉。生成脚本：工作区 `build_vsepr_lab.py`（外壳 CSS/主题 JS 提取自 chem_lab1.2.html）
- 2026-09-01 门户重排（commit f82bb15）：Teaching.tsx 改为 tk-chem.cc/nav.html 讲座目录式——罗马数字六大分区、衬线标题、朱红 accent、编号卡片「进入 →」；未做模块标「建设中」
- 2026-09-01 登录系统（commit 5eb4c72）：`netlify/functions/auth.js` + Netlify Blobs（store `chem-auth`）；管理员 18573854599 惰性初始化（初始密码见对话记录，**首次登录后应立即在 /profile 修改**）；邀请窗口 = 数字验证码 + 开放密码 + 起效时长 + 最大人数；他人注册须用开放密码，首次登录后改密即自由登录；/login、/profile（100 预设标签+自定义、头像、时长公开开关）；顶栏按角色显示「登录权限」/「个人信息」
- 2026-09-01 登录系统**后端全链路实测通过**（BLOBS_TOKEN 方案落地）：Netlify CLI 已登录本机（`netlify login` 授权完成，token 在 `%APPDATA%\netlify\Config\config.json`）；`netlify env:set BLOBS_TOKEN=<CLI token> --context production` 已设置；本地直接调用打包函数实测 10 步全过（inviteStatus/管理员登录/setInvite/注册/改资料/改密/新密码重登/me/closeInvite）。**注意**：实测向生产 Blobs 写入了管理员账号和一个测试号 testuser01（密码已隐去；Netlify 平台已废弃，无实际风险）
- 2026-09-01 核外电子排布实验室完成（chem_lab1.3.html，门户 Ⅰ-04 已点亮）：118 元素周期表点选；玻尔壳层动画（Canvas 2D）；轨道方框图（泡利+洪特，Fe 3d⁶/4s² 实测正确）；排布式三形态（完整/简化[Ar] 式/价电子层）；构造原理填充链高亮（最后填入能级实心）；Cr/Cu/Pd 等 21 个排布例外内置；常见离子切换（Fe²⁺/Fe³⁺ 先失 4s 实测正确、Cl⁻ 得电子正确）；同周期/同族半径对比条。生成脚本：工作区 `build_electron_lab.py`（外壳同样提取自 chem_lab1.2.html）。已本地浏览器截图验证

## 下一步（待办）
- [ ] chem_lab7.1/7.2/7.3 三个游戏无生成脚本只能手工维护，下次改动时评估是否补脚本

- [ ] 复习板块（知识球/闪卡/挑战树）、有机三大模块、反应原理四大模块、游戏板块：目前均为门户占位
- [ ] 交流论坛、排行榜/统计（依赖登录系统统计接口，当前仅有 showUsage/showGameTime 开关字段）
- [x] ✅ 登录/论坛/化合物代理已迁移至 Cloudflare Pages Functions（2026-09-03 完成，六项验收全过）；netlify/ 为历史遗留，已于 2026-09-14 删除
- [ ] 论坛/排行需要新增 Blobs 表（帖子、积分）

## 双设备工作流约定

1. 开始工作：`git pull`
2. 结束工作：更新本文件 → `git add -A && git commit && git push`
3. 不要把私钥、`.env` 等敏感文件放进仓库
4. 换设备首次：`npm install`；GitHub 凭据需登录一次（Netlify CLI 已不需要）

## 环境备注

- 设备 A（风逝台式机）：GitHub 直连偶发超时，push 失败多重试几次即可；npm/node 不在 PATH，构建用 `%APPDATA%\kimi-desktop\daimon-share\daimon\command-process-owner\bin\npm.cmd`
- **不要 `taskkill /F /IM node.exe`**——会误杀 Kimi 自身运行时导致断连；停 dev server 用 `netstat -ano | grep :端口` 找 PID 再按 PID 杀
- 教学实验室依赖 Three.js CDN（jsdelivr / unpkg），离线环境会加载失败
- 本地 vite dev 没有 Pages Functions，`/api/pubchem/*` 与 `/api/auth` 在本地 404（氨基酸键线式图有直连回退）；线上由 Cloudflare Pages Functions 提供，正常
- 两个实验室均由工作区 Python 生成器组装：`build_crystal_lab.py`（晶体，31 种数据+JS 模板）、`build_vsepr_lab.py`（分子，184 种+几何引擎）。**改分子/晶体数据请改生成器再运行，不要直接手改 HTML**
- 2026-09-01 化学闪卡复习完成（chem_lab2.2.html，门户 Ⅱ-02 点亮）：10 章 150 张精编卡（必修一二+选必 1-3）；Leitner 记忆盒（认识/模糊/不认识 → 盒 0-5，间隔 1/2/4/7/15 天，localStorage `chem-fc-progress-v1`）；智能复习（到期+新卡优先）/顺序/随机三模式；章节筛选、关键词查找、连胜计数、清空进度。生成脚本：工作区 `build_flashcards.py`
- 2026-09-01 化学反应的热效应完成（chem_lab4.1.html，门户 Ⅳ-01 点亮）：键能法 ΔH 计算器（8 预设反应，数值与教材一致：H₂+Cl₂ −183、CH₄ −802、合成氨 −92 等）；断键/成键清单自由增删改（键能可改）；能量-反应进程 Canvas 图（活化能垒+ΔH 箭头+吸放热底色）；盖斯定律演示（拖中间态能量，两段之和恒等于直接路径，实测 −250+(−144)=−394）。生成脚本：工作区 `build_thermo_lab.py`
- 2026-09-01 修复：两个新实验室生成器误用不存在的 CSS 变量 `--fg`/`--bg`（外壳实际是 `--ink`/`--surface`），已批量修正；外壳布局在窄屏（<900px）三栏挤压，闪卡页已加窄屏 padding 适配，桌面宽度（zoom 模拟 1280px）截图验证正常
- 2026-09-01 电化学实验室完成（chem_lab4.4.html，门户 Ⅳ-04 点亮）：7 种装置预设（Zn-Cu / Fe-Cu / Cu-Ag 原电池、电解 CuCl₂、电解饱和食盐水、铁镀铜、钢铁吸氧腐蚀）；Canvas 动画：导线电子流（方向随装置切换）、电表指针摆动/直流电源框、电极溶解变细与析出镀层、气泡上升、阴/阳离子分色迁移、铁锈生成标注；回路开关+速度滑块；判断口诀与放电顺序表。生成脚本：工作区 `build_electro_lab.py`。原电池/电解池两种模式均已截图验证
- 2026-09-01 水溶液中的离子平衡完成（chem_lab4.3.html，门户 Ⅳ-03 点亮）：pH 对数标尺（c(H⁺) 滑块 10⁰~10⁻¹⁴ + 13 个常见物质锚点交错标注 + Kw 联动显示）；中和滴定曲线三种体系（强强突跃 3.6→10.4 实测正确；强碱滴弱酸起点 pH2.9、半计量点 pH=pKa 4.74、计量点 8.7 正确；强酸滴弱碱）；指示剂变色域着色（甲基橙/石蕊/酚酞）；体积游标实时 pH；盐类水解速查表 12 条。生成脚本：工作区 `build_solution_lab.py`
- 2026-09-01 速率与平衡沙盘完成（chem_lab4.2.html，门户 Ⅳ-02 点亮）：粒子碰撞容器（NO₂ 红棕/N₂O₄ 无色等 3 预设：NO₂⇌N₂O₄、合成氨、醋酸电离）；A⇌B 概率互变达到动态平衡（实测比例约 pf:pb=2:1）；粒子数-时间曲线显示平台+微观波动；温度/压强/浓度三滑块扰动 → 勒夏特列方向判断文案 + 转化概率联动；重置按钮。生成脚本：工作区 `build_kinetics_lab.py`
- 2026-09-01 CBTI 化学人格鉴定完成（chem_lab5.3.html，门户 Ⅴ-03 点亮）：16 题 × 4 维度（能量/联结/行为/状态）→ 16 种物质人格（钠·烈火侠客、金刚石·秩序之王、氦·惰性观察者等，各配 emoji/描述/标签/四维条形图）；结果卡可复制分享；16 型图鉴可点开查看；再测一次重置。全 B 路径实测得 1111=氦 ✓。生成脚本：工作区 `build_cbti.py`
- 2026-09-01 有机系统命名中心完成（chem_lab3.2.html，门户 Ⅲ-02 点亮）：随机生成烷烃键线式（SVG 锯齿链+支链）四选一闯关；命名引擎=最长链+最低位次组（字典序）+相同基团合并+甲基在前；**防错**：生成器保证所画主链严格最长（甲基 max(p-1,n-p)+2<n、乙基 +3<n），500 次随机 brute-force 校验 0 错误；干扰项=反向编号/主链±1/位次偏移；连胜纪录+错题本（localStorage）；命名规则与官能团速查表。生成脚本：工作区 `build_naming_lab.py`
- 2026-09-01 同分异构体闯关完成（chem_lab3.3.html，门户 Ⅲ-03 点亮）：5 章 27 题四选一（烷烃骨架/等效氢与卤代/烯炔/苯环定位/醇醚羧酸酯），每题带解析；通关判定 ≥80%，章节进度 localStorage；右栏常用结论速记（丁基 4 种、苯二取代 3 种等）。生成脚本：工作区 `build_isomer_lab.py`
- 2026-09-01 有机反应机理库完成（chem_lab3.1.html，门户 Ⅲ-01 点亮，Ⅲ 区三个模块全部完成）：6 大机理（酯化 ¹⁸O 示踪、乙烯加成、乙醇消去、甲烷自由基取代、银镜反应、卤代烃水解/消去双路径），每机理 3 相动画：SVG 键线定位、断键红闪、成键绿闪、弯箭头电子推动（dash 流动动画）、分相解说；播放/上一相/下一相控制。生成脚本：工作区 `build_mech_lab.py`
- 2026-09-01 知识球 · 知识地图完成（chem_lab2.1.html，门户 Ⅱ-01 点亮）：52 个核心知识点（必修一 14 / 必修二 13 / 选必一 10 / 选必二 7 / 选必三 8）Canvas 力导向网络，五册教材分色；边带「前置→后续」箭头；点击节点出预习卡（要点+母题方向+前置/后续链）；节点拖拽、滚轮缩放、空白平移；教材筛选开关 + 关键词搜索高亮；关联节点高亮其余淡化。已实测：力导向收敛（最大速度 0.04）、点击「氧化还原反应」出卡正确、搜索「水解」命中。生成脚本：工作区 `build_knowledge_map.py`
- 2026-09-01 知识挑战树完成（chem_lab2.3.html，门户 Ⅱ-03 点亮，复习板块 3/3 全部完成）：10 条章节枝干 × 筑基/试炼/问鼎 3 层 = 30 个挑战节点（题库复用闪卡 150 卡，每章按难度切 5/5/5）；SVG 技能树（根节点扇形展开、弯曲枝干、状态三态：锁定/发光可挑战/金色已通关）；抽 3 题翻卡自评 ≥2 对点亮节点并解锁上层；XP（答对 8、通关 +25、复习减半）、等级（120 XP/级）、连胜/最高连胜、8 项成就、localStorage `chem-kt-progress-v1`；已实测完整通关流（+49 XP、解锁上层）、锁定提示、复习模式、刷新持久化。门户 desc 原写「549 知识点」已按实际改为 30 节点。生成脚本：工作区 `build_challengetree.py`
- 2026-09-01 元素纪元 RPG 完成（chem_lab5.1.html，门户 Ⅴ-01 点亮）：回合制对战——程序化出题真实判分（化合价计算 30 物、氧化剂/还原剂判断 16 反应、电子转移数、氧化还原性强弱链 4 组，5000 次 brute-force 校验 0 错且无答案泄露）；答对攻击/答错解析+反击；20 种元素精灵（HP≤45% 可捕获，概率随体力升高）；等级成长（XP 升级加攻加血）、图鉴、最佳波次，localStorage `chem-rpg-save-v1`；Canvas 场景（漂浮微粒、光晕精灵、伤害飘字、攻击闪光、受击震屏）。已实测：胜利/答错/捕获/阵亡复活/刷新持久化全链路。生成脚本：工作区 `build_rpg.py`
- 2026-09-01 元素防线：化学塔防完成（chem_lab5.2.html，门户 Ⅴ-02 点亮，游戏板块 3/3 全部完成）：12×8 网格 S 形路径 Canvas 塔防；3 种反应塔（沉淀塔 BaCl₂ / 中和塔 H⁺·OH⁻ / 氧化塔 KMnO₄）克制 10 种入侵离子 + 粗盐巨怪 boss；反应类型匹配 2.5× 伤害 + 击杀播报真实离子方程式；金币经济（建造/击杀/波次奖励）、核心血量 10 点、×2 加速、最佳波次 localStorage `chem-td-best-v1`；已 headless 模拟整局：15 波可通关（核心剩 7）、经济/克制/方程式播报/boss 泄漏扣 3 血全部正确。生成脚本：工作区 `build_td.py`
- 2026-09-01 社区板块完成（门户 Ⅵ 两个模块点亮，六大区 18 个模块全部完成）：新增 Netlify Function `forum.js`（Blobs store `chem-forum`）——论坛：发帖/回复/点赞/删帖（本人或管理员）、30 秒发帖限流、5 类标签；排行榜：report 上报（每人每游戏仅保留最高）、board Top 20。前端 React 页 `Forum.tsx`（列表+详情抽屉+发帖表单+筛选）、`Leaderboard.tsx`（三游戏 Tab 榜单），路由 /forum /leaderboard，顶部导航加入口。三个游戏模块（塔防/RPG/挑战树）已在生成器中接入成绩自动上报（读 localStorage `chem-token`，未登录静默跳过）。netlify.toml 修正：/api/forum 重定向必须放在 SPA 通配符之前（顺序敏感）。已直连 Blobs 实测：发帖/回复/点赞/上报保高/榜单/未登录拒绝/非法游戏拒绝/删帖全链路通过（测试数据已清理）；vite preview 截图确认两页渲染。注意：BLOBS_TOKEN 只配在生产 scope，netlify dev 本地上下文没有该变量，本地验证需直连函数方式
- 2026-09-02 优化方案落地 ① Three.js 本地化：three@0.160.0 下载至 public/vendor/three.min.js，build_vsepr_lab.py / build_crystal_lab.py 改用相对路径 ../vendor/，1.1/1.2 脱离 CDN 离线可用（已截图验证）；.gitattributes 防止 vendor js 换行转换 ③ 成绩上报离线队列：三个游戏生成器 reportScore 失败（无网/404/非 ok）自动存 localStorage `chem-score-queue`（上限 50 条），下次打开页面 flushScoreQueue 补传；已实测失败入队 ④ 排行榜「我的排名」：forum.js board 动作可选 token 附带 me{rank,score,total}，Leaderboard.tsx 顶部显示我的排名卡片；已直连 Blobs 验证（匿名 null / 登录 rank 1）
- 2026-09-02 优化方案落地（续）：② 路由级代码分割（App.tsx 改 React.lazy，主包 707KB→368KB，gzip 122KB）；⑤ 论坛搜索/分页/置顶——list 支持 q 关键词+offset 分页（每页 20）+hasMore，pin 动作仅管理员，前端搜索框/加载更多/置顶徽标/详情页置顶按钮；修复置顶排序 bug（undefined 参与布尔减法产生 NaN 导致排序失效，已直连 Blobs 复测通过，测试帖已清理）。注意：Kimi 客户端更新后其内置 npm 损坏（缺 semver），构建改用 node 直跑 `node_modules/typescript/bin/tsc -b` + `node_modules/vite/bin/vite.js build`
- 2026-09-03 迁移 Cloudflare Pages 完成（共 3 步）：① 新增 `public/_redirects`（SPA 回退 `/*  /index.html  200`）、`wrangler.toml`（项目 huaxue-shenghuo，KV 占位后填真实 ID：CHEM_AUTH=f2cf5fbd…、CHEM_FORUM=21f123c9…）、`functions/api/` 三个 Pages Function（auth.js 账号系统、forum.js 论坛+排行榜含 W-12 防刷榜：成绩上限 td≤20/rpg≤100/tree≤30 + 每分钟限报 10 次、pubchem/[[path]].js 代理）；旧 netlify.toml + netlify/functions 保留作回滚。② `migration/dump-netlify-blobs.mjs` 从 Netlify Blobs 导出（跳过 session），得 kv-auth.json 3 条（user×2、invite×1）、kv-forum.json 1 条（score×1）；两个 json 已入 .gitignore 绝不提交；注意 SITE_ID 以 1d2f8a48-9b2d-4bde-b348-dd19939d2136 为准（任务文档里的 5e274e59 是错的，会 401）。③ wrangler 4.128 登录后 `kv bulk put` 在本机崩溃（workerd access violation，疑缺 VC++ Redist），改用 OAuth token 直连 Cloudflare REST API `PUT /accounts/{acc}/storage/kv/namespaces/{id}/bulk` 导入成功：auth 3/3、forum 1/1。六项验收全过：inviteStatus 正常（旧邀请码 888888 已过期故 open:false，记录完整）；老账号登录 ok 且哈希兼容（token 正常签发）；排行榜 td total=1（站长 12 分）；PubChem water→CID 962；/teaching 回退 200；非白名单路径 400 拦截。期间修复 pubchem 通配符 bug：`params.path` 在 Pages 是数组需 join('/')（commit 0c2be35）。另：修复了 Kimi 客户端内置 npm（9-02 更新丢光 node_modules，已从官方 npm@11.12.1  tarball 补齐 117 个依赖，npm 恢复正常）。新站 https://huaxue-shenghuo.pages.dev 已上线可用；Netlify 旧站（额度耗尽停在 8-31 版）保留作回滚备份
- 2026-09-05 C-01 首页改版上线（commit bffd466）：交付包 c01-deliver 按手册执行——src/ 全量复制（fx 组件 6 个、home-fx.css、HomeRedesign.tsx、12 张 webp ≤200KB 全部达标）、旧 App.tsx 改名 App.tsx.bak 留作回滚；按手册「已知衔接项」顺带修复双导航（App.tsx 给 SiteHeader 加 pathname!=='/' 条件渲染）；npm run build 一次通过（npm 已于 09-03 修复），主包 262KB。线上验证：主包含新首页全部关键字（化学视界/晶格圣殿/和紙等）、12 张 webp 全部 200 可达。注意：Windows 与 Cloudflare Linux 构建的哈希不同（换行符差异），比对版本勿用文件名哈希。交互项（拖拽/主题切换/3D 偏转）待主人肉眼验收；仓库根目录 art-待转换/（原始大图）未提交
- 2026-09-06 C-01 v3 修复批上线（commit dd6db7d）：交付包 v3 按手册执行——①logo 化字重裁放大 ②横滑条手机修复（touch-action:pan-y + 原生惯性滚动）③和纸主题虚白修复（光晕 8%/4%、纸颗粒 .28、探照灯 .3，暗色不变）④世界卡改跳游戏（元素纪元→chem_lab5.1 / 元素防线→chem_lab5.2 / 人格星岛→chem_lab5.3，其余三张暂指 /teaching）⑤教学页删 tk-chem 字样。两个包外修正：交付包 App.tsx 丢了双导航条件渲染修复，已重新打上；Teaching.tsx 页脚残留一处 tk-chem 可见文案，已删。构建一次通过（主包 280KB）。线上验收（源码+线上产物双层核对）：游戏链接/和纸参数/pan-y/tk-chem=0 全部确认；logo 已看图（居中饱满，右下有装饰墨点）；手机滑动丝滑度需真机肉眼验收
- 2026-09-07 v4 导航整合上线（commit e848f1b）：交付包 c05-nav 按手册执行——3 个页面文件覆盖（首页顶栏「功能门户」改「排行榜」→/leaderboard、论坛→/forum；生活探究馆学习模块加第三张卡「厨房化学」→/kitchen；教学页删 Ⅴ游戏板块+Ⅵ社区与排行 只留四区）+ App.tsx 手改 3 行（删 SiteHeader import/渲染/useLocation，grep=0）。Teaching.tsx 复制后 git diff 核对：仅 -46 行（两个分区），本地页脚改动未被覆盖（包内页脚残留「目录式设计」半句已顺手清掉）。构建 32 秒通过。线上验收 6 项全过：排行/论坛链接、厨房化学卡、教学四区、旧导航三件套（首页/检索库/实时查询）全站 0 残留、三游戏入口在趣味探索。注意：SiteHeader 删除后全站无登录入口（/login 只能手输网址），已记入反馈清单待主人定夺；App.tsx.bak 回滚备份仍在
- 2026-09-07 v5 修复批上线（commit a6ff73b）：交付包 c06-fix 按手册执行——新增 NavChrome.tsx（路由变化 scrollTo 回顶 + 右下角悬浮 ⌂ 返回首页，除首页外全站出现）；Database.tsx 搜索栏吸顶 top-14→top-0（修复旧导航删除后 56px 空隙）；TiltCard 新增 reload 属性，三张游戏卡改整页直跳（reloadDocument，绕过前端路由 404）。App.tsx 覆盖前 diff 确认仅 +2 行（NavChrome import+挂载），v4 改动完好。构建 7 秒通过。线上验收 5 项全过：scrollTo/reloadDocument/⌂ 均在线；游戏页 308→去 .html 后缀 200 正常打开（Cloudflare 规范跳转，浏览器无感）；检索库 top-0/sticky 在线、top-14 零残留
- 2026-09-07 深夜四项调整上线（commit ba53a11，主人截图反馈）：① 返回首页全站补齐——React 页面悬浮 ⌂ 经 evaluate 实测在线（/database 存在 fixed 定位返回首页链接，主人截图疑为 v5 部署完成前所拍）；16 个静态实验页按钮改造：13 个实验室页保留「返回门户」+ 新增「返回首页」，3 个游戏页（5.1/5.2/5.3）删「返回门户」只留「返回首页」。重要：本次同步修改了 16 个生成脚本（工作区 build_*.py），以后重新生成不会丢按钮 ② /teaching 分区重排：Ⅰ结构 Ⅱ有机 Ⅲ原理 Ⅳ复习（复习移至末位，线上分包已验证新顺序）③ 反馈清单误报更正：首页顶栏「我的」→/profile 即登录入口，登录功能正常
- 2026-09-08 三个新游戏上线（commit 7f3175b）：交付包 c09-games3 按手册执行——chem_lab7.1 链式星蛇（贪吃蛇+链式裂变）、chem_lab7.2 元素熔炉（合成玩法/118元素）、chem_lab7.3 轨道之门（构造原理跑酷/59门）；首页趣味探索前三张卡点亮（晶脉回响→链式星蛇、有机迷林→元素熔炉、熔炉法则→轨道之门），HomeRedesign diff 确认仅 3 行卡片改动。包外补丁：三个新游戏页原本没有返回按钮，已按主人「每个跳转页都要返回首页」规则统一注入右下角悬浮 ⌂（与主站 NavChrome 同款，游戏页只放返回首页）。线上验收：三页全部 200 可达且含按钮；首页六卡文案全在线；存档键各自独立（starfallBest / fusionBest·fusionMin·fusionPp / aufbauBestGi·aufbauPlays，且与旧三游戏键不冲突）；核心机制词抽查通过（裂变/硼棒/重水、合成/质子/周期表、光子/洪特/电子排布）。备忘：排行榜上报未接（W-06 总批时统一做）；另实测 React 页面悬浮 ⌂ 在线上真实可见（fixed 定位/44px/z60），主人截图缺失系浏览器缓存旧包，已嘱 Ctrl+F5
- 2026-09-08 c11 总批 + 面包屑上线（commit 3151b61）：① 11 文件覆盖：forum.js 新增 snake/merge/aufbau 三分榜（上限 999999/9999999/59）+ usageBoard 使用时长榜（仅统计公开用户）；auth.js 新增 bindPhone/resetPassword；Login 加「忘记密码」页签、Profile 加「账号安全」区、Leaderboard 加时长榜 Tab、NavChrome 加 W-06 使用时长心跳（20s/次，页面可见时）。修复包内 Profile.tsx 漏导入 refresh（第 92 行用到）。② 包内三个游戏更新版覆盖了之前注入的返回按钮，已重新注入 ⌂（线上确认 7.1/7.2/7.3 均在）。③ 面包屑导航（主人参考 tk-chem 提出，要求不动布局）：NavChrome 新增左上角面包屑胶囊「首页 › 生活探究馆 › 厨房化学」式层级，滚动 >240px 才出现以免遮挡页首标题，纯悬浮零布局改动；本地 vite preview 实测渲染文本正确（截图受面板限制未拍）。④ 线上验收：snake/merge/aufbau 三榜接口在线（空榜待命）、usageBoard 在线、忘记密码/账号安全/时长榜各分包在线、未登录上报被拒。注意：主人已自改密码，需登录的实测流程（玩一局上榜/绑手机/找回密码）待主人自行点击验收；WORK-EXTRA 的 16 页注入昨天已做（且同步改了生成脚本），本包不再重复
- 2026-09-09 zao-chem.com 正式上线（宝塔/阿里云轻量 139.224.71.129）：B+ 变体构建——临时改 HomeRedesign 顶栏（隐藏 排行榜/论坛/我的，加朱砂胶囊「互动社区 ↗」外链 pages.dev）+ App.tsx 页脚换拾焰集社区卡片（视频号/公众号引导 + © 2026 石早晨 + 湘ICP备2026039674号-1 链 beian.miit.gov.cn）+ 19 个静态实验页同款页脚注入；构建打 zip 后 git checkout 还原主线（部署变体不入库）。宝塔上传解压至 /www/wwwroot/zao-chem.com/；伪静态 `location / { try_files $uri /index.html; }`（不可写 $uri/，否则 /teaching 类路由 403）；Let's Encrypt 双域名证书（面板 bug：逐勾两域只签主域，勾「全选」一次签成，有效期至 2026-12-08 自动续签）+ 强制HTTPS。验收 7 项全过：http 双域 301→https、https 双域 200、SPA 路由 200、静态实验页 200、页脚备案号/拾焰集在线、互动社区按钮外链正确。详细记录见 D:\我的AI\化学网站-2026-08-31\zao-chem上线部署记录.md（凭据不入库）。待办：主人 9/30 前办公安联网备案
- 2026-09-09 说明书入库：《AI使用须知.md》第 7 版（新增第七节「交付包工作法」+ 第八节「部署案例 zao-chem」）同步至 docs/AI使用须知.md，与 D:\我的AI\ 下 md/xlsx 三方一致
- 2026-09-14 仓库修路（交付包 chem-life修路-2026-09-14 按需求文档执行）：① patched/ 两个实验室页覆盖 public/teaching/（chem_lab1.1/1.2 删除被国内屏蔽的 Google Fonts 外链，全目录 grep 零残留）② 删除 3 个误导文件：根目录 AminoAcids.tsx（旧导航栏残骸）、根目录 App.tsx（氨基酸数据副本）、src/App.tsx.bak；删前核对 src/data/aminoAcids.ts 为 20 种氨基酸正式版（name/formula/structure 字段完整）③ 概况部署信息改为 Cloudflare Pages + zao-chem.com 双站；删除 netlify/ 目录与 netlify.toml（平台废弃）；待办区两条 Netlify 遗留项替换为迁移完成记录 ④ 实验室生成脚本抢救入库 scripts/labs/（16 个 build_*.py + rebuild_labs.py，来自本机工作区，从未入库）+ scripts/README.md 写清管线（脚本自足含数据、硬编码绝对路径需改、7.1-7.3 无脚本手工维护）⑤ 线上版本存档标签 zao-bplus-20260909 → e43efcc（B+ 变体构建基点）已推送。两次构建（删文件后/最终）均通过
- 2026-09-14 论坛上线核查（交付包 forum-launch-task 按手册执行）：论坛/登录/排行榜后端实早已在 Cloudflare Pages 生产环境运行（9-03 迁移），本次复测全过——inviteStatus ok、帖子列表正常返回（站长「收集贴」在线）、塔防榜 total=1；Pages 项目 huaxue-shenghuo 已连 GitHub、KV 双绑定（CHEM_AUTH/CHEM_FORUM）Production 生效（功能正常即证明）。SEO 修复：index.html lang=en→zh-CN、补 meta description。安全检查：⚠️ 仓库实为**公开**（匿名访问 200，此前 PROGRESS 误记为已转私有），需主人手动转私有（GitHub 设置页需本人登录态，AI 无凭据可操作）；git 历史 60 commit 扫描无私钥/真 Token 残留（仅 PROGRESS 旧日志里的占位符和已废弃平台的测试号密码，已隐去）。⚠️ 任务书验证项「zao-chem.com/forum 可发帖」与现行架构矛盾：zao-chem.com 是宝塔纯静态站（无后端），论坛按 9-09 既定 B+ 方案在 huaxue-shenghuo.pages.dev/forum 运行，待主人定夺是否在宝塔加 /api 反代

- 2026-09-14 论坛在 zao-chem.com 上线（主人拍板：主站必须直接收集用户数据，GitHub 仓库**保持公开**不再转私有——主人还要在 chat 用资料库）：① 宝塔站点 vhost 配置文件（REWRITE-END 后）加 /api/ 反代到 huaxue-shenghuo.pages.dev；**坑**：服务器无 IPv6 路由，直连 pages.dev 报 Network is unreachable→502，必须 `resolver 223.5.5.5 223.6.6.6 valid=300s ipv6=off;` 强制 IPv4；面板伪静态框写入不生效（面板怪癖），改 vhost 配置文件才管用 ② B+ v3 变体构建部署：临时改动仅 App.tsx 页脚（拾焰集社区卡片+备案号）+19 个静态实验页注入页脚，**导航不动**——排行榜/论坛/我的入口全部保留（推翻 9-09 的隐藏方案），构建后 git checkout 还原主线，zip 上传宝塔解压、安装包已删 ③ 线上验收全过：新构建哈希 index-RAg_vTnx.js 在线、/forum /leaderboard 200、POST /api/forum list 返回站长收集贴、board td total=1、静态实验页含拾焰集页脚、主包含备案号 ④ 数据同源：zao-chem.com 与 pages.dev 共用同一 Cloudflare KV，账号/帖子/成绩两边实时同步。待主人实测：用自己账号在 zao-chem.com 登录发帖；删帖/禁言管理功能需求已记反馈清单攒批

- 2026-09-14 互动功能增强批上线（commit 10be4a2，主人反馈 4+1 项）：① 昵称头像实时同步——forum.js 新增 resolveAuthors，list/get/board 读取时用 CHEM_AUTH 最新昵称头像覆盖展示，「古早名字」根治（帖子/榜单存储不动）② 一键禁言——user 记录加 banned 标记，ban 动作仅管理员（不可禁言管理员）；被禁言者 post/reply/like/report 全部 403，历史内容保留；管理入口在个人名片弹窗底部 ③ 个人名片——公开动作 userCard 返回头像/昵称/备注/标签，本人开了公开开关则附带使用时长（分模块）和游戏战绩（各游戏分数+排名，即「排名积分」钩子）；前端新增 UserCard.tsx 弹窗组件，论坛列表/详情/回复、排行榜两表昵称均可点击 ④ 资料保存确认弹窗——保存资料先弹「确认保存更改？」，保存→提示保存成功，放弃→表单还原原设置 ⑤ 头像图片上传——前端 canvas 居中裁方压缩至 128px webp/jpeg dataURL（<140KB），auth.js updateProfile 放行 data:image/...;base64（≤150KB）；新增 UserAvatar.tsx 组件兼容 emoji/图片双模式，论坛/排行榜/个人中心全接入 ⑥ 顺手修复：usageBoard 此前误读 CHEM_FORUM 的 usage:（心跳实际写 CHEM_AUTH）导致时长榜恒空；B+ v4 已部署 zao-chem.com（哈希 index-BNtYILow），线上六项验收全过

- 2026-09-14 体验反馈批 + VSEPR 换代上线（commit 7c23660）：① 禁言名单管理——forum.js 新增 banList（仅管理员），个人中心管理员区新增「禁言名单」卡片集中解禁 ② 全操作轻提示——Profile 页所有操作（绑定手机/改密/邀请窗口/解禁等）改为顶部居中胶囊 toast，成功 1.2s 自动消失、失败 2.6s；主按钮加 active:scale-95 按压感 ③ 新账号默认公开——register 的 showUsage/showGameTime 默认 true（本人可关；心跳与成绩照常存储，重新公开即同步榜单）④ VSEPR 模块换代——chem_lab1.1.html 替换为新版「VSEPR 轨道成键演化台」（单文件 726KB，three.js r160 内联离线可用，33 分子+成键演化滑杆+三主题），导航占位 href 接真实路由（首页/数据库/生活馆/教学实验）+ 注入悬浮 ⌂ 返回首页；说明书自检脚本（轨道对准）线上跑过 ✅。**注意：scripts/labs/build_vsepr_lab.py 已作废，不要再运行它覆盖新页** ⑤ 页脚署名按主人要求改「© 2026 早晨」（仅 B+ 变体与部署记录存档代码块，主线不动）⑥ B+ v5 已部署 zao-chem.com（哈希 index-D4f5BtTr）：新构建/新 VSEPR 页/返回键/页脚改名/名片接口六项验收全过。部署记录新增「宝塔 API 直传通道」（vite_public_request_token + /files?action=upload/UnZip/DeleteFile），绕开新版面板 UI 不吃 CDP 文件注入的坑


---

## 2026-09-14（晚）· 体验修复批 + chem_lab1.3 换代（commit d33009a）

主人批次需求（9-14 12:01）执行结果：

1. **拾焰集社区卡片只留首页**：App.tsx 页脚卡片改为 `pathname === '/'` 条件渲染，模块页不再出现。主线直接改，B+ 构建从此不再需要临时改 App.tsx。
2. **VSEPR 手机端适配**：chem_lab1.1.html 注入 @media(max-width:768px)，控制面板改底部抽屉式（bottom:8/left:8/right:8/max-height:34vh），字号压缩，电脑端不变。未真机实测。
3. **论坛/排行榜隐私打码**：forum.js 新增 maskName——昵称==账号且为 ≥6 位纯数字时显示「前3****后4」；resolveAuthors/buildUserCard/usageBoard 全接入。管理员带 token 请求 userCard 时额外返回 realUsername（禁言按钮用真实账号，且管理员自己名片不显示禁言钮）。
4. **舍弃资料归档**：build_vsepr_lab.py / build_electron_lab.py 移出仓库，归档到本机 `D:\我的AI\化学网站-2026-08-31\过渡文件已舍弃\`（含旧版 chem_lab1.1/1.3 HTML）；scripts/README.md 已注明 1.1/1.3 改为单文件直维护。
5. **点赞/发言延迟**：不是网络问题，原实现等服务器确认才刷新。Forum.tsx 改乐观更新（先改本地再请求，失败回滚），发帖/回复按钮加「发布中…」态和按压反馈。
6. **右下角「反馈」留言**：FeedbackWidget 组件（悬浮钮 right:20 bottom:76，叠在 ⌂ 上方），免登录可留言（IP 限频 5 条/小时），自动附带所在页面路径；管理端在个人中心「留言箱」查看/删除。接口：forum.js 的 feedback / feedbackList / feedbackDel。
7. **chem_lab1.3 换代**：按《上线说明书-chem_lab1.3_r128.md》整页覆盖为 r128 单文件版；three@0.128 入库 public/vendor/three.r128.min.js；顶栏注入返回门户/返回首页。线上实测：GL 自检徽章通过、Fe=[Ar]3d⁶4s²、练习模式（写排布式/认排布式/挑战区）在。

### 部署事故记录（重要教训）

宝塔 API 部署 v6 时，DeleteFile 接口误用（把目录当 path + data 列表）导致 **/www/wwwroot/zao-chem.com 整个目录被删进回收站**，全站 500 约 4 分钟。从回收站恢复（Re_Recycle_bin）后内容完好（解压先于删除，恢复即是 v6 完整内容）。

**规则**：宝塔 `DeleteFile` 的 `path` 参数 = 要删的文件完整路径本身，不要带 data 列表。删除前先在回收站确认目标。

### B+ v6 构建规则变化

- 主线 App.tsx 页脚已含「© 2026 早晨 ｜ 备案号链接」全站渲染；社区卡片仅首页。
- B+ 只需给 19 个静态实验页注入**角落备案小字**（position:fixed left:8 bottom:4, opacity:.55），不再注入大卡片页脚、不再临时改 App.tsx。
- 注入脚本模式：`</body>` 前替换，注入前断言无 beian 残留，构建打包后 `git checkout -- public/teaching/` 还原。

### 待办 / 待主人实测

- 留言箱里有两条「上线验收测试留言，可删除」（pages.dev 与 zao 各一条），可在个人中心删掉
- 名片打码效果、留言箱 UI、手机端 VSEPR 面板需主人实测
- chem_lab1.2 晶体实验室等大改需求仍在排队（等 chat 侧交付包）


---

## 2026-09-14（深夜）· 晶体实验室换代 + 体验修复批（commit 见 git log）

主人批次需求（9-14 12:58）执行结果：

1. **手机端误触保护**：19 个静态实验页 + React 全局 index.css 注入 `html,body{overscroll-behavior:none;}`，禁止边缘滑动触发浏览器前进/后退。重新生成实验页时必须保留该行（scripts/README.md 已注明）。
2. **晶体结构深度实验室换代**：chem_lab1.2.html 整页替换为 r128 版（42 种晶体 6 大类：ion 15 / metal 12 / covalent 6 / molecule 3 / mix 2 / alloy 4）；新增：本地 vendor（../vendor/three.r128.min.js）作为 three.js 第一回退源、顶栏「⌂ 返回首页」、误触保护。旧版与 build_crystal_lab.py 已归档「过渡文件已舍弃」。线上实测：__cx 体检钩子在、后处理链加载成功、42 晶体齐全、三主题切换正常（自检日志按说明书为启动全绿才就绪）。
3. **离子晶体晶胞专题模块删除**：Teaching.tsx 入口卡片已删（其内容与晶体实验室重复），结构专题重编号 01-03，晶体实验室描述更新为 42 种。
4. **反馈按钮改小球**：40px 圆形图标、半透明白底低调配色、移至 right:14 bottom:70（⌂ 上方）；**手机端（≤768px）只在「我的」/profile 页显示**，其余页面隐藏。

### 部署

- pages.dev：push main 自动部署（本批 hash index-DBybhEHz）
- zao-chem.com：B+ v7（19 静态页注入角落备案小字后构建，zao-chem-dist-v7.zip，60 文件 2241KB，hash index-BbgO5Ha-）宝塔 API 部署；DeleteFile 已按修正后的单文件路径用法，无误删
- 验收：zao 首页 200 新 hash；/teaching 无「离子晶体晶胞专题」、晶体描述已更新、无社区卡片；chem_lab1.2 双站均含 r128/vendor/误触保护；反馈球在手机宽度（602px 实测）下 /teaching 与 /login 隐藏，符合规则

### 备注

- 主人管理员账号密码已非初始密码（登录返回"密码错误"），说明改密流程生效；后续自动化验收需要登录态时请先问主人要当前密码
