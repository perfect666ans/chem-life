# -*- coding: utf-8 -*-
"""
生成 元素纪元 RPG chem_lab5.1.html
外壳提取自 chem_lab1.2.html；回合制对战：程序化生成氧化还原选择题（真实判分），
答对攻击 / 答错受击；元素精灵捕捉图鉴；等级 XP 连胜 localStorage 持久化
"""
import json, re

LAB12 = r"C:\Users\风逝\Documents\kimi\tasks\2026-08-31\06-27-38-247a26cf\chem-life-main\public\teaching\chem_lab1.2.html"
OUT   = r"C:\Users\风逝\Documents\kimi\tasks\2026-08-31\06-27-38-247a26cf\chem-life-main\public\teaching\chem_lab5.1.html"

old = open(LAB12, encoding="utf-8").read()
CSS = re.search(r"<style>(.*?)</style>", old, re.S).group(1)
THEME_JS = re.search(r"/\* =+ 主题切换 washi / sumi / ai =+ \*/\s*\(function\(\)\{.*?\}\)\(\);", old, re.S).group(0)

# ===== 元素精灵 =====
# (符号, 中文名, 颜色, 一句话设定)
SPIRITS = [
 ["H","氢","#7ec8e3","最轻的精灵，爆炸是它的问候"],
 ["He","氦","#d9c8f5","什么都不理的懒精灵"],
 ["C","碳","#555555","有机世界的骨架大师"],
 ["N","氮","#5b8ff0","空气里的沉默大多数"],
 ["O","氧","#e0635c","燃烧与呼吸的幕后推手"],
 ["F","氟","#8fd14f","氧化性强到没有朋友"],
 ["Na","钠","#f2c94c","遇水就炸的暴躁小黄"],
 ["Mg","镁","#c0c8d0","一点火就耀眼的闪光弹"],
 ["Al","铝","#a8b8c8","地壳含量第一的金属"],
 ["Si","硅","#d8a86a","芯片与沙子的共同灵魂"],
 ["P","磷","#f0e6d2","暗夜里会发光的骨头"],
 ["S","硫","#f5d90a","火山口的味道担当"],
 ["Cl","氯","#b8e04a","泳池消毒水的气味来源"],
 ["K","钾","#c9a0f0","比钠还暴躁的紫焰舞者"],
 ["Ca","钙","#e8e0d0","骨骼与石灰岩的基石"],
 ["Fe","铁","#b07050","会生锈的工业脊梁"],
 ["Cu","铜","#e08040","人类最早驯服的金属"],
 ["Zn","锌","#90a8b8","牺牲自己保护钢铁"],
 ["Br","溴","#a04030","唯一的液态非金属"],
 ["I","碘","#7040a0","升华时紫烟缭绕"],
]

