"""Generates Lotta's illustration set (flat colour, plum outlines) into src/assets/illu/.
Run: python3 tools/illu.py"""
import os, math, random

OUT = os.path.join(os.path.dirname(__file__), "..", "src", "assets", "illu")
PLUM, APRICOT, SAGE, CREAM, BLUSH = "#3a2340", "#f0a27f", "#a9bfa8", "#fbf6f0", "#f6c7b4"
INK = PLUM
SKIN = {"light": "#f6d3bb", "fair": "#eec09d", "tan": "#d59a72", "brown": "#a8694a", "deep": "#6e4330"}
HAIR = {"dark": "#2b1d22", "brown": "#6b4232", "auburn": "#a5503a", "blond": "#e2b867", "grey": "#b9b2b0", "silver": "#d9d4d2"}
S = f'stroke="{INK}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"'
S2 = S.replace('2.4', '2')
S5 = S.replace('2.4', '5')


def blob(cx, cy, r, color, seed, n=9, jitter=0.12, opacity=1):
    rnd = random.Random(seed)
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = r * (1 + rnd.uniform(-jitter, jitter))
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d = f"M{(pts[0][0]+pts[-1][0])/2:.1f},{(pts[0][1]+pts[-1][1])/2:.1f}"
    for i in range(n):
        p, q = pts[i], pts[(i + 1) % n]
        d += f" Q{p[0]:.1f},{p[1]:.1f} {(p[0]+q[0])/2:.1f},{(p[1]+q[1])/2:.1f}"
    return f'<path d="{d}Z" fill="{color}" opacity="{opacity}"/>'


def hair_back(style, c):
    if style == "long":
        return f'<path d="M58 70c-6 40 -8 78 -2 112 18 10 70 10 88 0 6-34 4-72-2-112z" fill="{c}" {S}/>'
    if style == "bob":
        return f'<path d="M56 74c-6 30-4 56 6 70 14 6 62 6 76 0 10-14 12-40 6-70z" fill="{c}" {S}/>'
    if style == "bun":
        return f'<circle cx="100" cy="34" r="20" fill="{c}" {S}/>'
    if style == "curly":
        return "".join(f'<circle cx="{x}" cy="{y}" r="17" fill="{c}" {S}/>' for x, y in
                       [(62, 80), (58, 104), (66, 126), (138, 80), (142, 104), (134, 126), (72, 56), (128, 56), (100, 46)])
    return ""


def hair_front(style, c):
    if style in ("long", "bob"):
        return f'<path d="M64 84c2-28 18-44 36-44s36 14 38 44c-14-6-26-18-30-30-8 14-24 26-44 30z" fill="{c}" {S}/>'
    if style == "bun":
        return f'<path d="M64 86c0-28 16-42 36-42s36 14 36 42c-10-14-22-22-36-22s-26 8-36 22z" fill="{c}" {S}/>'
    if style == "short":
        return f'<path d="M62 92c-4-34 14-52 38-52 26 0 42 18 38 52-6-14-12-22-20-26-12 8-34 10-56 26z" fill="{c}" {S}/>'
    if style == "curly":
        return "".join(f'<circle cx="{x}" cy="{y}" r="13" fill="{c}" {S}/>' for x, y in
                       [(74, 62), (92, 54), (110, 54), (126, 62), (66, 78), (134, 78)])
    return ""


