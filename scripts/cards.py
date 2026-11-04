# Executed by gen_cards.py. Builds ONE seamless cinematic SVG: the matrix header flowing into a descent
# through a digital world. Shares: w, G, repos, langs, html, random, OUT, os.
import re, math, datetime
random.seed(42)
W = 1000; HH = 260; SH = 1640           # header height, scene height (below header)
TOT = HH + SH
header = open(os.path.join(OUT, "matrix-header.svg")).read()
hbody = re.sub(r"^<svg[^>]*>|</svg>\s*$", "", header.strip())
K = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉ01"
P = []                                   # scene parts, y relative to scene top

# 1) rain thinning out and dissolving into drifting particles
for i in range(60):
    x = random.randint(0, W); d = random.uniform(3, 7); dl = random.uniform(-7, 0); s = random.randint(10, 16)
    ch = "".join(f'<tspan x="{x}" dy="{s+2}">{random.choice(K)}</tspan>' for _ in range(random.randint(4, 9)))
    P.append(f'<text font-size="{s}" opacity="{random.uniform(.2,.6):.2f}" style="animation:sdrop {d:.1f}s linear {dl:.1f}s infinite">{ch}</text>')
for i in range(140):
    x = random.randint(0, W); y = random.randint(40, 520); r = random.uniform(.6, 2.2); d = random.uniform(4, 10)
    P.append(f'<circle cx="{x}" cy="{y}" r="{r:.1f}" fill="{G}" style="animation:float {d:.1f}s ease-in-out {-random.uniform(0,d):.1f}s infinite alternate"/>')

# 2) glitch whisper line
P.append(f'''<g text-anchor="middle" class="gl"><text x="500" y="250" font-size="22" letter-spacing="8" class="glr">ENTER THE GRID</text>
<text x="500" y="250" font-size="22" letter-spacing="8" class="glc">ENTER THE GRID</text>
<text x="500" y="250" font-size="22" letter-spacing="8" filter="url(#sg)">ENTER THE GRID</text></g>
<text x="500" y="285" font-size="12" letter-spacing="6" text-anchor="middle" opacity=".55">descending into the grid<tspan class="blink">_</tspan></text>''')

# 3) neon sun + skyline
SY = 640
P.append(f'''<defs><clipPath id="sun"><circle cx="500" cy="{SY-40}" r="150"/></clipPath>
<linearGradient id="sunf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{G}" stop-opacity=".9"/><stop offset="1" stop-color="{G}" stop-opacity=".05"/></linearGradient></defs>
<g clip-path="url(#sun)"><rect x="350" y="{SY-190}" width="300" height="300" fill="url(#sunf)"/>
{"".join(f'<rect x="350" y="{SY-120+i*14}" width="300" height="{2+i*0.9:.1f}" fill="#000"/>' for i in range(10))}</g>''')
bx = 0
far, near = [], []
while bx < W:
    bw = random.randint(30, 70); bh = random.randint(60, 200)
    far.append(f'<rect x="{bx}" y="{SY-bh}" width="{bw}" height="{bh}" fill="#000" stroke="{G}" stroke-opacity=".25"/>')
    bx += bw + random.randint(0, 8)
bx = -10
while bx < W:
    bw = random.randint(40, 90); bh = random.randint(40, 140)
    near.append(f'<rect x="{bx}" y="{SY-bh+10}" width="{bw}" height="{bh+20}" fill="#000" stroke="{G}" stroke-opacity=".7"/>')
    for wy in range(SY - bh + 22, SY, 14):
        for wx in range(bx + 6, bx + bw - 6, 11):
            if random.random() < .35:
                near.append(f'<rect x="{wx}" y="{wy}" width="5" height="6" fill="{G}" style="animation:win {random.uniform(2,9):.1f}s steps(1) {-random.uniform(0,9):.1f}s infinite"/>')
    if random.random() < .3:
        ax = bx + bw // 2
        near.append(f'<line x1="{ax}" y1="{SY-bh+10}" x2="{ax}" y2="{SY-bh-25}" stroke="{G}"/><circle cx="{ax}" cy="{SY-bh-25}" r="2.5" fill="#ff0055" class="blink"/>')
    bx += bw + random.randint(2, 14)
P.append('<g filter="url(#sg)" opacity=".8">' + "".join(far) + '</g><g>' + "".join(near) + '</g>')

# 4) synthwave perspective grid floor (scrolling)
GY = SY + 30; GH = 330
lines = "".join(f'<line x1="500" y1="{GY}" x2="{500+k*90}" y2="{GY+GH}" stroke="{G}" stroke-opacity=".5"/>' for k in range(-16, 17))
hz = "".join(f'<line class="hz" x1="0" x2="{W}" y1="0" y2="0" stroke="{G}" style="animation:hz 4s linear {-i*4/9:.2f}s infinite"/>' for i in range(9))
P.append(f'''<rect x="0" y="{SY+10}" width="{W}" height="2" fill="{G}" filter="url(#sg)"/>
<svg x="0" y="{GY}" width="{W}" height="{GH}" overflow="hidden"><g transform="translate(0,{-GY})">{lines}</g>{hz}</svg>''')

