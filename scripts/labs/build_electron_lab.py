# -*- coding: utf-8 -*-
"""
生成 核外电子排布实验室 chem_lab1.3.html
外壳（CSS + 主题 JS）提取自 chem_lab1.2.html，保持三主题一致
功能：118 元素周期表选择 / 玻尔壳层动画 / 轨道方框图(泡利+洪特) /
      排布式(完整·简化·价电子) / 构造原理填充链 / 常见离子切换 / 半径对比
"""
import json, re

LAB12 = r"C:\Users\风逝\Documents\kimi\tasks\2026-08-31\06-27-38-247a26cf\chem-life-main\public\teaching\chem_lab1.2.html"
OUT   = r"C:\Users\风逝\Documents\kimi\tasks\2026-08-31\06-27-38-247a26cf\chem-life-main\public\teaching\chem_lab1.3.html"

old = open(LAB12, encoding="utf-8").read()
CSS = re.search(r"<style>(.*?)</style>", old, re.S).group(1)
THEME_JS = re.search(r"/\* =+ 主题切换 washi / sumi / ai =+ \*/\s*\(function\(\)\{.*?\}\)\(\);", old, re.S).group(0)

# ============ 元素基础数据（Z, 符号, 中文名） ============
SYMS = ["H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar",
 "K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr",
 "Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe",
 "Cs","Ba","La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu",
 "Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn",
 "Fr","Ra","Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr",
 "Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Nh","Fl","Mc","Lv","Ts","Og"]
ZHS = ["氢","氦","锂","铍","硼","碳","氮","氧","氟","氖","钠","镁","铝","硅","磷","硫","氯","氩",
 "钾","钙","钪","钛","钒","铬","锰","铁","钴","镍","铜","锌","镓","锗","砷","硒","溴","氪",
 "铷","锶","钇","锆","铌","钼","锝","钌","铑","钯","银","镉","铟","锡","锑","碲","碘","氙",
 "铯","钡","镧","铈","镨","钕","钷","钐","铕","钆","铽","镝","钬","铒","铥","镱","镥",
 "铪","钽","钨","铼","锇","铱","铂","金","汞","铊","铅","铋","钋","砹","氡",
 "钫","镭","锕","钍","镤","铀","镎","钚","镅","锔","锫","锎","锿","镄","钔","锘","铹",
 "Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Nh","Fl","Mc","Lv","Ts","Og"]
# 104 以后中文名用符号代替（超纲元素仅作排布演示）

AUFBAU = [(1,0),(2,0),(2,1),(3,0),(3,1),(4,0),(3,2),(4,1),(5,0),(4,2),(5,1),
          (6,0),(4,3),(5,2),(6,1),(7,0),(5,3),(6,2),(7,1)]
CAP = {0:2, 1:6, 2:10, 3:14}

# 基态排布例外（洪特规则特例/半满全满稳定）：Z -> {(n,l):occ}
EXC = {
 24:{(3,2):5,(4,0):1}, 29:{(3,2):10,(4,0):1},
 41:{(4,2):4,(5,0):1}, 42:{(4,2):5,(5,0):1}, 44:{(4,2):7,(5,0):1},
 45:{(4,2):8,(5,0):1}, 46:{(4,2):10,(5,0):0}, 47:{(4,2):10,(5,0):1},
 57:{(4,3):0,(5,2):1,(6,0):2}, 58:{(4,3):1,(5,2):1,(6,0):2}, 64:{(4,3):7,(5,2):1,(6,0):2},
 78:{(5,2):9,(6,0):1}, 79:{(5,2):10,(6,0):1},
 89:{(5,3):0,(6,2):1,(7,0):2}, 90:{(5,3):0,(6,2):2,(7,0):2},
 91:{(5,3):2,(6,2):1,(7,0):2}, 92:{(5,3):3,(6,2):1,(7,0):2},
 93:{(5,3):4,(6,2):1,(7,0):2}, 96:{(5,3):7,(6,2):1,(7,0):2},
}
EXC_REASON = {
 24:"3d⁵ 半满稳定（洪特规则特例）", 29:"3d¹⁰ 全满稳定（洪特规则特例）",
 42:"4d⁵ 半满稳定", 46:"4d¹⁰ 全满稳定（5s 全空）", 47:"4d¹⁰ 全满稳定",
 64:"4f⁷ 半满稳定", 78:"5d⁹6s¹ 近似全满", 79:"5d¹⁰ 全满稳定", 96:"5f⁷ 半满稳定",
}
NOBLE = {2:"He",10:"Ne",18:"Ar",36:"Kr",54:"Xe",86:"Rn"}