# ===== 化合价题库（程序化出题用） =====
# (化学式, 元素, 化合价, 解析)
OXSTATE = [
 ["KMnO₄","Mn","+7","K +1、O −2，设 Mn 为 x：+1+x+(−8)=0，x=+7"],
 ["MnO₂","Mn","+4","x+2×(−2)=0，x=+4"],
 ["K₂MnO₄","Mn","+6","2×(+1)+x+(−8)=0，x=+6"],
 ["K₂Cr₂O₇","Cr","+6","2×(+1)+2x+7×(−2)=0，x=+6"],
 ["CrCl₃","Cr","+3","Cl −1，x+3×(−1)=0，x=+3"],
 ["HNO₃","N","+5","+1+x+3×(−2)=0，x=+5"],
 ["NO₂","N","+4","x+2×(−2)=0，x=+4"],
 ["NO","N","+2","x+(−2)=0，x=+2"],
 ["N₂O","N","+1","2x+(−2)=0，x=+1"],
 ["NH₃","N","−3","x+3×(+1)=0，x=−3"],
 ["H₂SO₄","S","+6","2×(+1)+x+4×(−2)=0，x=+6"],
 ["SO₂","S","+4","x+2×(−2)=0，x=+4"],
 ["H₂S","S","−2","2×(+1)+x=0，x=−2"],
 ["Na₂S₂O₃","S","+2","平均价：2×(+1)+2x+3×(−2)=0，x=+2"],
 ["H₂O₂","O","−1","过氧根中 O 为 −1 价"],
 ["OF₂","O","+2","F 恒为 −1，O 为 +2（唯一 O 显正价的常见物）"],
 ["Fe₃O₄","Fe","+8/3","平均价：3x+4×(−2)=0，x=+8/3（可看作 FeO·Fe₂O₃）"],
 ["FeCl₂","Fe","+2","x+2×(−1)=0，x=+2"],
 ["KClO₃","Cl","+5","+1+x+3×(−2)=0，x=+5"],
 ["HClO","Cl","+1","+1+x+(−2)=0，x=+1"],
 ["HClO₄","Cl","+7","+1+x+4×(−2)=0，x=+7"],
 ["NaH","H","−1","金属氢化物中 H 为 −1 价"],
 ["CaH₂","H","−1","Ca +2，每个 H 为 −1 价"],
 ["CO","C","+2","x+(−2)=0，x=+2"],
 ["CH₄","C","−4","x+4×(+1)=0，x=−4"],
 ["CH₃OH","C","−2","x+4×(+1)+(−2)=0，x=−2"],
 ["H₂C₂O₄","C","+3","2×(+1)+2x+4×(−2)=0，x=+3"],
 ["Cu₂O","Cu","+1","2x+(−2)=0，x=+1"],
 ["CO₂","C","+4","x+2×(−2)=0，x=+4"],
 ["HCHO","C","0","x+2×(+1)+(−2)=0，x=0"],
]

# ===== 氧化还原反应题库 =====
# (方程式, 氧化剂, 还原剂, 1 mol 氧化剂得电子 mol, 备注)
REDOX = [
 ["Cl₂ + 2NaBr = 2NaCl + Br₂","Cl₂","NaBr","2","氯水置换溴"],
 ["2Na + Cl₂ =点燃= 2NaCl","Cl₂","Na","2","钠在氯气中燃烧"],
 ["Cu + 2FeCl₃ = CuCl₂ + 2FeCl₂","FeCl₃","Cu","1","Fe³⁺ 氧化铜（腐蚀电路板）"],
 ["Zn + CuSO₄ = ZnSO₄ + Cu","CuSO₄","Zn","2","湿法炼铜"],
 ["MnO₂ + 4HCl(浓) =△= MnCl₂ + Cl₂↑ + 2H₂O","MnO₂","HCl","2","实验室制氯气"],
 ["2H₂O₂ =MnO₂= 2H₂O + O₂↑","H₂O₂","H₂O₂","1","歧化反应：H₂O₂ 既是氧化剂又是还原剂"],
 ["Cl₂ + H₂O ⇌ HCl + HClO","Cl₂","Cl₂","1","歧化反应：Cl₂ 一歧为二"],
 ["3NO₂ + H₂O = 2HNO₃ + NO","NO₂","NO₂","2","歧化反应：2 升 1 降"],
 ["2Na₂O₂ + 2CO₂ = 2Na₂CO₃ + O₂","Na₂O₂","Na₂O₂","1","供氧剂原理，歧化"],
 ["Fe + 2HCl = FeCl₂ + H₂↑","HCl","Fe","1","活泼金属置换氢气"],
 ["2Al + Fe₂O₃ =高温= 2Fe + Al₂O₃","Fe₂O₃","Al","6","铝热反应，焊接钢轨"],
 ["3Cu + 8HNO₃(稀) = 3Cu(NO₃)₂ + 2NO↑ + 4H₂O","HNO₃","Cu","3","稀硝酸被还原为 NO"],
 ["C + 2H₂SO₄(浓) =△= CO₂↑ + 2SO₂↑ + 2H₂O","H₂SO₄","C","2","浓硫酸的强氧化性"],
 ["2FeCl₂ + Cl₂ = 2FeCl₃","Cl₂","FeCl₂","2","Fe²⁺ 被氯气氧化"],
 ["H₂ + CuO =△= Cu + H₂O","CuO","H₂","2","氢气还原氧化铜"],
 ["2Mg + CO₂ =点燃= 2MgO + C","CO₂","Mg","4","镁在二氧化碳中也能燃烧"],
]

