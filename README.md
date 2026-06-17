# gut-feeling

A scroll-driven piece on gut health during menopause.

> *"Your body is sending signals."*

Built as a single file — `flora.html` — with embedded CSS and JavaScript. No build step.

## Local preview

Open `flora.html` in your browser, or:

```bash
python -m http.server 8000
# visit http://localhost:8000/flora.html
```

## Deployment

Pushes to `main` deploy to **Vercel** automatically. The site root (`/`) serves `flora.html`.

## Project structure

```
gut-feeling/
├── flora.html    # The experience (HTML + embedded CSS/JS)
├── vercel.json   # Vercel config (root → flora.html)
├── .gitignore
└── README.md
```

## Fonts (work section)

From **"you're too emotional"** downward: **Source Serif Pro** bold for display lines, italic for small lines. All black. Earlier sections use Fraunces.

## Typography (work section)

- lowercase
- spaced punctuation (`speaking ;`, `themselves .`)
- no text boxes — plain on the canvas

## Particles

Flower glyphs only (✿ ❀ ✾ etc.), not spheres or tiles.

## Color

Warm park-inspired palette — see `PALETTE` in `flora.html`.

## Working together

1. `git pull` before you start
2. Branch for bigger changes: `git checkout -b your-name/feature`
3. Open a PR for preview deploys
4. Merge to `main` when ready