def base_config(z):
    """按构造原理填 z 个电子，再应用例外表。返回 {(n,l):occ}（已按书写序整理在外层）"""
    left = z; cfg = {}
    for (n,l) in AUFBAU:
        if left <= 0: break
        occ = min(CAP[l], left); cfg[(n,l)] = occ; left -= occ
    if z in EXC:
        # 例外：先算出例外前的总量，按例外表覆盖涉及亚层
        cfg = {k:v for k,v in cfg.items() if k not in EXC[z] or True}
        tot = sum(cfg.values())
        for k,v in EXC[z].items():
            tot -= cfg.get(k,0); cfg[k]=v; tot += v
        # 差量（一般例外只改 3d/4s 等已在表内的亚层，总量不变）
        assert tot == z, (z, tot)
        cfg = {k:v for k,v in cfg.items() if v>0}
    return cfg

def sort_write(cfg):
    return sorted(cfg.items(), key=lambda kv:(kv[0][0], kv[0][1]))

L_LETTER = "spdf"
def fmt_cfg(cfg):
    return "".join(f"{n}{L_LETTER[l]}{occ}" for (n,l),occ in sort_write(cfg))

def short_cfg(z, cfg):
    core = max([n for n in NOBLE if n < z] or [0])
    if core == 0: return None
    rest = {k:v for k,v in cfg.items()}
    c = base_config(core)
    for k,v in c.items(): rest[k] = rest.get(k,0)-v
    rest = {k:v for k,v in rest.items() if v>0}
    return f"[{NOBLE[core]}] " + fmt_cfg(rest)

def period_of(cfg): return max(n for (n,l) in cfg)
def block_of(cfg):
    # 最后填入的亚层（按构造序）
    last = None
    for (n,l) in AUFBAU:
        if (n,l) in cfg: last = (n,l)
    return L_LETTER[last[1]]

def group_of(z, cfg):
    """高中口径的族：主族给 1-18 列号，副族给 B 族标记的简化描述"""
    b = block_of(cfg)
    nmax = period_of(cfg)
    s = cfg.get((nmax,0),0); p = cfg.get((nmax,1),0)
    if z == 2: return ("18","0 族")
    if b == "s": return (str(s), "ⅠA" if s==1 else "ⅡA")
    if b == "p":
        g = 10 + s + p
        rom = {3:"ⅢA",4:"ⅣA",5:"ⅤA",6:"ⅥA",7:"ⅦA",8:"0 族"}[s+p]
        return (str(g), rom)
    if b == "d":
        d = cfg.get((nmax-1,2),0)
        col = d + s
        label = {3:"ⅢB",4:"ⅣB",5:"ⅤB",6:"ⅥB",7:"ⅦB",8:"Ⅷ",9:"Ⅷ",10:"Ⅷ",11:"ⅠB",12:"ⅡB"}.get(col,"Ⅷ")
        return (str(col) if col<=12 else "—", label)
    return ("—", "镧系" if 57<=z<=71 else ("锕系" if 89<=z<=103 else "f 区"))

# 原子半径（pm，约值，教学用；空缺 = None）
RAD = {1:37,2:31,3:152,4:111,5:88,6:77,7:70,8:66,9:64,10:38,
 11:186,12:160,13:143,14:117,15:110,16:104,17:99,18:71,
 19:227,20:197,21:162,22:147,23:134,24:128,25:127,26:126,27:125,28:124,29:128,30:134,
 31:135,32:122,33:120,34:119,35:114,36:88,
 37:248,38:215,39:180,40:160,41:146,42:139,43:136,44:134,45:134,46:137,47:144,48:151,
 49:167,50:140,51:140,52:142,53:133,54:108,
 55:265,56:217,72:159,73:146,74:139,75:137,76:135,77:136,78:139,79:144,80:151,
 81:170,82:146,83:148,84:168,85:150,86:120,87:270,88:220}

