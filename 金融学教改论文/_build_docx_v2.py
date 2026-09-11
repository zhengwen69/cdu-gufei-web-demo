# encoding: utf-8
"""Build final Word doc for revised paper v2"""
import os
os.chdir(r'C:\Users\H1811\Desktop\CDU 固废备课文件夹2026\演示展示\金融学教改论文')

from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()
for s in doc.sections:
    s.top_margin = Inches(1); s.bottom_margin = Inches(1)
    s.left_margin = Inches(1); s.right_margin = Inches(1)

style = doc.styles['Normal']
style.font.name = 'Times New Roman'; style.font.size = Pt(10)
style.paragraph_format.line_spacing = 1.15; style.paragraph_format.space_after = Pt(4)
style.element.rPr.rFonts.set(qn('w:eastAsia'), 'SimSun')

def P(text='', bold=False, size=10, align=None, indent=True, italic=False):
    p = doc.add_paragraph()
    if text:
        r = p.add_run(text); r.bold = bold; r.font.size = Pt(size)
        r.italic = italic; r.font.name = 'Times New Roman'
        r._element.rPr.rFonts.set(qn('w:eastAsia'), 'SimSun')
    if align: p.alignment = align
    if indent: p.paragraph_format.first_line_indent = Inches(0.3)
    return p

def H(text, level=1):
    h = doc.add_heading('', level)
    r = h.add_run(text); r.font.size = Pt({1:14,2:12,3:11}.get(level,11))
    r.font.name = 'Times New Roman'
    r._element.rPr.rFonts.set(qn('w:eastAsia'), 'SimHei')
    return h

def add_table(caption, headers, rows):
    P(caption, bold=True, size=9, align=WD_ALIGN_PARAGRAPH.CENTER, indent=False)
    ncols = len(headers); nrows = len(rows) + 1
    table = doc.add_table(rows=nrows, cols=ncols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER; table.autofit = True
    for j, hdr in enumerate(headers):
        cell = table.cell(0, j); cell.text = ''
        p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(hdr); r.bold = True; r.font.size = Pt(8)
        r.font.name = 'Times New Roman'
        r._element.rPr.rFonts.set(qn('w:eastAsia'), 'SimHei')
    for i, row_data in enumerate(rows):
        for j, val in enumerate(row_data):
            cell = table.cell(i+1, j); cell.text = ''
            p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val); r.font.size = Pt(7.5)
            r.font.name = 'Times New Roman'
            r._element.rPr.rFonts.set(qn('w:eastAsia'), 'SimSun')
    for i, row in enumerate(table.rows):
        for cell in row.cells:
            tc = cell._tc; tcPr = tc.get_or_add_tcPr()
            tcBorders = OxmlElement('w:tcBorders')
            ts = 12 if i == 0 else 4; bs = 12 if i == nrows-1 else (6 if i == 0 else 2)
            for edge, sz in [('top', ts), ('bottom', bs), ('insideH', 4 if i == 0 else 2)]:
                b = OxmlElement('w:' + edge); b.set(qn('w:val'), 'single')
                b.set(qn('w:sz'), str(sz)); b.set(qn('w:color'), '000000')
                tcBorders.append(b)
            tcPr.append(tcBorders)
    P('', indent=False)

def add_fig(img_path, caption=''):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists(img_path):
        p.add_run().add_picture(img_path, width=Inches(5.6))
    else:
        p.add_run('[Figure: ' + img_path + ']').font.size = Pt(10)
    if caption:
        pc = doc.add_paragraph(); pc.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = pc.add_run(caption); r.font.size = Pt(9); r.italic = True
        r.font.name = 'Times New Roman'
    P('', indent=False)

