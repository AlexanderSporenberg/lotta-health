"""Second-generation character portraits: no outline on skin, varied faces, props, grain.
Imported by tools/illu.py."""
import math

PLUM, APRICOT, SAGE, CREAM = "#3a2340", "#f0a27f", "#a9bfa8", "#fbf6f0"
LINE = 'stroke-linecap="round" stroke-linejoin="round" fill="none"'
import re as _re


def _fix(svg):
    """Give stroked line elements a default plum stroke when none was set."""
    return _re.sub(r'<(path|rect|circle|ellipse)([^>]*stroke-linecap[^>]*)/>',
                   lambda m: m.group(0) if 'stroke="' in m.group(2) else f'<{m.group(1)}{m.group(2)} stroke="{PLUM}"/>', svg)


def grain(id_):
    return (f'<filter id="{id_}" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/>'
            f'<feColorMatrix values="0 0 0 0 .23  0 0 0 0 .14  0 0 0 0 .25  0 0 0 .09 0"/><feComposite in2="SourceGraphic" operator="in"/></filter>')


def shade(hex_, f):
    h = hex_.lstrip("#"); r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(c * f))) for c in (r, g, b))


def hair_shape(style, c, part):
    dk = shade(c, .8)
    if part == "back":
        return {
            "long": f'<path d="M54 74c-10 34-12 74-4 110 22 12 78 12 100 0 8-36 6-76-4-110-20-26-72-26-92 0z" fill="{c}"/>',
            "bob": f'<path d="M52 78c-8 26-6 50 4 64 20 10 68 10 88 0 10-14 12-38 4-64-18-30-78-30-96 0z" fill="{c}"/>',
            "bun": f'<circle cx="112" cy="30" r="19" fill="{c}"/><path d="M104 22q8-6 16 0" {LINE} stroke="{dk}" stroke-width="2"/>',
            "curly": "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x, y, r in
                             [(58, 82, 18), (54, 108, 17), (62, 130, 15), (142, 82, 18), (146, 108, 17), (138, 130, 15), (68, 56, 18), (132, 56, 18), (100, 42, 20), (84, 46, 16), (116, 46, 16)]),
            "short": "", "wavy": f'<path d="M52 80c-14 30-6 54-12 80 30 16 90 16 120 0-6-26 2-50-12-80-20-30-76-30-96 0z" fill="{c}"/>',
        }[style]
    return {
        "long": f'<path d="M62 92c0-34 18-52 40-52 24 0 40 18 40 50-18-4-34-16-42-32-6 16-20 28-38 34z" fill="{c}"/><path d="M100 46c-4 10-12 20-24 26" {LINE} stroke="{dk}" stroke-width="1.6"/>',
        "bob": f'<path d="M60 96c-2-36 18-56 42-56s42 20 40 56c-6-14-14-26-26-30-18 8-38 12-56 30z" fill="{c}"/><path d="M118 52c6 8 10 18 12 30" {LINE} stroke="{dk}" stroke-width="1.6"/>',
        "bun": f'<path d="M64 88c0-28 16-44 38-44s38 16 38 44c-10-16-24-24-38-24s-28 8-38 24z" fill="{c}"/><path d="M84 52q16-6 32 2" {LINE} stroke="{dk}" stroke-width="1.6"/>',
        "curly": "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x, y, r in [(76, 60, 13), (92, 52, 13), (110, 52, 13), (126, 60, 13), (66, 74, 11), (136, 74, 11)]),
        "short": f'<path d="M62 94c-6-36 14-56 40-56 28 0 44 20 38 56-4-12-10-22-18-26-14 10-38 8-60 26z" fill="{c}"/><path d="M80 52q14 10 34 4" {LINE} stroke="{dk}" stroke-width="1.6"/>',
        "wavy": f'<path d="M60 96c-2-38 18-58 42-58s44 20 40 58c-4-6-10-20-18-28-8 12-24 16-34 14-10 6-22 8-30 14z" fill="{c}"/>',
    }[style]


def face(skin, eyes, mouth, older, brows_c):
    ck = shade(skin, .9)
    p = [f'<path d="M66 94c0-28 15-44 36-44s34 16 34 44c0 28-14 46-35 46S66 122 66 94z" fill="{skin}"/>',
         f'<path d="M70 112c8 18 20 26 32 26 8 0 16-4 22-10-10 2-30 0-54-16z" fill="{ck}" opacity=".35"/>',
         f'<ellipse cx="66" cy="100" rx="5.5" ry="8" fill="{skin}"/><ellipse cx="136" cy="100" rx="5.5" ry="8" fill="{skin}"/>',
         f'<ellipse cx="82" cy="110" rx="7.5" ry="5" fill="{APRICOT}" opacity=".4"/><ellipse cx="122" cy="110" rx="7.5" ry="5" fill="{APRICOT}" opacity=".4"/>']
    if eyes == "smile":
        p.append(f'<path d="M82 98q5-5 10 0M112 98q5-5 10 0" {LINE} stroke-width="2.4"/>')
    elif eyes == "closed":
        p.append(f'<path d="M81 97q6 5 12 0M111 97q6 5 12 0" {LINE} stroke-width="2.2"/><path d="M81 97l-3-2M123 97l3-2" {LINE} stroke-width="1.6"/>')
    else:
        p.append(f'<ellipse cx="87" cy="97" rx="3.2" ry="3.8" fill="{PLUM}"/><ellipse cx="117" cy="97" rx="3.2" ry="3.8" fill="{PLUM}"/>'
                 f'<circle cx="88.2" cy="95.8" r="1" fill="#fff"/><circle cx="118.2" cy="95.8" r="1" fill="#fff"/>')
    p.append(f'<path d="M79 87q8-5 15-1M110 86q7-4 15 1" {LINE} stroke="{brows_c}" stroke-width="2.6"/>')
    p.append(f'<path d="M102 98q-5 11 1 13" {LINE} stroke="{shade(skin, .7)}" stroke-width="1.8"/>')
    if mouth == "open":
        p.append(f'<path d="M92 119q10 10 20 0z" fill="{PLUM}"/><path d="M94 120q8 3 16 0" stroke="#fff" stroke-width="2" fill="none"/>')
    else:
        p.append(f'<path d="M92 120q10 7 20-1" {LINE} stroke-width="2.2"/>')
    if older:
        p.append(f'<path d="M76 101l-4 2M128 101l4 2M86 116q-2 6 2 9M118 116q2 6-2 9" {LINE} stroke="{shade(skin, .72)}" stroke-width="1.4"/>')
    return "".join(p)


