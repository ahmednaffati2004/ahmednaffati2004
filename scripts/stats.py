"""Builds assets/stats.svg from the GitHub API. Runs daily in GitHub Actions.

Numbers roll in like an odometer; each metric has an animated progress ring.
"""
import json, os, re, urllib.request
from collections import Counter
from datetime import datetime, timezone

USER = os.environ.get("GH_USER", "ahmednaffati2004")
TOKEN = os.environ.get("GITHUB_TOKEN")


def fetch(url, data=None, raw=False):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": "profile-stats"})
    if not raw:
        req.add_header("Accept", "application/vnd.github+json")
        if TOKEN:
            req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req) as r:
        body = r.read().decode()
    return body if raw else json.loads(body)


user = fetch(f"https://api.github.com/users/{USER}")
repos = fetch(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner")
stars = sum(r["stargazers_count"] for r in repos)
langs = Counter()
for r in repos:
    if r["language"] and not r["fork"]:
        langs[r["language"]] += max(r["size"], 1)
top = langs.most_common(5)
total = sum(v for _, v in top) or 1
years = max(datetime.now(timezone.utc).year - int(user["created_at"][:4]), 1)

contrib = 0
try:
    page = fetch(f"https://github.com/users/{USER}/contributions", raw=True)
    m = re.search(r"([\d,]+)\s+contributions?\s+in the last year", page)
    contrib = int(m.group(1).replace(",", "")) if m else 0
except Exception:
    pass

ACC = ["#eef0ff", "#a99bff", "#8b7cff", "#5ee1ff", "#4a4290"]
# (label, value, ring target used to scale the ring, ring colour)
metrics = [
    ("REPOSITORIES", len(repos), 50, "#a99bff"),
    ("STARS EARNED", stars, 25, "#5ee1ff"),
    ("CONTRIBUTIONS · 1Y", contrib, 365, "#8b7cff"),
    ("YEARS BUILDING", years, 10, "#eef0ff"),
]

DIGIT_H = 52


def odometer(value, x, y, delay):
    """Each digit is a 0-9 strip that rolls up to its final position."""
    out, s = "", str(value)
    for i, ch in enumerate(s):
        d = int(ch)
        col = "".join(f'<text x="0" y="{(n+1)*DIGIT_H - 10}" class="v">{n}</text>' for n in list(range(10)) + list(range(10)))
        stop = -(10 + d) * DIGIT_H
        out += (f'<svg x="{x + i*30}" y="{y}" width="30" height="{DIGIT_H}" overflow="hidden">'
                f'<g class="roll" style="--to:{stop}px;animation-delay:{delay + i*0.12:.2f}s">{col}</g></svg>')
    return out


cells = ""
for i, (label, val, target, col) in enumerate(metrics):
    x = 40 + i * 285
    d = 0.2 + i * 0.2
    frac = min(val / target, 1) if target else 0
    C = 2 * 3.14159 * 30
    cells += f'''<g class="in" style="animation-delay:{d:.1f}s">
<rect x="{x}" y="36" width="255" height="138" rx="18" fill="url(#card)" stroke="url(#edge)"/>
<circle cx="{x+205}" cy="82" r="30" fill="none" stroke="#ffffff" stroke-opacity=".07" stroke-width="5"/>
<circle cx="{x+205}" cy="82" r="30" fill="none" stroke="{col}" stroke-width="5" stroke-linecap="round"
  stroke-dasharray="{C:.1f}" stroke-dashoffset="{C:.1f}" transform="rotate(-90 {x+205} 82)" class="ring" style="--off:{C*(1-frac):.1f};animation-delay:{d+0.4:.1f}s"/>
<circle cx="{x+205}" cy="82" r="4" fill="{col}" class="pulse"/>
{odometer(val, x+24, 52, d+0.3)}
<text x="{x+24}" y="148" class="l">{label}</text>
<rect x="{x+24}" y="156" width="0" height="2" fill="{col}" class="bar" style="animation-delay:{d+0.6:.1f}s"/>
</g>'''

bar, legend, cx = "", "", 40
for i, (name, v) in enumerate(top):
    w = 1120 * v / total
    bar += f'<rect x="{cx:.1f}" y="226" width="{max(w-3,2):.1f}" height="10" fill="{ACC[i]}" class="grow" style="animation-delay:{1.2+i*0.12:.2f}s"/>'
    cx += w
for i, (name, v) in enumerate(top):
    lx = 40 + i * 224
    legend += f'<circle cx="{lx+6}" cy="266" r="5" fill="{ACC[i]}"/><text x="{lx+20}" y="271" class="lg">{name} <tspan fill="#7b7f94">{100*v/total:.0f}%</tspan></text>'

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="310" viewBox="0 0 1200 310">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#06070c"/><stop offset="1" stop-color="#110d24"/></linearGradient>
<linearGradient id="card" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#151729"/><stop offset="1" stop-color="#0c0d16"/></linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".16"/><stop offset="1" stop-color="#8b7cff" stop-opacity=".06"/></linearGradient>
<clipPath id="dg"><rect x="0" y="0" width="30" height="{DIGIT_H}"/></clipPath>
<clipPath id="bc"><rect x="40" y="226" width="1120" height="10" rx="5"/></clipPath>
<style>
.v{{font:800 46px 'Segoe UI',Inter,Helvetica,Arial,sans-serif;fill:#f3f4ff}}
.l{{font:600 11.5px 'SF Mono',Menlo,Consolas,monospace;letter-spacing:2.5px;fill:#a9adbf}}
.lg{{font:500 15px 'Segoe UI',Inter,Helvetica,Arial,sans-serif;fill:#cfd2e0}}
.h{{font:600 12px 'SF Mono',Menlo,Consolas,monospace;letter-spacing:3px;fill:#7b7f94}}
.in{{opacity:0;animation:in .9s cubic-bezier(.2,.8,.2,1) forwards}}
@keyframes in{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
.roll{{animation:roll 1.8s cubic-bezier(.16,1,.3,1) both}}
@keyframes roll{{from{{transform:translateY(0)}}to{{transform:translateY(var(--to))}}}}
.ring{{animation:ring 1.8s cubic-bezier(.16,1,.3,1) forwards}}
@keyframes ring{{to{{stroke-dashoffset:var(--off)}}}}
.pulse{{animation:p 2.4s ease-in-out infinite}}@keyframes p{{0%,100%{{opacity:.3}}50%{{opacity:1}}}}
.bar{{animation:bw 1.2s cubic-bezier(.16,1,.3,1) forwards}}@keyframes bw{{to{{width:40px}}}}
.grow{{transform-box:fill-box;transform-origin:left;transform:scaleX(0);animation:g 1.1s cubic-bezier(.16,1,.3,1) forwards}}
@keyframes g{{to{{transform:scaleX(1)}}}}
</style></defs>
<rect x="1" y="1" width="1198" height="308" rx="20" fill="url(#bg)" stroke="#ffffff" stroke-opacity=".08"/>
{cells}
<text x="40" y="212" class="h">LANGUAGES</text>
<rect x="40" y="226" width="1120" height="10" rx="5" fill="#1a1c2a"/>
<g clip-path="url(#bc)">{bar}</g>
{legend}
</svg>'''

os.makedirs("assets", exist_ok=True)
open("assets/stats.svg", "w").write(svg)
print("stats.svg written:", [(m[0], m[1]) for m in metrics])
