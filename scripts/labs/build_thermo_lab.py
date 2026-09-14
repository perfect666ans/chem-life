# -*- coding: utf-8 -*-
"""
生成 化学反应的热效应实验室 chem_lab4.1.html
功能：键能法 ΔH 即时计算（预设反应 + 自定义断键/成键清单）、能量-反应进程图（Canvas）、
      盖斯定律双路径演示（拖中间态能量，总和恒定）
外壳提取自 chem_lab1.2.html
"""
import json, re

LAB12 = r"C:\Users\风逝\Documents\kimi\tasks\2026-08-31\06-27-38-247a26cf\chem-life-main\public\teaching\chem_lab1.2.html"
OUT   = r"C:\Users\风逝\Documents\kimi\tasks\2026-08-31\06-27-38-247a26cf\chem-life-main\public\teaching\chem_lab4.1.html"

old = open(LAB12, encoding="utf-8").read()
CSS = re.search(r"<style>(.*?)</style>", old, re.S).group(1)
THEME_JS = re.search(r"/\* =+ 主题切换 washi / sumi / ai =+ \*/\s*\(function\(\)\{.*?\}\)\(\);", old, re.S).group(0)

# 键能表 kJ/mol（25 ℃ 平均值，教学口径）
BONDS = {
 "H-H":436, "F-F":159, "Cl-Cl":243, "Br-Br":193, "I-I":151,
 "H-F":565, "H-Cl":431, "H-Br":366, "H-I":299, "O-H":463, "N-H":391, "C-H":413, "S-H":339,
 "O=O":498, "N≡N":946, "N=N":418, "C-C":348, "C=C":614, "C≡C":839,
 "C-O":358, "C=O(CO₂)":799, "C=O":745, "O-O":142, "C-N":293, "C=N":615, "C≡N":891, "N-N":163,
}
# 预设反应：name, 方程式, 断键 {键:数}, 成键 {键:数}, 说明
PRESETS = [
 {"name":"氢气在氯气中燃烧", "eq":"H₂ + Cl₂ = 2HCl",
  "brk":{"H-H":1,"Cl-Cl":1}, "frm":{"H-Cl":2},
  "note":"苍白色火焰，瓶口有白雾。放热反应的典型代表。"},
 {"name":"氢气与溴蒸气化合", "eq":"H₂ + Br₂ = 2HBr",
  "brk":{"H-H":1,"Br-Br":1}, "frm":{"H-Br":2},
  "note":"卤素越不活泼，与氢气化合越难、放热越少（对比 Cl₂、I₂）。"},
 {"name":"氢气与碘化合", "eq":"H₂ + I₂ ⇌ 2HI",
  "brk":{"H-H":1,"I-I":1}, "frm":{"H-I":2},
  "note":"几乎热中性：ΔH 仅约 −11 kJ/mol，且反应可逆。"},
 {"name":"氢气在氧气中燃烧", "eq":"2H₂ + O₂ = 2H₂O(g)",
  "brk":{"H-H":2,"O=O":1}, "frm":{"O-H":4},
  "note":"生成水蒸气时 −482 kJ；若生成液态水还要加上汽化潜热（更放热）。"},
 {"name":"甲烷完全燃烧", "eq":"CH₄ + 2O₂ = CO₂ + 2H₂O(g)",
  "brk":{"C-H":4,"O=O":2}, "frm":{"C=O(CO₂)":2,"O-H":4},
  "note":"天然气主要成分。注意 CO₂ 中 C=O 键能按 799 kJ/mol 计。"},
 {"name":"合成氨反应", "eq":"N₂ + 3H₂ ⇌ 2NH₃",
  "brk":{"N≡N":1,"H-H":3}, "frm":{"N-H":6},
  "note":"放热但 N≡N 键能极大（946），故需高温高压+催化剂（工业合成氨）。"},
 {"name":"过氧化氢分解", "eq":"2H₂O₂ = 2H₂O + O₂",
  "brk":{"O-O":2,"O-H":4}, "frm":{"O-H":4,"O=O":1},
  "note":"净效果 = 断 2 个 O-O 键、成 1 个 O=O 键，O-H 键打平。MnO₂ 催化。"},
 {"name":"氢气与氟气化合", "eq":"H₂ + F₂ = 2HF",
  "brk":{"H-H":1,"F-F":1}, "frm":{"H-F":2},
  "note":"H-F 是最强的氢卤键，暗处即可爆炸化合，放热巨大。"},
]

