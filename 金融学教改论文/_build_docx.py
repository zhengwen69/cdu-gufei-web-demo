# encoding: utf-8
"""Build Word doc with embedded tables and figures"""
import os
os.chdir(r'C:\Users\H1811\Desktop\CDU 固废备课文件夹2026\演示展示\金融学教改论文')

from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
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
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    
    for j, hdr in enumerate(headers):
        cell = table.cell(0, j); cell.text = ''
        p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(hdr); r.bold = True; r.font.size = Pt(8)
        r.font.name = 'Times New Roman'
        r._element.rPr.rFonts.set(qn('w:eastAsia'), 'SimHei')
    
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = table.cell(i+1, j); cell.text = ''
            p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val); r.font.size = Pt(7.5)
            r.font.name = 'Times New Roman'
            r._element.rPr.rFonts.set(qn('w:eastAsia'), 'SimSun')
    
    # Three-line borders
    for i, row in enumerate(table.rows):
        for cell in row.cells:
            tc = cell._tc; tcPr = tc.get_or_add_tcPr()
            tcBorders = OxmlElement('w:tcBorders')
            top_sz = 12 if i == 0 else 4
            bot_sz = 12 if i == nrows-1 else (6 if i == 0 else 2)
            for edge, sz in [('top', top_sz), ('bottom', bot_sz), ('insideH', 4 if i == 0 else 2)]:
                b = OxmlElement('w:' + edge)
                b.set(qn('w:val'), 'single'); b.set(qn('w:sz'), str(sz)); b.set(qn('w:color'), '000000')
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
# BUILD
# ============================

P('Teaching Reform of Finance Course toward the Dual-Carbon Goals:', bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, indent=False)
P('A Migration Study of the NFSC Framework in Green Output Chain', bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, indent=False)
P('')
P('Jingwei Zhang(1)*, Zeyu Xie(2)', bold=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, indent=False)
P('1. Chengdu Ginkgo Hotel Management College, Chengdu 611743', size=10, align=WD_ALIGN_PARAGRAPH.CENTER, indent=False)
P('2. Shinawatra University, Thailand', size=10, align=WD_ALIGN_PARAGRAPH.CENTER, indent=False)
P('* Corresponding author', size=9, align=WD_ALIGN_PARAGRAPH.CENTER, indent=False, italic=True)
P('')
P('Abstract', bold=True, size=10, indent=False)
P("""China's carbon trading market surpassed RMB 240 billion in cumulative transaction value by late 2023, while green credit balances exceeded RMB 30 trillion. These numbers create a practical demand that undergraduate finance courses have yet to meet: future financial professionals must understand how carbon prices, ESG ratings, and green policy incentives affect lending, valuation, and investment decisions. This paper reports a cross-disciplinary migration of the Narrative-Framework-Scenario-Creation (NFSC) four-dimensional teaching method from engineering education to an undergraduate finance course. We construct a Green Output Chain - a progressive cognitive pathway mapping NFSC dimensions to green finance content. A 12-hour green finance module was delivered to 48 accounting majors. Student accuracy in applying three or more framework dimensions rose from 55% at baseline to 91% after practice. Among three output tracks, 61.9% chose financing plan design. Scenario received the highest impact rating (4.5/5.0). A four-element migration mechanism is proposed to explain how NFSC preserves structural integrity while enabling domain-specific content re-localization.""", size=10, indent=False)
P('')
P('Keywords: NFSC teaching method; green output chain; finance education reform; cross-disciplinary migration; dual-carbon goals', size=10, indent=False, italic=True)

# 1
H('1 Introduction')
P("""By the end of 2023, China's national carbon emission trading market had accumulated over RMB 240 billion in transactions [1]. Green credit balances had surpassed RMB 30 trillion [2]. ESG investing had shifted from a niche concern to a mainstream investment criterion. These figures represent more than economic data points - they signal a structural change in what financial professionals must know.""")

P("""The gap between this demand and current undergraduate finance instruction is measurable. The dominant textbook structure - money, credit, interest rates, markets, instruments, regulation - treats green finance as a terminal chapter, often skipped under time pressure [3]. Students who can recite the CAPM formula cannot explain why a carbon allowance price drop of RMB 10 per ton might trigger a loan covenant breach at a biomass power plant.""")