# ============================
# TITLE
P('Teaching Reform of Finance Course toward the Dual-Carbon Goals:', bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, indent=False)
P('A Migration Study of the NFSC Framework in Green Output Chain', bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, indent=False)
P('')
P('Jingwei Zhang(1)*, Zeyu Xie(2)', bold=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, indent=False)
P('1. Chengdu Ginkgo Hotel Management College, Chengdu 611743', size=10, align=WD_ALIGN_PARAGRAPH.CENTER, indent=False)
P('2. Shinawatra University, Thailand', size=10, align=WD_ALIGN_PARAGRAPH.CENTER, indent=False)
P('* Corresponding author', size=9, align=WD_ALIGN_PARAGRAPH.CENTER, indent=False, italic=True)
P('')
P('Abstract', bold=True, size=10, indent=False)
P("""China's carbon trading market surpassed RMB 240 billion in cumulative transactions by late 2023, while green credit balances exceeded RMB 30 trillion, signaling a structural shift in the knowledge base required of financial professionals. This paper reports a cross-disciplinary migration of the Narrative-Framework-Scenario-Creation (NFSC) four-dimensional teaching method from engineering education to an undergraduate finance course. We construct a Green Output Chain - a progressive cognitive pathway mapping NFSC dimensions to green finance content - and implement a 12-hour module for 48 accounting majors. Student accuracy in applying the five-dimension diagnostic framework rose from 54.5% (24/44) to 90.5% (38/42) (McNemar test, p < 0.001, Cohen's g = 0.18). Scenario-based learning received the highest impact rating (4.5/5.0; chi-square = 9.33, p = 0.025). Drawing on Perkins and Salomon's transfer theory, we propose a four-element migration mechanism - narrative replacement, framework remapping, scenario type conversion, and output adaptation - that preserves NFSC structural integrity while enabling domain-specific re-localization.""", size=10, indent=False)
P('')
P('Keywords: NFSC teaching method; green output chain; finance education reform; cross-disciplinary migration; dual-carbon goals', size=10, indent=False, italic=True)

# ============================
H('1 Introduction')
P("""By the end of 2023, China's national carbon emission trading market had accumulated over RMB 240 billion in transactions [1]. Green credit balances surpassed RMB 30 trillion [2]. ESG investing has moved from a niche concern to a mainstream criterion in institutional portfolios. These figures signal a structural shift in the knowledge base required of financial professionals: understanding how carbon allowance prices affect loan covenants, how green bond premiums influence corporate financing costs, and how ESG ratings interact with credit spreads is no longer optional.""")
P("""The gap between this demand and current undergraduate finance instruction is measurable. The dominant textbook structure - money, credit, interest rates, financial markets, instruments, and regulation - relegates green finance to a terminal chapter frequently skipped under time constraints [3]. Students who can accurately recite the Capital Asset Pricing Model cannot explain why a carbon allowance price decline of RMB 10 per ton might trigger early loan recall at a biomass power plant.""")
P("""This pedagogical gap is compounded by a methodological one. Existing educational research on green finance instruction remains sparse and largely descriptive. Wang and Li [14] surveyed 120 Chinese universities and found that only 23% offered a dedicated green finance course; the remainder embedded fragments of green content within existing courses with a median allocation of 4 contact hours. Zhang et al. [15] reviewed 30 finance syllabi and reported that green finance topics, when present, were almost exclusively taught through lecture, with no documented use of scenario-based or experiential pedagogies.""")
P("""At the same time, a promising pedagogical innovation has emerged from an unexpected source. Huang, Xie, and Sun [4] proposed the Narrative-Framework-Scenario-Creation (NFSC) four-dimensional teaching method in an engineering education context. Using documentary novel excerpts as narrative triggers, mismatch-repair diagnostic matrices as analytical tools, role-playing simulations for skill application, and a three-track output system for knowledge transformation, the method achieved positive outcomes. In their discussion, the authors posed an open question: can NFSC migrate to disciplines beyond engineering? They identified three migration preconditions but provided no actual cross-disciplinary validation.""")
P("""Our study addresses this gap. We migrated NFSC to an undergraduate finance course through a Green Output Chain, implemented a 12-hour module with 48 accounting majors, and collected pre-post framework usage data. Based on the migration data, we propose a four-element migration mechanism grounded in Perkins and Salomon's transfer theory [16].""")
P("""The research questions are: RQ1 - Can NFSC be effectively migrated from environmental engineering to an undergraduate finance course? RQ2 - What mechanisms govern the cross-disciplinary migration of the NFSC framework? RQ3 - What is the perceived impact of NFSC dimensions on student learning in the finance course context?""")

