# -*- coding: utf-8 -*-
"""
生成 VSEPR 分子构型实验室 chem_lab1.1.html
三大类：无机分子结构 / 离子团结构(正、负) / 有机分子结构，每类 40+ 种
外壳（CSS + 主题 JS）提取自已定稿的 chem_lab1.2.html
"""
import json, math, re
import numpy as np

LAB12 = r"C:\Users\风逝\Documents\kimi\tasks\2026-08-31\06-27-38-247a26cf\chem-life-main\public\teaching\chem_lab1.2.html"
OUT   = r"C:\Users\风逝\Documents\kimi\tasks\2026-08-31\06-27-38-247a26cf\chem-life-main\public\teaching\chem_lab1.1.html"

old = open(LAB12, encoding="utf-8").read()
CSS = re.search(r"<style>(.*?)</style>", old, re.S).group(1)
THEME_JS = re.search(r"/\* =+ 主题切换 washi / sumi / ai =+ \*/\s*\(function\(\)\{.*?\}\)\(\);", old, re.S).group(0)

# ================= 几何模板（单位向量） =================
def V(x, y, z):
    v = np.array([x, y, z], float)
    return v / np.linalg.norm(v)

T_LINEAR = [V(1,0,0), V(-1,0,0)]
T_TRIG   = [V(1,0,0), V(-0.5, math.sqrt(3)/2, 0), V(-0.5, -math.sqrt(3)/2, 0)]
T_TETRA  = [V(1,1,1), V(1,-1,-1), V(-1,1,-1), V(-1,-1,1)]
T_TBP    = [V(1,0,0), V(-0.5, math.sqrt(3)/2, 0), V(-0.5,-math.sqrt(3)/2,0), V(0,0,1), V(0,0,-1)]  # 前 3 赤道，后 2 轴向
T_OCT    = [V(1,0,0), V(-1,0,0), V(0,1,0), V(0,-1,0), V(0,0,1), V(0,0,-1)]
T_SQPL   = [V(1,0,0), V(-1,0,0), V(0,1,0), V(0,-1,0)]  # 平面四方 dsp2

TEMPLATE = {"sp": T_LINEAR, "sp2": T_TRIG, "sp3": T_TETRA, "sp3d": T_TBP, "sp3d2": T_OCT, "dsp2": T_SQPL,
            "term": [V(0,0,-1)]}  # 端基：仅占 1 个槽，不补 H
HYB_LABEL = {"sp":"sp", "sp2":"sp²", "sp3":"sp³", "sp3d":"sp³d", "sp3d2":"sp³d²", "dsp2":"dsp²", "term":"—"}

def rot_align(a, b):
    """把向量 a 旋转到 b 的旋转矩阵（Rodrigues）"""
    a = a / np.linalg.norm(a); b = b / np.linalg.norm(b)
    c = np.cross(a, b); d = float(np.dot(a, b))
    if np.linalg.norm(c) < 1e-9:
        if d > 0: return np.eye(3)
        # 反向：任选垂直轴转 180°
        axis = np.cross(a, [1.0,0,0])
        if np.linalg.norm(axis) < 1e-6: axis = np.cross(a, [0,1.0,0])
        axis = axis / np.linalg.norm(axis)
        K = np.array([[0,-axis[2],axis[1]],[axis[2],0,-axis[0]],[-axis[1],axis[0],0]])
        return np.eye(3) + 2 * K @ K
    K = np.array([[0,-c[2],c[1]],[c[2],0,-c[0]],[-c[1],c[0],0]])
    return np.eye(3) + K + K @ K * ((1 - d) / (np.linalg.norm(c) ** 2))

def rot_axis(axis, ang):
    axis = axis / np.linalg.norm(axis)
    K = np.array([[0,-axis[2],axis[1]],[axis[2],0,-axis[0]],[-axis[1],axis[0],0]])
    return np.eye(3) + math.sin(ang)*K + (1-math.cos(ang))*K@K

# ================= 元素数据 =================
ELEM = {  # 颜色, 显示半径, 共价半径
 "H":  (0xf2f2f0, 0.26, 0.31), "C": (0x5b6470, 0.40, 0.76), "N": (0x3b82f6, 0.38, 0.71),
 "O":  (0xef4444, 0.38, 0.66), "F": (0x34d399, 0.36, 0.57), "Cl":(0x22c55e, 0.50, 1.02),
 "Br": (0xb45309, 0.55, 1.20), "I": (0x8b5cf6, 0.62, 1.39), "S": (0xeab308, 0.50, 1.05),
 "P":  (0xf97316, 0.52, 1.07), "B": (0xf4a7b9, 0.42, 0.84), "Si":(0xc2b280, 0.55, 1.11),
 "Xe": (0x7dd3fc, 0.60, 1.40), "Be":(0x84cc16, 0.45, 0.96), "Hg":(0x9ca3af, 0.62, 1.32),
 "Sn": (0x94a3b8, 0.60, 1.39), "Ge":(0xa8a29e, 0.56, 1.20), "Al":(0xcbd5e1, 0.58, 1.21),
 "As": (0xd6a4a4, 0.55, 1.19), "Sb":(0xc08497, 0.60, 1.39), "Se":(0xfbbf24, 0.52, 1.20),
 "Te": (0xd97706, 0.58, 1.38), "Mn":(0xc084fc, 0.58, 1.39), "Cr":(0x8d99ae, 0.58, 1.39),
 "Cu": (0xd08770, 0.60, 1.32), "Ag":(0xe5e7eb, 0.62, 1.45), "Zn":(0xbac7d1, 0.60, 1.22),
 "Na": (0xa78bfa, 0.62, 1.66), "K": (0x8b5cf6, 0.66, 2.03),
}

BL = {  # 键长表：frozenset({a,b}) -> {order: len}
 frozenset(("C","C")):{1:1.54,2:1.34,3:1.20,1.5:1.40}, frozenset(("C","H")):{1:1.09},
 frozenset(("C","N")):{1:1.47,2:1.27,3:1.16,1.5:1.33}, frozenset(("C","O")):{1:1.43,2:1.23,3:1.13,1.5:1.26},
 frozenset(("C","S")):{1:1.82,2:1.56}, frozenset(("C","Cl")):{1:1.77}, frozenset(("C","F")):{1:1.35},
 frozenset(("C","Br")):{1:1.94}, frozenset(("N","H")):{1:1.01}, frozenset(("N","N")):{1:1.45,2:1.25,3:1.10,1.5:1.30},
 frozenset(("N","O")):{1:1.36,2:1.20,1.5:1.24}, frozenset(("O","H")):{1:0.96}, frozenset(("O","O")):{1:1.48,2:1.21},
 frozenset(("O","Cl")):{1:1.70}, frozenset(("S","H")):{1:1.34}, frozenset(("S","O")):{1:1.60,2:1.43,1.5:1.49},
 frozenset(("S","Cl")):{1:2.00}, frozenset(("S","S")):{1:2.05}, frozenset(("P","O")):{1:1.60,2:1.50,1.5:1.55},
 frozenset(("P","Cl")):{1:2.04}, frozenset(("P","F")):{1:1.54}, frozenset(("P","Br")):{1:2.20},
 frozenset(("P","H")):{1:1.42}, frozenset(("B","F")):{1:1.30}, frozenset(("B","Cl")):{1:1.74},
 frozenset(("B","Br")):{1:1.87}, frozenset(("B","H")):{1:1.19}, frozenset(("Si","H")):{1:1.48},
 frozenset(("Si","F")):{1:1.60}, frozenset(("Si","Cl")):{1:2.02}, frozenset(("Si","O")):{1:1.63},
 frozenset(("H","H")):{1:0.74}, frozenset(("F","F")):{1:1.42}, frozenset(("Cl","Cl")):{1:1.99},
 frozenset(("Br","Br")):{1:2.28}, frozenset(("I","I")):{1:2.66}, frozenset(("H","F")):{1:0.92},
 frozenset(("H","Cl")):{1:1.27}, frozenset(("H","Br")):{1:1.41}, frozenset(("H","I")):{1:1.61},
 frozenset(("Xe","F")):{1:2.00}, frozenset(("Be","Cl")):{1:1.75}, frozenset(("Be","H")):{1:1.33},
 frozenset(("Hg","Cl")):{1:2.30}, frozenset(("Sn","Cl")):{1:2.40}, frozenset(("Ge","H")):{1:1.53},
 frozenset(("Al","Cl")):{1:2.13}, frozenset(("Al","F")):{1:1.70}, frozenset(("As","H")):{1:1.52},
 frozenset(("As","F")):{1:1.71}, frozenset(("Sb","F")):{1:1.88}, frozenset(("Se","F")):{1:1.69},
 frozenset(("Se","H")):{1:1.46}, frozenset(("Te","F")):{1:1.84}, frozenset(("Br","F")):{1:1.76},
 frozenset(("Cl","F")):{1:1.63}, frozenset(("I","F")):{1:1.91}, frozenset(("I","Cl")):{1:2.30},
 frozenset(("Mn","O")):{1:1.60,2:1.58,1.5:1.60}, frozenset(("Cr","O")):{1:1.65,2:1.60,1.5:1.65},
 frozenset(("Cu","N")):{1:2.00}, frozenset(("Ag","N")):{1:2.10}, frozenset(("Zn","N")):{1:2.00},
 frozenset(("N","F")):{1:1.37}, frozenset(("N","Cl")):{1:1.75}, frozenset(("O","F")):{1:1.42},
}
def bond_len(a, b, order):
    t = BL.get(frozenset((a, b)))
    if t and order in t: return t[order]
    if t:  #  nearest order
        k = min(t, key=lambda x: abs(x - order)); base = t[k]
        return base * (0.87 if order == 2 else 0.78 if order == 3 else 0.93 if order == 1.5 else 1)
    r = ELEM[a][2] + ELEM[b][2]
    return round(r * (1.0 if order == 1 else 0.87 if order == 2 else 0.78 if order == 3 else 0.93), 3)

# ================= 输出结构 =================
# mol = {"atoms":[[el,x,y,z],...], "bonds":[[i,j,order],...], "lp":[[atomIdx,x,y,z],...] (方向端点)}

SUB = {0:"₀",1:"₁",2:"₂",3:"₃",4:"₄",5:"₅",6:"₆",7:"₇",8:"₈",9:"₉"}
def sub(n):
    return "" if n == 1 else "".join(SUB[int(c)] for c in str(n))
SUP = {"+":"⁺","-":"⁻","2+":"²⁺","3+":"³⁺","2-":"²⁻","3-":"³⁻","4-":"⁴⁻"}

def formula_of(atoms, charge=""):
    from collections import Counter
    cnt = Counter(a[0] for a in atoms)
    parts = []
    for el in (["C","H"] if "C" in cnt else sorted(cnt)):
        if el in cnt: parts.append(el + sub(cnt.pop(el)))
    for el in sorted(cnt): parts.append(el + sub(cnt[el]))
    return "".join(parts) + SUP.get(charge, charge)