# 常见离子（高中常考）：Z -> [(电荷, 示例说明)]
IONS = {
 1:[(1,"H⁺")], 3:[(1,"Li⁺")], 8:[(-2,"O²⁻")], 9:[(-1,"F⁻")], 11:[(1,"Na⁺")],
 12:[(2,"Mg²⁺")], 13:[(3,"Al³⁺")], 15:[(-3,"P³⁻")], 16:[(-2,"S²⁻")], 17:[(-1,"Cl⁻")],
 19:[(1,"K⁺")], 20:[(2,"Ca²⁺")], 24:[(3,"Cr³⁺")], 25:[(2,"Mn²⁺")],
 26:[(2,"Fe²⁺"),(3,"Fe³⁺")], 27:[(2,"Co²⁺")], 28:[(2,"Ni²⁺")],
 29:[(1,"Cu⁺"),(2,"Cu²⁺")], 30:[(2,"Zn²⁺")], 35:[(-1,"Br⁻")], 47:[(1,"Ag⁺")],
 50:[(2,"Sn²⁺")], 53:[(-1,"I⁻")], 56:[(2,"Ba²⁺")], 80:[(2,"Hg²⁺")], 82:[(2,"Pb²⁺")],
}

ELEMS = []
for z in range(1, 119):
    cfg = base_config(z)
    col, glabel = group_of(z, cfg)
    ELEMS.append({
        "z": z, "sym": SYMS[z-1], "zh": ZHS[z-1],
        "cfg": {f"{n},{l}": occ for (n,l),occ in sort_write(cfg)},
        "period": period_of(cfg), "block": block_of(cfg),
        "gcol": col, "glabel": glabel,
        "full": fmt_cfg(cfg), "short": short_cfg(z, cfg),
        "shells": {str(n): sum(v for (nn,l),v in cfg.items() if nn==n) for n in range(1,8)},
        "exc": EXC_REASON.get(z),
        "rad": RAD.get(z),
        "ions": IONS.get(z, []),
    })

# 周期表格子坐标（用于选择器网格）
def pt_pos(z):
    table = {1:(1,1),2:(1,18)}
    # 用周期/族列构造
    e = ELEMS[z-1]
    p = e["period"]
    b = e["block"]
    if z == 1: return (1,1)
    if z == 2: return (1,18)
    if b == "s": return (p, int(e["gcol"]))
    if b == "p": return (p, int(e["gcol"]))
    if b == "d": return (p, int(e["gcol"]))
    # f 区放下方两行
    if 57 <= z <= 71: return (9, z-57+3)
    if 89 <= z <= 103: return (10, z-89+3)
    return (p, 3)

POS = {str(z): pt_pos(z) for z in range(1,119)}

DATA = {"elems": ELEMS, "pos": POS,
        "aufbau": [f"{n}{L_LETTER[l]}" for (n,l) in AUFBAU],
        "cap": CAP}

