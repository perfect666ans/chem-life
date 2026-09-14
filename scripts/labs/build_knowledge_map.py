# -*- coding: utf-8 -*-
"""
生成 知识球 · 知识地图 chem_lab2.1.html
Canvas 力导向图：约 55 个知识点节点（按教材分五色），边=前置→后续；
节点可拖拽、滚轮缩放、悬停高亮关联、点击看预习卡；搜索与教材筛选
"""
import json, re

LAB12 = r"C:\Users\风逝\Documents\kimi\tasks\2026-08-31\06-27-38-247a26cf\chem-life-main\public\teaching\chem_lab1.2.html"
OUT   = r"C:\Users\风逝\Documents\kimi\tasks\2026-08-31\06-27-38-247a26cf\chem-life-main\public\teaching\chem_lab2.1.html"

old = open(LAB12, encoding="utf-8").read()
CSS = re.search(r"<style>(.*?)</style>", old, re.S).group(1)
THEME_JS = re.search(r"/\* =+ 主题切换 washi / sumi / ai =+ \*/\s*\(function\(\)\{.*?\}\)\(\);", old, re.S).group(0)

BOOKS = ["必修一","必修二","选必1","选必2","选必3"]

# (名称, 书, 一句话预习卡, 母题提示, [前置])
N = []
def A(name, book, card, exam, pre=[]): N.append({"n":name,"b":book,"c":card,"e":exam,"p":pre})