SHAPE = {  # (steric, m) -> (形状, 键角)
 (1,1):("直线形","—"), (2,1):("直线形","—"), (3,1):("直线形","—"), (4,1):("直线形","—"),
 (2,2):("直线形","180°"), (3,3):("平面三角形","120°"), (3,2):("V 形","≈119°"),
 (4,4):("正四面体形","109°28′"), (4,3):("三角锥形","≈107°"), (4,2):("V 形","≈104.5°"),
 (5,5):("三角双锥形","90°/120°"), (5,4):("变形四面体(跷跷板)形","≈89°/117°"), (5,3):("T 形","≈87.5°"), (5,2):("直线形","180°"),
 (6,6):("正八面体形","90°"), (6,5):("四方锥形","≈90°"), (6,4):("平面正方形","90°"),
}

def axe(m, n): return f"AX{m}" + (f"E{n}" if n else "")

MOLS = []  # {id,name,cat,sub,formula,axe,shape,hyb,angle,desc,mol}

def reg(id, name, cat, sub_, mol, desc, axe_=None, shape=None, hyb=None, angle=None):
    MOLS.append({"id": id, "name": name, "cat": cat, "sub": sub_,
                 "formula": name.split(" ")[0],
                 "axe": axe_ or "", "shape": shape or "", "hyb": hyb or "", "angle": angle or "",
                 "desc": desc, "mol": {"atoms": [[a[0]] + [round(float(v),4) for v in a[1:]] for a in mol["atoms"]],
                                        "bonds": mol["bonds"], "lp": mol.get("lp", [])}})

# ---------- 单中心构造器 ----------
def single(center_el, ligs, n_lp, charge="", hyb=None):
    """ligs: [(el, order)]；自动选模板、摆孤对。返回 mol"""
    m = len(ligs); sn = m + n_lp
    hyb = hyb or {1:"sp",2:"sp",3:"sp2",4:"sp3",5:"sp3d",6:"sp3d2"}[sn]
    slots = list(TEMPLATE[hyb])
    # 孤对优先占位规则
    if sn == 5:   # 孤对优先进赤道位（前 3）
        lp_slots = slots[:3][:n_lp]; bond_slots = slots[3:] + slots[:3][n_lp:]
    elif sn == 6: # 孤对优先占 ±z（第 5、6 位）
        lp_slots = (slots[4:6] + slots[:4])[:n_lp]; bond_slots = (slots[:4] + slots[4:6])[n_lp:]
    else:
        lp_slots = slots[m:]; bond_slots = slots[:m]
    atoms = [[center_el, 0,0,0]]; bonds = []; lp = []
    for (el, o), d in zip(ligs, bond_slots):
        L = bond_len(center_el, el, o)
        p = d * L
        atoms.append([el, *p]); bonds.append([0, len(atoms)-1, o])
    for d in lp_slots:
        atoms.append(["Lp", *(d * 1.05)]); lp.append([len(atoms)-1])
    shape, ang = SHAPE.get((sn, m), ("", ""))
    return {"atoms": atoms, "bonds": bonds, "lp": lp, "charge": charge}, axe(m, n_lp), shape, HYB_LABEL[hyb], ang

# ---------- 多中心引擎 ----------
def engine(centers, bonds, subst=None, charge="", lp_map=None):
    """
    centers: [{"el","hyb","pos":None|np.array,"slots":None|[dirs]}]  固定中心给 pos+slots
    bonds: [(i,j,order)]   subst: {i:[el,...]} 开放槽位填充（默认 H）
    lp_map: {i: n_lp} 覆盖默认孤对数
    """
    subst = subst or {}; lp_map = lp_map or {}
    n = len(centers)
    adj = [[] for _ in range(n)]
    for i, j, o in bonds: adj[i].append((j, o)); adj[j].append((i, o))
    pos = [None]*n; slot_world = [None]*n; used = [set() for _ in range(n)]
    # 固定中心
    for i, c in enumerate(centers):
        if c.get("pos") is not None:
            pos[i] = np.asarray(c["pos"], float)
            slot_world[i] = [np.asarray(s, float) for s in c["slots"]]
    # 固定中心之间的键：把对应槽位标记为已用
    for i, j, o in bonds:
        for a, b in ((i, j), (j, i)):
            if pos[a] is not None and pos[b] is not None:
                d = pos[b] - pos[a]; d = d / np.linalg.norm(d)
                k = max(range(len(slot_world[a])), key=lambda si: float(np.dot(slot_world[a][si], d)))
                used[a].add(k)
    # BFS 摆放自由中心
    placed = [i for i in range(n) if pos[i] is not None]
    queue = list(placed)
    if not queue:
        pos[0] = np.zeros(3); slot_world[0] = [s.copy() for s in TEMPLATE[centers[0]["hyb"]]]
        queue = [0]
    visited = set(queue)
    while queue:
        i = queue.pop(0)
        for j, o in adj[i]:
            if j in visited: continue
            visited.add(j)
            # 找 i 的空闲槽方向
            d = None
            for si, s in enumerate(slot_world[i]):
                if si not in used[i]: d = s; used[i].add(si); break
            if d is None: raise RuntimeError(f"center {i} no free slot")
            L = bond_len(centers[i]["el"], centers[j]["el"], o)
            pos[j] = pos[i] + d * L
            tmpl = [s.copy() for s in TEMPLATE[centers[j]["hyb"]]]
            # 对齐：槽 0 指向 -d
            R = rot_align(tmpl[0], -d)
            tmpl = [R @ s for s in tmpl]
            # 扭转
            bond_axis = d
            if centers[j]["hyb"] == centers[i]["hyb"] == "sp2":
                # 两个 sp2 中心（共轭）：p 轨道平行 → 法向量平行
                n_i = np.cross(slot_world[i][0], slot_world[i][1]); 
                best, ba = -1e9, 0
                for k in range(24):
                    a = k * math.pi/12
                    n_j = rot_axis(bond_axis, a) @ np.cross(tmpl[0], tmpl[1])
                    sc = abs(float(np.dot(n_i/ np.linalg.norm(n_i), n_j/ np.linalg.norm(n_j))))
                    if sc > best: best, ba = sc, a
            else:
                # 交错式：最大化与母体其余键的投影夹角
                others_i = [s for si, s in enumerate(slot_world[i]) if si in used[i] or abs(float(np.dot(s, d))) < 0.9]
                best, ba = -1e9, 0
                for k in range(24):
                    a = k * math.pi/12
                    sc_min = 1e9
                    for si, s in enumerate(tmpl):
                        if si == 0: continue
                        sp = rot_axis(bond_axis, a) @ s
                        sp = sp - np.dot(sp, bond_axis)*bond_axis
                        if np.linalg.norm(sp) < 1e-6: continue
                        for t in others_i:
                            tp = t - np.dot(t, bond_axis)*bond_axis
                            if np.linalg.norm(tp) < 1e-6: continue
                            ang = abs(float(np.dot(sp/ np.linalg.norm(sp), tp/ np.linalg.norm(tp))))
                            sc_min = min(sc_min, ang)
                    if -sc_min > best: best, ba = -sc_min, a
            Rt = rot_axis(bond_axis, ba)
            slot_world[j] = [Rt @ s for s in tmpl]
            used[j].add(0)
            queue.append(j)
    # 孤对数
    def default_lp(i):
        el, hyb = centers[i]["el"], centers[i]["hyb"]
        nb = len(adj[i])
        if el == "O": return 2 if hyb == "sp3" else (2 if hyb == "sp2" else (1 if hyb == "sp" else 0))
        if el == "N": return 1 if hyb in ("sp3","sp2") and nb < 4 else 0
        if el == "S": return 2 if hyb == "sp3" and nb <= 2 else 0
        if el in ("F","Cl","Br","I"): return 0
        return 0
    atoms = []; bonds_out = []; lp = []; info = []
    for i in range(n):
        atoms.append([centers[i]["el"], *pos[i]])
    for i, j, o in bonds: bonds_out.append([i, j, o])
    # 填充开放槽：先孤对，再指定取代基，最后补 H
    for i in range(n):
        if centers[i]["hyb"] == "term":
            info.append({"m": len(adj[i]), "n": 0}); continue
        fill = list(subst.get(i, []))
        nlp = lp_map.get(i, default_lp(i))
        total_slots = len(slot_world[i])
        free = [si for si in range(total_slots) if si not in used[i]]
        # 孤对
        cnt_lp = 0
        for si in free[:nlp]:
            d = slot_world[i][si]
            atoms.append(["Lp", *(pos[i] + d * 1.0)]); lp.append([len(atoms)-1])
            used[i].add(si); cnt_lp += 1
        # 取代基 / H
        for si in range(total_slots):
            if si in used[i]: continue
            el = fill.pop(0) if fill else "H"
            if el is None: used[i].add(si); continue  # None = 留空
            d = slot_world[i][si]
            L = bond_len(centers[i]["el"], el, 1)
            atoms.append([el, *(pos[i] + d * L)])
            bonds_out.append([i, len(atoms)-1, 1])
            used[i].add(si)
        info.append({"m": len(used[i]) - cnt_lp, "n": cnt_lp})
    return {"atoms": atoms, "bonds": bonds_out, "lp": lp, "charge": charge, "info": info}

print("part1 loaded ok")

# ================= 注册包装 =================
def regS(id, name, cat, sub_, center, ligs, n_lp, charge="", note="", hyb=None):
    mol, ax, shape, hy, ang = single(center, ligs, n_lp, charge, hyb)
    m = len(ligs)
    desc = f"中心 {center} 原子 {hy} 杂化，{m} 个成键电子对、{n_lp} 对孤电子对，{shape}，键角 {ang}。"
    if note: desc += note
    reg(id, name, cat, sub_, mol, desc, ax, shape, hy, ang)

def regE(id, name, cat, sub_, centers, bonds, subst=None, charge="", note="", lp_map=None):
    mol = engine(centers, bonds, subst, charge, lp_map)
    parts = []
    for i, c in enumerate(centers):
        if c["hyb"] == "term": continue
        inf = mol["info"][i]; m, n_ = inf["m"], inf["n"]
        shape, _ = SHAPE.get((m + n_, m), ("", ""))
        parts.append(f"{c['el']}{i+1}：{HYB_LABEL[c['hyb']]} 杂化·{axe(m, n_)}" + (f"·{shape}" if shape else ""))
    segs = [p.split("：", 1) for p in parts]
    if len(parts) > 2 and len(set(g[1] for g in segs)) == 1:
        el0 = segs[0][0].rstrip("0123456789")
        desc = f"每个 {el0}（共 {len(parts)} 个）：{segs[0][1]}。" + note
    else:
        desc = "；".join(parts) + "。" + note
    reg(id, name, cat, sub_, mol, desc)

