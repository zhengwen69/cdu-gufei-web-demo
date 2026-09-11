# encoding: utf-8
"""Agent7 + Agent8: Generate 6 listing images for Xianyu"""
import os, re, textwrap, json
from PIL import Image, ImageDraw, ImageFont
from collections import defaultdict

OUT_DIR = r'C:\Users\H1811\Desktop\CDU 固废备课文件夹2026\演示展示\闲鱼上架\素材'
FONT_DIR = r'C:\Windows\Fonts'
SIZE = 800

# --- Font loading ---
def load_font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except:
        return ImageFont.load_default()

FONT_SONG = load_font('simsun.ttc', 24)      # 宋体 body
FONT_HEI = load_font('simhei.ttf', 28)        # 黑体 title
FONT_YAHEI = load_font('msyh.ttc', 20)        # 微软雅黑
FONT_YAHEI_B = load_font('msyhbd.ttc', 22)    # 微软雅黑 bold
FONT_BIG = load_font('simhei.ttf', 42)        # 大标题
FONT_HUGE = load_font('simhei.ttf', 56)       # 超大
FONT_SMALL = load_font('msyh.ttc', 14)        # 小字
FONT_SONG_SM = load_font('simsun.ttc', 16)    # 宋体小

# --- Colors ---
INK_GREEN = (45, 80, 22)
DARK_INK = (26, 26, 26)
GOLD = (212, 163, 84)
PAPER = (245, 240, 232)
WHITE = (255, 255, 255)
DARK_BG = (10, 22, 40)
DARK_CARD = (13, 31, 53)
TEXT_GRAY = (136, 153, 170)
TEXT_LIGHT = (200, 214, 229)
RED_SEAL = (180, 50, 50)
GREEN_ACCENT = (46, 204, 113)
ORANGE_ACCENT = (230, 126, 34)
BLUE_ACCENT = (91, 155, 213)