# ===== 氧化性/还原性强弱链（强 → 弱） =====
CHAINS = [
 {"type":"氧化性","items":["KMnO₄(H⁺)","Cl₂","Br₂","Fe³⁺","I₂","S"]},
 {"type":"氧化性","items":["浓HNO₃","稀HNO₃","浓H₂SO₄","Fe³⁺","Cu²⁺","H⁺"]},
 {"type":"还原性","items":["S²⁻","I⁻","Fe²⁺","Br⁻","Cl⁻","F⁻"]},
 {"type":"还原性","items":["K","Na","Mg","Al","Zn","Fe","H₂","Cu"]},
]

DATA = {"spirits": SPIRITS, "oxstate": OXSTATE, "redox": REDOX, "chains": CHAINS}

EXTRA_CSS = r"""
/* ===== RPG 专用 ===== */
.rpg-wrap{position:absolute;inset:0}
#rpgCanvas{width:100%;height:100%;display:block}
.rpg-q{font-size:14px;line-height:1.9;font-weight:600;color:var(--ink)}
.rpg-eq{font-family:var(--mono);font-size:13.5px;background:color-mix(in srgb,var(--accent) 8%,transparent);
 border-left:3px solid var(--accent);padding:8px 10px;margin:8px 0;line-height:1.7}
.rpg-opts{display:flex;flex-direction:column;gap:7px;margin-top:10px}
.rpg-opt{border:1px solid var(--line);background:transparent;color:var(--ink);border-radius:6px;
 padding:8px 12px;font-size:13px;cursor:pointer;font-family:inherit;text-align:left;line-height:1.6}
.rpg-opt:hover{border-color:var(--accent);color:var(--accent)}
.rpg-opt.right{border-color:#2e7d4f;color:#2e7d4f;background:color-mix(in srgb,#2e7d4f 10%,transparent)}
.rpg-opt.wrong{border-color:#c8102e;color:#c8102e;background:color-mix(in srgb,#c8102e 10%,transparent)}
.rpg-log{margin-top:10px;font-size:11.5px;line-height:1.9;color:var(--ink-dim);max-height:150px;overflow:auto;
 border-top:1px dashed var(--line);padding-top:8px}
.rpg-log b{color:var(--accent)}
.rpg-dex{display:grid;grid-template-columns:repeat(5,1fr);gap:5px;margin-top:6px}
.rpg-dex span{font-size:11px;text-align:center;padding:5px 1px;border:1px solid var(--line);border-radius:5px;
 color:var(--ink-mute);opacity:.45}
.rpg-dex span.got{opacity:1;border-color:var(--accent);color:var(--ink);font-weight:600}
.rpg-stat{display:flex;justify-content:space-between;font-size:12.5px;color:var(--ink-dim);padding:3px 0}
.rpg-stat b{color:var(--ink);font-family:var(--mono)}
.rpg-hpbar{height:8px;border:1px solid var(--line);border-radius:4px;overflow:hidden;margin:4px 0 6px}
.rpg-hpbar i{display:block;height:100%;background:#c8102e;transition:width .3s}
.rpg-xpbar i{background:var(--accent)}
.rpg-act{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap}
.rpg-btn{border:1px solid var(--line);background:transparent;color:var(--ink);border-radius:6px;
 padding:7px 13px;font-size:12.5px;cursor:pointer;font-family:inherit}
.rpg-btn:hover:not(:disabled){border-color:var(--accent);color:var(--accent)}
.rpg-btn:disabled{opacity:.35;cursor:not-allowed}
.rpg-btn.primary{background:var(--accent);border-color:var(--accent);color:#fff}
"""