# ============ 附加 CSS ============
EXTRA_CSS = r"""
/* ===== 电子排布实验室专用 ===== */
.pt-grid{display:grid;grid-template-columns:repeat(18,1fr);gap:2px;margin-top:6px}
.pt-cell{aspect-ratio:1;border:1px solid var(--line,#ccc);border-radius:2px;font-size:9px;
 display:flex;align-items:center;justify-content:center;cursor:pointer;color:var(--ink);
 background:transparent;transition:all .15s;line-height:1;font-family:inherit}
.pt-cell:hover{border-color:var(--accent);transform:scale(1.25);z-index:2;position:relative}
.pt-cell.cur{background:var(--accent);color:#fff;border-color:var(--accent)}
.pt-cell.blk-s{background:color-mix(in srgb,var(--accent) 12%,transparent)}
.pt-cell.blk-d{background:color-mix(in srgb,#b8860b 16%,transparent)}
.pt-cell.blk-f{background:color-mix(in srgb,#7b5ea7 16%,transparent)}
.pt-spacer{grid-row:8;height:4px}
.cfg-line{font-family:"Courier New",monospace;font-size:14px;margin:4px 0;line-height:1.7}
.cfg-line sup{font-size:9px}
.cfg-label{font-size:11px;opacity:.65;margin-top:8px}
.shell-chips{display:flex;gap:4px;flex-wrap:wrap;margin-top:4px}
.shell-chip{border:1px solid var(--line,#ccc);border-radius:10px;padding:1px 8px;font-size:11px}
.aufbau-chain{display:flex;flex-wrap:wrap;gap:3px;margin-top:6px}
.ab-chip{font-size:10px;padding:1px 6px;border-radius:8px;border:1px solid var(--line,#ccc);opacity:.35}
.ab-chip.filled{opacity:1;border-color:var(--accent);color:var(--accent)}
.ab-chip.last{background:var(--accent);color:#fff;opacity:1}
.orb-rows{display:flex;flex-direction:column;gap:8px;margin-top:6px}
.orb-row{display:flex;align-items:center;gap:8px}
.orb-tag{width:52px;font-size:12px;font-family:"Courier New",monospace;text-align:right;flex:none}
.orb-boxes{display:flex;gap:3px}
.orb-box{width:26px;height:26px;border:1px solid var(--line,#999);border-radius:3px;
 display:flex;align-items:center;justify-content:center;font-size:15px;color:var(--accent);letter-spacing:1px}
.orb-box .up{color:var(--accent)} .orb-box .dn{color:#b89ae8}
.ion-btns{display:flex;gap:5px;flex-wrap:wrap;margin-top:4px}
.ion-btn{border:1px solid var(--line,#ccc);background:transparent;color:var(--ink);border-radius:4px;
 padding:2px 10px;font-size:12px;cursor:pointer;font-family:inherit}
.ion-btn.cur{background:var(--accent);color:#fff;border-color:var(--accent)}
.rad-bar-row{display:flex;align-items:center;gap:6px;font-size:11px;margin:3px 0}
.rad-bar-row .nm{width:34px;flex:none}
.rad-bar{height:8px;border-radius:4px;background:var(--accent);opacity:.8}
.rad-bar.dim{opacity:.3}
.rad-val{width:56px;flex:none;opacity:.7}
.bohr-wrap{position:relative;width:100%;height:100%}
#bohrCanvas{width:100%;height:100%;display:block}
.btm-scroll{position:absolute;left:0;right:0;bottom:0;max-height:46%;overflow:auto;
 background:color-mix(in srgb,var(--surface) 88%,transparent);backdrop-filter:blur(6px);
 border-top:1px solid var(--line,#ccc);padding:10px 14px}
@media (max-width:900px){.btm-scroll{position:static;max-height:none}}
.elem-big{display:flex;align-items:baseline;gap:10px}
.brand h1{white-space:nowrap}
.elem-big .sym{font-size:34px;font-family:Georgia,serif;color:var(--accent)}
.elem-big .znum{font-size:13px;opacity:.7}
.kv{font-size:12px;line-height:1.9}
.kv b{color:var(--accent)}
"""

