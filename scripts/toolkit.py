"""Builds assets/toolkit.svg: brand logos on glass tiles, grouped by discipline.

Logo paths are vendored in scripts/icons.json (from simple-icons, CC0).
"""
import json, os

ICONS = json.load(open(os.path.join(os.path.dirname(__file__), "icons.json")))

GROUPS = [
    ("FRONTEND", [("typescript", "TypeScript"), ("react", "React"), ("nextdotjs", "Next.js"), ("vite", "Vite"), ("tailwindcss", "Tailwind"), ("framer", "Motion")]),
    ("BACKEND", [("nodedotjs", "Node.js"), ("nestjs", "NestJS"), ("laravel", "Laravel"), ("php", "PHP"), ("prisma", "Prisma")]),
    ("DATA", [("postgresql", "PostgreSQL"), ("sqlite", "SQLite"), ("mysql", "MySQL")]),
    ("MOBILE", [("flutter", "Flutter"), ("dart", "Dart"), ("swift", "Swift")]),
    ("CRAFT", [("figma", "Figma"), ("git", "Git"), ("docker", "Docker")]),
]
# Brands whose official colour vanishes on a dark tile.
LIGHT = {"nextdotjs": "#ffffff", "prisma": "#ffffff", "framer": "#ffffff", "sqlite": "#44a8e0", "mysql": "#5d9ad6", "flutter": "#47c5fb", "postgresql": "#6b9bd8"}

TILE, GAP, LEFT = 96, 14, 190
cols = max(len(g[1]) for g in GROUPS)
W = 1200
rows, y, k = "", 40, 0
for label, items in GROUPS:
    rows += f'<text x="40" y="{y+52}" class="g">{label}</text><rect x="40" y="{y+62}" width="22" height="2" fill="url(#acc)"/>'
    x = LEFT
    for slug, name in items:
        ic = ICONS[slug]
        col = LIGHT.get(slug, "#" + ic["hex"])
        d = 0.1 + k * 0.06
        rows += f'''<g class="in" style="animation-delay:{d:.2f}s">
<rect x="{x}" y="{y}" width="{TILE}" height="{TILE}" rx="20" fill="url(#tile)" stroke="url(#edge)"/>
<circle cx="{x+TILE/2}" cy="{y+40}" r="26" fill="{col}" opacity=".13" class="halo" style="animation-delay:{k*0.21:.2f}s"/>
<svg x="{x+TILE/2-17}" y="{y+23}" width="34" height="34" viewBox="0 0 24 24"><path fill="{col}" d="{ic['path']}"/></svg>
<text x="{x+TILE/2}" y="{y+82}" class="t" text-anchor="middle">{name}</text></g>'''
        x += TILE + GAP
        k += 1
    y += TILE + 22

H = y + 18
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#07080d"/><stop offset="1" stop-color="#0e0c1c"/></linearGradient>
<linearGradient id="tile" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#161827"/><stop offset="1" stop-color="#0d0e17"/></linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".18"/><stop offset="1" stop-color="#8b7cff" stop-opacity=".08"/></linearGradient>
<linearGradient id="acc" x1="0" x2="1"><stop offset="0" stop-color="#8b7cff"/><stop offset="1" stop-color="#5ee1ff"/></linearGradient>
<style>
.g{{font:600 13px 'SF Mono',Menlo,Consolas,monospace;letter-spacing:3px;fill:#c4c8dc}}
.t{{font:500 12.5px 'Segoe UI',Inter,Helvetica,Arial,sans-serif;fill:#a9adbf}}
.in{{opacity:0;animation:in .7s cubic-bezier(.2,.8,.2,1) forwards}}
@keyframes in{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
.halo{{transform-box:fill-box;transform-origin:center;animation:h 3.2s ease-in-out infinite}}
@keyframes h{{0%,100%{{opacity:.06;transform:scale(.85)}}50%{{opacity:.2;transform:scale(1.1)}}}}
</style></defs>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="url(#bg)" stroke="#ffffff" stroke-opacity=".08"/>
{rows}
</svg>'''
os.makedirs("assets", exist_ok=True)
open("assets/toolkit.svg", "w").write(svg)