DATA = {"bonds": BONDS, "presets": PRESETS}

EXTRA_CSS = r"""
/* ===== 热效应实验室专用 ===== */
.dh-big{font-family:Georgia,serif;font-size:40px;color:var(--accent);line-height:1.1}
.dh-sub{font-size:12px;color:var(--ink-dim);margin-top:4px}
.dh-tag{display:inline-block;font-size:11px;border:1px solid var(--accent);color:var(--accent);
 border-radius:10px;padding:1px 10px;margin-top:8px}
.bond-row{display:flex;align-items:center;gap:6px;margin:5px 0}
.bond-row select{flex:1;padding:5px 8px;background:var(--surface-2);border:1px solid var(--line);
 color:var(--ink);border-radius:6px;font-size:12px;font-family:inherit}
.bond-row input[type=number]{width:52px;padding:5px 6px;background:var(--surface-2);border:1px solid var(--line);
 color:var(--ink);border-radius:6px;font-size:12px;font-family:inherit;text-align:center}
.bond-row input[type=text]{width:74px;padding:5px 6px;background:var(--surface-2);border:1px solid var(--line);
 color:var(--ink-dim);border-radius:6px;font-size:11px;font-family:inherit;text-align:center}
.bond-row .del{border:none;background:none;color:var(--ink-mute);cursor:pointer;font-size:14px}
.bond-row .del:hover{color:var(--accent)}
.bond-add{width:100%;margin-top:4px;padding:5px 0;border:1px dashed var(--line-strong);background:none;
 color:var(--ink-dim);border-radius:6px;font-size:12px;cursor:pointer;font-family:inherit}
.bond-add:hover{color:var(--accent);border-color:var(--accent)}
.hess-slider{width:100%}
.hess-val{font-family:var(--mono);font-size:12px;color:var(--accent);text-align:center}
.preset-eq{font-family:var(--serif-cn);font-size:15px;margin:6px 0}
"""

