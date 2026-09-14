# -*- coding: utf-8 -*-
"""
生成 电化学实验室 chem_lab4.4.html（原电池 / 电解池）
Canvas 场景动画：烧杯+双电极+导线电子流+气泡+离子迁移+电表/电源；
预设：Zn-Cu 原电池、Fe-Cu 原电池、电解 CuCl₂、电解饱和食盐水、铁镀铜、钢铁吸氧腐蚀
"""
import json, re

LAB12 = r"C:\Users\风逝\Documents\kimi\tasks\2026-08-31\06-27-38-247a26cf\chem-life-main\public\teaching\chem_lab1.2.html"
OUT   = r"C:\Users\风逝\Documents\kimi\tasks\2026-08-31\06-27-38-247a26cf\chem-life-main\public\teaching\chem_lab4.4.html"

old = open(LAB12, encoding="utf-8").read()
CSS = re.search(r"<style>(.*?)</style>", old, re.S).group(1)
THEME_JS = re.search(r"/\* =+ 主题切换 washi / sumi / ai =+ \*/\s*\(function\(\)\{.*?\}\)\(\);", old, re.S).group(0)

# 电极金属颜色
METAL = {"Zn":"#8b9bb4","Cu":"#c77b4a","Fe":"#9aa0a6","Ag":"#d0d4da","C":"#4a4a4e","Pt":"#cfd6e4"}

PRESETS = [
 {"name":"Zn-Cu 原电池（稀硫酸）","type":"galvanic",
  "left":{"metal":"Zn","role":"负极（−）"},"right":{"metal":"Cu","role":"正极（+）"},
  "electrolyte":"稀 H₂SO₄","color":"#dce8f5",
  "anode":"Zn − 2e⁻ = Zn²⁺（锌溶解变细，氧化）",
  "cathode":"2H⁺ + 2e⁻ = H₂↑（铜表面冒气泡，还原）",
  "eDir":"L2R","bubbles":"R","dissolve":"L",
  "ions":[["H⁺","R"],["SO₄²⁻","L"],["Zn²⁺","R"]],
  "note":"活泼金属 Zn 作负极。电子 Zn→导线→Cu；溶液中阳离子移向正极（Cu），阴离子移向负极（Zn）。"},
 {"name":"Fe-Cu 原电池（稀硫酸）","type":"galvanic",
  "left":{"metal":"Fe","role":"负极（−）"},"right":{"metal":"Cu","role":"正极（+）"},
  "electrolyte":"稀 H₂SO₄","color":"#dce8f5",
  "anode":"Fe − 2e⁻ = Fe²⁺（铁溶解，溶液变浅绿）",
  "cathode":"2H⁺ + 2e⁻ = H₂↑（铜冒气泡）",
  "eDir":"L2R","bubbles":"R","dissolve":"L",
  "ions":[["H⁺","R"],["SO₄²⁻","L"],["Fe²⁺","R"]],
  "note":"较活泼的 Fe 作负极被腐蚀——这也是电化学防腐要保护金属作正极的原因。"},
 {"name":"Cu-Ag 原电池（AgNO₃ 溶液）","type":"galvanic",
  "left":{"metal":"Cu","role":"负极（−）"},"right":{"metal":"Ag","role":"正极（+）"},
  "electrolyte":"AgNO₃ 溶液","color":"#e8eef7",
  "anode":"Cu − 2e⁻ = Cu²⁺（铜溶解，溶液变蓝）",
  "cathode":"Ag⁺ + e⁻ = Ag（银电极上有银白色析出）",
  "eDir":"L2R","bubbles":None,"dissolve":"L","deposit":"R",
  "ions":[["Ag⁺","R"],["NO₃⁻","L"],["Cu²⁺","R"]],
  "note":"不活泼金属也能作正极参与原电池：正极材料本身不反应，是溶液中的 Ag⁺ 在其表面得电子析出。"},
 {"name":"电解 CuCl₂ 溶液（惰性电极）","type":"electrolytic",
  "left":{"metal":"C","role":"阴极（接电源−）"},"right":{"metal":"C","role":"阳极（接电源+）"},
  "electrolyte":"CuCl₂ 溶液","color":"#cfe3d8",
  "anode":"阳极（右）：2Cl⁻ − 2e⁻ = Cl₂↑（黄绿色气泡，湿润淀粉-KI 试纸变蓝）",
  "cathode":"阴极（左）：Cu²⁺ + 2e⁻ = Cu（红色固体析出）",
  "eDir":"R2L","bubbles":"R","deposit":"L",
  "ions":[["Cu²⁺","L"],["Cl⁻","R"]],
  "note":"电解池由外接电源驱动：阳极接电源正极（失电子），阴极接电源负极（得电子）。阳离子移向阴极、阴离子移向阳极。"},
 {"name":"电解饱和食盐水（氯碱工业）","type":"electrolytic",
  "left":{"metal":"C","role":"阴极（接电源−）"},"right":{"metal":"C","role":"阳极（接电源+）"},
  "electrolyte":"饱和食盐水 + 酚酞","color":"#f2e4e4",
  "anode":"阳极（右）：2Cl⁻ − 2e⁻ = Cl₂↑",
  "cathode":"阴极（左）：2H₂O + 2e⁻ = H₂↑ + 2OH⁻（附近溶液变红）",
  "eDir":"R2L","bubbles":"BOTH",
  "ions":[["Na⁺","L"],["Cl⁻","R"],["H⁺(水)","L"]],
  "note":"阴极区生成 NaOH 使酚酞变红。总反应：2NaCl + 2H₂O =通电= 2NaOH + H₂↑ + Cl₂↑。"},
 {"name":"铁件镀铜（电镀）","type":"electrolytic",
  "left":{"metal":"Fe","role":"阴极（待镀件）"},"right":{"metal":"Cu","role":"阳极（镀层金属）"},
  "electrolyte":"CuSO₄ 溶液","color":"#cfe0f2",
  "anode":"阳极（右）：Cu − 2e⁻ = Cu²⁺（铜溶解补充）",
  "cathode":"阴极（左）：Cu²⁺ + 2e⁻ = Cu（铁件析出红色铜层）",
  "eDir":"R2L","dissolve":"R","deposit":"L",
  "ions":[["Cu²⁺","L"],["SO₄²⁻","R"]],
  "note":"电镀规律：待镀件作阴极、镀层金属作阳极、镀层金属离子溶液作电镀液，其浓度基本不变。"},
 {"name":"钢铁的吸氧腐蚀（中性水膜）","type":"corrosion",
  "left":{"metal":"Fe","role":"负极（Fe）"},"right":{"metal":"C","role":"正极（杂质 C）"},
  "electrolyte":"水膜（溶有 O₂）","color":"#e5e9ee",
  "anode":"负极：Fe − 2e⁻ = Fe²⁺（铁被腐蚀）",
  "cathode":"正极：O₂ + 2H₂O + 4e⁻ = 4OH⁻",
  "eDir":"L2R","dissolve":"L",
  "ions":[["Fe²⁺","R"],["OH⁻","R"]],
  "note":"Fe²⁺ 与 OH⁻ 结合成 Fe(OH)₂，再被氧化为 Fe(OH)₃，脱水形成铁锈 Fe₂O₃·xH₂O。酸性较强时则为析氢腐蚀。"},
]

