# -*- coding: utf-8 -*-
"""
晶体结构深度实验室 · 全量重写生成器
- 31 种真实晶体结构（分数坐标 → 世界坐标）
- 真·晶胞延展（滑块连续扩展键与粒子）
- 真·立方体切割（Three.js clipping planes，顶点 1/8、棱 1/4、面 1/2）
- 球棍短棍（原子表面到表面）/ 比例模型（相邻粒子真实半径相切）
- 微粒显隐按种类动态生成，单一种类自动隐藏
- 二维投影：四个视角、按种类着色、按半径定大小、深度明暗
"""
import json, re, math, pathlib

PROJ = pathlib.Path(r"C:\Users\风逝\Documents\kimi\tasks\2026-08-31\06-27-38-247a26cf\chem-life-main\public\teaching")
OLD = PROJ / "chem_lab1.2.html"

# ---------- 从旧版提取 tk-chem 风格 CSS 与主题 JS ----------
old = OLD.read_text(encoding="utf-8")
CSS = re.search(r"<style>(.*?)</style>", old, re.S).group(1)
THEME_JS = re.search(r"/\* =+ 主题切换 washi / sumi / ai =+ \*/\s*\(function\(\)\{.*?\}\)\(\);", old, re.S).group(0)

E, H = 1.6, 0.8
def W(f):  # 分数坐标 → 世界坐标
    return [round(f[0]*E-H, 4), round(f[1]*E-H, 4), round(f[2]*E-H, 4)]

CORNERS = [(0,0,0),(0,0,1),(0,1,0),(0,1,1),(1,0,0),(1,0,1),(1,1,0),(1,1,1)]
FACES = [(.5,.5,0),(.5,.5,1),(.5,0,.5),(.5,1,.5),(0,.5,.5),(1,.5,.5)]
BODY = [(.5,.5,.5)]
EDGES = [(.5,0,0),(0,.5,0),(0,0,.5),(.5,1,0),(.5,0,1),(1,.5,0),(0,.5,1),(1,0,.5),(0,1,.5),(.5,1,1),(1,.5,1),(1,1,.5)]
FCC = CORNERS + FACES
BCC = CORNERS + BODY
DIA_IN = [(.25,.25,.25),(.25,.75,.75),(.75,.25,.75),(.75,.75,.25)]
TETRA8 = DIA_IN + [(.25,.25,.75),(.25,.75,.25),(.75,.25,.25),(.75,.75,.75)]

def sp(*items):
    """(符号, 颜色, 真实相对半径)"""
    return [{"sp": s, "color": c, "r": r} for s, c, r in items]

def atoms(idx, pts, wrap=True):
    out = []
    for p in pts:
        if wrap:
            q = []
            for x in p:
                m = x % 1.0
                # 晶胞 +1 侧的面/棱/顶点不能被 % 1 折回 0 侧，否则正半侧原子全部丢失
                if abs(m) < 1e-9 and x > 0.5:
                    m = 1.0
                q.append(m)
        else:
            q = list(p)
        out.append([idx] + [round(v, 4) for v in W(q)])
    return out

CUBIC = {"half": [H, H, H], "vec": [E, E, E], "frame": "cube"}

CRYSTALS = {}

def add(cid, name, ctype, tags, desc, species, at, bond=True, cell=None, note=""):
    CRYSTALS[cid] = {
        "name": name, "type": ctype, "tags": tags, "desc": desc, "note": note,
        "species": species, "atoms": at, "bond": bond,
        "cell": cell or CUBIC,
    }

# ================= 离子晶体 =================
nacl_cl = FCC; nacl_na = EDGES + BODY
add("nacl", "NaCl 氯化钠（食盐）", "ion", ["NaCl 型", "配位数 6:6", "面心立方"],
    "Na⁺ 与 Cl⁻ 交替占据面心立方阵点。厨房食盐的微观结构。",
    sp(("Na", 0xf4a950, 1.02), ("Cl", 0x35c48d, 1.81)),
    atoms(0, nacl_na) + atoms(1, nacl_cl))
add("kcl", "KCl 氯化钾", "ion", ["NaCl 型", "配位数 6:6"],
    "低钠盐的主要成分，结构与食盐相同，K⁺ 半径更大。",
    sp(("K", 0xc8a2ff, 1.38), ("Cl", 0x35c48d, 1.81)),
    atoms(0, nacl_na) + atoms(1, nacl_cl))
add("lif", "LiF 氟化锂", "ion", ["NaCl 型", "配位数 6:6"],
    "锂离子电池电解质原料之一，Li⁺ 是常见离子中半径最小的一档。",
    sp(("Li", 0xffd166, 0.76), ("F", 0x87f0ff, 1.33)),
    atoms(0, nacl_na) + atoms(1, nacl_cl))
add("mgo", "MgO 氧化镁", "ion", ["NaCl 型", "耐火材料"],
    "耐火砖主要成分，熔点高达 2852 ℃，离子键很强。",
    sp(("Mg", 0x7cf07c, 0.72), ("O", 0xef6461, 1.40)),
    atoms(0, nacl_na) + atoms(1, nacl_cl))