P("""Huang, Xie, and Sun [4] proposed the Narrative-Framework-Scenario-Creation (NFSC) four-dimensional teaching method in an engineering education setting. The method uses documentary novel excerpts as narrative triggers, mismatch-repair diagnostic matrices as analytical tools, role-playing simulations for skill application, and a three-track creative output system for knowledge transformation. In their discussion, the authors asked whether NFSC could migrate to other disciplines, identifying three preconditions: a narratable material repository, an abstractable knowledge framework, and instructor capacity for scenario design. But no actual cross-disciplinary migration was reported.""")

P("""Our study answers that open question. We migrated NFSC to an undergraduate finance course by constructing a Green Output Chain concept that systematically maps the four dimensions to green finance content. We implemented a 12-hour green finance module for 48 accounting majors and tracked student framework usage before and after instruction. Based on the migration data, we propose a four-element migration mechanism model.""")

P("""Our contributions are: (1) the first complete cross-disciplinary NFSC migration empirical study beyond engineering; (2) the Green Output Chain concept as a structured coupling mechanism; and (3) a generalizable four-element migration mechanism model.""")

# 2
H('2 Methodology: NFSC Migration and Green Output Chain Design')
H('2.1 The NFSC Framework', 3)
P("""The NFSC method partitions cognitive progression into four dimensions [4]. Narrative triggers motivation through authentic storytelling - in the prototype engineering course, this meant documentary novel excerpts depicting landfill site disputes, incinerator controversies, and community NIMBY protests [5]. Framework equips learners with diagnostic tools - the prototype used a six-dimension mismatch-repair matrix. Scenario forges capabilities through role-playing - EIA hearings, moot courts, site selection hearings. Creation transforms knowledge through a three-track output system: academic paper, course design project, and pedagogical reform essay. The four dimensions follow Bloom's cognitive taxonomy [6].""")

H('2.2 The Green Output Chain', 3)
P("""We define the Green Output Chain as the progressive sequence of learning outputs from mapping NFSC dimensions onto green finance content. Using green as thematic qualifier, each NFSC dimension produces a specific, assessable learning output. Table 1 provides the migration mapping.""")

add_table('Table 1. NFSC Four-Dimensional Migration Mapping',
    ['Dimension','Engineering Prototype [4]','Green Output Chain','Migration Adjustment'],
    [['Narrative','Documentary novel excerpts (landfill externalities, incinerator siting, community protests)','Green finance event narratives (biomass plant carbon revenue shortfall, CATL green bond, wastewater plant carbon quota undervaluation)','Source material shifted from engineering conflict narratives to financial dilemma narratives'],
     ['Framework','Six-dimension mismatch-repair (spatial, technological, behavioral, humanistic, temporal, informational)','Five-dimension green finance diagnostic framework (financing accessibility, carbon asset valuation, policy incentive transmission, environmental disclosure, maturity-liquidity matching)','Framework reconstructed from spatial-social diagnosis to financial dimension diagnosis'],
     ['Scenario','EIA hearings, moot courts, site selection hearings','Green credit approval simulation, carbon trading decision simulation','Scenario converted from engineering decision-making to financial decision-making'],
     ['Creation','Three-track (academic paper, course design, pedagogical essay)','Three-track (research report, financing plan, teaching reflection)','Output type adapted to accounting students analytical disposition']])

P("""The formal structure of NFSC - the four-dimension progressive logic - remains invariant during migration. The domain-specific content undergoes re-localization for the target discipline.""")