def regR(id, name, cat, sub_, centers, bonds, charge="", note="", lp_map=None, subst=None):
    """固定几何（环等），centers 已含 pos/slots；不做 BFS 扩展时 bonds 可闭合成环"""
    mol = engine(centers, bonds, subst, charge, lp_map)
    parts = []
    for i, c in enumerate(centers):
        if c["hyb"] == "term": continue
        inf = mol["info"][i]; m, n_ = inf["m"], inf["n"]
        shape, _ = SHAPE.get((m + n_, m), ("", ""))
        parts.append(f"{c['el']}{i+1}：{HYB_LABEL[c['hyb']]} 杂化·{axe(m, n_)}" + (f"·{shape}" if shape else ""))
    segs = [p.split("：", 1) for p in parts]
    if len(parts) > 2 and len(set(g[1] for g in segs)) == 1:
        el0 = segs[0][0].rstrip("0123456789")
        desc = f"每个 {el0}（共 {len(parts)} 个）：{segs[0][1]}。" + note
    else:
        desc = "；".join(parts) + "。" + note
    reg(id, name, cat, sub_, mol, desc)

def C_(h="sp3"): return {"el": "C", "hyb": h}
def N_(h="sp3"): return {"el": "N", "hyb": h}
def O_(h="sp3"): return {"el": "O", "hyb": h}
def T_(el): return {"el": el, "hyb": "term"}

def fixed_center(el, hyb, pos, bond_dirs, extra):
    """固定中心：slots = 键方向 + 额外开放槽方向"""
    slots = [np.asarray(d, float)/np.linalg.norm(d) for d in bond_dirs]
    slots += [np.asarray(d, float)/np.linalg.norm(d) for d in extra]
    return {"el": el, "hyb": hyb, "pos": np.asarray(pos, float), "slots": slots}

def ring_extra(d_neigh, hyb):
    """已知环上键方向，按杂化补开放槽：sp2 → 1 个外向；sp3 → 2 个"""
    if len(d_neigh) >= 3: return []
    s = -np.sum(d_neigh, 0)
    out = s / np.linalg.norm(s)
    if len(d_neigh) == 2:
        if hyb == "sp2":
            return [out]
        z = np.cross(d_neigh[0], d_neigh[1])
        z = z / np.linalg.norm(z)
        h1 = out + z * 1.35; h2 = out - z * 1.35
        return [h1/np.linalg.norm(h1), h2/np.linalg.norm(h2)]
    return [out]

def make_ring(el_list, hyb_list, pos_list, edges, lp_of=None):
    """通用固定环构造。返回 (centers, bonds)。lp_of: {i:n} 在开放槽里放孤对（靠 lp_map 控制）"""
    adj = [[] for _ in pos_list]
    for i, j, o in edges: adj[i].append(j); adj[j].append(i)
    centers = []
    for i, p in enumerate(pos_list):
        d_neigh = [np.asarray(pos_list[k], float) - np.asarray(p, float) for k in adj[i]]
        d_neigh = [d/np.linalg.norm(d) for d in d_neigh]
        centers.append(fixed_center(el_list[i], hyb_list[i], p, d_neigh, ring_extra(d_neigh, hyb_list[i])))
    bonds = [(i, j, o) for i, j, o in edges]
    return centers, bonds

# ---------- 苯环 ----------
def benzene_ring():
    a = 1.40
    pos = [(a*math.cos(math.pi/3*k), a*math.sin(math.pi/3*k), 0.0) for k in range(6)]
    edges = [(k, (k+1) % 6, 1.5) for k in range(6)]
    return pos, edges

def phenyl_plus(name_tail_pos=0):
    """苯环固定中心 + 在 C0 外向位留一个键口。返回 (centers, bonds)，C0 的开放槽是外向"""
    pos, edges = benzene_ring()
    centers, bonds = make_ring(["C"]*6, ["sp2"]*6, pos, edges)
    return centers, bonds

# ---------- 萘 ----------
def naphthalene():
    a = 1.40; cx = a*math.sqrt(3)/2
    S1 = (0, a/2, 0.0); S2 = (0, -a/2, 0.0)
    left = [(-cx + a*math.cos(math.radians(t)), a*math.sin(math.radians(t)), 0.0) for t in (90,150,210,270)]
    right = [(cx + a*math.cos(math.radians(t)), a*math.sin(math.radians(t)), 0.0) for t in (90,30,-30,-90)]
    pos = [S1, S2] + left + right
    # 左环：S1(0)-L0(2)-L1(3)-L2(4)-L3(5)-S2(1)；右环：S1-R0(6)-R1(7)-R2(8)-R3(9)-S2
    edges = [(0,2,1.5),(2,3,1.5),(3,4,1.5),(4,5,1.5),(5,1,1.5),(1,0,1.5),
             (0,6,1.5),(6,7,1.5),(7,8,1.5),(8,9,1.5),(9,1,1.5)]
    return pos, edges

# ---------- 环己烷椅式（D3d） ----------
def chair_pos():
    r, h = 1.452, 0.2567
    A = [math.radians(t) for t in (0, 120, 240)]
    B = [math.radians(t) for t in (60, 180, 300)]
    pos = []
    for k in range(3):
        pos.append((r*math.cos(A[k]), r*math.sin(A[k]), h))
        pos.append((r*math.cos(B[k]), r*math.sin(B[k]), -h))
    return pos  # 交替 A,B；边 (i, i+1), (5, 0)

# ============================ 无机分子结构 ============================
IN = "inorg"
regS("h2",  "H₂ 氢气", IN, "", "H", [("H",1)], 0, note="非极性共价键，s-s σ 键。")
regS("n2",  "N₂ 氮气", IN, "", "N", [("N",3)], 1, hyb="sp", note="1 个 σ 键 + 2 个 π 键，叁键很稳定。")
regS("o2",  "O₂ 氧气", IN, "", "O", [("O",2)], 2, hyb="sp2", note="1 个 σ 键 + 1 个 π 键。")
regS("f2",  "F₂ 氟气", IN, "", "F", [("F",1)], 3)
regS("cl2", "Cl₂ 氯气", IN, "", "Cl", [("Cl",1)], 3)
regS("br2", "Br₂ 溴", IN, "", "Br", [("Br",1)], 3)
regS("i2",  "I₂ 碘", IN, "", "I", [("I",1)], 3)
regS("hf",  "HF 氟化氢", IN, "", "F", [("H",1)], 3)
regS("hcl", "HCl 氯化氢", IN, "", "Cl", [("H",1)], 3)
regS("hbr", "HBr 溴化氢", IN, "", "Br", [("H",1)], 3)
regS("hi",  "HI 碘化氢", IN, "", "I", [("H",1)], 3)
regS("co",  "CO 一氧化碳", IN, "", "C", [("O",3)], 1, hyb="sp", note="C≡O 配位键，结构与 N₂ 相似（等电子体）。")
regS("no",  "NO 一氧化氮", IN, "", "N", [("O",2)], 1, hyb="sp2", note="含 1 个未成对电子的顺磁性分子。")

regS("co2",  "CO₂ 二氧化碳", IN, "", "C", [("O",2),("O",2)], 0, note="2 个 σ 键 + 2 个 π 键，直线形非极性分子。")
regS("cs2",  "CS₂ 二硫化碳", IN, "", "C", [("S",2),("S",2)], 0)
regS("cos",  "COS 羰基硫", IN, "", "C", [("O",2),("S",2)], 0)
regS("hcn",  "HCN 氰化氢", IN, "", "C", [("H",1),("N",3)], 0, note="含 C≡N 叁键，直线形，剧毒。")
regS("becl2","BeCl₂ 氯化铍", IN, "", "Be", [("Cl",1),("Cl",1)], 0, note="Be 最外层仅 4 电子，缺电子分子。")
regS("beh2", "BeH₂ 氢化铍", IN, "", "Be", [("H",1),("H",1)], 0)
regS("hgcl2","HgCl₂ 氯化汞", IN, "", "Hg", [("Cl",1),("Cl",1)], 0)
regE("n2o",  "N₂O 一氧化二氮（笑气）", IN, "", [N_("sp"), T_("N"), T_("O")],
     [(0,1,2),(0,2,2)], charge="", note="直线形 N-N-O，共振结构 N≡N⁺-O⁻ ↔ N⁻=N⁺=O。")

regS("bf3",  "BF₃ 三氟化硼", IN, "", "B", [("F",1)]*3, 0, note="B 最外层 6 电子，缺电子，是路易斯酸。")
regS("bcl3", "BCl₃ 三氯化硼", IN, "", "B", [("Cl",1)]*3, 0)
regS("bbr3", "BBr₃ 三溴化硼", IN, "", "B", [("Br",1)]*3, 0)
regS("alcl3","AlCl₃ 三氯化铝", IN, "", "Al", [("Cl",1)]*3, 0, note="气态单体为平面三角形；实际上常以 Al₂Cl₆ 二聚体存在。")
regS("so3",  "SO₃ 三氧化硫", IN, "", "S", [("O",1.5)]*3, 0, note="S=O 键高度共振，3 个 S-O 键完全等同。")
regS("cocl2","COCl₂ 光气", IN, "", "C", [("O",2),("Cl",1),("Cl",1)], 0, note="平面三角形，剧毒。")
regS("cof2", "COF₂ 碳酰氟", IN, "", "C", [("O",2),("F",1),("F",1)], 0)

regS("nh3",  "NH₃ 氨气", IN, "", "N", [("H",1)]*3, 1, note="1 对孤对电子压缩键角至约 107°，三角锥形，极性分子。")
regS("ph3",  "PH₃ 磷化氢", IN, "", "P", [("H",1)]*3, 1)
regS("ash3", "AsH₃ 砷化氢", IN, "", "As", [("H",1)]*3, 1)
regS("pcl3", "PCl₃ 三氯化磷", IN, "", "P", [("Cl",1)]*3, 1)
regS("pbr3", "PBr₃ 三溴化磷", IN, "", "P", [("Br",1)]*3, 1)
regS("pf3",  "PF₃ 三氟化磷", IN, "", "P", [("F",1)]*3, 1)
regS("ncl3", "NCl₃ 三氯化氮", IN, "", "N", [("Cl",1)]*3, 1)
regS("nf3",  "NF₃ 三氟化氮", IN, "", "N", [("F",1)]*3, 1)
regS("ascl3","AsCl₃ 三氯化砷", IN, "", "As", [("Cl",1)]*3, 1)
regS("socl2","SOCl₂ 氯化亚砜", IN, "", "S", [("O",1),("Cl",1),("Cl",1)], 1, note="三角锥形，常用氯化剂。")

regS("h2o",  "H₂O 水", IN, "", "O", [("H",1)]*2, 2, note="2 对孤对电子使键角压缩至 104.5°，V 形强极性分子。")
regS("h2s",  "H₂S 硫化氢", IN, "", "S", [("H",1)]*2, 2)
regS("h2se", "H₂Se 硒化氢", IN, "", "Se", [("H",1)]*2, 2)
regS("of2",  "OF₂ 二氟化氧", IN, "", "O", [("F",1)]*2, 2)
regS("ocl2", "Cl₂O 一氧化二氯", IN, "", "O", [("Cl",1)]*2, 2)
regS("scl2", "SCl₂ 二氯化硫", IN, "", "S", [("Cl",1)]*2, 2)
regS("so2",  "SO₂ 二氧化硫", IN, "", "S", [("O",1.5),("O",1.5)], 1, note="V 形，S=O 键共振等同，是酸雨的主要成因。")
regS("o3",   "O₃ 臭氧", IN, "", "O", [("O",1.5),("O",1.5)], 1, note="V 形，含离域 π 键（π₃⁴），O-O 键等长。")
regS("no2",  "NO₂ 二氧化氮", IN, "", "N", [("O",1.5),("O",1.5)], 1, note="V 形，含 1 个未成对电子，红棕色。")

