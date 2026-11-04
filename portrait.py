import cv2, numpy as np, html
from PIL import Image
RAMP = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
def load(path, box=None):
    im = Image.open(path).convert("RGBA")
    if box: im = im.crop(box)
    a = np.array(im).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3] / 255
    return rgb, al
def lum(rgb, al, clahe=True):
    g = cv2.cvtColor(rgb.astype(np.uint8), cv2.COLOR_RGB2GRAY)
    if clahe: g = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(6, 6)).apply(g)
    return g.astype(np.float32) / 255
def grid(x, cols, rows):
    return cv2.resize(x, (cols, rows), interpolation=cv2.INTER_AREA)
def ascii_art(rgb, al, cols=88, rows=60, edges=False, invert=False):
    g = lum(rgb, al)
    if edges:
        e = cv2.Canny((g * 255).astype(np.uint8), 60, 140).astype(np.float32) / 255
        e = cv2.dilate(e, np.ones((2, 2)))
        g = np.clip(g + 0.0, 0, 1); E = grid(e, cols, rows)
    G = grid(g, cols, rows); A = grid(al, cols, rows)
    if invert: G = 1 - G
    out = []
    for y in range(rows):
        r = ""
        for x in range(cols):
            if A[y, x] < .4: r += " "; continue
            if edges and E[y, x] > .35: r += "#" if not invert else "@"; continue
            r += RAMP[1 + int(G[y, x] * (len(RAMP) - 2))]
        out.append(r)
    return out
def braille(rgb, al, cols=88, rows=60, invert=False):
    g = lum(rgb, al); W, H = cols * 2, rows * 4
    G = cv2.resize(g, (W, H), interpolation=cv2.INTER_AREA); A = cv2.resize(al, (W, H))
    if invert: G = 1 - G
    G = G.copy()
    for y in range(H):              # Floyd-Steinberg
        for x in range(W):
            o = G[y, x]; n = 1.0 if o > .5 else 0.0; G[y, x] = n; e = o - n
            if x + 1 < W: G[y, x + 1] += e * 7 / 16
            if y + 1 < H:
                if x > 0: G[y + 1, x - 1] += e * 3 / 16
                G[y + 1, x] += e * 5 / 16
                if x + 1 < W: G[y + 1, x + 1] += e * 1 / 16
    bits = [(0, 0, 0x01), (0, 1, 0x02), (0, 2, 0x04), (1, 0, 0x08), (1, 1, 0x10), (1, 2, 0x20), (0, 3, 0x40), (1, 3, 0x80)]
    out = []
    for cy in range(rows):
        r = ""
        for cx in range(cols):
            v = 0
            for dx, dy, b in bits:
                yy, xx = cy * 4 + dy, cx * 2 + dx
                if A[yy, xx] > .4 and G[yy, xx] > .5: v |= b
            r += chr(0x2800 + v) if v else " "
        out.append(r)
    return out
def colors(rgb, al, cols, rows, theme):
    C = cv2.resize(rgb, (cols, rows), interpolation=cv2.INTER_AREA)
    if theme == "dark": C = np.clip(C * 1.25 + 30, 0, 255)
    else: C = np.clip(C * 0.7, 0, 200)
    return (C // 16 * 16 + 8).astype(int)
def to_svg_tspans(lines, x0, y0, width, lh, fs, cols=None, default="#c9d1d9"):
    out = []
    for y, l in enumerate(lines):
        if cols is None:
            body = html.escape(l)
        else:
            body = ""; run = ""; cur = None
            for x, ch in enumerate(l):
                c = "#%02x%02x%02x" % tuple(cols[y, x]) if ch != " " else cur
                if c != cur and run:
                    body += f'<tspan fill="{cur}">{html.escape(run)}</tspan>' if cur else html.escape(run); run = ""
                cur = c; run += ch
            if run: body += f'<tspan fill="{cur}">{html.escape(run)}</tspan>' if cur else html.escape(run)
        out.append(f'<text x="{x0}" y="{y0 + y*lh}" font-size="{fs}" textLength="{width}" lengthAdjust="spacingAndGlyphs" fill="{default}" xml:space="preserve">{body}</text>')
    return "\n".join(out)
def colors2(rgb, al, cols, rows, theme):
    C = cv2.resize(rgb, (cols, rows), interpolation=cv2.INTER_AREA).astype(np.uint8)
    hsv = cv2.cvtColor(C, cv2.COLOR_RGB2HSV).astype(np.float32)
    if theme == "dark": hsv[..., 2] = 120 + hsv[..., 2] * 0.55; hsv[..., 1] *= 1.2
    else: hsv[..., 2] = 25 + hsv[..., 2] * 0.45; hsv[..., 1] *= 1.3
    hsv = np.clip(hsv, 0, 255).astype(np.uint8)
    C = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB).astype(int)
    return C // 12 * 12 + 6
def braille_edges(rgb, al, cols=88, rows=60, invert=False):
    g = lum(rgb, al); e = cv2.Canny((g*255).astype(np.uint8), 50, 130).astype(np.float32)/255
    k = rgb.copy(); 
    g2 = np.clip(g + (e * (-0.6 if not invert else 0.6)), 0, 1)
    rgb2 = np.dstack([g2*255]*3)
    return braille(rgb2, al, cols, rows, invert)
