# -*- coding: utf-8 -*-
"""
生成 知识挑战树 chem_lab2.3.html
外壳提取自 chem_lab1.2.html；题库复用 build_flashcards.py 的 150 张卡；
10 条章节枝干 × 3 层（筑基/试炼/问鼎）= 30 个挑战节点 + 根节点；
答题自评（翻卡式），≥2/3 通过解锁下一层；XP/等级/连胜/成就 localStorage 持久化
"""
import json, re, importlib.util

LAB12 = r"C:\Users\风逝\Documents\kimi\tasks\2026-08-31\06-27-38-247a26cf\chem-life-main\public\teaching\chem_lab1.2.html"
OUT   = r"C:\Users\风逝\Documents\kimi\tasks\2026-08-31\06-27-38-247a26cf\chem-life-main\public\teaching\chem_lab2.3.html"

old = open(LAB12, encoding="utf-8").read()
CSS = re.search(r"<style>(.*?)</style>", old, re.S).group(1)
THEME_JS = re.search(r"/\* =+ 主题切换 washi / sumi / ai =+ \*/\s*\(function\(\)\{.*?\}\)\(\);", old, re.S).group(0)

# 复用闪卡题库
spec = importlib.util.spec_from_file_location("bf", r"build_flashcards.py")
bf = importlib.util.module_from_spec(spec); spec.loader.exec_module(bf)
CARDS, CHAPTERS, CH_BOOK = bf.C, bf.CHAPTERS, bf.CH_BOOK

SHORT = ["分类计量","离子反应","氧化还原","金属","非金属","周期律","能量电化","速率平衡","结构晶体","有机基础"]
TIER_NAME = ["筑基", "试炼", "问鼎"]

# 每章 15 卡按难度排序，切 5/5/5 三层
NODES = [{"id": 0, "br": -1, "tier": -1, "name": "高中化学", "q": []}]
for ch in range(10):
    pool = sorted([i for i, c in enumerate(CARDS) if c["ch"] == ch], key=lambda i: CARDS[i]["d"])
    for t in range(3):
        NODES.append({
            "id": len(NODES), "br": ch, "tier": t,
            "name": SHORT[ch] + " · " + TIER_NAME[t],
            "q": pool[t*5:(t+1)*5],
        })

DATA = {
    "cards": CARDS, "chapters": CHAPTERS, "books": CH_BOOK,
    "short": SHORT, "tiers": TIER_NAME, "nodes": NODES,
}

EXTRA_CSS = r"""
/* ===== 挑战树专用 ===== */
.kt-wrap{position:absolute;inset:0;overflow:auto;display:flex;align-items:center;justify-content:center}
.kt-svg{width:100%;height:100%;min-width:760px}
.kt-edge{fill:none;stroke:var(--line);stroke-width:2}
.kt-edge.on{stroke:var(--accent);stroke-width:2.5}
.kt-node{cursor:pointer}
.kt-node circle{stroke-width:2;transition:filter .2s}
.kt-node.locked circle{fill:var(--surface);stroke:var(--line)}
.kt-node.avail circle{fill:var(--accent);stroke:var(--accent);filter:drop-shadow(0 0 6px var(--accent))}
.kt-node.master circle{fill:#c89028;stroke:#c89028}
.kt-node text{fill:var(--ink);font-size:12px;text-anchor:center;font-family:inherit}
.kt-node.locked text{fill:var(--ink-mute)}
.kt-node.avail text{fill:var(--ink);font-weight:600}
.kt-node.master text{fill:var(--ink-dim)}
.kt-brlabel{fill:var(--ink-mute);font-size:11px;text-anchor:center;letter-spacing:2px}
.kt-root-t{fill:var(--accent);font-size:15px;font-weight:700;text-anchor:center;font-family:var(--serif-cn)}
.kt-xpbar{height:8px;border:1px solid var(--line);border-radius:4px;overflow:hidden;margin:6px 0 4px}
.kt-xpbar i{display:block;height:100%;background:var(--accent);transition:width .4s}
.kt-stat{display:flex;justify-content:space-between;font-size:12.5px;color:var(--ink-dim);padding:3px 0}
.kt-stat b{color:var(--ink);font-family:var(--mono)}
.kt-ach{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:6px}
.kt-ach span{font-size:11px;text-align:center;padding:6px 2px;border:1px solid var(--line);border-radius:6px;color:var(--ink-mute)}
.kt-ach span.got{border-color:var(--accent);color:var(--accent)}
.kt-q{font-size:14.5px;line-height:1.9;font-weight:600;color:var(--ink)}
.kt-a{font-size:13px;line-height:1.95;color:var(--ink-dim);border-top:1px dashed var(--line);margin-top:10px;padding-top:10px}
.kt-dots{display:flex;gap:6px;margin:8px 0}
.kt-dots i{width:9px;height:9px;border-radius:50%;border:1px solid var(--line)}
.kt-dots i.ok{background:#2e7d4f;border-color:#2e7d4f}
.kt-dots i.no{background:#c8102e;border-color:#c8102e}
.kt-btns{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap}
.kt-btn{border:1px solid var(--line);background:transparent;color:var(--ink);border-radius:6px;
 padding:7px 14px;font-size:12.5px;cursor:pointer;font-family:inherit}
.kt-btn:hover{border-color:var(--accent);color:var(--accent)}
.kt-btn.primary{background:var(--accent);border-color:var(--accent);color:#fff}
.kt-btn.primary:hover{opacity:.85;color:#fff}
.kt-msg{font-size:12px;color:var(--accent);margin-top:8px;min-height:18px}
.kt-meta{font-size:11px;color:var(--ink-mute);margin-bottom:8px}
"""

