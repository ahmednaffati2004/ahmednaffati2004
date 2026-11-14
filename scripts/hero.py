"""Builds assets/hero.svg with embedded subset fonts (Playfair Display, Space Grotesk, Reem Kufi; OFL)."""
import base64, os

D = os.path.dirname(__file__)
def font(name):
    return base64.b64encode(open(os.path.join(D, "fonts", name), "rb").read()).decode()

NAME = "Ahmed Naffati"
letters = ""
for i, ch in enumerate(NAME):
    if ch == " ":
        letters += '<tspan class="ch"> </tspan>'
        continue
    letters += f'<tspan class="ch" style="animation-delay:{0.25 + i * 0.07:.2f}s">{ch}</tspan>'

stars = ""
import random
random.seed(7)
for _ in range(46):
    x, y, r = random.randint(10, 1190), random.randint(10, 390), random.choice([0.6, 0.8, 1, 1.3])
    stars += f'<circle cx="{x}" cy="{y}" r="{r}" class="st" style="animation-delay:-{random.uniform(0,4):.1f}s"/>'

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="400" viewBox="0 0 1200 400">
<defs>
<style>
@font-face{{font-family:'PF';font-style:italic;font-weight:800;src:url(data:font/woff2;base64,{font("playfair-name.woff2")}) format('woff2')}}
@font-face{{font-family:'SG';font-weight:500;src:url(data:font/woff2;base64,{font("grotesk-role.woff2")}) format('woff2')}}
@font-face{{font-family:'RK';font-weight:500;src:url(data:font/woff2;base64,{font("kufi-ar.woff2")}) format('woff2')}}
.name{{font:italic 800 104px 'PF',Georgia,serif;letter-spacing:-1px}}
.ch{{opacity:0;animation:ch .9s cubic-bezier(.2,.8,.2,1) forwards}}
@keyframes ch{{from{{opacity:0;filter:blur(8px)}}to{{opacity:1;filter:blur(0)}}}}
.outline{{fill:none;stroke:url(#metal);stroke-width:1.2;stroke-dasharray:900;stroke-dashoffset:900;animation:draw 2.4s .2s ease forwards}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
.role{{font:500 17px 'SG',Helvetica,Arial,sans-serif;letter-spacing:9px;fill:#c4c8dc;opacity:0;animation:up 1s 1.3s cubic-bezier(.2,.8,.2,1) forwards}}
.ar{{font:500 24px 'RK',Tahoma,sans-serif;fill:#8f93ab;opacity:0;animation:up 1s 1.6s cubic-bezier(.2,.8,.2,1) forwards}}
@keyframes up{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
.rule{{stroke:url(#acc);stroke-width:1.5;stroke-dasharray:300;stroke-dashoffset:300;animation:draw 1.4s 1.1s ease forwards}}
.st{{fill:#dfe3ff;animation:tw 4s ease-in-out infinite}}
@keyframes tw{{0%,100%{{opacity:.1}}50%{{opacity:.8}}}}
.au1{{animation:a1 14s ease-in-out infinite}}.au2{{animation:a2 18s ease-in-out infinite}}
@keyframes a1{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(120px,30px)}}}}
@keyframes a2{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(-140px,-20px)}}}}
.orbit{{transform-origin:600px 200px;animation:spin 40s linear infinite}}
.orbit2{{transform-origin:600px 200px;animation:spin 60s linear infinite reverse}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.sheen{{animation:sh 6s ease-in-out 2.4s infinite}}
@keyframes sh{{0%{{transform:translateX(-500px)}}60%,100%{{transform:translateX(1300px)}}}}
</style>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#05060b"/><stop offset=".6" stop-color="#0b0b18"/><stop offset="1" stop-color="#120d26"/></linearGradient>
<linearGradient id="metal" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#ffffff"/><stop offset=".45" stop-color="#d9dcf0"/><stop offset=".7" stop-color="#a99bff"/><stop offset="1" stop-color="#5ee1ff"/></linearGradient>
<linearGradient id="acc" x1="0" x2="1"><stop offset="0" stop-color="#8b7cff" stop-opacity="0"/><stop offset=".5" stop-color="#b9adff"/><stop offset="1" stop-color="#5ee1ff" stop-opacity="0"/></linearGradient>
<linearGradient id="shine" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<radialGradient id="a" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#6d5cff" stop-opacity=".45"/><stop offset="1" stop-color="#6d5cff" stop-opacity="0"/></radialGradient>
<radialGradient id="b" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#25c7ff" stop-opacity=".28"/><stop offset="1" stop-color="#25c7ff" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse"><path d="M48 0H0V48" fill="none" stroke="#ffffff" stroke-opacity=".035"/></pattern>
<clipPath id="r"><rect width="1200" height="400" rx="22"/></clipPath>
<mask id="tm"><text x="600" y="208" text-anchor="middle" class="name" fill="#fff">{NAME}</text></mask>
</defs>
<g clip-path="url(#r)">
<rect width="1200" height="400" fill="url(#bg)"/>
<rect width="1200" height="400" fill="url(#grid)"/>
<g class="au1"><ellipse cx="330" cy="120" rx="380" ry="220" fill="url(#a)"/></g>
<g class="au2"><ellipse cx="900" cy="300" rx="360" ry="200" fill="url(#b)"/></g>
{stars}
<g class="orbit" fill="none" stroke="#ffffff" stroke-opacity=".07"><ellipse cx="600" cy="200" rx="470" ry="150"/><circle cx="1070" cy="200" r="3.5" fill="#b9adff" stroke="none"/></g>
<g class="orbit2" fill="none" stroke="#ffffff" stroke-opacity=".05"><ellipse cx="600" cy="200" rx="540" ry="185"/><circle cx="60" cy="200" r="2.5" fill="#5ee1ff" stroke="none"/></g>
</g>
<text x="600" y="208" text-anchor="middle" class="name outline">{NAME}</text>
<text x="600" y="208" text-anchor="middle" class="name" fill="url(#metal)">{letters}</text>
<g mask="url(#tm)"><rect class="sheen" x="0" y="80" width="220" height="160" fill="url(#shine)" transform="skewX(-20)"/></g>
<line class="rule" x1="450" y1="246" x2="750" y2="246"/>
<text x="600" y="286" text-anchor="middle" class="role">FULL-STACK · MOBILE · PRODUCT ENGINEER</text>
<text x="600" y="334" text-anchor="middle" class="ar" direction="rtl">أحمد النفاتي — طرابلس، ليبيا</text>
<rect x="1" y="1" width="1198" height="398" rx="22" fill="none" stroke="#ffffff" stroke-opacity=".08"/>
</svg>'''
open(os.path.join(D, "..", "assets", "hero.svg"), "w").write(svg)
