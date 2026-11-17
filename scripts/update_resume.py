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

root = Path(__file__).resolve().parents[1]
out = root / "output"
out.mkdir(exist_ok=True)
fonts = Path("C:/Windows/Fonts")
for name, file in [("Resume", "arial.ttf"), ("ResumeBold", "arialbd.ttf")]:
    pdfmetrics.registerFont(TTFont(name, str(fonts / file)))

pages = [
[
("title", "ARMAAN KHAN"),
("subtitle", "Backend and AI/ML Developer | B.Tech CSE (AI & ML)"),
("contact", "armaankhanmub@gmail.com | +91 98550 73331 | Punjab, India"),
("links", 'github.com/armaankhan2905 | linkedin.com/in/armaanthisside | leetcode.com/u/armaankhan2905'),
("section", "Profile"),
("body", "Second-year B.Tech CSE (AI/ML) student at Chitkara University with a 9.38 CGPA. Builds backend-first, full-stack and AI-integrated applications using Python, Java, React, FastAPI and SQL. Project experience spans research agents, computer vision, policy tools and industrial security simulations. Microsoft certified in Azure AI and Data Fundamentals."),
("section", "Education"),
("heading", "Chitkara University, Punjab | B.Tech CSE (AI & ML)"),
("body", "Expected graduation: 2029 | CGPA: 9.38"),
("body", "Coursework: Data Structures & Algorithms, Database Management Systems, Artificial Intelligence, Web Development and Java Programming."),
("section", "Technical Skills"),
("body", "Languages: Python, Java, JavaScript, TypeScript, C, SQL, HTML and CSS"),
("body", "Backend and databases: FastAPI, Node.js, Express, REST APIs, authentication, Supabase, SQLite and MySQL"),
("body", "Frontend: React, Vite and responsive web design"),
("body", "AI and vision: PyTorch, AI/LLM APIs, model inference, NumPy, Pandas, MediaPipe Face Mesh and data pipelines"),
("body", "Tools: Git, GitHub, Vercel, VS Code, Linux, Jupyter and Postman"),
("section", "Certifications"),
("body", "Microsoft Certified: Azure AI Fundamentals (AI-900)"),
("body", "Microsoft Certified: Azure Data Fundamentals (DP-900)"),
("section", "Recent Projects"),
("heading", "ClaimSaathi | The Builder's Theory 1.0 | Team Leader"),
("bullet", "Led OverCooked Brains in building an insurance companion demo covering policy explanations, comparisons, rejected-claim evidence and complaint drafting."),
("bullet", "Created a multilingual walkthrough in English, Hindi and Hinglish. The prototype uses fictional cases and predefined AI results."),
("tech", "HTML, CSS, JavaScript | github.com/armaankhan2905/ClaimSaathi"),
("heading", "AgentSwarm | Multi-agent Research Platform"),
("bullet", "Built a platform that coordinates specialized agents for web research, academic paper analysis, fact-checking and report generation."),
("tech", "Python, multi-agent AI | github.com/armaankhan2905/AgentSwarm"),
("heading", "AirSync | Touchless Desktop Control"),
("bullet", "Built a Windows app for touchless PowerPoint and Word control using hand gestures, air writing, slide annotations, facial authentication and role-based access."),
("tech", "Python, computer vision, Windows | github.com/armaankhan2905/AirSync"),
],
[
("section", "Engineering and Hackathon Projects"),
("heading", "Weather Intelligence & Anomaly Detection | SIH 2026"),
("bullet", "Built a mobile and web weather intelligence platform for Smart India Hackathon 2026, problem statement SIH26077, to detect unusual weather patterns and alert users."),
("bullet", "Developed backend workflows for real-time data processing, feature engineering, model inference, risk assessment, database persistence and notifications."),
("bullet", "Delivered location- and terrain-aware risk prediction, interactive weather maps and explainable AI insights."),
("tech", "AI/ML backend, APIs, databases, maps and notifications"),
("heading", "CogniFlow | Hack Helix, Thapar University"),
("bullet", "Prototyped a fatigue-aware UI concept using activity patterns and facial signals."),
("bullet", "Applied MediaPipe Face Mesh in a facial-landmark monitoring pipeline and designed a family-notification concept for concerning patterns."),
("tech", "React, FastAPI, MediaPipe Face Mesh, Supabase Auth"),
("heading", "TRUSTGRID | NexHack 2.0"),
("bullet", "Built a SCADA water-pipeline security simulation to demonstrate Zero Trust principles and identity- and role-based command verification."),
("bullet", "Simulated unknown devices, brute-force attempts, abnormal traffic, insider threats and unauthorized commands with alerts, audit logs and device-isolation concepts."),
("bullet", "Integrated live data with risk scoring, persisted events in SQLite and exposed risk outputs and alert lifecycle management through REST APIs."),
("tech", "HTML, CSS, JavaScript, SQLite, REST APIs"),
("heading", "Sustainify | Full-stack Web Project"),
("bullet", "Developed a multi-page platform covering all 17 UN Sustainable Development Goals, with a global impact dashboard, live statistics and engagement analytics."),
("bullet", "Built an interactive carbon-footprint calculator for SDG 13 and deployed the site on Vercel."),
("tech", "React, JavaScript, Vercel"),
("heading", "QuizVerse | Team Project"),
("bullet", "Contributed to a responsive quiz platform with category navigation, search, authentication and difficulty-based timers; collaborated through Git and GitHub."),
("tech", "Web frontend, authentication, Git/GitHub"),
("section", "Hackathons and Problem Solving"),
("body", "Smart India Hackathon 2026; Hack Helix at Thapar University; NexHack 2.0; The Builder's Theory 1.0."),
("body", "Solved 100+ LeetCode problems across arrays, strings, matrices, binary search and sliding window."),
("body", "Current focus: backend engineering, AI/ML applications, databases, system integration, and Java data structures and algorithms."),
]]