BODY_JS = r"""
/* ===== 知识挑战树 ===== */
const D = window.__KT__;
const $ = (id) => document.getElementById(id);
const SVGNS = "http://www.w3.org/2000/svg";
const KEY = "chem-kt-progress-v1";
let S = {mastered:[], xp:0, streak:0, best:0, seen:[], ach:[]};
try { const s = JSON.parse(localStorage.getItem(KEY)); if (s && s.mastered) S = s; } catch(e){}
const save = () => localStorage.setItem(KEY, JSON.stringify(S));

/* 布局 */
const VB_W = 1400, VB_H = 780;
const colX = i => 95 + i * 134;
const tierY = t => [540, 355, 175][t];
const pos = n => n.id === 0 ? {x: VB_W/2, y: 705} : {x: colX(n.br), y: tierY(n.tier)};

/* 状态判定 */
const isMaster = id => S.mastered.includes(id);
function isAvail(n){
  if (n.id === 0) return true;
  if (isMaster(n.id)) return false;
  if (n.tier === 0) return true;
  const pre = D.nodes.find(m => m.br === n.br && m.tier === n.tier - 1);
  return isMaster(pre.id);
}

/* 画树 */
function drawTree(){
  const svg = $("ktSvg"); svg.innerHTML = "";
  const mk = (tag, attrs) => { const e = document.createElementNS(SVGNS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]); return e; };
  // 枝干标签
  D.short.forEach((s, i) => {
    svg.appendChild(mk("text", {x: colX(i), y: 78, class: "kt-brlabel"})).textContent = s;
    const ln = mk("line", {x1: colX(i), y1: 92, x2: colX(i), y2: 118,
      stroke: "var(--line)", "stroke-width": 1});
    svg.appendChild(ln);
  });
  // 边
  for (const n of D.nodes){
    if (n.id === 0) continue;
    const pre = n.tier === 0 ? D.nodes[0] : D.nodes.find(m => m.br === n.br && m.tier === n.tier - 1);
    const a = pos(pre), b = pos(n);
    const p = mk("path", {class: "kt-edge" + (isMaster(n.id) ? " on" : ""),
      d: `M ${a.x} ${a.y} C ${a.x} ${(a.y+b.y)/2}, ${b.x} ${(a.y+b.y)/2}, ${b.x} ${b.y}`});
    svg.appendChild(p);
  }
  // 根节点
  const rp = pos(D.nodes[0]);
  svg.appendChild(mk("circle", {cx: rp.x, cy: rp.y, r: 26, fill: "var(--accent)", opacity: .15}));
  svg.appendChild(mk("circle", {cx: rp.x, cy: rp.y, r: 15, fill: "var(--accent)"}));
  svg.appendChild(mk("text", {x: rp.x, y: rp.y + 40, class: "kt-root-t"})).textContent = "高中化学";
  // 挑战节点
  for (const n of D.nodes){
    if (n.id === 0) continue;
    const st = isMaster(n.id) ? "master" : (isAvail(n) ? "avail" : "locked");
    const p = pos(n);
    const g = mk("g", {class: "kt-node " + st});
    g.appendChild(mk("circle", {cx: p.x, cy: p.y, r: st === "avail" ? 14 : 12}));
    const t = mk("text", {x: p.x, y: p.y - 20});
    t.textContent = TIER_MARK[n.tier] + " " + n.name.split(" · ")[1];
    g.appendChild(t);
    if (st === "master"){
      const ck = mk("text", {x: p.x, y: p.y + 4, "text-anchor": "middle",
        "font-size": 12, fill: "#fff"});
      ck.textContent = "✓"; g.appendChild(ck);
    }
    g.addEventListener("click", () => clickNode(n, st));
    svg.appendChild(g);
  }
}
const TIER_MARK = ["Ⅰ", "Ⅱ", "Ⅲ"];

/* 左栏统计 */
const ACHS = [
  ["初露锋芒", () => S.mastered.length >= 1],
  ["小有所成", () => S.mastered.length >= 5],
  ["半壁江山", () => S.mastered.length >= 15],
  ["登峰造极", () => S.mastered.length >= 30],
  ["十连胜",   () => S.best >= 10],
  ["一枝独秀", () => D.short.some((_, b) => [0,1,2].every(t => isMaster(D.nodes.find(m => m.br===b && m.tier===t).id)))],
  ["博览群书", () => S.seen.length >= 100],
  ["炉火纯青", () => level() >= 6],
];
function level(){ return Math.floor(S.xp / 120) + 1; }
function renderStats(){
  $("ktLv").textContent = level();
  $("ktXp").textContent = S.xp;
  $("ktXpBar").style.width = (S.xp % 120) / 120 * 100 + "%";
  $("ktStreak").textContent = S.streak;
  $("ktBest").textContent = S.best;
  $("ktMaster").textContent = S.mastered.length + " / 30";
  const box = $("ktAch"); box.innerHTML = "";
  ACHS.forEach(([name, fn]) => {
    const got = fn();
    if (got && !S.ach.includes(name)){ S.ach.push(name); save(); }
    const s = document.createElement("span");
    s.className = got ? "got" : ""; s.textContent = name;
    box.appendChild(s);
  });
}

/* 答题流程 */
let quiz = null; // {node, qs:[cardIdx], i, got:[]}
function clickNode(n, st){
  if (st === "locked"){
    $("ktMsg").textContent = "🔒 先通关本枝干的上一层节点再来挑战。";
    return;
  }
  startQuiz(n, st === "master");
}
function startQuiz(n, review){
  const qs = n.q.slice().sort(() => Math.random() - .5).slice(0, 3);
  quiz = {node: n, qs, i: 0, got: [], review};
  $("ktMsg").textContent = "";
  showQ();
}
function showQ(){
  const c = D.cards[quiz.qs[quiz.i]];
  if (!S.seen.includes(quiz.qs[quiz.i])){ S.seen.push(quiz.qs[quiz.i]); save(); }
  $("ktQuiz").innerHTML = `
    <div class="kt-meta">${quiz.node.name} · 第 ${quiz.i+1}/3 题 · ${D.books[c.ch]}《${D.chapters[c.ch]}》${quiz.review ? " · 复习模式" : ""}</div>
    <div class="kt-dots">${quiz.got.map(g => `<i class="${g ? "ok" : "no"}"></i>`).join("")}</div>
    <div class="kt-q">${c.f}</div>
    <div class="kt-btns"><button class="kt-btn primary" id="ktReveal">显示答案</button></div>`;
  $("ktReveal").onclick = () => {
    $("ktQuiz").innerHTML = `
      <div class="kt-meta">${quiz.node.name} · 第 ${quiz.i+1}/3 题</div>
      <div class="kt-dots">${quiz.got.map(g => `<i class="${g ? "ok" : "no"}"></i>`).join("")}</div>
      <div class="kt-q">${c.f}</div>
      <div class="kt-a">${c.b}</div>
      <div class="kt-btns">
        <button class="kt-btn primary" id="ktOk">✓ 答对了</button>
        <button class="kt-btn" id="ktNo">✗ 答错了</button>
      </div>`;
    $("ktOk").onclick = () => grade(true);
    $("ktNo").onclick = () => grade(false);
  };
}
function grade(ok){
  quiz.got.push(ok);
  const gain = ok ? (quiz.review ? 3 : 8) : 0;
  S.xp += gain;
  S.streak = ok ? S.streak + 1 : 0;
  if (S.streak > S.best) S.best = S.streak;
  quiz.i++;
  if (quiz.i < 3){ save(); renderStats(); showQ(); return; }
  // 结算
  const pass = quiz.got.filter(Boolean).length >= 2;
  const n = quiz.node;
  if (pass && !quiz.review && !isMaster(n.id)){
    S.mastered.push(n.id); S.xp += 25;
    reportScore('tree', S.mastered.length);
  }
  save(); renderStats(); drawTree();
  const acc = quiz.got.filter(Boolean).length;
  $("ktQuiz").innerHTML = `
    <div class="kt-meta">${n.name} · 挑战结束</div>
    <div class="kt-dots">${quiz.got.map(g => `<i class="${g ? "ok" : "no"}"></i>`).join("")}</div>
    <div class="kt-q" style="font-size:16px">${pass ? "🎉 通过！" : "😤 未通过（需 ≥2/3）"}</div>
    <div class="kt-a">答对 ${acc}/3${pass && !quiz.review ? "，节点已点亮，+25 XP 通关奖励" : ""}。</div>
    <div class="kt-btns">
      ${pass ? "" : `<button class="kt-btn primary" id="ktRetry">再挑战一次</button>`}
      <button class="kt-btn" id="ktBack">返回挑战树</button>
    </div>`;
  if (!pass) $("ktRetry").onclick = () => startQuiz(n, quiz.review);
  $("ktBack").onclick = renderWelcome;
  quiz = null;
}
function renderWelcome(){
  $("ktQuiz").innerHTML = `
    <div class="kt-q" style="font-size:15px">点击发光的节点开始挑战</div>
    <div class="kt-a">每条枝干 3 层：筑基 → 试炼 → 问鼎。每次挑战随机抽 3 题，自评对错，≥2 题答对即点亮节点并解锁下一层。金色节点可反复复习（XP 减半）。</div>`;
  $("ktMsg").textContent = "";
}

/* 成绩上报：登录状态下自动上传排行榜；失败进入离线队列，下次启动补传 */
const SCORE_Q = "chem-score-queue";
function reportScore(game, score){
  try {
    const t = localStorage.getItem('chem-token');
    if (!t) return;
    fetch('/api/forum', {method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({action: 'report', token: t, game, score})})
      .then(r => r.json()).then(r => { if (!r.ok) queueScore(game, score); })
      .catch(() => queueScore(game, score));
  } catch(e){ queueScore(game, score); }
}
function queueScore(game, score){
  try {
    const q = JSON.parse(localStorage.getItem(SCORE_Q) || '[]');
    q.push({game, score});
    localStorage.setItem(SCORE_Q, JSON.stringify(q.slice(-50)));
  } catch(e){}
}
function flushScoreQueue(){
  try {
    const t = localStorage.getItem('chem-token');
    const q = JSON.parse(localStorage.getItem(SCORE_Q) || '[]');
    if (!t || !q.length) return;
    localStorage.setItem(SCORE_Q, '[]');
    q.forEach(({game, score}) => reportScore(game, score));
  } catch(e){}
}
flushScoreQueue();

$("ktReset").onclick = () => {
  if (!confirm("清空挑战树全部进度（XP、连胜、成就）？")) return;
  S = {mastered:[], xp:0, streak:0, best:0, seen:[], ach:[]};
  save(); renderStats(); drawTree(); renderWelcome();
};

renderStats(); drawTree(); renderWelcome();
"""

