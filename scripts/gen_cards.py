#!/usr/bin/env python3
"""Regenerate assets/*.svg from live GitHub data. Usage: python3 scripts/gen_cards.py (needs `gh` logged in)."""
import json, subprocess, random, collections, html, os
U = "anonymous-namo-1"
OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
G = "#00ff41"
def gh(*a): return json.loads(subprocess.check_output(["gh", *a]))
repos = gh("repo", "list", U, "--limit", "200", "--json", "name,description,primaryLanguage,stargazerCount,forkCount,isPrivate,updatedAt,diskUsage")
langs = collections.Counter()
for r in repos:
    try: langs.update(gh("api", f"repos/{U}/{r['name']}/languages"))
    except Exception: pass
def w(name, s): open(os.path.join(OUT, name), "w").write(s)
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
.t{{font-size:78px;font-weight:900;letter-spacing:10px;opacity:0;animation:rev 1s 1.2s forwards}} @keyframes rev{{to{{opacity:1}}}}
.r{{fill:#ff0055;opacity:0;animation:gl1 3s 2.2s infinite}} .c{{fill:#00e5ff;opacity:0;animation:gl2 3s 2.2s infinite}}
@keyframes gl1{{0%,86%,100%{{opacity:0;transform:none}}88%{{opacity:.8;transform:translate(-6px,2px)}}91%{{opacity:.8;transform:translate(5px,-3px)}}94%{{opacity:0}}}}
@keyframes gl2{{0%,86%,100%{{opacity:0;transform:none}}89%{{opacity:.8;transform:translate(6px,-2px)}}92%{{opacity:.8;transform:translate(-4px,3px)}}95%{{opacity:0}}}}
.s{{font-size:18px;opacity:0;animation:rev .5s 2s forwards}} .cur{{animation:bl 1s steps(1) infinite}} @keyframes bl{{50%{{opacity:0}}}}</style>
<rect width="{W}" height="{H}" fill="#000"/><g opacity=".55">{"".join(cols)}</g><rect width="{W}" height="{H}" fill="url(#fade)"/>
<rect x="190" y="72" width="620" height="120" fill="#000" opacity="0"><animate attributeName="opacity" from="0" to=".75" begin="1s" dur="1s" fill="freeze"/></rect>
<g text-anchor="middle"><text class="t r" x="500" y="155">JATIN VERMA</text><text class="t c" x="500" y="155">JATIN VERMA</text>
<text class="t" x="500" y="155" filter="url(#g)">JATIN VERMA</text>
<text class="s" x="500" y="185">&gt; full-stack dev // game builder // breaking things since boot<tspan class="cur">█</tspan></text></g>
<rect width="{W}" height="{H}" fill="url(#scan)"/></svg>''')

# ---- boot terminal
nrep = len(repos); pub = sum(not r["isPrivate"] for r in repos)
lines = [("[  OK  ] booting jatin-os v26.11 ...", 0), ("[  OK  ] loading modules: react node unity python docker", 0),
 ("[  OK  ] mounting /dev/creativity", 0), ("$ whoami", 1), ("jatin verma :: full-stack developer + game dev", 0),
 ("$ ls ~/projects | head", 1), ("spin-rumble  blade-tilt  neon-fps  Battle-Royale-Core  neon-deceit-game", 0),
 (f"$ gh repo list --count  ->  {nrep} repos", 1), ("$ ./ship --now", 1), ("access granted. welcome, operator.█", 0)]
body = ""
for i, (l, cmd) in enumerate(lines):
    y = 70 + i * 24; b = 0.4 + i * 0.7; n = len(l)
    body += (f'<clipPath id="c{i}"><rect x="18" y="{y-16}" height="22" width="0"><animate attributeName="width" from="0" to="{n*9+10}" begin="{b}s" dur="{min(.6,n*.02):.2f}s" fill="freeze"/></rect></clipPath>'
             f'<text x="22" y="{y}" font-size="15" clip-path="url(#c{i})" class="{"" if cmd else "dim" if l.startswith("[") else ""}">{html.escape(l)}</text>')
term = crt(1000, 330, body, "jatin@matrix: ~ — bash").replace('<text x="18" y="28"', '<circle cx="24" cy="22" r="6" fill="#ff5f56"/><circle cx="44" cy="22" r="6" fill="#ffbd2e"/><circle cx="64" cy="22" r="6" fill="#27c93f"/><text x="84" y="27"')
w("boot.svg", term)

# ---- stats card
tot = sum(langs.values()) or 1
stars = sum(r["stargazerCount"] for r in repos)
recent = sorted(repos, key=lambda r: r["updatedAt"])[-1]["name"]
rows = [("REPOSITORIES", nrep), ("PUBLIC", pub), ("LANGUAGES", len(langs)), ("CODE (KB)", f"{tot//1024:,}"), ("STARS", stars), ("LAST PUSH", recent[:22])]
b = "".join(f'<text x="22" y="{70+i*28}" font-size="14" class="dim">&gt; {k}</text><text x="470" y="{70+i*28}" font-size="15" text-anchor="end" font-weight="bold">{html.escape(str(v))}</text>' for i, (k, v) in enumerate(rows))
w("stats.svg", crt(490, 240, b, "SYS.STATS // anonymous-namo-1"))
b = ""
for i, (l, v) in enumerate(langs.most_common(6)):
    p = v / tot * 100; y = 66 + i * 28
    b += (f'<text x="22" y="{y}" font-size="13">{html.escape(l)}</text><text x="470" y="{y}" font-size="13" text-anchor="end">{p:.1f}%</text>'
          f'<rect x="150" y="{y-10}" width="260" height="10" fill="{G}" opacity=".12"/><rect x="150" y="{y-10}" height="10" fill="{G}" width="0"><animate attributeName="width" to="{2.6*p:.1f}" dur="1.5s" begin="{.2*i}s" fill="freeze"/></rect>')
w("languages.svg", crt(490, 240, b, "LANG.BYTES // across all repos"))

# ---- dossiers
proj = [("spin-rumble", "ARENA BRAWLER", "Spinner combat game"), ("blade-tilt", "PHYSICS ACTION", "Tilt-and-slice blade game"),
        ("neon-fps", "FPS", "Neon-lit shooter in the browser"), ("Battle-Royale-Core", "MULTIPLAYER", "Battle royale core systems"),
        ("neon-deceit-game", "SOCIAL DEDUCTION", "Neon deception game"),
        ("SIH26151-Threat-Intelligence-1", "CYBERSEC", "SIH threat-intel platform"), ("synth-eight", "WEB", "Synth-eight project")]
info = {r["name"]: r for r in repos}
for i, (n, tag, d) in enumerate(proj):
    r = info.get(n, {}); lg = (r.get("primaryLanguage") or {}).get("name", "?")
    b = (f'<text x="22" y="62" font-size="11" class="dim">CLASSIFICATION: {tag}</text><text x="22" y="84" font-size="13">{html.escape(d)}</text>'
         f'<text x="22" y="108" font-size="11" class="dim">LANG: {lg}  ★ {r.get("stargazerCount",0)}  STATUS: ACTIVE</text>'
         f'<rect x="300" y="50" width="70" height="20" fill="none" stroke="{G}"><animate attributeName="opacity" values="1;.2;1" dur="2s" begin="{i*.3}s" repeatCount="indefinite"/></rect><text x="335" y="64" font-size="10" text-anchor="middle">ACCESS</text>')
    w(f"dossier-{n}.svg", crt(390, 125, b, f"FILE #{i+1:03d} :: {n[:26]}"))
# ---- footer
w("footer.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="90" viewBox="0 0 1000 90">{FX}<rect width="1000" height="90" fill="#000"/>
<g filter="url(#glow)" class="flick"><text x="500" y="40" font-size="16" text-anchor="middle">[ CONNECTION TERMINATED ] — thanks for visiting, operator</text>
<text x="500" y="66" font-size="12" text-anchor="middle" class="dim">jatin@matrix:~$ exit <tspan style="animation:fl 1s steps(1) infinite">█</tspan></text></g>
<rect class="sweep" width="1000" height="20" fill="{G}" opacity=".06"/><rect width="1000" height="90" fill="url(#scan)"/></svg>''')
print("ok", nrep, dict(langs.most_common(6)))
