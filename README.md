# gut-feeling

A data visualization on the importance of gut health, specifically during menopause.

> *"Your body is sending signals."*

Built as a single-file, scroll-driven web experience (`index.html`) with embedded CSS and JavaScript — no build step, no dependencies.

## Local preview

Just open `index.html` in your browser. Double-click it, or:

```powershell
# Windows
start index.html
```

```bash
# macOS
open index.html
```

If you want a local web server (useful if you add features that need one, like `fetch()`):

```bash
# Python 3
python -m http.server 8000

# Node (requires npx)
npx serve .
```

Then visit <http://localhost:8000>.

## Design system

### Fonts

From **"you're too emotional"** downward, all copy uses **Source Serif Pro** in exactly two styles:

- **Bold** — display / large lines
- **Italic** — small lines (e.g. science notes, footer)

No other typefaces in this section. All text is **black** (`#000`).

Earlier sections above that point still use **Fraunces**.

### Typography (work section, from "you're too emotional" down)

Poetry-style rules:

- always lowercase
- a normal word space before sentence-ending periods (e.g. `themselves .`, not `themselves.`)
- spaced punctuation elsewhere where needed (e.g. `speaking ;`, `says :`)
- text is never shown in boxes or plates — plain on the canvas

### Particles

This page uses the **glyph version** — particles render as flower glyphs (✿ ❀ ✾ etc.), not spheres or tiles.

### Color

Palette is inspired by a hand-drawn park illustration — warm and saturated rather than muted greys:

- creamy off-white background (`#F9F9F5`)
- spring leaf & forest greens
- terracotta & warm coral
- blossom pink & lavender
- sunny yellow & sky blue

See `PALETTE` in `index.html` for the exact values.

## Deployment

This project deploys to **Vercel** automatically on every push to `main`.

- **Live site:** _link goes here once Vercel is connected_
- **How it works:** Vercel watches the `main` branch on GitHub. When anyone pushes, it deploys the new version within ~10 seconds.
- **Preview deploys:** Any push to a non-`main` branch (or a pull request) gets its own preview URL for review before merging.

No build step runs — Vercel serves `index.html` directly as a static site.

## Project structure

```
gut-feeling/
├── index.html        # The site (HTML + embedded CSS/JS)
├── vercel.json       # Vercel deploy config (clean URLs, no trailing slash)
├── .gitignore
└── README.md
```

## Working together

### Section ownership

- **Maddie** — header through "but, these signals are invisible." (S0 → S2)
- **Catherine** — through "More than a billion women will be in menopause globally by 2030." (S3)
- **Katarina** — storm through garden (S4 → end)

### Workflow

1. **Pull before you start:** `git pull origin main` to grab the latest baseline
2. **Work on your own branch:** `name/feature` convention (e.g. `maddi/header-landing`)
3. **Commit often** with clear messages
4. **Push and open a PR** to `main` when your section is ready
5. **Merge to `main`** when reviewed — live site updates

If you change something the whole team uses (palette, typography, etc.), flag it in the group chat so others can pull and rebase.
