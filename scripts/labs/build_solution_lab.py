# -*- coding: utf-8 -*-
"""
生成 水溶液中的离子平衡实验室 chem_lab4.3.html
功能：pH 对数标尺（滑块调浓度 + 常见物质锚点）、中和滴定曲线（强强/强碱滴弱酸/强酸滴弱碱，
      突跃+指示剂变色域+体积游标）、盐类水解速查表
"""
import json, re

LAB12 = r"C:\Users\风逝\Documents\kimi\tasks\2026-08-31\06-27-38-247a26cf\chem-life-main\public\teaching\chem_lab1.2.html"
OUT   = r"C:\Users\风逝\Documents\kimi\tasks\2026-08-31\06-27-38-247a26cf\chem-life-main\public\teaching\chem_lab4.3.html"

old = open(LAB12, encoding="utf-8").read()
CSS = re.search(r"<style>(.*?)</style>", old, re.S).group(1)
THEME_JS = re.search(r"/\* =+ 主题切换 washi / sumi / ai =+ \*/\s*\(function\(\)\{.*?\}\)\(\);", old, re.S).group(0)

# pH 标尺锚点
PH_MARKS = [
 [0.0,"1 mol/L 强酸"],[1.1,"胃酸"],[2.3,"柠檬汁"],[2.9,"食醋"],[4.0,"酸雨临界 5.6 以下"],[5.6,"正常雨水（溶 CO₂）"],
 [6.5,"牛奶"],[7.0,"纯水 25℃"],[7.4,"血液"],[8.3,"小苏打溶液"],[9.2,"肥皂水"],[10.5,"氨水"],[13.0,"0.1 mol/L NaOH"],
]
# 滴定预设：弱酸/弱碱的 Ka/Kb
TITRATIONS = [
 {"id":"ss","name":"强碱滴定强酸","desc":"0.1 mol/L NaOH 滴入 20 mL 0.1 mol/L HCl","kind":"ss"},
 {"id":"ws","name":"强碱滴定弱酸（CH₃COOH）","desc":"0.1 mol/L NaOH 滴入 20 mL 0.1 mol/L CH₃COOH（Ka=1.8×10⁻⁵）","kind":"wa","ka":1.8e-5},
 {"id":"wb","name":"强酸滴定弱碱（NH₃·H₂O）","desc":"0.1 mol/L HCl 滴入 20 mL 0.1 mol/L NH₃·H₂O（Kb=1.8×10⁻⁵）","kind":"wb","kb":1.8e-5},
]
INDICATORS = [
 {"name":"甲基橙","lo":3.1,"hi":4.4,"c1":"#d23838","c2":"#e8c168"},
 {"name":"石蕊","lo":5.0,"hi":8.0,"c1":"#d23838","c2":"#2a5d9f"},
 {"name":"酚酞","lo":8.2,"hi":10.0,"c1":"#999999","c2":"#d2389a"},
]
# 盐类水解速查
SALTS = [
 ["NaCl","强酸强碱盐","不水解","中性"],["CH₃COONa","强碱弱酸盐","CH₃COO⁻ 水解","碱性"],
 ["NH₄Cl","强酸弱碱盐","NH₄⁺ 水解","酸性"],["Na₂CO₃","强碱弱酸盐","CO₃²⁻ 分步水解","碱性（纯碱）"],
 ["NaHCO₃","酸式盐","水解 > 电离","弱碱性"],["NaHSO₄","酸式盐","只电离不水解","酸性"],
 ["CH₃COONH₄","弱酸弱碱盐","双水解（程度相当）","近中性"],["(NH₄)₂CO₃","弱酸弱碱盐","双水解互促","碱性"],
 ["AlCl₃","强酸弱碱盐","Al³⁺ 水解","酸性"],["NaAlO₂","强碱弱酸盐","AlO₂⁻ 水解","碱性"],
 ["KNO₃","强酸强碱盐","不水解","中性"],["Na₂SO₃","强碱弱酸盐","SO₃²⁻ 水解","碱性"],
]

DATA = {"marks": PH_MARKS, "titrations": TITRATIONS, "indicators": INDICATORS, "salts": SALTS}