def portrait(skin, hair, style, top, bg, seed, glasses=False, eyes="open", earring=False, accent=None):
    """200x200 bust portrait in a circle-friendly frame."""
    sk = SKIN[skin]; hc = HAIR[hair]
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img">']
    p.append(f'<rect width="200" height="200" fill="{bg}"/>')
    p.append(blob(150, 50, 34, "#ffffff", seed, opacity=0.45))
    p.append('<g transform="translate(100 112) scale(1.2) translate(-100 -100)">')
    p.append(hair_back(style, hc))
    # shoulders / top
    p.append(f'<path d="M30 206c4-38 30-58 70-58s66 20 70 58z" fill="{top}" {S}/>')
    p.append(f'<path d="M84 148c4 14 28 14 32 0" fill="none" {S}/>')
    # neck
    p.append(f'<path d="M88 124v24c6 8 18 8 24 0v-24z" fill="{sk}" {S}/>')
    # face
    p.append(f'<path d="M66 92c0-26 14-42 34-42s34 16 34 42c0 26-14 44-34 44s-34-18-34-44z" fill="{sk}" {S}/>')
    p.append(f'<ellipse cx="66" cy="98" rx="6" ry="9" fill="{sk}" {S}/><ellipse cx="134" cy="98" rx="6" ry="9" fill="{sk}" {S}/>')
    if earring:
        p.append(f'<circle cx="66" cy="112" r="3.5" fill="{APRICOT}" {S}/><circle cx="134" cy="112" r="3.5" fill="{APRICOT}" {S}/>')
    p.append(hair_front(style, hc))
    # cheeks
    p.append(f'<circle cx="80" cy="106" r="7" fill="{APRICOT}" opacity=".45"/><circle cx="120" cy="106" r="7" fill="{APRICOT}" opacity=".45"/>')
    # eyes
    if eyes == "closed":
        p.append(f'<path d="M80 95q6 5 12 0M108 95q6 5 12 0" fill="none" {S}/>')
    else:
        p.append(f'<circle cx="86" cy="95" r="3" fill="{INK}"/><circle cx="114" cy="95" r="3" fill="{INK}"/>')
        p.append(f'<path d="M80 86q6-4 12-1M108 85q6-3 12 1" fill="none" {S2}/>')
    if glasses:
        p.append(f'<circle cx="86" cy="95" r="10" fill="none" {S}/><circle cx="114" cy="95" r="10" fill="none" {S}/><path d="M96 95h8" {S}/>')
    p.append(f'<path d="M100 98q-4 10 2 12" fill="none" {S2}/>')
    p.append(f'<path d="M90 118q10 8 20 0" fill="none" {S}/>')
    if accent == "stethoscope":
        p.append(f'<path d="M80 150c-6 24 6 36 20 36s26-12 20-36" fill="none" stroke="{INK}" stroke-width="3"/><circle cx="100" cy="186" r="6" fill="{SAGE}" {S}/>')
    if accent == "collar":
        p.append(f'<path d="M70 156l30 34 30-34-12-8-18 22-18-22z" fill="#ffffff" {S}/>')
    p.append("</g></svg>")
    return "".join(p)