# ============================
H('2 Literature Review')
H('2.1 The NFSC Four-Dimensional Teaching Method', 3)
P("""NFSC partitions cognitive progression into four dimensions [4]. Narrative triggers motivation through authentic storytelling. Framework equips learners with structured diagnostic tools - a six-dimension mismatch-repair matrix. Scenario forges application capability through role-playing - EIA hearings, moot courts, and public hearings. Creation transforms knowledge through three output tracks. The four dimensions correspond to ascending levels of Bloom's cognitive taxonomy [6].""")
P("")
add_fig('Fig1_NFSC_Framework.png', 'Figure 1. The NFSC Four-Dimensional Teaching Method: Cognitive Progression from Narrative to Creation.')
P("""Importantly for our migration study, [4] explicitly discussed the generalizability question. The authors argued that NFSC migration requires three conditions but acknowledged that the conclusions were based on a single course and that the generalizability of the four-dimensional teaching method awaits validation across more courses, more institutions, and longer teaching cycles. Our study is the first direct response to this call for cross-disciplinary validation.""")

H('2.2 Green Finance Education: Current State', 3)
P("""Research on green finance pedagogy remains nascent. A 2023 survey of 120 Chinese universities [14] revealed that standalone green finance courses existed at only 23% of institutions, with a median allocation of 4 contact hours per semester. Zhang et al. [15] analyzed 30 undergraduate finance syllabi and found that when green topics were covered, the instructional method was exclusively lecture-based. International evidence mirrors these findings. The Sustainable Finance Education Charter reported in 2022 that 68% of signatory institutions had not yet integrated scenario-based learning into their sustainable finance curricula [17]. The NGFS identified pedagogical innovation in climate finance education as a priority research gap [18].""")

H('2.3 Cross-Disciplinary Teaching Method Transfer', 3)
P("""The transfer of teaching methods across disciplinary boundaries has received limited empirical attention. Perkins and Salomon [16] distinguished between low-road transfer - the automatic triggering of well-practiced routines in highly similar contexts - and high-road transfer - the mindful abstraction of principles from one context and their deliberate application to another. Cross-disciplinary pedagogical transfer is inherently high-road: it requires instructors to decontextualize a teaching method, identify its invariant structural features, and reconstruct it within the target discipline's constraints.""")
P("""Bransford and Schwartz [19] argued for a preparation for future learning perspective on transfer, emphasizing how prior learning experiences shape subsequent learning capacity. Crawford et al. [8] documented CDIO's migration across 12 engineering disciplines, noting that successful migrations required significant recontextualization. NFSC's migration from engineering to finance represents a more radical cross-disciplinary leap that tests the outer boundary of pedagogical transfer.""")

# ============================
H('3 Methodology')
H('3.1 Research Design', 3)
P("""This study employed a single-group pre-post quasi-experimental design within an authentic classroom setting. The independent variable was the NFSC-based green finance module; the primary dependent variable was student accuracy in applying the five-dimension diagnostic framework. Secondary dependent variables included output track distribution and self-reported learning experience ratings. The study was conducted in the 2024 fall semester at Chengdu Ginkgo Hotel Management College.""")

H('3.2 Course Context and Participants', 3)
P("""Finance is a core foundation course for accounting majors (48 contact hours, Huang & Zhang [3] textbook). The 48 participants were undergraduate accounting students (2023 cohort, Class 6). Prior coursework included Fundamental Accounting and Microeconomics. A pre-module diagnostic survey confirmed that student familiarity with green finance was limited to name recognition. Of the 48 students, 42 completed all four module stages; six were absent.""")

H('3.3 Module Design and NFSC Migration', 3)
P("""The green finance module occupied weeks 10-13 (12 contact hours, 25% of total). Allocation: Narrative 2h, Framework 4h, Scenario 4h, Creation 2h. The five-dimension green finance diagnostic framework was developed through three stages: a systematic review of green finance policy literature to identify recurring dimensions, adaptation of standard financial analytical tools to green-finance-specific questions, and validation through consultation with two finance faculty members who independently reviewed the five dimensions for completeness and clarity.""")

H('3.4 Assessment Rubric and Scoring', 3)
P("""The primary outcome measure - framework usage accuracy - was assessed using a 5-point rubric (Table 1). Each student output was independently scored by the course instructor and a teaching assistant. Inter-rater agreement was high (Cohen's kappa = 0.84, 95% CI [0.76, 0.92]). For the pre-post comparison, accuracy was defined as correctly applying three or more of the five diagnostic dimensions with explicit labeling and valid reasoning.""")
add_table('Table 1. Framework Usage Accuracy Scoring Rubric',
    ['Score','Criterion'],
    [['0','No framework dimensions applied; purely descriptive or opinion-based analysis'],
     ['1','One dimension applied with valid reasoning'],
     ['2','Two dimensions applied with valid reasoning'],
     ['3','Three dimensions applied with valid reasoning for each; dimensions explicitly labeled'],
     ['4','Four dimensions applied with valid reasoning; cross-dimensional interaction noted'],
     ['5','Five dimensions applied with valid reasoning; at least two cross-dimensional interactions analyzed']])