EXTRA_CSS = r"""
/* ===== 水溶液实验室专用 ===== */
.ph-scale{position:relative;height:70px;margin-top:20px}
.ph-track{position:absolute;left:0;right:0;top:22px;height:10px;border-radius:5px;
 background:linear-gradient(90deg,#d23838,#e8843c,#e8c168,#6b8e4e,#4a93d4,#5b4fa0,#7a3a78)}
.ph-mark{position:absolute;top:0;font-size:9px;color:var(--ink-mute);transform:translateX(-50%);text-align:center;width:64px}
.ph-mark i{display:block;width:1px;height:8px;background:var(--ink-mute);margin:2px auto 0}
.ph-cur{position:absolute;top:16px;width:2px;height:22px;background:var(--ink);transform:translateX(-50%)}
.ph-num{font-family:Georgia,serif;font-size:34px;color:var(--accent)}
.salt-table{width:100%;font-size:11.5px;border-collapse:collapse;color:var(--ink-dim)}
.salt-table td,.salt-table th{border:1px solid var(--line);padding:4px 6px}
.salt-table th{background:var(--surface-2);color:var(--ink)}
.tit-info{font-family:var(--mono);font-size:11.5px;color:var(--ink-dim);line-height:1.9}
"""

BODY_JS = r"""
/* ===== 水溶液中的离子平衡 ===== */
const D = window.__SOL__;
const $ = (id) => document.getElementById(id);
let titKind = "ws", titKa = 1.8e-5, titKb = 1.8e-5;
let cursorV = 10; // mL 游标

/* ---------- pH 标尺 ---------- */
function renderScale(){
  const w = $("phScale"); w.innerHTML = "";
  D.marks.forEach(([ph, label], i) => {
    const d = document.createElement("div");
    d.className = "ph-mark"; d.style.left = (ph/14*100) + "%";
    d.style.top = (i % 2 ? 0 : -13) + "px";
    d.innerHTML = `${label}<i></i><span>${ph}</span>`;
    w.appendChild(d);
  });
  const cur = document.createElement("div");
  cur.className = "ph-cur"; cur.id = "phCur";
  w.appendChild(cur);
}
function updatePH(){
  const exp = +$("phSlider").value;          // -14 ~ 0，c(H+) = 10^exp
  const pH = -exp;
  $("phNum").textContent = "pH = " + pH.toFixed(1);
  $("phConc").textContent = `c(H⁺) = 10${supNum(exp)} mol/L　c(OH⁻) = 10${supNum(-14-exp)} mol/L`;
  $("phJudge").textContent = pH < 6.95 ? "酸性" : pH > 7.05 ? "碱性" : "中性（25 ℃）";
  const c = $("phCur"); if (c) c.style.left = Math.min(100, Math.max(0, pH/14*100)) + "%";
}
function supNum(n){ return String(n).replace(/-/g,"⁻").replace(/\d/g, d=>"⁰¹²³⁴⁵⁶⁷⁸⁹"[+d]); }

/* ---------- 滴定曲线计算 ---------- */
const C0 = 0.1, V0 = 20;  // 被滴液浓度 mol/L、体积 mL；滴定液 0.1 mol/L
function titrationPH(v){
  const n0 = C0*V0, nt = C0*v, Vt = V0+v;
  if (titKind === "ss"){
    const ex = (n0 - nt)/Vt;   // 剩余 H+ 浓度
    if (Math.abs(ex) < 1e-7) return 7;
    return ex > 0 ? -Math.log10(ex) : 14 + Math.log10(-ex);
  }
  if (titKind === "wa"){       // NaOH 滴 CH3COOH
    const Ka = titKa;
    if (v <= 0) return 0.5*( -Math.log10(Ka) - Math.log10(C0) );  // √Ka·c
    if (nt < n0){ const pH = -Math.log10(Ka) + Math.log10(nt/(n0-nt)); return pH; }
    if (Math.abs(nt-n0) < 1e-9){
      const cs = n0/Vt; constKb(cs);
      const Kw = 1e-14, Kb = Kw/Ka;
      const oh = Math.sqrt(Kb*cs); return 14 + Math.log10(oh);
    }
    const ex = (nt-n0)/Vt; return 14 + Math.log10(ex);
  }
  // HCl 滴 NH3·H2O
  const Kb = titKb, Kw = 1e-14, Ka = Kw/Kb;
  if (v <= 0){ const oh = Math.sqrt(Kb*C0); return 14 + Math.log10(oh); }
  if (nt < n0){ const pOH = -Math.log10(Kb) + Math.log10(nt/(n0-nt)); return 14 - pOH; }
  if (Math.abs(nt-n0) < 1e-9){ const cs = n0/Vt; return -Math.log10(Math.sqrt(Ka*cs)); }
  const ex = (nt-n0)/Vt; return -Math.log10(ex);
}
function constKb(){}

/* ---------- 滴定曲线绘制 ---------- */
function drawTitr(){
  const c = $("titCanvas"); const box = c.parentElement.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  c.width = box.width*dpr; c.height = box.height*dpr;
  const ctx = c.getContext("2d"); ctx.setTransform(dpr,0,0,dpr,0,0);
  const W = box.width, H = box.height; ctx.clearRect(0,0,W,H);
  const cs2 = getComputedStyle(document.body);
  const ink = cs2.getPropertyValue("--ink").trim()||"#999";
  const acc = cs2.getPropertyValue("--accent").trim()||"#c8102e";
  const VMAX = 40;
  const X = v => W*0.09 + v/VMAX * W*0.86;
  const Y = ph => H*0.08 + (14-ph)/14 * H*0.82;
  // 坐标
  ctx.strokeStyle = ink; ctx.globalAlpha = .25;
  for (let ph = 0; ph <= 14; ph += 2){
    ctx.beginPath(); ctx.moveTo(X(0), Y(ph)); ctx.lineTo(X(VMAX), Y(ph)); ctx.stroke();
    ctx.globalAlpha = .6; ctx.fillStyle = ink; ctx.font = "10px sans-serif"; ctx.textAlign = "right";
    ctx.fillText(ph, X(0)-5, Y(ph)+3); ctx.globalAlpha = .25;
  }
  ctx.globalAlpha = 1;
  ctx.beginPath(); ctx.moveTo(X(0), Y(0)); ctx.lineTo(X(0), Y(14)); ctx.lineTo(X(VMAX), Y(14)); ctx.strokeStyle = ink; ctx.stroke();
  ctx.fillStyle = ink; ctx.font = "10px sans-serif"; ctx.textAlign = "center";
  for (let v = 0; v <= 40; v += 10) ctx.fillText(v, X(v), Y(14)+14);
  ctx.fillText("滴定液体积 V / mL", X(20), Y(14)+30);
  ctx.save(); ctx.translate(14, Y(7)); ctx.rotate(-Math.PI/2); ctx.fillText("pH", 0, 0); ctx.restore();
  // 指示剂变色域
  for (const ind of D.indicators){
    ctx.fillStyle = ind.c2; ctx.globalAlpha = .08;
    ctx.fillRect(X(0), Y(ind.hi), X(VMAX)-X(0), Y(ind.lo)-Y(ind.hi));
    ctx.globalAlpha = .5; ctx.fillStyle = ind.c2; ctx.textAlign = "left";
    ctx.fillText(`${ind.name} ${ind.lo}~${ind.hi}`, X(30.5), (Y(ind.lo)+Y(ind.hi))/2+3);
  }
  ctx.globalAlpha = 1;
  // 曲线
  ctx.beginPath(); ctx.strokeStyle = acc; ctx.lineWidth = 2;
  let eqV = 20;
  for (let i = 0; i <= 800; i++){
    const v = i/800*VMAX;
    const ph = Math.min(14.2, Math.max(-0.2, titrationPH(v)));
    i ? ctx.lineTo(X(v), Y(ph)) : ctx.moveTo(X(v), Y(ph));
  }
  ctx.stroke(); ctx.lineWidth = 1;
  // 计量点
  const phEq = titrationPH(20);
  ctx.setLineDash([4,4]); ctx.strokeStyle = ink; ctx.globalAlpha = .5;
  ctx.beginPath(); ctx.moveTo(X(20), Y(14)); ctx.lineTo(X(20), Y(phEq)); ctx.lineTo(X(0), Y(phEq)); ctx.stroke();
  ctx.setLineDash([]); ctx.globalAlpha = 1;
  ctx.fillStyle = acc; ctx.beginPath(); ctx.arc(X(20), Y(phEq), 4, 0, 7); ctx.fill();
  ctx.font = "11px sans-serif"; ctx.textAlign = "left";
  ctx.fillText(`化学计量点 V=20 mL，pH=${phEq.toFixed(1)}`, X(20)+8, Y(phEq)-8);
  // 游标
  const phC = Math.min(14.2, Math.max(-0.2, titrationPH(cursorV)));
  ctx.strokeStyle = "#b8860b"; ctx.beginPath(); ctx.moveTo(X(cursorV), Y(14)); ctx.lineTo(X(cursorV), Y(0)); ctx.stroke();
  ctx.fillStyle = "#b8860b"; ctx.beginPath(); ctx.arc(X(cursorV), Y(phC), 4.5, 0, 7); ctx.fill();
  $("titInfo").innerHTML =
    `游标：V = ${cursorV.toFixed(1)} mL，pH = ${titrationPH(cursorV).toFixed(2)}<br>` +
    `计量点 pH = ${phEq.toFixed(1)} → ${phEq<7?"酸性（选甲基橙）":phEq>7?"碱性（选酚酞）":"中性（甲基橙/酚酞均可）"}`;
}

/* ---------- 水解表 ---------- */
function renderSalts(){
  $("saltTable").innerHTML = "<tr><th>盐</th><th>类型</th><th>水解情况</th><th>酸碱性</th></tr>" +
    D.salts.map(r => `<tr>${r.map(x => `<td>${x}</td>`).join("")}</tr>`).join("");
}

$("phSlider").oninput = updatePH;
$("titSel").innerHTML = D.titrations.map(t => `<option value="${t.id}">${t.name}</option>`).join("");
$("titSel").onchange = (e) => {
  const t = D.titrations.find(x => x.id === e.target.value);
  titKind = t.kind; if (t.ka) titKa = t.ka; if (t.kb) titKb = t.kb;
  $("titDesc").textContent = t.desc; drawTitr();
};
$("titCursor").oninput = (e) => { cursorV = +e.target.value; drawTitr(); };

renderScale(); renderSalts();
$("titSel").value = "ws"; $("titSel").onchange({target:{value:"ws"}});
updatePH();
window.addEventListener("resize", drawTitr);
"""