BODY_JS = r"""
/* ===== 元素纪元 RPG ===== */
const D = window.__RPG__;
const $ = (id) => document.getElementById(id);
const KEY = "chem-rpg-save-v1";
let P = {lv:1, xp:0, hp:100, maxhp:100, atk:12, wave:0, wins:0, dex:{}, best:0};
try { const s = JSON.parse(localStorage.getItem(KEY)); if (s && s.dex) P = Object.assign(P, s); P.hp = P.maxhp; } catch(e){}
const save = () => { const t = Object.assign({}, P); t.hp = t.maxhp; localStorage.setItem(KEY, JSON.stringify(t)); };

/* ---------- 出题器（真实判分） ---------- */
function shuffle(a){ return a.slice().sort(() => Math.random() - .5); }
function fmtOx(v){ return v; }
function mkOxQ(){
  const [f, el, v, why] = D.oxstate[Math.floor(Math.random()*D.oxstate.length)];
  const num = parseFloat(v.replace("−","-").replace("+","")) || 0;
  const opts = new Set([v]);
  const cand = ["+1","+2","+3","+4","+5","+6","+7","0","−1","−2","−3","−4","+8/3"];
  while (opts.size < 4){
    const c = cand[Math.floor(Math.random()*cand.length)];
    if (c !== v) opts.add(c);
  }
  return {q: `${f} 中 ${el} 元素的化合价是多少？`, eq: f, opts: shuffle([...opts]), ans: v, why};
}
function mkRedoxQ(){
  const [eq, ox, re, e, note] = D.redox[Math.floor(Math.random()*D.redox.length)];
  const kind = Math.random() < 0.5 ? "氧化剂" : "还原剂";
  const ans = kind === "氧化剂" ? ox : re;
  const pool = new Set([ox, re]);
  // 干扰项从其他反应的反应物里抓
  while (pool.size < 4){
    const r = D.redox[Math.floor(Math.random()*D.redox.length)];
    pool.add(Math.random() < 0.5 ? r[1] : r[2]);
  }
  return {q: `该反应中的${kind}是？`, eq, opts: shuffle([...pool]), ans,
    why: `${note}。氧化剂 ${ox}（得电子被还原），还原剂 ${re}（失电子被氧化）。`};
}
function mkEQ(){
  const [eq, ox, re, e, note] = D.redox[Math.floor(Math.random()*D.redox.length)];
  const opts = new Set([e]);
  while (opts.size < 4){
    const c = String(Math.max(1, parseInt(e) + [-2,-1,1,2,3][Math.floor(Math.random()*5)]));
    opts.add(c);
  }
  return {q: `该反应中 1 mol 氧化剂（${ox}）得到多少 mol 电子？`, eq, opts: shuffle([...opts]), ans: e,
    why: `${note}；${ox} 中变价元素化合价降低总数为 ${e}。`};
}
function mkChainQ(){
  const ch = D.chains[Math.floor(Math.random()*D.chains.length)];
  const pick = shuffle(ch.items).slice(0, 4);
  const strong = Math.random() < 0.5;
  const ans = pick.reduce((a, b) =>
    (ch.items.indexOf(a) - ch.items.indexOf(b)) * (strong ? 1 : -1) < 0 ? a : b);
  return {q: `下列微粒中${ch.type}最${strong ? "强" : "弱"}的是？`, eq: `（先回忆常见${ch.type}顺序，再作答）`,
    opts: pick, ans, why: `${ch.type}链：${ch.items.join(" > ")}，故${strong ? "最靠前" : "最靠后"}的是 ${ans}。`};
}
function mkQuestion(){
  return [mkOxQ, mkRedoxQ, mkEQ, mkChainQ][Math.floor(Math.random()*4)]();
}

/* ---------- 战斗状态 ---------- */
let sp = null, qLock = false, over = false;
const floaters = []; // {x,y,txt,t,color}
let shake = 0, flashT = 0;

function spiritFor(wave){
  const base = D.spirits[Math.floor(Math.random()*D.spirits.length)];
  return {sym: base[0], name: base[1], color: base[2], intro: base[3],
    maxhp: 28 + wave * 6, hp: 28 + wave * 6, atk: 4 + Math.floor(wave * 0.8),
    bob: Math.random() * 7};
}
function nextWave(){
  P.wave++;
  if (P.wave > P.best) P.best = P.wave;
  sp = spiritFor(P.wave);
  qLock = false;
  save(); renderStats(); renderDex(); drawOpts();
  log(`遭遇了野生精灵 <b>${sp.name}(${sp.sym})</b>！${sp.intro}。`);
  ask();
}
function log(t){
  const el = $("rpgLog");
  el.innerHTML = `<div>· ${t}</div>` + el.innerHTML;
  while (el.children.length > 10) el.lastChild.remove();
}
let curQ = null;
function ask(){
  curQ = mkQuestion();
  qLock = false;
  $("rpgQ").innerHTML = `
    <div class="rpg-q">${curQ.q}</div>
    <div class="rpg-eq">${curQ.eq}</div>
    <div class="rpg-opts" id="rpgOpts"></div>`;
  curQ.opts.forEach(o => {
    const b = document.createElement("button");
    b.className = "rpg-opt"; b.textContent = o;
    b.onclick = () => answer(o, b);
    $("rpgOpts").appendChild(b);
  });
  drawOpts();
}
function answer(o, btn){
  if (qLock || over || !sp) return;
  qLock = true;
  const ok = o === curQ.ans;
  [...$("rpgOpts").children].forEach(b => {
    if (b.textContent === curQ.ans) b.classList.add("right");
    else if (b === btn && !ok) b.classList.add("wrong");
  });
  if (ok){
    const dmg = P.atk + Math.floor(Math.random() * 5);
    sp.hp = Math.max(0, sp.hp - dmg);
    floaters.push({x: 0.68, y: 0.32, txt: "-" + dmg, t: 1, color: "#c8102e"});
    flashT = 1;
    log(`答对！对 ${sp.name} 造成 <b>${dmg}</b> 点伤害。`);
    if (sp.hp <= 0){
      const xp = 20 + P.wave * 4;
      P.xp += xp; P.wins++;
      P.hp = Math.min(P.maxhp, P.hp + 15);
      log(`战胜了 ${sp.name}！+<b>${xp}</b> XP，回复 15 HP。`);
      checkLv();
      sp = null; save(); renderStats();
      setTimeout(() => { if (!over) drawOpts(true); }, 900);
      return;
    }
  } else {
    const dmg = sp.atk + Math.floor(Math.random() * 3);
    P.hp = Math.max(0, P.hp - dmg);
    shake = 1;
    floaters.push({x: 0.2, y: 0.62, txt: "-" + dmg, t: 1, color: "#c8102e"});
    log(`答错了（正确：${curQ.ans}）。${curQ.why} ${sp.name} 反击 <b>${dmg}</b> 点！`);
    if (P.hp <= 0){ gameOver(); return; }
  }
  renderStats();
  setTimeout(() => { if (!over && sp) ask(); }, 1400);
}
function checkLv(){
  const need = P.lv * 100;
  if (P.xp >= need){
    P.xp -= need; P.lv++; P.atk += 3; P.maxhp += 12; P.hp = P.maxhp;
    log(`🎉 升到 <b>Lv.${P.lv}</b>！攻击 +3，HP 上限 +12 并回满。`);
  }
}
function capture(){
  if (!sp || qLock || over) return;
  if (sp.hp > sp.maxhp * 0.45){ log("精灵体力还很充沛，先削弱再捕获！"); return; }
  qLock = true;
  const p = 0.5 + 0.5 * (1 - sp.hp / sp.maxhp);
  if (Math.random() < p){
    P.dex[sp.sym] = (P.dex[sp.sym] || 0) + 1;
    P.xp += 12;
    log(`🎊 捕获成功！<b>${sp.name}(${sp.sym})</b> 加入图鉴，+12 XP。`);
    checkLv(); sp = null; save(); renderStats(); renderDex();
    setTimeout(() => { if (!over) drawOpts(true); }, 900);
  } else {
    const dmg = sp.atk;
    P.hp = Math.max(0, P.hp - dmg); shake = 1;
    floaters.push({x: 0.2, y: 0.62, txt: "-" + dmg, t: 1, color: "#c8102e"});
    log(`捕获失败（概率 ${(p*100)|0}%）！${sp.name} 反击 ${dmg} 点。`);
    qLock = false; renderStats();
    if (P.hp <= 0) gameOver();
  }
}
function gameOver(){
  over = true; save();
  reportScore('rpg', P.best);
  $("rpgQ").innerHTML = `
    <div class="rpg-q" style="font-size:16px">💀 你被元素精灵击倒了……</div>
    <div class="rpg-eq">战绩：第 ${P.wave} 波 · 胜场 ${P.wins} · 图鉴 ${Object.keys(P.dex).length}/20 · 最佳波次 ${P.best}</div>
    <div class="rpg-act"><button class="rpg-btn primary" id="rpgRe">复活再战（保留等级图鉴）</button></div>`;
  $("rpgRe").onclick = () => { over = false; P.hp = P.maxhp; P.wave = 0; nextWave(); };
}
function drawOpts(victory){
  const can = sp && !qLock && !over;
  $("rpgCap").disabled = !can;
  if (victory){
    $("rpgQ").innerHTML = `<div class="rpg-q">这片区域安静下来了……</div>
      <div class="rpg-act"><button class="rpg-btn primary" id="rpgNext">继续探索 →</button></div>`;
    $("rpgNext").onclick = nextWave;
  }
}

/* ---------- 左栏渲染 ---------- */
function renderStats(){
  $("rpgLv").textContent = P.lv;
  $("rpgXp").textContent = P.xp + " / " + (P.lv * 100);
  $("rpgXpBar").style.width = Math.min(100, P.xp / (P.lv * 100) * 100) + "%";
  $("rpgHp").textContent = P.hp + " / " + P.maxhp;
  $("rpgHpBar").style.width = (P.hp / P.maxhp * 100) + "%";
  $("rpgAtk").textContent = P.atk;
  $("rpgWave").textContent = P.wave;
  $("rpgWins").textContent = P.wins;
  $("rpgDexN").textContent = Object.keys(P.dex).length + " / 20";
}
function renderDex(){
  const box = $("rpgDex"); box.innerHTML = "";
  D.spirits.forEach(s => {
    const el = document.createElement("span");
    if (P.dex[s[0]]){ el.className = "got"; el.textContent = s[0] + "×" + P.dex[s[0]]; }
    else el.textContent = s[0];
    box.appendChild(el);
  });
}

/* ---------- Canvas 场景 ---------- */
const cv = $("rpgCanvas");
const ctx = cv.getContext("2d");
let T = 0;
function loop(){
  T += 0.016;
  const box = cv.parentElement.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  if (cv.width !== box.width * dpr){ cv.width = box.width * dpr; cv.height = box.height * dpr; }
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  const W = box.width, H = box.height;
  const cs = getComputedStyle(document.body);
  const ink = cs.getPropertyValue("--ink").trim() || "#333";
  const acc = cs.getPropertyValue("--accent").trim() || "#c8102e";
  // 背景
  const g = ctx.createLinearGradient(0, 0, 0, H);
  g.addColorStop(0, "rgba(0,0,0,0.06)"); g.addColorStop(1, "rgba(0,0,0,0.16)");
  ctx.clearRect(0, 0, W, H); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  // 漂浮微粒
  ctx.globalAlpha = .25;
  for (let i = 0; i < 26; i++){
    const x = ((i * 97.3 + T * 12 * (i % 3 + 1)) % (W + 40)) - 20;
    const y = (Math.sin(T * .6 + i) * .5 + .5) * H;
    ctx.beginPath(); ctx.arc(x, y, 1.6 + (i % 3), 0, 7);
    ctx.fillStyle = ink; ctx.fill();
  }
  ctx.globalAlpha = 1;
  const sx = shake > 0 ? (Math.random() - .5) * 10 * shake : 0;
  shake = Math.max(0, shake - 0.04);
  ctx.save(); ctx.translate(sx, 0);
  // 玩家（小炼金术士）
  const px = W * 0.2, py = H * 0.62;
  ctx.beginPath(); ctx.moveTo(px, py - 46); ctx.lineTo(px - 22, py + 8); ctx.lineTo(px + 22, py + 8); ctx.closePath();
  ctx.fillStyle = acc; ctx.globalAlpha = .9; ctx.fill(); ctx.globalAlpha = 1;
  ctx.beginPath(); ctx.arc(px, py - 50, 10, 0, 7); ctx.fillStyle = acc; ctx.fill();
  ctx.strokeStyle = ink; ctx.lineWidth = 3;
  ctx.beginPath(); ctx.moveTo(px + 16, py - 30); ctx.lineTo(px + 34, py - 62); ctx.stroke();
  ctx.beginPath(); ctx.arc(px + 34, py - 66, 4 + Math.sin(T * 3) * 1.5, 0, 7);
  ctx.fillStyle = "#ffd76a"; ctx.fill();
  bar(px, py - 78, P.hp / P.maxhp, "#c8102e");
  label(px, py + 24, "你 Lv." + P.lv, ink);
  // 精灵
  if (sp){
    const ex = W * 0.68, ey = H * 0.32 + Math.sin(T * 2 + sp.bob) * 8;
    const rg = ctx.createRadialGradient(ex, ey, 4, ex, ey, 40);
    rg.addColorStop(0, sp.color); rg.addColorStop(1, "transparent");
    ctx.beginPath(); ctx.arc(ex, ey, 40, 0, 7); ctx.fillStyle = rg; ctx.globalAlpha = .55; ctx.fill();
    ctx.globalAlpha = 1;
    ctx.beginPath(); ctx.arc(ex, ey, 24, 0, 7); ctx.fillStyle = sp.color; ctx.fill();
    ctx.beginPath(); ctx.arc(ex - 8, ey - 9, 7, 0, 7); ctx.fillStyle = "rgba(255,255,255,.4)"; ctx.fill();
    ctx.fillStyle = "#fff"; ctx.font = "bold 17px 'Noto Sans SC',sans-serif";
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText(sp.sym, ex, ey + 1);
    bar(ex, ey - 46, sp.hp / sp.maxhp, "#c89028");
    label(ex, ey + 42, `${sp.name} ${sp.hp}/${sp.maxhp}`, ink);
    // 攻击闪光
    if (flashT > 0){
      ctx.strokeStyle = acc; ctx.lineWidth = 3 * flashT; ctx.globalAlpha = flashT;
      ctx.beginPath(); ctx.moveTo(px + 34, py - 66); ctx.lineTo(ex, ey); ctx.stroke();
      ctx.globalAlpha = 1; flashT -= 0.05;
    }
  } else if (!over){
    ctx.fillStyle = ink; ctx.globalAlpha = .5; ctx.font = "14px 'Noto Sans SC',sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("—— 点击「继续探索」寻找下一个精灵 ——", W * 0.6, H * 0.35);
    ctx.globalAlpha = 1;
  }
  // 伤害飘字
  for (let i = floaters.length - 1; i >= 0; i--){
    const f = floaters[i];
    ctx.globalAlpha = Math.max(0, f.t);
    ctx.fillStyle = f.color; ctx.font = "bold 20px 'Noto Sans SC',sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(f.txt, f.x * W, f.y * H - (1 - f.t) * 40);
    f.t -= 0.02; if (f.t <= 0) floaters.splice(i, 1);
  }
  ctx.globalAlpha = 1; ctx.restore();
  requestAnimationFrame(loop);
}
function bar(x, y, p, color){
  ctx.fillStyle = "rgba(0,0,0,.25)"; ctx.fillRect(x - 34, y, 68, 6);
  ctx.fillStyle = color; ctx.fillRect(x - 34, y, 68 * Math.max(0, p), 6);
}
function label(x, y, t, color){
  ctx.fillStyle = color; ctx.font = "12px 'Noto Sans SC',sans-serif";
  ctx.textAlign = "center"; ctx.fillText(t, x, y);
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

$("rpgCap").onclick = capture;$("rpgNew").onclick = () => {
  if (!confirm("重新开始？等级、图鉴、战绩将全部清空！")) return;
  P = {lv:1, xp:0, hp:100, maxhp:100, atk:12, wave:0, wins:0, dex:{}, best:0};
  over = false; save(); renderStats(); renderDex(); nextWave();
};

renderStats(); renderDex(); nextWave(); loop();
"""