BODY_JS = r"""
/* ===== 化学反应的热效应 ===== */
const D = window.__THERMO__;
const $ = (id) => document.getElementById(id);
let brk = {}, frm = {};           // 键 -> 数目
let hessMid = -110;               // 盖斯演示中间态能量（相对反应物 0）

/* ---- ΔH 计算 ---- */
function calcDH(){
  let s1 = 0, s2 = 0;
  for (const k in brk) s1 += D.bonds[k] * brk[k];
  for (const k in frm) s2 += D.bonds[k] * frm[k];
  return {s1, s2, dh: s1 - s2};
}
function fmtDH(x){ return (x>0?"+":"") + x.toFixed(0); }

/* ---- 键清单编辑 ---- */
function bondOptions(sel){
  return Object.keys(D.bonds).map(k =>
    `<option value="${k}" ${k===sel?"selected":""}>${k}（${D.bonds[k]} kJ/mol）</option>`).join("");
}
function renderBondEditor(wrapId, store, other){
  const w = $(wrapId); w.innerHTML = "";
  Object.keys(store).forEach(k => {
    const row = document.createElement("div"); row.className = "bond-row";
    row.innerHTML = `<select>${bondOptions(k)}</select>
      <span style="font-size:11px;color:var(--ink-mute)">×</span>
      <input type="number" min="1" max="12" value="${store[k]}">
      <input type="text" value="${D.bonds[k]} kJ" title="键能（可改）">
      <button class="del">×</button>`;
    const [sel, cnt, en] = [row.children[0], row.children[1], row.children[2]];
    sel.onchange = () => { delete store[k]; store[sel.value] = +cnt.value || 1; renderAll(); };
    cnt.onchange = () => { store[k] = Math.max(1, +cnt.value || 1); renderAll(); };
    en.onchange = () => { const v = parseFloat(en.value); if (v > 0) { D.bonds[k] = v; renderAll(); } };
    row.querySelector(".del").onclick = () => { delete store[k]; renderAll(); };
    w.appendChild(row);
  });
}
$("addBrk").onclick = () => { brk["H-H"] = brk["H-H"] || 1; renderAll(); };
$("addFrm").onclick = () => { frm["H-Cl"] = frm["H-Cl"] || 1; renderAll(); };

/* ---- 预设反应 ---- */
function renderPresets(){
  const sel = $("presetSel");
  sel.innerHTML = `<option value="-1">— 自定义反应 —</option>` +
    D.presets.map((p,i) => `<option value="${i}">${p.name}</option>`).join("");
  sel.onchange = () => {
    const i = +sel.value;
    if (i < 0){ brk = {"H-H":1}; frm = {"H-H":1}; }
    else { const p = D.presets[i]; brk = {...p.brk}; frm = {...p.frm}; }
    renderAll();
  };
}

/* ---- 能量-进程图 ---- */
function drawEnergy(){
  const c = $("eCanvas"); const box = c.parentElement.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  c.width = box.width * dpr; c.height = box.height * dpr;
  const ctx = c.getContext("2d"); ctx.setTransform(dpr,0,0,dpr,0,0);
  const W = box.width, H = box.height; ctx.clearRect(0,0,W,H);
  const ink = getComputedStyle(document.body).getPropertyValue("--ink").trim() || "#999";
  const acc = getComputedStyle(document.body).getPropertyValue("--accent").trim() || "#c8102e";
  const {s1, s2, dh} = calcDH();
  // 能量布局：反应物 0，生成物 -dh（放热在下）。能量越高越靠上。
  const Ea = Math.max(s1 * 0.35, Math.abs(dh) * 0.3, 60);   // 示意活化能垒高度
  const eR = 0, eP = -dh, eT = Ea;                          // 反应物/产物/过渡态
  const all = [eR, eP, eT];
  const eMin = Math.min(...all) - 40, eMax = Math.max(...all) + 60;
  const Y = (e) => H*0.12 + (eMax - e) / (eMax - eMin) * H*0.72;
  const X = (t) => W*0.14 + t * W*0.72;
  // 网格线
  ctx.strokeStyle = ink; ctx.globalAlpha = .12;
  for (let i = 0; i < 5; i++){ const y = H*0.12 + i*H*0.18;
    ctx.beginPath(); ctx.moveTo(W*0.08, y); ctx.lineTo(W*0.92, y); ctx.stroke(); }
  ctx.globalAlpha = 1;
  // 反应进程曲线（双驼峰简化：单驼峰）
  ctx.beginPath();
  for (let i = 0; i <= 100; i++){
    const t = i/100;
    // 三段：R 平台 → 高斯峰 → P 平台
    const hump = Math.exp(-((t-0.5)**2)/0.055);
    const eBase = eR + (eP - eR) * smooth(t);
    const eCurve = eBase + (eT - eBase) * hump;
    const x = X(t), y = Y(eCurve);
    i ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
  }
  ctx.strokeStyle = acc; ctx.lineWidth = 2.5; ctx.stroke(); ctx.lineWidth = 1;
  function smooth(t){ return t<0.08 ? 0 : t>0.92 ? 1 : (Math.cos((t-0.08)/0.84*Math.PI - Math.PI)+1)/2; }
  // 平台线
  ctx.strokeStyle = ink; ctx.globalAlpha = .5;
  ctx.beginPath(); ctx.moveTo(X(0), Y(eR)); ctx.lineTo(X(0.08), Y(eR)); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(X(0.92), Y(eP)); ctx.lineTo(X(1), Y(eP)); ctx.stroke();
  ctx.globalAlpha = 1;
  // ΔH 箭头（反应物平台右端到产物水平）
  const ax = X(0.86);
  ctx.strokeStyle = acc; ctx.fillStyle = acc;
  ctx.beginPath(); ctx.moveTo(ax, Y(eR)); ctx.lineTo(ax, Y(eP)); ctx.stroke();
  ctx.beginPath();
  const dir = eP > eR ? -1 : 1;
  ctx.moveTo(ax, Y(eP)); ctx.lineTo(ax-5, Y(eP)+8*dir); ctx.lineTo(ax+5, Y(eP)+8*dir); ctx.fill();
  ctx.font = "bold 13px Georgia"; ctx.textAlign = "left";
  ctx.fillText(`ΔH = ${fmtDH(dh)} kJ/mol`, ax + 10, (Y(eR)+Y(eP))/2);
  // 活化能标注
  ctx.fillStyle = ink; ctx.font = "11px sans-serif"; ctx.globalAlpha = .7;
  ctx.fillText(`Eₐ(正) ≈ ${(eT-eR).toFixed(0)} kJ/mol（示意）`, X(0.42), Y(eT) - 8);
  ctx.fillText("反应物", X(0.0)-2, Y(eR) - 8);
  ctx.fillText("生成物", X(0.9)-2, Y(eP) - 8);
  ctx.globalAlpha = 1;
  // 吸热/放热底色提示
  ctx.fillStyle = acc; ctx.globalAlpha = .06;
  if (dh < 0) ctx.fillRect(X(0.1), Y(eR), X(0.9)-X(0.1), Y(eP)-Y(eR));
  else ctx.fillRect(X(0.1), Y(eP), X(0.9)-X(0.1), Y(eR)-Y(eP));
  ctx.globalAlpha = 1;
}

/* ---- 盖斯定律演示 ---- */
function drawHess(){
  const c = $("hessCanvas"); const box = c.parentElement.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  c.width = box.width * dpr; c.height = box.height * dpr;
  const ctx = c.getContext("2d"); ctx.setTransform(dpr,0,0,dpr,0,0);
  const W = box.width, H = box.height; ctx.clearRect(0,0,W,H);
  const ink = getComputedStyle(document.body).getPropertyValue("--ink").trim() || "#999";
  const acc = getComputedStyle(document.body).getPropertyValue("--accent").trim() || "#c8102e";
  // 例：C + O₂ → CO₂（−394）；路径2：C→CO（hessMid）→CO₂
  const E_A = 0, E_C = -394, E_B = hessMid;
  const all = [E_A, E_B, E_C];
  const eMin = Math.min(...all) - 60, eMax = Math.max(...all) + 80;
  const Y = (e) => H*0.15 + (eMax - e)/(eMax - eMin) * H*0.7;
  const lanes = [W*0.16, W*0.5, W*0.84];
  const labels = ["C + O₂", "CO + ½O₂", "CO₂"];
  const vals = [E_A, E_B, E_C];
  // 能级横线
  lanes.forEach((x,i) => {
    ctx.strokeStyle = i===1 ? "#b8860b" : acc; ctx.lineWidth = 2.5;
    ctx.beginPath(); ctx.moveTo(x-46, Y(vals[i])); ctx.lineTo(x+46, Y(vals[i])); ctx.stroke();
    ctx.fillStyle = ink; ctx.font = "12px var(--sans-cn)"; ctx.textAlign = "center";
    ctx.fillText(labels[i], x, Y(vals[i]) - 10);
    ctx.font = "11px Georgia"; ctx.fillStyle = "#b8860b";
    ctx.fillText(vals[i] + " kJ/mol", x, Y(vals[i]) + 18);
  });
  // 箭头 A→C 直接、A→B、B→C
  const arrow = (x1,y1,x2,y2,color) => {
    ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2,y2); ctx.stroke();
    const ang = Math.atan2(y2-y1, x2-x1);
    ctx.beginPath(); ctx.moveTo(x2,y2);
    ctx.lineTo(x2-8*Math.cos(ang-0.4), y2-8*Math.sin(ang-0.4));
    ctx.lineTo(x2-8*Math.cos(ang+0.4), y2-8*Math.sin(ang+0.4)); ctx.fill();
  };
  arrow(lanes[0], Y(E_A), lanes[2], Y(E_C), acc);
  arrow(lanes[0]+6, Y(E_A)+6, lanes[1]-6, Y(E_B), "#b8860b");
  arrow(lanes[1]+6, Y(E_B), lanes[2]-6, Y(E_C)+4, "#b8860b");
  ctx.lineWidth = 1;
}

function renderAll(){
  const {s1, s2, dh} = calcDH();
  $("dhBig").textContent = fmtDH(dh) + " kJ/mol";
  $("dhSub").textContent = `断键吸热 ${s1.toFixed(0)} − 成键放热 ${s2.toFixed(0)}`;
  $("dhTag").textContent = dh < 0 ? "放热反应 ΔH<0" : dh > 0 ? "吸热反应 ΔH>0" : "近似热中性";
  const pi = +$("presetSel").value;
  $("presetEq").textContent = pi >= 0 ? D.presets[pi].eq : "自定义反应";
  $("presetNote").textContent = pi >= 0 ? D.presets[pi].note : "自由组合断键与成键清单，观察 ΔH 变化。";
  renderBondEditor("brkList", brk); renderBondEditor("frmList", frm);
  // 盖斯
  const step1 = hessMid, step2 = -394 - hessMid;
  $("hessVal").textContent = `中间态 CO+½O₂ 能量：${hessMid} kJ/mol`;
  $("hessSum").textContent = `路径① 直接：−394 kJ/mol ＝ 路径② 两段之和：(${fmtDH(step1)}) + (${fmtDH(step2)}) = ${fmtDH(step1+step2)} kJ/mol —— 与途径无关`;
  drawEnergy(); drawHess();
}

$("hessSlider").oninput = (e) => { hessMid = +e.target.value; renderAll(); };
window.addEventListener("resize", renderAll);
renderPresets();
$("presetSel").value = "4"; // 默认甲烷燃烧
$("presetSel").onchange();
"""