regS("sih4", "SiH₄ 硅烷", IN, "", "Si", [("H",1)]*4, 0)
regS("sif4", "SiF₄ 四氟化硅", IN, "", "Si", [("F",1)]*4, 0)
regS("sicl4","SiCl₄ 四氯化硅", IN, "", "Si", [("Cl",1)]*4, 0)
regS("geh4", "GeH₄ 锗烷", IN, "", "Ge", [("H",1)]*4, 0)
regS("sncl4","SnCl₄ 四氯化锡", IN, "", "Sn", [("Cl",1)]*4, 0)
regS("pocl3","POCl₃ 三氯氧磷", IN, "", "P", [("O",2),("Cl",1),("Cl",1),("Cl",1)], 0)
regS("so2cl2","SO₂Cl₂ 磺酰氯", IN, "", "S", [("O",2),("O",2),("Cl",1),("Cl",1)], 0)

regS("pcl5", "PCl₅ 五氯化磷", IN, "", "P", [("Cl",1)]*5, 0, note="三角双锥：轴向键比赤道键长。")
regS("pf5",  "PF₅ 五氟化磷", IN, "", "P", [("F",1)]*5, 0)
regS("pbr5", "PBr₅ 五溴化磷", IN, "", "P", [("Br",1)]*5, 0)
regS("asf5", "AsF₅ 五氟化砷", IN, "", "As", [("F",1)]*5, 0)
regS("sbf5", "SbF₅ 五氟化锑", IN, "", "Sb", [("F",1)]*5, 0)
regS("sf4",  "SF₄ 四氟化硫", IN, "", "S", [("F",1)]*4, 1, note="孤对占赤道位，呈变形四面体（跷跷板形）。")
regS("sef4", "SeF₄ 四氟化硒", IN, "", "Se", [("F",1)]*4, 1)
regS("clf3", "ClF₃ 三氟化氯", IN, "", "Cl", [("F",1)]*3, 2, note="2 对孤对占赤道位，分子呈 T 形。")
regS("brf3", "BrF₃ 三氟化溴", IN, "", "Br", [("F",1)]*3, 2)
regS("xef2", "XeF₂ 二氟化氙", IN, "", "Xe", [("F",1)]*2, 3, note="3 对孤对全占赤道位，分子为直线形。")
regS("sf6",  "SF₆ 六氟化硫", IN, "", "S", [("F",1)]*6, 0, note="正八面体形，极其稳定，用作绝缘气体。")
regS("sef6", "SeF₆ 六氟化硒", IN, "", "Se", [("F",1)]*6, 0)
regS("tef6", "TeF₆ 六氟化碲", IN, "", "Te", [("F",1)]*6, 0)
regS("brf5", "BrF₅ 五氟化溴", IN, "", "Br", [("F",1)]*5, 1, note="孤对与底部 4 个 F 相对，呈四方锥形。")
regS("if5",  "IF₅ 五氟化碘", IN, "", "I", [("F",1)]*5, 1)
regS("clf5", "ClF₅ 五氟化氯", IN, "", "Cl", [("F",1)]*5, 1)
regS("xef4", "XeF₄ 四氟化氙", IN, "", "Xe", [("F",1)]*4, 2, note="2 对孤对上下相对，分子为平面正方形。")

regE("h2o2", "H₂O₂ 过氧化氢", IN, "", [O_(), O_()], [(0,1,1)],
     note="非平面的'半开书本'形，二面角约 111°，O-O 键易断裂。")
regE("n2h4", "N₂H₄ 肼（联氨）", IN, "", [N_(), N_()], [(0,1,1)],
     note="每个 N 各有 1 对孤对电子，火箭燃料。")
regE("hno3", "HNO₃ 硝酸", IN, "", [N_("sp2"), O_("sp2"), O_(), O_()],
     [(0,1,2),(0,2,1),(0,3,1)], lp_map={2:3}, note="平面形分子，N=O 与 N-O⁻ 共振，-OH 上的 H 可电离。")
regE("h2so4","H₂SO₄ 硫酸", IN, "", [{"el":"S","hyb":"sp3"}, O_("sp2"), O_("sp2"), O_(), O_()],
     [(0,1,2),(0,2,2),(0,3,1),(0,4,1)], note="S 为四面体构型，2 个 S=O、2 个 S-OH。")
regE("h3po4","H₃PO₄ 磷酸", IN, "", [{"el":"P","hyb":"sp3"}, O_("sp2"), O_(), O_(), O_()],
     [(0,1,2),(0,2,1),(0,3,1),(0,4,1)], note="1 个 P=O、3 个 P-OH，三元中强酸。")
regE("hclo", "HClO 次氯酸", IN, "", [O_()], [], subst={0:["Cl","H"]},
     note="结构为 H-O-Cl，O 为 V 形中心，84 消毒液有效成分的母体。")

print("inorganic:", sum(1 for m in MOLS if m["cat"] == "inorg"))

# ============================ 离子团结构 ============================
CAT, AN = "ion", "ion"  # cat 都是 ion，用 sub 区分 cat/anion
# ---------- 阳离子 ----------
regS("nh4p", "NH₄⁺ 铵根离子", CAT, "cat", "N", [("H",1)]*4, 0, "+", note="N-H 中有 1 个配位键，4 个键完全等同。")
regS("h3op", "H₃O⁺ 水合氢离子", CAT, "cat", "O", [("H",1)]*3, 1, "+", note="三角锥形，酸溶液中 H⁺ 的实际存在形式。")
regS("ph4p", "PH₄⁺ 鏻离子", CAT, "cat", "P", [("H",1)]*4, 0, "+")
regS("no2p", "NO₂⁺ 硝酰正离子", CAT, "cat", "N", [("O",2),("O",2)], 0, "+", note="直线形，与 CO₂ 等电子。")
regS("ch3p", "CH₃⁺ 甲基碳正离子", CAT, "cat", "C", [("H",1)]*3, 0, "+", note="平面三角形，空 p 轨道垂直于平面，亲电反应中间体。")
regE("n2h5p", "N₂H₅⁺ 肼鎓离子", CAT, "cat", [N_(), N_()], [(0,1,1)], charge="+",
     lp_map={1:0}, note="一端正电 N 无孤对（4 键），另一端 N 保留 1 对孤对。")
regE("nh3ohp", "NH₃OH⁺ 羟胺鎓离子", CAT, "cat", [N_(), O_()], [(0,1,1)], charge="+",
     lp_map={0:0}, note="NH₂OH 质子化产物。")
regE("ch3nh3p", "CH₃NH₃⁺ 甲胺鎓离子", CAT, "cat", [C_(), N_()], [(0,1,1)], charge="+",
     lp_map={1:0}, note="甲胺结合 H⁺ 后的形式，N 上 4 键无孤对。")
regE("c2h5nh3p", "C₂H₅NH₃⁺ 乙胺鎓离子", CAT, "cat", [C_(), C_(), N_()], [(0,1,1),(1,2,1)],
     charge="+", lp_map={2:0})
regE("me2nh2p", "(CH₃)₂NH₂⁺ 二甲胺鎓离子", CAT, "cat", [N_(), C_(), C_()], [(0,1,1),(0,2,1)],
     charge="+", lp_map={0:0})
regE("me3nhp", "(CH₃)₃NH⁺ 三甲胺鎓离子", CAT, "cat", [N_(), C_(), C_(), C_()],
     [(0,1,1),(0,2,1),(0,3,1)], charge="+", lp_map={0:0})
regE("agnh32p", "[Ag(NH₃)₂]⁺ 银氨离子", CAT, "cat", [{"el":"Ag","hyb":"sp"}, N_(), N_()],
     [(0,1,1),(0,2,1)], charge="+", lp_map={1:0,2:0},
     note="直线形配离子，N 的孤对电子配位给 Ag⁺，银镜反应与银氨溶液的核心。")
regE("cunh34p", "[Cu(NH₃)₄]²⁺ 四氨合铜离子", CAT, "cat",
     [{"el":"Cu","hyb":"dsp2"}, N_(), N_(), N_(), N_()],
     [(0,1,1),(0,2,1),(0,3,1),(0,4,1)], charge="2+", lp_map={1:0,2:0,3:0,4:0},
     note="平面正方形配离子，深蓝色，检验 Cu²⁺ 的特征现象。")
regE("znnh34p", "[Zn(NH₃)₄]²⁺ 四氨合锌离子", CAT, "cat",
     [{"el":"Zn","hyb":"sp3"}, N_(), N_(), N_(), N_()],
     [(0,1,1),(0,2,1),(0,3,1),(0,4,1)], charge="2+", lp_map={1:0,2:0,3:0,4:0},
     note="正四面体配离子，Zn(OH)₂ 溶于浓氨水的产物。")

