# encoding: utf-8
"""Patent Figures v5: ALL BLACK bold, no gray text, taller boxes, wider spacing"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = r'C:\Users\H1811\Desktop\CDU 固废备课文件夹2026\演示展示\笛箫教学专利\附图v5'
FONT_DIR = r'C:\Windows\Fonts'
W, H = 3500, 2500

def font(name, size):
    try: return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except: return ImageFont.load_default()

# All fonts: simhei (bold) or msyhbd (extra bold)
F_HEAD   = font('msyhbd.ttc', 64)
F_BODY   = font('msyhbd.ttc', 50)
F_SMALL  = font('msyhbd.ttc', 42)
F_BOX    = font('msyhbd.ttc', 60)
F_CODE   = font('msyhbd.ttc', 46)
F_TINY   = font('simhei.ttf', 36)
F_ANN    = font('msyhbd.ttc', 48)

WHITE = (255,255,255)
BLACK = (0,0,0)
DGRAY = (80,80,80)  # only for faint structural lines, NEVER for text

def box(d, x, y, w, h, bw=5, text="", tfont=F_BOX):
    """Plain white box with black border"""
    d.rounded_rectangle([x,y,x+w,y+h], radius=14, fill=WHITE, outline=BLACK, width=bw)
    if text:
        lines = text.split('\n')
        bb = d.textbbox((0,0), "X", font=tfont)
        lh = bb[3]-bb[0] + 8
        total_h = len(lines) * lh
        sy = y + (h - total_h)//2
        for ln in lines:
            bb2 = d.textbbox((0,0), ln, font=tfont)
            lw = bb2[2]-bb2[0]
            d.text((x+(w-lw)//2, sy), ln, font=tfont, fill=BLACK)
            sy += lh

def arrow(d, x1, y1, x2, y2, w=6):
    d.line([x1,y1,x2,y2], fill=BLACK, width=w)
    L=36; a=math.atan2(y2-y1,x2-x1)
    ax1=x2-L*math.cos(a-0.4); ay1=y2-L*math.sin(a-0.4)
    ax2=x2-L*math.cos(a+0.4); ay2=y2-L*math.sin(a+0.4)
    d.polygon([(x2,y2),(ax1,ay1),(ax2,ay2)], fill=BLACK)

# ============================================================
def fig1():
    img=Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(img)

    box(d, 100, 30, 3300, 140, 5, "学习者终端 ( 智能手机 / 平板 / 个人电脑，运行浏览器 )", F_SMALL)

    mw, mh = 720, 1100; my = 240
    xs = [120, 950, 1780, 2610]
    ttl = ["叙事情境模块\n  ( 叙 )", "框架诊断模块\n  ( 框 )", "场景淬炼模块\n  ( 境 )", "创造评估模块\n  ( 创 )"]
    desc = [
        ["曲目叙事数据包","背景音频播放","演奏表情标记叠加"],
        ["音频实时采集","ACF 音高检测","五维诊断矩阵"],
        ["粉红噪声生成","合奏延迟模拟","BLE 触觉反馈"],
        ["MFCC 特征提取","PCA 降维","余弦相似度匹配"],
    ]
    for i in range(4):
        x = xs[i]
        box(d, x, my, mw, mh, 5, ttl[i], F_BOX)
        dy = my + 170
        for ln in desc[i]:
            d.text((x+30, dy), ln, font=F_SMALL, fill=BLACK)
            dy += 65
        if i < 3:
            arrow(d, x+mw, my+mh//2, xs[i+1], my+mh//2, 6)

    box(d, 100, 1480, 3300, 140, 5, "技术支撑层：音频采集接口  |  信号分析引擎  |  本地持久化存储  |  蓝牙通信接口", F_SMALL)
    box(d, 100, 1720, 3300, 140, 5, "学习数据分析模块：偏差模式匹配   练习建议模板库比对   个性化建议生成   闭环学习路径", F_SMALL)

    arrow(d, 1750, 240+1100, 1750, 1480, 6)
    arrow(d, 1750, 1480+140, 1750, 1720, 6)

    for i in range(4):
        cx = xs[i]+mw//2
        d.ellipse([cx-38,185,cx+38,261],outline=BLACK,width=5)
        d.text((cx-22,200),f"S{i+1}",font=F_SMALL,fill=BLACK)

    img.save(os.path.join(OUT,'专利_图1_系统架构.png'),'PNG')
    print('OK: 图1')

def fig2():
    img=Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(img)

    y=50
    items=[('{',1),('  "曲目ID": "DZ001",',1),('  "曲名": "沧海一声笑",',1),
           ('  "难度级别": "入门",',1),('  "叙事类型": "叙",',1),
           ('  "叙事标签": ["江湖", "侠客豪情", "洒脱"],',1),
           ('  "情境文本": "1990年黄霑为《笑傲江湖》创作...",',0),
           ('  "背景音频URL": "/audio/waves.mp3",',0),
           ('  "演奏表情标记": [',1),
           ('    {"指法段落":"65321", "标记":"如推窗望远山"},',1),
           ('    {"指法段落":"32165", "标记":"如归舟渐远"}',1),
           ('  ],',1),
           ('  "诊断维度关联": ["音准", "气息", "音色"],',0),
           ('  "场景推荐": ["独奏回课", "合奏排练"]',0),
           ('}',1)]
    for txt,flag in items:
        d.text((250,y),txt,font=F_CODE,fill=BLACK)
        y += 80

    # Annotation boxes — taller, larger font
    box(d, 1950, 55, 1400, 100, 4, "  情境文本字段 ( 叙维度核心数据 )", F_ANN)
    box(d, 1950, 305, 1400, 100, 4, "  演奏表情标记字段 ( 叙-框桥接数据 )", F_ANN)
    box(d, 1950, 810, 1400, 100, 4, "  维度关联字段 ( 跨模块链接数据 )", F_ANN)
    box(d, 1950, 950, 1400, 100, 4, "  场景推荐字段 ( 与境模块联动 )", F_ANN)

    img.save(os.path.join(OUT,'专利_图2_叙事数据包.png'),'PNG')
    print('OK: 图2')

def fig3():
    img=Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(img)

    # Shorter text per step, taller boxes to prevent overlap
    steps = [
        ("S1: 音频采集", "采样率 44100Hz, 单声道, 关闭降噪与自动增益控制"),
        ("S2: 频率幅度谱提取", "FFT 点数 2048, 平滑系数 0, 分辨率约 21.5 Hz/bin"),
        ("S3: ACF 自相关音高检测", "R[k] = Sum( x[n]  x[n+k] ), k = 8..512"),
        ("S4: 五维参数提取", "音准(音分)  |  节奏(ms)  |  气息(dB)  |  指法(ms)  |  音色(%)"),
        ("S5: 诊断矩阵比对", "实测值 vs 参考标准值 vs 容差阈值   五维偏差量化   等级判定"),
        ("S6: 雷达图可视化输出", "五轴雷达图 + 按偏差严重程度排序的修复建议文本列表"),
    ]
    bw=1600; bh=360
    for i,(title,desc) in enumerate(steps):
        y=60+i*(bh+30)
        box(d,80,y,bw,bh,5,title,F_BOX)
        d.text((110,y+150),desc,font=F_SMALL,fill=BLACK)
        if i<5:
            arrow(d,880,y+bh,880,y+bh+30,6)

    # Radar chart
    cx,cy=2680,1300; r=380
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
        ly=cy+(r+90)*math.sin(angs[i])-28
        d.text((lx,ly),labs[i],font=F_SMALL,fill=BLACK)

    img.save(os.path.join(OUT,'专利_图3_框架诊断流程图.png'),'PNG')
    print('OK: 图3')

def fig4():
    img=Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(img)

    actors=["学习者","场景淬炼\n模块","触觉反馈\n手环","学习数据\n分析模块"]
    ax=[340,1120,1900,2680]

    for i,(name,x) in enumerate(zip(actors,ax)):
        box(d,x-160,40,320,180,5,name,F_SMALL)
        for dy in range(220,1700,24):
            d.line([(x,dy),(x,dy+10)],fill=DGRAY,width=3)

    # Messages with wider vertical spacing (50px gaps)
    msgs=[
        (30, "1. 选择场景模式", ax[0], ax[1]),
        (80, "2. 请求场景参数配置", ax[1], ax[3]),
        (130,"3. 返回场景参数包", ax[3], ax[1]),
        (190,"4. 生成粉红噪声并播放", ax[1], ax[1]),
        (250,"5. 发送触觉指令 [0x01, 8, 5]", ax[1], ax[2]),
        (300,"6. 触觉反馈确认 (ACK)", ax[2], ax[1]),
        (360,"7. 开始演奏", ax[0], ax[0]),
        (420,"8. 实时诊断数据  分析模块", ax[1], ax[3]),
        (480,"9. 返回演出质量评估", ax[3], ax[1]),
        (540,"10. 噪音升至 70dB (高潮段)", ax[1], ax[1]),
        (600,"11. 触觉频率升至 12Hz", ax[1], ax[2]),
        (660,"12. 演奏结束", ax[0], ax[0]),
        (720,"13. 生成完整诊断报告", ax[1], ax[1]),
        (780,"14. 推送报告至学习者终端", ax[1], ax[0]),
    ]
    for (y,label,src,dst) in msgs:
        py=y+220
        d.text((25,py-12),label,font=F_SMALL,fill=BLACK)
        arrow(d,src,py+4,dst,py+4,5)

    img.save(os.path.join(OUT,'专利_图4_场景交互时序图.png'),'PNG')
    print('OK: 图4')

def fig5():
    img=Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(img)

    steps=[
        ("输入: 即兴演奏音频 ( 约 3 分钟, 44.1kHz 采样率 )"),
        ("S1: 分帧加窗 ( 帧长 150ms, 50% 重叠, 汉明窗函数 )"),
        ("S2: MFCC 特征提取 ( 26 个 Mel 三角滤波器, 每帧 24 维系数 )"),
        ("S3: PCA 降维 ( 协方差矩阵   特征值分解   取前 8 个主成分 )"),
        ("S4: 余弦相似度匹配 ( 与 50 个风格模板逐一计算相似度 )"),
        ("S5: 三联创造性评分 ( 0.4  契合度 + 0.3  辨识度 + 0.3  复杂度 )"),
        ("输出: 创造性评分 ( 0-100 分 ) + 风格标签 + 相似度排名"),
    ]
    bw=1700; bh=220
    for i,title in enumerate(steps):
        y=80+i*(bh+30)
        box(d,80,y,bw,bh,4,title,F_BOX)
        if i<6:
            arrow(d,930,y+bh,930,y+bh+30,5)

    # Right side
    ff=font('msyhbd.ttc',46)
    fy=90
    d.text((1900,fy),"评分因子定义:",font=F_HEAD,fill=BLACK); fy+=80
    for lbl,desc in[
        ("S_fit  ( 风格契合度 ):","与最近模板的余弦相似度值"),
        ("S_dist ( 风格辨识度 ):","最高相似度与第二高相似度的差值"),
        ("S_comp ( 即兴复杂度 ):","超出模板包络的创新特征维度占比"),
    ]:
        d.text((1900,fy),lbl,font=ff,fill=BLACK)
        bw_lbl=d.textbbox((0,0),lbl,font=ff)[2]-d.textbbox((0,0),lbl,font=ff)[0]
        d.text((1900+bw_lbl+15,fy),desc,font=F_SMALL,fill=BLACK)
        fy+=56
    fy+=24
    d.text((1900,fy),"综合评分公式:",font=F_HEAD,fill=BLACK); fy+=80
    d.text((1900,fy),"Score = 0.4  S_fit  +  0.3  S_dist  +  0.3  S_comp",font=F_BOX,fill=BLACK)
    fy+=90
    d.text((1900,fy),"风格模板库 ( >50 模板 ):",font=F_HEAD,fill=BLACK); fy+=70
    d.text((1910,fy),"江南丝竹  /  昆曲伴奏  /  现代新笛  /  即兴爵士融合  /  北方梆笛  /  ...",font=F_SMALL,fill=BLACK)

    img.save(os.path.join(OUT,'专利_图5_创造评估算法.png'),'PNG')
    print('OK: 图5')

def fig6():
    img=Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(img)

    dims=[
        ("一、叙 Narrative","情感触发","曲目叙事  |  情境数据包  |  背景音频","动机激活   情感记忆编码"),
        ("二、框 Framework","诊断赋能","ACF 音高检测  |  五维矩阵  |  雷达图","主观听觉   量化偏差   精准纠偏"),
        ("三、境 Scenario","压力淬炼","粉红噪声  |  合奏延迟  |  BLE 触觉","琴房练习   模拟演出环境   真实演出适应"),
        ("四、创 Creation","创造致用","MFCC  |  PCA降维  |  余弦匹配  |  三联评分","模仿者   创作者: 风格辨识与即兴评分"),
    ]
    for i,(name,func,techs,effect) in enumerate(dims):
        y=50+i*560
        box(d,60,y,1200,520,5,name,F_BOX)
        d.text((80,y+130),f"功能: {func}",font=F_BODY,fill=BLACK)
        d.text((80,y+230),f"技术: {techs}",font=F_SMALL,fill=BLACK)
        d.text((80,y+350),effect,font=F_SMALL,fill=BLACK)
        if i<3:
            arrow(d,660,y+520,660,y+560,6)
        rx=1400
        d.rounded_rectangle([rx,y+60,3420,y+480],radius=14,fill=WHITE,outline=BLACK,width=3)
        items=techs.split('  |  ')
        for j,it in enumerate(items):
            d.text((rx+50,y+100+j*60),f"[{j+1}]  {it}",font=F_SMALL,fill=BLACK)

    box(d,60,2350,3380,70,4,"技术效果链: 叙 ( 情感记忆 )    框 ( 量化诊断 )    境 ( 压力适应 )    创 ( 风格创造 )",F_SMALL)

    img.save(os.path.join(OUT,'专利_图6_四维递进关系图.png'),'PNG')
    print('OK: 图6')

def fig7():
    img=Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(img)

    box(d,100,20,3300,120,4,"笛箫民乐交互式教学系统",F_BOX)
    d.rounded_rectangle([100,140,3400,2440],radius=14,fill=WHITE,outline=BLACK,width=3)

    # Left sidebar
    d.rounded_rectangle([120,170,500,2420],radius=10,fill=WHITE,outline=DGRAY,width=3)
    d.text((150,220),"选择难度",font=F_BOX,fill=BLACK)
    for i,lv in enumerate(["入门","中级","高级"]):
        d.text((180,300+i*75),f"[ ] {lv}",font=F_SMALL,fill=BLACK)
    d.text((150,570),"场景模式",font=F_BOX,fill=BLACK)
    for i,md in enumerate(["独奏回课","合奏排练","公演模拟","即兴创作"]):
        d.text((180,650+i*75),f"[ ] {md}",font=F_SMALL,fill=BLACK)

    # Center track cards
    d.text((580,220),"曲目选择",font=F_BOX,fill=BLACK)
    tracks=[("沧海一声笑","入门","叙事: 江湖 / 侠客豪情 / 洒脱"),
            ("姑苏行","中级","叙事: 江南 / 园林漫步 / 宁静"),
            ("梅花三弄","中级","叙事: 寒冬 / 不屈 / 清雅"),
            ("鹧鸪飞","高级","叙事: 楚地 / 逐鸟 / 灵动")]
    for i,(nm,lv,tg) in enumerate(tracks):
        x=580+(i%2)*950; y=300+(i//2)*270
        box(d,x,y,900,250,3,"",None)
        d.text((x+25,y+15),nm,font=F_HEAD,fill=BLACK)
        d.text((x+25,y+95),f"难度: {lv}",font=F_SMALL,fill=BLACK)
        d.text((x+25,y+155),tg,font=F_SMALL,fill=BLACK)
        d.text((x+25,y+215),"> 预览叙事情境",font=F_SMALL,fill=BLACK)

    # Right diagnostic
    d.text((2550,220),"诊断雷达图",font=F_BOX,fill=BLACK)
    dx,dy=2550,290
    d.rounded_rectangle([dx,dy,3380,dy+680],radius=10,fill=WHITE,outline=BLACK,width=3)
    cx,cy=dx+415,dy+360; r=240
    labs=["音准","节奏","气息","指法","音色"]
    angs=[2*math.pi*i/5-math.pi/2 for i in range(5)]
    pts=[(cx+r*math.cos(a),cy+r*math.sin(a)) for a in angs]
    for i in range(5):
        d.line([(cx,cy),pts[i]],fill=DGRAY,width=2)
        d.line([pts[i],pts[(i+1)%5]],fill=BLACK,width=3)
    for i in range(5):
        lx=cx+(r+80)*math.cos(angs[i])-35
        ly=cy+(r+80)*math.sin(angs[i])-25
        d.text((lx,ly),labs[i],font=F_SMALL,fill=BLACK)

    d.text((2550,dy+720),"修复建议",font=F_BOX,fill=BLACK)
    d.text((2550,dy+800),"1. 音准偏差 +12 音分",font=F_SMALL,fill=BLACK)
    d.text((2550,dy+860),"   > 建议口风角度微调",font=F_TINY,fill=BLACK)
    d.text((2550,dy+920),"2. 节奏偏差 +45 ms",font=F_SMALL,fill=BLACK)
    d.text((2550,dy+980),"   > 建议节拍器 60 BPM 练习",font=F_TINY,fill=BLACK)

    # Creative bar
    box(d,580,870,2400,100,3,"即兴创作   命题 [ 落日 ]  以五声音阶创作 16 小节原创旋律   [开始录音]   [提交评估]",F_SMALL)

    # Status bar
    d.rounded_rectangle([120,2390,3380,2420],radius=6,fill=WHITE,outline=DGRAY,width=2)
    d.text((150,2395),"NFSC v1.0  |  当前场景: 独奏回课  |  麦克风: 已连接  |  手环: BLE 配对中  |  学习进度: 3 / 10",font=F_TINY,fill=BLACK)

    img.save(os.path.join(OUT,'专利_图7_界面原型.png'),'PNG')
    print('OK: 图7')

# ============================================================
if __name__=='__main__':
    os.makedirs(OUT,exist_ok=True)
    print("Generating v5 (ALL BLACK bold, msyhbd, taller boxes, wider spacing)...\n")
    fig1();fig2();fig3();fig4();fig5();fig6();fig7()
    total=sum(os.path.getsize(os.path.join(OUT,f)) for f in os.listdir(OUT) if f.endswith('.png'))
    print(f"\nDone! total: {total/1024:.0f} KB ({total/1024/1024:.1f} MB)")
