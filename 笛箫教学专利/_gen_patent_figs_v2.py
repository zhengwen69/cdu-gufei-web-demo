# encoding: utf-8
"""Patent Figures v2: A4 print optimized, B/W compatible, 2400x1800, no AI traces"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = r'C:\Users\H1811\Desktop\CDU 固废备课文件夹2026\演示展示\笛箫教学专利\附图v2'
FONT_DIR = r'C:\Windows\Fonts'
W, H = 2400, 1800

def load_font(name, size):
    try: return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except: return ImageFont.load_default()

F_TITLE  = load_font('simhei.ttf', 50)
F_HEAD   = load_font('simhei.ttf', 32)
F_BODY   = load_font('simhei.ttf', 24)
F_SMALL  = load_font('simhei.ttf', 18)
F_BOX    = load_font('simhei.ttf', 26)
F_CODE   = load_font('simsun.ttc', 26)

WHITE = (255,255,255)
BLACK = (0,0,0)
LGRAY = (210,210,210)
MGRAY = (150,150,150)
DGRAY = (80,80,80)

# Hatch pattern helpers - draw pattern lines inside a rect
def fill_hatch_45(d, x, y, w, h, spacing=14, lw=1, color=BLACK):
    for i in range(-h, w, spacing):
        d.line([(x+i, y), (x+i+h, y+h)], fill=color, width=lw)

def fill_hatch_135(d, x, y, w, h, spacing=14, lw=1, color=BLACK):
    for i in range(-h, w, spacing):
        d.line([(x+i, y+h), (x+i+h, y)], fill=color, width=lw)

def fill_crosshatch(d, x, y, w, h, spacing=14, lw=1, color=BLACK):
    fill_hatch_45(d, x, y, w, h, spacing, lw, color)
    fill_hatch_135(d, x, y, w, h, spacing, lw, color)

def fill_dots(d, x, y, w, h, spacing=8, r=2, color=BLACK):
    for dx in range(0, w, spacing):
        for dy in range(0, h, spacing):
            d.ellipse([x+dx-r, y+dy-r, x+dx+r, y+dy+r], fill=color)

def draw_rect_with_pattern(d, x, y, w, h, border_color, border_width, pattern_type, pattern_color=BLACK):
    """Draw a rectangle with border and hatched fill for B/W printing"""
    # White fill base
    d.rounded_rectangle([x, y, x+w, y+h], radius=10, fill=WHITE, outline=border_color, width=border_width)
    # Clip to rounded rect by drawing pattern inside a slightly smaller area
    margin = 6
    cx, cy, cw, ch = x+margin, y+margin, w-2*margin, h-2*margin
    if pattern_type == '45':
        fill_hatch_45(d, cx, cy, cw, ch, spacing=16, lw=2, color=pattern_color)
    elif pattern_type == '135':
        fill_hatch_135(d, cx, cy, cw, ch, spacing=16, lw=2, color=pattern_color)
    elif pattern_type == 'cross':
        fill_crosshatch(d, cx, cy, cw, ch, spacing=18, lw=1, color=pattern_color)
    elif pattern_type == 'dots':
        fill_dots(d, cx, cy, cw, ch, spacing=10, r=3, color=pattern_color)
    elif pattern_type == 'grid':
        for idx in range(0, cw, 20):
            d.line([(cx+idx, cy), (cx+idx, cy+ch)], fill=pattern_color, width=1)
        for idy in range(0, ch, 20):
            d.line([(cx, cy+idy), (cx+cw, cy+idy)], fill=pattern_color, width=1)

def draw_plain_box(d, x, y, w, h, bw=3, text="", tcolor=BLACK, tfont=F_BOX):
    """Simple box with border no fill"""
    d.rounded_rectangle([x, y, x+w, y+h], radius=8, fill=WHITE, outline=BLACK, width=bw)
    if text:
        b = d.textbbox((0,0), text, font=tfont)
        tw, th = b[2]-b[0], b[3]-b[1]
        d.text((x+(w-tw)//2, y+(h-th)//2), text, font=tfont, fill=tcolor)

def draw_arrow(d, x1, y1, x2, y2, w=4, color=BLACK):
    d.line([x1, y1, x2, y2], fill=color, width=w)
    L = 24
    angle = math.atan2(y2-y1, x2-x1)
    ax1 = x2 - L*math.cos(angle-0.4)
    ay1 = y2 - L*math.sin(angle-0.4)
    ax2 = x2 - L*math.cos(angle+0.4)
    ay2 = y2 - L*math.sin(angle+0.4)
    d.polygon([(x2,y2), (ax1,ay1), (ax2,ay2)], fill=color)

def center_text(d, text, y, font=F_BODY, color=BLACK):
    b = d.textbbox((0,0), text, font=font)
    tw = b[2]-b[0]
    d.text(((W-tw)//2, y), text, font=font, fill=color)

# ================================================================
# FIGURE 1: System Architecture
# ================================================================
def fig1():
    img = Image.new('RGB', (W,H), WHITE)
    d = ImageDraw.Draw(img)
    center_text(d, "图1  系统整体架构", 20, F_TITLE)

    # User terminal
    d.rounded_rectangle([80, 90, 2320, 170], radius=10, fill=WHITE, outline=BLACK, width=3)
    d.text((300, 115), "学习者终端（智能手机、平板电脑或个人计算机，运行现代浏览器）", font=F_HEAD, fill=BLACK)

    # Four modules with patterns
    mod_w, mod_h = 480, 520
    mod_y = 230
    x_pos = [100, 660, 1220, 1780]
    patterns = ['45', '135', 'dots', 'cross']  # distinct B/W patterns
    titles = ["叙事情境模块\n(叙)", "框架诊断模块\n(框)", "场景淬炼模块\n(境)", "创造评估模块\n(创)"]
    descs = [
        "曲目叙事数据包\n背景音频播放\n演奏表情标记",
        "音频采集与分析\nACF音高检测\n五维诊断矩阵",
        "粉红噪声生成\n合奏延迟模拟\nBLE触觉反馈",
        "MFCC特征提取\nPCA降维\n余弦相似度匹配"
    ]

    for i in range(4):
        x = x_pos[i]
        draw_rect_with_pattern(d, x, mod_y, mod_w, mod_h, BLACK, 3, patterns[i], BLACK)
        d.text((x+20, mod_y+15), titles[i], font=F_BOX, fill=BLACK)
        dy = mod_y + 85
        for line in descs[i].split('\n'):
            d.text((x+25, dy), line, font=F_SMALL, fill=DGRAY)
            dy += 34

    # Arrows between modules
    for i in range(3):
        mid_y = mod_y + mod_h//2
        draw_arrow(d, x_pos[i]+mod_w, mid_y, x_pos[i+1], mid_y, 4)

    # Bottom infrastructure
    d.rounded_rectangle([80, 830, 2320, 910], radius=10, fill=WHITE, outline=BLACK, width=3)
    d.text((200, 855), "技术支撑层：音频采集接口  /  信号分析引擎  /  本地持久化存储  /  蓝牙通信接口", font=F_HEAD, fill=BLACK)

    # Learning analysis module
    d.rounded_rectangle([100, 980, 2300, 1060], radius=10, fill=WHITE, outline=BLACK, width=3)
    fill_hatch_45(d, 106, 986, 2188, 68, spacing=14, lw=1, color=DGRAY)
    d.text((200, 1005), "学习数据分析模块：偏差模式匹配  →  练习建议模板库比对  →  个性化练习建议生成  →  闭环学习路径", font=F_HEAD, fill=BLACK)

    # Connection arrows
    draw_arrow(d, 1300, 230+520, 1300, 830, 4)
    draw_arrow(d, 1300, 910, 1300, 980, 4)

    # Step labels
    for i in range(4):
        cx = x_pos[i] + mod_w//2
        d.ellipse([cx-24, 185, cx+24, 233], outline=BLACK, width=3)
        d.text((cx-16, 192), f"S{i+1}", font=F_SMALL, fill=BLACK)

    img.save(os.path.join(OUT, '专利_图1_系统架构.png'), 'PNG')
    print('OK: 图1')

# ================================================================
# FIGURE 2: JSON Schema
# ================================================================
def fig2():
    img = Image.new('RGB', (W,H), WHITE)
    d = ImageDraw.Draw(img)
    center_text(d, "图2  叙事情境数据包数据结构", 20, F_TITLE)

    lines = [
        ('{', BLACK),
        ('  "曲目ID": "DZ001",', BLACK),
        ('  "曲名": "沧海一声笑",', BLACK),
        ('  "难度级别": "入门",', BLACK),
        ('  "叙事类型": "叙",', BLACK),
        ('  "叙事标签": ["江湖","侠客豪情","洒脱"],', BLACK),
        ('  "情境文本": "1990年黄霑为《笑傲江湖》创作...",', DGRAY),
        ('  "背景音频URL": "/audio/waves.mp3",', DGRAY),
        ('  "演奏表情标记": [', BLACK),
        ('    {"指法段落":"65321","标记":"如推窗望远山"},', BLACK),
        ('    {"指法段落":"32165","标记":"如归舟渐远"}', BLACK),
        ('  ],', BLACK),
        ('  "诊断维度关联": ["音准","气息","音色"],', DGRAY),
        ('  "场景推荐": ["独奏回课","合奏排练"]', DGRAY),
        ('}', BLACK)
    ]
    
    y = 90
    for text, color in lines:
        d.text((180, y), text, font=F_CODE, fill=color)
        y += 52

    # Annotation boxes
    ann_font = load_font('simhei.ttf', 22)
    draw_plain_box(d, 1400, 120, 850, 45, 2, "← 情境文本字段（叙维度核心数据）", DGRAY, ann_font)
    draw_plain_box(d, 1400, 300, 850, 45, 2, "← 演奏表情标记字段（叙→框过渡桥接数据）", DGRAY, ann_font)
    draw_plain_box(d, 1400, 690, 850, 45, 2, "← 诊断维度与场景关联字段（跨模块链接数据）", DGRAY, ann_font)
    draw_plain_box(d, 1400, 810, 850, 45, 2, "← 场景推荐字段（与境模块的场景参数配置联动）", DGRAY, ann_font)

    img.save(os.path.join(OUT, '专利_图2_叙事数据包.png'), 'PNG')
    print('OK: 图2')

# ================================================================
# FIGURE 3: Diagnostic Flowchart
# ================================================================
def fig3():
    img = Image.new('RGB', (W,H), WHITE)
    d = ImageDraw.Draw(img)
    center_text(d, "图3  框架诊断模块算法流程图", 20, F_TITLE)

    steps_data = [
        ("S1: 音频采集", "采样率 44100Hz, 单声道, 关闭降噪与AGC", '45'),
        ("S2: 频率幅度谱提取", "FFT点数 2048, 平滑系数 0, 频率分辨率 ~21.5Hz/bin", '135'),
        ("S3: ACF自相关音高检测", "自相关函数 R[k]=Sum(x[n]*x[n+k]), k=8..512\n峰值位置→基频→MIDI音符号", 'dots'),
        ("S4: 五维参数提取", "音准(音分) / 节奏(ms) / 气息(dB标准差) / 指法(ms) / 音色(%)", 'cross'),
        ("S5: 诊断矩阵比对", "实测值 vs 参考标准值 vs 容差阈值 → 五维偏差量化 → 等级判定", 'grid'),
        ("S6: 雷达图可视化输出", "Canvas五轴雷达图 + 按偏差严重程度排序的修复建议文本列表", '45'),
    ]

    for i, (title, desc, pattern) in enumerate(steps_data):
        y = 95 + i * 195
        draw_rect_with_pattern(d, 100, y, 1100, 170, BLACK, 3, pattern)
        d.text((120, y+15), title, font=F_BOX, fill=BLACK)
        dy = y + 70
        for line in desc.split('\n'):
            d.text((130, dy), line, font=F_SMALL, fill=DGRAY)
            dy += 28
        if i < len(steps_data)-1:
            draw_arrow(d, 650, y+170, 650, y+195, 4)

    # Right side: radar chart
    cx, cy = 1800, 900
    r_base = 280
    labels = ["音准","节奏","气息","指法","音色"]
    angles = [2*math.pi*i/5 - math.pi/2 for i in range(5)]
    # Outer pentagon
    pts = [(cx+r_base*math.cos(a), cy+r_base*math.sin(a)) for a in angles]
    for i in range(5):
        d.line([(cx, cy), pts[i]], fill=DGRAY, width=1)
        d.line([pts[i], pts[(i+1)%5]], fill=BLACK, width=2)
    # Inner pentagon (simulated data)
    vals = [0.72, 0.88, 0.55, 0.91, 0.63]
    pts2 = [(cx+r_base*v*math.cos(a), cy+r_base*v*math.sin(a)) for v,a in zip(vals, angles)]
    for i in range(5):
        d.line([pts2[i], pts2[(i+1)%5]], fill=BLACK, width=4)
        d.ellipse([pts2[i][0]-8, pts2[i][1]-8, pts2[i][0]+8, pts2[i][1]+8], fill=BLACK)
    for i in range(5):
        lx = cx+(r_base+70)*math.cos(angles[i])-30
        ly = cy+(r_base+70)*math.sin(angles[i])-16
        d.text((lx, ly), labels[i], font=F_BOX, fill=BLACK)
    d.text((cx-200, cy+r_base+80), "--- 五维诊断雷达图示例", font=F_SMALL, fill=DGRAY)

    img.save(os.path.join(OUT, '专利_图3_框架诊断流程图.png'), 'PNG')
    print('OK: 图3')

# ================================================================
# FIGURE 4: Sequence Diagram (fixed participant names)
# ================================================================
def fig4():
    img = Image.new('RGB', (W,H), WHITE)
    d = ImageDraw.Draw(img)
    center_text(d, "图4  场景淬炼模块交互时序图", 20, F_TITLE)

    # Participants
    actors = ["学习者", "场景淬炼\n模块", "触觉反馈\n手环", "学习数据\n分析模块"]
    ax = [250, 830, 1410, 1990]
    
    for i, (name, x) in enumerate(zip(actors, ax)):
        d.rounded_rectangle([x-90, 90, x+90, 160], radius=8, fill=WHITE, outline=BLACK, width=3)
        for j, line in enumerate(name.split('\n')):
            d.text((x-70, 100+j*30), line, font=F_SMALL, fill=BLACK)
        # Lifeline (dashed)
        for dy in range(160, 1200, 12):
            d.line([(x, dy), (x, dy+6)], fill=DGRAY, width=2)

    # Messages
    msgs = [
        (55, "1. 选择场景模式", ax[0], ax[1]),
        (105, "2. 请求场景参数配置", ax[1], ax[3]),
        (155, "3. 返回场景参数包", ax[3], ax[1]),
        (215, "4. 生成粉红噪声并播放", ax[1], ax[1]),
        (275, "5. 发送触觉指令[0x01,8,5]", ax[1], ax[2]),
        (315, "6. 触觉反馈确认 ACK", ax[2], ax[1]),
        (375, "7. 开始演奏", ax[0], ax[0]),
        (435, "8. 实时诊断数据 → 分析模块", ax[1], ax[3]),
        (495, "9. 返回演出质量评估", ax[3], ax[1]),
        (555, "10. 噪音升至 70dB（高潮段）", ax[1], ax[1]),
        (615, "11. 触觉频率升至 12Hz", ax[1], ax[2]),
        (675, "12. 演奏结束", ax[0], ax[0]),
        (735, "13. 生成完整诊断报告", ax[1], ax[1]),
        (795, "14. 推送报告至学习者终端", ax[1], ax[0]),
    ]

    for (y, label, src, dst) in msgs:
        py = y + 90
        d.text((30, py-8), label, font=F_SMALL, fill=BLACK)
        draw_arrow(d, src, py+4, dst, py+4, 3)

    img.save(os.path.join(OUT, '专利_图4_场景交互时序图.png'), 'PNG')
    print('OK: 图4')

# ================================================================
# FIGURE 5: Creative Assessment Algorithm
# ================================================================
def fig5():
    img = Image.new('RGB', (W,H), WHITE)
    d = ImageDraw.Draw(img)
    center_text(d, "图5  创造评估模块算法流程图", 20, F_TITLE)

    steps = [
        ("输入: 即兴演奏音频 (约3分钟, 44.1kHz采样率)", 'plain'),
        ("S1: 分帧加窗 (帧长150ms, 50%重叠, 汉明窗)", '45'),
        ("S2: MFCC特征提取 (26个Mel三角滤波器, 每帧24维系数)", '135'),
        ("S3: PCA降维 (协方差矩阵→特征值分解→取前8个主成分)", 'dots'),
        ("S4: 余弦相似度匹配 (与50个风格模板逐一计算相似度)", 'cross'),
        ("S5: 三联创造性评分 (0.4x风格契合度+0.3x辨识度+0.3x复杂度)", 'grid'),
        ("输出: 创造性评分(0-100分) + 风格标签建议 + 相似度排名", '45'),
    ]

    for i, (title, pattern) in enumerate(steps):
        y = 90 + i * 135
        w_box = 1000
        if pattern == 'plain':
            d.rounded_rectangle([100, y, 100+w_box, y+110], radius=10, fill=WHITE, outline=BLACK, width=3)
            d.text((120, y+30), title, font=F_BOX, fill=BLACK)
        else:
            draw_rect_with_pattern(d, 100, y, w_box, 110, BLACK, 3, pattern)
            d.text((120, y+30), title, font=F_BOX, fill=BLACK)
        if i < len(steps)-1:
            draw_arrow(d, 600, y+110, 600, y+135, 4)

    # Right side: formulas
    form_font = load_font('simhei.ttf', 26)
    line_h = 38
    fy = 110
    d.text((1150, fy), "评分因子定义:", font=F_HEAD, fill=BLACK); fy += 55

    formulas = [
        ("S_fit  (风格契合度):", "与最近模板的余弦相似度值"),
        ("S_dist (风格辨识度):", "最高相似度与第二高相似度的差值"),
        ("S_comp (即兴复杂度):", "超出模板包络的创新特征维度占比"),
        ("", ""),
        ("综合评分公式:", ""),
        ("Score = 0.4 x S_fit + 0.3 x S_dist + 0.3 x S_comp", ""),
        ("", ""),
        ("风格模板库 (>50模板):", ""),
    ]
    for label, desc in formulas:
        if label and desc:
            d.text((1150, fy), label, font=form_font, fill=BLACK)
            bw = d.textbbox((0,0), label, font=form_font)[2]-d.textbbox((0,0), label, font=form_font)[0]
            d.text((1150+bw+10, fy), desc, font=F_SMALL, fill=DGRAY)
        else:
            d.text((1150, fy), label, font=form_font, fill=BLACK)
        fy += line_h

    fy += 10
    for st in ["江南丝竹 / 昆曲伴奏 / 现代新笛 / 即兴爵士融合 / 北方梆笛 / ..."]:
        d.text((1160, fy), st, font=F_SMALL, fill=DGRAY)
        fy += 28

    img.save(os.path.join(OUT, '专利_图5_创造评估算法.png'), 'PNG')
    print('OK: 图5')

# ================================================================
# FIGURE 6: Four-dimension progression
# ================================================================
def fig6():
    img = Image.new('RGB', (W,H), WHITE)
    d = ImageDraw.Draw(img)
    center_text(d, "图6  四维递进关系及技术效果链", 20, F_TITLE)

    dims = [
        ("一、叙 (Narrative)", "情感触发", "曲目叙事 | 情境数据包 | 背景音频",
         "效果: 动机激活 → 情感记忆编码", '45'),
        ("二、框 (Framework)", "诊断赋能", "ACF音高检测 | 五维矩阵 | 雷达图",
         "效果: 主观听觉 → 量化偏差 → 精准纠偏", '135'),
        ("三、境 (Scenario)", "压力淬炼", "粉红噪声 | 合奏延迟 | BLE触觉",
         "效果: 琴房练习 → 模拟演出环境 → 真实演出适应", 'dots'),
        ("四、创 (Creation)", "创造致用", "MFCC | PCA | 余弦匹配 | 三联评分",
         "效果: 模仿者 → 创作者: 风格辨识与即兴评分", 'cross'),
    ]

    for i, (name, func, techs, effect, pattern) in enumerate(dims):
        y = 100 + i * 340
        # Main box
        draw_rect_with_pattern(d, 80, y, 650, 300, BLACK, 3, pattern)
        d.text((100, y+15), name, font=F_BOX, fill=BLACK)
        d.text((100, y+70), f"功能: {func}", font=F_BODY, fill=BLACK)
        d.text((100, y+115), f"技术: {techs}", font=F_SMALL, fill=DGRAY)
        d.text((100, y+170), f"{effect}", font=F_SMALL, fill=BLACK)

        if i < 3:
            draw_arrow(d, 405, y+300, 405, y+340, 4)

        # Right side info box
        rx = 820
        d.rounded_rectangle([rx, y+30, 2300, y+270], radius=8, fill=WHITE, outline=BLACK, width=2)
        items = techs.split(' | ')
        for j, item in enumerate(items):
            d.text((rx+30, y+55+j*40), f"[{j+1}] {item}", font=F_SMALL, fill=BLACK)

    # Bottom summary
    draw_plain_box(d, 80, 1500, 2240, 60, 3, "", BLACK)
    d.text((150, 1510), "技术效果链: 叙(情感记忆) → 框(量化诊断) → 境(压力适应) → 创(风格创造)", font=F_HEAD, fill=BLACK)

    draw_plain_box(d, 300, 1610, 1800, 65, 3, "", BLACK)
    d.text((350, 1620), "核心创新: 四模块事件总线闭环 -- 吹管乐器ACF适配 -- 参数化演出压力模拟 -- 三联创造性评分", font=F_BOX, fill=BLACK)

    img.save(os.path.join(OUT, '专利_图6_四维递进关系图.png'), 'PNG')
    print('OK: 图6')

# ================================================================
# FIGURE 7: UI Wireframe (pure B/W, no decorative elements)
# ================================================================
def fig7():
    img = Image.new('RGB', (W,H), WHITE)
    d = ImageDraw.Draw(img)
    center_text(d, "图7  用户界面原型示意", 20, F_TITLE)

    # Browser window chrome
    d.rounded_rectangle([120, 70, 2280, 150], radius=8, fill=WHITE, outline=BLACK, width=3)
    d.text((160, 90), "笛箫民乐交互式教学系统", font=F_BOX, fill=BLACK)
    d.line([(2200, 95), (2230, 95)], fill=BLACK, width=3)
    d.line([(2200, 120), (2230, 120)], fill=BLACK, width=3)

    # Content area
    d.rounded_rectangle([120, 150, 2280, 1730], radius=8, fill=WHITE, outline=BLACK, width=2)

    # Left panel - difficulty selector
    d.rounded_rectangle([140, 170, 420, 1710], radius=6, fill=WHITE, outline=DGRAY, width=2)
    d.text((165, 195), "--- 选择难度", font=F_BOX, fill=BLACK)
    for i, lv in enumerate(["入门", "中级", "高级"]):
        d.text((180, 240+i*45), f"[ ] {lv}", font=F_BODY, fill=BLACK)

    d.text((165, 410), "--- 场景模式", font=F_BOX, fill=BLACK)
    for i, md in enumerate(["独奏回课", "合奏排练", "公演模拟", "即兴创作"]):
        d.text((180, 455+i*45), f"[ ] {md}", font=F_BODY, fill=DGRAY)

    # Center panel - track list
    d.text((500, 195), "--- 曲目选择", font=F_BOX, fill=BLACK)
    tracks_list = [
        ("沧海一声笑", "入门", "叙事: 江湖 / 侠客豪情 / 洒脱"),
        ("姑苏行", "中级", "叙事: 江南 / 园林漫步 / 宁静"),
        ("梅花三弄", "中级", "叙事: 寒冬 / 不屈 / 清雅"),
        ("鹧鸪飞", "高级", "叙事: 楚地 / 逐鸟 / 灵动"),
    ]
    for i, (name, level, tags) in enumerate(tracks_list):
        x = 500 + (i%2)*750
        y = 240 + (i//2)*160
        d.rounded_rectangle([x, y, x+700, y+140], radius=6, fill=WHITE, outline=BLACK, width=2)
        d.text((x+20, y+15), name, font=F_HEAD, fill=BLACK)
        d.text((x+20, y+55), f"难度: {level}", font=F_SMALL, fill=DGRAY)
        d.text((x+20, y+85), tags, font=F_SMALL, fill=DGRAY)
        d.text((x+20, y+115), "> 预览叙事情境", font=F_SMALL, fill=BLACK)

    # Right panel - diagnostic
    d.text((1750, 195), "--- 诊断雷达图", font=F_BOX, fill=BLACK)
    d.rounded_rectangle([1750, 240, 2260, 700], radius=6, fill=WHITE, outline=BLACK, width=2)
    # Draw simplified radar in the box
    rc_x, rc_y = 2005, 470
    r_r = 180
    r_labels = ["音准","节奏","气息","指法","音色"]
    r_angles = [2*math.pi*i/5 - math.pi/2 for i in range(5)]
    r_pts = [(rc_x+r_r*math.cos(a), rc_y+r_r*math.sin(a)) for a in r_angles]
    for i in range(5):
        d.line([(rc_x, rc_y), r_pts[i]], fill=DGRAY, width=1)
        d.line([r_pts[i], r_pts[(i+1)%5]], fill=BLACK, width=2)
    for i in range(5):
        lx = rc_x+(r_r+50)*math.cos(r_angles[i])-20
        ly = rc_y+(r_r+50)*math.sin(r_angles[i])-12
        d.text((lx, ly), r_labels[i], font=F_SMALL, fill=BLACK)

    d.text((1750, 730), "--- 修复建议", font=F_BOX, fill=BLACK)
    d.text((1750, 770), "1. 音准偏差 +12音分", font=F_SMALL, fill=BLACK)
    d.text((1750, 800), "   > 建议口风角度微调", font=F_SMALL, fill=DGRAY)
    d.text((1750, 840), "2. 节奏偏差 +45ms", font=F_SMALL, fill=BLACK)
    d.text((1750, 870), "   > 建议节拍器60BPM练习", font=F_SMALL, fill=DGRAY)

    # Bottom: creative mode bar
    d.rounded_rectangle([500, 680, 1700, 770], radius=6, fill=WHITE, outline=BLACK, width=2)
    d.text((530, 710), "即兴创作模式: 命题 [落日] -- 以五声音阶自由创作16小节原创旋律  [开始录音]  [提交评估]", font=F_BOX, fill=BLACK)

    # Bottom status bar
    d.rounded_rectangle([140, 1680, 2260, 1710], radius=4, fill=WHITE, outline=DGRAY, width=1)
    d.text((160, 1688), "NFSC v1.0  |  当前场景: 独奏回课  |  麦克风: 已连接  |  手环: BLE配对中  |  学习进度: 3/10", font=F_SMALL, fill=DGRAY)

    img.save(os.path.join(OUT, '专利_图7_界面原型.png'), 'PNG')
    print('OK: 图7')

# ================================================================
if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    print("Generating 7 patent figures v2 (2400x1800, B/W optimized)...\n")
    fig1()
    fig2()
    fig3()
    fig4()
    fig5()
    fig6()
    fig7()
    total = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT) if f.endswith('.png'))
    print(f"\nDone! 7 figures, total: {total/1024:.0f} KB ({total/1024/1024:.1f} MB)")
