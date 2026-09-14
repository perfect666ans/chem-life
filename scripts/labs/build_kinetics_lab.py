# -*- coding: utf-8 -*-
"""
生成 化学反应速率与平衡实验室 chem_lab4.2.html
功能：粒子碰撞沙盘（温度/浓度滑块）、A⇌B 动态平衡互变动画 + 浓度-时间曲线、
      勒夏特列三预设（NO₂/N₂O₄ 颜色、合成氨、醋酸电离），温度压强扰动看平衡移动
"""
import json, re

LAB12 = r"C:\Users\风逝\Documents\kimi\tasks\2026-08-31\06-27-38-247a26cf\chem-life-main\public\teaching\chem_lab1.2.html"
OUT   = r"C:\Users\风逝\Documents\kimi\tasks\2026-08-31\06-27-38-247a26cf\chem-life-main\public\teaching\chem_lab4.2.html"

old = open(LAB12, encoding="utf-8").read()
CSS = re.search(r"<style>(.*?)</style>", old, re.S).group(1)
THEME_JS = re.search(r"/\* =+ 主题切换 washi / sumi / ai =+ \*/\s*\(function\(\)\{.*?\}\)\(\);", old, re.S).group(0)

PRESETS = [
 {"name":"2NO₂ ⇌ N₂O₄","eq":"2NO₂(红棕) ⇌ N₂O₄(无色)　ΔH<0",
  "aName":"NO₂","bName":"N₂O₄","aColor":"#a5502e","bColor":"#c8ccd4",
  "exo":True,"gasMoles":[2,1],
  "note":"升温：平衡左移，红棕色加深；加压：平衡右移，颜色先深后浅（体积缩小 vs 平衡移动）。"},
 {"name":"N₂+3H₂ ⇌ 2NH₃","eq":"N₂ + 3H₂ ⇌ 2NH₃　ΔH<0",
  "aName":"N₂+3H₂","bName":"2NH₃","aColor":"#2a5d9f","bColor":"#6b8e4e",
  "exo":True,"gasMoles":[4,2],
  "note":"合成氨：低温高压有利平衡，但低温速率太慢——工业选 500 ℃ 是速率与产率的折中，催化剂不改平衡。"},
 {"name":"CH₃COOH ⇌ H⁺+CH₃COO⁻","eq":"CH₃COOH ⇌ H⁺ + CH₃COO⁻　ΔH>0",
  "aName":"CH₃COOH","bName":"H⁺+CH₃COO⁻","aColor":"#7a4fb0","bColor":"#c8102e",
  "exo":False,"gasMoles":None,
  "note":"弱酸电离吸热：升温电离度增大；加水稀释：平衡右移但 c(H⁺) 反而减小。"},
]

DATA = {"presets": PRESETS}

EXTRA_CSS = r"""
/* ===== 速率与平衡实验室专用 ===== */
.kb-tag{display:inline-block;font-size:11px;border-radius:10px;padding:1px 10px;margin:2px 4px 2px 0;
 border:1px solid var(--line-strong);color:var(--ink-dim)}
.kb-eq{font-family:var(--serif-cn);font-size:14.5px;line-height:1.8;margin:6px 0}
.shift-big{font-size:15px;font-weight:700;color:var(--accent);margin:6px 0;min-height:22px}
.legend-dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:5px}
#simCanvas{width:100%;height:62%;display:block}
#chartCanvas{width:100%;height:38%;display:block;border-top:1px solid var(--line)}
"""

