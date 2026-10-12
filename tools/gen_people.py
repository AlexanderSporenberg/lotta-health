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
base = dict(SPEC["story1"], bare=True)
SPEC["journey1"] = dict(base, eyes="open", mouth="open", prop_kind=None, tilt=-3)
SPEC["journey2"] = dict(base, eyes="open", mouth="smile", prop_kind="book", tilt=2)
SPEC["journey3"] = dict(base, eyes="smile", mouth="open", prop_kind=None, tilt=-2)
for k in ["story2", "story3", "lead", "board1", "board2", "board3", "story1"]:
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
hero = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 560" overflow="visible" role="img" aria-label="Illustration einer Frau mit einer Tasse Tee im Sessel am Fenster, entspannt und zuversichtlich">',
        '<defs>' + P.grain("hg") + '<clipPath id="arch"><path d="M40 560V260C40 136 138 40 260 40s220 96 220 220v300z"/></clipPath></defs>',
        '<path d="M40 560V260C40 136 138 40 260 40s220 96 220 220v300z" fill="#f6c7b4"/>',
        '<path d="M40 560V260C40 136 138 40 260 40s220 96 220 220v300z" fill="#f6c7b4" filter="url(#hg)"/>',
        '<g clip-path="url(#arch)"><circle cx="352" cy="150" r="52" fill="#f0a27f"/><path d="M40 470c90-40 170-20 260-50s140-10 180 0v190H40z" fill="#e9d2c4"/></g>',
        '<path d="M120 120a26 26 0 1 0 22 40 20 20 0 0 1-22-40z" fill="#fbf6f0"/>',
        leaf(60, 430, -28, "#a9bfa8"), leaf(92, 400, -6, "#8fae8d"), leaf(48, 372, -44, "#a9bfa8"),
        '<path d="M78 560c-4-60 0-120 14-180" stroke="#3a2340" stroke-width="2" fill="none" stroke-linecap="round"/>',
        # window mullions in the arch, armchair behind the figure, side table with plant and book
        '<g clip-path="url(#arch)"><path d="M260 40v250M70 200h380" stroke="#fbf6f0" stroke-width="10" opacity=".55"/>'
        '<rect x="40" y="290" width="440" height="14" fill="#fbf6f0" opacity=".7"/>'
        '<path d="M92 560V380c0-70 60-110 168-110s168 40 168 110v180z" fill="#8fae8d" stroke="#3a2340" stroke-width="2"/>'
        '<path d="M92 560V380c0-70 60-110 168-110s168 40 168 110v180z" fill="#8fae8d" filter="url(#hg)"/><path d="M128 300c-6 30-6 70-4 110M392 300c6 30 6 70 4 110" stroke="#3a2340" stroke-width="1.6" fill="none" opacity=".3"/>'
        '</g>',
        "<g clip-path=\"url(#arch)\">" + fig + "</g>",
        '<g clip-path="url(#arch)"><rect x="76" y="456" width="84" height="104" rx="30" fill="#a9bfa8" stroke="#3a2340" stroke-width="2"/>'
        '<rect x="360" y="456" width="84" height="104" rx="30" fill="#a9bfa8" stroke="#3a2340" stroke-width="2"/></g>',
        '<rect x="400" y="470" width="96" height="10" rx="5" fill="#3a2340"/><path d="M412 480v80M484 480v80" stroke="#3a2340" stroke-width="4"/>',
        '<path d="M418 470l6-30h44l6 30z" fill="#f0a27f" stroke="#3a2340" stroke-width="2"/>',
        leaf(436, 410, -20, "#8fae8d"), leaf(456, 404, 18, "#a9bfa8"), leaf(446, 396, 0, "#8fae8d"),
        '<rect x="404" y="456" width="40" height="8" rx="2" fill="#efe7f3" stroke="#3a2340" stroke-width="1.6" transform="rotate(-4 424 460)"/>',
        '<g stroke="#3a2340" stroke-width="2.2" stroke-linecap="round"><path d="M420 250v22M409 261h22"/><path d="M180 96v16M172 104h16"/></g>',
        '</svg>']
with open(os.path.join(OUT, "hero.svg"), "w") as f:
    f.write("".join(hero))
print("hero ok")
