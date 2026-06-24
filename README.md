# gut-feeling

A scroll-driven data visualization on gut health during menopause.

> *"Your body is sending signals."*

Built as a single file — `flora.html` — with embedded CSS and JavaScript. No build step.

## Local preview

Open `flora.html` in your browser, or:

```bash
python -m http.server 8000
# visit http://localhost:8000/flora
```

## Design system

### Fonts

All body copy uses **Source Serif Pro** in exactly two styles:

- **Bold** — display / large lines
- **Italic** — small lines (e.g. science notes, footer)

No other typefaces for body copy. All text is **black** (`#000`).

### Typography

Poetry-style rules apply to all copy across every section:

- always lowercase
- a normal word space before sentence-ending periods (e.g. `themselves .`, not `themselves.`)
- spaced punctuation elsewhere where needed (e.g. `speaking ;`, `says :`)
- text is never shown in boxes or plates — plain on the canvas

### Particles

Flower glyphs only (✿ ❀ ✾ etc.), not spheres or tiles.

### Color

Warm park-inspired palette — see `PALETTE` in `flora.html`.

## Deployment

Pushes to `main` deploy to **Vercel** automatically.

- **Live site:** [https://trust-your-gut-feeling.vercel.app/flora](https://trust-your-gut-feeling.vercel.app/flora) (`/` redirects here)
- **Preview deploys:** PRs and non-`main` branches get their own Vercel preview URL

## Project structure

```
gut-feeling/
├── flora.html    # Deployed site (HTML + embedded CSS/JS)
├── index.html    # Maddi's working copy during integration
├── vercel.json   # Vercel config (root → /flora)
├── .gitignore
└── README.md
```

## Working together

### Section ownership

- **Madeleine** — header through "but, these signals are invisible." (S0 → S2)
- **Catherine** — through "More than a billion women will be in menopause globally by 2030." (S3)
- **Katarina** — storm through garden (S4 → end)

### Workflow

1. **Pull before you start:** `git pull origin main`
2. **Work on your own branch:** `name/feature` convention (e.g. `maddi/header-landing`)
3. **Commit often** with clear messages
4. **Push and open a PR** to `main` when your section is ready
5. **Merge to `main`** when reviewed — live site updates

If you change something the whole team uses (palette, typography, etc.), flag it in the group chat so others can pull and rebase.