# 必修一
A("物质的量",0,"n = m/M = N/Nᴀ = V/V_m = cV，四个公式互转是计算总开关","标况下气体体积与粒子数换算",[])
A("分散系与胶体",0,"1~100 nm 是胶体；丁达尔效应是最快鉴别","Fe(OH)₃ 胶体制备与聚沉",[])
A("电解质与非电解质",0,"看「自身能否电离」：CO₂、NH₃ 是非电解质；单质混合物两边都不是","判断给定物质类别",[])
A("离子反应与方程式",0,"拆：强酸强碱可溶性盐；查：事实、守恒（原子+电荷）","少量/过量 CO₂ 通入碱液",["电解质与非电解质"])
A("离子共存",0,"沉淀、气体、弱电解质、氧化还原——四大不共存","酸性/无色等隐含条件",["离子反应与方程式"])
A("氧化还原反应",0,"升失氧、降得还；本质是电子转移","双线桥分析",["物质的量"])
A("氧化剂与还原剂",0,"氧化性：氧化剂>氧化产物；常见强氧化剂/还原剂清单要背","强弱比较与先后反应",["氧化还原反应"])
A("钠及其化合物",0,"Na 与水五现象；Na₂O₂ 歧化供氧；Na₂CO₃/NaHCO₃ 对比","Na₂O₂ 与 CO₂/H₂O 计算",["氧化还原反应"])
A("铝及其化合物",0,"Al、Al₂O₃、Al(OH)₃ 两性；铝热反应","Al³⁺ 与 OH⁻ 分步图像",["离子反应与方程式"])
A("铁及其化合物",0,"Fe²⁺/Fe³⁺ 检验与转化；Fe(OH)₂ 变色三连","保存 FeSO₄ 的措施",["氧化剂与还原剂"])
A("氯及其化合物",0,"氯水三分四离；HClO 漂白不可逆","氯气制备与净化流程",["氧化还原反应"])
A("硫及其化合物",0,"SO₂ 漂白可逆（对比 HClO）；浓硫酸三特性","SO₂ 与 CO₂ 鉴别",["氧化还原反应"])
A("氮及其化合物",0,"NH₃ 喷泉+制法；硝酸强氧化性（浓 NO₂ 稀 NO）","喷泉实验与氨水计算",["氧化还原反应"])
A("硅及其化合物",0,"SiO₂ 与 HF/NaOH 两个特殊反应；硅酸盐材料","试剂瓶塞选择",[])
# 必修二
A("原子结构",1,"ᴬzX：质量数=质子+中子；同位素、同素异形体分清","粒子中质子/中子/电子计数",[])
A("元素周期律",1,"同周期左→右金属性减弱；同主族上→下金属性增强","金属性/非金属性判据选择",["原子结构"])
A("元素周期表",1,"7 周期 16 族 18 列；定位=周期+族","由位置推性质",["元素周期律"])
A("化学键",1,"离子键 vs 共价键；离子化合物一定含离子键","AlCl₃ 等特殊判断",["原子结构"])
A("化学反应与能量变化",1,"断键吸热成键放热；放热≠需要点燃","由能量图判 ΔH 正负",["化学键"])
A("原电池",1,"负氧正还；电子负→正，阳离子→正极","电极方程式书写",["氧化还原反应","化学反应与能量变化"])
A("化学反应速率",1,"v=Δc/Δt；速率之比=系数之比；四因素影响","固体纯液体不表示速率",["物质的量"])
A("化学平衡基础",1,"v正=v逆、变量不变即平衡","平衡标志判断",["化学反应速率"])
A("甲烷与烷烃",1,"取代反应光照逐步，产物是混合物","取代产物种数",["化学键"])
A("乙烯与加成",1,"双键 1σ+1π；加成使溴水褪色","与取代反应的条件对比",["甲烷与烷烃"])
A("苯及其同系物",1,"特殊大 π 键：易取代难加成","邻二甲苯一种结构说明什么",["乙烯与加成"])
A("乙醇与乙酸",1,"乙醇四反应；酯化=酸脱羟基醇脱氢","酯化实验装置与 Na₂CO₃ 作用",["苯及其同系物"])
A("基本营养物质",1,"糖/油脂/蛋白质的水解与特征反应","淀粉水解程度检验",["乙醇与乙酸"])
# 选必1
A("反应热与焓变",2,"ΔH=生成物−反应物=断键−成键；热化学方程式四要点","由键能算 ΔH",["化学反应与能量变化"])
A("盖斯定律",2,"反应热只与始末态有关，方程加减对应 ΔH 加减","多步合成路径计算",["反应热与焓变"])
A("化学平衡常数",2,"K 只随温度变；固液不写入；Q 与 K 定方向","三段式计算",["化学平衡基础"])
A("平衡移动原理",2,"勒夏特列：减弱而不抵消；催化剂不移动平衡","图像题（T、p、浓度）",["化学平衡常数"])
A("弱电解质的电离",2,"部分电离可逆；多元弱酸分步；稀释促进电离但浓度反降","导电能力变化曲线",["化学平衡基础"])
A("水的电离与 pH",2,"Kw=10⁻¹⁴(25℃)；酸抑制碱抑制、水解盐促进","pH 速算与混合",["弱电解质的电离"])
A("盐类的水解",2,"有弱才水解、谁强显谁性；三大守恒是压轴工具","粒子浓度大小排序",["水的电离与 pH"])
A("沉淀溶解平衡",2,"Ksp 比较看类型；沉淀向更难溶转化","Ksp 计算与沉淀转化",["盐类的水解"])
A("电解池",2,"阳氧阴还；放电顺序表；电镀三要素","电解产物判断与计算",["原电池"])
A("金属的腐蚀与防护",2,"吸氧腐蚀更普遍；牺牲阳极、外加电流","铁锈形成过程分析",["电解池"])
# 选必2
A("能级与电子排布",3,"构造原理+泡利+洪特；Cr/Cu 特例","排布式与排布图",["原子结构"])
A("电离能与电负性",3,"ⅡA>ⅢA、ⅤA>ⅥA 两个反常；差 1.7 判键型","由电离能突变推族",["能级与电子排布"])
A("VSEPR 模型",3,"价层电子对=σ+孤对；4/3/2 对对应三类构型","分子构型判断",["能级与电子排布"])
A("杂化轨道",3,"sp³/sp²/sp 与构型一一对应","有机物中碳的杂化判断",["VSEPR 模型"])
A("分子极性与氢键",3,"对称则非极性；氢键使 HF/H₂O/NH₃ 沸点反常","溶解性与相似相溶",["杂化轨道"])
A("晶体类型判断",3,"共价>离子>分子（熔沸点一般规律）；金属晶体差异大","熔沸点排序",["化学键"])
A("晶胞计算",3,"均摊法：顶点1/8 棱1/4 面1/2 体1","密度与配位数计算",["晶体类型判断"])
# 选必3
A("官能团与同系物",4,"结构相似、差 n 个 CH₂ 为同系物","官能团识别",["化学键"])
A("同分异构体",4,"碳链/位置/官能团三类；等效氢+定一议二","限定条件数异构体",["官能团与同系物"])
A("有机命名",4,"选主链→编号→书写；甲基在前","键线式命名",["同分异构体"])
A("卤代烃",4,"水解要水溶液、消去要醇溶液","双路径条件辨析",["官能团与同系物"])
A("醇与酚",4,"醇：Na/氧化/消去/酯化；酚：弱酸+FeCl₃ 显色+浓溴水","醇酚鉴别",["卤代烃"])
A("醛与酮",4,"银镜+斐林检验醛基；加成还原成醇","银镜方程式配平",["醇与酚"])
A("羧酸与酯",4,"酯化机理¹⁸O 示踪；酯的水解（酸/碱）","合成路线设计",["醛与酮"])
A("高分子化合物",4,"加聚无双键残留、缩聚脱小分子；单体反推","由聚合物写单体",["羧酸与酯"])