def draw_centered_text(draw, text, font, y, color, img_w=SIZE):
    """Draw centered text at y position"""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((img_w - tw) // 2, y), text, font=font, fill=color)
    return bbox[3] - bbox[1]  # return text height

def draw_line(draw, y, color=GOLD, width=2, margin=100):
    draw.line([(margin, y), (SIZE - margin, y)], fill=color, width=width)

# ================================================================
# IMAGE 1: COVER (文学意象型)
# ================================================================
def gen_image1():
    img = Image.new('RGB', (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(img)
    
    # --- Top: Pond landscape (stylized) ---
    # Sky gradient
    for i in range(0, 280):
        r = int(245 - i * 0.05)
        g = int(240 - i * 0.05)
        b = int(232 - i * 0.05)
        draw.line([(0, i), (SIZE, i)], fill=(r, g, b), width=1)
    
    # Water surface (horizontal band)
    water_y = 200
    for i in range(water_y, 280):
        shade = int(140 + (i - water_y) * 0.5)
        draw.line([(0, i), (SIZE, i)], fill=(shade, shade + 20, shade + 30), width=1)
    
    # Left village silhouette (Yangliuba)
    village_color = (35, 45, 30)
    for x, h in [(120, 80), (180, 65), (210, 90), (260, 55), (300, 70)]:
        draw.polygon([(x - 20, water_y - h), (x, water_y - h - 25), (x + 20, water_y - h)], fill=village_color)
    
    # Right village silhouette (Liujiawan)
    for x, h in [(500, 75), (560, 60), (600, 85), (650, 50), (690, 70)]:
        draw.polygon([(x - 20, water_y - h), (x, water_y - h - 20), (x + 20, water_y - h)], fill=village_color)
    
    # Trees
    for x in [80, 360, 440, 730]:
        draw.polygon([(x - 15, water_y - 40), (x, water_y - 80), (x + 15, water_y - 40)], fill=(40, 60, 30))
    
    # Reflection on water
    for x, h in [(120, 40), (180, 30), (260, 25), (500, 35), (560, 30), (650, 25)]:
        draw.polygon([(x - 10, water_y + 5), (x, water_y + h + 5), (x + 10, water_y + 5)], fill=(80, 100, 110, 80))
    
    # Road/path from center to bottom
    path_points = [(390, water_y + 20), (380, 320), (370, 380), (360, 440), (350, 500)]
    for i in range(len(path_points) - 1):
        draw.line([path_points[i], path_points[i + 1]], fill=(160, 140, 110), width=3)
    
    # --- Title area ---
    title_y = 310
    
    # Decorative line
    draw_line(draw, title_y - 20, color=INK_GREEN, width=1)
    
    # Main title
    title_lines = [
        ("上岸", FONT_HUGE, INK_GREEN),
        ("基于研究生培养视角导读", FONT_HEI, DARK_INK),
        ("杨柳坝与刘家湾", FONT_BIG, DARK_INK),
        ("中间隔着一张大塘", FONT_HEI, DARK_INK),
    ]
    
    ty = title_y
    for text, font, color in title_lines:
        th = draw_centered_text(draw, text, font, ty, color)
        ty += th + 8
    
    # Decorative line
    draw_line(draw, ty + 10, color=INK_GREEN, width=1)
    ty += 30
    
    # Author
    draw_centered_text(draw, "点暇斋 著", FONT_YAHEI_B, ty, DARK_INK)
    ty += 30
    
    # Stats
    stats_font = load_font('msyh.ttc', 16)
    draw_centered_text(draw, "30万字 · 章回体长篇 · 纪实教育资料", stats_font, ty, (120, 120, 120))
    ty += 35
    
    # Bottom: red seal
    seal_size = 50
    draw.rectangle([(SIZE//2 - seal_size, ty), (SIZE//2 + seal_size, ty + seal_size)], outline=RED_SEAL, width=2)
    seal_font = load_font('simsun.ttc', 14)
    seal_text = "点暇斋"
    sbbox = draw.textbbox((0, 0), seal_text, font=seal_font)
    sw = sbbox[2] - sbbox[0]
    draw.text(((SIZE - sw)//2, ty + seal_size//2 - 8), seal_text, font=seal_font, fill=RED_SEAL)
    
    path = os.path.join(OUT_DIR, '图1_封面.jpg')
    img.save(path, 'JPEG', quality=90)
    print(f'OK: 图1_封面.jpg')
    return img

# ================================================================
# IMAGE 2: TOC (目录)
# ================================================================
def gen_image2():
    # Load chapter data
    base = r'C:\Users\H1811\Desktop\CDU 固废备课文件夹2026\_归档\20260515之1-350回定稿版'
    files = [f for f in os.listdir(base) if f.endswith('.txt') and re.match(r'第\d+回', f)]
    chapters = {}
    for f in files:
        m = re.match(r'第(\d+)回', f)
        if m:
            num = int(m.group(1))
            if num not in chapters or len(f) < len(chapters[num]):
                chapters[num] = f
    sorted_nums = sorted(chapters.keys())
    
    img = Image.new('RGB', (SIZE, SIZE), DARK_BG)
    draw = ImageDraw.Draw(img)
    
    # Title
    y = 30
    draw_centered_text(draw, "《上岸》 完整目录", load_font('simhei.ttf', 32), y, GOLD)
    y += 40
    draw_centered_text(draw, f"共 {len(sorted_nums)} 回目 · 对句章回体", FONT_SMALL, y, TEXT_GRAY)
    y += 25
    draw_line(draw, y, color=GOLD, width=1, margin=60)
    y += 15
    
    # List chapters
    toc_font = load_font('simsun.ttc', 13)
    show_count = min(55, len(sorted_nums))
    cols = 2
    col_w = (SIZE - 120) // cols
    
    for i, num in enumerate(sorted_nums[:show_count]):
        col = i % cols
        row = i // cols
        x = 60 + col * (col_w + 20)
        ry = y + row * 22
        
        fname = chapters[num].replace('.txt', '')
        title = re.sub(r'^第\d+回[\- ]?', '', fname).strip()
        # Truncate long titles
        if len(title) > 22:
            title = title[:20] + '…'
        
        num_text = f"第{num:03d}回"
        num_bbox = draw.textbbox((0, 0), num_text, font=toc_font)
        draw.text((x, ry), num_text, font=toc_font, fill=GOLD)
        
        title_x = x + num_bbox[2] - num_bbox[0] + 8
        draw.text((title_x, ry), title, font=toc_font, fill=TEXT_LIGHT)
    
    # Bottom note
    bottom_y = SIZE - 40
    draw_centered_text(draw, f"... 完整 {len(sorted_nums)} 回目录随书附赠 ...", FONT_SMALL, bottom_y, TEXT_GRAY)
    
    path = os.path.join(OUT_DIR, '图2_目录.jpg')
    img.save(path, 'JPEG', quality=90)
    print(f'OK: 图2_目录.jpg')
    return img

# ================================================================
# IMAGE 3: Golden Quote 1 (文艺展示)
# ================================================================
def gen_image3():
    img = Image.new('RGB', (SIZE, SIZE), tuple(int(c*0.85) for c in PAPER))
    draw = ImageDraw.Draw(img)
    
    # Decorative top bar
    draw.rectangle([(0, 0), (SIZE, 8)], fill=INK_GREEN)
    
    y = 40
    draw_centered_text(draw, "章回体纪实 · 文白交融", load_font('simhei.ttf', 26), y, DARK_INK)
    y += 45
    
    # Quote card
    card_margin = 60
    card_top = y
    card_height = 480
    draw.rounded_rectangle(
        [(card_margin, card_top), (SIZE - card_margin, card_top + card_height)],
        radius=12, fill=WHITE, outline=(200, 190, 175), width=1
    )
    
    # Chapter header
    y += 40
    draw_centered_text(draw, "第 172 回", FONT_YAHEI_B, y, GOLD, SIZE - card_margin * 2)
    y += 32
    draw_centered_text(draw, "论证会上专家语 · 八秒沉默震人心", load_font('simhei.ttf', 20), y, DARK_INK, SIZE - card_margin * 2)
    y += 30
    draw_line(draw, y, color=GOLD, width=1, margin=card_margin + 60)
    y += 30
    
    # Quote text
    quote = "镇政府三楼会议室之空调坏了——一台老式落地风扇呼呼地摆着头，气流扫过桌面，吹动摊开之文件边缘，簌簌作响，如无数只极小之飞蛾在扑棱翅膀。"
    
    quote_font = load_font('simsun.ttc', 18)
    # Word wrap
    words = list(quote)
    lines = []
    line = ""
    for ch in words:
        test = line + ch
        bbox = draw.textbbox((0, 0), test, font=quote_font)
        if bbox[2] - bbox[0] > SIZE - card_margin * 2 - 80:
            lines.append(line)
            line = ch
        else:
            line = test
    if line:
        lines.append(line)
    
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=quote_font)
        tw = bbox[2] - bbox[0]
        draw.text(((SIZE - tw) // 2, y), line, font=quote_font, fill=DARK_INK)
        y += 36
    
    # Bottom tag
    y = card_top + card_height - 80
    tag_font = load_font('msyh.ttc', 14)
    draw_centered_text(draw, "—— 从技术思维到系统思维的叙事转化", tag_font, y, INK_GREEN, SIZE - card_margin * 2)
    
    path = os.path.join(OUT_DIR, '图3_金句①.jpg')
    img.save(path, 'JPEG', quality=90)
    print(f'OK: 图3_金句①.jpg')
    return img

# ================================================================
# IMAGE 4: Golden Quote 2 (另一故事线)
# ================================================================
def gen_image4():
    img = Image.new('RGB', (SIZE, SIZE), DARK_BG)
    draw = ImageDraw.Draw(img)
    
    y = 40
    draw_centered_text(draw, "多视角叙事 · 五条故事线并行", load_font('simhei.ttf', 26), y, GOLD)
    y += 45
    
    card_margin = 40
    card_top = y
    card_height = 430
    draw.rounded_rectangle(
        [(card_margin, card_top), (SIZE - card_margin, card_top + card_height)],
        radius=12, fill=tuple(int(c*1.2) for c in DARK_CARD), outline=GOLD, width=1
    )
    
    y += 30
    draw_centered_text(draw, "第 287 回", FONT_YAHEI_B, y, GOLD)
    y += 30
    draw_centered_text(draw, "杨柳坝调研分类难 · 四色桶前问素质", load_font('simhei.ttf', 19), y, TEXT_LIGHT)
    y += 30
    draw_line(draw, y, color=GOLD, width=1, margin=card_margin + 80)
    y += 25
    
    quote = "杨柳坝的垃圾分类调研进行了三天。四色桶整齐地摆在村口，桶身崭新，标签清晰——可回收、有害、厨余、其他。张婶端着一簸箕混合垃圾走过来，停在桶前，端详了足足半分钟，然后将簸箕里的东西一股脑倒进了标着'其他垃圾'的那个桶里。"
    
    quote_font = load_font('simsun.ttc', 16)
    words = list(quote)
    lines = []
    line = ""
    for ch in words:
        test = line + ch
        bbox = draw.textbbox((0, 0), test, font=quote_font)
        if bbox[2] - bbox[0] > SIZE - card_margin * 2 - 60:
            lines.append(line)
            line = ch
        else:
            line = test
    if line:
        lines.append(line)
    
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=quote_font)
        tw = bbox[2] - bbox[0]
        draw.text(((SIZE - tw) // 2, y), line, font=quote_font, fill=TEXT_LIGHT)
        y += 32
    
    y = card_top + card_height - 100
    
    # Story thread tags
    tags = [
        ("杨柳坝/刘家湾线", GOLD),
        ("龙栖湾线", GREEN_ACCENT),
        ("三多里巷线", ORANGE_ACCENT),
        ("雍葭·学生线", BLUE_ACCENT),
        ("呼昂·导师线", (192, 130, 74)),
    ]
    
    tag_y = y
    tag_font = load_font('msyh.ttc', 11)
    for tag_text, tag_color in tags:
        tbbox = draw.textbbox((0, 0), tag_text, font=tag_font)
        tw = tbbox[2] - tbbox[0]
        tx = card_margin + 20 + (tag_y - y) // 30 * 180  # rough layout
        # Simple horizontal: just center them all
        pass
    
    # Center all tags
    all_tags_width = 0
    for tag_text, _ in tags:
        tbbox = draw.textbbox((0, 0), tag_text, font=tag_font)
        all_tags_width += tbbox[2] - tbbox[0] + 20
    start_x = (SIZE - all_tags_width) // 2
    tx = start_x
    for tag_text, tag_color in tags:
        draw.text((tx, y), tag_text, font=tag_font, fill=tag_color)
        tbbox = draw.textbbox((0, 0), tag_text, font=tag_font)
        tx += tbbox[2] - tbbox[0] + 20
    
    y += 30
    draw_centered_text(draw, "章回体长卷，五线交织的工科研究生思维重塑之路", FONT_SMALL, y, TEXT_GRAY)
    
    path = os.path.join(OUT_DIR, '图4_金句②.jpg')
    img.save(path, 'JPEG', quality=90)
    print(f'OK: 图4_金句②.jpg')
    return img

# ================================================================
# IMAGE 5: Copyright & Compliance (信任背书)
# ================================================================
def gen_image5():
    img = Image.new('RGB', (SIZE, SIZE), DARK_BG)
    draw = ImageDraw.Draw(img)
    
    y = 50
    draw_centered_text(draw, "版权声明 & 合规说明", load_font('simhei.ttf', 28), y, GOLD)
    y += 10
    draw_line(draw, y + 25, color=GOLD, width=1, margin=80)
    y += 45
    
    # Card
    card_margin = 50
    card_top = y
    card_h = 420
    draw.rounded_rectangle(
        [(card_margin, card_top), (SIZE - card_margin, card_top + card_h)],
        radius=10, fill=DARK_CARD, outline=GOLD, width=1
    )
    
    y += 25
    items = [
        ("📋", "著作权归属", "点暇斋个人创作之纪实文学与教育资料汇编，全部作品已办理版权登记"),
        ("📖", "电子版权说明", "作者自有版权独立发行，著作权归创作者所有"),
        ("✅", "合法转让声明", "本商品为作者自有资料之合法转让，非盗版电子书，非代购虚拟商品"),
        ("🔒", "使用限制", "仅供购买者个人学习研究使用，请勿复制、传播、转售或用于商业用途"),
    ]
    
    icon_font = load_font('seguiemj.ttf', 28) if os.path.exists(os.path.join(FONT_DIR, 'seguiemj.ttf')) else load_font('simhei.ttf', 22)
    title_font = load_font('msyhbd.ttc', 16)
    body_font = load_font('simsun.ttc', 13)
    
    for icon, title, desc in items:
        # Icon
        draw.text((card_margin + 20, y), icon, font=icon_font, fill=GOLD)
        # Title
        draw.text((card_margin + 55, y), title, font=title_font, fill=TEXT_LIGHT)
        y += 22
        # Description
        words = list(desc)
        lines = []
        line = ""
        for ch in words:
            test = line + ch
            bbox = draw.textbbox((0, 0), test, font=body_font)
            if bbox[2] - bbox[0] > SIZE - card_margin * 2 - 80:
                lines.append(line)
                line = ch
            else:
                line = test
        if line:
            lines.append(line)
        
        for l in lines:
            draw.text((card_margin + 55, y), l, font=body_font, fill=TEXT_GRAY)
            y += 20
        y += 15
    
    # Bottom seal
    y = card_top + card_h - 50
    draw_centered_text(draw, "© 点暇斋 · 全部作品版权登记 · 合法独立发行", 
                      load_font('msyh.ttc', 12), y, GOLD)
    
    path = os.path.join(OUT_DIR, '图5_版权声明.jpg')
    img.save(path, 'JPEG', quality=90)
    print(f'OK: 图5_版权声明.jpg')
    return img

# ================================================================
# IMAGE 6: Delivery + Cross-promotion
# ================================================================
def gen_image6():
    img = Image.new('RGB', (SIZE, SIZE), DARK_BG)
    draw = ImageDraw.Draw(img)
    
    y = 40
    draw_centered_text(draw, "交付方式 & 作者关联作品", load_font('simhei.ttf', 26), y, GOLD)
    y += 10
    draw_line(draw, y + 25, color=GOLD, width=1, margin=80)
    y += 50
    
    # --- Delivery steps ---
    draw_centered_text(draw, "如何收货？简单三步", load_font('msyhbd.ttc', 18), y, TEXT_LIGHT)
    y += 35
    
    steps = [
        ("①", "拍下商品", "点击「立即购买」"),
        ("②", "留言邮箱", "在订单留言/聊天中\n留下邮箱或百度网盘账号"),
        ("③", "查收文件", "24h 内收到百度网盘链接\n含完整版 PDF（529页）"),
    ]
    
    step_w = (SIZE - 100) // 3
    for i, (num, title, desc) in enumerate(steps):
        sx = 50 + i * step_w
        sy = y
        
        # Number circle
        draw.ellipse([(sx + step_w//2 - 18, sy), (sx + step_w//2 + 18, sy + 36)], outline=GOLD, width=2)
        draw_centered_text(draw, num, load_font('msyhbd.ttc', 18), sy + 6, GOLD, step_w)
        
        sy += 45
        draw_centered_text(draw, title, load_font('msyhbd.ttc', 14), sy, TEXT_LIGHT, step_w)
        sy += 22
        for line in desc.split('\n'):
            draw_centered_text(draw, line, FONT_SMALL, sy, TEXT_GRAY, step_w)
            sy += 18
    
    y += 110
    draw.centered_text = draw_centered_text  # already available
    draw_line(draw, y, color=GOLD, width=1, margin=80)
    y += 20
    
    # --- Related works ---
    draw_centered_text(draw, "作者其他在售资料", load_font('msyhbd.ttc', 16), y, GOLD)
    y += 35
    
    works = [
        ("📊", "穿越周期：四种非标新出口", "16页PPT · 教改研讨会专题报告"),
        ("📋", "IP孵化结题报告", "32,000字 · 产教融合范式研究"),
        ("📈", "绩效新政解读", "8章 · 学术排版 · PDF"),
    ]
    
    icon_f = load_font('seguiemj.ttf', 22) if os.path.exists(os.path.join(FONT_DIR, 'seguiemj.ttf')) else load_font('simhei.ttf', 18)
    work_title_f = load_font('msyh.ttc', 14)
    work_desc_f = FONT_SMALL
    
    for icon, title, desc in works:
        draw.text((120, y), icon, font=icon_f, fill=GOLD)
        draw.text((155, y), title, font=work_title_f, fill=TEXT_LIGHT)
        y += 20
        draw.text((155, y), desc, font=work_desc_f, fill=TEXT_GRAY)
        y += 28
    
    y += 5
    draw_centered_text(draw, "点击作者头像查看全部在售商品 →", load_font('msyh.ttc', 13), y, GOLD)
    
    path = os.path.join(OUT_DIR, '图6_交付导流.jpg')
    img.save(path, 'JPEG', quality=90)
    print(f'OK: 图6_交付导流.jpg')
    return img

# ================================================================
# MAIN
# ================================================================
if __name__ == '__main__':
    os.makedirs(OUT_DIR, exist_ok=True)
    
    print("Generating 6 listing images...")
    gen_image1()
    gen_image2()
    gen_image3()
    gen_image4()
    gen_image5()
    gen_image6()
    
    # Print total size
    total = sum(os.path.getsize(os.path.join(OUT_DIR, f)) 
                for f in os.listdir(OUT_DIR) if f.endswith('.jpg'))
    print(f"\nDone! 6 images, total: {total/1024:.0f} KB")
