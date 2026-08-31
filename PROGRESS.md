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

## 下一步（待办）

- [ ] 门户页 `/teaching` 排版细化（目前是第一版粗排）
- [ ] 教学模块其余板块（复习、有机、反应原理、游戏）陆续接入
- [ ] 实验室页面窄屏适配（当前为桌面三栏布局，窄屏下信息卡过挤）

## 双设备工作流约定

1. 开始工作：`git pull`
2. 结束工作：更新本文件 → `git add -A && git commit && git push`
3. 不要把私钥、`.env` 等敏感文件放进仓库
4. 换设备首次：`npm install`；Netlify CLI 与 GitHub 凭据需各自登录一次

## 环境备注

- 设备 A（风逝台式机）：GitHub 直连偶发超时，push 失败多重试几次即可；npm/node 不在 PATH，构建用 `%APPDATA%\kimi-desktop\daimon-share\daimon\command-process-owner\bin\npm.cmd`
- **不要 `taskkill /F /IM node.exe`**——会误杀 Kimi 自身运行时导致断连；停 dev server 用 `netstat -ano | grep :端口` 找 PID 再按 PID 杀
- 教学实验室依赖 Three.js CDN（jsdelivr / unpkg），离线环境会加载失败
- 本地 vite dev 没有 Netlify 函数，`/api/pubchem/*` 在本地 404（氨基酸键线式图有直连回退）；线上正常