H('2.3 Five-Dimension Green Finance Diagnostic Framework', 3)
P("""The Framework dimension was operationalized through a five-dimension diagnostic framework that adapts standard financial analytical tools to green finance questions.""")
add_table('Table 2. Five-Dimension Green Finance Diagnostic Framework',
    ['Dimension','Core Question','Key Indicators','Analytical Tools','Case Illustration'],
    [['Financing Accessibility','Can a green project obtain adequate and reasonably priced capital?','Debt ratio < 70%; credit line/investment > 1.2; green vs. conventional loan spread','DuPont analysis, DCF','CATL 2021 green bond: AAA-rated, 3.28% coupon, ~50bp below conventional'],
     ['Carbon Asset Valuation','Are emission allowances and related green assets priced correctly?','Allowance price/marginal abatement cost ratio; carbon assets/total assets','DCF valuation, Real options approach','China national CEA: 55-65 CNY/ton range during 2023; intra-year volatility ~18%'],
     ['Policy Incentive Transmission','Do policy preferences effectively reach project financials?','Tax relief/revenue; interest subsidy/financial expense; actual vs. eligible benefits','Sensitivity analysis, Scenario simulation','Green loan interest subsidies estimated at RMB 120 billion cumulative (2018-2023) [2]'],
     ['Environmental Disclosure','Does environmental data transparency affect financing costs?','ESG rating tier; disclosure completeness index; third-party audit coverage','Regression analysis, Event study','Each one-notch ESG upgrade ~30bp reduction in corporate financing cost [7]'],
     ['Maturity-Liquidity Matching','Does the long-term nature of green projects align with financial instruments?','Current ratio > 1.5; payback period/loan term; long-term/short-term debt split','Cash flow matching, Duration analysis','Typical solar farm: 8-12 yr payback vs. 5-10 yr green loan max tenor - 2-3 yr gap']])

P("""The five dimensions interact: financing accessibility depends jointly on carbon asset valuation and policy incentive transmission; environmental disclosure quality affects both accessibility and valuation.""")

H('2.4 Course Context', 3)
P("""Finance is a core foundation course for accounting majors at Chengdu Ginkgo Hotel Management College (48 contact hours, Huang & Zhang [3] textbook). The study cohort - 2023 cohort Class 6 (n = 48) - had completed Fundamental Accounting and Microeconomics. A diagnostic survey at course onset confirmed that student familiarity with green finance was limited to name recognition.""")

P("""The green finance module occupied weeks 10 through 13 (12 contact hours, 25% of total). Allocation: Narrative 2h, Framework 4h, Scenario 4h, Creation 2h. Module objectives required students to: (1) analyze a green enterprise financing proposal using three or more diagnostic dimensions; (2) make framework-supported decisions in a simulated green credit approval scenario; and (3) independently produce a green financing plan or research report.""")

# 3
H('3 Implementation and Results')
H('3.1 Module Delivery', 3)
P("""Narrative (Week 10). Three narrative texts were distributed via course WeChat group before class: (a) a Shandong biomass power plant that faced early loan recall when carbon allowance prices dropped below operational breakeven, shrinking annual carbon revenue by approximately RMB 4 million (adapted from a 36Kr industry report); (b) CATL's RMB 5 billion green medium-term note offering circular (abridged); (c) a Jiangsu wastewater treatment plant that lost about RMB 3 million in carbon trading revenue due to undervalued emission allowances. Each text carried three guided questions. The first 20 minutes of class were devoted to extracting the academic problem - how does carbon revenue volatility affect financing accessibility? - from the visceral narrative of a clean-energy plant facing default.""")

P("""Framework (Weeks 11-12). The instructor introduced the five-dimension framework. The initial exercise required students to analyze a photovoltaic equipment manufacturer seeking RMB 50 million in green technology upgrade financing. Baseline accuracy - defined as correctly applying three or more of five dimensions - was 55% (24 of 44 students attempting). After two additional guided practice sessions with three more cases, the end-of-week-12 re-test showed 91% accuracy (38 of 42 students).""")

P("""Scenario (Week 13). The class split into four role groups: corporate CFO team (9 students, arguing project feasibility), bank credit review team (9 students, using the five-dimension framework for risk assessment), third-party environmental auditor team (9 students, verifying carbon data), and observer team (remaining students, recording framework usage). Each team had 20 minutes for preparation, followed by a 30-minute open inquiry session. The instructor did not prescribe whether the loan should be approved or rejected - the outcome depended on argument quality.""")

P("""Creation (Weeks 14-16). Students chose from three output tracks, all requiring explicit application of three or more diagnostic dimensions: Track A (green bond/ESG fund research report), Track B (green financing plan for a real listed company), and Track C (teaching reflection).""")

H('3.2 Student Outputs', 3)
P("""Of 48 enrolled students, 42 completed all four stages. Framework usage accuracy showed measurable improvement: 55% baseline (Week 11, n = 44) to 91% post-practice (Week 12, n = 42).""")