def spot(kind, seed):
    """120x120 spot illustration on an organic blob."""
    bgc = {"aerztlich": BLUSH, "training": "#dfe9dd", "lifestyle": "#e9e1ef", "tracking": BLUSH,
           "ernaehrung": "#dfe9dd", "mind": "#e9e1ef", "community": BLUSH, "gespraech": BLUSH,
           "plan": "#dfe9dd", "begleitung": "#e9e1ef"}[kind]
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" aria-hidden="true">', blob(60, 62, 48, bgc, seed)]
    if kind == "aerztlich":
        p.append(f'<rect x="34" y="30" width="52" height="64" rx="8" fill="#fff" {S}/><rect x="48" y="24" width="24" height="12" rx="4" fill="{APRICOT}" {S}/>'
                 f'<path d="M60 50v20M50 60h20" stroke="{APRICOT}" stroke-width="6" stroke-linecap="round"/><path d="M44 82h32" {S}/>')
    elif kind == "training":
        p.append(f'<rect x="22" y="48" width="12" height="26" rx="4" fill="{PLUM}" {S}/><rect x="86" y="48" width="12" height="26" rx="4" fill="{PLUM}" {S}/>'
                 f'<rect x="34" y="54" width="8" height="14" rx="3" fill="{APRICOT}" {S}/><rect x="78" y="54" width="8" height="14" rx="3" fill="{APRICOT}" {S}/><path d="M42 61h36" {S5}/>')
    elif kind == "lifestyle":
        p.append(f'<path d="M78 30a32 32 0 1 0 14 48 26 26 0 0 1-14-48z" fill="{APRICOT}" {S}/><circle cx="34" cy="34" r="3" fill="{PLUM}"/><circle cx="92" cy="28" r="2.5" fill="{PLUM}"/><path d="M28 90l4-6 4 6" fill="none" {S}/>')
    elif kind == "tracking":
        p.append(f'<rect x="28" y="30" width="64" height="58" rx="8" fill="#fff" {S}/><path d="M36 74l14-14 10 10 22-22" fill="none" stroke="{APRICOT}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="82" cy="48" r="4" fill="{PLUM}"/>')
    elif kind == "ernaehrung":
        p.append(f'<path d="M30 62h60c0 18-14 30-30 30S30 80 30 62z" fill="#fff" {S}/><circle cx="48" cy="56" r="9" fill="{APRICOT}" {S}/><path d="M62 58c4-14 16-18 22-16-2 10-10 18-22 16z" fill="{SAGE}" {S}/><circle cx="70" cy="60" r="5" fill="#c55a5a" {S}/>')
    elif kind == "mind":
        p.append(f'<path d="M60 94c-22-12-34-26-34-40a16 16 0 0 1 34-6 16 16 0 0 1 34 6c0 14-12 28-34 40z" fill="{APRICOT}" {S}/><path d="M46 60q14 10 28 0" fill="none" {S}/>')
    elif kind == "community":
        p.append(f'<circle cx="42" cy="48" r="11" fill="{SKIN["tan"]}" {S}/><circle cx="78" cy="48" r="11" fill="{SKIN["light"]}" {S}/><circle cx="60" cy="42" r="11" fill="{SKIN["fair"]}" {S}/>'
                 f'<path d="M24 92c0-14 8-24 18-24s16 6 18 12c2-6 8-12 18-12s18 10 18 24z" fill="{SAGE}" {S}/><path d="M42 92c0-14 8-26 18-26s18 12 18 26z" fill="{APRICOT}" {S}/>')
    elif kind == "gespraech":
        p.append(f'<rect x="20" y="30" width="54" height="36" rx="12" fill="#fff" {S}/><path d="M34 66l-4 12 14-12" fill="#fff" {S}/>'
                 f'<rect x="50" y="52" width="52" height="34" rx="12" fill="{APRICOT}" {S}/><path d="M88 86l4 10-14-10" fill="{APRICOT}" {S}/><path d="M32 44h28M32 52h18" {S}/>')
    elif kind == "plan":
        p.append(f'<rect x="30" y="24" width="60" height="74" rx="8" fill="#fff" {S}/>' + "".join(
            f'<rect x="40" y="{y}" width="10" height="10" rx="3" fill="{c}" {S2}/><path d="M58 {y+5}h22" {S}/>'
            for y, c in [(38, SAGE), (56, APRICOT), (74, "#fff")]))
    elif kind == "begleitung":
        p.append(f'<path d="M24 84c16-30 30-10 44-34s20-18 28-24" fill="none" stroke="{PLUM}" stroke-width="3" stroke-dasharray="2 7" stroke-linecap="round"/>'
                 f'<circle cx="24" cy="84" r="7" fill="{SAGE}" {S}/><circle cx="62" cy="54" r="7" fill="{APRICOT}" {S}/><path d="M96 14v26M96 14l18 7-18 7" fill="{APRICOT}" {S}/>')
    p.append("</svg>")
    return "".join(p)