BODY_JS = r"""
/* ===== 速率与平衡沙盘 ===== */
const D = window.__KIN__;
const $ = (id) => document.getElementById(id);
let cur = 0;
let particles = [];       // {s:0(A)|1(B), x,y,vx,vy}
let N = 60, tempK = 1.0, pf = 0.004, pb = 0.002;
let history = [], t = 0, running = true;

function P(){ return D.presets[cur]; }

function spawn(){
  particles = [];
  for (let i = 0; i < N; i++)
    particles.push({s: Math.random() < 0.8 ? 0 : 1,
      x: Math.random(), y: Math.random(),
      vx: (Math.random()-.5)*0.004, vy: (Math.random()-.5)*0.004});
  history = [];
}

function step(){
  if (!running) return;
  t += 1;
  for (const p of particles){
    p.x += p.vx*tempK; p.y += p.vy*tempK;
    if (p.x < 0.02 || p.x > 0.98) p.vx *= -1;
    if (p.y < 0.02 || p.y > 0.98) p.vy *= -1;
    p.x = Math.min(.98, Math.max(.02, p.x));
    p.y = Math.min(.98, Math.max(.02, p.y));
    // 相互转化
    if (p.s === 0 && Math.random() < pf) p.s = 1;
    else if (p.s === 1 && Math.random() < pb) p.s = 0;
  }
  if (t % 6 === 0){
    const na = particles.filter(p=>p.s===0).length;
    history.push([na, N-na]);
    if (history.length > 400) history.shift();
  }
}

function drawSim(){
  const c = $("simCanvas"); const box = c.parentElement.getBoundingClientRect();
  const dpr = window.devicePixelRatio||1;
  const W = box.width, H = box.height*0.62;
  c.width = W*dpr; c.height = H*dpr;
  const ctx = c.getContext("2d"); ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,W,H);
  const p = P();
  // 容器
  ctx.strokeStyle = "rgba(128,128,128,.5)"; ctx.lineWidth = 2;
  ctx.strokeRect(W*0.02, H*0.02, W*0.96, H*0.96);
  ctx.lineWidth = 1;
  for (const pt of particles){
    ctx.fillStyle = pt.s===0 ? p.aColor : p.bColor;
    ctx.beginPath(); ctx.arc(pt.x*W, pt.y*H, pt.s===0?4:6, 0, 7); ctx.fill();
  }
  const na = particles.filter(x=>x.s===0).length;
  ctx.font = "12px sans-serif"; ctx.textAlign = "left";
  ctx.fillStyle = p.aColor; ctx.fillText(`${p.aName}：${na}`, W*0.05, H*0.09);
  ctx.fillStyle = p.bColor === "#c8ccd4" ? "#7a7f8a" : p.bColor;
  ctx.fillText(`${p.bName}：${N-na}`, W*0.05, H*0.09 + 18);
}

function drawChart(){
  const c = $("chartCanvas"); const box = c.parentElement.getBoundingClientRect();
  const dpr = window.devicePixelRatio||1;
  const W = box.width, H = box.height*0.38;
  c.width = W*dpr; c.height = H*dpr;
  const ctx = c.getContext("2d"); ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,W,H);
  const ink = "rgba(128,128,128,.6)";
  ctx.strokeStyle = ink;
  ctx.strokeRect(W*0.06, H*0.08, W*0.9, H*0.78);
  ctx.font = "10px sans-serif"; ctx.fillStyle = ink; ctx.textAlign = "center";
  ctx.fillText("粒子数-时间曲线（→ 平衡时宏观不变、微观仍动）", W/2, H*0.97);
  if (history.length < 2) return;
  const p = P();
  const plot = (idx, color) => {
    ctx.strokeStyle = color; ctx.lineWidth = 1.6; ctx.beginPath();
    history.forEach((h,i) => {
      const x = W*0.06 + i/400 * W*0.9;
      const y = H*0.08 + (1 - h[idx]/N) * H*0.78;
      i ? ctx.lineTo(x,y) : ctx.moveTo(x,y);
    });
    ctx.stroke();
  };
  plot(0, p.aColor); plot(1, p.bColor==="#c8ccd4" ? "#7a7f8a" : p.bColor);
}

function leChatelierText(){
  const p = P();
  const T = +$("tempSlider").value, Pr = +$("presSlider").value;
  const msgs = [];
  if (T > 1.02) msgs.push(p.exo ? "升温 → 平衡向吸热方向（逆向）移动，K 减小" : "升温 → 平衡向吸热方向（正向）移动，K 增大");
  else if (T < 0.98) msgs.push(p.exo ? "降温 → 平衡向放热方向（正向）移动，K 增大" : "降温 → 平衡向放热方向（逆向）移动，K 减小");
  if (p.gasMoles){
    if (Pr > 1.02) msgs.push(`加压 → 向气体分子数减少方向移动（${p.gasMoles[0]}→${p.gasMoles[1]}，正向）`);
    else if (Pr < 0.98) msgs.push(`减压 → 向气体分子数增多方向移动（逆向）`);
  }
  $("shiftTxt").textContent = msgs.length ? msgs.join("；") : "当前无扰动，体系处于平衡状态";
  // 调整转化概率体现平衡移动
  const kf = 0.004, kb = 0.002;
  let m = 1;
  if (p.exo) m = T > 1 ? 1/T : 2 - T;   // 放热正向：升温不利
  else m = T;
  if (p.gasMoles) m *= Pr > 1 ? Pr : Pr;  // 加压促正向
  pf = kf * m; pb = kb * (p.exo ? T : 2 - T);
  tempK = T;
}

$("presetSel").innerHTML = D.presets.map((p,i)=>`<option value="${i}">${p.name}</option>`).join("");
$("presetSel").onchange = e => { cur = +e.target.value;
  $("kbEq").textContent = P().eq; $("kbNote").textContent = P().note; spawn(); };
$("concSlider").oninput = e => { N = +e.target.value; $("concTip").textContent = N + " 个粒子";
  // 保比例增减
  const curN = particles.length;
  if (N > curN){ for (let i=curN;i<N;i++) particles.push({s:Math.random()<.8?0:1,x:Math.random(),y:Math.random(),vx:(Math.random()-.5)*.004,vy:(Math.random()-.5)*.004}); }
  else particles = particles.slice(0, N);
};
$("tempSlider").oninput = leChatelierText;
$("presSlider").oninput = leChatelierText;
$("btnReset").onclick = spawn;

$("presetSel").value = "0"; $("presetSel").onchange({target:{value:"0"}});
(function frame(){ step(); drawSim(); drawChart(); requestAnimationFrame(frame); })();
"""