# ---------- 阴离子 ----------
regS("ohm", "OH⁻ 氢氧根离子", AN, "anion", "O", [("H",1)], 3, "-")
regS("hsm", "HS⁻ 硫氢根离子", AN, "anion", "S", [("H",1)], 3, "-")
regS("cnm", "CN⁻ 氰根离子", AN, "anion", "C", [("N",3)], 1, "-", hyb="sp", note="与 N₂、CO 等电子，C 端孤对配位能力强。")
regS("no2m", "NO₂⁻ 亚硝酸根", AN, "anion", "N", [("O",1.5),("O",1.5)], 1, "-", note="V 形。")
regS("no3m", "NO₃⁻ 硝酸根", AN, "anion", "N", [("O",1.5)]*3, 0, "-", note="平面三角形，π₄⁶ 大 π 键，3 个 N-O 键等同。")
regS("co3m", "CO₃²⁻ 碳酸根", AN, "anion", "C", [("O",1.5)]*3, 0, "2-", note="平面三角形，π₄⁶ 大 π 键。")
regS("so3m", "SO₃²⁻ 亚硫酸根", AN, "anion", "S", [("O",1.5)]*3, 1, "2-", note="三角锥形。")
regS("so4m", "SO₄²⁻ 硫酸根", AN, "anion", "S", [("O",1.5)]*4, 0, "2-", note="正四面体形，S-O 键共振等同。")
regS("po4m", "PO₄³⁻ 磷酸根", AN, "anion", "P", [("O",1.5)]*4, 0, "3-")
regS("clo4m", "ClO₄⁻ 高氯酸根", AN, "anion", "Cl", [("O",1.5)]*4, 0, "-")
regS("clo3m", "ClO₃⁻ 氯酸根", AN, "anion", "Cl", [("O",1.5)]*3, 1, "-", note="三角锥形。")
regS("bro3m", "BrO₃⁻ 溴酸根", AN, "anion", "Br", [("O",1.5)]*3, 1, "-")
regS("io3m", "IO₃⁻ 碘酸根", AN, "anion", "I", [("O",1.5)]*3, 1, "-")
regS("clo2m", "ClO₂⁻ 亚氯酸根", AN, "anion", "Cl", [("O",1.5),("O",1.5)], 2, "-", note="V 形。")
regS("clom", "ClO⁻ 次氯酸根", AN, "anion", "Cl", [("O",1)], 3, "-", note="84 消毒液的有效成分。")
regS("mno4m", "MnO₄⁻ 高锰酸根", AN, "anion", "Mn", [("O",1.5)]*4, 0, "-", note="正四面体形，紫红色，强氧化剂。")
regS("mno42m", "MnO₄²⁻ 锰酸根", AN, "anion", "Mn", [("O",1.5)]*4, 0, "2-", note="绿色。")
regS("cro4m", "CrO₄²⁻ 铬酸根", AN, "anion", "Cr", [("O",1.5)]*4, 0, "2-", note="黄色，与重铬酸根存在平衡。")
regS("bf4m", "BF₄⁻ 四氟硼酸根", AN, "anion", "B", [("F",1)]*4, 0, "-", note="B 接受 F⁻ 孤对形成配位键。")
regS("pf6m", "PF₆⁻ 六氟磷酸根", AN, "anion", "P", [("F",1)]*6, 0, "-")
regS("sif6m", "SiF₆²⁻ 六氟合硅酸根", AN, "anion", "Si", [("F",1)]*6, 0, "2-")
regS("alf6m", "AlF₆³⁻ 六氟合铝酸根", AN, "anion", "Al", [("F",1)]*6, 0, "3-", note="冰晶石 Na₃AlF₆ 的组成部分。")
regS("i3m", "I₃⁻ 三碘离子", AN, "anion", "I", [("I",1),("I",1)], 3, "-", note="直线形：3 对孤对占赤道位。碘酒中 I₂ 溶于 KI 的产物。")
regS("nh2m", "NH₂⁻ 氨基负离子", AN, "anion", "N", [("H",1),("H",1)], 2, "-")
regE("scnm", "SCN⁻ 硫氰酸根", AN, "anion", [C_("sp"), T_("S"), T_("N")],
     [(0,1,1),(0,2,3)], charge="-", note="直线形，检验 Fe³⁺ 的试剂（生成红色配合物）。")
regE("ocnm", "OCN⁻ 氰酸根", AN, "anion", [C_("sp"), T_("N"), T_("O")],
     [(0,1,3),(0,2,1)], charge="-")
regE("n3m", "N₃⁻ 叠氮根", AN, "anion", [N_("sp"), T_("N"), T_("N")],
     [(0,1,2),(0,2,2)], charge="-", note="直线形，与 CO₂ 等电子，汽车安全气囊的原理物质。")
regE("o2m2", "O₂²⁻ 过氧根", AN, "anion", [O_(), O_()], [(0,1,1)], charge="2-",
     lp_map={0:3,1:3}, note="Na₂O₂、H₂O₂ 中的过氧结构，O-O 单键。")
regE("hco3m", "HCO₃⁻ 碳酸氢根", AN, "anion", [C_("sp2"), O_("sp2"), O_(), O_()],
     [(0,1,2),(0,2,1),(0,3,1)], charge="-", lp_map={2:3},
     note="平面三角形骨架，1 个 C=O、1 个 C-O⁻、1 个 C-OH。")
regE("hcoom", "HCOO⁻ 甲酸根", AN, "anion", [C_("sp2"), O_("sp2"), O_()],
     [(0,1,2),(0,2,1)], charge="-", lp_map={2:3}, subst={0:["H"]},
     note="2 个 C-O 键共振等同。")
regE("ch3coom", "CH₃COO⁻ 乙酸根", AN, "anion", [C_(), C_("sp2"), O_("sp2"), O_()],
     [(0,1,1),(1,2,2),(1,3,1)], charge="-", lp_map={3:3},
     note="羧基 2 个 C-O 键共振等同，甲基为四面体。")
regE("hso4m", "HSO₄⁻ 硫酸氢根", AN, "anion", [{"el":"S","hyb":"sp3"}, O_("sp2"), O_("sp2"), O_("sp2"), O_()],
     [(0,1,1.5),(0,2,1.5),(0,3,1.5),(0,4,1)], charge="-")
regE("hpo4m", "HPO₄²⁻ 磷酸氢根", AN, "anion", [{"el":"P","hyb":"sp3"}, O_("sp2"), O_("sp2"), O_("sp2"), O_()],
     [(0,1,1.5),(0,2,1.5),(0,3,1.5),(0,4,1)], charge="2-")
regE("h2po4m", "H₂PO₄⁻ 磷酸二氢根", AN, "anion", [{"el":"P","hyb":"sp3"}, O_("sp2"), O_("sp2"), O_(), O_()],
     [(0,1,1.5),(0,2,1.5),(0,3,1),(0,4,1)], charge="-")
regE("cr2o7m", "Cr₂O₇²⁻ 重铬酸根", AN, "anion",
     [{"el":"Cr","hyb":"sp3"}, {"el":"Cr","hyb":"sp3"}, O_(), T_("O"), T_("O"), T_("O"), T_("O"), T_("O"), T_("O")],
     [(0,2,1),(1,2,1),(0,3,1.5),(0,4,1.5),(0,5,1.5),(1,6,1.5),(1,7,1.5),(1,8,1.5)],
     charge="2-", lp_map={2:2}, note="2 个 CrO₄ 四面体共用 1 个顶点 O，橙色，强氧化剂。")
regE("aloh4m", "[Al(OH)₄]⁻ 四羟基合铝酸根", AN, "anion",
     [{"el":"Al","hyb":"sp3"}, O_(), O_(), O_(), O_()],
     [(0,1,1),(0,2,1),(0,3,1),(0,4,1)], charge="-",
     note="Al(OH)₃ 溶于强碱的产物（旧教材写作 AlO₂⁻）。")

print("ions:", sum(1 for m in MOLS if m["cat"] == "ion"),
      " cat:", sum(1 for m in MOLS if m["sub"] == "cat"),
      " anion:", sum(1 for m in MOLS if m["sub"] == "anion"))

# ============================ 有机分子结构 ============================
OR = "org"
# ---- 烷烃 ----
regS("ch4", "CH₄ 甲烷", OR, "", "C", [("H",1)]*4, 0, note="最简单的有机物，天然气主要成分。")
regE("c2h6", "C₂H₆ 乙烷", OR, "", [C_(), C_()], [(0,1,1)],
     note="C-C 单键可旋转，交错式构象最稳定。")
regE("c3h8", "C₃H₈ 丙烷", OR, "", [C_(), C_(), C_()], [(0,1,1),(1,2,1)], note="液化石油气主要成分。")
regE("c4h10", "C₄H₁₀ 正丁烷", OR, "", [C_(), C_(), C_(), C_()], [(0,1,1),(1,2,1),(2,3,1)])
regE("ic4h10", "C₄H₁₀ 异丁烷（2-甲基丙烷）", OR, "", [C_(), C_(), C_(), C_()],
     [(0,1,1),(0,2,1),(0,3,1)], note="正丁烷的同分异构体，中心碳为叔碳。")
regE("c5h12", "C₅H₁₂ 正戊烷", OR, "", [C_(), C_(), C_(), C_(), C_()],
     [(0,1,1),(1,2,1),(2,3,1),(3,4,1)])
# 环丙烷
_cy3_pos = [(0.872*math.cos(math.radians(t)), 0.872*math.sin(math.radians(t)), 0.0) for t in (0,120,240)]
_cy3_c, _cy3_b = make_ring(["C"]*3, ["sp3"]*3, _cy3_pos, [(0,1,1),(1,2,1),(2,0,1)])
regR("cy3", "C₃H₆ 环丙烷", OR, "", _cy3_c, _cy3_b,
     note="三元环张力极大（键角 60°），香蕉形弯曲键。")
# 环己烷椅式
_ch_pos = chair_pos()
_ch_edges = [(i,(i+1)%6,1) for i in range(6)]
_ch_c, _ch_b = make_ring(["C"]*6, ["sp3"]*6, _ch_pos, _ch_edges)
regR("cy6", "C₆H₁₂ 环己烷（椅式构象）", OR, "", _ch_c, _ch_b,
     note="椅式构象最稳定，C-H 分直立键(a键)与平伏键(e键)。")

# ---- 烯/炔 ----
regE("c2h4", "C₂H₄ 乙烯", OR, "", [C_("sp2"), C_("sp2")], [(0,1,2)],
     note="平面形分子，C=C 为 1 σ + 1 π，π 键不能旋转。")
regE("c3h6", "C₃H₆ 丙烯", OR, "", [C_(), C_("sp2"), C_("sp2")], [(0,1,1),(1,2,2)])
regE("b1ene", "C₄H₈ 1-丁烯", OR, "", [C_("sp2"), C_("sp2"), C_(), C_()],
     [(0,1,2),(1,2,1),(2,3,1)])
regE("b2ene", "C₄H₈ 2-丁烯", OR, "", [C_(), C_("sp2"), C_("sp2"), C_()],
     [(0,1,1),(1,2,2),(2,3,1)], note="双键两侧存在顺反异构（图示为反式）。")
regE("b13diene", "C₄H₆ 1,3-丁二烯", OR, "", [C_("sp2")]*4,
     [(0,1,2),(1,2,1),(2,3,2)], note="共轭二烯，π 电子离域，橡胶的单体骨架。")
regE("c2h2", "C₂H₂ 乙炔", OR, "", [C_("sp"), C_("sp")], [(0,1,3)],
     note="直线形，C≡C 为 1 σ + 2 π，电石气。")
regE("c3h4", "C₃H₄ 丙炔", OR, "", [C_(), C_("sp"), C_("sp")], [(0,1,1),(1,2,3)])
regE("b1yne", "C₄H₆ 1-丁炔", OR, "", [C_("sp"), C_("sp"), C_(), C_()],
     [(0,1,3),(1,2,1),(2,3,1)])
regE("b2yne", "C₄H₆ 2-丁炔", OR, "", [C_(), C_("sp"), C_("sp"), C_()],
     [(0,1,1),(1,2,3),(2,3,1)])

# ---- 芳香族 ----
_bz_c, _bz_b = phenyl_plus()
regR("benzene", "C₆H₆ 苯", OR, "", _bz_c, _bz_b,
     note="平面正六边形，π₆⁶ 大 π 键，6 个 C-C 键完全等同（介于单双键之间）。")
_bz_c, _bz_b = phenyl_plus()
regE("toluene", "C₇H₈ 甲苯", OR, "", _bz_c + [C_()], _bz_b + [(0,6,1)],
     note="甲基使苯环邻对位活化。")
_bz_c, _bz_b = phenyl_plus()
regE("phenol", "C₆H₆O 苯酚", OR, "", _bz_c + [O_()], _bz_b + [(0,6,1)],
     note="羟基直接连苯环，弱酸性（石炭酸）。")
