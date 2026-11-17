from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas


assets = Path(__file__).resolve().parents[1] / "dist" / "assets"
assets.mkdir(parents=True, exist_ok=True)

mat = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" preserveAspectRatio="none">',
    '<g fill="none" stroke="#c5f7df">',
    '<path d="M36 38H1228V636H36Z" stroke-width="1.6"/>',
    '<path d="M36 636l600-598" stroke-dasharray="4 4" opacity=".38"/>',
]
for i in range(107):
    x = i * 12
    length = 14 if i % 5 == 0 else 7
    mat.append(f'<path d="M{x} 0v{length}m0 {718 - length}v-{length}" opacity=".43"/>')
for i in range(60):
    y = i * 12
    length = 13 if i % 5 == 0 else 7
    mat.append(f'<path d="M0 {y}h{length}m{1279 - length} 0h-{length}" opacity=".43"/>')
for row in range(10):
    for col in range(20):
        x, y = 36 + 59.6 * col, 98 + 59.6 * row
        mat.append(f'<path d="M{x-2.7:.1f} {y:.1f}h5.4m-2.7 -2.7v5.4" opacity=".53"/>')
mat.append('</g><g fill="#c9f8df" font-family="monospace" font-size="12" font-weight="bold">')
mat.append('<text x="8" y="27">inch</text>')
for i in range(1, 21):
    x = 36 + 59.6 * i
    mat.append(f'<text x="{x - 4:.1f}" y="31">{i}</text><text x="{x - 4:.1f}" y="663">{i}</text>')
for i in range(1, 11):
    y = 45 + 59.6 * i
    mat.append(f'<text x="{18 if i < 10 else 12}" y="{y:.1f}">{i}</text><text x="1237" y="{y:.1f}">{21 - i}</text>')
mat.append('</g></svg>')
(assets / "mat.svg").write_text("".join(mat), encoding="utf-8")

pdf = Canvas(str(assets / "Armaan_Khan_Resume.pdf"), pagesize=letter)
pdf.setTitle("Armaan Khan - Resume")
pdf.setAuthor("Armaan Khan")
pdf.setSubject("Developer portfolio and selected projects")
pdf.setFillColor("#1b2027")
pdf.setFont("Times-Bold", 24)
pdf.drawCentredString(306, 738, "Armaan Khan")
contacts = [
    ("Chandigarh, India", None),
    ("armaankhanmub@gmail.com", "mailto:armaankhanmub@gmail.com"),
    ("LinkedIn", "https://www.linkedin.com/in/armaanthisside/"),
    ("GitHub", "https://github.com/armaankhan2905"),
]
font, size = "Times-Roman", 10.5
contact_text = "  |  ".join(label for label, _ in contacts)
x = (612 - stringWidth(contact_text, font, size)) / 2
pdf.setFont(font, size)
for i, (label, url) in enumerate(contacts):
    width = stringWidth(label, font, size)
    pdf.drawString(x, 719, label)
    if url:
        pdf.linkURL(url, (x, 717, x + width, 730), relative=0)
    x += width
    if i < len(contacts) - 1:
        pdf.drawString(x, 719, "  |  ")
        x += stringWidth("  |  ", font, size)

y = 692


def paragraph(value, font="Times-Roman", size=11.5, indent=0):
    global y
    pdf.setFont(font, size)
    words = value.split()
    line = ""
    for word in words:
        new = f"{line} {word}".strip()
        if line and stringWidth(new, font, size) > 518 - indent:
            pdf.drawString(47 + indent, y, line)
            y -= 15
            line = word
        else:
            line = new
    if line:
        pdf.drawString(47 + indent, y, line)
        y -= 15


def section(title):
    global y
    pdf.setFont("Times-Bold", 14)
    pdf.drawString(47, y, title.upper())
    pdf.setStrokeColor("#555a62")
    pdf.setLineWidth(.45)
    pdf.line(47, y - 5, 565, y - 5)
    y -= 22


section("Summary")
paragraph("Computer Science Engineering student specializing in Artificial Intelligence and Machine Learning. I build web and computer vision projects and study data structures, backend development, and cloud technology.")
y -= 12
section("Education")
paragraph("B.Tech, Computer Science Engineering (Artificial Intelligence and Machine Learning)", "Times-Bold")
paragraph("Undergraduate coursework in progress.")
y -= 12
section("Technical Skills")
paragraph("Languages: Java, Python, JavaScript, TypeScript")
paragraph("Web: HTML, CSS, React, Git, GitHub")
paragraph("Focus areas: Data structures and algorithms, computer vision, and multi-agent AI")
y -= 12
section("Selected Projects")
for name, detail, url in [
    ("ClaimSaathi", "Led a hackathon team building a clickable insurance companion demo. It shows how to explain policy terms, compare plans, review rejected claims, and draft complaints using sample cases.", "ClaimSaathi"),
    ("AgentSwarm", "Developed a multi-agent research platform that separates web research, academic paper analysis, fact-checking, and report preparation.", "AgentSwarm"),
    ("AirSync", "Built a Windows app for touchless PowerPoint and Word control with gestures, air writing, slide annotation, and facial authentication.", "AirSync"),
    ("CTRL-ALT-TRUST", "Explored zero-trust security in a simulated SCADA water pipeline using TypeScript.", "CTRL-ALT-TRUST"),
]:
    pdf.linkURL(f"https://github.com/armaankhan2905/{url}", (47, y-3, 47+stringWidth(name, "Times-Bold", 11.5), y+10), relative=0)
    paragraph(name, "Times-Bold")
    paragraph(detail, indent=9)
    y -= 7
y -= 5
section("Coding Profiles")
paragraph("GitHub, LeetCode, and GeeksforGeeks: armaankhan2905")
assert y > 36, f"Content extends past the bottom margin: {y}"
pdf.save()