# ============ 页面主体 JS ============
BODY_JS = r"""
/* ===== 核外电子排布实验室 ===== */
const D = window.__ELAB__;
const CAP = {s:2,p:6,d:10,f:14};
let curZ = 26, curQ = 0;   // 默认 Fe

const $ = (id) => document.getElementById(id);
const sup = (n) => String(n).replace(/\d/g, d => "⁰¹²³⁴⁵⁶⁷⁸⁹"[+d]).replace(/-/g,"⁻");

/* ---- 周期表选择器 ---- */
function buildPicker(){
  const g = $("ptGrid"); g.innerHTML = "";
  const spacer = document.createElement("div");
  spacer.className = "pt-spacer"; spacer.style.gridColumn = "1 / span 18";
  const cells = [];
  for (const e of D.elems){
    const [r,c] = D.pos[String(e.z)];
    const b = document.createElement("button");
    b.className = "pt-cell blk-" + e.block;
    b.style.gridRow = r; b.style.gridColumn = c;
    b.textContent = e.sym; b.title = `${e.z} ${e.zh} ${e.sym}`;
    b.onclick = () => { curZ = e.z; curQ = 0; render(); };
    b.dataset.z = e.z;
    cells.push(b); g.appendChild(b);
  }
  g.appendChild(spacer);
}

/* ---- 离子排布计算 ---- */
function parseCfg(e){ return Object.entries(e.cfg).map(([k,occ]) => { const [n,l]=k.split(",").map(Number); return {n,l,occ}; }); }
function ionConfig(e, q){
  let subs = parseCfg(e).map(s => ({...s}));
  if (q > 0){
    let k = q;
    // 失电子：n 大者优先；同 n，l 大者优先（先 np 再 ns；过渡金属先失 ns 再失 (n-1)d）
    const order = [...subs].sort((a,b) => b.n - a.n || b.l - a.l);
    for (const s of order){
      if (k <= 0) break;
      const take = Math.min(s.occ, k);
      subs.find(x => x.n===s.n && x.l===s.l).occ -= take; k -= take;
    }
  } else if (q < 0){
    let k = -q;
    // 得电子：沿构造序继续填
    const order = D.aufbau.map(t => ({n:+t[0], l:"spdf".indexOf(t[1])}));
    for (const s of order){
      if (k <= 0) break;
      const cur = subs.find(x => x.n===s.n && x.l===s.l);
      const cap = CAP["spdf"[s.l]];
      const have = cur ? cur.occ : 0;
      const add = Math.min(cap - have, k);
      if (add > 0){ if (cur) cur.occ += add; else subs.push({n:s.n,l:s.l,occ:add}); k -= add; }
    }
  }
  return subs.filter(s => s.occ > 0).sort((a,b) => a.n - b.n || a.l - b.l);
}
function fmtCfg(subs){ return subs.map(s => `${s.n}${"spdf"[s.l]}${sup(s.occ)}`).join(" "); }

/* ---- 轨道方框图（泡利 + 洪特） ---- */
function orbitalBoxes(subs){
  return subs.map(s => {
    const boxes = 2*s.l + 1;
    let up = Math.min(s.occ, boxes), dn = s.occ - up;
    const arr = Array.from({length: boxes}, (_, i) =>
      (i < up ? "↑" : "") + (i >= up - dn && dn > 0 && i < up ? "" : ""));
    // 规范：先每盒一个 ↑，再从头补 ↓
    const cells = [];
    let rem = s.occ;
    for (let i = 0; i < boxes && rem > 0; i++){ cells.push(["up"]); rem--; }
    for (let i = 0; i < boxes && rem > 0; i++){ cells[i].push("dn"); rem--; }
    return {label:`${s.n}${"spdf"[s.l]}`, occ:s.occ, cap:CAP["spdf"[s.l]], cells};
  });
}

/* ---- 渲染 ---- */
function render(){
  const e = D.elems[curZ - 1];
  document.querySelectorAll(".pt-cell.cur").forEach(x => x.classList.remove("cur"));
  const cell = document.querySelector(`.pt-cell[data-z="${curZ}"]`);
  if (cell) cell.classList.add("cur");

  const subs = curQ === 0 ? parseCfg(e).sort((a,b)=>a.n-b.n||a.l-b.l) : ionConfig(e, curQ);
  const ionTxt = curQ === 0 ? e.sym : e.sym + (curQ>0 ? (curQ>1?sup(curQ):"")+"⁺" : (curQ<-1?sup(-curQ):"")+"⁻");

  /* 左：信息卡 */
  $("elemBig").innerHTML = `<span class="sym">${ionTxt}</span><span class="znum">${e.z} 号 · ${e.zh}</span>`;
  $("tagWrap").innerHTML = [
    `第 ${e.period} 周期`, e.glabel + (e.block==="f"?"":" 族"),
    {s:"s 区",p:"p 区",d:"d 区",f:"f 区"}[e.block],
    e.exc ? "排布例外" : null,
  ].filter(Boolean).map(t => `<span class="tag">${t}</span>`).join("");
  let desc = "";
  if (curQ !== 0) desc = `${e.zh}原子${curQ>0?"失去":"得到"} ${Math.abs(curQ)} 个电子形成 ${ionTxt}。${curQ>0&&e.block==="d"?"过渡金属失电子顺序：先失最外层 ns 电子，再失 (n−1)d 电子。":""}`;
  else if (e.exc) desc = `基态排布不服从构造原理的顺序推断：${e.exc}。`;
  else desc = `基态原子，核外共 ${e.z} 个电子，按构造原理依次填入各能级。`;
  $("crysDesc").textContent = desc;

  /* 排布式 */
  const fullTxt = fmtCfg(subs);
  $("cfgFull").innerHTML = fullTxt;
  // 简化排布式：找小于总电子数的最大稀有气体核心
  const total = subs.reduce((a,s)=>a+s.occ, 0);
  const NOB = [[2,"He"],[10,"Ne"],[18,"Ar"],[36,"Kr"],[54,"Xe"],[86,"Rn"]];
  const core = [...NOB].reverse().find(([n]) => n < total);
  if (core){
    const coreSubs = ionConfig(D.elems[core[0]-1], 0);
    const rest = subs.map(s => ({...s}));
    for (const cs of coreSubs){
      const r = rest.find(x => x.n===cs.n && x.l===cs.l);
      if (r) r.occ -= cs.occ;
    }
    const restList = rest.filter(s => s.occ>0).sort((a,b)=>a.n-b.n||a.l-b.l);
    $("cfgShort").innerHTML = `[${core[1]}] ` + fmtCfg(restList);
  } else $("cfgShort").textContent = "—（无更小的稀有气体核心）";
  // 价电子层
  const nmax = Math.max(...subs.map(s=>s.n));
  const val = subs.filter(s => s.n===nmax || (e.block==="d"&&s.n===nmax-1&&s.l===2));
  $("cfgVal").innerHTML = fmtCfg(val);
  // 每层电子数
  const shells = {};
  subs.forEach(s => shells[s.n]=(shells[s.n]||0)+s.occ);
  $("shellChips").innerHTML = Object.keys(shells).sort().map(n =>
    `<span class="shell-chip">${"KLMNOPQ"[n-1]} 层 ${shells[n]}</span>`).join("");

  /* 构造原理链：最后填入 = 构造序中最后一个已填能级 */
  let lastKey = null;
  for (const t of D.aufbau){
    if (subs.some(s => `${s.n}${"spdf"[s.l]}`===t)) lastKey = t;
  }
  $("aufbauChain").innerHTML = D.aufbau.map(t => {
    const filled = subs.some(s => `${s.n}${"spdf"[s.l]}`===t);
    return `<span class="ab-chip ${filled?"filled":""} ${t===lastKey?"last":""}">${t}</span>`;
  }).join("");

  /* 轨道方框图 */
  const rows = orbitalBoxes(subs);
  $("orbRows").innerHTML = rows.map(r => `
    <div class="orb-row">
      <div class="orb-tag">${r.label} ${r.occ}/${r.cap}</div>
      <div class="orb-boxes">${r.cells.map(c =>
        `<div class="orb-box">${c.map(x=>`<span class="${x}">${x==="up"?"↑":"↓"}</span>`).join("")}</div>`).join("")}</div>
    </div>`).join("");

  /* 离子按钮 */
  $("ionBtns").innerHTML = [`<button class="ion-btn ${curQ===0?"cur":""}" data-q="0">${e.sym} 原子</button>`]
    .concat(e.ions.map(([q,lab]) =>
      `<button class="ion-btn ${curQ===q?"cur":""}" data-q="${q}">${lab}</button>`)).join("");
  $("ionBtns").querySelectorAll(".ion-btn").forEach(b =>
    b.onclick = () => { curQ = +b.dataset.q; render(); });
  $("ionSection").style.display = "block";

  /* 半径对比 */
  renderRadius(e);

  drawBohr(subs, ionTxt);
}

function renderRadius(e){
  const wrap = $("radBars");
  if (!e.rad){ wrap.innerHTML = `<p class="info-desc">该元素暂无教学半径数据。</p>`; return; }
  const rows = [];
  const push = (z2, tag) => {
    const o = D.elems[z2-1];
    if (o && o.rad && o.z!==e.z) rows.push({nm:o.sym, val:o.rad, me:false, tag});
  };
  // 同周期相邻
  for (const o of D.elems) if (o.period===e.period && Math.abs(o.z-e.z)===1) push(o.z,"期");
  // 同族（同列）相邻
  for (const o of D.elems) if (o.gcol===e.gcol && o.block===e.block && o.z!==e.z && Math.abs(o.period-e.period)===1) push(o.z,"族");
  rows.push({nm:e.sym, val:e.rad, me:true, tag:""});
  const max = Math.max(...rows.map(r=>r.val), 1);
  wrap.innerHTML = rows.map(r => `
    <div class="rad-bar-row"><span class="nm">${r.nm}</span>
      <div class="rad-bar ${r.me?"":"dim"}" style="width:${(r.val/max*100).toFixed(0)}%"></div>
      <span class="rad-val">${r.val} pm${r.tag?` ·同${r.tag}`:""}</span></div>`).join("");
}

/* ---- 玻尔壳层动画 ---- */
let bohrSubs = [], bohrLabel = "", animT = 0;
function drawBohr(subs, label){
  const shells = {};
  subs.forEach(s => shells[s.n]=(shells[s.n]||0)+s.occ);
  bohrSubs = Object.keys(shells).map(n => ({n:+n, cnt:shells[n]}));
  bohrLabel = label;
}
const cv = () => $("bohrCanvas");
function cssVar(name){ return getComputedStyle(document.body).getPropertyValue(name).trim(); }
function frame(){
  const c = cv(); if (!c) return;
  const box = c.parentElement.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  if (c.width !== box.width*dpr){ c.width = box.width*dpr; c.height = box.height*dpr; }
  const ctx = c.getContext("2d");
  ctx.setTransform(dpr,0,0,dpr,0,0);
  const W = box.width, H = box.height, cx = W/2, cy = H/2;
  ctx.clearRect(0,0,W,H);
  const ink = cssVar("--fg") || "#333", acc = cssVar("--accent") || "#c8102e";
  const nshell = bohrSubs.length;
  const R0 = 34, Rstep = Math.min(34, (Math.min(W,H)/2 - 60) / Math.max(nshell-1,1) || 34);
  animT += 0.008;
  // 核
  ctx.beginPath(); ctx.arc(cx,cy,20,0,7); ctx.fillStyle = acc; ctx.fill();
  ctx.fillStyle = "#fff"; ctx.font = "bold 11px Georgia"; ctx.textAlign="center"; ctx.textBaseline="middle";
  ctx.fillText(bohrLabel.slice(0,4), cx, cy);
  // 壳层
  bohrSubs.forEach((sh, i) => {
    const r = R0 + i*Rstep;
    ctx.beginPath(); ctx.arc(cx,cy,r,0,7);
    ctx.strokeStyle = ink; ctx.globalAlpha = .25; ctx.stroke(); ctx.globalAlpha = 1;
    // 电子点
    const dots = Math.min(sh.cnt, 40);
    const speed = 0.5 / (0.6 + i*0.35);
    for (let k = 0; k < dots; k++){
      const a = animT*speed + k/dots*Math.PI*2;
      const x = cx + r*Math.cos(a), y = cy + r*Math.sin(a);
      ctx.beginPath(); ctx.arc(x,y,4,0,7); ctx.fillStyle = acc; ctx.fill();
      ctx.beginPath(); ctx.arc(x-1.2,y-1.2,1.4,0,7); ctx.fillStyle="rgba(255,255,255,.75)"; ctx.fill();
    }
    // 层标注
    ctx.fillStyle = ink; ctx.globalAlpha = .55; ctx.font = "10px sans-serif"; ctx.textAlign="left";
    ctx.fillText(`${"KLMNOPQ"[sh.n-1]}·${sh.cnt}`, cx + r*Math.SQRT1_2 + 6, cy - r*Math.SQRT1_2);
    ctx.globalAlpha = 1;
  });
  requestAnimationFrame(frame);
}

buildPicker();
render();
requestAnimationFrame(frame);
"""

