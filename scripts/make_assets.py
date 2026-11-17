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