HTML = f"""<!DOCTYPE html>
<html lang="zh-CN" data-theme="washi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>元素纪元 RPG · 化学生活教学中心</title>
<style>{CSS}
{EXTRA_CSS}</style>
</head>
<body>
<nav class="topnav">
  <div class="brand">
    <span class="badge">RPG</span>
    <h1 style="white-space:nowrap">元素纪元 RPG</h1>
    <span class="lecture-tag">GAMES · LAB 01</span>
  </div>
  <div class="nav-right">
    <a class="nav-btn" href="chem_lab5.3.html">CBTI 鉴定 <span class="arr">→</span></a>
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
      <div class="panel-title">炼金术士档案</div>
      <div class="rpg-stat"><span>等级</span><b>Lv.<span id="rpgLv">1</span></b></div>
      <div class="rpg-stat"><span>经验</span><b id="rpgXp">0</b></div>
      <div class="rpg-hpbar rpg-xpbar"><i id="rpgXpBar"></i></div>
      <div class="rpg-stat"><span>生命</span><b id="rpgHp">100</b></div>
      <div class="rpg-hpbar"><i id="rpgHpBar"></i></div>
      <div class="rpg-stat"><span>攻击力</span><b id="rpgAtk">12</b></div>
      <div class="rpg-stat"><span>当前波次</span><b id="rpgWave">0</b></div>
      <div class="rpg-stat"><span>胜场</span><b id="rpgWins">0</b></div>
      <div class="rpg-stat"><span>图鉴收集</span><b id="rpgDexN">0 / 20</b></div>
    </div>
    <div class="panel-section">
      <div class="panel-title">元素图鉴</div>
      <div class="rpg-dex" id="rpgDex"></div>
    </div>
    <div class="panel-section">
      <div class="panel-title">操作</div>
      <button class="rpg-btn" id="rpgNew" style="width:100%">重新开始</button>
    </div>
  </div>

  <div class="canvas-box" style="background:var(--bg-deep)">
    <div class="rpg-wrap"><canvas id="rpgCanvas"></canvas></div>
  </div>

  <div class="side right-panel">
    <div class="panel-section">
      <div class="panel-title">战斗 · 知识问答</div>
      <div id="rpgQ"></div>
      <div class="rpg-act">
        <button class="rpg-btn" id="rpgCap" disabled>🫙 捕获（HP≤45% 时可用）</button>
      </div>
      <div class="rpg-log" id="rpgLog"></div>
    </div>
  </div>
</div>

<script>window.__RPG__ = {json.dumps(DATA, ensure_ascii=False)};</script>
<script>{BODY_JS}</script>
<script>{THEME_JS}</script>
</body>
</html>
"""

open(OUT, "w", encoding="utf-8").write(HTML)
print("written:", OUT, len(HTML), "bytes,", len(SPIRITS), "spirits,",
      len(OXSTATE), "oxstate,", len(REDOX), "redox,", len(CHAINS), "chains")
