# -*- coding: utf-8 -*-
"""
生成 同分异构体闯关 chem_lab3.3.html
5 章关卡（烷烃骨架/等效氢与卤代/烯炔/苯环/含氧），每章 5 题四选一，带解析；
章节进度 + 通关判定（≥80%）存 localStorage
"""
import json, re

LAB12 = r"C:\Users\风逝\Documents\kimi\tasks\2026-08-31\06-27-38-247a26cf\chem-life-main\public\teaching\chem_lab1.2.html"
OUT   = r"C:\Users\风逝\Documents\kimi\tasks\2026-08-31\06-27-38-247a26cf\chem-life-main\public\teaching\chem_lab3.3.html"

old = open(LAB12, encoding="utf-8").read()
CSS = re.search(r"<style>(.*?)</style>", old, re.S).group(1)
THEME_JS = re.search(r"/\* =+ 主题切换 washi / sumi / ai =+ \*/\s*\(function\(\)\{.*?\}\)\(\);", old, re.S).group(0)

CHAPTERS = ["烷烃骨架", "等效氢与卤代", "烯烃与炔烃", "苯环定位", "醇醚·羧酸与酯"]

# q, opts(4), ans(index), 解析
Q = [
 # ===== 烷烃骨架 =====
 (0,"丁烷 C₄H₁₀ 的同分异构体有几种？",["1 种","2 种","3 种","4 种"],1,
  "2 种：正丁烷 CH₃CH₂CH₂CH₃ 和异丁烷（2-甲基丙烷）。从 C₄ 开始才有碳链异构。"),
 (0,"戊烷 C₅H₁₂ 的同分异构体有几种？",["2 种","3 种","4 种","5 种"],1,
  "3 种：正戊烷、2-甲基丁烷（异戊烷）、2,2-二甲基丙烷（新戊烷）。"),
 (0,"己烷 C₆H₁₄ 的同分异构体有几种？",["4 种","5 种","6 种","7 种"],1,
  "5 种：正己烷、2-甲基戊烷、3-甲基戊烷、2,2-二甲基丁烷、2,3-二甲基丁烷。"),
 (0,"庚烷 C₇H₁₆ 的同分异构体有几种？",["7 种","8 种","9 种","11 种"],2,
  "9 种。常用数轴记忆：C₄=2、C₅=3、C₆=5、C₇=9、C₈=18。"),
 (0,"戊烷的三种同分异构体中，沸点最高的是？",["新戊烷","异戊烷","正戊烷","三者相同"],2,
  "正戊烷。支链越多分子间接触面积越小、范德华力越弱，沸点越低：正戊烷 36℃ > 异戊烷 28℃ > 新戊烷 9.5℃。"),
 # ===== 等效氢与卤代 =====
 (1,"新戊烷（2,2-二甲基丙烷）的一氯代物有几种？",["1 种","2 种","3 种","4 种"],0,
  "1 种。12 个氢全部等效（4 个甲基对称）——这也是证明分子高度对称的经典例子。"),
 (1,"丁烷 C₄H₁₀ 的一氯代物共有几种？",["2 种","3 种","4 种","5 种"],2,
  "4 种：正丁烷有 2 种等效氢（1 位、2 位）→ 2 种；异丁烷有 2 种（甲基氢、叔氢）→ 2 种；共 4 种。"),
 (1,"CH₄ 的二氯代物只有 1 种，这一事实证明了什么？",["甲烷是平面正方形","甲烷是正四面体结构","C-H 键完全相同","氯原子很大"],1,
  "若 CH₄ 是平面正方形，CH₂Cl₂ 应有邻位、对位 2 种；只有 1 种说明 4 个氢在空间完全等价 → 正四面体。"),
 (1,"丙烷的二氯代物 C₃H₆Cl₂ 有几种？",["2 种","3 种","4 种","5 种"],2,
  "4 种：1,1-、2,2-、1,2-、1,3-二氯丙烷。方法：定一议二——先固定一个 Cl，再移动另一个。"),
 (1,"戊烷 C₅H₁₂ 的一氯代物共有几种？",["6 种","7 种","8 种","9 种"],2,
  "8 种：正戊烷 3 种等效氢、异戊烷 4 种、新戊烷 1 种，共 3+4+1=8 种。"),
 # ===== 烯烃与炔烃 =====
 (2,"分子式 C₄H₈ 的烯烃（不含环烷烃）有几种？",["2 种","3 种","4 种","5 种"],1,
  "3 种：1-丁烯、2-丁烯、2-甲基丙烯（异丁烯）。若把 2-丁烯的顺反异构也算上则为 4 种，高考默认不算顺反时答 3。"),
 (2,"分子式 C₄H₈ 的同分异构体（含环烷烃）共几种？",["3 种","4 种","5 种","6 种"],2,
  "5 种：3 种烯烃 + 环丁烷 + 甲基环丙烷。烯烃与环烷烃互为官能团异构（类别异构）。"),
 (2,"C₄H₆ 的炔烃同分异构体有几种？",["1 种","2 种","3 种","4 种"],1,
  "2 种：1-丁炔、2-丁炔。三键不能在端位以外的支链位——炔烃没有碳链异构只有位置异构。"),
 (2,"C₅H₁₀ 的烯烃（不算顺反）有几种？",["4 种","5 种","6 种","7 种"],1,
  "5 种：1-戊烯、2-戊烯、2-甲基-1-丁烯、3-甲基-1-丁烯、2-甲基-2-丁烯。"),
 (2,"既能发生加成反应、又能使酸性 KMnO₄ 褪色的 C₄H₈ 有几种结构？",["1 种","2 种","3 种","4 种"],2,
  "3 种（1-丁烯、2-丁烯、异丁烯）。环烷烃虽同为 C₄H₈ 但不能加成、不能使 KMnO₄ 褪色，被性质排除。"),
 # ===== 苯环定位 =====
 (3,"苯的二氯代物有几种？",["2 种","3 种","4 种","6 种"],1,
  "3 种：邻位、间位、对位。苯环 6 个氢完全等效，第二个氯只有三种相对位置。"),
 (3,"分子式 C₈H₁₀ 的芳香烃有几种？",["2 种","3 种","4 种","5 种"],2,
  "4 种：乙苯、邻二甲苯、间二甲苯、对二甲苯。"),
 (3,"甲苯的一氯代物（苯环上 + 侧链上）共几种？",["3 种","4 种","5 种","6 种"],1,
  "4 种：苯环上邻、间、对 3 种 + 侧链甲基上 1 种（苄氯）。注意审题是否限定「苯环上」。"),
 (3,"苯的三氯代物有几种？",["3 种","4 种","5 种","6 种"],0,
  "3 种：1,2,3-（连）、1,2,4-（偏）、1,3,5-（均）。技巧：三氯代物 = 三氢代物，把未被取代的氢当取代基想。"),
 (3,"对二甲苯苯环上的一氯代物有几种？",["1 种","2 种","3 种","4 种"],0,
  "1 种。对二甲苯苯环上 4 个氢完全等效（高度对称）。比较：邻二甲苯 2 种、间二甲苯 3 种。"),
 # ===== 醇醚·羧酸与酯 =====
 (4,"分子式 C₄H₁₀O 的醇类有几种？",["2 种","3 种","4 种","5 种"],2,
  "4 种，等于丁基的种数：正丁醇、异丁醇（2-甲基-1-丙醇）、仲丁醇（2-丁醇）、叔丁醇。技巧：—OH 插在哪，就看丁基有几种。"),
 (4,"分子式 C₄H₁₀O 的醚类有几种？",["2 种","3 种","4 种","5 种"],1,
  "3 种：甲丙醚、甲异丙醚、乙醚。醚 = 两个烃基夹一个氧，注意甲乙醚与甲异丙醚不同。"),
 (4,"分子式 C₂H₆O 的两种同分异构体体现了哪种异构类型？",["碳链异构","位置异构","官能团异构","顺反异构"],2,
  "官能团异构：乙醇（CH₃CH₂OH，醇）与二甲醚（CH₃OCH₃，醚）。可用与 Na 是否反应鉴别。"),
 (4,"分子式 C₄H₈O₂ 的羧酸有几种？",["1 种","2 种","3 种","4 种"],1,
  "2 种：丁酸、2-甲基丙酸。羧基必在端位（—COOH 占一个碳），剩下丙基有 2 种。"),
 (4,"分子式 C₄H₈O₂ 的酯有几种？",["2 种","3 种","4 种","5 种"],2,
  "4 种：甲酸正丙酯、甲酸异丙酯、乙酸乙酯、丙酸甲酯。方法：按「酸的碳数」从 1 开始枚举，两边碳数之和=3。"),
 (4,"分子式 C₅H₁₀O₂ 的羧酸有几种？",["2 种","3 种","4 种","5 种"],2,
  "4 种：—COOH 占一个碳，剩余丁基有 4 种（正/异/仲/叔），即 4 种戊酸。"),
 (4,"分子式 C₅H₁₀O₂ 的酯有几种？",["5 种","7 种","9 种","10 种"],2,
  "9 种：甲酸丁酯 4 种（丁基 4）+ 乙酸丙酯 2 种（丙基 2）+ 丙酸乙酯 1 种 + 丁酸甲酯 2 种 = 9。"),
]

