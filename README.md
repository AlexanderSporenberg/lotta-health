# Lotta Health website

Marketing site for Lotta Health ("Frag Lotte"), a digital companion for perimenopause and menopause.
Page structure and feature set are modeled on frieda.health; all copy, design and assets are original.

## Run

```bash
npm run build   # builds src/ into dist/
npm run check   # build, then check internal links, anchors, no en/em dashes
npm run serve   # http://localhost:8080
```

No dependencies. Plain HTML, CSS and a small vanilla JS file.

## Structure

- `src/partials/`: head, header, footer, shared by every page
- `src/pages/`: one file per page; first line is a meta comment (`title | description | nav`)
- `src/assets/`: styles, `main.js` (mobile nav, waitlist form, symptom check), logo SVGs

| Page | Purpose |
| --- | --- |
| `index.html` | Hero with "Frag Lotte" chat, symptoms, 3 steps, features, why, on prescription, FAQ, waitlist |
| `symptom-check.html` | 11-question check, runs fully in the browser, nothing stored |
| `wechseljahre.html` | Knowledge: phases, typical symptoms (anchor per symptom), when to see a doctor |
| `programm.html` | The 12-week program and its building blocks |
| `auf-rezept.html` | Planned DiGA flow: prescription, health insurer, activation code |
| `fachkreise.html` | Info for doctors |
| `ueber-uns.html`, `faq.html`, `impressum.html`, `datenschutz.html`, `404.html` | |

## Open before launch

Yellow `todo` markers on the pages show every placeholder: legal details (Impressum, Datenschutz),
DiGA status, price, statistics sources, medical reviewer, team. The waitlist form has no backend yet,
and Google Fonts should be self-hosted for GDPR.