_bz_c, _bz_b = phenyl_plus()
regE("aniline", "C₆H₇N 苯胺", OR, "", _bz_c + [N_()], _bz_b + [(0,6,1)],
     note="氨基的孤对电子与苯环共轭，碱性弱于脂肪胺。")
_bz_c, _bz_b = phenyl_plus()
regR("chlorobenzene", "C₆H₅Cl 氯苯", OR, "", _bz_c, _bz_b, subst={0:["Cl"]},
     note="Cl 与苯环 p-π 共轭，C-Cl 键难断裂。")
_bz_c, _bz_b = phenyl_plus()
regE("benzoic", "C₇H₆O₂ 苯甲酸", OR, "", _bz_c + [C_("sp2"), O_("sp2"), O_()],
     _bz_b + [(0,6,1),(6,7,2),(6,8,1)], note="常用食品防腐剂。")
_bz_c, _bz_b = phenyl_plus()
regE("benzaldehyde", "C₇H₆O 苯甲醛", OR, "", _bz_c + [C_("sp2"), O_("sp2")],
     _bz_b + [(0,6,1),(6,7,2)], note="苦杏仁气味。")
_bz_c, _bz_b = phenyl_plus()
regE("styrene", "C₈H₈ 苯乙烯", OR, "", _bz_c + [C_("sp2"), C_("sp2")],
     _bz_b + [(0,6,1),(6,7,2)], note="聚苯乙烯塑料的单体，整体共平面共轭。")
_na_pos, _na_edges = naphthalene()
_na_c, _na_b = make_ring(["C"]*10, ["sp2"]*10, _na_pos, _na_edges)
regR("naphthalene", "C₁₀H₈ 萘", OR, "", _na_c, _na_b,
     note="两个苯环稠合，π₁₀¹⁰ 离域，卫生球（樟脑丸）的传统成分。")

# ---- 醇 / 醚 ----
regE("meoh", "CH₄O 甲醇", OR, "", [C_(), O_()], [(0,1,1)],
     note="工业酒精，有毒（致盲）。")
regE("etoh", "C₂H₆O 乙醇", OR, "", [C_(), C_(), O_()], [(0,1,1),(1,2,1)],
     note="酒精的主要成分，O 为 V 形中心。")
regE("proh1", "C₃H₈O 1-丙醇", OR, "", [C_(), C_(), C_(), O_()], [(0,1,1),(1,2,1),(2,3,1)])
regE("proh2", "C₃H₈O 2-丙醇（异丙醇）", OR, "", [C_(), C_(), C_(), O_()],
     [(0,1,1),(1,2,1),(1,3,1)], note="常用消毒擦拭剂。")
regE("eg", "C₂H₆O₂ 乙二醇", OR, "", [C_(), C_(), O_(), O_()], [(0,1,1),(0,2,1),(1,3,1)],
     note="汽车防冻液主要成分。")
regE("glycerol", "C₃H₈O₃ 丙三醇（甘油）", OR, "",
     [C_(), C_(), C_(), O_(), O_(), O_()],
     [(0,1,1),(1,2,1),(0,3,1),(1,4,1),(2,5,1)], note="护肤品保湿剂，硝酸甘油的母体。")
regE("dme", "C₂H₆O 甲醚", OR, "", [C_(), O_(), C_()], [(0,1,1),(1,2,1)],
     note="乙醇的同分异构体，O 为 V 形。")
regE("dee", "C₄H₁₀O 乙醚", OR, "", [C_(), C_(), O_(), C_(), C_()],
     [(0,1,1),(1,2,1),(2,3,1),(3,4,1)], note="早期麻醉剂。")
_eo_pos = [(-0.735,0,0), (0.735,0,0), (0, 1.204, 0)]
_eo_c, _eo_b = make_ring(["C","C","O"], ["sp3","sp3","sp3"], _eo_pos,
                         [(0,1,1),(1,2,1),(2,0,1)])
regR("eo", "C₂H₄O 环氧乙烷", OR, "", _eo_c, _eo_b, lp_map={2:2},
     note="三元环醚，张力大易开环，医用消毒剂。")

# ---- 醛 / 酮 / 酸 / 酯 ----
regE("hcho", "CH₂O 甲醛", OR, "", [C_("sp2"), O_("sp2")], [(0,1,2)],
     note="平面三角形，福尔马林、装修污染的主角。")
regE("ch3cho", "C₂H₄O 乙醛", OR, "", [C_(), C_("sp2"), O_("sp2")], [(0,1,1),(1,2,2)])
regE("acetone", "C₃H₆O 丙酮", OR, "", [C_(), C_("sp2"), O_("sp2"), C_()],
     [(0,1,1),(1,2,2),(1,3,1)], note="羰基平面三角形，常见有机溶剂。")
regE("hcooh", "CH₂O₂ 甲酸（蚁酸）", OR, "", [C_("sp2"), O_("sp2"), O_()],
     [(0,1,2),(0,2,1)], subst={0:["H"]}, note="羧基为平面结构，C=O 与 C-OH 有明显区别。")
regE("ch3cooh", "C₂H₄O₂ 乙酸（醋酸）", OR, "", [C_(), C_("sp2"), O_("sp2"), O_()],
     [(0,1,1),(1,2,2),(1,3,1)], note="食醋的主要成分。")
regE("mf", "C₂H₄O₂ 甲酸甲酯", OR, "", [C_("sp2"), O_("sp2"), O_(), C_()],
     [(0,1,2),(0,2,1),(2,3,1)], subst={0:["H"]}, note="乙酸的同分异构体。")
regE("ea", "C₄H₈O₂ 乙酸乙酯", OR, "", [C_(), C_("sp2"), O_("sp2"), O_(), C_(), C_()],
     [(0,1,1),(1,2,2),(1,3,1),(3,4,1),(4,5,1)],
     note="水果香味，酯化反应的经典产物。")

# ---- 含氮 ----
regE("menh2", "CH₅N 甲胺", OR, "", [C_(), N_()], [(0,1,1)],
     note="N 为三角锥形，1 对孤对电子，有碱性。")
regE("me2nh", "C₂H₇N 二甲胺", OR, "", [N_(), C_(), C_()], [(0,1,1),(0,2,1)])
regE("me3n", "C₃H₉N 三甲胺", OR, "", [N_(), C_(), C_(), C_()], [(0,1,1),(0,2,1),(0,3,1)])
regE("urea", "CH₄N₂O 尿素", OR, "", [C_("sp2"), O_("sp2"), N_(), N_()],
     [(0,1,2),(0,2,1),(0,3,1)], note="第一个人工合成的有机物（维勒，1828）。")
regE("gly", "C₂H₅NO₂ 甘氨酸", OR, "", [N_(), C_(), C_("sp2"), O_("sp2"), O_()],
     [(0,1,1),(1,2,1),(2,3,2),(2,4,1)], note="最简单的氨基酸，氨基 + 羧基连在同一碳链上。")
regE("mecn", "C₂H₃N 乙腈", OR, "", [C_(), C_("sp"), T_("N")], [(0,1,1),(1,2,3)],
     note="含 C≡N 叁键，常用极性溶剂。")
regE("meno2", "CH₃NO₂ 硝基甲烷", OR, "", [C_(), N_("sp2"), O_("sp2"), O_()],
     [(0,1,1),(1,2,2),(1,3,1)], lp_map={3:3},
     note="硝基中 N=O 与 N-O⁻ 共振，2 个 N-O 键等同。")

# ---- 卤代烃 ----
regE("ch3cl", "CH₃Cl 一氯甲烷", OR, "", [C_()], [], subst={0:["Cl"]})
regE("ch2cl2", "CH₂Cl₂ 二氯甲烷", OR, "", [C_()], [], subst={0:["Cl","Cl"]},
     note="常用萃取溶剂，四面体但不是正四面体。")
regE("chcl3", "CHCl₃ 三氯甲烷（氯仿）", OR, "", [C_()], [], subst={0:["Cl","Cl","Cl"]},
     note="早期麻醉剂，光照下生成光气。")
regE("ccl4", "CCl₄ 四氯化碳", OR, "", [C_()], [], subst={0:["Cl","Cl","Cl","Cl"]},
     note="正四面体，非极性分子，曾用灭火剂。")
regE("vc", "C₂H₃Cl 氯乙烯", OR, "", [C_("sp2"), C_("sp2")], [(0,1,2)], subst={1:["Cl"]},
     note="PVC 塑料的单体。")
regE("dce", "C₂H₄Cl₂ 1,2-二氯乙烷", OR, "", [C_(), C_()], [(0,1,1)], subst={0:["Cl"],1:["Cl"]})
regE("c2f4", "C₂F₄ 四氟乙烯", OR, "", [C_("sp2"), C_("sp2")], [(0,1,2)],
     subst={0:["F","F"],1:["F","F"]}, note="特氟龙（PTFE）的单体。")
regE("cf4", "CF₄ 四氟化碳", OR, "", [C_()], [], subst={0:["F","F","F","F"]})

print("organic:", sum(1 for m in MOLS if m["cat"] == "org"))
print("total:", len(MOLS))

