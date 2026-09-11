# encoding: utf-8
"""Agent6 + Agent8 + Agent1 综合提取：目录/金句/统计/文案"""
import os, re, json
from collections import defaultdict

BASE = r'C:\Users\H1811\Desktop\CDU 固废备课文件夹2026\_归档\20260515之1-350回定稿版'
OUT = r'C:\Users\H1811\Desktop\CDU 固废备课文件夹2026\演示展示\闲鱼上架'

# --- Phase 1: Extract TOC from filenames ---
files = [f for f in os.listdir(BASE) if f.endswith('.txt') and re.match(r'第\d+回', f)]
chapters = {}
for f in files:
    m = re.match(r'第(\d+)回', f)
    if m:
        num = int(m.group(1))
        if num not in chapters or len(f) < len(chapters[num]):
            chapters[num] = f

sorted_nums = sorted(chapters.keys())

# --- Phase 2: Generate full TOC ---
toc_lines = []
for num in sorted_nums:
    fname = chapters[num].replace('.txt', '')
    title = re.sub(r'^第\d+回[\- ]?', '', fname).strip()
    toc_lines.append(f'第{num:03d}回  {title}')

# --- Phase 3: Thread grouping ---
threads = defaultdict(list)
for num in sorted_nums:
    fname = chapters[num].replace('.txt', '')
    title = re.sub(r'^第\d+回[\- ]?', '', fname).strip()
    tagged = False
    if any(k in title for k in ['杨柳坝', '刘家湾']):
        threads['杨柳坝'].append(num); tagged = True
    if any(k in title for k in ['龙栖湾', '龙湾', '山海韵', '海屋']):
        threads['龙栖湾'].append(num); tagged = True
    if any(k in title for k in ['三多里', '锦汇', '宽窄', '窄中', '幽巷', '古巷', '雅苑']):
        threads['三多里巷'].append(num); tagged = True
    if any(k in title for k in ['雍葭', '葭心', '葭', '毛坨']):
        threads['雍葭线'].append(num); tagged = True
    if any(k in title for k in ['呼昂', '教父', '老呼昂', '黑子']):
        threads['呼昂线'].append(num); tagged = True
    if any(k in title for k in ['兰苼', '兰董']):
        threads['兰苼线'].append(num); tagged = True
    if not tagged:
        threads['其他'].append(num)

