# -*- coding: utf-8 -*-
"""
生成 有机系统命名中心 chem_lab3.2.html
功能：烷烃命名闯关（随机生成主链 5-9 碳 + 1~3 个甲基/乙基支链，SVG 键线式，四选一）、
      连胜/错题记录（localStorage）、命名规则速查、常见官能团命名表
"""
import json, re

LAB12 = r"C:\Users\风逝\Documents\kimi\tasks\2026-08-31\06-27-38-247a26cf\chem-life-main\public\teaching\chem_lab1.2.html"
OUT   = r"C:\Users\风逝\Documents\kimi\tasks\2026-08-31\06-27-38-247a26cf\chem-life-main\public\teaching\chem_lab3.2.html"

old = open(LAB12, encoding="utf-8").read()
CSS = re.search(r"<style>(.*?)</style>", old, re.S).group(1)
THEME_JS = re.search(r"/\* =+ 主题切换 washi / sumi / ai =+ \*/\s*\(function\(\)\{.*?\}\)\(\);", old, re.S).group(0)

RULES = [
 ["选主链","选含碳原子最多、取代基最多的碳链作主链，按碳数称「某烷」（甲乙丙丁戊己庚辛壬癸，>10 用汉字数字）。"],
 ["编号","从离取代基最近的一端开始编号；两端等近时，使各取代基位次之和最小；仍相同则让简单基团位次小。"],
 ["书写","取代基位次-名称写在主链名称前；相同基团合并用「二、三」表示个数，位次间用逗号；简单基团（甲基）在前，复杂基团（乙基）在后。"],
 ["烯炔","选含双键/三键的最长链，从离不饱和键最近端编号，标出不饱和键位次：如 CH₃CH=CHCH₂CH₃ 为 2-戊烯。"],
 ["含氧","醇：选含 —OH 最长链，标羟基位次（2-丙醇）；醛基/羧基必在 1 号位不标注（丙醛、丙酸）；酯命名「某酸某酯」（乙酸乙酯）。"],
]

FUNC = [
 ["羟基 —OH","醇 / 酚","乙醇 CH₃CH₂OH、苯酚 C₆H₅OH"],
 ["醛基 —CHO","醛","乙醛 CH₃CHO（银镜反应）"],
 ["羧基 —COOH","羧酸","乙酸 CH₃COOH（弱酸性）"],
 ["酯基 —COO—","酯","乙酸乙酯 CH₃COOCH₂CH₃"],
 ["碳碳双键 C=C","烯烃","乙烯 CH₂=CH₂（加成、加聚）"],
 ["碳碳三键 C≡C","炔烃","乙炔 CH≡CH"],
 ["卤原子 —X","卤代烃","溴乙烷 CH₃CH₂Br（水解/消去）"],
 ["氨基 —NH₂","胺 / 氨基酸","甘氨酸 H₂NCH₂COOH"],
]

DATA = {"rules": RULES, "func": FUNC}

EXTRA_CSS = r"""
/* ===== 命名中心专用 ===== */
.nm-stage{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:24px;overflow:auto}
.nm-card{width:min(600px,94%);border:1px solid var(--line);border-radius:14px;padding:26px 30px;
 background:var(--paper);box-shadow:0 8px 30px rgba(0,0,0,.10)}
.nm-svg-wrap{display:flex;justify-content:center;margin:10px 0 4px}
.nm-opt{display:block;width:100%;text-align:left;border:1px solid var(--line-strong);background:transparent;
 color:var(--ink);border-radius:8px;padding:11px 16px;font-size:14px;margin:8px 0;cursor:pointer;
 font-family:Georgia,"Noto Serif SC",serif;transition:all .15s}
.nm-opt:hover{border-color:var(--accent);color:var(--accent)}
.nm-opt.right{border-color:#2e7d4f;color:#2e7d4f;background:rgba(46,125,79,.08)}
.nm-opt.wrong{border-color:#c0392b;color:#c0392b;background:rgba(192,57,43,.08)}
.nm-score{display:flex;gap:14px;justify-content:center;font-size:12.5px;color:var(--ink-dim);margin-bottom:8px}
.nm-score b{color:var(--accent);font-family:Georgia,serif;font-size:16px}
.rule-table{width:100%;font-size:12px;border-collapse:collapse;color:var(--ink-dim)}
.rule-table td{border:1px solid var(--line);padding:6px 8px;line-height:1.7;vertical-align:top}
.rule-table td:first-child{white-space:nowrap;color:var(--accent);font-weight:700}
.nm-feedback{min-height:22px;text-align:center;font-size:13px;margin-top:4px}
"""

