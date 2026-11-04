#!/usr/bin/env python3
"""Regenerate assets/*.svg from live GitHub data. Usage: python3 scripts/gen_cards.py (needs `gh` logged in)."""
import json, subprocess, random, collections, html, os
U = "anonymous-namo-1"
OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
G = "#00ff41"
_CACHE = os.environ.get("GH_CACHE")
_c = json.load(open(_CACHE)) if _CACHE and os.path.exists(_CACHE) else {}
def gh(*a):
    k = " ".join(a)
    if k not in _c: _c[k] = json.loads(subprocess.check_output(["gh", *a]))
    if _CACHE: json.dump(_c, open(_CACHE, "w"))
    return _c[k]
repos = gh("repo", "list", U, "--limit", "200", "--json", "name,description,primaryLanguage,stargazerCount,forkCount,isPrivate,updatedAt,createdAt,diskUsage")
langs = collections.Counter()
for r in repos:
    try: l = gh("api", f"repos/{U}/{r['name']}/languages")
    except Exception: continue
    # repos with huge C/C++ blobs are vendored engines/SDKs, not hand-written code
    if l.get("C", 0) + l.get("C++", 0) > 20_000_000:
        l.pop("C", None); l.pop("C++", None)
    langs.update(l)
PAPER, INK, AMBER = "#f5f0e1", "#14532d", "#a16207"
def light(s):
    """Light 'field notebook' variant: paper bg, deep-green ink, amber secondary, crisp (low) glow."""
    return (s.replace("#020a04", PAPER).replace("#000", PAPER).replace(G, INK).replace("#0a8f2a", AMBER)
             .replace('stdDeviation="2"', 'stdDeviation=".4"').replace('stdDeviation="3"', 'stdDeviation=".6"')
             .replace('opacity=".55"', 'opacity=".28"').replace('opacity=".35"', 'opacity=".5"')
             .replace("#0d1117", "#ffffff").replace("#ff0055", "#be123c").replace("#00e5ff", "#0369a1"))
def w(name, s):
    open(os.path.join(OUT, name), "w").write(s)
    open(os.path.join(OUT, name.replace(".svg", "-light.svg")), "w").write(light(s))
FX = f'''<defs><filter id="glow"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#000" opacity=".35"/></pattern>
<radialGradient id="vig" cx="50%" cy="50%" r="75%"><stop offset="60%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#000" stop-opacity=".7"/></radialGradient></defs>
<style>text{{font-family:'Courier New',Consolas,monospace;fill:{G}}} .dim{{fill:#0a8f2a}} .flick{{animation:fl 4s infinite}} @keyframes fl{{0%,100%{{opacity:1}}92%{{opacity:1}}93%{{opacity:.6}}94%{{opacity:1}}96%{{opacity:.8}}}}
.sweep{{animation:sw 6s linear infinite}} @keyframes sw{{from{{transform:translateY(-40px)}}to{{transform:translateY(400px)}}}}</style>'''
def crt(wd, ht, body, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{wd}" height="{ht}" viewBox="0 0 {wd} {ht}">{FX}
<rect width="{wd}" height="{ht}" rx="10" fill="#020a04" stroke="{G}" stroke-opacity=".6"/>
<g class="flick" filter="url(#glow)"><text x="18" y="28" font-size="14" font-weight="bold">{html.escape(title)}</text>
<line x1="18" y1="38" x2="{wd-18}" y2="38" stroke="{G}" stroke-opacity=".4"/>{body}</g>
<rect class="sweep" width="{wd}" height="30" fill="{G}" opacity=".05"/>
<rect width="{wd}" height="{ht}" rx="10" fill="url(#scan)"/><rect width="{wd}" height="{ht}" rx="10" fill="url(#vig)"/></svg>'''

LC = {"TypeScript":"#3178c6","C#":"#178600","JavaScript":"#f1e05a","Python":"#3572A5","CSS":"#663399","HTML":"#e34c26","Shell":"#89e051"}
# ---- matrix header
random.seed(7); W, H = 1000, 260
chars = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉ0123456789"
cols = []
for i in range(50):
    x = i * 20 + 6; d = random.uniform(2.5, 6); dl = random.uniform(-6, 0)
    txt = "".join(f'<tspan x="{x}" dy="20">{random.choice(chars)}</tspan>' for _ in range(14))
    cols.append(f'<text y="-300" font-size="18" style="animation:fall {d:.2f}s linear {dl:.2f}s infinite">{txt}</text>')
w("matrix-header.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".9"/></linearGradient>
<filter id="g"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#000" opacity=".3"/></pattern></defs>
<style>text{{font-family:'Courier New',monospace;fill:{G}}} @keyframes fall{{from{{transform:translateY(0)}}to{{transform:translateY(600px)}}}}
.t{{font-size:78px;font-weight:900;letter-spacing:10px;opacity:0;animation:rev .6s .3s forwards}} @keyframes rev{{to{{opacity:1}}}}
.r{{fill:#ff0055;opacity:0;animation:gl1 3s 1s infinite}} .c{{fill:#00e5ff;opacity:0;animation:gl2 3s 1s infinite}}
@keyframes gl1{{0%,86%,100%{{opacity:0;transform:none}}88%{{opacity:.8;transform:translate(-6px,2px)}}91%{{opacity:.8;transform:translate(5px,-3px)}}94%{{opacity:0}}}}
@keyframes gl2{{0%,86%,100%{{opacity:0;transform:none}}89%{{opacity:.8;transform:translate(6px,-2px)}}92%{{opacity:.8;transform:translate(-4px,3px)}}95%{{opacity:0}}}}
.s{{font-size:18px;opacity:0;animation:rev .5s .8s forwards}} .cur{{animation:bl 1s steps(1) infinite}} @keyframes bl{{50%{{opacity:0}}}}</style>
<rect width="{W}" height="{H}" fill="#000"/><g opacity=".55">{"".join(cols)}</g><rect width="{W}" height="{H}" fill="url(#fade)"/>
<rect x="190" y="72" width="620" height="120" fill="#000" opacity="0"><animate attributeName="opacity" from="0" to=".75" begin="1s" dur="1s" fill="freeze"/></rect>
<g text-anchor="middle"><text class="t r" x="500" y="155">JATIN VERMA</text><text class="t c" x="500" y="155">JATIN VERMA</text>
<text class="t" x="500" y="155" filter="url(#g)">JATIN VERMA</text>
<text class="s" x="500" y="185">&gt; full-stack dev // game builder // breaking things since boot<tspan class="cur">█</tspan></text></g>
<g text-anchor="middle" font-size="14" opacity=".9">{"".join(f'<text x="500" y="222" opacity="0">[ {r} ]<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.04;.21;.25;1" dur="12s" begin="{1+i*3}s" repeatCount="indefinite"/></text>' for i,r in enumerate(["FULL-STACK DEV","GAME DEVELOPER","UNITY + C#","REACT + NODE"]))}</g>
<rect width="{W}" height="24" fill="{G}" opacity=".06"><animate attributeName="y" from="-24" to="{H}" dur="5s" repeatCount="indefinite"/></rect>
<rect width="{W}" height="{H}" fill="url(#scan)"/></svg>''')

nrep = len(repos); pub = sum(not r["isPrivate"] for r in repos)
exec(open(os.path.join(os.path.dirname(__file__), "cards.py")).read())
print("ok", nrep, dict(langs.most_common(6)))