HTML = f"""<!DOCTYPE html>
<html lang="zh-CN" data-theme="washi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>化学反应速率与平衡 · 化学生活教学中心</title>
<style>{CSS}
{EXTRA_CSS}</style>
</head>
<body>
<nav class="topnav">
  <div class="brand">
    <span class="badge">衡</span>
    <h1 style="white-space:nowrap">化学反应速率与平衡</h1>
    <span class="lecture-tag">PRINCIPLES · LAB 02</span>
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
      <h2 id="presetName">平衡沙盘</h2>
      <div class="kb-eq" id="kbEq"></div>
      <p class="info-desc" id="kbNote"></p>
    </div>
    <div class="panel-section">
      <div class="panel-title">反应体系</div>
      <select class="select-box" id="presetSel"></select>
      <button class="func-btn" id="btnReset" style="margin-top:8px">重置模拟</button>
    </div>
    <div class="panel-section">
      <div class="panel-title">平衡移动判断</div>
      <div class="shift-big" id="shiftTxt">当前无扰动，体系处于平衡状态</div>
      <p class="info-desc">勒夏特列原理：平衡总是向「减弱」扰动的方向移动，但不能完全抵消。催化剂同等加快正逆速率，不移动平衡，只缩短到达平衡的时间。</p>
    </div>
  </div>

  <div class="canvas-box" style="background:var(--bg-deep)">
    <canvas id="simCanvas"></canvas>
    <canvas id="chartCanvas"></canvas>
  </div>

  <div class="side right-panel">
    <div class="panel-section">
      <div class="panel-title">浓度（粒子数）</div>
      <div class="slider-wrap">
        <input type="range" id="concSlider" min="20" max="160" step="10" value="60">
        <div class="slider-tip" id="concTip">60 个粒子</div>
      </div>
    </div>
    <div class="panel-section">
      <div class="panel-title">温度扰动</div>
      <div class="slider-wrap">
        <input type="range" id="tempSlider" min="0.5" max="1.5" step="0.05" value="1">
        <div class="slider-tip">1.00 = 原温度</div>
      </div>
    </div>
    <div class="panel-section">
      <div class="panel-title">压强扰动（气体体系）</div>
      <div class="slider-wrap">
        <input type="range" id="presSlider" min="0.5" max="1.5" step="0.05" value="1">
        <div class="slider-tip">1.00 = 原压强</div>
      </div>
    </div>
    <div class="panel-section">
      <div class="panel-title">观察要点</div>
      <p class="info-desc">① 曲线进入平台 = 宏观平衡；粒子仍在闪烁互变 = 动态平衡（v正=v逆≠0）。<br>
      ② 温度升高所有粒子运动加快——升温同时加快正逆速率。<br>
      ③ 扰动后曲线重新进入新平台 = 平衡移动。</p>
    </div>
  </div>
</div>

<script>window.__KIN__ = {json.dumps(DATA, ensure_ascii=False)};</script>
<script>{BODY_JS}</script>
<script>{THEME_JS}</script>
</body>
</html>
"""

open(OUT, "w", encoding="utf-8").write(HTML)
print("written:", OUT, len(HTML), "bytes")