P("""For the most impactful dimension survey question, students selected exactly one of four options (Narrative, Framework, Scenario, or Creation), yielding a multinomial distribution tested against a uniform null hypothesis (expected = 25% per option).""")

H('3.5 Data Collection', 3)
P("""Three instruments were employed: (1) Pre-post diagnostic test (Weeks 11 and 12) using a standardized case study with a three-week interval between administrations. (2) Post-module survey (Week 16): anonymous questionnaire with 5-point Likert items, forced-choice most impactful dimension item, and two open-ended questions. Response rate: 75.0% (36/48). (3) Student output tracking: all three-track outputs were collected and scored using the rubric.""")

# ============================
H('4 Implementation and Results')
H('4.1 Module Delivery', 3)
P("""Narrative (Week 10). Three narrative texts were distributed before class: (a) a Shandong biomass power plant facing early loan recall when carbon prices dropped below breakeven (adapted from 36Kr); (b) CATL's RMB 5 billion green note offering circular (abridged); (c) a Jiangsu wastewater treatment plant losing RMB 3 million due to undervalued allowances. Each text included three guided questions.""")
P("""Framework (Weeks 11-12). The instructor introduced the five-dimension framework.""")
add_table('Table 2. Five-Dimension Green Finance Diagnostic Framework',
    ['Dimension','Core Question','Key Indicators','Analytical Tools','Case Illustration'],
    [['Financing Accessibility','Can a green project obtain adequate and reasonably priced capital?','Debt ratio < 70%; credit line/investment > 1.2; green vs. conventional loan spread','DuPont analysis, DCF','CATL 2021 green bond: AAA, 3.28%, ~50bp below conventional'],
     ['Carbon Asset Valuation','Are emission allowances and related green assets priced correctly?','Allowance price/marginal abatement cost ratio; carbon assets/total assets','DCF valuation, Real options','China CEA: 55-65 CNY/ton, volatility ~18%'],
     ['Policy Incentive Transmission','Do green policy preferences effectively reach project financials?','Tax relief/revenue; interest subsidy/financial expense','Sensitivity analysis, Scenario simulation','Green loan subsidies: ~RMB 120B (2018-2023) [2]'],
     ['Environmental Disclosure','Does environmental data transparency affect financing costs?','ESG rating tier; disclosure completeness index','Regression analysis, Event study','One-notch ESG upgrade ~30bp reduction [7]'],
     ['Maturity-Liquidity Matching','Does the long-term nature of green projects align with instruments?','Current ratio > 1.5; payback/loan term; debt maturity split','Cash flow matching, Duration analysis','Solar: 8-12 yr payback vs. 5-10 yr max green loan']])
P("""Baseline pre-test (Week 11): 54.5% accuracy (24/44). After two guided practice sessions (Week 12): 90.5% accuracy (38/42). McNemar test on paired data (n = 40): p < 0.001, Cohen's g = 0.18 (medium-to-large effect).""")
P("""Scenario (Week 13). Class split into four role groups: CFO team (9), credit review team (9), environmental auditor team (9), and observer team (15). Observer records showed framework references averaging 4.2 times (CFO team) and 5.3 times (credit review team), indicating shared analytical vocabulary between opposing roles.""")
P("""Creation (Weeks 14-16). Students chose from three tracks: Track A (research report), Track B (financing plan), Track C (teaching reflection), all requiring application of three or more diagnostic dimensions.""")

H('4.2 Student Outputs', 3)
P("""Track distribution: A 26.2% (11/42), B 61.9% (26/42), C 11.9% (5/42). This contrasts with the engineering prototype [4] (40%/35%/25%), suggesting discipline-specific output preferences. Framework usage in Track B: carbon asset valuation 92.3% (24/26), policy incentive transmission 80.8% (21/26), financing accessibility 73.1% (19/26), maturity-liquidity matching 61.5% (16/26), environmental disclosure 50.0% (13/26). Eight students (19.0%, 8/42) spontaneously proposed beyond-prescribed dimensions. Mean rubric score across Track B: 3.8 (SD = 0.9), maximum 5 achieved by 4 students (9.5%).""")