DATA = {"presets": PRESETS, "metal": METAL}

EXTRA_CSS = r"""
/* ===== 电化学实验室专用 ===== */
.eq-card{border:1px solid var(--line);border-radius:8px;padding:10px 12px;margin:8px 0;background:var(--surface)}
.eq-card .t{font-size:11px;color:var(--ink-mute);margin-bottom:4px}
.eq-card .e{font-size:13px;line-height:1.8;color:var(--ink)}
.eq-card.an{border-left:3px solid var(--accent)}
.eq-card.ca{border-left:3px solid #2a5d9f}
.rule-list{font-size:12px;line-height:2;color:var(--ink-dim)}
.rule-list b{color:var(--accent)}
.disc-table{width:100%;font-size:11.5px;border-collapse:collapse;color:var(--ink-dim)}
.disc-table td{border:1px solid var(--line);padding:5px 7px;line-height:1.6}
.disc-table td:first-child{white-space:nowrap;color:var(--ink)}
"""

BODY_JS = r"""
/* ===== 电化学实验室 ===== */
const D = window.__ELEC__;
const $ = (id) => document.getElementById(id);
let cur = 0, running = true, speed = 1, t = 0;
let electrons = [], bubbles = [], ions = [];

function P(){ return D.presets[cur]; }

function initParticles(){
  electrons = Array.from({length: 14}, (_,i) => ({t: i/14}));
  bubbles = [];
  ions = [];
  const ionColors = {"+":"#c8102e","-":"#2a5d9f"};
  for (const [name, to] of P().ions){
    const cat = !name.includes("⁻");
    for (let k = 0; k < 5; k++)
      ions.push({x: 0.2+Math.random()*0.6, y: 0.55+Math.random()*0.3,
                 to, c: cat ? "#d23838" : "#2a5d9f", name, ph: Math.random()*9});
  }
}

/* 场景几何：烧杯内液面、两电极位置（归一化坐标） */
const GEO = {beaker:[0.12,0.34,0.76,0.58], liquid:0.42, eL:0.30, eR:0.70, wireY:0.16};

function draw(){
  const c = $("ecCanvas"); const box = c.parentElement.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  if (c.width !== box.width*dpr){ c.width = box.width*dpr; c.height = box.height*dpr; }
  const ctx = c.getContext("2d"); ctx.setTransform(dpr,0,0,dpr,0,0);
  const W = box.width, H = box.height;
  const cs = getComputedStyle(document.body);
  const ink = cs.getPropertyValue("--ink").trim() || "#999";
  const acc = cs.getPropertyValue("--accent").trim() || "#c8102e";
  ctx.clearRect(0,0,W,H);
  const p = P();
  const G = GEO;
  const bx = G.beaker[0]*W, by = G.beaker[1]*H, bw = G.beaker[2]*W, bh = G.beaker[3]*H;
  const liqY = (G.liquid)*H;

  /* 导线：左电极顶 → 顶部 → 右电极顶，中间串电表或电源 */
  const topY = G.wireY*H;
  const lx = G.eL*W, rx = G.eR*W;
  ctx.strokeStyle = ink; ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(lx, by - 30); ctx.lineTo(lx, topY); ctx.lineTo(W/2 - 36, topY);
  ctx.moveTo(W/2 + 36, topY); ctx.lineTo(rx, topY); ctx.lineTo(rx, by - 30);
  ctx.stroke(); ctx.lineWidth = 1;

  /* 电表（原电池/腐蚀）或电源（电解池） */
  if (p.type === "electrolytic"){
    ctx.strokeRect(W/2-36, topY-20, 72, 40);
    ctx.fillStyle = ink; ctx.font = "11px sans-serif"; ctx.textAlign = "center";
    ctx.fillText("直流电源", W/2, topY + 2);
    ctx.fillStyle = acc; ctx.fillText("+", W/2+26, topY - 6);
    ctx.fillStyle = "#2a5d9f"; ctx.fillText("−", W/2-26, topY - 6);
  } else {
    ctx.beginPath(); ctx.arc(W/2, topY, 20, 0, 7); ctx.stroke();
    ctx.fillStyle = ink; ctx.font = "13px Georgia"; ctx.textAlign = "center";
    ctx.fillText("A", W/2, topY + 4);
    if (running){
      const ang = -0.9 + 0.9*Math.abs(Math.sin(t*2));
      ctx.beginPath(); ctx.moveTo(W/2, topY);
      ctx.lineTo(W/2 + 14*Math.sin(ang)*0.9, topY - 14*Math.cos(ang)*0.9 + 4);
      ctx.strokeStyle = acc; ctx.stroke(); ctx.strokeStyle = ink;
    }
  }

  /* 电子流（沿导线） */
  if (running && p.type !== "corrosion" || running){
    const dir = p.eDir === "L2R" ? 1 : -1;
    ctx.fillStyle = "#e8c168";
    for (const e of electrons){
      e.t += 0.0016 * speed * dir;
      if (e.t > 1) e.t -= 1; if (e.t < 0) e.t += 1;
      let x, y;
      const tt = e.t;
      if (tt < 0.42){ x = lx; y = (by-30) + (topY-(by-30)) * (tt/0.14) * -1 * dir*0 + (topY-(by-30))*(Math.min(tt/0.14,1)); y = (by-30) + (topY-(by-30))*Math.min(tt/0.14,1); }
      // 简化：三段线性 L: 0~0.14 竖直, 0.14~0.86 水平, 0.86~1 竖直
      if (tt < 0.14){ x = lx; y = (by-30) + (topY-(by-30))*(tt/0.14); }
      else if (tt < 0.86){ const s = (tt-0.14)/0.72; x = lx + (rx-lx)*s; y = topY; }
      else { x = rx; y = topY + ((by-30)-topY)*((tt-0.86)/0.14); }
      ctx.beginPath(); ctx.arc(x, y, 2.6, 0, 7); ctx.fill();
    }
    // 电子方向标注
    ctx.fillStyle = ink; ctx.font = "10px sans-serif"; ctx.globalAlpha = .6; ctx.textAlign = "center";
    ctx.fillText(dir === 1 ? "e⁻ →" : "← e⁻", W/2 + 70, topY + 4);
    ctx.globalAlpha = 1;
  }

  /* 烧杯 */
  ctx.strokeStyle = ink; ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(bx, by); ctx.lineTo(bx, by+bh); ctx.lineTo(bx+bw, by+bh); ctx.lineTo(bx+bw, by);
  ctx.stroke(); ctx.lineWidth = 1;
  /* 溶液 */
  ctx.fillStyle = p.color; ctx.globalAlpha = .55;
  ctx.fillRect(bx+2, liqY, bw-4, by+bh-liqY-2);
  ctx.globalAlpha = 1;
  ctx.fillStyle = ink; ctx.font = "11px sans-serif"; ctx.textAlign = "center"; ctx.globalAlpha = .6;
  ctx.fillText(p.electrolyte, W/2, by+bh+18); ctx.globalAlpha = 1;

  /* 电极 */
  const drawElectrode = (x, side) => {
    const e = side === "L" ? p.left : p.right;
    let w = 14, h = by + bh - liqY + 34;
    // 溶解效果：电极随时间变细（循环演示）
    let shrink = 0;
    if (running && p.dissolve === side) shrink = (Math.sin(t*0.3)+1)/2 * 4;
    ctx.fillStyle = D.metal[e.metal] || "#999";
    ctx.fillRect(x - w/2 + shrink/2, by - 30, w - shrink, h);
    // 析出效果
    if (running && p.deposit === side){
      const dep = (Math.sin(t*0.3)+1)/2;
      ctx.fillStyle = side==="L" && p.name.includes("镀") ? "#c77b4a" : (p.name.includes("Ag")?"#e8ecf2":"#b8563a");
      ctx.globalAlpha = .5 + dep*.5;
      ctx.fillRect(x - w/2 - 2.5, liqY + 6, 3, h - 40);
      ctx.fillRect(x + w/2 - .5, liqY + 6, 3, h - 40);
      ctx.globalAlpha = 1;
    }
    ctx.fillStyle = ink; ctx.font = "bold 12px sans-serif"; ctx.textAlign = "center";
    ctx.fillText(e.metal, x, by - 38);
    ctx.font = "11px sans-serif"; ctx.fillStyle = acc;
    ctx.fillText(e.role, x, by + bh + 34);
  };
  drawElectrode(lx, "L"); drawElectrode(rx, "R");

  /* 气泡 */
  if (running && p.bubbles){
    const at = p.bubbles === "BOTH" ? ["L","R"] : [p.bubbles];
    if (Math.random() < 0.12*speed)
      for (const s of at) bubbles.push({x: (s==="L"?lx:rx) + (Math.random()*14-7), y: liqY + 40 + Math.random()*40, r: 1.5+Math.random()*2});
    ctx.strokeStyle = ink; ctx.globalAlpha = .6;
    for (const b of bubbles){
      b.y -= 0.9*speed; b.r += 0.008;
      ctx.beginPath(); ctx.arc(b.x, b.y, b.r, 0, 7); ctx.stroke();
    }
    bubbles = bubbles.filter(b => b.y > liqY + 6);
    ctx.globalAlpha = 1;
  }

  /* 离子迁移 */
  if (running){
    for (const io of ions){
      const target = io.to === "L" ? G.eL : G.eR;
      io.x += (target - io.x) * 0.004 * speed;
      io.y += Math.sin(t*2 + io.ph) * 0.0006;
      if (Math.abs(io.x - target) < 0.02) io.x = 0.2 + Math.random()*0.6;
      ctx.fillStyle = io.c;
      ctx.beginPath(); ctx.arc(io.x*W, io.y*H, 3, 0, 7); ctx.fill();
      ctx.font = "9px sans-serif"; ctx.textAlign = "center";
      ctx.fillText(io.name, io.x*W, io.y*H - 6);
    }
  }

  /* 腐蚀特殊标注 */
  if (p.type === "corrosion" && running){
    ctx.fillStyle = "#b8563a"; ctx.globalAlpha = .5 + .3*Math.sin(t);
    ctx.beginPath(); ctx.arc(lx, liqY + 26, 8, 0, 7); ctx.fill();
    ctx.globalAlpha = .8; ctx.font = "10px sans-serif"; ctx.textAlign = "left";
    ctx.fillText("Fe²⁺ + OH⁻ → Fe(OH)₂ → 铁锈", lx + 16, liqY + 30);
    ctx.globalAlpha = 1;
  }
}

function frame(){
  if (running) t += 0.016 * speed;
  draw();
  requestAnimationFrame(frame);
}

function renderPanel(){
  const p = P();
  $("cellName").textContent = p.name;
  $("cellType").textContent = {galvanic:"原电池", electrolytic:"电解池", corrosion:"金属腐蚀"}[p.type];
  $("eqAn").textContent = p.anode;
  $("eqCa").textContent = p.cathode;
  $("cellNote").textContent = p.note;
  $("anTitle").textContent = p.type === "galvanic" ? "负极（氧化）" : p.type === "corrosion" ? "负极（氧化）" : "阳极（氧化）";
  $("caTitle").textContent = p.type === "galvanic" ? "正极（还原）" : p.type === "corrosion" ? "正极（还原）" : "阴极（还原）";
  initParticles();
}

$("cellSel").innerHTML = D.presets.map((p,i) => `<option value="${i}">${p.name}</option>`).join("");
$("cellSel").onchange = (e) => { cur = +e.target.value; renderPanel(); };
$("runSwitch").onclick = () => { running = !running;
  $("runSwitch").classList.toggle("active", running);
  $("runState").textContent = running ? "闭合（粒子迁移中）" : "断开（反应停止）"; };
$("speedSlider").oninput = (e) => { speed = +e.target.value; $("speedTip").textContent = "速度 ×" + speed.toFixed(1); };
$("runSwitch").classList.add("active");

renderPanel();
requestAnimationFrame(frame);
"""

