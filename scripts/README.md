# scripts/ · 实验室生成脚本

> 入库日期：2026-09-14（抢救自本机工作区，此前从未入库）
> 用途：`public/teaching/` 下的 3D 实验室 / 复习 / 游戏静态页，大多不是手写的，而是用这里的 Python 脚本「数据 + 外壳模板 → 组装成完整 HTML」生成的。

## 管线（真实流程，逆向自脚本代码）

每个 `build_*.py` 都是**独立自足**的：数据（分子/晶体/题目等）直接写在脚本内部的常量里，跑脚本 = 全量重新生成对应 HTML 并**覆盖** `public/teaching/` 下的产物。

```
改脚本里的数据/逻辑 → python scripts/labs/build_xxx.py → 覆盖 public/teaching/chem_labX.Y.html → npm run build / 部署
```

⚠️ **脚本内的输入/输出路径是硬编码的绝对路径**（指向本机 `C:\Users\风逝\...\chem-life-main\public\teaching\`）。换设备或移动仓库后，先把脚本顶部的 `OUT` / `LAB12` / `PROJ` 等路径常量改成当前机器的实际路径再运行。

## 脚本 ↔ 产物对照

| 脚本 | 产物 | 页面 |
|---|---|---|
| ~~build_vsepr_lab.py~~ | chem_lab1.1.html | VSEPR 分子构型实验室（2026-09-14 起改为单文件直维护，脚本已归档舍弃） |
| ~~build_crystal_lab.py~~ | chem_lab1.2.html | 晶体结构深度实验室（2026-09-14 起换代为 r128 单文件版·42 种晶体，脚本已归档舍弃） |
| ~~build_electron_lab.py~~ | chem_lab1.3.html | 核外电子排布实验室（2026-09-14 起换代为 r128 单文件版，脚本已归档舍弃） |
| build_knowledge_map.py | chem_lab2.1.html | 知识球 · 知识地图 |
| build_flashcards.py | chem_lab2.2.html | 化学闪卡复习 |
| build_challengetree.py | chem_lab2.3.html | 知识挑战树 |
| ~~build_mech_lab.py~~ | chem_lab3.1.html | 有机反应机理库（2026-09-14 起换代为 r128 单文件版·18 反应，脚本已归档舍弃） |
| build_naming_lab.py | chem_lab3.2.html | 有机系统命名中心 |
| build_isomer_lab.py | chem_lab3.3.html | 同分异构体闯关 |
| build_thermo_lab.py | chem_lab4.1.html | 化学反应的热效应 |
| build_kinetics_lab.py | chem_lab4.2.html | 化学反应速率与平衡 |
| build_solution_lab.py | chem_lab4.3.html | 水溶液中的离子平衡 |
| build_electro_lab.py | chem_lab4.4.html | 电化学实验室 |
| build_rpg.py | chem_lab5.1.html | 元素纪元 RPG |
| build_td.py | chem_lab5.2.html | 元素防线：化学塔防 |
| build_cbti.py | chem_lab5.3.html | CBTI 化学人格鉴定 |

## rebuild_labs.py（外壳换装）

不同用途：它**不生成数据**，而是把已定稿实验室页的内联 `<script>`（Three.js 逻辑）原样抽出，套上 tk-chem 设计系统的新外壳（`<style>` + HTML 结构，washi/sumi/ai 三主题），JS 依赖的 id/class 钩子逐一保留。改全站实验室"皮肤"时用它。

## 没有生成脚本的页面

- `chem_lab1.1.html`（VSEPR）、`chem_lab1.2.html`（晶体结构）、`chem_lab1.3.html`（核外电子排布）、`chem_lab3.1.html`（有机反应机理库）：2026-09-14 起改为**单文件直接维护**（交付包整页覆盖），原 build_vsepr_lab.py / build_crystal_lab.py / build_electron_lab.py / build_mech_lab.py 已归档到本机「过渡文件已舍弃」文件夹并从仓库删除
- 全部 19 个静态实验页已注入误触保护样式 `html,body{overscroll-behavior:none;}`（2026-09-14，手机端边缘滑动防浏览器后退）；重新生成页面时需保留这一行
- `chem_lab7.1 / 7.2 / 7.3`（链式星蛇 / 元素熔炉 / 轨道之门，2026-09-08 交付包新增）：**无生成脚本**，由交付包直接维护 HTML，改它们就手工改文件

## 依赖

脚本用 `numpy`（几何向量计算）和标准库；本机 Kimi Work 托管 Python 可直接运行。