add_fig('Fig2_PrePost_Comparison.png', 'Figure 2. Pre-Post Comparison: Framework Usage Accuracy (n = 42).')

P("""The three-track distribution appears in Figure 3: Track A 26.2% (11 students), Track B 61.9% (26 students), Track C 11.9% (5 students). The 61.9% share for Track B contrasts with the engineering prototype distribution (paper 40%, design 35%, pedagogical essay 25%) reported in [4], suggesting output track preferences correlate with discipline-specific cognitive styles.""")

P("""The carbon asset valuation dimension appeared most frequently in student outputs (92% of Track B reports), followed by policy incentive transmission (81%). Eight students (18%) spontaneously proposed dimensions beyond the prescribed five - international carbon tariff risk (4 students) and technology iteration risk (3 students). Huang et al. [4] identify such spontaneous framework extension as a Creation-dimension indicator.""")

add_fig('Fig3_Track_Distribution.png', 'Figure 3. Distribution of Three-Track Output Choices (n = 42).')

H('3.3 Student Feedback', 3)
P("""An anonymous post-module survey (36 responses, 75% response rate) yielded the results in Table 3.""")
add_table('Table 3. Student Perceived Learning Gains Across NFSC Dimensions (n = 36)',
    ['NFSC Dimension','Mean Rating (1-5)','Most Impactful Votes','Representative Student Comment'],
    [['Narrative','4.2','10 (27.8%)','The biomass plant story made carbon prices tangible - they can shut down a factory.'],
     ['Framework','3.9','6 (16.7%)','The framework provides structure but I needed more practice to internalize all five dimensions.'],
     ['Scenario','4.5','15 (41.7%)','When the CFO argued their case, I had to counter using specific framework dimensions. That pressure made the framework real.'],
     ['Creation','4.0','5 (13.9%)','Choosing my own company for the financing plan made me actually care about the analysis.']])

P("""Scenario received the highest impact rating (4.5/5.0, 41.7% naming it most impactful), consistent with [4]'s finding that students consistently rank scenario immersion as the most memorable component. Limitations include the 75% survey response rate, single-section single-semester design, and absence of a parallel control group.""")

# 4
H('4 Discussion: Migration Mechanism')
H('4.1 Four-Element Migration Model', 3)
P("""Based on the engineering-to-finance migration data, we propose that NFSC cross-disciplinary migration follows a four-element mechanism.""")
add_fig('Fig1_Migration_Mechanism.png', 'Figure 1. NFSC Four-Element Cross-Disciplinary Migration Mechanism.')

P("""Narrative replacement. Source material type shifts from engineering conflict narratives to the target discipline's narrative events. The replacement criterion: materials must contain authentic economic or social conflicts with emotional tension that can be abstracted into academic questions.""")

P("""Framework remapping. Diagnostic dimensions are reconstructed from the original discipline's framework to the target discipline's knowledge framework. The remapping criterion: each dimension must be operable, independently assessable, and verifiable within simulated scenarios.""")

P("""Scenario type conversion. Simulation type converts from engineering decision-making to the target discipline's prototypical professional decision scenario. The conversion criterion: the scenario must involve multi-party interest conflict and information incompleteness.""")

P("""Output adaptation. Output types adjust to match the target discipline's student learning styles and academic level. The adaptation criterion: outputs must demonstrate framework application while allowing student autonomy in form selection.""")

H('4.2 Dimension-Specific Adaptation', 3)
P("""Among the four NFSC dimensions, adaptation fit varies. Narrative shows the highest fit - financial history is rich with narrative material (2008 subprime crisis, 2020 negative rates, 2023 Silicon Valley Bank run). Framework shows high fit - standard financial tools can be remapped with minimal restructuring. Scenario shows medium-to-high fit - business education already uses case methods; NFSC adds structured role cards. Creation shows the highest fit - finance education is inherently oriented toward producing decision proposals.""")

H('4.3 Implications for Engineering Education', 3)
P("""The cross-disciplinary migration offers bidirectional value. Forward: the successful migration demonstrates NFSC core mechanisms do not depend on specific disciplinary content. Reverse: simulation practices from finance can feed back into engineering education - for example, embedding incinerator plant BOT project financing scenarios in environmental engineering courses to help students grasp financial consequences of technical decisions.""")