add("bao", "BaO 氧化钡", "ion", ["NaCl 型", "配位数 6:6"],
    "Ba²⁺ 半径大，与 O²⁻ 形成 NaCl 型堆积。",
    sp(("Ba", 0x66ccff, 1.35), ("O", 0xef6461, 1.40)),
    atoms(0, nacl_na) + atoms(1, nacl_cl))
add("cscl", "CsCl 氯化铯", "ion", ["CsCl 型", "配位数 8:8", "简单立方"],
    "Cl⁻ 作简单立方堆积，Cs⁺ 填入体心立方空隙。",
    sp(("Cs", 0xb089f7, 1.67), ("Cl", 0x35c48d, 1.81)),
    atoms(0, BODY) + atoms(1, CORNERS))
add("csbr", "CsBr 溴化铯", "ion", ["CsCl 型", "配位数 8:8"],
    "与 CsCl 同构，红外光学材料。",
    sp(("Cs", 0xb089f7, 1.67), ("Br", 0xd97762, 1.96)),
    atoms(0, BODY) + atoms(1, CORNERS))
add("zns", "ZnS 闪锌矿", "ion", ["闪锌矿型", "配位数 4:4", "四面体配位"],
    "S²⁻ 面心立方，Zn²⁺ 占据半数四面体空隙。夜光粉常用基材。",
    sp(("Zn", 0xe8c168, 0.74), ("S", 0xffdd44, 1.84)),
    atoms(0, DIA_IN) + atoms(1, FCC))
add("caf2", "CaF₂ 萤石", "ion", ["萤石型", "配位数 8:4"],
    "Ca²⁺ 面心立方，F⁻ 填满全部四面体空隙。萤石可磨制光学镜片。",
    sp(("Ca", 0xffa500, 1.00), ("F", 0x87f0ff, 1.33)),
    atoms(0, FCC) + atoms(1, TETRA8))
tio2_o = [(0.3,0.3,0),(0.7,0.7,0),(0.8,0.2,0.5),(0.2,0.8,0.5)]
add("tio2", "TiO₂ 金红石", "ion", ["金红石型", "配位数 6:3"],
    "防晒霜与白色颜料的主要成分，Ti 六配位、O 三配位。",
    sp(("Ti", 0xb0c4de, 0.61), ("O", 0xef6461, 1.40)),
    atoms(0, CORNERS + BODY) + atoms(1, tio2_o))
add("cu2o", "Cu₂O 氧化亚铜", "ion", ["赤铜矿型", "半导体"],
    "O 作体心立方排布，Cu 位于四面体位置，是经典半导体材料。",
    sp(("Cu", 0xd08b4f, 0.77), ("O", 0xef6461, 1.40)),
    atoms(0, DIA_IN) + atoms(1, BCC))

# ================= 金属晶体 =================
for cid, nm, col, r, extra in [
    ("cu", "Cu 金属铜", 0xd08b4f, 1.28, "导线、电缆的核心材料。"),
    ("ag", "Ag 金属银", 0xe8e8e8, 1.44, "导电性最好的金属。"),
    ("au", "Au 金属金", 0xffd700, 1.44, "延展性最好的金属。"),
    ("al", "Al 金属铝", 0xd0d0d0, 1.43, "地壳含量最高的金属。"),
    ("ni", "Ni 金属镍", 0xa8b0b8, 1.25, "不锈钢与电池材料。"),
]:
    add(cid, nm, "metal", ["金属晶体", "面心立方最密堆积", "配位数 12"],
        f"fcc 最密堆积，配位数 12，空间利用率 74%。{extra}",
        sp((nm.split()[1][0:2].strip() if False else nm.split()[1][:2], col, r)),
        atoms(0, FCC), bond=False)
# 修正金属符号（上面占位逻辑绕，直接重建）
for cid, sym in [("cu","Cu"),("ag","Ag"),("au","Au"),("al","Al"),("ni","Ni")]:
    CRYSTALS[cid]["species"][0]["sp"] = sym

for cid, nm, sym, col, r, extra in [
    ("na", "Na 金属钠", "Na", 0xf4a950, 1.86, "活泼金属，保存在煤油中。"),
    ("k", "K 金属钾", "K", 0xc8a2ff, 2.27, "比钠更活泼。"),
    ("fe", "Fe α-铁", "Fe", 0x9c8f8f, 1.26, "常温下铁为体心立方。"),
    ("w", "W 金属钨", "W", 0x6e7b8b, 1.37, "熔点最高的金属，灯丝材料。"),
    ("ba", "Ba 金属钡", "Ba", 0x66ccff, 2.17, "碱土金属。"),
]:
    add(cid, nm, "metal", ["金属晶体", "体心立方堆积", "配位数 8"],
        f"bcc 体心立方，配位数 8，空间利用率 68%。{extra}",
        sp((sym, col, r)), atoms(0, BCC), bond=False)

add("po", "Po 金属钋（简单立方）", "metal", ["金属晶体", "简单立方", "配位数 6"],
    "唯一以简单立方堆积的金属，配位数 6，空间利用率仅 52%。",
    sp(("Po", 0xaa88bb, 1.68)), atoms(0, CORNERS), bond=False)

