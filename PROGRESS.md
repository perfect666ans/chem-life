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

## 下一步（待办）

- [ ] **按 tk-chem.cc/nav.html 的风格重做 VSEPR 与晶体结构两个实验室**（用户反馈豆包版太粗糙）
- [ ] 门户页排版细化（目前是第一版粗排）
- [ ] 教学模块其余板块（复习、有机、反应原理、游戏）陆续接入

## 双设备工作流约定

1. 开始工作：`git pull`
2. 结束工作：更新本文件 → `git add -A && git commit && git push`
3. 不要把私钥、`.env` 等敏感文件放进仓库
4. 换设备首次：`npm install`；Netlify CLI 与 GitHub 凭据需各自登录一次

## 环境备注

- 设备 A（风逝台式机）：GitHub 直连偶发超时，push 失败多重试几次即可；npm/node 不在 PATH，构建用 `%APPDATA%\kimi-desktop\daimon-share\daimon\command-process-owner\bin\npm.cmd`
- 教学实验室依赖 Three.js CDN（jsdelivr / unpkg），离线环境会加载失败