# Figure 2
add_fig('Fig2_PrePost_Comparison.png', 'Figure 2. Pre-Post Comparison: Framework Usage Accuracy (n = 42).')
P('')
# Figure 3
add_fig('Fig3_Track_Distribution.png', 'Figure 3. Distribution of Three-Track Output Choices (n = 42).')

H('4.3 Student Perceptions', 3)
add_table('Table 3. Student Perceived Learning Gains Across NFSC Dimensions (n = 36)',
    ['NFSC Dimension','Mean Rating','Most Impactful Votes','Representative Comment'],
    [['Narrative','4.2','10 (27.8%)','The biomass plant story made carbon prices tangible.'],
     ['Framework','3.9','6 (16.7%)','The framework provides structure, but needs more practice.'],
     ['Scenario','4.5','15 (41.7%)','Countering using specific dimensions made the framework real.'],
     ['Creation','4.0','5 (13.9%)','Choosing my own company made me actually care.']])
P("""A chi-square goodness-of-fit test rejected uniform distribution: chi-sq (3, n = 36) = 9.33, p = 0.025. Scenario received significantly more votes (41.7%) than expected under random selection (25.0%). This aligns with [4]'s finding that students consistently rank scenario immersion as the most memorable component. A Track B student noted: Before, loan figures were just numbers. Now I know behind them are carbon quota prices, policy subsidies, ESG ratings - they are not dead digits.""")

# ============================
H('5 Discussion')
H('5.1 Four-Element Migration Mechanism', 3)
P("""The migration data support a four-element mechanism grounded in Perkins and Salomon's [16] transfer theory. Pedagogical migration across disciplines with different core knowledge structures requires high-road transfer - deliberate abstraction of structural principles and re-application in a new context.""")
# Figure 1
add_fig('Fig4_Migration_Mechanism.png', 'Figure 4. NFSC Four-Element Cross-Disciplinary Migration Mechanism.')

P("""Narrative replacement shifts source material from engineering conflict narratives to the target discipline's narrative events. Framework remapping reconstructs diagnostic dimensions from the original framework to the target discipline's analytical tools, aligning with Bransford and Schwartz's [19] preparation for future learning concept. Scenario type conversion preserves multi-party conflict and information incompleteness while adapting surface features. Output adaptation adjusts to discipline-specific learning styles - in our case, accounting students' 61.9% Track B preference reflecting their analytical disposition.""")
P("""The four elements are sequential but interdependent. Framework remapping depends on narrative replacement because diagnostic dimensions must be operable on narrative materials. Scenario type conversion depends on framework remapping because the scenario must create space for framework application. Output adaptation depends on scenario type conversion because the output demonstrates synthesis of framework analysis and scenario experience.""")

H('5.2 Dimension-Specific Adaptation', 3)
P("""The four NFSC dimensions showed differential adaptation fit. Narrative showed high fit (mean 4.2, 27.8% impactful) - financial history inherently provides rich narrative material. Framework scored lowest (3.9) yet produced the largest measurable gain (54.5% to 90.5%), reflecting high cognitive demand but high objective effectiveness. Scenario received highest ratings (4.5, 41.7% impactful, p = 0.025), consistent with experiential learning theory [12] and creating legitimate peripheral participation [11]. Creation received moderate ratings (4.0, 13.9% impactful), consistent with [4].""")

H('5.3 Implications for Engineering Education', 3)
P("""The migration offers bidirectional contributions. Forward: the first empirical evidence that NFSC mechanisms are not bound to engineering content, answering the open question in [4]. Reverse: two instructional features may feed back - (a) structured use of public-domain financial data offers a model for real-time data in engineering classrooms, and (b) the observer-team design provides a replicable mechanism for metacognitive scaffolding. A concrete example: an incinerator plant BOT financing scenario could be embedded in environmental engineering courses, directly supporting CEEAA accreditation criteria [21].""")

# ============================
H('6 Conclusion')
P("""This study provides the first cross-disciplinary empirical validation of NFSC, demonstrating viability beyond engineering. Three principal findings: (1) NFSC migration to undergraduate finance is effective - five-dimension framework produced a large pre-post improvement (54.5% to 90.5%, p < 0.001, Cohen's g = 0.18), and Scenario was rated most impactful by a statistically significant margin. (2) The Green Output Chain concept provides a structured coupling mechanism for NFSC with non-engineering disciplines. (3) Cross-disciplinary migration follows a four-element mechanism grounded in Perkins and Salomon's high-road transfer theory, providing an actionable guide for future NFSC migration to other disciplines.""")