# HCP 镁（六方最密堆积）：直接世界坐标
R_HCP, C_HCP = 0.62, 1.012  # 最近邻 a，c = 1.633a
hcp_atoms = []
for z, rot, ring in [(-C_HCP/2, 0, True), (0, 30, False), (C_HCP/2, 0, True)]:
    if ring:
        for k in range(6):
            ang = math.radians(60*k)
            hcp_atoms.append([0, round(R_HCP*math.cos(ang),4), round(R_HCP*math.sin(ang),4), round(z,4)])
        hcp_atoms.append([0, 0, 0, round(z,4)])
    else:
        for k in range(3):
            ang = math.radians(60*k + 30)
            rr = R_HCP * 0.5774
            hcp_atoms.append([0, round(rr*math.cos(ang),4), round(rr*math.sin(ang),4), 0])
add("mg", "Mg 金属镁（六方最密）", "metal", ["金属晶体", "六方最密堆积", "配位数 12"],
    "hcp 六方最密堆积（Mg、Zn、Ti 同类），配位数 12，空间利用率 74%。",
    sp(("Mg", 0x7cf07c, 1.60)), hcp_atoms, bond=False,
    cell={"half": [R_HCP, R_HCP, C_HCP/2], "vec": [0, 0, C_HCP], "frame": "hex", "hexR": R_HCP},
    note="六方晶胞：延展仅沿 c 轴方向堆叠")

# ================= 共价晶体 =================
add("diamond", "金刚石 C", "covalent", ["共价晶体", "sp³ 正四面体", "最硬天然物质"],
    "每个 C 与 4 个相邻 C 以共价键相连，形成空间网状结构。",
    sp(("C", 0xb0b6bd, 0.77)), atoms(0, FCC + DIA_IN))
add("si", "单晶硅 Si", "covalent", ["共价晶体", "金刚石型", "芯片基材"],
    "与金刚石同构，是芯片与光伏板的基础材料。",
    sp(("Si", 0xc2b280, 1.11)), atoms(0, FCC + DIA_IN))
add("sic", "SiC 碳化硅", "covalent", ["共价晶体", "闪锌矿型", "金刚砂"],
    "C 与 Si 交替占据金刚石阵点，硬度仅次于金刚石，作磨料。",
    sp(("Si", 0xc2b280, 1.11), ("C", 0xb0b6bd, 0.77)),
    atoms(0, DIA_IN) + atoms(1, FCC))
# SiO2 β-方石英：Si 金刚石位，O 在每对最近邻 Si 中点
si_pos = [W(p) for p in FCC + DIA_IN]
o_pos, seen = [], set()
inner = [W(p) for p in DIA_IN]
outer = [W(p) for p in FCC]
for ip in inner:
    ds = sorted(outer, key=lambda op: sum((a-b)**2 for a, b in zip(ip, op)))[:4]
    for op in ds:
        mid = tuple(round((a+b)/2, 4) for a, b in zip(ip, op))
        key = tuple(round(v*4) for v in mid)
        if key not in seen:
            seen.add(key); o_pos.append(mid)
add("sio2", "SiO₂ 石英（方石英型）", "covalent", ["共价晶体", "SiO₄ 四面体", "沙子主要成分"],
    "每个 Si 连 4 个 O 形成四面体，每个 O 桥接两个 Si。河沙、水晶的主要成分。",
    sp(("Si", 0xc2b280, 1.11), ("O", 0xef6461, 0.66)),
    [[0]+list(p) for p in si_pos] + [[1]+list(p) for p in o_pos])

# ================= 分子晶体 =================
co2_at = atoms(0, FCC)
for p in FCC:
    for sgn in (1, -1):
        co2_at.append([1] + [round(v, 4) for v in W(tuple((c + sgn*0.13) % 1.0 for c in p))])
add("co2", "CO₂ 干冰", "molecule", ["分子晶体", "面心立方", "升华制冷"],
    "CO₂ 分子占据面心立方阵点，分子间仅靠范德华力，所以易升华。",
    sp(("C", 0xb0b6bd, 0.77), ("O", 0xef6461, 0.66)), co2_at)
i2_at = []
for p in CORNERS + [(.5,.5,0),(.5,.5,1)]:
    for sgn in (1, -1):
        i2_at.append([0] + [round(v, 4) for v in W((p[0], p[1], (p[2] + sgn*0.16) % 1.0))])
add("i2", "I₂ 碘晶体", "molecule", ["分子晶体", "双原子分子", "易升华"],
    "I₂ 分子成对排列，分子内是共价键、分子间是范德华力，所以碘易升华、易溶于酒精。",
    sp(("I", 0xb57edc, 1.33)), i2_at)
p4_at = []
T4 = [(0.09,0.09,0.09),(0.09,-0.09,-0.09),(-0.09,0.09,-0.09),(-0.09,-0.09,0.09)]
for p in FCC:
    for t in T4:
        p4_at.append([0] + [round(v, 4) for v in W(tuple((p[i]+t[i]) % 1.0 for i in range(3)))])
add("p4", "P₄ 白磷", "molecule", ["分子晶体", "正四面体分子", "自燃"],
    "4 个 P 构成正四面体小分子，键角被迫弯成 60°，张力大所以活泼、40℃ 即自燃。",
    sp(("P", 0xff8c69, 1.10)), p4_at)

