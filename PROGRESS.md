# PROGRESS · 项目进展笔记

> 用途：双设备切换时恢复上下文。每次结束工作前更新本文件并 commit + push；
> 换设备后先 `git pull`，再让 Kimi 读这个文件即可无缝继续。

## 项目概况

- 名称：chem-life（化学生活网站）
- 技术栈：React 19 + TypeScript + Vite + Tailwind CSS + shadcn/ui
- 线上地址：https://huaxue-shenghuo.netlify.app/
- 仓库：https://github.com/perfect666ans/chem-life （**私有**，2026-08-31 由公开转为私密）
- 部署：Netlify，`npm run build` → `dist/`；`/api/pubchem/*` 由 Netlify Function 中转代理

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
- 2026-09-01 登录系统**后端全链路实测通过**（BLOBS_TOKEN 方案落地）：Netlify CLI 已登录本机（`netlify login` 授权完成，token 在 `%APPDATA%\netlify\Config\config.json`）；`netlify env:set BLOBS_TOKEN=<CLI token> --context production` 已设置；本地直接调用打包函数实测 10 步全过（inviteStatus/管理员登录/setInvite/注册/改资料/改密/新密码重登/me/closeInvite）。**注意**：实测向生产 Blobs 写入了管理员账号和一个测试号 testuser01（密码 mynewpass123，可忽略）
- 2026-09-01 核外电子排布实验室完成（chem_lab1.3.html，门户 Ⅰ-04 已点亮）：118 元素周期表点选；玻尔壳层动画（Canvas 2D）；轨道方框图（泡利+洪特，Fe 3d⁶/4s² 实测正确）；排布式三形态（完整/简化[Ar] 式/价电子层）；构造原理填充链高亮（最后填入能级实心）；Cr/Cu/Pd 等 21 个排布例外内置；常见离子切换（Fe²⁺/Fe³⁺ 先失 4s 实测正确、Cl⁻ 得电子正确）；同周期/同族半径对比条。生成脚本：工作区 `build_electron_lab.py`（外壳同样提取自 chem_lab1.2.html）。已本地浏览器截图验证

## 下一步（待办）

- [ ] 复习板块（知识球/闪卡/挑战树）、有机三大模块、反应原理四大模块、游戏板块：目前均为门户占位
- [ ] 交流论坛、排行榜/统计（依赖登录系统统计接口，当前仅有 showUsage/showGameTime 开关字段）
- [ ] 登录系统线上激活（**额度恢复后自动完成，无需手动操作**）：BLOBS_TOKEN 已配置好且实测有效，但 2026-09-01 账户免费构建额度耗尽（"Account credit usage exceeded"），生产部署被阻断；额度按账单月重置，恢复后任意 push 或 `netlify api createSiteBuild` 触发一次部署即全线生效。届时用 curl 测 `POST /api/auth {action:'inviteStatus'}`
- [ ] 部署积压：commit 610700b（移除 debugEnv 调试代码）本地已提交，因 GitHub 直连超时+额度阻断**尚未上线**；恢复后 push 即可
- [ ] 论坛/排行需要新增 Blobs 表（帖子、积分）

## 双设备工作流约定

1. 开始工作：`git pull`
2. 结束工作：更新本文件 → `git add -A && git commit && git push`
3. 不要把私钥、`.env` 等敏感文件放进仓库
4. 换设备首次：`npm install`；Netlify CLI 与 GitHub 凭据需各自登录一次

## 环境备注

- 设备 A（风逝台式机）：GitHub 直连偶发超时，push 失败多重试几次即可；npm/node 不在 PATH，构建用 `%APPDATA%\kimi-desktop\daimon-share\daimon\command-process-owner\bin\npm.cmd`
- **不要 `taskkill /F /IM node.exe`**——会误杀 Kimi 自身运行时导致断连；停 dev server 用 `netstat -ano | grep :端口` 找 PID 再按 PID 杀
- 教学实验室依赖 Three.js CDN（jsdelivr / unpkg），离线环境会加载失败
- 本地 vite dev 没有 Netlify 函数，`/api/pubchem/*` 与 `/api/auth` 在本地 404（氨基酸键线式图有直连回退）；线上正常
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