# ================= HTML / JS 组装 =================
HTML_TMPL = r"""<!DOCTYPE html>
<html lang="zh-CN" data-theme="washi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VSEPR 分子构型实验室 | 生活中的化学 · 教学实验室</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;500;700;800&family=Noto+Serif+SC:wght@400;500;700;900&family=Noto+Sans+SC:wght@300;400;500;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<script src="../vendor/three.min.js"></script>
<style>
__CSS__

/* ---- VSEPR 页专用 ---- */
#molCanvas{width:100%;height:100%;display:block;}
.mol-formula{font-family:var(--mono);font-size:13px;letter-spacing:2px;color:var(--accent);margin:-4px 0 10px;}
.search-input{
  width:100%;padding:8px 12px;background:var(--surface-2);border:1px solid var(--line);
  border-radius:999px;font-size:12.5px;color:var(--ink);font-family:var(--sans-cn);outline:none;
}
.search-input:focus{border-color:var(--accent);}
.acc{margin-bottom:8px;border:1px solid var(--line);border-radius:10px;overflow:hidden;}
.acc-head{
  display:flex;justify-content:space-between;align-items:center;cursor:pointer;
  padding:10px 12px;background:var(--paper);user-select:none;
}
.acc-head .t{font-family:var(--serif-cn);font-weight:700;font-size:13.5px;letter-spacing:1px;}
.acc-head .n{font-family:var(--mono);font-size:10px;color:var(--ink-mute);}
.acc-head .chev{transition:transform .25s;color:var(--ink-mute);font-size:12px;}
.acc.open .acc-head .chev{transform:rotate(90deg);}
.acc-body{display:none;padding:6px 8px 10px;background:var(--surface);}
.acc.open .acc-body{display:block;}
.sub-label{
  font-family:var(--mono);font-size:10px;letter-spacing:2px;color:var(--ink-mute);
  margin:8px 4px 4px;text-transform:uppercase;
}
.mol-item{
  display:flex;justify-content:space-between;align-items:baseline;gap:8px;
  padding:6px 10px;border-radius:7px;cursor:pointer;font-size:12.5px;color:var(--ink-dim);
  transition:background .2s,color .2s;
}
.mol-item:hover{background:var(--accent-soft);color:var(--accent);}
.mol-item.active{background:var(--accent-soft);color:var(--accent);font-weight:600;}
.mol-item .f{font-family:var(--mono);font-size:11px;color:var(--ink-mute);flex:none;}
.mol-item.active .f{color:var(--accent);}
#navToggle{
  display:none;position:absolute;right:14px;top:14px;z-index:40;
  padding:7px 14px;border-radius:999px;border:1px solid var(--accent);
  background:var(--accent-soft);color:var(--accent);font-size:12.5px;cursor:pointer;
  font-family:var(--sans-cn);
}
.main-wrap{position:relative;}
@media (max-width:1100px){
  #navToggle{display:inline-flex;}
  .right-panel{
    position:absolute;top:0;right:0;height:100%;z-index:35;
    transform:translateX(102%);transition:transform .3s;
    box-shadow:-12px 0 30px rgba(0,0,0,.3);
  }
  .right-panel.open{transform:none;}
}
.canvas-hint{
  position:absolute;left:14px;bottom:12px;font-family:var(--mono);font-size:10px;
  letter-spacing:1.5px;color:rgba(230,235,242,.45);pointer-events:none;
}
</style>
</head>
<body>
<nav class="topnav">
  <div class="brand">
    <span class="badge">形</span>
    <h1>VSEPR 分子构型实验室</h1>
    <span class="lecture-tag">STRUCTURE · LAB 01</span>
  </div>
  <div class="nav-right">
    <a class="nav-btn" href="chem_lab1.2.html">切换 晶体结构实验室 <span class="arr">→</span></a>
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
  <div class="side left-panel" style="width:280px">
    <div class="info-card">
      <h2 id="molName">—</h2>
      <div class="mol-formula" id="molFormula"></div>
      <div class="tag-wrap" id="tagWrap"></div>
      <p class="info-desc" id="molDesc"></p>
    </div>
    <div class="panel-section">
      <div class="panel-title">显示控制</div>
      <div class="switch-row"><span class="switch-label"><span class="legend-ball" style="background:#6aa6dd;margin-right:5px"></span>σ 键电子云</span><div class="switch active" id="tgSigma"></div></div>
      <div class="switch-row"><span class="switch-label"><span class="legend-ball" style="background:#e06b6b;margin-right:5px"></span>π 键电子云</span><div class="switch active" id="tgPi"></div></div>
      <div class="switch-row"><span class="switch-label"><span class="legend-ball" style="background:#b89ae8;margin-right:5px"></span>孤对电子云</span><div class="switch active" id="tgLone"></div></div>
      <div class="switch-row"><span class="switch-label">云内悬浮光点</span><div class="switch active" id="tgDots"></div></div>
      <div class="switch-row"><span class="switch-label">自动旋转</span><div class="switch active" id="tgSpin"></div></div>
    </div>
    <div class="panel-section">
      <div class="panel-title">电子云浓度</div>
      <div class="slider-wrap">
        <input type="range" id="cloudSlider" min="0.3" max="1.3" step="0.01" value="0.85">
        <div class="slider-tip" id="cloudTip">浓度 0.85</div>
      </div>
    </div>
  </div>
  <div class="canvas-box">
    <canvas id="molCanvas"></canvas>
    <button id="navToggle">分子库 ☰</button>
    <div class="canvas-hint">拖动旋转 · 滚轮缩放 · 右栏切换分子</div>
  </div>
  <div class="side right-panel" style="width:300px">
    <div class="panel-section">
      <div class="panel-title">搜索分子</div>
      <input class="search-input" id="searchInput" placeholder="输入名称 / 分子式…">
    </div>
    <div id="navBox"></div>
  </div>
</div>

<script>
__THEME_JS__

/* ================= 数据 ================= */
const ELEM = __ELEM__;
const MOLS = __DATA__;

const COL = {
  sigma: 0x6aa6dd, sigmaDots: 0xbfdcff,
  pi:    0xe06b6b, piDots:   0xffc2b8,
  lone:  0xb89ae8, loneDots: 0xe4d4ff,
  stick: 0xc8ccd4,
};

/* ================= 场景 ================= */
const canvas = document.getElementById('molCanvas');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0d1017);
const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 200);
scene.add(new THREE.AmbientLight(0xffffff, 0.75));
const key = new THREE.DirectionalLight(0xffffff, 0.9); key.position.set(4, 6, 5); scene.add(key);
const rim = new THREE.DirectionalLight(0x9db8ff, 0.45); rim.position.set(-5, -3, -4); scene.add(rim);
const root = new THREE.Group(); scene.add(root);

let fitR = 2.5, fitDir = new THREE.Vector3(0.42, 0.3, 0.86).normalize();
function fitCamera(R){
  fitR = R;
  const vfov = camera.fov * Math.PI / 180;
  const distH = R / Math.tan(vfov / 2);
  const distW = R / (Math.tan(vfov / 2) * Math.max(camera.aspect, 0.2));
  const dist = Math.max(distH, distW) * 1.12;
  camera.position.copy(fitDir).multiplyScalar(dist);
}
function resize(){
  const w = canvas.parentElement.clientWidth;
  const h = canvas.parentElement.clientHeight;
  renderer.setSize(w, h, false);
  camera.aspect = w / h; camera.updateProjectionMatrix();
  fitCamera(fitR);
}
window.addEventListener('resize', resize);

/* ================= 光点纹理 ================= */
function dotTexture(){
  const c = document.createElement('canvas'); c.width = c.height = 64;
  const g = c.getContext('2d');
  const grd = g.createRadialGradient(32,32,0,32,32,32);
  grd.addColorStop(0, 'rgba(255,255,255,1)');
  grd.addColorStop(0.4, 'rgba(255,255,255,.6)');
  grd.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = grd; g.fillRect(0,0,64,64);
  return new THREE.CanvasTexture(c);
}
const DOT_TEX = dotTexture();

/* ================= 电子云构建 ================= */
const unitSphere = new THREE.SphereGeometry(1, 26, 18);
const anims = [];   // {pts, axis:'x'|'z', speed}
let cloudK = 0.85;

function cloudMat(color, op){
  return new THREE.MeshBasicMaterial({
    color, transparent: true, opacity: op * cloudK,
    blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide,
  });
}
function samplePoints(n, radii){
  const p = new Float32Array(n * 3);
  for (let i = 0; i < n; i++){
    // 严格在椭球内部（半径 ×0.72）
    let x, y, z;
    do { x = Math.random()*2-1; y = Math.random()*2-1; z = Math.random()*2-1; }
    while (x*x + y*y + z*z > 1);
    const r = Math.cbrt(Math.random()) * 0.72;
    const L = Math.hypot(x, y, z) || 1;
    p[i*3]   = x / L * r * radii[0];
    p[i*3+1] = y / L * r * radii[1];
    p[i*3+2] = z / L * r * radii[2];
  }
  return p;
}
function makeCloud(kind, radii, colorMain, colorDots, nDots, axis, speed){
  const g = new THREE.Group();
  g.userData.kind = kind;
  const m1 = new THREE.Mesh(unitSphere, cloudMat(colorMain, 0.17));
  m1.scale.set(...radii);
  const m2 = new THREE.Mesh(unitSphere, cloudMat(colorMain, 0.09));
  m2.scale.set(radii[0]*1.18, radii[1]*1.35, radii[2]*1.35);
  g.add(m1, m2);
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(samplePoints(nDots, radii), 3));
  const pts = new THREE.Points(geo, new THREE.PointsMaterial({
    color: colorDots, size: 0.05, map: DOT_TEX, transparent: true, opacity: 0.9,
    blending: THREE.AdditiveBlending, depthWrite: false, sizeAttenuation: true,
  }));
  pts.userData.isDots = true;
  g.add(pts);
  anims.push({ pts, axis, speed });
  return g;
}
function basisOf(xDir, zHint){
  const x = xDir.clone().normalize();
  let z = zHint.clone().sub(x.clone().multiplyScalar(zHint.dot(x)));
  if (z.length() < 1e-6) z = new THREE.Vector3(0,0,1).sub(x.clone().multiplyScalar(x.z));
  z.normalize();
  const y = new THREE.Vector3().crossVectors(z, x);
  return new THREE.Matrix4().makeBasis(x, y, z);
}

function clearRoot(){
  anims.length = 0;
  while (root.children.length){
    const ch = root.children.pop();
    ch.traverse(o => {
      if (o.geometry && o.geometry !== unitSphere) o.geometry.dispose();
      if (o.material && o.material.dispose) o.material.dispose();
    });
  }
}

function buildMol(id){
  clearRoot();
  const d = MOLS[id];
  const atoms = d.atoms; const bonds = d.bonds;
  const P = atoms.map(a => new THREE.Vector3(a[1], a[2], a[3]));
  const isLp = atoms.map(a => a[0] === 'Lp');

  /* 原子球 + 标签半径 */
  atoms.forEach((a, i) => {
    if (isLp[i]) return;
    const e = ELEM[a[0]] || ELEM.H;
    const m = new THREE.Mesh(unitSphere, new THREE.MeshPhysicalMaterial({
      color: e[0], roughness: 0.28, metalness: 0.15, clearcoat: 0.5,
    }));
    m.position.copy(P[i]); m.scale.setScalar(e[1] * 0.55);
    root.add(m);
  });

  /* 键棍 */
  const stickMat = new THREE.MeshStandardMaterial({ color: COL.stick, roughness: 0.5, metalness: 0.2 });
  bonds.forEach(([i, j, o]) => {
    const A = P[i], B = P[j];
    const dir = B.clone().sub(A); const L = dir.length(); dir.normalize();
    const mk = (off) => {
      const g = new THREE.CylinderGeometry(0.045, 0.045, L, 10);
      const m = new THREE.Mesh(g, stickMat);
      m.position.copy(A).lerp(B, 0.5).add(off);
      m.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0), dir);
      root.add(m);
    };
    const ref = Math.abs(dir.y) < 0.9 ? new THREE.Vector3(0,1,0) : new THREE.Vector3(1,0,0);
    const p1 = new THREE.Vector3().crossVectors(dir, ref).normalize();
    if (o === 2){ mk(p1.clone().multiplyScalar(0.085)); mk(p1.clone().multiplyScalar(-0.085)); }
    else if (o === 3){
      const p2 = new THREE.Vector3().crossVectors(dir, p1).normalize();
      [0, 2.094, 4.189].forEach(a => {
        mk(p1.clone().multiplyScalar(Math.cos(a)*0.11).add(p2.clone().multiplyScalar(Math.sin(a)*0.11)));
      });
    }
    else mk(new THREE.Vector3());
  });

  /* σ 云 */
  bonds.forEach(([i, j]) => {
    const A = P[i], B = P[j];
    const dir = B.clone().sub(A); const L = dir.length();
    const g = makeCloud('sigma', [L*0.52, 0.34, 0.34], COL.sigma, COL.sigmaDots, 42, 'x', 0.010);
    g.position.copy(A).lerp(B, 0.5);
    g.quaternion.setFromUnitVectors(new THREE.Vector3(1,0,0), dir.normalize());
    root.add(g);
  });

  /* π 云 */
  bonds.forEach(([i, j, o]) => {
    if (o < 1.5) return;
    const A = P[i], B = P[j];
    const dir = B.clone().sub(A); const L = dir.length(); dir.normalize();
    const mid = A.clone().lerp(B, 0.5);
    const opK = o === 1.5 ? 0.62 : 1.0;
    if (o === 3){
      // 三键：红色圆柱壳 + σ 已画
      const shell = new THREE.Mesh(
        new THREE.CylinderGeometry(0.42, 0.42, L*0.8, 26, 1, true),
        cloudMat(COL.pi, 0.13));
      shell.position.copy(mid);
      shell.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0), dir);
      const grp = new THREE.Group(); grp.userData.kind = 'pi'; grp.add(shell);
      const geo = new THREE.BufferGeometry();
      const n = 60, pp = new Float32Array(n*3);
      for (let k = 0; k < n; k++){
        const a = Math.random()*Math.PI*2, r = 0.42*(0.75+Math.random()*0.35);
        pp[k*3] = Math.cos(a)*r; pp[k*3+1] = (Math.random()-0.5)*L*0.7; pp[k*3+2] = Math.sin(a)*r;
      }
      geo.setAttribute('position', new THREE.BufferAttribute(pp, 3));
      const pts = new THREE.Points(geo, new THREE.PointsMaterial({
        color: COL.piDots, size: 0.05, map: DOT_TEX, transparent: true, opacity: 0.85,
        blending: THREE.AdditiveBlending, depthWrite: false }));
      pts.userData.isDots = true; grp.add(pts);
      anims.push({ pts, axis: 'y', speed: 0.012 });
      root.add(grp);
    } else {
      // 双键（含 1.5）：上下两个 π 透镜
      const ref = Math.abs(dir.y) < 0.9 ? new THREE.Vector3(0,1,0) : new THREE.Vector3(1,0,0);
      const perp = new THREE.Vector3().crossVectors(dir, ref).normalize();
      [-1, 1].forEach(sgn => {
        const g = makeCloud('pi', [L*0.40, 0.36, 0.15], COL.pi, COL.piDots, 30, 'x', 0.008);
        g.material;
        g.children.forEach(c => { if (c.material) c.material.opacity *= opK; });
        g.position.copy(mid).add(perp.clone().multiplyScalar(sgn * 0.34));
        g.setRotationFromMatrix(basisOf(dir, perp));
        root.add(g);
      });
    }
  });

  /* 孤对云 */
  (d.lp || []).forEach(([li]) => {
    // 找最近的非 Lp 原子作为中心
    let ci = -1, best = 1e9;
    atoms.forEach((a, i) => {
      if (isLp[i]) return;
      const t = P[i].distanceToSquared(P[li]);
      if (t < best){ best = t; ci = i; }
    });
    if (ci < 0) return;
    const dir = P[li].clone().sub(P[ci]).normalize();
    const g = makeCloud('lone', [0.40, 0.40, 0.62], COL.lone, COL.loneDots, 30, 'z', 0.006);
    g.position.copy(P[ci]).add(dir.clone().multiplyScalar(0.55));
    g.setRotationFromMatrix(basisOf(new THREE.Vector3(1,0,0), dir));
    // makeCloud 的椭球长轴在 x：把它转到 dir 上
    g.quaternion.setFromUnitVectors(new THREE.Vector3(1,0,0), dir);
    root.add(g);
  });

  /* 相机取景：同时适配垂直与水平视场 */
  let R = 1.2;
  P.forEach((p, i) => { if (!isLp[i]) R = Math.max(R, p.length() + 0.9); });
  fitCamera(R);
  camera.lookAt(0, 0, 0);

  /* 信息卡 */
  document.getElementById('molName').textContent = d.name;
  document.getElementById('molFormula').textContent = d.formula;
  const tags = [d.catLabel, d.axe, d.shape, d.hyb && (d.hyb + ' 杂化'), d.angle && ('键角 ' + d.angle)].filter(Boolean);
  document.getElementById('tagWrap').innerHTML = tags.map(t => `<span class="info-tag">${t}</span>`).join('');
  document.getElementById('molDesc').textContent = d.desc;
  document.querySelectorAll('.mol-item').forEach(el => el.classList.toggle('active', el.dataset.id === id));
}

/* ================= 显隐开关 ================= */
const kindOn = { sigma: true, pi: true, lone: true };
let dotsOn = true, spinOn = true;
function applyVis(){
  root.traverse(o => {
    const grp = o.userData && o.userData.kind ? o : null;
  });
  root.children.forEach(ch => {
    const k = ch.userData && ch.userData.kind;
    if (!k) return;
    ch.visible = kindOn[k];
    ch.children.forEach(c => { if (c.userData.isDots) c.visible = dotsOn; });
  });
}
function bindSwitch(id, fn){
  const el = document.getElementById(id);
  el.onclick = () => { el.classList.toggle('active'); fn(el.classList.contains('active')); };
}
bindSwitch('tgSigma', v => { kindOn.sigma = v; applyVis(); });
bindSwitch('tgPi',    v => { kindOn.pi = v; applyVis(); });
bindSwitch('tgLone',  v => { kindOn.lone = v; applyVis(); });
bindSwitch('tgDots',  v => { dotsOn = v; applyVis(); });
bindSwitch('tgSpin',  v => { spinOn = v; });
document.getElementById('cloudSlider').oninput = e => {
  cloudK = Number(e.target.value);
  document.getElementById('cloudTip').textContent = '浓度 ' + cloudK.toFixed(2);
  root.traverse(o => {
    if (o.isMesh && o.material && o.material.blending === THREE.AdditiveBlending && o.geometry === unitSphere){
      o.material.opacity = o.material.userData.base ? o.material.userData.base * cloudK : o.material.opacity;
    }
  });
  // 简单可靠：直接重建当前分子
  buildMol(currentId);
};

/* ================= 左栏导航 ================= */
const GROUPS = [
  { key: 'inorg', label: '无机分子结构' },
  { key: 'ion',   label: '离子团结构', subs: [{ key: 'cat', label: '阳离子' }, { key: 'anion', label: '阴离子' }] },
  { key: 'org',   label: '有机分子结构' },
];
const LIST = Object.keys(MOLS).map(id => ({ id, ...MOLS[id] }));
function renderNav(filter){
  const box = document.getElementById('navBox');
  box.innerHTML = '';
  GROUPS.forEach(g => {
    let items = LIST.filter(m => m.cat === g.key);
    const acc = document.createElement('div'); acc.className = 'acc open';
    const head = document.createElement('div'); head.className = 'acc-head';
    head.innerHTML = `<span class="t">${g.label}</span><span class="n"></span><span class="chev">▶</span>`;
    head.onclick = () => acc.classList.toggle('open');
    acc.appendChild(head);
    const body = document.createElement('div'); body.className = 'acc-body';
    const addItems = (arr, subLabel) => {
      const its = arr.filter(m => !filter || m.name.includes(filter) || m.formula.includes(filter));
      if (!its.length) return 0;
      if (subLabel){ const sl = document.createElement('div'); sl.className = 'sub-label'; sl.textContent = subLabel; body.appendChild(sl); }
      its.forEach(m => {
        const el = document.createElement('div');
        el.className = 'mol-item' + (m.id === currentId ? ' active' : '');
        el.dataset.id = m.id;
        el.innerHTML = `<span>${m.name}</span><span class="f">${m.formula}</span>`;
        el.onclick = () => {
          currentId = m.id; buildMol(m.id);
          renderNav(document.getElementById('searchInput').value.trim());
          if (window.innerWidth <= 1100) document.querySelector('.right-panel').classList.remove('open');
        };
        body.appendChild(el);
      });
      return its.length;
    };
    let count = 0;
    if (g.subs){
      g.subs.forEach(s => { count += addItems(items.filter(m => m.sub === s.key), s.label); });
    } else count = addItems(items);
    head.querySelector('.n').textContent = count + ' 种';
    acc.appendChild(body);
    box.appendChild(acc);
  });
}
document.getElementById('searchInput').oninput = e => renderNav(e.target.value.trim());
document.getElementById('navToggle').onclick = () => document.querySelector('.right-panel').classList.toggle('open');

/* ================= 交互 ================= */
let dragging = false, px = 0, py = 0;
canvas.addEventListener('pointerdown', e => { dragging = true; px = e.clientX; py = e.clientY; canvas.setPointerCapture(e.pointerId); });
window.addEventListener('pointerup', () => dragging = false);
window.addEventListener('pointermove', e => {
  if (!dragging) return;
  const dx = (e.clientX - px) * 0.007, dy = (e.clientY - py) * 0.007;
  px = e.clientX; py = e.clientY;
  const qy = new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0,1,0), dx);
  const qx = new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(1,0,0), dy);
  root.quaternion.premultiply(qy).premultiply(qx);
});
canvas.addEventListener('wheel', e => {
  e.preventDefault();
  camera.position.multiplyScalar(e.deltaY > 0 ? 1.07 : 0.93);
}, { passive: false });

/* ================= 主循环 ================= */
const qSpin = new THREE.Quaternion();
function animate(){
  requestAnimationFrame(animate);
  if (spinOn && !dragging){
    qSpin.setFromAxisAngle(new THREE.Vector3(0,1,0), 0.004);
    root.quaternion.premultiply(qSpin);
  }
  anims.forEach(a => {
    if (a.axis === 'x') a.pts.rotation.x += a.speed;
    else if (a.axis === 'y') a.pts.rotation.y += a.speed;
    else a.pts.rotation.z += a.speed;
  });
  renderer.render(scene, camera);
}

let currentId = 'co2';
resize();
renderNav('');
buildMol(currentId);
animate();
</script>
</body>
</html>
"""

ELEM_JS = {el: [c, r] for el, (c, r, _rc) in ELEM.items()}
DATA = {}
CAT_LABEL = {"inorg": "无机分子", "ion": "离子团", "org": "有机分子"}
for m in MOLS:
    DATA[m["id"]] = {
        "name": m["name"], "formula": m["formula"], "cat": m["cat"], "sub": m["sub"],
        "catLabel": CAT_LABEL[m["cat"]], "axe": m["axe"], "shape": m["shape"],
        "hyb": m["hyb"], "angle": m["angle"], "desc": m["desc"],
        "atoms": m["mol"]["atoms"], "bonds": m["mol"]["bonds"], "lp": m["mol"]["lp"],
    }

html = (HTML_TMPL
        .replace("__CSS__", CSS)
        .replace("__THEME_JS__", THEME_JS)
        .replace("__ELEM__", json.dumps(ELEM_JS))
        .replace("__DATA__", json.dumps(DATA, ensure_ascii=False)))
open(OUT, "w", encoding="utf-8").write(html)
print("written:", OUT, len(html), "bytes")
