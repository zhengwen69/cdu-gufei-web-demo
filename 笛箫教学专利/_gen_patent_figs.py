# encoding: utf-8
"""Agent3: Generate 7 patent figures at high resolution (1600x1200 PNG)"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = r'C:\Users\H1811\Desktop\CDU 固废备课文件夹2026\演示展示\笛箫教学专利'
FONT_DIR = r'C:\Windows\Fonts'
W, H = 1600, 1200

def font(name, size):
    try: return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except: return ImageFont.load_default()

F_TITLE = font('msyhbd.ttc', 28)
F_HEAD = font('msyhbd.ttc', 18)
F_BODY = font('msyh.ttc', 13)
F_SMALL = font('msyh.ttc', 10)
F_BOX = font('msyhbd.ttc', 14)

WHITE = (255,255,255)
BLACK = (30,30,30)
GRAY = (100,100,100)
LGRAY = (220,220,220)
BLUE = (41,128,185)
LBLUE = (214,234,248)
GREEN = (39,174,96)
LGREEN = (213,245,227)
ORANGE = (230,126,34)
LORANGE = (252,229,210)
GOLD = (212,163,84)
LGOLD = (252,240,220)
RED = (192,64,64)

def draw_box(d, x, y, w, h, color, lcolor, text="", text_color=BLACK):
    d.rounded_rectangle([x,y,x+w,y+h], radius=8, fill=lcolor, outline=color, width=2)
    if text:
        b = d.textbbox((0,0), text, font=F_BOX)
        tw, th = b[2]-b[0], b[3]-b[1]
        d.text((x+(w-tw)//2, y+(h-th)//2), text, font=F_BOX, fill=text_color)

def arrow_r(d, x1, y1, x2, y2, color=BLUE, w=2):
    d.line([x1,y1,x2,y2], fill=color, width=w)
    # arrowhead
    import math
    angle = math.atan2(y2-y1, x2-x1)
    L = 15
    ax1 = x2 - L*math.cos(angle-0.4)
    ay1 = y2 - L*math.sin(angle-0.4)
    ax2 = x2 - L*math.cos(angle+0.4)
    ay2 = y2 - L*math.sin(angle+0.4)
    d.polygon([(x2,y2),(ax1,ay1),(ax2,ay2)], fill=color)

def center_text(d, text, y, font=F_BODY, color=BLACK):
    b = d.textbbox((0,0), text, font=font)
    tw = b[2]-b[0]
    d.text(((W-tw)//2, y), text, font=font, fill=color)

# ==============================
# FIGURE 1: System Architecture
# ==============================
def fig1():
    img = Image.new('RGB', (W,H), WHITE)
    d = ImageDraw.Draw(img)
    center_text(d, "图1 系统整体架构", 15, F_TITLE, BLACK)

    # Top: User/browser layer
    draw_box(d, 50, 65, 1500, 60, GRAY, LGRAY, "学习者终端（任意现代浏览器：Chrome/Edge/Safari）", BLACK)
    
    # Four modules
    mod_w, mod_h = 330, 350
    mod_y = 160
    x_pos = [80, 450, 820, 1190]
    colors = [(BLUE, LBLUE), (GREEN, LGREEN), (ORANGE, LORANGE), (GOLD, LGOLD)]
    titles = ["叙事情境模块\n(叙)", "框架诊断模块\n(框)", "场景淬炼模块\n(境)", "创造评估模块\n(创)"]
    descs = [
        "曲目叙事数据包\n背景音频播放\n演奏表情标记",
        "Web Audio API\nACF音高检测\n五维诊断矩阵",
        "噪音生成OSC\n合奏延迟Delay\n触觉反馈BLE",
        "MFCC特征提取\nPCA降维\n余弦相似度匹配"
    ]
    
    for i in range(4):
        x = x_pos[i]
        draw_box(d, x, mod_y, mod_w, 50, colors[i][0], colors[i][1], titles[i], BLACK)
        # desc text
        dy = mod_y + 55
        for line in descs[i].split('\n'):
            d.text((x+15, dy), line, font=F_BODY, fill=GRAY)
            dy += 22

    # Arrows between modules
    for i in range(3):
        mid_y = mod_y + 25
        arrow_r(d, x_pos[i]+mod_w, mid_y, x_pos[i+1], mid_y, BLUE, 2)

    # Bottom: Infrastructure layer
    draw_box(d, 50, 550, 1500, 55, GRAY, LGRAY, "基础设施层：Web Audio API / MediaRecorder / IndexedDB / localStorage", BLACK)
    
    # Bottom: AI cloud
    draw_box(d, 80, 640, 1440, 55, GOLD, LGOLD, "云端AI助教层：9-Agent协同体系 / 个性化练习建议 / 进度追踪", BLACK)

    # Connection arrows
    arrow_r(d, 800, 160+350, 800, 550, RED, 2)  # modules → infra
    arrow_r(d, 800, 550+55, 800, 640, GOLD, 2)  # infra → AI
    
    # NFSC cycle at top
    for i in range(4):
        cx = x_pos[i] + mod_w//2
        d.ellipse([cx-20, 65-40, cx+20, 65], outline=colors[i][0], width=2)
        d.text((cx-23, 65-35), f"S{i+1}", font=F_SMALL, fill=colors[i][0])

    img.save(os.path.join(OUT, '专利_图1_系统架构.png'), 'PNG')
    print('OK: 图1')

# ==============================
# FIGURE 2: JSON Schema
# ==============================
def fig2():
    img = Image.new('RGB', (W,H), WHITE)
    d = ImageDraw.Draw(img)
    center_text(d, "图2 叙事情境数据包数据结构", 15, F_TITLE, BLACK)

    schema_lines = [
        ("{", GRAY),
        ('  "曲目ID": "DZ001",', BLACK),
        ('  "曲名": "沧海一声笑",', BLACK),
        ('  "难度级别": "入门",', BLACK),
        ('  "叙事类型": "叙",', BLACK),
        ('  "叙事标签": ["江湖","侠客豪情","洒脱"],', BLACK),
        ('  "情境文本": "1990年黄霑为《笑傲江湖》创作...",', BLUE),
        ('  "背景音频URL": "/audio/waves.mp3",', GREEN),
        ('  "演奏表情标记": [', ORANGE),
        ('    {"指法段落":"65321","标记":"如推窗望远山，由近及远"},', ORANGE),
        ('    {"指法段落":"32165","标记":"如归舟渐远，余韵袅袅"}', ORANGE),
        ('  ],', GRAY),
        ('  "关联诊断维度": ["音准","气息","音色"],', GOLD),
        ('  "推荐场景": ["境-独奏回课","境-合奏排练"]', GOLD),
        ('}', GRAY)
    ]
    
    y = 70
    for text, color in schema_lines:
        d.text((120, y), text, font=font('consola.ttf', 18) if os.path.exists(os.path.join(FONT_DIR,'consola.ttf')) else F_BODY, fill=color)
        y += 42

    # Annotation boxes
    draw_box(d, 1000, 120, 520, 24, BLUE, LBLUE, "← 情境文本（叙维度核心）", BLUE)
    draw_box(d, 1000, 288, 520, 24, ORANGE, LORANGE, "← 演奏表情标记（叙→框过渡）", ORANGE)
    draw_box(d, 1000, 456, 520, 24, GOLD, LGOLD, "← 教学关联数据（跨模块链接）", GOLD)

    img.save(os.path.join(OUT, '专利_图2_叙事数据包.png'), 'PNG')
    print('OK: 图2')

# ==============================
# FIGURE 3: Diagnostic Flowchart
# ==============================
def fig3():
    img = Image.new('RGB', (W,H), WHITE)
    d = ImageDraw.Draw(img)
    center_text(d, "图3 框架诊断模块算法流程图", 15, F_TITLE, BLACK)

    steps = [
        ("S1: 音频采集", "getUserMedia() → MediaStream → AnalyserNode\n采样率44100Hz, fftSize=2048", BLUE, LBLUE),
        ("S2: 频率幅度谱", "getByteFrequencyData() → 频域数据数组", GREEN, LGREEN),
        ("S3: ACF音高检测", "自相关函数 R[k]=Σx[n]·x[n+k]\n取自相关峰值→基频→MIDI音符号", ORANGE, LORANGE),
        ("S4: 五维参数提取", "音准(cent) | 节奏(ms) | 气息(dB,σ)\n指法(ms) | 音色(频谱质心差)", GOLD, LGOLD),
        ("S5: 诊断矩阵比对", "实测值 vs 参考值 vs 阈值\n→ 五维偏差量化", RED, (255,230,230)),
        ("S6: 可视化输出", "Canvas雷达图 + 修复建议文本\n优先级排序：偏差最大→最小", BLUE, LBLUE),
    ]
    
    for i, (title, desc, color, lcolor) in enumerate(steps):
        y = 80 + i * 130
        draw_box(d, 80, y, 550, 105, color, lcolor, title, color)
        dy = y + 35
        for line in desc.split('\n'):
            d.text((95, dy), line, font=F_SMALL, fill=GRAY)
            dy += 18
        
        if i < len(steps)-1:
            arrow_r(d, 355, y+105, 355, y+130, BLUE, 2)

    # Right side annotation: Radar chart illustration
    cx, cy = 1000, 450
    import math
    labels = ["音准","节奏","气息","指法","音色"]
    angles = [2*math.pi*i/5 - math.pi/2 for i in range(5)]
    r_base = 150
    # pentagon
    pts = [(cx+r_base*math.cos(a), cy+r_base*math.sin(a)) for a in angles]
    for i in range(5):
        d.line([(cx, cy), pts[i]], fill=GRAY, width=1)
        d.line([pts[i], pts[(i+1)%5]], fill=GRAY, width=1)
    # inner values (simulated)
    vals = [0.7,0.85,0.55,0.9,0.6]
    pts2 = [(cx+r_base*v*math.cos(a), cy+r_base*v*math.sin(a)) for v,a in zip(vals, angles)]
    for i in range(5):
        d.line([pts2[i], pts2[(i+1)%5]], fill=BLUE, width=3)
        d.ellipse([pts2[i][0]-4, pts2[i][1]-4, pts2[i][0]+4, pts2[i][1]+4], fill=BLUE)
    # labels
    for i in range(5):
        lx = cx + (r_base+40)*math.cos(angles[i]) - 20
        ly = cy + (r_base+40)*math.sin(angles[i]) - 10
        d.text((lx, ly), labels[i], font=F_BOX, fill=BLACK)
    d.text((cx-80, cy+r_base+30), "五维诊断雷达图示例", font=F_SMALL, fill=GRAY)

    img.save(os.path.join(OUT, '专利_图3_框架诊断流程图.png'), 'PNG')
    print('OK: 图3')

# ==============================
# FIGURE 4: Sequence Diagram  
# ==============================
def fig4():
    img = Image.new('RGB', (W,H), WHITE)
    d = ImageDraw.Draw(img)
    center_text(d, "图4 场景淬炼模块交互时序图", 15, F_TITLE, BLACK)

    # Participants
    actors = ["学习者", "浏览器\n(境模块)", "触觉手环\n(BLE)", "云端AI\n助教"]
    ax = [150, 520, 890, 1260]
    for i, (name, x) in enumerate(zip(actors, ax)):
        draw_box(d, x-50, 60, 100, 40, BLUE, LBLUE, name.split('\n')[0], BLUE)
        # lifeline
        d.line([(x, 100), (x, 750)], fill=GRAY, width=1)

    # Sequence messages
    msgs = [
        (60, "1. 选择场景（公演模式）", ax[0], ax[1], BLUE),
        (100, "2. 请求场景参数", ax[1], ax[3], GREEN),
        (140, "3. 返回场景参数包(JSON)", ax[3], ax[1], GREEN),
        (190, "4. 生成噪音 OSC + 灯光 CSS", ax[1], ax[1], ORANGE),
        (240, "5. 发送触觉指令（振动 8Hz）", ax[1], ax[2], RED),
        (280, "6. 触觉反馈确认 (ACK)", ax[2], ax[1], RED),
        (330, "7. 开始演奏", ax[0], ax[0], BLUE),
        (370, "8. 实时诊断数据流 → AI评估", ax[1], ax[3], BLUE),
        (420, "9. 返回演出质量评分", ax[3], ax[1], GOLD),
        (470, "10. 变更噪音至70dB (高潮段)", ax[1], ax[1], ORANGE),
        (520, "11. 触觉频率升至12Hz", ax[1], ax[2], RED),
        (580, "12. 演奏结束", ax[0], ax[0], BLACK),
        (630, "13. 生成完整诊断报告", ax[1], ax[1], GREEN),
        (680, "14. 推送报告至学习者终端", ax[1], ax[0], BLUE),
    ]

    for (y, label, src, dst, color) in msgs:
        d.text((20, y+70), label, font=F_SMALL, fill=color)
        arrow_r(d, src, y+75, dst, y+75, color, 1)

    img.save(os.path.join(OUT, '专利_图4_场景交互时序图.png'), 'PNG')
    print('OK: 图4')

# ==============================
# FIGURE 5: Creative Assessment Algorithm
# ==============================
def fig5():
    img = Image.new('RGB', (W,H), WHITE)
    d = ImageDraw.Draw(img)
    center_text(d, "图5 创造评估模块算法流程图", 15, F_TITLE, BLACK)

    steps = [
        ("输入：即兴演奏音频 (3min, 44.1kHz)", GRAY, LGRAY),
        ("S1: 分帧 → 150ms帧 / 50%重叠", BLUE, LBLUE),
        ("S2: MFCC提取 → 每帧24维系数", GREEN, LGREEN),
        ("S3: PCA降维 → 24维→8维核心特征向量", ORANGE, LORANGE),
        ("S4: 余弦匹配 → 与50个风格模板逐一计算相似度", GOLD, LGOLD),
        ("S5: 三联评分 = 0.4×风格契合度 + 0.3×风格辨识度 + 0.3×即兴复杂度", RED, (255,230,230)),
        ("输出：创造性评分(0-100) + 风格标签建议", BLUE, LBLUE),
    ]
    
    for i, (title, color, lcolor) in enumerate(steps):
        y = 80 + i * 105
        w_size = 700 if i < len(steps)-1 else 750
        draw_box(d, 80, y, w_size, 80, color, lcolor, title, color)
        if i < len(steps)-1:
            arrow_r(d, 80+w_size//2, y+80, 80+w_size//2, y+105, color, 2)

    # Right side: formula illustration
    d.text((950, 100), "风格契合度 S_f:", font=F_HEAD, fill=BLUE)
    d.text((950, 130), "  S_f = cos(θ) = (v₁·v₂)/(||v₁||·||v₂||)", font=F_BODY, fill=BLACK)
    d.text((950, 180), "风格辨识度 S_d:", font=F_HEAD, fill=GREEN)
    d.text((950, 210), "  S_d = max(sim) − second_max(sim)", font=F_BODY, fill=BLACK)
    d.text((950, 260), "即兴复杂度 S_c:", font=F_HEAD, fill=ORANGE)
    d.text((950, 290), "  S_c = N_novel/(N_total), 创新特征数/总特征数", font=F_BODY, fill=BLACK)
    d.text((950, 350), "综合评分:", font=F_HEAD, fill=RED)
    d.text((950, 380), "  Score = 0.4S_f + 0.3S_d + 0.3S_c", font=F_BODY, fill=RED)
    d.text((950, 430), "风格标签库 (>50模板):", font=F_HEAD, fill=BLACK)
    labels = ["T01 江南丝竹","T02 昆曲伴奏","T03 现代新笛","T04 即兴爵士","T05 北方梆笛","..."]
    for i, lbl in enumerate(labels):
        d.text((950, 460+i*24), lbl, font=F_SMALL, fill=GRAY)

    img.save(os.path.join(OUT, '专利_图5_创造评估算法.png'), 'PNG')
    print('OK: 图5')

# ==============================
# FIGURE 6: Four-dimension progression
# ==============================
def fig6():
    img = Image.new('RGB', (W,H), WHITE)
    d = ImageDraw.Draw(img)
    center_text(d, "图6 四维递进关系及技术效果链", 15, F_TITLE, BLACK)

    dims = [
        ("叙 Narrative", "情感触发", "曲目叙事 | 情境数据包 | 背景音频", BLUE, LBLUE,
         "动机激活 → 情感记忆编码"),
        ("框 Framework", "诊断赋能", "ACF音高检测 | 五维矩阵 | 雷达图", GREEN, LGREEN,
         "主观听觉 → 量化偏差 → 精准纠偏"),
        ("境 Scenario", "压力淬炼", "噪音OSC | 合奏延迟 | BLE触觉", ORANGE, LORANGE,
         "琴房安静练习 → 模拟演出环境 → 真实演出适应"),
        ("创 Creation", "创造致用", "MFCC | PCA | 余弦匹配 | 三联评分", GOLD, LGOLD,
         "模仿者 → 创作者：风格辨识+即兴评分"),
    ]

    for i, (name, func, techs, color, lcolor, effect) in enumerate(dims):
        y = 90 + i * 220
        draw_box(d, 60, y, 380, 180, color, lcolor, name, color)
        d.text((75, y+35), f"功能: {func}", font=F_BODY, fill=BLACK)
        d.text((75, y+60), f"技术: {techs}", font=F_SMALL, fill=GRAY)
        d.text((75, y+120), f"效果: {effect}", font=F_SMALL, fill=color)
        
        if i < 3:
            arrow_r(d, 250, y+180, 250, y+220, color, 3)
        
        # Right side: diagram
        rx = 500 + i * 290
        draw_box(d, rx, y+40, 260, 100, color, lcolor, "", color)
        # Internal sub-elements
        items = techs.split(' | ')
        for j, item in enumerate(items):
            d.text((rx+15, y+50+j*22), f"· {item}", font=F_SMALL, fill=BLACK)

    # Bottom: full chain
    draw_box(d, 60, 980, 1480, 55, GRAY, LGRAY, 
             "四维递进技术效果链: 叙(情感记忆) → 框(量化诊断) → 境(压力适应) → 创(风格创造)", BLACK)
    draw_box(d, 200, 1070, 1200, 55, RED, (255,230,230),
             "核心技术创新: 首次将NFSC四维框架系统化+可装置化+跨乐器迁移, 形成全闭环智能教学系统", RED)

    img.save(os.path.join(OUT, '专利_图6_四维递进关系图.png'), 'PNG')
    print('OK: 图6')

# ==============================
# FIGURE 7: UI Mockup
# ==============================
def fig7():
    img = Image.new('RGB', (W,H), (245,245,245))
    d = ImageDraw.Draw(img)
    center_text(d, "图7 用户界面原型示意", 10, F_SMALL, GRAY)

    # Browser window
    draw_box(d, 100, 40, 1400, 50, GRAY, (230,230,230), "笛箫民乐交互式教学系统  ───  ×  □", GRAY)
    
    # Content area
    draw_box(d, 100, 90, 1400, 1070, GRAY, WHITE, "", WHITE)

    # Left sidebar
    draw_box(d, 120, 110, 200, 1030, LGRAY[0], LGRAY, "", LGRAY[0])
    d.text((135, 130), "≡ 选择难度", font=F_HEAD, fill=BLACK)
    levels = ["● 入门", "● 中级", "● 高级"]
    for i, lv in enumerate(levels):
        d.text((145, 165+i*30), lv, font=F_BODY, fill=BLACK)
    
    d.text((135, 280), "⚙ 场景模式", font=F_HEAD, fill=BLACK)
    modes = ["○ 独奏回课", "○ 合奏排练", "○ 公演模拟", "○ 即兴创作"]
    for i, md in enumerate(modes):
        d.text((145, 315+i*30), md, font=F_BODY, fill=GRAY)

    # Center area: music selection
    d.text((380, 130), "📀 曲目选择", font=F_HEAD, fill=BLACK)
    tracks = [
        ("沧海一声笑", "入门", "武侠·江湖", BLUE, LBLUE),
        ("姑苏行", "中级", "江南·园林", GREEN, LGREEN),
        ("梅花三弄", "中级", "寒冬·清雅", GREEN, LGREEN),
        ("鹧鸪飞", "高级", "楚地·灵动", ORANGE, LORANGE),
    ]
    for i, (name, level, tags, color, lcolor) in enumerate(tracks):
        x = 380 + (i%2)*370
        y = 175 + (i//2)*120
        draw_box(d, x, y, 350, 100, color, lcolor, "", color)
        d.text((x+15, y+8), name, font=F_HEAD, fill=color)
        d.text((x+15, y+35), f"难度: {level} | 标签: {tags}", font=F_SMALL, fill=GRAY)
        d.text((x+15, y+55), "▶ 预览叙事情境", font=F_SMALL, fill=BLUE)

    # Right: diagnostic radar placeholder
    d.text((1140, 130), "📊 诊断雷达图", font=F_HEAD, fill=BLACK)
    draw_box(d, 1140, 160, 320, 280, GRAY, WHITE, "← 五维雷达图\nCanvas绘制\n(音准/节奏/气息/\n指法/音色)", GRAY)
    d.text((1140, 460), "修复建议:", font=F_HEAD, fill=GREEN)
    d.text((1140, 490), "1. 音准偏差 +15音分 →", font=F_SMALL, fill=BLACK)
    d.text((1140, 510), "   建议口风角度微调", font=F_SMALL, fill=GRAY)
    d.text((1140, 540), "2. 节奏偏差 +45ms →", font=F_SMALL, fill=BLACK)
    d.text((1140, 560), "   建议节拍器 60BPM", font=F_SMALL, fill=GRAY)

    # Bottom: creative mode
    draw_box(d, 380, 500, 1080, 70, GOLD, LGOLD, 
             "即兴创作模式: 命题 '落日' - 以五声音阶自由创作16小节原创旋律  [开始录音]  [提交评估]", GOLD)
    
    # Bottom status bar
    draw_box(d, 120, 1080, 1380, 30, GRAY, (240,240,240), 
             "NFSC v1.0 | 当前场景: 独奏回课 | 麦克风: 已连接 | 手环: BLE配对中 | 进度: 3/10 曲目", GRAY)

    img.save(os.path.join(OUT, '专利_图7_界面原型.png'), 'PNG')
    print('OK: 图7')

# ==============================
# MAIN
# ==============================
if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    print("Generating 7 patent figures (1600x1200 PNG)...\n")
    fig1()
    fig2()
    fig3()
    fig4()
    fig5()
    fig6()
    fig7()
    
    total = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT) if f.endswith('.png'))
    print(f"\nDone! 7 figures, total size: {total/1024:.0f} KB ({total/1024/1024:.1f} MB)")
