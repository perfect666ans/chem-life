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

## 最近完成

- 2026-08-31 修复同步：首页浅色化 + 氨基酸增肌模块 + 维生素速查（commit efd2173）
- 2026-08-31 双设备基础设施：删除项目内重复的 .ssh 私钥副本（真钥在 `~/.ssh/`）、`.gitignore` 加入 `.ssh/`、仓库转为私有

## 下一步（待办）

- [ ] （暂无，由会话更新）

## 双设备工作流约定

1. 开始工作：`git pull`
2. 结束工作：更新本文件 → `git add -A && git commit && git push`
3. 不要把私钥、`.env` 等敏感文件放进仓库
4. 换设备首次：`npm install`；Netlify CLI 与 GitHub 凭据需各自登录一次

## 环境备注

- 设备 A（风逝台式机）：GitHub 直连偶发超时（2026-08-31 git fetch 失败、curl 正常），如遇 push/pull 失败先重试或检查代理