# ================= 混合型：石墨 =================
d_cc = 0.30
L = math.sqrt(3) * d_cc
a1 = (L, 0.0); a2 = (L/2, math.sqrt(3)*L/2)
off = ((a1[0]+a2[0])/3, (a1[1]+a2[1])/3)
def graphene_layer(z, shift=(0, 0)):
    pts = []
    for m in range(-3, 4):
        for n in range(-3, 4):
            for base in ((0, 0), off):
                x = m*a1[0] + n*a2[0] + base[0] + shift[0]
                y = m*a1[1] + n*a2[1] + base[1] + shift[1]
                if abs(x) <= 0.76 and abs(y) <= 0.76:
                    pts.append([0, round(x, 4), round(y, 4), z])
    return pts
gra = graphene_layer(-0.42) + graphene_layer(0.42, shift=(0, d_cc))
add("graphite", "石墨 C", "mix", ["混合型晶体", "层状结构", "导电"],
    "层内 C–C 共价键（键长 142 pm），层间范德华力。铅笔芯、电极材料。",
    sp(("C", 0xb0b6bd, 0.77)), gra,
    cell={"half": [H, H, 0.84], "vec": [0, 0, 1.68], "frame": "cube"},
    note="层状结构：延展仅沿层间方向堆叠")

# 类型分组
GROUPS = {}
for cid, c in CRYSTALS.items():
    GROUPS.setdefault(c["type"], []).append(cid)

data_js = "const CRYSTALS = " + json.dumps(CRYSTALS, ensure_ascii=False) + ";\n"
data_js += "const GROUPS = " + json.dumps(GROUPS, ensure_ascii=False) + ";\n"
pathlib.Path(r"C:\Users\风逝\Documents\kimi\tasks\2026-08-31\07-18-32-e4826c65\crystal_data.js").write_text(data_js, encoding="utf-8")
counts = {t: len(v) for t, v in GROUPS.items()}
print("crystals:", len(CRYSTALS), counts)
print("css bytes:", len(CSS), "theme js:", len(THEME_JS))