DATA = {"chapters": CHAPTERS, "qs": Q}

EXTRA_CSS = r"""
/* ===== 同分异构体闯关专用 ===== */
.iso-stage{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:24px;overflow:auto}
.iso-card{width:min(580px,94%);border:1px solid var(--line);border-radius:14px;padding:28px 32px;
 background:var(--paper);box-shadow:0 8px 30px rgba(0,0,0,.10)}
.iso-q{font-size:17px;font-family:var(--serif-cn);line-height:1.8;margin:10px 0 18px}
.iso-opt{display:block;width:100%;text-align:left;border:1px solid var(--line-strong);background:transparent;
 color:var(--ink);border-radius:8px;padding:11px 16px;font-size:14px;margin:8px 0;cursor:pointer;font-family:inherit;transition:all .15s}
.iso-opt:hover{border-color:var(--accent);color:var(--accent)}
.iso-opt.right{border-color:#2e7d4f;color:#2e7d4f;background:rgba(46,125,79,.08)}
.iso-opt.wrong{border-color:#c0392b;color:#c0392b;background:rgba(192,57,43,.08)}
.iso-exp{margin-top:12px;font-size:12.5px;line-height:1.9;color:var(--ink-dim);
 border-left:3px solid var(--accent);padding:6px 12px;background:var(--accent-soft)}
.lvl-item{display:flex;justify-content:space-between;align-items:center;padding:7px 9px;border-radius:5px;
 cursor:pointer;font-size:12.5px;border:1px solid transparent}
.lvl-item:hover{border-color:var(--line)}
.lvl-item.cur{border-color:var(--accent);color:var(--accent)}
.lvl-badge{font-size:11px;padding:1px 8px;border-radius:8px;border:1px solid var(--line-strong);color:var(--ink-mute)}
.lvl-badge.pass{border-color:#2e7d4f;color:#2e7d4f}
.iso-hud{display:flex;gap:14px;justify-content:center;font-size:12px;color:var(--ink-dim);margin-bottom:6px}
.iso-hud b{color:var(--accent);font-family:Georgia,serif;font-size:15px}
"""