styles = {
 "title": ParagraphStyle("title",fontName="ResumeBold",fontSize=21,leading=25,alignment=1,spaceAfter=4),
 "subtitle": ParagraphStyle("subtitle",fontName="ResumeBold",fontSize=10,leading=13,alignment=1,spaceAfter=4),
 "contact": ParagraphStyle("contact",fontName="Resume",fontSize=9,leading=12,alignment=1,spaceAfter=3),
 "links": ParagraphStyle("links",fontName="Resume",fontSize=8.5,leading=12,alignment=1,spaceAfter=4),
 "section": ParagraphStyle("section",fontName="ResumeBold",fontSize=11.5,leading=15,spaceBefore=11,spaceAfter=5,keepWithNext=True),
 "heading": ParagraphStyle("heading",fontName="ResumeBold",fontSize=10,leading=13,spaceBefore=7,spaceAfter=3,keepWithNext=True),
 "body": ParagraphStyle("body",fontName="Resume",fontSize=9.5,leading=13,spaceAfter=3),
 "bullet": ParagraphStyle("bullet",fontName="Resume",fontSize=9.5,leading=13,spaceAfter=3,leftIndent=9,firstLineIndent=-9),
 "tech": ParagraphStyle("tech",fontName="Resume",fontSize=8.5,leading=11.5,spaceAfter=3,textColor=colors.HexColor("#374151")),
}

def rich(text):
    import re
    text = escape(text)
    text = re.sub(r'(github\.com/[^ |]+|linkedin\.com/in/[^ |]+|leetcode\.com/u/[^ |]+)', r'<link href="https://\1" color="#17202c">\1</link>',text)
    text = text.replace("armaankhanmub@gmail.com", '<link href="mailto:armaankhanmub@gmail.com">armaankhanmub@gmail.com</link>')
    return text

flow = []
for i, page in enumerate(pages):
    if i: flow.append(PageBreak())
    for kind,text in page:
        flow.append(Paragraph(("- " if kind == "bullet" else "") + rich(text), styles[kind]))

pdf = root / "dist/assets/Armaan_Khan_Resume.pdf"
SimpleDocTemplate(str(pdf),pagesize=letter,rightMargin=38,leftMargin=38,topMargin=27,bottomMargin=28,
                  title="Armaan Khan Resume",author="Armaan Khan").build(flow)

# Editable source kept alongside the final PDF; Word pagination requires local review.
doc = Document()
sec=doc.sections[0]
sec.page_width=Inches(8.5);sec.page_height=Inches(11)
sec.top_margin=Inches(.375);sec.bottom_margin=Inches(.39)
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