def hero():
    """Large hero illustration: woman with tea in an arch, plants, sun."""
    sk, hc = SKIN["fair"], HAIR["auburn"]
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 560" role="img" aria-label="Illustration einer Frau mit Tasse, entspannt und zuversichtlich">']
    p.append(f'<path d="M60 560V250C60 130 150 40 260 40s200 90 200 210v310z" fill="{BLUSH}"/>')
    p.append(f'<circle cx="372" cy="150" r="46" fill="{APRICOT}"/>')
    p.append(blob(110, 470, 70, "#dfe9dd", 3))
    # plant left
    for i, (x, y, r) in enumerate([(84, 420, -30), (96, 380, -10), (70, 360, -45), (112, 340, 10)]):
        p.append(f'<ellipse cx="{x}" cy="{y}" rx="14" ry="34" transform="rotate({r} {x} {y})" fill="{SAGE}" {S}/>')
    p.append(f'<path d="M98 470c-2-40-4-80 4-120" fill="none" {S}/>')
    # hair back
    p.append(f'<path d="M190 200c-16 80-20 150-6 210 40 20 120 20 160 0 12-60 10-130-6-210z" fill="{hc}" {S}/>')
    # body
    p.append(f'<path d="M120 560c6-90 60-140 150-140s144 50 150 140z" fill="{PLUM}" {S}/>')
    p.append(f'<path d="M226 424c10 30 78 30 88 0" fill="none" stroke="{CREAM}" stroke-width="3"/>')
    # neck + face
    p.append(f'<path d="M244 330v80c14 18 38 18 52 0v-80z" fill="{sk}" {S}/>')
    p.append(f'<path d="M200 248c0-62 30-98 70-98s70 36 70 98c0 60-30 100-70 100s-70-40-70-100z" fill="{sk}" {S}/>')
    p.append(f'<path d="M198 236c4-64 36-96 72-96s70 30 72 96c-26-10-50-34-58-58-14 30-46 52-86 58z" fill="{hc}" {S}/>')
    p.append(f'<path d="M232 262q10 8 20 0M288 262q10 8 20 0" fill="none" {S}/>')
    p.append(f'<circle cx="230" cy="290" r="13" fill="{APRICOT}" opacity=".45"/><circle cx="310" cy="290" r="13" fill="{APRICOT}" opacity=".45"/>')
    p.append(f'<path d="M270 268q-8 20 4 24" fill="none" {S}/><path d="M252 310q18 14 36 0" fill="none" {S}/>')
    p.append(f'<circle cx="200" cy="280" r="6" fill="{APRICOT}" {S}/>')
    # hands with mug
    p.append(f'<path d="M200 560c0-40 20-70 50-84" fill="none" {S}/>')
    p.append(f'<rect x="236" y="452" width="68" height="70" rx="12" fill="{CREAM}" {S}/><path d="M304 470c22 0 22 34 0 34" fill="none" {S}/>')
    p.append(f'<path d="M256 440c-6-10 6-16 0-28M282 440c-6-10 6-16 0-28" fill="none" stroke="{PLUM}" stroke-width="2.4" stroke-linecap="round" opacity=".6"/>')
    p.append(f'<path d="M226 520c-4-26 6-48 22-52 8 4 8 40 0 56zM314 520c4-26-6-48-22-52-8 4-8 40 0 56z" fill="{sk}" {S}/>')
    # sparkles
    for x, y in [(430, 260), (150, 140), (420, 400)]:
        p.append(f'<path d="M{x} {y-12}v24M{x-12} {y}h24" {S}/>')
    p.append("</svg>")
    return "".join(p)


def write(name, svg):
    with open(os.path.join(OUT, name + ".svg"), "w") as f:
        f.write(svg)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    write("hero", hero())
    people = {
        "lead": ("fair", "brown", "bob", "#ffffff", "#dfe9dd", 1, False, "open", True, "collar"),
        "board1": ("brown", "dark", "curly", SAGE, BLUSH, 2, False, "open", True, None),
        "board2": ("light", "blond", "bun", APRICOT, "#dfe9dd", 3, False, "open", False, None),
        "board3": ("fair", "grey", "short", PLUM, "#e9e1ef", 4, True, "open", False, None),
        "story1": ("tan", "dark", "long", SAGE, BLUSH, 5, False, "closed", True, None),
        "story2": ("light", "auburn", "bob", PLUM, "#dfe9dd", 6, False, "open", False, None),
        "story3": ("fair", "silver", "short", APRICOT, "#e9e1ef", 7, True, "open", True, None),
    }
    for name, a in people.items():
        write(name, portrait(*a[:6], glasses=a[6], eyes=a[7], earring=a[8], accent=a[9]))
    for i, k in enumerate(["aerztlich", "training", "lifestyle", "tracking", "ernaehrung", "mind", "community", "gespraech", "plan", "begleitung"]):
        write("spot-" + k, spot(k, 10 + i))
    print("ok", len(os.listdir(OUT)))
