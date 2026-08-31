// 数据文件：日常物品物质成分库（后续新模块数据可在此目录新增文件）
export interface MaterialRow {
  category: string
  item: string
  part: string
  common: string
  chemName: string
  formula: string
  use: string
  rare: string
  safety: string
}

export interface RareMetal {
  element: string
  symbol: string
  kind: string
  foundIn: string
  role: string
}

export interface DangerItem {
  name: string
  formula: string
  hazard: string
  advice: string
}

export const CATEGORIES: string[] = ["调味食品", "清洁日化", "医药保健", "建筑工业", "农业化肥", "燃料气体", "手机", "文具", "钱币", "奶茶外卖", "衣物纺织", "家具日用", "电池照明", "汽车", "化妆品洗漱"]

export const MATERIALS: MaterialRow[] = [
  { category: "调味食品", item: "食盐", part: "整体", common: "食盐", chemName: "氯化钠", formula: "NaCl", use: "调味、防腐、维持体液平衡", rare: "否", safety: "安全" },
  { category: "调味食品", item: "食糖", part: "整体", common: "白糖/砂糖", chemName: "蔗糖", formula: "C₁₂H₂₂O₁₁", use: "调味、提供能量", rare: "否", safety: "安全" },
  { category: "调味食品", item: "食醋", part: "有效成分", common: "醋酸", chemName: "乙酸", formula: "CH₃COOH", use: "调味、杀菌、去水垢", rare: "否", safety: "安全（稀释使用）" },
  { category: "调味食品", item: "小苏打", part: "整体", common: "小苏打", chemName: "碳酸氢钠", formula: "NaHCO₃", use: "发酵粉、清洁去污、中和胃酸", rare: "否", safety: "安全" },
  { category: "调味食品", item: "食用碱", part: "整体", common: "纯碱/苏打", chemName: "碳酸钠", formula: "Na₂CO₃", use: "发面、洗涤剂原料", rare: "否", safety: "安全" },
  { category: "调味食品", item: "味精", part: "整体", common: "味精", chemName: "谷氨酸钠", formula: "C₅H₈NNaO₄", use: "增鲜调味", rare: "否", safety: "安全" },
  { category: "调味食品", item: "明矾", part: "整体", common: "明矾", chemName: "十二水合硫酸铝钾", formula: "KAl(SO₄)₂·12H₂O", use: "净水、传统膨松剂（现多限用）", rare: "否", safety: "食品中限用" },
  { category: "调味食品", item: "点豆腐石膏", part: "整体", common: "石膏", chemName: "二水合硫酸钙", formula: "CaSO₄·2H₂O", use: "豆腐凝固剂、医用固定绷带", rare: "否", safety: "安全" },
  { category: "清洁日化", item: "管道疏通剂", part: "有效成分", common: "烧碱/火碱/苛性钠", chemName: "氢氧化钠", formula: "NaOH", use: "疏通下水道、制肥皂", rare: "否", safety: "是：强腐蚀，戴手套" },
  { category: "清洁日化", item: "刷墙石灰", part: "整体", common: "熟石灰/消石灰", chemName: "氢氧化钙", formula: "Ca(OH)₂", use: "刷墙、改良酸性土壤", rare: "否", safety: "是：腐蚀性粉尘" },
  { category: "清洁日化", item: "食品干燥剂", part: "整体", common: "生石灰", chemName: "氧化钙", formula: "CaO", use: "干燥剂、建筑材料", rare: "否", safety: "是：遇水剧烈放热" },
  { category: "清洁日化", item: "漂白粉", part: "有效成分", common: "漂白粉", chemName: "次氯酸钙", formula: "Ca(ClO)₂", use: "消毒、漂白", rare: "否", safety: "是：强氧化性" },
  { category: "清洁日化", item: "84消毒液", part: "有效成分", common: "84消毒液", chemName: "次氯酸钠", formula: "NaClO", use: "杀菌消毒、漂白衣物", rare: "否", safety: "是：禁与洁厕灵混用（产生氯气Cl₂）" },
  { category: "清洁日化", item: "洁厕灵", part: "有效成分", common: "洁厕灵", chemName: "盐酸", formula: "HCl", use: "去尿垢、水垢", rare: "否", safety: "是：强酸腐蚀，禁与84混用" },
  { category: "清洁日化", item: "双氧水", part: "有效成分", common: "双氧水", chemName: "过氧化氢", formula: "H₂O₂", use: "伤口消毒、漂白", rare: "否", safety: "是：高浓度灼伤皮肤" },
  { category: "清洁日化", item: "樟脑丸", part: "整体", common: "樟脑丸", chemName: "萘/对二氯苯", formula: "C₁₀H₈ / C₆H₄Cl₂", use: "防虫防蛀", rare: "否", safety: "是：有毒，远离儿童" },
  { category: "清洁日化", item: "洗衣粉", part: "有效成分", common: "表面活性剂", chemName: "十二烷基苯磺酸钠", formula: "C₁₈H₂₉NaO₃S", use: "去油污", rare: "否", safety: "安全" },
  { category: "医药保健", item: "胃药", part: "有效成分", common: "小苏打片", chemName: "碳酸氢钠", formula: "NaHCO₃", use: "中和胃酸", rare: "否", safety: "安全" },
  { category: "医药保健", item: "泻盐", part: "整体", common: "泻盐/苦盐", chemName: "七水合硫酸镁", formula: "MgSO₄·7H₂O", use: "导泻、消肿外敷", rare: "否", safety: "安全" },
  { category: "医药保健", item: "消毒粉", part: "整体", common: "PP粉", chemName: "高锰酸钾", formula: "KMnO₄", use: "皮肤/果蔬消毒", rare: "否", safety: "是：强氧化剂" },
  { category: "医药保健", item: "硼砂", part: "整体", common: "硼砂", chemName: "十水合四硼酸钠", formula: "Na₂B₄O₇·10H₂O", use: "外用防腐", rare: "否", safety: "是：有毒，禁作食品添加剂" },
  { category: "建筑工业", item: "石灰石/大理石", part: "整体", common: "石灰石", chemName: "碳酸钙", formula: "CaCO₃", use: "建材、补钙剂、水泥原料", rare: "否", safety: "安全" },
  { category: "建筑工业", item: "石英/水晶", part: "整体", common: "石英", chemName: "二氧化硅", formula: "SiO₂", use: "玻璃、陶瓷、建材", rare: "否", safety: "粉尘致矽肺" },
  { category: "建筑工业", item: "老式体温计", part: "感温液", common: "水银", chemName: "汞", formula: "Hg", use: "测温（逐步淘汰）", rare: "是：汞（重金属）", safety: "是：剧毒，打破需特殊处理" },
  { category: "建筑工业", item: "干冰", part: "整体", common: "干冰", chemName: "固态二氧化碳", formula: "CO₂", use: "制冷保鲜、舞台烟雾", rare: "否", safety: "是：冻伤/密闭空间窒息" },
  { category: "建筑工业", item: "铁锈", part: "整体", common: "铁锈", chemName: "水合氧化铁", formula: "Fe₂O₃·nH₂O", use: "铁制品腐蚀产物", rare: "否", safety: "安全" },
  { category: "建筑工业", item: "电石", part: "整体", common: "电石", chemName: "碳化钙", formula: "CaC₂", use: "焊接切割（遇水生成乙炔）", rare: "否", safety: "是：遇水产生易燃乙炔" },
  { category: "农业化肥", item: "尿素", part: "整体", common: "尿素", chemName: "碳酰胺", formula: "CO(NH₂)₂", use: "氮肥", rare: "否", safety: "安全" },
  { category: "农业化肥", item: "硝铵", part: "整体", common: "硝铵", chemName: "硝酸铵", formula: "NH₄NO₃", use: "氮肥", rare: "否", safety: "是：爆炸风险，受管制" },
  { category: "农业化肥", item: "波尔多液", part: "有效成分", common: "波尔多液", chemName: "氢氧化铜", formula: "Cu(OH)₂", use: "果园杀菌剂", rare: "否", safety: "低毒" },
  { category: "农业化肥", item: "草木灰", part: "主要成分", common: "草木灰", chemName: "碳酸钾", formula: "K₂CO₃", use: "钾肥", rare: "否", safety: "安全" },
  { category: "燃料气体", item: "天然气/沼气", part: "主要成分", common: "沼气", chemName: "甲烷", formula: "CH₄", use: "燃料", rare: "否", safety: "是：易燃易爆" },
  { category: "燃料气体", item: "液化石油气", part: "主要成分", common: "液化气", chemName: "丙烷、丁烷", formula: "C₃H₈、C₄H₁₀", use: "家庭燃气", rare: "否", safety: "是：易燃易爆" },
  { category: "燃料气体", item: "煤气", part: "有效成分", common: "煤气", chemName: "一氧化碳+氢气", formula: "CO、H₂", use: "燃料", rare: "否", safety: "是：CO剧毒，防中毒" },
  { category: "燃料气体", item: "医用酒精", part: "有效成分", common: "酒精", chemName: "乙醇", formula: "C₂H₅OH", use: "消毒、燃料、饮品成分", rare: "否", safety: "是：易燃" },
  { category: "手机", item: "手机屏幕", part: "外玻璃", common: "大猩猩玻璃", chemName: "铝硅酸盐玻璃", formula: "SiO₂·Al₂O₃ 体系", use: "抗刮耐摔", rare: "否", safety: "安全" },
  { category: "手机", item: "手机屏幕", part: "触摸导电层", common: "ITO导电膜", chemName: "氧化铟锡", formula: "In₂O₃:SnO₂", use: "导电且透明，触控关键", rare: "是：铟 In（稀有）", safety: "安全" },
  { category: "手机", item: "手机屏幕", part: "OLED发光层", common: "有机发光材料", chemName: "铱配合物等", formula: "含 Ir 配合物", use: "红绿磷光材料核心", rare: "是：铱 Ir（贵金属）", safety: "安全" },
  { category: "手机", item: "手机芯片", part: "基体", common: "单晶硅", chemName: "硅", formula: "Si（99.9999999%）", use: "CPU主体", rare: "否", safety: "安全" },
  { category: "手机", item: "手机芯片", part: "内部导线", common: "铜互连", chemName: "铜/钴", formula: "Cu / Co", use: "纳米级互连线", rare: "是：钴 Co", safety: "安全" },
  { category: "手机", item: "手机芯片", part: "引脚/焊点", common: "镀金触点", chemName: "金/锡", formula: "Au / Sn", use: "关键触点，耐腐蚀不氧化", rare: "是：金 Au（贵金属）", safety: "安全" },
  { category: "手机", item: "手机主板", part: "焊锡", common: "锡银铜焊料", chemName: "锡银铜合金", formula: "Sn-Ag-Cu", use: "焊接所有元器件", rare: "是：银 Ag（贵金属）", safety: "安全" },
  { category: "手机", item: "手机主板", part: "电容器", common: "钽电容", chemName: "五氧化二钽", formula: "Ta₂O₅", use: "体积小容量大", rare: "是：钽 Ta（稀有）", safety: "安全" },
  { category: "手机", item: "手机电池", part: "正极", common: "钴酸锂/三元", chemName: "钴酸锂", formula: "LiCoO₂ / Li(NiCoMn)O₂", use: "储电核心", rare: "是：锂 Li、钴 Co", safety: "安全" },
  { category: "手机", item: "手机电池", part: "负极", common: "石墨", chemName: "石墨", formula: "C", use: "锂离子嵌入储存", rare: "否", safety: "安全" },
  { category: "手机", item: "手机电池", part: "隔膜", common: "PP隔膜", chemName: "聚丙烯", formula: "(C₃H₆)ₙ", use: "防正负极短路", rare: "否", safety: "安全" },
  { category: "手机", item: "手机电池", part: "电解液", common: "电解液", chemName: "六氟磷酸锂", formula: "LiPF₆", use: "锂离子迁移通道", rare: "是：锂 Li", safety: "是：腐蚀性" },
  { category: "手机", item: "手机扬声器", part: "磁体", common: "钕铁硼磁铁", chemName: "钕铁硼", formula: "Nd₂Fe₁₄B", use: "磁力最强的永磁体", rare: "是：钕Nd、镝Dy（稀土）", safety: "安全" },
  { category: "手机", item: "闪光灯/背光", part: "LED芯片", common: "LED", chemName: "氮化镓", formula: "GaN", use: "发光", rare: "是：镓 Ga（稀散）", safety: "安全" },
  { category: "手机", item: "手机机身", part: "中框", common: "铝/钛合金", chemName: "铝合金/钛合金", formula: "Al / Ti", use: "轻量化、散热", rare: "否", safety: "安全" },
  { category: "手机", item: "手机散热", part: "散热片", common: "石墨烯/铜", chemName: "石墨烯/铜", formula: "C / Cu", use: "导热", rare: "否", safety: "安全" },
  { category: "手机", item: "手机摄像头", part: "镜片镀膜", common: "增透膜", chemName: "氟化镁等", formula: "MgF₂", use: "增透成像", rare: "否", safety: "安全" },
  { category: "文具", item: "铅笔", part: "笔芯", common: "铅芯（实为石墨）", chemName: "石墨+黏土", formula: "C + 铝硅酸盐", use: "石墨层间滑动留痕；黏土比例定软硬", rare: "否", safety: "安全（不含铅）" },
  { category: "文具", item: "铅笔", part: "笔杆", common: "木杆", chemName: "纤维素+木质素", formula: "(C₆H₁₀O₅)ₙ", use: "保护笔芯、易削", rare: "否", safety: "安全" },
  { category: "文具", item: "白橡皮", part: "整体", common: "橡皮", chemName: "聚氯乙烯+增塑剂", formula: "(C₂H₃Cl)ₙ", use: "摩擦吸附石墨颗粒", rare: "否", safety: "安全" },
  { category: "文具", item: "绘图橡皮", part: "整体", common: "橡皮", chemName: "天然橡胶", formula: "聚异戊二烯 (C₅H₈)ₙ", use: "弹性擦除", rare: "否", safety: "安全" },
  { category: "文具", item: "纸张", part: "整体", common: "纸", chemName: "纤维素", formula: "(C₆H₁₀O₅)ₙ", use: "书写载体；加CaCO₃填料增白", rare: "否", safety: "安全" },
  { category: "文具", item: "修正液", part: "有效成分", common: "涂改液", chemName: "二氧化钛+溶剂", formula: "TiO₂", use: "白色遮盖力极强", rare: "否", safety: "是：溶剂挥发有刺激" },
  { category: "文具", item: "圆珠笔", part: "球珠", common: "笔尖钢珠", chemName: "碳化钨", formula: "WC", use: "超耐磨", rare: "否", safety: "安全" },
  { category: "文具", item: "荧光笔", part: "墨水", common: "荧光墨水", chemName: "荧光素钠", formula: "C₂₀H₁₀Na₂O₅", use: "吸收紫外发出可见光", rare: "否", safety: "安全" },
  { category: "文具", item: "502胶水", part: "有效成分", common: "瞬间胶", chemName: "α-氰基丙烯酸乙酯", formula: "C₆H₇NO₂", use: "遇水分瞬间聚合固化", rare: "否", safety: "是：刺激、易粘皮肤" },
  { category: "钱币", item: "1元硬币", part: "整体", common: "钢镚", chemName: "钢芯镀镍", formula: "Fe + Ni 镀层", use: "镍防腐、色泽银白", rare: "是：镍 Ni", safety: "安全" },
  { category: "钱币", item: "5角硬币", part: "整体", common: "钢镚", chemName: "钢芯镀铜锌", formula: "Fe + Cu-Zn 镀层", use: "金黄色外观", rare: "否", safety: "安全" },
  { category: "钱币", item: "纸币", part: "基材", common: "钞票纸", chemName: "棉纤维（纤维素）", formula: "(C₆H₁₀O₅)ₙ", use: "棉浆耐折耐水洗", rare: "否", safety: "安全" },
  { category: "钱币", item: "纸币", part: "防伪油墨", common: "磁性油墨", chemName: "四氧化三铁", formula: "Fe₃O₄", use: "验钞机识别", rare: "否", safety: "安全" },
  { category: "钱币", item: "纸币", part: "荧光防伪", common: "荧光纤维", chemName: "稀土荧光材料", formula: "含铕 Eu 等", use: "紫外灯下发光防伪", rare: "是：铕 Eu（稀土）", safety: "安全" },
  { category: "奶茶外卖", item: "透明奶茶杯", part: "杯身", common: "PET杯", chemName: "聚对苯二甲酸乙二醇酯", formula: "(C₁₀H₈O₄)ₙ", use: "透明轻便，冷饮用（耐热<70℃）", rare: "否", safety: "勿装热饮" },
  { category: "奶茶外卖", item: "杯盖/热饮杯", part: "整体", common: "PP杯", chemName: "聚丙烯", formula: "(C₃H₆)ₙ", use: "耐热120℃，可微波", rare: "否", safety: "安全" },
  { category: "奶茶外卖", item: "纸质热饮杯", part: "内膜", common: "PE淋膜", chemName: "聚乙烯", formula: "(C₂H₄)ₙ", use: "防水渗透", rare: "否", safety: "安全" },
  { category: "奶茶外卖", item: "可降解吸管", part: "整体", common: "PLA吸管", chemName: "聚乳酸", formula: "(C₃H₄O₂)ₙ", use: "玉米淀粉发酵制成，可降解", rare: "否", safety: "安全" },
  { category: "奶茶外卖", item: "珍珠（波霸）", part: "整体", common: "粉圆", chemName: "木薯淀粉", formula: "(C₆H₁₀O₅)ₙ", use: "糊化后Q弹", rare: "否", safety: "安全" },
  { category: "奶茶外卖", item: "奶盖/植脂末", part: "主要成分", common: "植脂末", chemName: "氢化植物油+酪蛋白", formula: "甘油三酯+蛋白质", use: "提供奶香口感", rare: "否", safety: "反式脂肪酸争议" },
  { category: "奶茶外卖", item: "茶", part: "有效成分", common: "茶多酚/咖啡因", chemName: "儿茶素/咖啡因", formula: "C₂₂H₁₈O₁₁ / C₈H₁₀N₄O₂", use: "提神、涩感来源", rare: "否", safety: "安全" },
  { category: "奶茶外卖", item: "外卖盒", part: "盒体", common: "PP盒/铝箔盒", chemName: "聚丙烯/铝", formula: "(C₃H₆)ₙ / Al", use: "PP可微波；铝箔保温不可微波", rare: "否", safety: "铝箔勿进微波炉" },
  { category: "奶茶外卖", item: "食品干燥剂", part: "整体", common: "干燥剂", chemName: "硅胶/生石灰", formula: "SiO₂·nH₂O / CaO", use: "吸湿防潮", rare: "否", safety: "是：生石灰型遇水放热" },
  { category: "衣物纺织", item: "棉T恤", part: "纤维", common: "纯棉", chemName: "纤维素", formula: "(C₆H₁₀O₅)ₙ", use: "吸湿透气", rare: "否", safety: "安全" },
  { category: "衣物纺织", item: "涤纶衣物", part: "纤维", common: "聚酯纤维", chemName: "PET（同矿泉水瓶）", formula: "(C₁₀H₈O₄)ₙ", use: "抗皱快干", rare: "否", safety: "安全" },
  { category: "衣物纺织", item: "尼龙丝袜", part: "纤维", common: "锦纶", chemName: "聚酰胺", formula: "[-NH(CH₂)₅CO-]ₙ", use: "耐磨", rare: "否", safety: "安全" },
  { category: "衣物纺织", item: "腈纶毛衣", part: "纤维", common: "人造羊毛", chemName: "聚丙烯腈", formula: "(C₃H₃N)ₙ", use: "仿羊毛保暖", rare: "否", safety: "安全" },
  { category: "衣物纺织", item: "瑜伽裤", part: "弹性纤维", common: "氨纶", chemName: "聚氨酯", formula: "聚氨基甲酸酯", use: "高弹性", rare: "否", safety: "安全" },
  { category: "衣物纺织", item: "羊毛/蚕丝", part: "纤维", common: "羊毛/真丝", chemName: "蛋白质（角蛋白/丝蛋白）", formula: "—", use: "保暖；燃烧有烧头发味可鉴别", rare: "否", safety: "安全" },
  { category: "家具日用", item: "实木桌子", part: "主体", common: "木材", chemName: "纤维素+木质素+半纤维素", formula: "(C₆H₁₀O₅)ₙ 等", use: "结构主体", rare: "否", safety: "安全" },
  { category: "家具日用", item: "密度板", part: "胶粘剂", common: "脲醛树脂", chemName: "脲醛树脂", formula: "CO(NH₂)₂·CH₂O", use: "粘合木纤维", rare: "否", safety: "是：缓释甲醛HCHO" },
  { category: "家具日用", item: "木器清漆", part: "涂层", common: "油漆", chemName: "聚氨酯/醇酸树脂", formula: "聚合物", use: "表面保护光泽", rare: "否", safety: "是：施工时溶剂挥发" },
  { category: "家具日用", item: "不锈钢餐具", part: "整体", common: "304不锈钢", chemName: "铁铬镍合金", formula: "Fe-Cr-Ni（18%Cr,8%Ni）", use: "铬形成Cr₂O₃钝化膜防锈", rare: "是：镍 Ni", safety: "安全" },
  { category: "家具日用", item: "不粘锅", part: "涂层", common: "特氟龙", chemName: "聚四氟乙烯", formula: "(C₂F₄)ₙ", use: "摩擦系数最低，不粘", rare: "否", safety: "是：>260℃分解有害" },
  { category: "家具日用", item: "玻璃水杯", part: "整体", common: "钠钙玻璃", chemName: "钠钙硅酸盐", formula: "Na₂O·CaO·6SiO₂", use: "透明化学稳定", rare: "否", safety: "安全" },
  { category: "家具日用", item: "陶瓷碗", part: "坯体", common: "陶瓷", chemName: "高岭土烧制", formula: "Al₂O₃·2SiO₂·2H₂O", use: "高温烧制餐具", rare: "否", safety: "安全" },
  { category: "家具日用", item: "镜子", part: "反射层", common: "银镜", chemName: "银镀层", formula: "Ag", use: "银镜反应镀银反射", rare: "是：银 Ag（贵金属）", safety: "安全" },
  { category: "家具日用", item: "塑料脸盆", part: "整体", common: "PP/PE盆", chemName: "聚丙烯/聚乙烯", formula: "(C₃H₆)ₙ/(C₂H₄)ₙ", use: "轻便耐摔", rare: "否", safety: "安全" },
  { category: "家具日用", item: "拖鞋/瑜伽垫", part: "整体", common: "EVA发泡", chemName: "乙烯-醋酸乙烯共聚物", formula: "EVA", use: "发泡柔软", rare: "否", safety: "安全" },
  { category: "电池照明", item: "碱性电池", part: "正极", common: "锰干电池", chemName: "二氧化锰", formula: "MnO₂", use: "得电子", rare: "否", safety: "安全" },
  { category: "电池照明", item: "碱性电池", part: "负极", common: "锌筒", chemName: "锌", formula: "Zn", use: "失电子被氧化", rare: "否", safety: "安全" },
  { category: "电池照明", item: "纽扣电池", part: "正极", common: "银锌电池", chemName: "氧化银", formula: "Ag₂O", use: "小体积高电压", rare: "是：银 Ag（贵金属）", safety: "安全" },
  { category: "电池照明", item: "LED灯泡", part: "芯片+荧光粉", common: "LED", chemName: "氮化镓+铈荧光粉", formula: "GaN + YAG:Ce", use: "稀土荧光粉把蓝光转白光", rare: "是：镓Ga、铈Ce（稀土）", safety: "安全" },
  { category: "电池照明", item: "荧光灯管", part: "填充物", common: "日光灯", chemName: "汞蒸气+荧光粉", formula: "Hg", use: "紫外激发荧光粉发光", rare: "是：汞（重金属）", safety: "是：汞有毒，废旧需回收" },
  { category: "汽车", item: "轮胎", part: "胎面", common: "橡胶轮胎", chemName: "天然/丁苯橡胶+炭黑", formula: "(C₅H₈)ₙ + C", use: "炭黑补强耐磨", rare: "否", safety: "安全" },
  { category: "汽车", item: "尾气催化器", part: "催化剂", common: "三元催化", chemName: "铂、钯、铑", formula: "Pt / Pd / Rh", use: "净化尾气", rare: "是：铂族贵金属", safety: "安全" },
  { category: "汽车", item: "车窗玻璃", part: "整体", common: "夹层玻璃", chemName: "钢化玻璃+PVB膜", formula: "SiO₂ 体系", use: "夹层防爆", rare: "否", safety: "安全" },
  { category: "汽车", item: "火花塞", part: "电极", common: "铱金火花塞", chemName: "铱/铂", formula: "Ir / Pt", use: "耐高温电弧", rare: "是：铱Ir、铂Pt（贵金属）", safety: "安全" },
  { category: "汽车", item: "动力电池", part: "正极", common: "磷酸铁锂电池", chemName: "磷酸铁锂", formula: "LiFePO₄", use: "电动车动力（无钴更便宜）", rare: "是：锂 Li", safety: "安全" },
  { category: "化妆品洗漱", item: "牙膏", part: "摩擦剂", common: "摩擦剂", chemName: "碳酸钙/二氧化硅", formula: "CaCO₃ / SiO₂", use: "物理打磨清洁", rare: "否", safety: "安全" },
  { category: "化妆品洗漱", item: "牙膏", part: "防蛀成分", common: "含氟牙膏", chemName: "氟化钠/单氟磷酸钠", formula: "NaF / Na₂PO₃F", use: "促进牙釉质再矿化", rare: "否", safety: "安全" },
  { category: "化妆品洗漱", item: "防晒霜", part: "物理防晒剂", common: "物理防晒", chemName: "二氧化钛/氧化锌", formula: "TiO₂ / ZnO", use: "反射紫外线", rare: "否", safety: "安全" },
  { category: "化妆品洗漱", item: "口红", part: "基质", common: "唇膏", chemName: "蓖麻油+蜡+色素", formula: "甘油三酯+巴西棕榈蜡", use: "成型上色", rare: "否", safety: "安全" },
  { category: "化妆品洗漱", item: "爽身粉", part: "整体", common: "滑石粉", chemName: "滑石粉/玉米淀粉", formula: "Mg₃Si₄O₁₀(OH)₂", use: "吸湿滑爽", rare: "否", safety: "安全" },
  { category: "化妆品洗漱", item: "肥皂", part: "有效成分", common: "肥皂", chemName: "脂肪酸钠", formula: "C₁₇H₃₅COONa", use: "油脂皂化产物，去污", rare: "否", safety: "安全" },
  { category: "化妆品洗漱", item: "洗发水", part: "有效成分", common: "表面活性剂", chemName: "月桂醇聚醚硫酸酯钠", formula: "SLES", use: "起泡去污", rare: "否", safety: "安全" }
]

