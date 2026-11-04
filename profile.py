#!/usr/bin/env python3
"""Builds dark_mode.svg / light_mode.svg (neofetch-style profile card) from live GitHub data.
Layout inspired by Andrew6rant's profile README (github.com/Andrew6rant/Andrew6rant); code written from scratch.
Usage: python3 profile.py [--ascii-from photo.jpg]   (needs `gh` logged in, or GH_TOKEN for CI)"""
import json, subprocess, sys, os, datetime, html
U = "anonymous-namo-1"
HERE = os.path.dirname(os.path.abspath(__file__))

def gh(*a): return json.loads(subprocess.check_output(["gh", *a]))

def image_to_ascii(path, cols=38, rows=24):
    from PIL import Image, ImageOps
    ramp = " .'`^,:;Il!i><~+_-?][}{1)(|tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    im = ImageOps.autocontrast(Image.open(path).convert("L")).resize((cols, rows))
    return "\n".join("".join(ramp[(255 - im.getpixel((x, y))) * (len(ramp) - 1) // 255] for x in range(cols)) for y in range(rows))

if "--ascii-from" in sys.argv:
    open(os.path.join(HERE, "ascii.txt"), "w").write(image_to_ascii(sys.argv[sys.argv.index("--ascii-from") + 1]))

# ---- data
user = gh("api", f"users/{U}")
repos = gh("repo", "list", U, "--limit", "200", "--json", "name,stargazerCount,isFork")
q = '{user(login:"%s"){repositoriesContributedTo(contributionTypes:[COMMIT,PULL_REQUEST,REPOSITORY]){totalCount} contributionsCollection{totalCommitContributions restrictedContributionsCount}}}' % U
g = gh("api", "graphql", "-f", "query=" + q)["data"]["user"]
commits = gh("api", f"search/commits?q=author:{U}")["total_count"]  # all-time, public repos
add = dele = 0
for r in repos:
    if r["isFork"]: continue
    st = []
    for _ in range(5):  # GitHub answers 202 (empty) while it computes stats
        try: st = gh("api", f"repos/{U}/{r['name']}/stats/contributors")
        except Exception: st = []
        if isinstance(st, list) and st: break
        import time; time.sleep(3)
    for c in st if isinstance(st, list) else []:
        if (c.get("author") or {}).get("login", "").lower() == U.lower():
            # skip weeks that look like bulk imports of vendored engines/assets (>50k lines)
            wk_ok = [wk for wk in c["weeks"] if wk["a"] + wk["d"] <= 50_000]
            add += sum(wk["a"] for wk in wk_ok); dele += sum(wk["d"] for wk in wk_ok)
created = datetime.datetime.fromisoformat(user["created_at"].replace("Z", "+00:00"))
now = datetime.datetime.now(datetime.timezone.utc)
m = (now.year - created.year) * 12 + now.month - created.month - (now.day < created.day)
dd = (now - created.replace(year=created.year + (created.month + m - 1) // 12, month=(created.month + m - 1) % 12 + 1)).days
up = f"{m//12} year{'s'*(m//12!=1)}, {m%12} month{'s'*(m%12!=1)}, {dd} day{'s'*(dd!=1)}" if m >= 12 else f"{m} months, {dd} days"
stats = dict(repos=len(repos), stars=sum(r["stargazerCount"] for r in repos), contrib=g["repositoriesContributedTo"]["totalCount"],
             commits=commits, followers=user["followers"], loc=add - dele, add=add, dele=dele)

# ---- render
W = 52  # chars in the info column
def row(y, key, val, cls="value"):
    keys = key.split(".")
    klen = len(key) + 1; dots = max(1, W - klen - len(val) - 3)
    k = '</tspan>.<tspan class="key">'.join(keys)
    return f'<tspan x="390" y="{y}" class="cc">. </tspan><tspan class="key">{k}</tspan>:<tspan class="cc"> {"."*dots} </tspan><tspan class="{cls}">{html.escape(val)}</tspan>'
def head(y, t): return f'<tspan x="390" y="{y}">{t}</tspan> -{"—"*(W-len(t)-2)}-—-'
def multi(y, parts):  # [(key, val), ...] on one line separated by |
    out = f'<tspan x="390" y="{y}" class="cc">. </tspan>'
    first = parts[0]; rest = parts[1:]
    used = sum(len(k) + 2 + len(v) for k, v in parts) + 3 * len(rest)
    dots = max(1, W - used - 2)
    out += f'<tspan class="key">{first[0]}</tspan>:<tspan class="cc"> {"."*dots} </tspan><tspan class="value">{first[1]}</tspan>'
    for k, v in rest: out += f' | <tspan class="key">{k}</tspan>: <tspan class="value">{v}</tspan>'
    return out
f = lambda n: f"{n:,}"
lines = [
    head(30, "jatin@verma"),
    row(50, "OS", "Linux Mint, Windows 11, Android"),
    row(70, "Uptime", up),
    row(90, "Host", "Thapar Institute of Engineering"),
    row(110, "Kernel", "Full-Stack Developer"),
    row(130, "IDE", "VSCode, Unity, Cursor"),
    f'<tspan x="390" y="150" class="cc">. </tspan>',
    row(170, "Languages.Programming", "TypeScript, C#, JS, Python"),
    row(190, "Languages.Computer", "HTML, CSS, JSON, SQL"),
    row(210, "Languages.Real", "Hindi, English"),
    f'<tspan x="390" y="230" class="cc">. </tspan>',
    row(250, "Hobbies.Software", "Game Dev, Web Templates"),
    row(270, "Hobbies.Hardware", "Gesture Control, Tinkering"),
    f'<tspan x="390" y="290" class="cc">. </tspan>',
    row(310, "Projects.Games", "spin-rumble, neon-fps, blade-tilt"),
    row(330, "Projects.Web", "PresentProof, Battle-Royale-Core"),
    row(350, "Projects.Security", "SIH Threat-Intelligence"),
    head(390, "- GitHub Stats"),
    multi(410, [("Repos", f(stats["repos"])), ("Contributed", f(stats["contrib"])), ("Stars", f(stats["stars"]))]),
    multi(430, [("Commits", f(stats["commits"])), ("Followers", f(stats["followers"]))]),
    f'<tspan x="390" y="450" class="cc">. </tspan><tspan class="key">Lines of Code on GitHub</tspan>:<tspan class="cc"> {"."*max(1, W-34-len(f(stats["loc"]))-len(f(stats["add"]))-len(f(stats["dele"])))} </tspan><tspan class="value">{f(stats["loc"])}</tspan> ( <tspan class="addColor">{f(stats["add"])}++</tspan>, <tspan class="delColor">{f(stats["dele"])}--</tspan> )',
]
ascii_art = open(os.path.join(HERE, "ascii.txt")).read().rstrip("\n").split("\n")
art = "".join(f'<tspan x="15" y="{30+i*20}">{html.escape(l)}</tspan>\n' for i, l in enumerate(ascii_art[:24]))
TH = {"dark": dict(bg="#161b22", fg="#c9d1d9", key="#ffa657", val="#a5d6ff", add="#3fb950", dele="#f85149", cc="#616e7f"),
      "light": dict(bg="#f6f8fa", fg="#24292f", key="#953800", val="#0a3069", add="#1a7f37", dele="#cf222e", cc="#c2cfde")}
for name, c in TH.items():
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,'Courier New',monospace" width="985px" height="500px" font-size="16px">
<style>@font-face{{src:local('Consolas'),local('Consolas Bold');font-family:'ConsolasFallback';font-display:swap;size-adjust:109%;}}
.key{{fill:{c["key"]}}} .value{{fill:{c["val"]}}} .addColor{{fill:{c["add"]}}} .delColor{{fill:{c["dele"]}}} .cc{{fill:{c["cc"]}}} text,tspan{{white-space:pre}}</style>
<rect width="985px" height="500px" fill="{c["bg"]}" rx="15"/>
<text x="15" y="30" fill="{c["fg"]}" class="ascii">
{art}</text>
<text x="390" y="30" fill="{c["fg"]}">
{chr(10).join(lines)}
</text>
</svg>'''
    open(os.path.join(HERE, f"{name}_mode.svg"), "w").write(svg)
print(json.dumps(stats))