BODY_JS = r"""
/* ===== 有机系统命名中心 ===== */
const D = window.__NAMING__;
const $ = (id) => document.getElementById(id);
const CN_NUM = "零一二三四五六七八九十";
const CHAIN = ["","甲","乙","丙","丁","戊","己","庚","辛","壬","癸"];
let streak = 0, best = +(localStorage.getItem("chem-naming-best")||0), wrongBook = JSON.parse(localStorage.getItem("chem-naming-wrong")||"[]");
let curQ = null, answered = false;

/* ---- 随机生成分子：主链 n 碳（5~9），k 个支链（甲基/乙基），保证主链仍最长 ---- */
function genMolecule(){
  const n = 5 + Math.floor(Math.random()*5);          // 主链 5-9
  const k = 1 + Math.floor(Math.random()*Math.min(3, n-3));
  const posAvail = [];
  for (let i = 2; i <= n-1; i++) posAvail.push(i);    // 支链不在端位
  const subs = [];
  const used = new Set();
  let guard = 0;
  while (subs.length < k && guard++ < 50){
    const p = posAvail[Math.floor(Math.random()*posAvail.length)];
    if (used.has(p)) continue;
    // 严格保证主链最长：甲基需 max(p-1,n-p)+2 < n；乙基需 max(p-1,n-p)+3 < n
    const canMe = Math.max(p-1, n-p) + 2 < n;
    const canEt = Math.max(p-1, n-p) + 3 < n;
    if (!canMe) continue;
    const kind = (Math.random() < 0.7 || !canEt) ? "甲基" : "乙基";
    used.add(p); subs.push({p, kind});
  }
  return {n, subs};
}
/* ---- 命名 ---- */
function nameMolecule(m){
  // 从两端编号，按「最低位次组」规则：排序后逐位比较（字典序），而不是简单求和
  const f = m.subs.map(s => s.p).sort((a,b)=>a-b), b = m.subs.map(s => m.n + 1 - s.p).sort((a,b)=>a-b);
  let useF = true;
  for (let i = 0; i < f.length; i++){ if (f[i] !== b[i]){ useF = f[i] < b[i]; break; } }
  const list = m.subs.map(s => ({p: useF ? s.p : m.n+1-s.p, kind: s.kind}));
  // 合并相同基团；甲基在前乙基在后
  list.sort((x,y) => (x.kind===y.kind ? x.p - y.p : x.kind==="甲基" ? -1 : 1));
  const groups = [];
  for (const s of list){
    const g = groups.find(g => g.kind===s.kind);
    if (g) g.ps.push(s.p); else groups.push({kind:s.kind, ps:[s.p]});
  }
  const parts = groups.map(g => g.ps.join(",") + "-" +
    (g.ps.length>1 ? CN_NUM[g.ps.length] : "") + g.kind);
  return parts.join("") + CHAIN[m.n] + "烷";
}
function distractors(m, correct){
  const outs = new Set([correct]);
  const tries = [];
  // 1. 反向编号错误
  const back = m.subs.map(s => ({p: m.n+1-s.p, kind: s.kind}));
  tries.push(nameMolecule({n:m.n, subs:m.subs.map(s=>({p:m.n+1-s.p, kind:s.kind}))}));
  // 2. 主链选错（±1 碳）
  tries.push(nameMolecule({n: m.n-1, subs: m.subs.map(s=>({p:s.p,kind:s.kind}))}) + "");
  tries.push(nameMolecule({n: m.n+1, subs: m.subs.map(s=>({p:s.p,kind:s.kind}))}) + "");
  // 3. 位次 ±1
  if (m.subs.length) tries.push(nameMolecule({n:m.n, subs: m.subs.map((s,i)=> i===0 ? {p: Math.min(m.n-1, s.p+1), kind:s.kind} : s)}));
  // 4. 不合并基团（拆分写法错误版）——直接用不同主链名混淆
  tries.push(nameMolecule({n:m.n, subs:[...m.subs, {p:2,kind:"甲基"}]}));
  const res = [];
  for (const t of tries){
    if (!outs.has(t) && res.length < 3 && /烷$/.test(t)){ outs.add(t); res.push(t); }
  }
  while (res.length < 3) res.push(correct.replace(CHAIN[m.n]+"烷", CHAIN[Math.max(4, m.n-2)] + "烷") + "");
  return res;
}
/* ---- SVG 键线式 ---- */
function drawMol(m){
  const dw = 64, dh = 34, x0 = 60, y0 = 90;
  let pts = [];
  for (let i = 0; i < m.n; i++) pts.push([x0 + i*dw, y0 + (i%2 ? -dh : 0)]);
  let svg = "";
  for (let i = 0; i < m.n-1; i++)
    svg += `<line x1="${pts[i][0]}" y1="${pts[i][1]}" x2="${pts[i+1][0]}" y2="${pts[i+1][1]}" stroke="currentColor" stroke-width="2"/>`;
  // 端点与拐点标记碳数
  pts.forEach((p,i) => {
    svg += `<circle cx="${p[0]}" cy="${p[1]}" r="3" fill="currentColor"/>`;
  });
  for (const s of m.subs){
    const [x,y] = pts[s.p-1];
    const dir = (s.p-1)%2 ? 1 : -1;     // 与主链折线相反方向
    const ey = y + dir*44;
    svg += `<line x1="${x}" y1="${y}" x2="${x}" y2="${ey}" stroke="currentColor" stroke-width="2"/>`;
    if (s.kind === "乙基"){
      const ey2 = ey + dir*30;
      svg += `<line x1="${x}" y1="${ey}" x2="${x+34}" y2="${ey2}" stroke="currentColor" stroke-width="2"/>`;
      svg += `<circle cx="${x+34}" cy="${ey2}" r="3" fill="currentColor"/>`;
    }
    svg += `<circle cx="${x}" cy="${ey}" r="3" fill="currentColor"/>`;
  }
  const W = x0 + (m.n-1)*dw + 90, H = 190;
  return `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" style="max-width:100%;color:var(--ink)">${svg}</svg>`;
}

/* ---- 出题流程 ---- */
function newQuestion(){
  answered = false;
  const m = genMolecule();
  const correct = nameMolecule(m);
  const opts = [correct, ...distractors(m, correct)];
  for (let i = opts.length-1; i>0; i--){ const j = Math.floor(Math.random()*(i+1)); [opts[i],opts[j]]=[opts[j],opts[i]]; }
  curQ = {m, correct, opts};
  $("stage").innerHTML = `
    <div class="nm-card">
      <div class="nm-score"><span>连胜 <b>${streak}</b></span><span>最高 <b>${best}</b></span><span>错题本 <b>${wrongBook.length}</b></span></div>
      <div style="text-align:center;font-size:13px;color:var(--ink-dim)">请写出该有机物的系统名称</div>
      <div class="nm-svg-wrap">${drawMol(m)}</div>
      ${opts.map((o,i) => `<button class="nm-opt" data-o="${o}">${String.fromCharCode(65+i)}. ${o}</button>`).join("")}
      <div class="nm-feedback" id="fb"></div>
    </div>`;
  $("stage").querySelectorAll(".nm-opt").forEach(b => b.onclick = () => answer(b));
}
function answer(btn){
  if (answered) return; answered = true;
  const pick = btn.dataset.o, right = pick === curQ.correct;
  $("stage").querySelectorAll(".nm-opt").forEach(b => {
    if (b.dataset.o === curQ.correct) b.classList.add("right");
    else if (b === btn) b.classList.add("wrong");
  });
  const m = curQ.m;
  const locTxt = m.subs.map(s => `${s.p} 位 ${s.kind}`).join("、");
  if (right){ streak++; if (streak > best){ best = streak; localStorage.setItem("chem-naming-best", best); }
    $("fb").innerHTML = `<span style="color:#2e7d4f">✓ 正确！主链 ${m.n} 碳（${CHAIN[m.n]}烷），${locTxt}</span>`;
  } else {
    streak = 0;
    wrongBook.push({svg:null, correct: curQ.correct, pick, t: Date.now()});
    localStorage.setItem("chem-naming-wrong", JSON.stringify(wrongBook.slice(-30)));
    $("fb").innerHTML = `<span style="color:#c0392b">✗ 应为「${curQ.correct}」：主链 ${m.n} 碳，${locTxt}；编号取位次和最小</span>`;
  }
  setTimeout(newQuestion, right ? 1300 : 3000);
}

$("ruleTable").innerHTML = D.rules.map(r => `<tr><td>${r[0]}</td><td>${r[1]}</td></tr>`).join("");
$("funcTable").innerHTML = D.func.map(r => `<tr><td>${r[0]}</td><td>${r[1]}</td><td>${r[2]}</td></tr>`).join("");
$("btnWrongBook").onclick = () => {
  if (!wrongBook.length) return alert("错题本是空的，去做几题吧！");
  alert("最近错题（答案）：\n" + wrongBook.slice(-10).map((w,i) => `${i+1}. ${w.correct}（你选了 ${w.pick}）`).join("\n"));
};
newQuestion();
"""