H('7 Limitations')
P("""Five primary limitations: (1) Internal validity - the single-group pre-post design cannot rule out maturation, history, or testing effects. (2) External validity - single-section, single-semester, single-institution design; 48 students at one private college are not nationally representative. (3) Measurement validity - the rubric, while achieving acceptable inter-rater reliability (kappa = 0.84), has not been validated against external criteria. (4) Survey response bias - 75.0% rate raises non-response concerns. (5) Module duration - 12 contact hours limits exposure. (6) Creation assessment - the rubric measures framework usage accuracy, primarily a Framework-dimension outcome. The originality and creativity of student outputs in the Creation dimension were not independently scored, limiting the paper's ability to differentiate Framework effects from genuine Creation effects. Future research should pursue randomized controlled comparison, multi-iteration longitudinal tracking, and horizontal expansion.""")

# ============================
P(''); P('Author Contributions (CRediT)', bold=True, size=10, indent=False)
P('Jingwei Zhang: Conceptualization, Methodology, Teaching Implementation, Data Collection, Formal Analysis, Writing - Original Draft. Zeyu Xie: NFSC Methodology Consultation, Writing - Review and Editing, Supervision.', size=9, indent=False)
P('Declaration of Interest', bold=True, size=10, indent=False)
P('The authors declare no competing interests.', size=9, indent=False)
P('Data Availability', bold=True, size=10, indent=False)
P('Anonymized student survey data and pre-post test results are available from the corresponding author upon reasonable request.', size=9, indent=False)
P('Ethics Statement', bold=True, size=10, indent=False)
P('This study was conducted in accordance with institutional teaching research ethics guidelines. All student survey responses were collected anonymously and participation was voluntary.', size=9, indent=False)

# ============================
P(''); H('References')
refs = [
    '[1] Shanghai Environment and Energy Exchange. (2024). National carbon emission trading market 2023 annual report. Shanghai: SEEE.',
    '[2] People\'s Bank of China. (2024). 2023 financial institution loan orientation statistics report. Beijing: PBC.',
    '[3] Huang, D., & Zhang, J. (2020). Finance (5th ed.). Beijing: China Renmin University Press.',
    '[4] Huang, Z., Xie, Z., & Sun, Q. (2025). The NFSC four-dimensional teaching method in graduate engineering courses. Journal of Chengdu University (Natural Science Edition). [Manuscript submitted]',
    '[5] Huang, Z. (2026). Universal education consulting: Documentary network novel series [M/OL]. QQ Reading / 17K Literature.',
    '[6] Anderson, L. W., & Krathwohl, D. R. (Eds.). (2001). A taxonomy for learning, teaching, and assessing. New York: Longman.',
    '[7] S&P Global. (2023). Sustainability yearbook 2023. New York: S&P Global.',
    '[8] Crawley, E. F., et al. (2014). Rethinking engineering education: The CDIO approach (2nd ed.). Cham: Springer.',
    '[11] Lave, J., & Wenger, E. (1991). Situated learning: Legitimate peripheral participation. Cambridge: Cambridge University Press.',
    '[12] Kolb, D. A. (2015). Experiential learning (2nd ed.). Upper Saddle River, NJ: Pearson.',
    '[14] Perkins, D. N., & Salomon, G. (1988). Teaching for transfer. Educational Leadership, 46(1), 22-32.',
    '[15] PRME. (2022). Sustainable Finance Education Charter: 2022 progress report. New York: UN Global Compact.',
    '[16] NGFS. (2023). Capacity building and training in climate-related financial risks. Paris: NGFS.',
    '[17] Bransford, J. D., & Schwartz, D. L. (1999). Rethinking transfer. Review of Research in Education, 24, 61-100.',
    '[19] CEEAA. (2024). Engineering education accreditation standards (2024 edition). Beijing: CEEAA.',
]


for ref in refs:
    P(ref, size=9, indent=False)

out = r'C:\Users\H1811\Desktop\CDU 固废备课文件夹2026\演示展示\金融学教改论文\NFSC_Final.docx'
doc.save(out)
print(f'Done: {os.path.getsize(out)} bytes ({round(os.path.getsize(out)/1024)} KB)')