HTML = f"""<!DOCTYPE html>
<html lang="zh-CN" data-theme="washi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>化学反应与电能 · 化学生活教学中心</title>
<style>{CSS}
{EXTRA_CSS}</style>
</head>
<body>
<nav class="topnav">
  <div class="brand">
    <span class="badge">电</span>
    <h1 style="white-space:nowrap">化学反应与电能</h1>
    <span class="lecture-tag">PRINCIPLES · LAB 04</span>
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
    <div class="info-card">
      <h2 id="cellName">—</h2>
      <div class="tag-wrap"><span class="tag" id="cellType"></span></div>
      <p class="info-desc" id="cellNote"></p>
    </div>
    <div class="panel-section">
      <div class="panel-title" id="anTitle">负极（氧化）</div>
      <div class="eq-card an"><div class="e" id="eqAn"></div></div>
      <div class="panel-title" id="caTitle">正极（还原）</div>
      <div class="eq-card ca"><div class="e" id="eqCa"></div></div>
    </div>
    <div class="panel-section">
      <div class="panel-title">回路开关</div>
      <div class="switch-row">
        <span class="switch-label" id="runState">闭合（粒子迁移中）</span>
        <div class="switch" id="runSwitch"></div>
      </div>
      <div class="slider-wrap" style="margin-top:10px">
        <input type="range" id="speedSlider" min="0.2" max="3" step="0.1" value="1">
        <div class="slider-tip" id="speedTip">速度 ×1.0</div>
      </div>
    </div>
  </div>

  <div class="canvas-box" style="background:var(--bg-deep)">
    <canvas id="ecCanvas"></canvas>
  </div>

  <div class="side right-panel">
    <div class="panel-section">
      <div class="panel-title">装置选择</div>
      <select class="select-box" id="cellSel"></select>
    </div>
    <div class="panel-section">
      <div class="panel-title">判断口诀</div>
      <div class="rule-list">
        原电池：负<b>氧</b>正<b>还</b>，电子负→正（外电路），阳离子→正极。<br>
        电解池：阳<b>氧</b>阴<b>还</b>，阳极接电源正极，阳离子→阴极。<br>
        电镀：镀件作<b>阴极</b>，镀层金属作<b>阳极</b>。
      </div>
    </div>
    <div class="panel-section">
      <div class="panel-title">放电顺序（惰性电极）</div>
      <table class="disc-table">
        <tr><td>阳极</td><td>活性电极自身 &gt; S²⁻&gt;I⁻&gt;Br⁻&gt;Cl⁻&gt;OH⁻&gt;含氧酸根</td></tr>
        <tr><td>阴极</td><td>Ag⁺&gt;Fe³⁺&gt;Cu²⁺&gt;H⁺(酸)&gt;Fe²⁺&gt;Zn²⁺&gt;H⁺(水)&gt;Al³⁺&gt;Mg²⁺&gt;Na⁺</td></tr>
      </table>
    </div>
  </div>
</div>

<script>window.__ELEC__ = {json.dumps(DATA, ensure_ascii=False)};</script>
<script>{BODY_JS}</script>
<script>{THEME_JS}</script>
</body>
</html>
"""

open(OUT, "w", encoding="utf-8").write(HTML)
print("written:", OUT, len(HTML), "bytes")