DATA = {"books": BOOKS, "nodes": N}

EXTRA_CSS = r"""
/* ===== 知识地图专用 ===== */
.km-wrap{position:absolute;inset:0}
#kmCanvas{width:100%;height:100%;display:block;cursor:grab}
.km-card h3{margin:0 0 4px;font-family:var(--serif-cn);font-size:18px;color:var(--accent)}
.km-book{font-size:11px;color:var(--ink-mute)}
.km-sec{margin-top:10px;font-size:12.5px;line-height:1.9;color:var(--ink-dim)}
.km-sec b{color:var(--ink)}
.km-rel{margin-top:8px;font-size:11.5px;color:var(--ink-mute);line-height:1.8}
.bk-item{display:flex;align-items:center;gap:7px;font-size:12.5px;padding:4px 6px;border-radius:4px;cursor:pointer;color:var(--ink-dim)}
.bk-item i{width:10px;height:10px;border-radius:50%;flex:none}
.bk-item.off{opacity:.35}
.km-search{width:100%;padding:6px 10px;border:1px solid var(--line);border-radius:4px;
 background:transparent;color:var(--ink);font-size:12.5px;font-family:inherit}
"""

BODY_JS = r"""
/* ===== 知识球 · 知识地图（Canvas 力导向） ===== */
const D = window.__KM__;
const $ = (id) => document.getElementById(id);
const COLORS = ["#c8102e","#2a5d9f","#2e7d4f","#c89028","#7a4fb0"];
const idx = {}; D.nodes.forEach((n,i) => idx[n.n] = i);
const edges = [];
D.nodes.forEach((n,i) => n.p.forEach(p => { if (idx[p] !== undefined) edges.push([idx[p], i]); }));

/* 初始化位置：按书分簇 */
const nodes = D.nodes.map((n,i) => ({
  ...n, i,
  x: Math.cos(n.b/5*Math.PI*2)*140 + (Math.random()-.5)*80,
  y: Math.sin(n.b/5*Math.PI*2)*140 + (Math.random()-.5)*80,
  vx: 0, vy: 0,
}));
let camX = 0, camY = 0, zoom = 1, sel = -1, hover = -1;
let dragNode = null, dragCam = null;
let bookOn = [true,true,true,true,true];
let keyword = "";

/* 力学模拟 */
function physics(){
  for (let i = 0; i < nodes.length; i++){
    const a = nodes[i];
    for (let j = i+1; j < nodes.length; j++){
      const b = nodes[j];
      let dx = a.x-b.x, dy = a.y-b.y;
      let d2 = dx*dx+dy*dy; if (d2 < 1) d2 = 1;
      const f = 2600/d2;
      dx /= Math.sqrt(d2); dy /= Math.sqrt(d2);
      a.vx += dx*f*0.01; a.vy += dy*f*0.01;
      b.vx -= dx*f*0.01; b.vy -= dy*f*0.01;
    }
  }
  for (const [s,t] of edges){
    const a = nodes[s], b = nodes[t];
    let dx = b.x-a.x, dy = b.y-a.y;
    const d = Math.hypot(dx,dy)||1;
    const f = (d-85)*0.006;
    a.vx += dx*f/d*d*0.01+dx*f*0.05; a.vy += dy*f/d*d*0.01+dy*f*0.05;
    b.vx -= dx*f/d*d*0.01+dx*f*0.05; b.vy -= dy*f/d*d*0.01+dy*f*0.05;
  }
  for (const n of nodes){ n.vx *= 0.82; n.vy *= 0.82; n.x += n.vx; n.y += n.vy; }
}

function visible(n){
  if (!bookOn[n.b]) return false;
  if (keyword && !n.n.includes(keyword)) return false;
  return true;
}

function draw(){
  const c = $("kmCanvas"); const box = c.parentElement.getBoundingClientRect();
  const dpr = window.devicePixelRatio||1;
  if (c.width !== box.width*dpr){ c.width = box.width*dpr; c.height = box.height*dpr; }
  const ctx = c.getContext("2d"); ctx.setTransform(dpr,0,0,dpr,0,0);
  const W = box.width, H = box.height;
  ctx.clearRect(0,0,W,H);
  const cs = getComputedStyle(document.body);
  const ink = cs.getPropertyValue("--ink").trim()||"#999";
  const X = x => W/2 + (x-camX)*zoom, Y = y => H/2 + (y-camY)*zoom;
  // 关联高亮集
  const rel = new Set();
  if (sel >= 0 || hover >= 0){
    const k = sel >= 0 ? sel : hover;
    rel.add(k);
    edges.forEach(([s,t]) => { if (s===k) rel.add(t); if (t===k) rel.add(s); });
  }
  // 边
  for (const [s,t] of edges){
    const a = nodes[s], b = nodes[t];
    if (!visible(a) || !visible(b)) continue;
    const hot = rel.size && rel.has(s) && rel.has(t) && (s===sel||t===sel||s===hover||t===hover);
    ctx.strokeStyle = hot ? "#c8102e" : ink;
    ctx.globalAlpha = hot ? 0.9 : (rel.size ? 0.12 : 0.3);
    ctx.lineWidth = hot ? 2 : 1;
    ctx.beginPath(); ctx.moveTo(X(a.x), Y(a.y)); ctx.lineTo(X(b.x), Y(b.y)); ctx.stroke();
    // 箭头（前置→后续）
    const mx = (X(a.x)+X(b.x))/2, my = (Y(a.y)+Y(b.y))/2;
    const ang = Math.atan2(Y(b.y)-Y(a.y), X(b.x)-X(a.x));
    ctx.fillStyle = ctx.strokeStyle;
    ctx.beginPath(); ctx.moveTo(mx+7*Math.cos(ang)*zoom, my+7*Math.sin(ang)*zoom);
    ctx.lineTo(mx-3*Math.cos(ang-0.5)*zoom, my-3*Math.sin(ang-0.5)*zoom);
    ctx.lineTo(mx-3*Math.cos(ang+0.5)*zoom, my-3*Math.sin(ang+0.5)*zoom);
    ctx.fill();
  }
  ctx.globalAlpha = 1; ctx.lineWidth = 1;
  // 节点（标签碰撞避让：选中/悬停/关联节点始终显示，其余重叠时隐藏）
  ctx.textAlign = "center";
  const placed = [];
  const labelOK = (x, y, w, h) => {
    for (const p of placed){
      if (Math.abs(p.x - x) < (p.w + w) / 2 && Math.abs(p.y - y) < (p.h + h) / 2) return false;
    }
    return true;
  };
  // 第一遍：优先画关键节点标签
  const priority = new Set();
  if (sel >= 0) priority.add(sel);
  if (hover >= 0) priority.add(hover);
  rel.forEach(i => priority.add(i));
  for (const pass of [true, false]){
    for (const n of nodes){
      if (!visible(n)) continue;
      const isPri = priority.has(n.i);
      if (pass !== isPri) continue;
      const r = (n.i===sel ? 13 : 10) * zoom;
      const dim = rel.size && !rel.has(n.i);
      ctx.globalAlpha = dim ? 0.18 : 1;
      if (pass){ // 关键节点的圆点在第二遍统一画之前先画，避免漏
      }
      ctx.beginPath(); ctx.arc(X(n.x), Y(n.y), r, 0, 7);
      ctx.fillStyle = COLORS[n.b]; ctx.fill();
      ctx.beginPath(); ctx.arc(X(n.x)-r*0.3, Y(n.y)-r*0.3, r*0.3, 0, 7);
      ctx.fillStyle = "rgba(255,255,255,.35)"; ctx.fill();
      const fs = Math.max(10, 11*zoom);
      ctx.font = `${fs}px "Noto Sans SC",sans-serif`;
      const lx = X(n.x), ly = Y(n.y) + r + 13*zoom;
      const lw = ctx.measureText(n.n).width + 6, lh = fs + 6;
      if (isPri || labelOK(lx, ly, lw, lh)){
        ctx.fillStyle = ink;
        ctx.fillText(n.n, lx, ly);
        placed.push({x: lx, y: ly, w: lw, h: lh});
      }
      ctx.globalAlpha = 1;
    }
  }
  window.__KM_POS = {X, Y, zoom};
}

function frame(){ physics(); draw(); requestAnimationFrame(frame); }

/* 交互 */
function toWorld(e){
  const r = $("kmCanvas").getBoundingClientRect();
  const px = e.clientX - r.left, py = e.clientY - r.top;
  return {wx: (px - r.width/2)/zoom + camX, wy: (py - r.height/2)/zoom + camY, px, py};
}
function pick(e){
  const {wx, wy} = toWorld(e);
  let best = -1, bd = 1e9;
  nodes.forEach(n => {
    if (!visible(n)) return;
    const d = Math.hypot(n.x-wx, n.y-wy);
    if (d < 14 && d < bd){ bd = d; best = n.i; }
  });
  return best;
}
$("kmCanvas").addEventListener("mousedown", e => {
  const k = pick(e);
  if (k >= 0){ dragNode = nodes[k]; sel = k; renderCard(); }
  else dragCam = {x: e.clientX, y: e.clientY, camX, camY};
});
window.addEventListener("mousemove", e => {
  if (dragNode){ const {wx,wy} = toWorld(e); dragNode.x = wx; dragNode.y = wy; dragNode.vx = dragNode.vy = 0; }
  else if (dragCam){ camX = dragCam.camX - (e.clientX-dragCam.x)/zoom; camY = dragCam.camY - (e.clientY-dragCam.y)/zoom; }
  else hover = pick(e);
});
window.addEventListener("mouseup", () => { dragNode = null; dragCam = null; });
$("kmCanvas").addEventListener("wheel", e => {
  e.preventDefault();
  zoom = Math.min(3, Math.max(0.4, zoom * (e.deltaY < 0 ? 1.12 : 0.89)));
}, {passive:false});

function renderCard(){
  const n = nodes[sel];
  if (!n) return;
  const pres = n.p.join("、") || "无（起点知识）";
  const nxts = D.nodes.filter(m => m.p.includes(n.n)).map(m => m.n).join("、") || "无（顶端知识）";
  $("kmCard").innerHTML = `
    <h3>${n.n}</h3><div class="km-book">${D.books[n.b]}</div>
    <div class="km-sec"><b>预习卡：</b>${n.c}</div>
    <div class="km-sec"><b>母题方向：</b>${n.e}</div>
    <div class="km-rel">前置：${pres}<br>后续：${nxts}</div>`;
}

/* 筛选与搜索 */
function renderBooks(){
  $("bkList").innerHTML = "";
  D.books.forEach((b,i) => {
    const d = document.createElement("div");
    d.className = "bk-item" + (bookOn[i]?"":" off");
    d.innerHTML = `<i style="background:${COLORS[i]}"></i>${b}（${D.nodes.filter(n=>n.b===i).length}）`;
    d.onclick = () => { bookOn[i] = !bookOn[i]; renderBooks(); };
    $("bkList").appendChild(d);
  });
}
$("kmSearch").oninput = e => { keyword = e.target.value.trim(); };

renderBooks();
renderCard && null;
$("kmCard").innerHTML = `<h3>点击任意知识球</h3><div class="km-sec">拖动节点整理网络，滚轮缩放，点空白拖动平移。箭头方向 = 建议学习顺序（前置 → 后续）。</div>`;
frame();
"""