export const RARE_METALS: RareMetal[] = [
  { element: "金", symbol: "Au", kind: "贵金属", foundIn: "手机芯片引脚、焊点、金饰", role: "抗氧化、导电，关键触点" },
  { element: "银", symbol: "Ag", kind: "贵金属", foundIn: "主板焊锡、纽扣电池、镜子镀层", role: "导电性最好的金属、反光" },
  { element: "铂", symbol: "Pt", kind: "贵金属", foundIn: "汽车三元催化器、火花塞、首饰", role: "催化净化尾气、耐高温" },
  { element: "钯", symbol: "Pd", kind: "贵金属", foundIn: "汽车三元催化器", role: "催化净化尾气" },
  { element: "铑", symbol: "Rh", kind: "贵金属", foundIn: "汽车三元催化器", role: "催化净化尾气，极稀有昂贵" },
  { element: "铱", symbol: "Ir", kind: "贵金属", foundIn: "OLED发光材料、火花塞电极", role: "磷光材料核心、耐高温电弧" },
  { element: "铟", symbol: "In", kind: "稀有金属", foundIn: "手机屏幕ITO导电膜", role: "导电且透明，触控关键" },
  { element: "钽", symbol: "Ta", kind: "稀有金属", foundIn: "手机钽电容", role: "体积小容量大" },
  { element: "镓", symbol: "Ga", kind: "稀散金属", foundIn: "LED芯片（GaN）", role: "半导体发光" },
  { element: "锂", symbol: "Li", kind: "战略金属", foundIn: "手机/电动车电池", role: "储电核心" },
  { element: "钴", symbol: "Co", kind: "战略金属", foundIn: "锂电池正极、芯片导线", role: "稳定电池结构" },
  { element: "钕", symbol: "Nd", kind: "稀土", foundIn: "扬声器/振动马达磁铁", role: "最强永磁体" },
  { element: "镝", symbol: "Dy", kind: "稀土", foundIn: "钕铁硼磁铁添加剂", role: "提高磁铁耐温性" },
  { element: "铕", symbol: "Eu", kind: "稀土", foundIn: "纸币荧光防伪", role: "紫外灯下发光" },
  { element: "铈", symbol: "Ce", kind: "稀土", foundIn: "LED荧光粉（YAG:Ce）", role: "蓝光转白光" },
  { element: "镍", symbol: "Ni", kind: "常见有色金属", foundIn: "硬币镀层、不锈钢", role: "防腐蚀" },
  { element: "汞", symbol: "Hg", kind: "有毒重金属", foundIn: "老式体温计、荧光灯管", role: "测温/发光，剧毒需回收" }
]

