"""Build the portfolio resume from the supplied Word document and verified projects."""
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from xml.sax.saxutils import escape
import re

root = Path(__file__).resolve().parents[1]
out = root / "output"
out.mkdir(exist_ok=True)
fonts = Path("C:/Windows/Fonts")
for name, file in [("Resume", "arial.ttf"), ("ResumeBold", "arialbd.ttf")]:
    pdfmetrics.registerFont(TTFont(name, str(fonts / file)))

# One letter-size page. Projects follow the portfolio order; older or minor work is omitted.
pages = [
[
("title", "ARMAAN KHAN"),
("subtitle", "Backend and AI/ML Developer | B.Tech CSE (AI & ML)"),
("contact", "armaankhanmub@gmail.com | +91 98550 73331 | Punjab, India"),
("links", 'github.com/armaankhan2905 | linkedin.com/in/armaanthisside | leetcode.com/u/armaankhan2905'),
("section", "Education"),
("heading", "Chitkara University, Punjab | B.Tech CSE (AI & ML) | Expected 2029 | CGPA: 9.38"),
("section", "Technical Skills"),
("skill", "Languages: Python, Java, JavaScript, TypeScript, C, SQL, HTML, CSS"),
("skill", "Backend and databases: FastAPI, Node.js, Express, REST APIs, Supabase, SQLite, MySQL"),
("skill", "AI/ML: PyTorch, LLM APIs, NumPy, Pandas, MediaPipe | Frontend: React, Vite"),
("skill", "Tools: Git, GitHub, Vercel, Linux, Jupyter, Postman"),
("section", "Projects"),
("heading", "PhishShield | Graviton 2026 | Explainable phishing and scam detection"),
("bullet", "Built the detection rules, domain and brand checks, sender checks and evidence-gated scoring for a tool that checks SMS, emails and URLs, with a web app and a Gmail Chrome extension."),
("bullet", "Each verdict shows a risk score and the phrases and links behind it, combining calibrated text and URL models with technical evidence."),
("tech", "Python, TF-IDF, logistic regression, gradient-boosted trees | phishshield-1jrz.onrender.com"),
("heading", "ClaimSaathi | The Builder's Theory 1.0 | Team Leader"),
("bullet", "Led a team building an insurance companion demo covering policy explanations, plan comparisons, rejected-claim evidence and complaint drafting, in English, Hindi and Hinglish."),
("tech", "HTML, CSS, JavaScript | github.com/armaankhan2905/ClaimSaathi"),
("heading", "WeatherGuard AI (SkyVengers) | Smart India Hackathon 2026, SIH26077"),
("bullet", "Built a severe-weather nowcasting prototype for 2-6 hour warnings of thunderstorms, cloudbursts and flash floods, using a multi-task PyTorch ConvLSTM."),
("bullet", "Added terrain-aware risk maps, explainable predictions and escalating alerts with acknowledgement tracking."),
("tech", "React, TypeScript, FastAPI, PyTorch, Leaflet | github.com/armaankhan2905/SkyVengers"),
("heading", "AgentGuard | AI firewall for autonomous agents"),
("bullet", "Routes every agent tool call through a default-deny firewall with audited policies, and scans tool output for prompt injection before it reaches the model."),
("tech", "Python, FastAPI, SQLite, React | github.com/armaankhan2905/AgentGuard"),
("heading", "PrivacyLens | PECathon 2026, Top 40 Teams | Local PII redaction for AI agents"),
("bullet", "Built the regex and Luhn detection layer, the sanitization pipeline and the demo server, running the team's BERT NER model alongside the patterns."),
("tech", "Python, PyTorch, Transformers | privacylens-demo.onrender.com | github.com/PECathon-2026/PF-NH5DR2"),
("heading", "TRUSTGRID | NexHack 2.0"),
("bullet", "Built a Zero Trust security simulation of a SCADA water pipeline with role-based command checks, attack scenarios, risk scoring, audit logs and REST APIs."),
("tech", "JavaScript, SQLite, REST APIs | github.com/armaankhan2905/CTRL-ALT-TRUST"),
("heading", "AirSync | Touchless desktop control"),
("bullet", "Windows app for controlling PowerPoint and Word with hand gestures and air writing, with face authentication and role-based access."),
("tech", "Python, computer vision | github.com/armaankhan2905/AirSync"),
("section", "Certifications and Achievements"),
("bullet", "Microsoft Certified: Azure AI Fundamentals (AI-900) and Azure Data Fundamentals (DP-900)."),
("bullet", "Hackathons: Smart India Hackathon 2026, Graviton 2026, Hack Helix (Thapar), NexHack 2.0, PECathon 2026, The Builder's Theory 1.0."),
("bullet", "Solved 100+ LeetCode problems in arrays, strings, binary search and sliding window."),
],
]