# ============================================================
# 渲染引擎 JS
# ============================================================
ENGINE_JS = r"""
/* ================= 基础场景 ================= */
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0d1017);
const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 2000);
camera.position.set(6.5, 5.2, 8.5);
camera.lookAt(0, 0, 0);
const canvas = document.getElementById('crystalCanvas');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.localClippingEnabled = true;
const wrapDom = document.querySelector('.canvas-box');
function resizeRender(){
  const w = wrapDom.clientWidth, h = wrapDom.clientHeight;
  renderer.setSize(w, h); camera.aspect = w / h; camera.updateProjectionMatrix();
}
resizeRender();
window.addEventListener('resize', resizeRender);

scene.add(new THREE.AmbientLight(0xffffff, 0.45));
const keyLight = new THREE.DirectionalLight(0xffffff, 0.85);
keyLight.position.set(9, 11, 13); scene.add(keyLight);
const rimLight = new THREE.DirectionalLight(0xa7c8ff, 0.35);
rimLight.position.set(-9, -7, -11); scene.add(rimLight);

const root = new THREE.Group(); scene.add(root);

/* 拖拽旋转 + 滚轮缩放 */
let drag = false, lastX = 0, lastY = 0;
canvas.addEventListener('mousedown', e => { drag = true; lastX = e.clientX; lastY = e.clientY; });
canvas.addEventListener('mousemove', e => {
  if (!drag) return;
  root.rotation.y += (e.clientX - lastX) * 0.005;
  root.rotation.x += (e.clientY - lastY) * 0.005;
  lastX = e.clientX; lastY = e.clientY;
  updateClipPlanes();
});
['mouseup','mouseleave'].forEach(ev => canvas.addEventListener(ev, () => drag = false));
canvas.addEventListener('wheel', e => {
  e.preventDefault();
  const s = 1 + e.deltaY * 0.001;
  camera.position.multiplyScalar(s);
  const l = camera.position.length();
  if (l < 3.5) camera.position.setLength(3.5);
  if (l > 30) camera.position.setLength(30);
}, { passive:false });

/* ================= 状态 ================= */
const state = { type:'ion', mat:'nacl', extend:0, style:'ballstick', opacity:0.85, clip:false, hidden:new Set() };

/* ================= 晶胞边界切割 ================= */
let clipBases = [];   // {n:Vector3 局部法向, c:常数}
let clipPlanes = [];
function buildClipBases(cell){
  clipBases = [];
  if (cell.frame === 'cube'){
    const [hx, hy, hz] = cell.half;
    [[1,0,0,hx],[-1,0,0,hx],[0,1,0,hy],[0,-1,0,hy],[0,0,1,hz],[0,0,-1,hz]]
      .forEach(([x,y,z,c]) => clipBases.push({ n:new THREE.Vector3(x,y,z), c }));
  } else if (cell.frame === 'hex'){
    const R = cell.hexR, hz = cell.half[2];
    for (let k = 0; k < 6; k++){
      const a = Math.PI/3 * k + Math.PI/6;
      clipBases.push({ n:new THREE.Vector3(Math.cos(a), Math.sin(a), 0), c: R * Math.cos(Math.PI/6) });
    }
    clipBases.push({ n:new THREE.Vector3(0,0,1), c: hz });
    clipBases.push({ n:new THREE.Vector3(0,0,-1), c: hz });
  }
  clipPlanes = clipBases.map(b => new THREE.Plane(b.n.clone().negate(), b.c));
}
function updateClipPlanes(){
  if (!clipPlanes.length) return;
  const q = root.quaternion;
  clipPlanes.forEach((p, i) => {
    p.normal.copy(clipBases[i].n).applyQuaternion(q).negate();
    p.constant = clipBases[i].c;
  });
}
function activeClip(){ return state.clip ? clipPlanes : null; }

/* ================= 渲染 ================= */
const unitSphere = new THREE.SphereGeometry(1, 28, 28);
let stickMat;

function clearRoot(){
  while (root.children.length) {
    const ch = root.children.pop();
    ch.traverse(o => {
      if (o.geometry && o.geometry !== unitSphere) o.geometry.dispose();
      if (o.material && o.material !== stickMat) { /* 共享材质不单独 dispose */ }
    });
  }
}

function visibleRadius(sp){   // 球棍模型的视觉半径（压缩差异便于观察）
  return 0.14 + sp.r * 0.085;
}

function buildCrystal(){
  clearRoot();
  const d = CRYSTALS[state.mat];
  const cell = d.cell;
  buildClipBases(cell);

  /* ---- 1. 延展：收集所有可见原子 ---- */
  const ext = state.extend;
  const atoms = [];
  const [hx, hy, hz] = cell.half;
  const [vx, vy, vz] = cell.vec;
  const range = 1.0001 + ext * 1.05;   // 以晶胞为单位的外扩圈数
  const offRange = ext <= 0.001 ? [0] : [-1, 0, 1];
  for (const oi of offRange) for (const oj of offRange) for (const ok of offRange){
    const ox = oi*vx, oy = oj*vy, oz = ok*vz;
    // 六方晶胞只允许沿 z 轴延展
    if (cell.frame === 'hex' && (oi !== 0 || oj !== 0)) continue;
    for (const [si, x, y, z] of d.atoms){
      const px = x+ox, py = y+oy, pz = z+oz;
      if (Math.abs(px) <= hx*range + 1e-4 &&
          Math.abs(py) <= hy*range + 1e-4 &&
          Math.abs(pz) <= hz*range + 1e-4){
        atoms.push({ si, p: new THREE.Vector3(px, py, pz) });
      }
    }
  }

  /* ---- 2. 半径：比例模型按真实半径相切 ---- */
  let radiusOf = si => visibleRadius(d.species[si]);
  if (state.style === 'spacefill'){
    // 找最近邻对，令 r1+r2 = 最近邻距
    let best = null;
    const inner = atoms.filter(a => Math.abs(a.p.x)<=hx+1e-3 && Math.abs(a.p.y)<=hy+1e-3 && Math.abs(a.p.z)<=hz+1e-3);
    for (let i = 0; i < atoms.length; i++){
      for (let j = i+1; j < atoms.length; j++){
        const dist = atoms[i].p.distanceTo(atoms[j].p);
        if (dist < 1e-4) continue;
        const rs = d.species[atoms[i].si].r + d.species[atoms[j].si].r;
        const ratio = dist / rs;
        if (!best || ratio < best.ratio) best = { ratio };
      }
    }
    const k = best ? best.ratio : 0.4;
    radiusOf = si => d.species[si].r * k;
  }

  /* ---- 3. 画原子 ---- */
  const clip = activeClip();
  const mats = d.species.map(s => new THREE.MeshPhysicalMaterial({
    color: s.color, transparent: true, opacity: state.opacity,
    roughness: 0.25, metalness: 0.15, clearcoat: 0.4,
    clippingPlanes: clip, clipShadows: true,
  }));
  atoms.forEach(a => {
    if (state.hidden.has(a.si)) return;
    const m = new THREE.Mesh(unitSphere, mats[a.si]);
    m.position.copy(a.p);
    m.scale.setScalar(radiusOf(a.si));
    root.add(m);
  });

  /* ---- 4. 化学键：短棍（表面到表面） ---- */
  if (d.bond && state.style === 'ballstick'){
    // 自动键长阈值 = 中心晶胞内最小非零距离 × 1.25
    const inner = atoms.filter(a => Math.abs(a.p.x)<=hx+1e-3 && Math.abs(a.p.y)<=hy+1e-3 && Math.abs(a.p.z)<=hz+1e-3);
    let minD = Infinity;
    for (let i = 0; i < inner.length; i++)
      for (let j = i+1; j < inner.length; j++){
        const dist = inner[i].p.distanceTo(inner[j].p);
        if (dist > 1e-4 && dist < minD) minD = dist;
      }
    const cutoff = minD * 1.25;
    stickMat = new THREE.MeshStandardMaterial({ color: 0xb8c0cc, roughness: 0.45, metalness: 0.3, clippingPlanes: clip });
    const up = new THREE.Vector3(0,1,0);
    for (let i = 0; i < atoms.length; i++){
      for (let j = i+1; j < atoms.length; j++){
        const A = atoms[i], B = atoms[j];
        if (state.hidden.has(A.si) && state.hidden.has(B.si)) continue;
        const dist = A.p.distanceTo(B.p);
        if (dist > cutoff) continue;
        const dir = B.p.clone().sub(A.p).normalize();
        const r1 = radiusOf(A.si) * 0.92, r2 = radiusOf(B.si) * 0.92;
        const start = A.p.clone().addScaledVector(dir, r1);
        const end = B.p.clone().addScaledVector(dir, -r2);
        const len = start.distanceTo(end);
        if (len <= 0.02) continue;
        const geo = new THREE.CylinderGeometry(0.05, 0.05, len, 10);
        const stick = new THREE.Mesh(geo, stickMat);
        stick.position.copy(start).lerp(end, 0.5);
        stick.quaternion.setFromUnitVectors(up, dir);
        root.add(stick);
      }
    }
  }

  /* ---- 5. 晶胞框架 ---- */
  const frameMat = new THREE.LineBasicMaterial({ color: 0x8a94a6, transparent: true, opacity: 0.75 });
  if (cell.frame === 'cube'){
    const g = new THREE.EdgesGeometry(new THREE.BoxGeometry(hx*2, hy*2, hz*2));
    root.add(new THREE.LineSegments(g, frameMat));
  } else if (cell.frame === 'hex'){
    const pts = [];
    const R = cell.hexR, zt = cell.half[2];
    for (let k = 0; k < 6; k++){
      const a1 = Math.PI/3*k, a2 = Math.PI/3*(k+1);
      const p1 = [R*Math.cos(a1), R*Math.sin(a1)], p2 = [R*Math.cos(a2), R*Math.sin(a2)];
      pts.push(new THREE.Vector3(p1[0],p1[1],zt), new THREE.Vector3(p2[0],p2[1],zt));
      pts.push(new THREE.Vector3(p1[0],p1[1],-zt), new THREE.Vector3(p2[0],p2[1],-zt));
      pts.push(new THREE.Vector3(p1[0],p1[1],zt), new THREE.Vector3(p1[0],p1[1],-zt));
    }
    const g = new THREE.BufferGeometry().setFromPoints(pts);
    root.add(new THREE.LineSegments(g, frameMat));
  }

  updateInfo(d);
  drawProjection();
}

/* ================= 信息卡 / 图例 / 显隐 ================= */
function hex(c){ return '#' + c.toString(16).padStart(6, '0'); }
function updateInfo(d){
  document.getElementById('crysName').textContent = d.name;
  document.getElementById('tagWrap').innerHTML = d.tags.map(t => `<span class="info-tag">${t}</span>`).join('');
  document.getElementById('crysDesc').textContent = d.desc + (d.note ? '（' + d.note + '）' : '');
  // 图例
  document.getElementById('legendWrap').innerHTML = d.species.map((s, i) =>
    `<span class="legend-item"><span class="legend-ball" style="background:${hex(s.color)}"></span>${s.sp}</span>`
  ).join('');
  // 显隐开关：只有一种粒子时整块隐藏
  const sec = document.getElementById('speciesSection');
  const box = document.getElementById('speciesToggles');
  if (d.species.length < 2){ sec.classList.add('hidden'); state.hidden.clear(); return; }
  sec.classList.remove('hidden');
  box.innerHTML = '';
  d.species.forEach((s, i) => {
    const row = document.createElement('div');
    row.className = 'switch-row';
    row.innerHTML = `<span class="switch-label"><span class="legend-ball" style="background:${hex(s.color)};margin-right:5px"></span>${s.sp} 微粒</span>`;
    const sw = document.createElement('div');
    sw.className = 'switch' + (state.hidden.has(i) ? '' : ' active');
    sw.onclick = () => {
      state.hidden.has(i) ? state.hidden.delete(i) : state.hidden.add(i);
      buildCrystal();
    };
    row.appendChild(sw);
    box.appendChild(row);
  });
}

/* ================= 二维投影点阵 ================= */
function drawProjection(){
  const modal = document.getElementById('projModal');
  if (modal.style.display !== 'block') return;
  const cv = document.getElementById('projCanvas');
  // 弹层刚 display:block 时可能尚未排版，等一帧再画，避免 0 尺寸画布
  if (!cv.offsetWidth || !cv.offsetHeight){ requestAnimationFrame(drawProjection); return; }
  const ctx = cv.getContext('2d');
  const w = cv.width = cv.offsetWidth * 2, h = cv.height = cv.offsetHeight * 2;
  ctx.clearRect(0, 0, w, h);
  const d = CRYSTALS[state.mat];
  const cell = d.cell;
  const axis = document.getElementById('projViewSelect').value;
  // 投影基
  let u, v, depthAxis;
  if (axis === '001'){ u = new THREE.Vector3(1,0,0); v = new THREE.Vector3(0,1,0); depthAxis = 'z'; }
  else if (axis === '100'){ u = new THREE.Vector3(0,1,0); v = new THREE.Vector3(0,0,1); depthAxis = 'x'; }
  else if (axis === '010'){ u = new THREE.Vector3(1,0,0); v = new THREE.Vector3(0,0,1); depthAxis = 'y'; }
  else { u = new THREE.Vector3(Math.SQRT1_2,Math.SQRT1_2,0); v = new THREE.Vector3(0,0,1); depthAxis = 'd'; }
  const [hx, hy, hz] = cell.half;
  const halfU = axis==='110' ? Math.hypot(hx, hy) : Math.max(Math.abs(u.x)*hx + Math.abs(u.y)*hy + Math.abs(u.z)*hz);
  const halfV = Math.max(Math.abs(v.x)*hx + Math.abs(v.y)*hy + Math.abs(v.z)*hz);
  const scale = Math.min(w, h) * 0.42 / Math.max(halfU, halfV);
  const cx = w/2, cy = h/2;
  // 晶胞边界
  ctx.strokeStyle = 'rgba(160,170,185,.8)'; ctx.lineWidth = 2; ctx.setLineDash([8, 6]);
  if (cell.frame === 'hex'){
    ctx.beginPath();
    for (let k = 0; k <= 6; k++){
      const a = Math.PI/3*k;
      const px = cx + cell.hexR*Math.cos(a)*scale*(axis==='001'?1:0.9);
      const py = cy - cell.hexR*Math.sin(a)*scale*(axis==='001'?1:0.9);
      k ? ctx.lineTo(px, py) : ctx.moveTo(px, py);
    }
    ctx.stroke();
  } else {
    ctx.strokeRect(cx - halfU*scale, cy - halfV*scale, halfU*2*scale, halfV*2*scale);
  }
  ctx.setLineDash([]);
  // 原子（中心晶胞），按深度排序，远的先画且变淡
  const list = d.atoms
    .map(([si, x, y, z]) => ({ si, p: new THREE.Vector3(x, y, z) }))
    .filter(a => !state.hidden.has(a.si))
    .filter(a => Math.abs(a.p.x)<=hx+1e-3 && Math.abs(a.p.y)<=hy+1e-3 && Math.abs(a.p.z)<=hz+1e-3)
    .map(a => ({ ...a, depth: depthAxis==='x' ? a.p.x : depthAxis==='y' ? a.p.y : depthAxis==='z' ? a.p.z : (a.p.x - a.p.y) }))
    .sort((a, b) => a.depth - b.depth);
  const dmin = list.length ? list[0].depth : 0, dmax = list.length ? list[list.length-1].depth : 1;
  list.forEach(a => {
    const s = d.species[a.si];
    const px = cx + a.p.dot(u) * scale;
    const py = cy - a.p.dot(v) * scale;
    const rr = Math.max(6, s.r * 14);
    const t = dmax > dmin ? (a.depth - dmin) / (dmax - dmin) : 0.5;
    ctx.globalAlpha = 0.35 + 0.65 * t;
    ctx.beginPath(); ctx.arc(px, py, rr, 0, Math.PI*2);
    ctx.fillStyle = hex(s.color); ctx.fill();
    ctx.globalAlpha = 1;
    ctx.strokeStyle = 'rgba(255,255,255,.55)'; ctx.lineWidth = 2; ctx.stroke();
  });
  // 标注
  ctx.fillStyle = 'rgba(230,235,242,.9)';
  ctx.font = `500 ${Math.round(w/46)}px "JetBrains Mono", monospace`;
  ctx.fillText('[' + axis + '] view · 颜色区分粒子种类 · 近亮远暗', 16, h - 18);
}

/* ================= 控件绑定 ================= */
const typeSel = document.getElementById('crystalTypeSel');
const matSel = document.getElementById('crystalMatSel');
const TYPE_LABEL = { ion:'离子晶体', metal:'金属晶体', covalent:'共价晶体', molecule:'分子晶体', mix:'混合型晶体' };
function refreshMats(){
  matSel.innerHTML = '';
  GROUPS[state.type].forEach(id => {
    const o = document.createElement('option');
    o.value = id; o.textContent = CRYSTALS[id].name;
    matSel.appendChild(o);
  });
  state.mat = GROUPS[state.type][0];
  state.hidden.clear();
  buildCrystal();
}
typeSel.onchange = e => { state.type = e.target.value; refreshMats(); };
matSel.onchange = e => { state.mat = e.target.value; state.hidden.clear(); buildCrystal(); };
document.getElementById('modelStyleSel').onchange = e => { state.style = e.target.value; buildCrystal(); };

const opSlider = document.getElementById('opacitySlider');
opSlider.oninput = () => {
  state.opacity = Number(opSlider.value);
  document.getElementById('opacityTip').textContent = '透明度 ' + state.opacity.toFixed(2);
  buildCrystal();
};
const extSlider = document.getElementById('cellExtendSlider');
extSlider.oninput = () => {
  state.extend = Number(extSlider.value);
  const tip = document.getElementById('sliderTip');
  if (state.extend <= 0.01) tip.textContent = '仅显示中心 1 个晶胞';
  else if (state.extend < 0.5) tip.textContent = '延展中：相邻晶胞的键与微粒渐入';
  else tip.textContent = '完全延展：3×3×3 晶胞';
  buildCrystal();
};
document.getElementById('clipCellSwitch').onclick = function(){
  this.classList.toggle('active');
  state.clip = this.classList.contains('active');
  buildCrystal();
};
document.getElementById('openProjBtn').onclick = () => {
  document.getElementById('projModal').style.display = 'block';
  drawProjection();
};
document.getElementById('closeProj').onclick = () => {
  document.getElementById('projModal').style.display = 'none';
};
document.getElementById('projViewSelect').onchange = drawProjection;

/* ================= 主循环 ================= */
function animate(){ requestAnimationFrame(animate); renderer.render(scene, camera); }
animate();
refreshMats();
"""