export const DANGERS: DangerItem[] = [
  { name: "84消毒液 + 洁厕灵", formula: "NaClO + HCl", hazard: "混合产生剧毒氯气Cl₂", advice: "绝对禁止混用，已致多起中毒事故" },
  { name: "烧碱（管道疏通剂）", formula: "NaOH", hazard: "强腐蚀", advice: "戴手套操作，避免接触皮肤眼睛" },
  { name: "生石灰干燥剂", formula: "CaO", hazard: "遇水剧烈放热", advice: "勿拆包玩耍，勿加水" },
  { name: "水银体温计", formula: "Hg", hazard: "汞蒸气剧毒", advice: "打破后勿用手碰，开窗通风，硫磺粉覆盖" },
  { name: "电石", formula: "CaC₂", hazard: "遇水生成易燃乙炔", advice: "干燥密封存放" },
  { name: "煤气/一氧化碳", formula: "CO", hazard: "无色无味剧毒", advice: "燃气热水器强排通风，装CO报警器" },
  { name: "高锰酸钾", formula: "KMnO₄", hazard: "强氧化剂", advice: "勿与有机物/还原剂混合" },
  { name: "硼砂", formula: "Na₂B₄O₇·10H₂O", hazard: "有毒", advice: "禁作食品添加剂（粽子/凉皮非法添加）" },
  { name: "樟脑丸", formula: "C₁₀H₈/C₆H₄Cl₂", hazard: "有毒", advice: "远离儿童，勿与食物同放" },
  { name: "不粘锅空烧", formula: "(C₂F₄)ₙ", hazard: ">260℃涂层分解有害", advice: "避免空锅干烧" },
  { name: "荧光灯管", formula: "Hg", hazard: "汞污染", advice: "废旧灯管投有害垃圾回收" },
  { name: "锂电池", formula: "LiCoO₂等", hazard: "挤压穿刺可起火", advice: "勿摔勿刺，鼓包即停用" },
  { name: "502胶水", formula: "C₆H₇NO₂", hazard: "瞬间粘合皮肤", advice: "勿对准眼睛，粘手用丙酮/温水浸泡" },
  { name: "密度板家具", formula: "释放HCHO", hazard: "甲醛缓释致癌", advice: "新家具通风，选E0/ENF级板材" },
  { name: "酒精", formula: "C₂H₅OH", hazard: "易燃", advice: "远离明火，勿大面积喷洒后遇火源" }
]