# 5) project names drifting as holographic ghosts through the void
projects = ["SPIN-RUMBLE", "BLADE-TILT", "NEON-FPS", "BATTLE-ROYALE-CORE", "NEON-DECEIT", "SYNTH-EIGHT", "THREAT-INTEL"]
for i, n in enumerate(projects):
    y = GY + 40 + i * 42; sz = 14 + (i % 3) * 8; d = 18 + i * 3
    P.append(f'<text y="{y}" font-size="{sz}" letter-spacing="6" opacity="{.25+(i%3)*.2:.2f}" style="animation:drift {d}s linear {-i*5}s infinite">{n}</text>')

# 6) the tunnel: rotating dashed rings + orbiting language words
TY = GY + GH + 280
rings = "".join(f'<circle cx="500" cy="{TY}" r="{r}" fill="none" stroke="{G}" stroke-opacity="{.15+i*.08:.2f}" stroke-dasharray="{4+i*3} {8+i*5}" style="transform-origin:500px {TY}px;animation:spin {10+i*4}s linear infinite {"reverse" if i%2 else "normal"}"/>' for i, r in enumerate([40, 80, 125, 175, 230]))
words = [l for l, _ in langs.most_common(6)] or ["TypeScript", "C#", "Python"]
orb = "".join(f'<g style="transform-origin:500px {TY}px;animation:spin {26+i*5}s linear {-i*4}s infinite"><text x="{500+90+i*28}" y="{TY}" font-size="{12+i%3*2}" opacity=".75">{html.escape(wd)}</text></g>' for i, wd in enumerate(words))
P.append(rings + orb + f'''<circle cx="500" cy="{TY}" r="10" fill="{G}" filter="url(#sg)"><animate attributeName="r" values="8;14;8" dur="2s" repeatCount="indefinite"/></circle>''')

# 7) outro: heartbeat line + transmission end + fade to page background
OY = SH - 150
ekg = f"M0 {OY} " + " ".join(f"L{x} {OY}" if (x // 100) % 3 else f"L{x} {OY} L{x+10} {OY-40} L{x+20} {OY+30} L{x+30} {OY}" for x in range(0, W, 50))
P.append(f'''<path d="{ekg}" fill="none" stroke="{G}" stroke-width="2" filter="url(#sg)" stroke-dasharray="1400" style="animation:ekg 4s linear infinite"/>
<text x="500" y="{OY+60}" font-size="13" letter-spacing="10" text-anchor="middle" opacity=".7">END OF TRANSMISSION</text>
<text x="500" y="{OY+82}" font-size="10" letter-spacing="4" text-anchor="middle" opacity=".4">jatin@matrix:~$ exit<tspan class="blink">█</tspan></text>''')

scene = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{TOT}" viewBox="0 0 {W} {TOT}">
<defs><filter id="sg"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="outfade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d1117" stop-opacity="0"/><stop offset="1" stop-color="#0d1117"/></linearGradient>
<pattern id="sscan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#000" opacity=".3"/></pattern></defs>
<style>
@keyframes sdrop{{from{{transform:translateY(-200px);opacity:.6}}to{{transform:translateY(560px);opacity:0}}}}
@keyframes float{{from{{transform:translate(0,0)}}to{{transform:translate(12px,-40px)}}}}
@keyframes win{{0%{{opacity:1}}50%{{opacity:.15}}}}
@keyframes hz{{from{{transform:translateY(0)}}to{{transform:translateY({GH}px)}}}}
@keyframes drift{{from{{transform:translateX(-420px)}}to{{transform:translateX(1100px)}}}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes ekg{{from{{stroke-dashoffset:1400}}to{{stroke-dashoffset:-1400}}}}
@keyframes sb{{50%{{opacity:0}}}} .blink{{animation:sb 1s steps(1) infinite}}
.glr{{fill:#ff0055;animation:g1 3.5s infinite}} .glc{{fill:#00e5ff;animation:g2 3.5s infinite}}
@keyframes g1{{0%,84%,100%{{opacity:0;transform:none}}86%{{opacity:.8;transform:translate(-5px,1px)}}90%{{opacity:.8;transform:translate(4px,-2px)}}92%{{opacity:0}}}}
@keyframes g2{{0%,84%,100%{{opacity:0;transform:none}}87%{{opacity:.8;transform:translate(5px,-1px)}}91%{{opacity:.8;transform:translate(-3px,2px)}}93%{{opacity:0}}}}
</style>
<rect width="{W}" height="{TOT}" fill="#000"/>
<g>{hbody}</g>
<g transform="translate(0,{HH})" font-family="'Courier New',monospace" fill="{G}">{"".join(P)}</g>
<rect y="{TOT-120}" width="{W}" height="120" fill="url(#outfade)"/>
<rect width="{W}" height="{TOT}" fill="url(#sscan)" opacity=".6"/>
</svg>'''
w("scene.svg", scene)
