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

1. **Pull before you start:** `git pull` to grab the latest changes
2. **Make a branch for non-trivial changes:** `git checkout -b your-name/feature`
3. **Commit often** with clear messages
4. **Push and open a PR** — gets you a preview URL automatically
5. **Merge to `main`** when ready — live site updates

For tiny changes (typos, copy tweaks), pushing directly to `main` is fine.