HTML = f"""<!DOCTYPE html>
<html lang="zh-CN" data-theme="washi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>知识球 · 知识地图 · 化学生活教学中心</title>
<style>{CSS}
{EXTRA_CSS}</style>
</head>
<body>
<nav class="topnav">
  <div class="brand">
    <span class="badge">图</span>
    <h1 style="white-space:nowrap">知识球 · 知识地图</h1>
    <span class="lecture-tag">REVIEW · LAB 01</span>
  </div>
  <div class="nav-right">
    <a class="nav-btn" href="chem_lab2.2.html">闪卡复习 <span class="arr">→</span></a>
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
      <div class="panel-title">教材筛选</div>
      <div id="bkList"></div>
    </div>
    <div class="panel-section">
      <div class="panel-title">搜索知识点</div>
      <input class="km-search" id="kmSearch" placeholder="如：水解 / 原电池 / 命名">
    </div>
    <div class="panel-section">
      <div class="panel-title">使用说明</div>
      <p class="info-desc">每个球是一个知识点，颜色代表教材分册；箭头表示「先学 → 后学」。点球看预习卡与母题方向，悬停可高亮它的关联知识。</p>
    </div>
  </div>

  <div class="canvas-box" style="background:var(--bg-deep)">
    <div class="km-wrap"><canvas id="kmCanvas"></canvas></div>
  </div>

  <div class="side right-panel">
    <div class="panel-section km-card" id="kmCard"></div>
  </div>
</div>

<script>window.__KM__ = {json.dumps(DATA, ensure_ascii=False)};</script>
<script>{BODY_JS}</script>
<script>{THEME_JS}</script>
</body>
</html>
"""

open(OUT, "w", encoding="utf-8").write(HTML)
print("written:", OUT, len(HTML), "bytes,", len(N), "nodes,", sum(len(n["p"]) for n in N), "edges")
