"""Builds assets/stats.svg from the GitHub API. Runs daily in GitHub Actions."""
import json, os, urllib.request
from collections import Counter
from datetime import datetime, timezone

USER = os.environ.get("GH_USER", "ahmednaffati2004")
TOKEN = os.environ.get("GITHUB_TOKEN")


def get(url, data=None):
    req = urllib.request.Request(url, data=data)
    req.add_header("Accept", "application/vnd.github+json")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req) as r:
        return json.load(r)


user = get(f"https://api.github.com/users/{USER}")
repos = get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner")
stars = sum(r["stargazers_count"] for r in repos)
langs = Counter()
for r in repos:
    if r["language"] and not r["fork"]:
        langs[r["language"]] += max(r["size"], 1)
top = langs.most_common(5)
total = sum(v for _, v in top) or 1
years = datetime.now(timezone.utc).year - int(user["created_at"][:4])

contrib = "—"
if TOKEN:
    q = json.dumps({"query": "query{user(login:\"%s\"){contributionsCollection{contributionCalendar{totalContributions}}}}" % USER}).encode()
    try:
        contrib = get("https://api.github.com/graphql", q)["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    except Exception:
        pass

GOLD = ["#eef0ff", "#a99bff", "#8b7cff", "#5ee1ff", "#4a4290"]
metrics = [("REPOSITORIES", len(repos)), ("STARS EARNED", stars), ("CONTRIBUTIONS · 1Y", contrib), ("YEARS ON GITHUB", years)]

cells = ""
for i, (label, val) in enumerate(metrics):
    x = 40 + i * 285
    d = 0.2 + i * 0.25
    cells += f'''<g class="in" style="animation-delay:{d}s">
<rect x="{x}" y="40" width="255" height="120" rx="14" fill="#11141b" stroke="#8b7cff" stroke-opacity=".22"/>
<text x="{x+24}" y="108" class="v">{val}</text>
<text x="{x+24}" y="138" class="l">{label}</text>
<rect x="{x+24}" y="62" width="28" height="2" fill="#8b7cff"/></g>'''

bar, legend, cx = "", "", 40
for i, (name, v) in enumerate(top):
    w = 1120 * v / total
    bar += f'<rect x="{cx:.1f}" y="214" width="{max(w-3,2):.1f}" height="12" fill="{GOLD[i]}" class="grow" style="animation-delay:{0.9+i*0.12:.2f}s"/>'
    cx += w
for i, (name, v) in enumerate(top):
    lx = 40 + i * 224
    legend += f'<circle cx="{lx+6}" cy="258" r="5" fill="{GOLD[i]}"/><text x="{lx+20}" y="263" class="lg">{name} <tspan fill="#7b7f94">{100*v/total:.0f}%</tspan></text>'

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" viewBox="0 0 1200 300">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a0c11"/><stop offset="1" stop-color="#0e0c1c"/></linearGradient>
<clipPath id="bc"><rect x="40" y="214" width="1120" height="12" rx="6"/></clipPath>
<style>
.v{{font:800 44px 'Segoe UI',Inter,Helvetica,Arial,sans-serif;fill:#eef0ff}}
.l{{font:600 12px 'SF Mono',Menlo,Consolas,monospace;letter-spacing:2.5px;fill:#8b7cff}}
.lg{{font:500 15px 'Segoe UI',Inter,Helvetica,Arial,sans-serif;fill:#cfd2e0}}
.h{{font:600 12px 'SF Mono',Menlo,Consolas,monospace;letter-spacing:3px;fill:#7b7f94}}
.in{{opacity:0;animation:in .9s cubic-bezier(.2,.8,.2,1) forwards}}
@keyframes in{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:none}}}}
.grow{{transform-box:fill-box;transform-origin:left;transform:scaleX(0);animation:g 1s cubic-bezier(.2,.8,.2,1) forwards}}
@keyframes g{{to{{transform:scaleX(1)}}}}
</style></defs>
<rect x="1" y="1" width="1198" height="298" rx="18" fill="url(#bg)" stroke="#8b7cff" stroke-opacity=".25"/>
{cells}
<text x="40" y="200" class="h">LANGUAGES</text>
<rect x="40" y="214" width="1120" height="12" rx="6" fill="#1b1f28"/>
<g clip-path="url(#bc)">{bar}</g>
{legend}
</svg>'''

os.makedirs("assets", exist_ok=True)
open("assets/stats.svg", "w").write(svg)
print("stats.svg written:", metrics, top)
