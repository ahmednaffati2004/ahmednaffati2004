"""Builds assets/toolkit.svg: gold-on-black grouped tech chips."""
import os

GROUPS = [
    ("FRONTEND", ["TypeScript", "React", "Next.js", "Vite", "Tailwind CSS", "Framer Motion"]),
    ("BACKEND", ["Node.js", "NestJS", "Laravel", "PHP", "REST APIs", "Prisma"]),
    ("DATA", ["PostgreSQL", "SQLite", "MySQL"]),
    ("MOBILE", ["Flutter", "Dart", "iOS · Swift"]),
    ("CRAFT", ["Figma", "Git", "Docker", "Playwright"]),
]

rows, y, k = "", 40, 0
for label, items in GROUPS:
    rows += f'<text x="40" y="{y+25}" class="g">{label}</text>'
    x = 190
    for it in items:
        w = 26 + len(it) * 9.2
        d = 0.15 + k * 0.05
        rows += (f'<g class="in" style="animation-delay:{d:.2f}s">'
                 f'<rect x="{x}" y="{y}" width="{w:.0f}" height="38" rx="19" fill="#12151c" stroke="#c9a227" stroke-opacity=".35"/>'
                 f'<circle cx="{x+16}" cy="{y+19}" r="3" fill="#c9a227" class="dot" style="animation-delay:{k*0.17:.2f}s"/>'
                 f'<text x="{x+28}" y="{y+24}" class="t">{it}</text></g>')
        x += w + 12
        k += 1
    y += 56

H = y + 20
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{H}" viewBox="0 0 1200 {H}">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a0c11"/><stop offset="1" stop-color="#17130a"/></linearGradient>
<style>
.g{{font:600 13px 'SF Mono',Menlo,Consolas,monospace;letter-spacing:3px;fill:#c9a227}}
.t{{font:500 15px 'Segoe UI',Inter,Helvetica,Arial,sans-serif;fill:#ece4cc}}
.in{{opacity:0;animation:in .7s cubic-bezier(.2,.8,.2,1) forwards}}
@keyframes in{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
.dot{{animation:p 2.4s ease-in-out infinite}}@keyframes p{{0%,100%{{opacity:.3}}50%{{opacity:1}}}}
</style></defs>
<rect x="1" y="1" width="1198" height="{H-2}" rx="18" fill="url(#bg)" stroke="#c9a227" stroke-opacity=".25"/>
{rows}
</svg>'''
os.makedirs("assets", exist_ok=True)
open("assets/toolkit.svg", "w").write(svg)