BODY_JS = r"""
/* ===== 同分异构体闯关 ===== */
const D = window.__ISO__;
const $ = (id) => document.getElementById(id);
const LS = "chem-iso-progress-v1";
let prog = JSON.parse(localStorage.getItem(LS) || "{}");
const save = () => localStorage.setItem(LS, JSON.stringify(prog));
let ch = 0, qi = 0, rightCnt = 0, answered = false;

function chQs(c){ return D.qs.map((q,i)=>({...q,i})).filter(q => q[0] === c); }

function renderChapters(){
  const w = $("lvlList"); w.innerHTML = "";
  D.chapters.forEach((n,c) => {
    const p = prog[c];
    const total = chQs(c).length;
    const badge = p && p.done ? `<span class="lvl-badge pass">已通关 ${p.score}/${total}</span>`
      : p ? `<span class="lvl-badge">${p.score}/${total}</span>` : `<span class="lvl-badge">未开始</span>`;
    const d = document.createElement("div");
    d.className = "lvl-item" + (c===ch?" cur":"");
    d.innerHTML = `<span>第${"一二三四五"[c]}章 · ${n}</span>${badge}`;
    d.onclick = () => { ch = c; qi = 0; rightCnt = 0; renderChapters(); renderQ(); };
    w.appendChild(d);
  });
}

function renderQ(){
  answered = false;
  const list = chQs(ch);
  if (qi >= list.length) return renderSummary(list.length);
  const q = list[qi];
  $("stage").innerHTML = `
    <div class="iso-card">
      <div class="iso-hud"><span>第${"一二三四五"[ch]}章 · ${D.chapters[ch]}</span>
        <span>第 <b>${qi+1}</b> / ${list.length} 题</span><span>已对 <b>${rightCnt}</b></span></div>
      <div class="iso-q">${q[1]}</div>
      ${q[2].map((o,i) => `<button class="iso-opt" data-i="${i}">${String.fromCharCode(65+i)}. ${o}</button>`).join("")}
      <div id="exp"></div>
    </div>`;
  $("stage").querySelectorAll(".iso-opt").forEach(b => b.onclick = () => answer(q, +b.dataset.i, b));
}
function answer(q, pick, btn){
  if (answered) return; answered = true;
  const right = pick === q[3];
  if (right) rightCnt++;
  $("stage").querySelectorAll(".iso-opt").forEach(b => {
    if (+b.dataset.i === q[3]) b.classList.add("right");
    else if (b === btn) b.classList.add("wrong");
  });
  $("exp").innerHTML = `<div class="iso-exp">${right?"✓ 回答正确。":"✗ 正确答案：" + q[2][q[3]] + "。"}${q[4]}</div>`;
  setTimeout(() => { qi++; renderQ(); }, right ? 1600 : 3200);
}
function renderSummary(total){
  const pass = rightCnt / total >= 0.8;
  const old = prog[ch] || {score: 0, done: false};
  prog[ch] = {score: Math.max(old.score, rightCnt), done: old.done || pass};
  save(); renderChapters();
  $("stage").innerHTML = `
    <div class="iso-card" style="text-align:center">
      <div style="font-size:44px">${pass?"🏆":"📖"}</div>
      <div style="font-size:20px;font-family:var(--serif-cn);margin:10px 0">
        本章得分 ${rightCnt} / ${total}　${pass ? "通关！" : "未通关（需 ≥80%）"}</div>
      <p class="info-desc">${pass ? "可以去挑战下一章了。" : "建议看解析复盘后再来一轮，同分异构体数错一次就要补一次。"}</p>
      <button class="func-btn" id="btnAgain2" style="margin-top:8px">再来一轮</button>
    </div>`;
  $("btnAgain2").onclick = () => { qi = 0; rightCnt = 0; renderQ(); };
}

renderChapters(); renderQ();
"""