HTML = f"""<!DOCTYPE html>
<html lang="zh-CN" data-theme="washi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>有机系统命名中心 · 化学生活教学中心</title>
<style>{CSS}
{EXTRA_CSS}</style>
</head>
<body>
<nav class="topnav">
  <div class="brand">
    <span class="badge">名</span>
    <h1 style="white-space:nowrap">有机系统命名中心</h1>
    <span class="lecture-tag">ORGANIC · LAB 02</span>
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
      <h2>命名闯关</h2>
      <p class="info-desc">随机生成带支链的烷烃键线式（顶点与端点都是碳原子，氢省略），选出正确的系统名称。答错进错题本，连胜刷新纪录。</p>
      <button class="func-btn" id="btnWrongBook">查看错题本</button>
    </div>
    <div class="panel-section">
      <div class="panel-title">系统命名规则</div>
      <table class="rule-table" id="ruleTable"></table>
    </div>
  </div>

  <div class="canvas-box" style="background:var(--bg-deep)">
    <div class="nm-stage" id="stage"></div>
  </div>

  <div class="side right-panel">
    <div class="panel-section">
      <div class="panel-title">常见官能团速查</div>
      <table class="rule-table" id="funcTable"></table>
    </div>
    <div class="panel-section">
      <div class="panel-title">读键线式三步</div>
      <p class="info-desc">① 找最长碳链作主链；② 从离支链最近的一端编号（比较位次和）；③ 位次-基团名 + 主链名，相同基团合并，甲基在前。</p>
    </div>
  </div>
</div>

<script>window.__NAMING__ = {json.dumps(DATA, ensure_ascii=False)};</script>
<script>{BODY_JS}</script>
<script>{THEME_JS}</script>
</body>
</html>
"""

open(OUT, "w", encoding="utf-8").write(HTML)
print("written:", OUT, len(HTML), "bytes")
