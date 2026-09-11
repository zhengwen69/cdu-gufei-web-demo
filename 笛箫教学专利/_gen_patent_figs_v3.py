# encoding: utf-8
"""Patent Figures v3: A4 300DPI, NO captions in figures, 3x fonts, B/W print optimized"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = r'C:\Users\H1811\Desktop\CDU 固废备课文件夹2026\演示展示\笛箫教学专利\附图v3'
FONT_DIR = r'C:\Windows\Fonts'
# A4 landscape at ~300 DPI
W, H = 3500, 2500

def font(name, size):
    try: return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except: return ImageFont.load_default()

F_HEAD   = font('simhei.ttf', 56)
F_BODY   = font('simhei.ttf', 42)
F_SMALL  = font('simhei.ttf', 32)
F_BOX    = font('simhei.ttf', 50)
F_CODE   = font('simsun.ttc', 40)
F_TINY   = font('simhei.ttf', 26)

WHITE = (255,255,255)
BLACK = (0,0,0)
LGRAY = (210,210,210)
DGRAY = (80,80,80)

# ---- B/W pattern fills ----
def hatch_45(d, x, y, w, h, sp=24, lw=2, c=BLACK):
    for i in range(-h, w, sp):
        d.line([(x+i,y), (x+i+h,y+h)], fill=c, width=lw)

def hatch_135(d, x, y, w, h, sp=24, lw=2, c=BLACK):
    for i in range(-h, w, sp):
        d.line([(x+i,y+h), (x+i+h,y)], fill=c, width=lw)

def hatch_cross(d, x, y, w, h, sp=28, c=BLACK):
    hatch_45(d,x,y,w,h,sp,1,c); hatch_135(d,x,y,w,h,sp,1,c)

def hatch_dots(d, x, y, w, h, sp=16, r=5, c=BLACK):
    for dx in range(0, w, sp):
        for dy in range(0, h, sp):
            d.ellipse([x+dx-r,y+dy-r,x+dx+r,y+dy+r], fill=c)

def hatch_grid(d, x, y, w, h, sp=28, c=BLACK):
    for i in range(0, w, sp): d.line([(x+i,y),(x+i,y+h)], fill=c, width=1)
    for i in range(0, h, sp): d.line([(x,y+i),(x+w,y+i)], fill=c, width=1)

def box(d, x, y, w, h, pat=None, bw=4, text="", tfont=F_BOX, tcol=BLACK):
    """Draw a rectangle with optional pattern fill. No caption/title."""
    d.rounded_rectangle([x,y,x+w,y+h], radius=14, fill=WHITE, outline=BLACK, width=bw)
    if pat:
        mx, my = x+10, y+10; mw, mh = w-20, h-20
        if pat=='45': hatch_45(d,mx,my,mw,mh)
        elif pat=='135': hatch_135(d,mx,my,mw,mh)
        elif pat=='cross': hatch_cross(d,mx,my,mw,mh)
        elif pat=='dots': hatch_dots(d,mx,my,mw,mh)
        elif pat=='grid': hatch_grid(d,mx,my,mw,mh)
    if text:
        bb = d.textbbox((0,0), text, font=tfont)
        tw, th = bb[2]-bb[0], bb[3]-bb[1]
        lines = text.split('\n')
        total_h = len(lines) * (th+8)
        sy = y + (h-total_h)//2
        for ln in lines:
            bb2 = d.textbbox((0,0), ln, font=tfont)
            lw = bb2[2]-bb2[0]
            d.text((x+(w-lw)//2, sy), ln, font=tfont, fill=tcol)
            sy += th+8

def arrow(d, x1, y1, x2, y2, w=5, c=BLACK):
    d.line([x1,y1,x2,y2], fill=c, width=w)
    L=32; a=math.atan2(y2-y1,x2-x1)
    ax1=x2-L*math.cos(a-0.4); ay1=y2-L*math.sin(a-0.4)
    ax2=x2-L*math.cos(a+0.4); ay2=y2-L*math.sin(a+0.4)
    d.polygon([(x2,y2),(ax1,ay1),(ax2,ay2)], fill=c)

# ========================================
def fig1():
    img = Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(img)

    # User terminal
    d.rounded_rectangle([100,40,3400,160],radius=14,fill=WHITE,outline=BLACK,width=5)
    d.text((280,75), "学习者终端", font=F_HEAD, fill=BLACK)
    d.text((700,75), "(智能手机 / 平板 / 个人电脑，运行浏览器)", font=F_SMALL, fill=DGRAY)

    # Four modules
    mw, mh = 720, 780
    my = 250
    xs = [120, 950, 1780, 2610]
    pats = ['45','135','dots','cross']
    ttl = ["叙事情境模块\n (叙)", "框架诊断模块\n (框)", "场景淬炼模块\n (境)", "创造评估模块\n (创)"]
    desc = [
        "曲目叙事数据包\n背景音频播放\n演奏表情标记叠加",
        "音频实时采集\nACF音高检测\n五维诊断矩阵",
        "粉红噪声生成\n合奏延迟模拟\nBLE触觉反馈",
        "MFCC特征提取\nPCA降维\n余弦相似度匹配"
    ]

    for i in range(4):
        x = xs[i]
        box(d, x, my, mw, mh, pats[i], 5, ttl[i], F_BOX)
        dy = my + 140
        for ln in desc[i].split('\n'):
            d.text((x+30, dy), ln, font=F_SMALL, fill=DGRAY)
            dy += 52
        # Arrow to next
        if i<3:
            arrow(d, x+mw, my+mh//2, xs[i+1], my+mh//2, 5)

    # Infrastructure
    d.rounded_rectangle([100,1120,3400,1230],radius=14,fill=WHITE,outline=BLACK,width=5)
    d.text((200,1155), "技术支撑层：音频采集接口  |  信号分析引擎  |  本地持久化存储  |  蓝牙通信接口", font=F_SMALL, fill=BLACK)

    # Learning analysis
    d.rounded_rectangle([100,1320,3400,1430],radius=14,fill=WHITE,outline=BLACK,width=5)
    hatch_45(d, 110,1330,3380,90,sp=20,lw=2,c=DGRAY)
    d.text((200,1355), "学习数据分析模块：偏差模式匹配  →  练习建议模板库比对  →  个性化建议生成  →  闭环学习", font=F_SMALL, fill=BLACK)

    # Connection arrows
    arrow(d, 1750, 250+780, 1750, 1120, 5)
    arrow(d, 1750, 1230, 1750, 1320, 5)

    # Step labels
    for i in range(4):
        cx = xs[i]+mw//2
        d.ellipse([cx-35,200,cx+35,270],outline=BLACK,width=4)
        d.text((cx-20,215), f"S{i+1}", font=F_BOX, fill=BLACK)

    img.save(os.path.join(OUT,'专利_图1_系统架构.png'),'PNG')
    print('OK: 图1')

def fig2():
    img = Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(img)

    y = 60
    lines = [
        ('{',BLACK), ('  "曲目ID":"DZ001",',BLACK), ('  "曲名":"沧海一声笑",',BLACK),
        ('  "难度级别":"入门",',BLACK), ('  "叙事类型":"叙",',BLACK),
        ('  "叙事标签":["江湖","侠客豪情","洒脱"],',BLACK),
        ('  "情境文本":"1990年黄霑为《笑傲江湖》创作...",',DGRAY),
        ('  "背景音频URL":"/audio/waves.mp3",',DGRAY),
        ('  "演奏表情标记":[',BLACK),
        ('    {"指法段落":"65321","标记":"如推窗望远山"},',BLACK),
        ('    {"指法段落":"32165","标记":"如归舟渐远"}',BLACK),
        ('  ],',BLACK),
        ('  "诊断维度关联":["音准","气息","音色"],',DGRAY),
        ('  "场景推荐":["独奏回课","合奏排练"]',DGRAY),
        ('}',BLACK)
    ]
    for txt,col in lines:
        d.text((250,y),txt,font=F_CODE,fill=col)
        y += 62

    # Annotation boxes on right
    ann = font('simhei.ttf',36)
    box(d,2050,80,1300,60, bw=3, text=" 情境文本字段 (叙维度核心数据)", tfont=ann, tcol=DGRAY)
    box(d,2050,310,1300,60, bw=3, text=" 演奏表情标记字段 (叙-框桥接数据)", tfont=ann, tcol=DGRAY)
    box(d,2050,810,1300,60, bw=3, text=" 维度关联字段 (跨模块链接数据)", tfont=ann, tcol=DGRAY)
    box(d,2050,950,1300,60, bw=3, text=" 场景推荐字段 (与境模块联动)", tfont=ann, tcol=DGRAY)

    img.save(os.path.join(OUT,'专利_图2_叙事数据包.png'),'PNG')
    print('OK: 图2')

def fig3():
    img = Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(img)

    steps = [
        ("S1: 音频采集", "采样率44100Hz, 单声道, 关闭降噪与AGC", '45'),
        ("S2: 频率幅度谱提取", "FFT点数2048, 平滑系数0, 分辨率~21.5Hz/bin", '135'),
        ("S3: ACF自相关音高检测", "自相关函数 R[k]=Sum(x[n]x[n+k]), k=8..512\n峰值位置 基频  MIDI音符号", 'dots'),
        ("S4: 五维参数提取", "音准(音分) / 节奏(ms) / 气息(dB) / 指法(ms) / 音色(%)", 'cross'),
        ("S5: 诊断矩阵比对", "实测值 vs 参考标准值 vs 容差阈值  五维偏差量化  等级判定", 'grid'),
        ("S6: 雷达图可视化输出", "Canvas五轴雷达图 + 按偏差严重程度排序的修复建议文本列表", '45'),
    ]
    bw_box = 1400
    for i,(title,desc,pat) in enumerate(steps):
        y = 60 + i*260
        box(d, 100, y, bw_box, 240, pat, 5, title, F_BOX, BLACK)
        dy = y+100
        for ln in desc.split('\n'):
            d.text((130,dy), ln, font=F_SMALL, fill=DGRAY)
            dy += 40
        if i<5:
            arrow(d, 800, y+240, 800, y+260, 6)

    # Radar chart on right
    cx,cy = 2700,1300; r=380
    labs=["音准","节奏","气息","指法","音色"]
    angs=[2*math.pi*i/5-math.pi/2 for i in range(5)]
    pts=[(cx+r*math.cos(a),cy+r*math.sin(a)) for a in angs]
    for i in range(5):
        d.line([(cx,cy),pts[i]],fill=DGRAY,width=2)
        d.line([pts[i],pts[(i+1)%5]],fill=BLACK,width=3)
    vals=[0.72,0.88,0.55,0.91,0.63]
    pts2=[(cx+r*v*math.cos(a),cy+r*v*math.sin(a)) for v,a in zip(vals,angs)]
    for i in range(5):
        d.line([pts2[i],pts2[(i+1)%5]],fill=BLACK,width=6)
        d.ellipse([pts2[i][0]-10,pts2[i][1]-10,pts2[i][0]+10,pts2[i][1]+10],fill=BLACK)
    for i in range(5):
        lx=cx+(r+90)*math.cos(angs[i])-40
        ly=cy+(r+90)*math.sin(angs[i])-25
        d.text((lx,ly),labs[i],font=F_BOX,fill=BLACK)

    img.save(os.path.join(OUT,'专利_图3_框架诊断流程图.png'),'PNG')
    print('OK: 图3')

def fig4():
    img = Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(img)

    actors = ["学习者", "场景淬炼\n模块", "触觉反馈\n手环", "学习数据\n分析模块"]
    ax = [340, 1120, 1900, 2680]

    for i,(name,x) in enumerate(zip(actors,ax)):
        box(d, x-130, 50, 260, 130, bw=4)
        for j,ln in enumerate(name.split('\n')):
            bb = d.textbbox((0,0), ln, font=F_SMALL)
            tw = bb[2]-bb[0]
            d.text((x-tw//2, 65+j*36), ln, font=F_SMALL, fill=BLACK)
        for dy in range(180,2000,18):
            d.line([(x,dy),(x,dy+10)], fill=DGRAY, width=3)

    msgs = [
        (50,"1. 选择场景模式",ax[0],ax[1]),
        (100,"2. 请求场景参数配置",ax[1],ax[3]),
        (150,"3. 返回场景参数包",ax[3],ax[1]),
        (210,"4. 生成粉红噪声并播放",ax[1],ax[1]),
        (270,"5. 发送触觉指令 [0x01, 8, 5]",ax[1],ax[2]),
        (310,"6. 触觉反馈确认 (ACK)",ax[2],ax[1]),
        (370,"7. 开始演奏",ax[0],ax[0]),
        (430,"8. 实时诊断数据  分析模块",ax[1],ax[3]),
        (490,"9. 返回演出质量评估",ax[3],ax[1]),
        (550,"10. 噪音升至 70dB (高潮段)",ax[1],ax[1]),
        (610,"11. 触觉频率升至 12Hz",ax[1],ax[2]),
        (670,"12. 演奏结束",ax[0],ax[0]),
        (730,"13. 生成完整诊断报告",ax[1],ax[1]),
        (790,"14. 推送报告至学习者终端",ax[1],ax[0]),
    ]
    for (y,label,src,dst) in msgs:
        py = y+170
        d.text((30,py-8), label, font=F_SMALL, fill=BLACK)
        arrow(d, src, py+4, dst, py+4, 4)

    img.save(os.path.join(OUT,'专利_图4_场景交互时序图.png'),'PNG')
    print('OK: 图4')

def fig5():
    img = Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(img)

    steps = [
        ("输入: 即兴演奏音频 (约3分钟, 44.1kHz)", None),
        ("S1: 分帧加窗 (帧长150ms, 50%重叠, 汉明窗)", '45'),
        ("S2: MFCC特征提取 (26个Mel滤波器, 每帧24维系数)", '135'),
        ("S3: PCA降维 (协方差矩阵  特征值分解  前8主成分)", 'dots'),
        ("S4: 余弦相似度匹配 (与50个风格模板逐一计算)", 'cross'),
        ("S5: 三联评分 (0.4 契合度 + 0.3 辨识度 + 0.3 复杂度)", 'grid'),
        ("输出: 创造性评分(0-100) + 风格标签 + 相似度排名", '45'),
    ]
    bw_box = 1500
    for i,(title,pat) in enumerate(steps):
        y = 80 + i*170
        if pat:
            box(d, 100, y, bw_box, 155, pat, 4, title, F_BOX)
        else:
            d.rounded_rectangle([100,y,100+bw_box,y+155],radius=12,fill=WHITE,outline=BLACK,width=4)
            bb = d.textbbox((0,0), title, font=F_BOX)
            d.text((120, y+50), title, font=F_BOX, fill=BLACK)
        if i<6:
            arrow(d, 850, y+155, 850, y+170, 5)

    # Right side formulas
    ff = font('simhei.ttf',36)
    fy = 90
    d.text((1750,fy),"评分因子定义:",font=F_HEAD,fill=BLACK); fy+=65
    for lbl,desc in [("S_fit  (风格契合度):","与最近模板的余弦相似度值"),
                     ("S_dist (风格辨识度):","最高相似度与第二高相似度的差值"),
                     ("S_comp (即兴复杂度):","超出模板包络的创新特征维度占比")]:
        d.text((1750,fy),lbl,font=ff,fill=BLACK)
        bw = d.textbbox((0,0),lbl,font=ff)[2]-d.textbbox((0,0),lbl,font=ff)[0]
        d.text((1750+bw+10,fy),desc,font=F_SMALL,fill=DGRAY)
        fy += 48
    fy += 20
    d.text((1750,fy),"综合评分公式:",font=F_HEAD,fill=BLACK); fy+=65
    d.text((1750,fy),"Score = 0.4  S_fit + 0.3  S_dist + 0.3  S_comp",font=F_BOX,fill=BLACK)
    fy += 70
    d.text((1750,fy),"风格模板库 (>50模板):",font=F_HEAD,fill=BLACK); fy+=55
    for s in ["江南丝竹 / 昆曲伴奏 / 现代新笛 / 即兴爵士 / 北方梆笛 / ..."]:
        d.text((1760,fy),s,font=F_SMALL,fill=DGRAY); fy+=38

    img.save(os.path.join(OUT,'专利_图5_创造评估算法.png'),'PNG')
    print('OK: 图5')

def fig6():
    img = Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(img)

    dims = [
        ("一、叙 (Narrative)", "情感触发", "曲目叙事 | 情境数据包 | 背景音频",
         "动机激活  情感记忆编码", '45'),
        ("二、框 (Framework)", "诊断赋能", "ACF音高检测 | 五维矩阵 | 雷达图",
         "主观听觉  量化偏差  精准纠偏", '135'),
        ("三、境 (Scenario)", "压力淬炼", "粉红噪声 | 合奏延迟 | BLE触觉",
         "琴房练习  模拟演出环境  真实演出适应", 'dots'),
        ("四、创 (Creation)", "创造致用", "MFCC | PCA | 余弦匹配 | 三联评分",
         "模仿者  创作者: 风格辨识与即兴评分", 'cross'),
    ]

    for i,(name,func,techs,effect,pat) in enumerate(dims):
        y = 60 + i*540
        box(d, 80, y, 1100, 500, pat, 5, name, F_BOX)
        d.text((100,y+120), f"功能: {func}", font=F_BODY, fill=BLACK)
        d.text((100,y+200), f"技术: {techs}", font=F_SMALL, fill=DGRAY)
        d.text((100,y+290), effect, font=F_SMALL, fill=BLACK)
        if i<3:
            arrow(d, 630, y+500, 630, y+540, 6)
        # Right detail
        rx = 1350
        d.rounded_rectangle([rx,y+50,3400,y+450],radius=12,fill=WHITE,outline=BLACK,width=3)
        items = techs.split(' | ')
        for j,it in enumerate(items):
            d.text((rx+40,y+80+j*55), f"[{j+1}] {it}", font=F_SMALL, fill=BLACK)

    # Bottom
    box(d,80,2270,3340,70, bw=4, text="技术效果链: 叙(情感记忆)   框(量化诊断)   境(压力适应)   创(风格创造)", tfont=F_SMALL)

    img.save(os.path.join(OUT,'专利_图6_四维递进关系图.png'),'PNG')
    print('OK: 图6')

def fig7():
    img = Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(img)

    # Browser chrome
    d.rounded_rectangle([100,30,3400,130],radius=12,fill=WHITE,outline=BLACK,width=4)
    d.text((180,65),"笛箫民乐交互式教学系统",font=F_BOX,fill=BLACK)
    d.line([(3250,55),(3300,55)],fill=BLACK,width=4)
    d.line([(3250,100),(3300,100)],fill=BLACK,width=4)

    # Content area
    d.rounded_rectangle([100,130,3400,2430],radius=12,fill=WHITE,outline=BLACK,width=3)

    # Left sidebar
    d.rounded_rectangle([120,160,500,2410],radius=8,fill=WHITE,outline=DGRAY,width=3)
    d.text((150,200),"--- 选择难度",font=F_BOX,fill=BLACK)
    for i,lv in enumerate(["入门","中级","高级"]):
        d.text((180,270+i*60),f"[ ] {lv}",font=F_SMALL,fill=BLACK)
    d.text((150,500),"--- 场景模式",font=F_BOX,fill=BLACK)
    for i,md in enumerate(["独奏回课","合奏排练","公演模拟","即兴创作"]):
        d.text((180,570+i*60),f"[ ] {md}",font=F_SMALL,fill=DGRAY)

    # Center: track cards
    d.text((600,200),"--- 曲目选择",font=F_BOX,fill=BLACK)
    tracks = [
        ("沧海一声笑","入门","叙事: 江湖 / 侠客豪情 / 洒脱"),
        ("姑苏行","中级","叙事: 江南 / 园林漫步 / 宁静"),
        ("梅花三弄","中级","叙事: 寒冬 / 不屈 / 清雅"),
        ("鹧鸪飞","高级","叙事: 楚地 / 逐鸟 / 灵动"),
    ]
    for i,(nm,lv,tg) in enumerate(tracks):
        x=600+(i%2)*950; y=270+(i//2)*220
        d.rounded_rectangle([x,y,x+900,y+200],radius=10,fill=WHITE,outline=BLACK,width=3)
        d.text((x+25,y+20),nm,font=F_HEAD,fill=BLACK)
        d.text((x+25,y+80),f"难度: {lv}",font=F_SMALL,fill=DGRAY)
        d.text((x+25,y+125),tg,font=F_SMALL,fill=DGRAY)
        d.text((x+25,y+170),"> 预览叙事情境",font=F_SMALL,fill=BLACK)

    # Right: radar + suggestions
    d.text((2550,200),"--- 诊断雷达图",font=F_BOX,fill=BLACK)
    d.rounded_rectangle([2550,260,3400,900],radius=10,fill=WHITE,outline=BLACK,width=3)
    # radar inside
    cx,cy=2975,580; r0=250
    labs=["音准","节奏","气息","指法","音色"]
    angs=[2*math.pi*i/5-math.pi/2 for i in range(5)]
    pts=[(cx+r0*math.cos(a),cy+r0*math.sin(a)) for a in angs]
    for i in range(5):
        d.line([(cx,cy),pts[i]],fill=DGRAY,width=2)
        d.line([pts[i],pts[(i+1)%5]],fill=BLACK,width=3)
    for i in range(5):
        lx=cx+(r0+80)*math.cos(angs[i])-35
        ly=cy+(r0+80)*math.sin(angs[i])-22
        d.text((lx,ly),labs[i],font=F_SMALL,fill=BLACK)

    d.text((2550,950),"--- 修复建议",font=F_BOX,fill=BLACK)
    d.text((2550,1020),"1. 音准偏差 +12音分",font=F_SMALL,fill=BLACK)
    d.text((2550,1070),"   > 建议口风角度微调",font=F_TINY,fill=DGRAY)
    d.text((2550,1130),"2. 节奏偏差 +45ms",font=F_SMALL,fill=BLACK)
    d.text((2550,1180),"   > 建议节拍器60BPM练习",font=F_TINY,fill=DGRAY)

    # Creative bar
    d.rounded_rectangle([600,760,2500,870],radius=10,fill=WHITE,outline=BLACK,width=3)
    d.text((640,800),"即兴创作: 命题 [落日]  以五声音阶创作16小节  [开始录音]  [提交评估]",font=F_BOX,fill=BLACK)

    # Status bar
    d.rounded_rectangle([120,2370,3380,2410],radius=6,fill=WHITE,outline=DGRAY,width=2)
    d.text((150,2380),"NFSC v1.0  |  当前场景: 独奏回课  |  麦克风: 已连接  |  手环: BLE配对中  |  学习进度: 3/10",font=F_TINY,fill=DGRAY)

    img.save(os.path.join(OUT,'专利_图7_界面原型.png'),'PNG')
    print('OK: 图7')

# ========================================
if __name__=='__main__':
    os.makedirs(OUT,exist_ok=True)
    print("Generating 7 patent figures v3 (3500x2500, NO captions, 3x fonts, B/W)...\n")
    fig1();fig2();fig3();fig4();fig5();fig6();fig7()
    total=sum(os.path.getsize(os.path.join(OUT,f)) for f in os.listdir(OUT) if f.endswith('.png'))
    print(f"\nDone! 7 figures, total: {total/1024:.0f} KB ({total/1024/1024:.1f} MB)")