HTML = f"""<!DOCTYPE html>
<html lang="zh-CN" data-theme="washi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>水溶液中的离子平衡 · 化学生活教学中心</title>
<style>{CSS}
{EXTRA_CSS}</style>
</head>
<body>
<nav class="topnav">
  <div class="brand">
    <span class="badge">液</span>
    <h1 style="white-space:nowrap">水溶液中的离子平衡</h1>
    <span class="lecture-tag">PRINCIPLES · LAB 03</span>
  </div>
  <div class="nav-right">
    <a class="nav-btn" href="chem_lab4.1.html">热效应 <span class="arr">→</span></a>
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
    <div class="panel-section">
      <div class="panel-title">pH 对数标尺</div>
      <div class="ph-num" id="phNum">pH = 7.0</div>
      <div class="tit-info" id="phConc"></div>
      <div class="tag-wrap"><span class="tag" id="phJudge">中性</span></div>
      <div class="slider-wrap" style="margin-top:6px">
        <input type="range" id="phSlider" min="-14" max="0" step="0.1" value="-7">
      </div>
      <div class="ph-scale" id="phScale"></div>
      <p class="info-desc">拖动改变 c(H⁺)：pH 是对数标尺，差 1 个单位浓度差 10 倍。Kw = c(H⁺)·c(OH⁻) = 10⁻¹⁴（25 ℃）。</p>
    </div>
    <div class="panel-section">
      <div class="panel-title">盐类水解速查</div>
      <table class="salt-table" id="saltTable"></table>
      <p class="info-desc">口诀：有弱才水解，谁弱谁水解，谁强显谁性，越弱越水解。</p>
    </div>
  </div>

  <div class="canvas-box" style="background:var(--bg-deep)">
    <canvas id="titCanvas"></canvas>
  </div>

  <div class="side right-panel">
    <div class="panel-section">
      <div class="panel-title">滴定体系</div>
      <select class="select-box" id="titSel"></select>
      <p class="info-desc" id="titDesc" style="margin-top:6px"></p>
    </div>
    <div class="panel-section">
      <div class="panel-title">体积游标</div>
      <div class="slider-wrap">
        <input type="range" id="titCursor" min="0" max="40" step="0.1" value="10">
      </div>
      <div class="tit-info" id="titInfo"></div>
    </div>
    <div class="panel-section">
      <div class="panel-title">要点</div>
      <p class="info-desc">① 突跃范围决定指示剂：强碱滴弱酸计量点 &gt; 7，选酚酞；强酸滴弱碱计量点 &lt; 7，选甲基橙。<br>
      ② 半计量点（V=10 mL）处 pH = pKa，可用来测弱酸的 Ka。<br>
      ③ 终点判断：最后一滴使指示剂变色且半分钟不褪。</p>
    </div>
  </div>
</div>

<script>window.__SOL__ = {json.dumps(DATA, ensure_ascii=False)};</script>
<script>{BODY_JS}</script>
<script>{THEME_JS}</script>
</body>
</html>
"""

open(OUT, "w", encoding="utf-8").write(HTML)
print("written:", OUT, len(HTML), "bytes")

# 自检滴定 pH
import math
def ph_ss(v, n0=2.0, nt=0.1):
    ex = (2.0 - 0.1*v)/(20+v)
    if abs(ex) < 1e-9: return 7
    return -math.log10(ex) if ex > 0 else 14 + math.log10(-ex)
print("强强 V=0:", round(ph_ss(0),2), "V=19.9:", round(ph_ss(19.9),2), "V=20:", ph_ss(20), "V=20.1:", round(ph_ss(20.1),2), "V=40:", round(ph_ss(40),2))