def prop(kind, skin, top):
    if kind == "tea":
        hand = shade(skin, .96)
        return (f'<g transform="translate(0 -6)"><path d="M84 160h34v30c0 9-7 14-17 14s-17-5-17-14z" fill="{CREAM}" stroke="{PLUM}" stroke-width="2"/>'
                f'<ellipse cx="101" cy="160" rx="17" ry="4.5" fill="{shade(CREAM, .86)}" stroke="{PLUM}" stroke-width="2"/>'
                f'<path d="M89 176h24" stroke="{APRICOT}" stroke-width="5" stroke-linecap="round"/>'
                f'<path d="M66 214c2-16 8-30 22-34 6-2 10 4 8 10l-4 12c-2 6-4 10-4 14z" fill="{hand}" stroke="none"/>'
                f'<path d="M136 214c-2-16-8-30-22-34-6-2-10 4-8 10l4 12c2 6 4 10 4 14z" fill="{hand}" stroke="none"/>'
                f'<path d="M86 184q-6 2-6 8M116 184q6 2 6 8" {LINE} stroke="{shade(skin, .75)}" stroke-width="1.4"/></g>')
    if kind == "book":
        return (f'<path d="M70 200l30-34 30 34z" fill="{skin}"/><path d="M66 176l34 8 34-8v24l-34 8-34-8z" fill="{APRICOT}" stroke="{PLUM}" stroke-width="2"/>'
                f'<path d="M100 184v24" stroke="{PLUM}" stroke-width="2"/>')
    if kind == "dumbbell":
        return (f'<path d="M126 200c0-18 4-30 12-34" {LINE} stroke-width="0"/><rect x="128" y="150" width="10" height="22" rx="3" fill="{PLUM}"/><rect x="152" y="150" width="10" height="22" rx="3" fill="{PLUM}"/>'
                f'<path d="M138 161h14" stroke="{PLUM}" stroke-width="4"/><ellipse cx="145" cy="168" rx="11" ry="9" fill="{skin}"/>')
    if kind == "stethoscope":
        return (f'<path d="M82 150c-8 24 4 40 18 40s26-16 18-40" fill="none" stroke="{PLUM}" stroke-width="2.6"/>'
                f'<circle cx="100" cy="190" r="6" fill="{SAGE}" stroke="{PLUM}" stroke-width="2"/>')
    return ""


def portrait(name, skin, hair_c, style, top, bg, eyes="open", mouth="smile", older=False, glasses=False,
             earring=False, prop_kind=None, tilt=0, collar=False, bare=False):
    gid = f"g-{name}"
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 210" role="img"><defs>{grain(gid)}</defs>',
         "" if bare else f'<circle cx="100" cy="104" r="92" fill="{bg}"/><circle cx="100" cy="104" r="92" fill="{bg}" filter="url(#{gid})"/>',
         "" if bare else f'<path d="M150 40a30 30 0 0 1 22 22" {LINE} stroke="#fff" stroke-width="6" opacity=".6"/>',
         f'<g transform="rotate({tilt} 100 120)">', hair_shape(style, hair_c, "back"),
         f'<path d="M26 240c0-58 32-92 74-92s74 34 74 92z" fill="{top}" stroke="{PLUM}" stroke-width="2"/>',
         f'<path d="M88 126v22c6 10 20 10 26 0v-22z" fill="{shade(skin, .9)}" stroke="none"/>']
    if collar:
        p.append(f'<path d="M72 154l28 30 28-30-10-8-18 20-18-20z" fill="#fff" stroke="{PLUM}" stroke-width="2"/>')
    else:
        p.append(f'<path d="M86 150q14 14 30 0" {LINE} stroke-width="2"/>')
    p.append(prop(prop_kind, skin, top))
    p.append(face(skin, eyes, mouth, older, shade(hair_c, .7) if hair_c not in ("#b9b2b0", "#d9d4d2") else "#8a8180"))
    if earring:
        p.append(f'<circle cx="66" cy="112" r="3.2" fill="{APRICOT}"/><circle cx="136" cy="112" r="3.2" fill="{APRICOT}"/>')
    p.append(hair_shape(style, hair_c, "front"))
    if glasses:
        p.append(f'<rect x="76" y="89" width="22" height="16" rx="7" {LINE} stroke-width="2.2"/><rect x="106" y="89" width="22" height="16" rx="7" {LINE} stroke-width="2.2"/><path d="M98 96h8" {LINE} stroke-width="2.2"/>')
    p.append("</g></svg>")
    return _fix("".join(p))