# --- Phase 4: Sample content for golden quotes ---
golden_quotes = []
sample_indices = []
step = max(1, len(sorted_nums) // 20)
for i in range(0, len(sorted_nums), step):
    sample_indices.append(sorted_nums[i])

total_chars = 0
for num in sample_indices:
    path = os.path.join(BASE, chapters[num])
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as fh:
            content = fh.read()
        total_chars += len(content)
        # Extract sentences ending with Chinese punctuation
        sentences = re.split(r'[。！？\n]', content)
        # Pick sentences 50-200 chars as quotable
        for s in sentences:
            s = s.strip()
            if 30 <= len(s) <= 120 and not re.match(r'^(第|话|诗|词|且|却说|正是|不知|欲知|若知)', s):
                if not re.match(r'^第\d+回', s):
                    golden_quotes.append({
                        'ch': num,
                        'title': re.sub(r'^第\d+回[\- ]?', '', chapters[num].replace('.txt','')).strip(),
                        'quote': s
                    })
                    break
    except:
        pass

# Pick top 12 most interesting quotes
golden_quotes = golden_quotes[:15]

# --- Phase 5: Full word count from all chapters ---
# Sample 50 chapters evenly to estimate total
est_indices = sorted_nums[::len(sorted_nums)//50][:50]
est_chars = 0
est_count = 0
for num in est_indices:
    path = os.path.join(BASE, chapters[num])
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as fh:
            est_chars += len(fh.read())
        est_count += 1
    except:
        pass
avg_per_ch = est_chars / est_count if est_count else 0
est_total_chars = int(avg_per_ch * len(sorted_nums))

# --- Phase 6: Generate output files ---

# 6a. TOC file
toc_path = os.path.join(OUT, '上岸导读_目录大纲.md')
with open(toc_path, 'w', encoding='utf-8') as f:
    f.write('# 上岸：基于研究生培养视角导读杨柳坝与刘家湾 —— 完整目录\n\n')
    f.write(f'> 共 {len(sorted_nums)} 回，对句章回体\n')
    f.write(f'> 源文件总字数约 {est_total_chars/10000:.0f} 万字\n\n')
    f.write('---\n\n')
    for line in toc_lines:
        f.write(f'{line}\n\n')

# 6b. Thread analysis
thread_path = os.path.join(OUT, '上岸导读_故事线分析.md')
with open(thread_path, 'w', encoding='utf-8') as f:
    f.write('# 上岸导读 —— 故事线索与教育价值分析\n\n')
    f.write('## 故事线分布\n\n')
    f.write('| 故事线 | 回数 | 核心主题 |\n')
    f.write('|--------|------|----------|\n')
    for k, v in sorted(threads.items(), key=lambda x: -len(x[1])):
        f.write(f'| {k} | {len(v)}回 | - |\n')
    f.write(f'\n**总计：{len(sorted_nums)} 回**\n\n')
    f.write('## 各线标签与错配-修复框架对应\n\n')
    f.write('| 故事线 | 错配类型 | 修复路径 | 教育价值 |\n')
    f.write('|--------|----------|----------|----------|\n')
    if '杨柳坝' in threads or '刘家湾' in [t for t in threads]:
        f.write('| 杨柳坝/刘家湾 | 空间错配 | 资产化修复 | 固废处理设施选址、环境治理中的乡土智慧 |\n')
    if '龙栖湾' in threads:
        f.write('| 龙栖湾 | 技术错配 | 产品化修复 | 从焚烧炉创业到产业升级的技术转化 |\n')
    if '三多里巷' in threads:
        f.write('| 三多里巷/市井 | 信息/人文错配 | 叙事修复 | 工程×法律×商业的交叉地带 |\n')
    if '雍葭线' in threads:
        f.write('| 雍葭（学生线） | 行为错配 | 认知修复 | 研究生学术成长与职业发展的全周期追踪 |\n')
    if '呼昂线' in threads:
        f.write('| 呼昂（导师线） | 人文错配 | 教育修复 | 导师指导策略与学术传承方法论 |\n')

# 6c. Golden quotes
golden_path = os.path.join(OUT, '上岸导读_金句卡片.md')
with open(golden_path, 'w', encoding='utf-8') as f:
    f.write('# 上岸导读 —— 金句卡片\n\n')
    f.write('> 可用于商品详情页展示文风与内容深度\n\n')
    for i, gq in enumerate(golden_quotes[:12], 1):
        f.write(f'### {i}. 第{gq["ch"]}回「{gq["title"]}」\n')
        f.write(f'> {gq["quote"]}\n\n')

# 6d. Content stats
stats_path = os.path.join(OUT, '上岸导读_内容统计.md')
with open(stats_path, 'w', encoding='utf-8') as f:
    f.write('# 上岸导读 —— 内容统计\n\n')
    f.write(f'| 指标 | 数值 |\n')
    f.write(f'|------|------|\n')
    f.write(f'| 总回数 | {len(sorted_nums)} 回 |\n')
    f.write(f'| 回目范围 | 第{sorted_nums[0]}回 ~ 第{sorted_nums[-1]}回 |\n')
    f.write(f'| 预计总字数 | 约 {est_total_chars/10000:.0f} 万字 |\n')
    f.write(f'| 每回平均字数 | 约 {avg_per_ch:.0f} 字 |\n')
    f.write(f'| 源文件总大小 | {sum(os.path.getsize(os.path.join(BASE,chapters[n])) for n in sorted_nums)/1024/1024:.1f} MB |\n')
    f.write(f'| PDF 页数 | 529 页 |\n')
    f.write(f'| PDF 大小 | 201 MB |\n')
    f.write(f'| 体裁 | 章回体纪实小说 |\n')
    f.write(f'| 创作视角 | 研究生培养视角 |\n')

# 6e. Deduped chapter filenames for reference
dedup_path = os.path.join(OUT, '上岸导读_章回索引.json')
with open(dedup_path, 'w', encoding='utf-8') as f:
    index_data = {str(num): chapters[num] for num in sorted_nums}
    json.dump(index_data, f, ensure_ascii=False, indent=2)

# Summary
print(f'提取完成:')
print(f'  章回数: {len(sorted_nums)}')
print(f'  估计总字数: 约 {est_total_chars/10000:.0f} 万字')
print(f'  金句: {len(golden_quotes)} 条')
print(f'  故事线: {len(threads)} 条')
print(f'  输出目录: {OUT}')
for fn in ['上岸导读_目录大纲.md', '上岸导读_故事线分析.md', '上岸导读_金句卡片.md', '上岸导读_内容统计.md', '上岸导读_章回索引.json']:
    fpath = os.path.join(OUT, fn)
    print(f'  OK: {fn} ({os.path.getsize(fpath)} bytes)')