# ============ 组装 HTML ============
HTML = f"""<!DOCTYPE html>
<html lang="zh-CN" data-theme="washi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>核外电子排布实验室 · 化学生活教学中心</title>
<style>{CSS}
{EXTRA_CSS}</style>
</head>
<body>
<nav class="topnav">
  <div class="brand">
    <span class="badge">电</span>
    <h1>核外电子排布实验室</h1>
    <span class="lecture-tag">STRUCTURE · LAB 04</span>
  </div>
  <div class="nav-right">
    <a class="nav-btn" href="chem_lab1.1.html">VSEPR 分子构型 <span class="arr">→</span></a>
    <a class="nav-btn" href="chem_lab1.2.html">晶体结构 <span class="arr">→</span></a>
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
      <div class="elem-big" id="elemBig"></div>
      <div class="tag-wrap" id="tagWrap"></div>
      <p class="info-desc" id="crysDesc"></p>
    </div>
    <div class="panel-section">
      <div class="panel-title">核外电子排布式</div>
      <div class="cfg-label">完整排布式</div>
      <div class="cfg-line" id="cfgFull"></div>
      <div class="cfg-label">简化排布式（稀有气体核心）</div>
      <div class="cfg-line" id="cfgShort"></div>
      <div class="cfg-label">价电子层排布</div>
      <div class="cfg-line" id="cfgVal"></div>
      <div class="cfg-label">各电子层容纳电子数</div>
      <div class="shell-chips" id="shellChips"></div>
    </div>
    <div class="panel-section" id="ionSection">
      <div class="panel-title">原子 / 常见离子</div>
      <div class="ion-btns" id="ionBtns"></div>
    </div>
  </div>

  <div class="canvas-box">
    <div class="bohr-wrap">
      <canvas id="bohrCanvas"></canvas>
      <div class="btm-scroll">
        <div class="panel-title">电子排布图 · 轨道方框（泡利不相容 · 洪特规则）</div>
        <div class="orb-rows" id="orbRows"></div>
      </div>
    </div>
  </div>

  <div class="side right-panel">
    <div class="panel-section">
      <div class="panel-title">元素周期表 · 点击选择</div>
      <div class="pt-grid" id="ptGrid"></div>
    </div>
    <div class="panel-section">
      <div class="panel-title">构造原理 · 能级填充顺序</div>
      <div class="aufbau-chain" id="aufbauChain"></div>
      <p class="info-desc">高亮 = 已填入；实心 = 最后填入的能级。例外元素（Cr/Cu 等）按半满·全满稳定处理。</p>
    </div>
    <div class="panel-section">
      <div class="panel-title">微粒半径对比（约值）</div>
      <div id="radBars"></div>
      <p class="info-desc">同周期左→右渐小，同主族上→下渐大；阳离子 &lt; 原子 &lt; 阴离子。</p>
    </div>
  </div>
</div>

<script>window.__ELAB__ = {json.dumps(DATA, ensure_ascii=False)};</script>
<script>{BODY_JS}</script>
<script>{THEME_JS}</script>
</body>
</html>
"""

open(OUT, "w", encoding="utf-8").write(HTML)
print("written:", OUT, len(HTML), "bytes")

# 自检：排布总量 & 经典案例
for z, expect in [(26,"1s2 2s2 2p6 3s2 3p6 3d6 4s2"), (24,"1s2 2s2 2p6 3s2 3p6 3d5 4s1"),
                  (29,"1s2 2s2 2p6 3s2 3p6 3d10 4s1"), (118,None)]:
    got = fmt_cfg(base_config(z))
    got_sp = " ".join(re.findall(r"\d+[spdf]\d+", got))
    print(z, "OK" if (expect is None or got_sp==expect) else f"MISMATCH {got_sp}")