styles = {
 "title": ParagraphStyle("title",fontName="ResumeBold",fontSize=20,leading=23,alignment=1,spaceAfter=2),
 "subtitle": ParagraphStyle("subtitle",fontName="ResumeBold",fontSize=10,leading=13,alignment=1,spaceAfter=2),
 "contact": ParagraphStyle("contact",fontName="Resume",fontSize=9,leading=12,alignment=1,spaceAfter=1),
 "links": ParagraphStyle("links",fontName="Resume",fontSize=8.5,leading=12,alignment=1,spaceAfter=2),
 "section": ParagraphStyle("section",fontName="ResumeBold",fontSize=11,leading=14,spaceBefore=8,spaceAfter=3,keepWithNext=True),
 "heading": ParagraphStyle("heading",fontName="ResumeBold",fontSize=9.5,leading=12.5,spaceBefore=5,spaceAfter=1,keepWithNext=True),
 "body": ParagraphStyle("body",fontName="Resume",fontSize=9.25,leading=12.25,spaceAfter=2),
 "skill": ParagraphStyle("skill",fontName="Resume",fontSize=9.25,leading=12.25,spaceAfter=1.5),
 "bullet": ParagraphStyle("bullet",fontName="Resume",fontSize=9.25,leading=12.25,spaceAfter=1.5,leftIndent=9,firstLineIndent=-9),
 "tech": ParagraphStyle("tech",fontName="Resume",fontSize=8.5,leading=11,spaceAfter=1,textColor=colors.HexColor("#374151")),
}

def rich(text):
    text = escape(text)
    text = re.sub(r'(github\.com/[^ |]+|linkedin\.com/in/[^ |]+|leetcode\.com/u/[^ |]+|[\w-]+\.onrender\.com)', r'<link href="https://\1" color="#17202c">\1</link>',text)
    text = text.replace("armaankhanmub@gmail.com", '<link href="mailto:armaankhanmub@gmail.com">armaankhanmub@gmail.com</link>')
    return text

flow = []
for i, page in enumerate(pages):
    if i: flow.append(PageBreak())
    for kind,text in page:
        html = rich(text)
        if kind == "skill":
            html = re.sub(r"(^|\| )([^:|]+:)", r'\1<font name="ResumeBold">\2</font>', html)
        flow.append(Paragraph(("- " if kind == "bullet" else "") + html, styles[kind]))

pdf = root / "dist/assets/Armaan_Khan_Resume.pdf"
SimpleDocTemplate(str(pdf),pagesize=letter,rightMargin=38,leftMargin=38,topMargin=27,bottomMargin=28,
                  title="Armaan Khan Resume",author="Armaan Khan").build(flow)

# Editable source kept alongside the final PDF; Word pagination requires local review.
doc = Document()
sec=doc.sections[0]
sec.page_width=Inches(8.5);sec.page_height=Inches(11)
sec.top_margin=Inches(27/72);sec.bottom_margin=Inches(28/72)
sec.left_margin=sec.right_margin=Inches(38/72)
for i,page in enumerate(pages):
    if i:doc.add_page_break()
    for kind,text in page:
        p=doc.add_paragraph(("- " if kind=="bullet" else "")+text)
        if kind=="title":p.style=doc.styles["Title"]
        s=styles[kind]
        pf=p.paragraph_format
        pf.space_before=Pt(s.spaceBefore);pf.space_after=Pt(s.spaceAfter)
        pf.line_spacing=Pt(s.leading);pf.keep_with_next=kind in ("section","heading")
        if kind in ("title","subtitle","contact","links"):p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name="Arial";r.font.size=Pt(s.fontSize);r.font.color.rgb=RGBColor(0,0,0)
            r.bold=kind in ("title","subtitle","section","heading")
doc.save(out / "Armaan_Khan_Resume_Updated.docx")
print(pdf)
