"""Builds assets/avatar.svg: AN monogram in the profile's platinum/indigo style."""
import base64, os

D = os.path.dirname(__file__)
pf = base64.b64encode(open(os.path.join(D, "fonts", "playfair-name.woff2"), "rb").read()).decode()

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
<defs>
<style>@font-face{{font-family:'PF';font-style:italic;font-weight:800;src:url(data:font/woff2;base64,{pf}) format('woff2')}}</style>
<radialGradient id="bg" cx=".3" cy=".25" r=".95"><stop offset="0" stop-color="#2a2160"/><stop offset=".45" stop-color="#0f0d24"/><stop offset="1" stop-color="#04050a"/></radialGradient>
<radialGradient id="cy" cx=".85" cy=".9" r=".6"><stop offset="0" stop-color="#25c7ff" stop-opacity=".35"/><stop offset="1" stop-color="#25c7ff" stop-opacity="0"/></radialGradient>
<linearGradient id="metal" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".45" stop-color="#dcdff3"/><stop offset=".72" stop-color="#a99bff"/><stop offset="1" stop-color="#5ee1ff"/></linearGradient>
<linearGradient id="ring" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".55"/><stop offset=".5" stop-color="#8b7cff" stop-opacity=".25"/><stop offset="1" stop-color="#5ee1ff" stop-opacity=".6"/></linearGradient>
<filter id="glow"><feGaussianBlur stdDeviation="18"/></filter>
</defs>
<rect width="1024" height="1024" fill="url(#bg)"/>
<rect width="1024" height="1024" fill="url(#cy)"/>
<g fill="none" stroke="#ffffff" stroke-opacity=".06">
<ellipse cx="512" cy="512" rx="470" ry="170" transform="rotate(-24 512 512)"/>
<ellipse cx="512" cy="512" rx="470" ry="170" transform="rotate(24 512 512)"/></g>
<circle cx="512" cy="512" r="372" fill="none" stroke="url(#ring)" stroke-width="3"/>
<circle cx="512" cy="512" r="392" fill="none" stroke="#ffffff" stroke-opacity=".08"/>
<circle cx="855" cy="365" r="9" fill="#b9adff"/><circle cx="182" cy="650" r="6" fill="#5ee1ff"/>
<text x="500" y="625" text-anchor="middle" font-family="PF" font-style="italic" font-weight="800" font-size="330" fill="#8b7cff" opacity=".55" filter="url(#glow)">AN</text>
<text x="500" y="625" text-anchor="middle" font-family="PF" font-style="italic" font-weight="800" font-size="330" fill="url(#metal)">AN</text>
<rect x="432" y="690" width="160" height="2" fill="url(#ring)"/>
</svg>'''
open(os.path.join(D, "..", "assets", "avatar.svg"), "w").write(svg)
