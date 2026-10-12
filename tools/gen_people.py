"""Writes the character portraits. Run: python3 tools/gen_people.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import people as P

SK = {"light": "#f6d3bb", "fair": "#eec09d", "tan": "#d59a72", "brown": "#a8694a"}
HC = {"dark": "#2b1d22", "brown": "#6b4232", "auburn": "#a5503a", "blond": "#e2b867", "grey": "#b9b2b0", "silver": "#d9d4d2"}
BL, SG, LV = "#f6c7b4", "#dfe9dd", "#e9e1ef"
OUT = os.path.join(os.path.dirname(__file__), "..", "src", "assets", "illu")
SPEC = {
    "lead": dict(skin=SK["fair"], hair_c=HC["brown"], style="bob", top="#ffffff", bg=SG, earring=True, prop_kind="stethoscope", collar=True, tilt=-3),
    "board1": dict(skin=SK["brown"], hair_c=HC["dark"], style="curly", top="#a9bfa8", bg=BL, eyes="smile", mouth="open", earring=True, tilt=4),
    "board2": dict(skin=SK["light"], hair_c=HC["blond"], style="bun", top="#f0a27f", bg=SG, tilt=-4),
    "board3": dict(skin=SK["fair"], hair_c=HC["grey"], style="short", top="#3a2340", bg=LV, older=True, glasses=True, tilt=3),
    "story1": dict(skin=SK["tan"], hair_c=HC["dark"], style="long", top="#a9bfa8", bg=BL, eyes="closed", earring=True, prop_kind="tea", tilt=-5),
    "story2": dict(skin=SK["light"], hair_c=HC["auburn"], style="wavy", top="#3a2340", bg=SG, mouth="open", prop_kind="book", tilt=4),
    "phase1": dict(skin=SK["brown"], hair_c=HC["dark"], style="bob", top="#f0a27f", bg=BL, bare=True, eyes="open", mouth="smile", earring=True, tilt=-3),
    "phase2": dict(skin=SK["light"], hair_c=HC["silver"], style="bun", top="#8fae8d", bg=SG, bare=True, older=True, glasses=True, eyes="smile", tilt=3),
    "story3": dict(skin=SK["fair"], hair_c=HC["silver"], style="short", top="#f0a27f", bg=LV, eyes="smile", mouth="open", older=True, glasses=True, earring=True, prop_kind="dumbbell", tilt=-3),
}
for k in ["story2", "story3", "lead", "board1"]:
    SPEC[k + "-bare"] = dict(SPEC[k], bare=True)
for name, a in SPEC.items():
    with open(os.path.join(OUT, name + ".svg"), "w") as f:
        f.write(P.portrait(name, **a))
print("ok")

# Hero scene: arch, sun, moon, botanicals and a large character with tea.
import re
fig = P.portrait("hero-fig", skin="#eec09d", hair_c="#a5503a", style="long", top="#3a2340", bg="#fff",
                 eyes="closed", earring=True, prop_kind="tea", tilt=-4, bare=True)
fig = re.sub(r'^<svg[^>]*>', '<svg x="40" y="118" width="440" height="462" viewBox="0 0 200 210" overflow="visible">', fig)
leaf = lambda x, y, r, c: f'<ellipse cx="{x}" cy="{y}" rx="16" ry="40" transform="rotate({r} {x} {y})" fill="{c}"/><path d="M{x} {y+36}V{y-36}" transform="rotate({r} {x} {y})" stroke="#3a2340" stroke-width="1.6" opacity=".35"/>'
hero = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 560" role="img" aria-label="Illustration einer Frau mit einer Tasse Tee, entspannt und zuversichtlich">',
        '<defs>' + P.grain("hg") + '<clipPath id="arch"><path d="M40 560V260C40 136 138 40 260 40s220 96 220 220v300z"/></clipPath></defs>',
        '<path d="M40 560V260C40 136 138 40 260 40s220 96 220 220v300z" fill="#f6c7b4"/>',
        '<path d="M40 560V260C40 136 138 40 260 40s220 96 220 220v300z" fill="#f6c7b4" filter="url(#hg)"/>',
        '<g clip-path="url(#arch)"><circle cx="352" cy="150" r="52" fill="#f0a27f"/><path d="M40 470c90-40 170-20 260-50s140-10 180 0v190H40z" fill="#e9d2c4"/></g>',
        '<path d="M120 120a26 26 0 1 0 22 40 20 20 0 0 1-22-40z" fill="#fbf6f0"/>',
        leaf(60, 430, -28, "#a9bfa8"), leaf(92, 400, -6, "#8fae8d"), leaf(48, 372, -44, "#a9bfa8"), leaf(470, 420, 26, "#a9bfa8"), leaf(450, 380, 8, "#8fae8d"),
        '<path d="M78 560c-4-60 0-120 14-180M462 560c2-50-2-100-12-150" stroke="#3a2340" stroke-width="2" fill="none" stroke-linecap="round"/>',
        "<g clip-path=\"url(#arch)\">" + fig + "</g>",
        '<g stroke="#3a2340" stroke-width="2.2" stroke-linecap="round"><path d="M420 250v22M409 261h22"/><path d="M180 96v16M172 104h16"/></g>',
        '</svg>']
with open(os.path.join(OUT, "hero.svg"), "w") as f:
    f.write("".join(hero))
print("hero ok")