HTML = f"""<!DOCTYPE html>
<html lang="zh-CN" data-theme="washi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>同分异构体闯关 · 化学生活教学中心</title>
<style>{CSS}
{EXTRA_CSS}</style>
</head>
<body>
<nav class="topnav">
  <div class="brand">
    <span class="badge">构</span>
    <h1 style="white-space:nowrap">同分异构体闯关挑战</h1>
    <span class="lecture-tag">ORGANIC · LAB 03</span>
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
    <div class="panel-section">
      <div class="panel-title">关卡（正确率 ≥80% 通关）</div>
      <div id="lvlList"></div>
    </div>
    <div class="panel-section">
      <div class="panel-title">三大异构类型</div>
      <p class="info-desc">① 碳链异构：主链骨架不同（正/异/新戊烷）；<br>
      ② 位置异构：官能团位置不同（1-丁烯/2-丁烯）；<br>
      ③ 官能团异构：类别不同（乙醇/二甲醚、羧酸/酯、烯烃/环烷）。</p>
    </div>
    <div class="panel-section">
      <div class="panel-title">两大数法</div>
      <p class="info-desc">① 等效氢法：对称位置的氢等效，一氯代物种数 = 等效氢种数；<br>
      ② 定一议二法：二元取代先固定一个，再移动另一个，注意去重。</p>
    </div>
  </div>

  <div class="canvas-box" style="background:var(--bg-deep)">
    <div class="iso-stage" id="stage"></div>
  </div>

  <div class="side right-panel">
    <div class="panel-section">
      <div class="panel-title">常用结论速记</div>
      <p class="info-desc">
      烷烃异构数：C₄=2，C₅=3，C₆=5，C₇=9，C₈=18。<br><br>
      丁基 4 种 → 丁醇 4、丁基氯 4、戊酸 4；<br>
      丙基 2 种 → 丙醇 2、丁酸 2。<br><br>
      苯二取代 3 种（邻间对）；三取代 3 种（连偏均）。<br><br>
      酯按「酸的碳数」枚举：甲酸酯→醇基种类数……</p>
    </div>
  </div>
</div>

<script>window.__ISO__ = {json.dumps(DATA, ensure_ascii=False)};</script>
<script>{BODY_JS}</script>
<script>{THEME_JS}</script>
</body>
</html>
"""

open(OUT, "w", encoding="utf-8").write(HTML)
print("written:", OUT, len(HTML), "bytes,", len(Q), "questions")