HTML = f"""<!DOCTYPE html>
<html lang="zh-CN" data-theme="washi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>知识挑战树 · 化学生活教学中心</title>
<style>{CSS}
{EXTRA_CSS}</style>
</head>
<body>
<nav class="topnav">
  <div class="brand">
    <span class="badge">树</span>
    <h1 style="white-space:nowrap">知识挑战树</h1>
    <span class="lecture-tag">REVIEW · LAB 03</span>
  </div>
  <div class="nav-right">
    <a class="nav-btn" href="chem_lab2.1.html">知识地图 <span class="arr">→</span></a>
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
      <div class="panel-title">修炼档案</div>
      <div class="kt-stat"><span>等级</span><b>Lv.<span id="ktLv">1</span></b></div>
      <div class="kt-xpbar"><i id="ktXpBar"></i></div>
      <div class="kt-stat"><span>总 XP</span><b id="ktXp">0</b></div>
      <div class="kt-stat"><span>当前连胜</span><b id="ktStreak">0</b></div>
      <div class="kt-stat"><span>最高连胜</span><b id="ktBest">0</b></div>
      <div class="kt-stat"><span>点亮节点</span><b id="ktMaster">0 / 30</b></div>
    </div>
    <div class="panel-section">
      <div class="panel-title">成就</div>
      <div class="kt-ach" id="ktAch"></div>
    </div>
    <div class="panel-section">
      <div class="panel-title">操作</div>
      <button class="kt-btn" id="ktReset" style="width:100%">清空进度</button>
      <div class="kt-msg" id="ktMsg"></div>
    </div>
  </div>

  <div class="canvas-box" style="background:var(--bg-deep)">
    <div class="kt-wrap">
      <svg class="kt-svg" id="ktSvg" viewBox="0 0 1400 780" preserveAspectRatio="xMidYMid meet"></svg>
    </div>
  </div>

  <div class="side right-panel">
    <div class="panel-section">
      <div class="panel-title">挑战台</div>
      <div id="ktQuiz"></div>
    </div>
  </div>
</div>

<script>window.__KT__ = {json.dumps(DATA, ensure_ascii=False)};</script>
<script>{BODY_JS}</script>
<script>{THEME_JS}</script>
</body>
</html>
"""

open(OUT, "w", encoding="utf-8").write(HTML)
print("written:", OUT, len(HTML), "bytes,", len(NODES) - 1, "challenge nodes")