# ============================================================
# 组装最终 HTML
# ============================================================
BODY = r"""
<nav class="topnav">
  <div class="brand">
    <span class="badge">晶</span>
    <h1>晶体结构深度实验室</h1>
    <span class="lecture-tag">STRUCTURE · LAB 02</span>
  </div>
  <div class="nav-right">
    <a class="nav-btn" href="chem_lab1.1.html">切换 VSEPR 分子模型 <span class="arr">→</span></a>
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
      <h2 id="crysName">—</h2>
      <div class="tag-wrap" id="tagWrap"></div>
      <p class="info-desc" id="crysDesc"></p>
    </div>
    <div class="panel-section">
      <div class="panel-title">微粒透明度</div>
      <div class="slider-wrap">
        <input type="range" id="opacitySlider" min="0.1" max="1.0" step="0.01" value="0.85">
        <div class="slider-tip" id="opacityTip">透明度 0.85</div>
      </div>
    </div>
    <div class="panel-section">
      <div class="panel-title">晶胞延展范围</div>
      <div class="slider-wrap">
        <input type="range" id="cellExtendSlider" min="0" max="1" step="0.01" value="0">
        <div class="slider-tip" id="sliderTip">仅显示中心 1 个晶胞</div>
      </div>
    </div>
    <div class="panel-section">
      <div class="panel-title">粒子图例</div>
      <div class="legend-row" id="legendWrap"></div>
    </div>
    <div class="panel-section">
      <div class="panel-title">晶胞边界切割</div>
      <div class="switch-row">
        <span class="switch-label">沿晶胞边界切平</span>
        <div class="switch" id="clipCellSwitch"></div>
      </div>
      <p class="info-desc">顶点微粒只留 1/8，棱上留 1/4，面上留 1/2——真实呈现晶胞分摊。</p>
    </div>
  </div>

  <div class="canvas-box">
    <canvas id="crystalCanvas"></canvas>
    <div class="proj-modal" id="projModal">
      <h3>二维投影点阵图 <button class="proj-close" id="closeProj">×</button></h3>
      <select class="proj-select" id="projViewSelect">
        <option value="001">俯视 c 轴 [001]</option>
        <option value="100">俯视 a 轴 [100]</option>
        <option value="010">俯视 b 轴 [010]</option>
        <option value="110">对角视图 [110]</option>
      </select>
      <canvas class="proj-canvas" id="projCanvas"></canvas>
    </div>
  </div>

  <div class="side right-panel">
    <div class="panel-section">
      <div class="panel-title">晶体大类</div>
      <select class="select-box" id="crystalTypeSel">
        <option value="ion">离子晶体</option>
        <option value="metal">金属晶体</option>
        <option value="covalent">共价晶体</option>
        <option value="molecule">分子晶体</option>
        <option value="mix">混合型晶体</option>
      </select>
    </div>
    <div class="panel-section">
      <div class="panel-title">晶体物质</div>
      <select class="select-box" id="crystalMatSel"></select>
    </div>
    <div class="panel-section">
      <div class="panel-title">显示样式</div>
      <select class="select-box" id="modelStyleSel">
        <option value="ballstick">球棍模型</option>
        <option value="spacefill">比例模型（相邻粒子相切）</option>
      </select>
    </div>
    <div class="panel-section" id="speciesSection">
      <div class="panel-title">微粒显隐</div>
      <div id="speciesToggles"></div>
    </div>
    <div class="panel-section">
      <div class="panel-title">点阵投影分析</div>
      <button class="func-btn" id="openProjBtn">打开二维投影面板</button>
    </div>
  </div>
</div>
"""

HTML = """<!DOCTYPE html>
<html lang="zh-CN" data-theme="washi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>晶体结构深度实验室 | 生活中的化学 · 教学实验室</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;500;700;800&family=Noto+Serif+SC:wght@400;500;700;900&family=Noto+Sans+SC:wght@300;400;500;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<script src="../vendor/three.min.js"></script>
<style>__CSS__
</style>
</head>
<body>__BODY__
<script>
__THEME__
</script>
<script>
__DATA__
__ENGINE__
</script>
</body>
</html>
"""

out = (HTML
       .replace("__CSS__", CSS)
       .replace("__BODY__", BODY)
       .replace("__THEME__", THEME_JS)
       .replace("__DATA__", data_js)
       .replace("__ENGINE__", ENGINE_JS))
OLD.write_text(out, encoding="utf-8")
print("written:", OLD, len(out), "bytes")