# 5
H('5 Conclusion')
P("""This study provides the first complete cross-disciplinary migration empirical evidence for the NFSC teaching method. (1) The migration from environmental engineering to an undergraduate finance course is viable. Student framework accuracy improved from 55% to 91% after practice. (2) The Green Output Chain concept provides a structured pathway for coupling NFSC with non-engineering disciplines. (3) Cross-disciplinary migration follows a four-element mechanism: narrative replacement, framework remapping, scenario type conversion, and output adaptation. Future work should pursue multi-iteration longitudinal tracking and randomized controlled comparisons.""")

# DECLARATIONS
P(''); P('Author Contributions (CRediT)', bold=True, size=10, indent=False)
P('Jingwei Zhang: Conceptualization, Methodology, Teaching Implementation, Data Collection, Writing - Original Draft. Zeyu Xie: NFSC Methodology Consultation, Writing - Review and Editing, Supervision.', size=9, indent=False)
P('Declaration of Interest', bold=True, size=10, indent=False)
P('The authors declare no competing interests.', size=9, indent=False)
P('Data Availability', bold=True, size=10, indent=False)
P('The student feedback data are available from the corresponding author upon reasonable request.', size=9, indent=False)
P('Ethics Statement', bold=True, size=10, indent=False)
P('This study was conducted in accordance with institutional teaching research ethics guidelines.', size=9, indent=False)

# REFERENCES
P(''); H('References')
refs = [
    '[1] Shanghai Environment and Energy Exchange. (2024). National carbon emission trading market 2023 annual report. Shanghai: SEEE.',
    "[2] People's Bank of China. (2024). 2023 financial institution loan orientation statistics report. Beijing: PBC.",
    '[3] Huang, D., & Zhang, J. (2020). Finance (5th ed.). Beijing: China Renmin University Press.',
    '[4] Huang, Z., Xie, Z., & Sun, Q. (2025). The NFSC four-dimensional teaching method in graduate engineering courses. Journal of Chengdu University (Natural Science Edition). [Manuscript submitted]',
    '[5] Huang, Z. (2026). Universal education consulting: Documentary network novel series [M/OL]. QQ Reading / 17K Literature.',
    '[6] Anderson, L. W., & Krathwohl, D. R. (Eds.). (2001). A taxonomy for learning, teaching, and assessing. New York: Longman.',
    '[7] S&P Global. (2023). Sustainability yearbook 2023. New York: S&P Global.',
    '[8] Crawley, E. F., et al. (2014). Rethinking engineering education: The CDIO approach (2nd ed.). Cham: Springer.',
    '[9] Spady, W. G. (1994). Outcome-based education: Critical issues and answers. Arlington, VA: AASA.',
    '[10] Bruner, J. (1986). Actual minds, possible worlds. Cambridge, MA: Harvard University Press.',
    '[11] Lave, J., & Wenger, E. (1991). Situated learning: Legitimate peripheral participation. Cambridge: Cambridge University Press.',
    '[12] Kolb, D. A. (2015). Experiential learning (2nd ed.). Upper Saddle River, NJ: Pearson.',
    '[13] Perkins, D. N. (1991). Technology meets constructivism. Educational Technology, 31(5), 18-23.',
    '[14] IPCC. (2022). Climate change 2022: Mitigation of climate change. Cambridge: Cambridge University Press.',
    '[15] IFC. (2017). Green finance: A bottom-up approach to track existing flows. Washington, DC: IFC.',
    '[16] World Bank. (2022). State and trends of carbon pricing 2022. Washington, DC: World Bank.',
    '[17] Li, Z. (2015). Outcome-based instructional design. China University Teaching, (3), 32-39.',
    '[18] CEEAA. (2024). Engineering education accreditation standards (2024 edition). Beijing: CEEAA.',
]
for ref in refs:
    P(ref, size=9, indent=False)

out = 'NFSC_GreenFinance_Final_v3.docx'
doc.save(out)
print('Done: ' + str(os.path.getsize(out)) + ' bytes (' + str(round(os.path.getsize(out)/1024)) + ' KB)')