HTML = f"""<!DOCTYPE html>
<html lang="zh-CN" data-theme="washi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>化学反应的热效应 · 化学生活教学中心</title>
<style>{CSS}
{EXTRA_CSS}</style>
</head>
<body>
<nav class="topnav">
  <div class="brand">
    <span class="badge">热</span>
    <h1 style="white-space:nowrap">化学反应的热效应</h1>
    <span class="lecture-tag">PRINCIPLES · LAB 01</span>
  </div>
  <div class="nav-right">
    <button class="nav-btn" onclick="location.href='/teaching'"><span class="arr">←</span> 返回门户</button>
    <button class="nav-btn" onclick="location.href='/'"><span class="arr">⌂</span> 返回首页</button>
    <div class="theme-switch" role="group" aria-label="主题切换">
      <button class="ts-dot" data-set-theme="washi" aria-label="和紙"><span class="ts-swatch" style="--a:#efebe0;--b:#c8102e"></span><span class="ts-name">和紙</span></button>
      <button class="ts-dot" data-set-theme="sumi" aria-label="墨朱"><span class="ts-swatch" style="--a:#0d0d0f;--b:#d23838"></span><span class="ts-name">墨朱</span></button>
      <button class="ts-dot" data-set-theme="ai" aria-label="藍"><span class="ts-swatch" style="--a:#0a0e15;--b:#4a93d4"></span><span class="ts-name">藍</span></button>
    </div>
  </div>
</nav>

<div class="main-wrap">
  <div class="side left-panel">
    <div class="info-card">
      <h2 style="white-space:nowrap">ΔH 计算器</h2>
      <div class="preset-eq" id="presetEq"></div>
      <div class="dh-big" id="dhBig">—</div>
      <div class="dh-sub" id="dhSub"></div>
      <span class="dh-tag" id="dhTag"></span>
      <p class="info-desc" id="presetNote" style="margin-top:10px"></p>
      <p class="info-desc">ΔH = 断裂化学键吸收的总能量 − 形成化学键释放的总能量。键能为 25 ℃ 平均值，可点击数值修改。</p>
    </div>
    <div class="panel-section">
      <div class="panel-title">预设反应</div>
      <select class="select-box" id="presetSel"></select>
    </div>
  </div>

  <div class="canvas-box" style="background:var(--bg-deep)">
    <canvas id="eCanvas" style="width:100%;height:52%;display:block"></canvas>
    <canvas id="hessCanvas" style="width:100%;height:48%;display:block;border-top:1px solid var(--line)"></canvas>
  </div>

  <div class="side right-panel">
    <div class="panel-section">
      <div class="panel-title">断裂的键（吸热）</div>
      <div id="brkList"></div>
      <button class="bond-add" id="addBrk">+ 添加一种键</button>
    </div>
    <div class="panel-section">
      <div class="panel-title">形成的键（放热）</div>
      <div id="frmList"></div>
      <button class="bond-add" id="addFrm">+ 添加一种键</button>
    </div>
    <div class="panel-section">
      <div class="panel-title">盖斯定律 · 碳燃烧的两条路径</div>
      <input type="range" class="hess-slider" id="hessSlider" min="-394" max="0" step="1" value="-110">
      <div class="hess-val" id="hessVal"></div>
      <p class="info-desc" id="hessSum" style="margin-top:6px"></p>
      <p class="info-desc">拖动滑块改变中间态能量：两段 ΔH 各自改变，但总和恒等于直接路径——反应热只取决于始态与终态。</p>
    </div>
  </div>
</div>

<script>window.__THERMO__ = {json.dumps(DATA, ensure_ascii=False)};</script>
<script>{BODY_JS}</script>
<script>{THEME_JS}</script>
</body>
</html>
"""

open(OUT, "w", encoding="utf-8").write(HTML)
print("written:", OUT, len(HTML), "bytes")

# 自检键能计算
def dh(brk, frm): return sum(BONDS[k]*v for k,v in brk.items()) - sum(BONDS[k]*v for k,v in frm.items())
for p in PRESETS:
    print(p["eq"], "→", dh(p["brk"], p["frm"]), "kJ/mol")
