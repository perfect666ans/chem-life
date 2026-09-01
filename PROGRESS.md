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
