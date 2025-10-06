---
title: Documentation
date: 2025-10-06
description: How to install, build, customize, and deploy this static site generator.
---

# Docs

This project converts Markdown in `content/` into static HTML in `docs/` using a simple Python pipeline.

## Install

```bash
git clone https://github.com/Ilia01/static-site-generator
cd static-site-generator
```

Python 3.10+ recommended. No external dependencies.

## Develop locally

```bash
./main.sh
```

- Builds the site into `docs/`
- Serves `docs/` at `http://localhost:8888`

## Build for GitHub Pages

```bash
# Replace REPO_NAME with your repository name
./build.sh
```

This runs `python3 src/main.py "/REPO_NAME/"`, which rewrites root-relative `href="/…"` and `src="/…"` to include your base path so assets and links work on Pages.

## Content structure

- Put Markdown files in `content/`
- Nested folders are preserved in `docs/`
- Files ending in `.md` become `.html`

Examples:

- `content/index.md` → `docs/index.html`
- `content/about.md` → `docs/about.html`
- `content/blog/first-post.md` → `docs/blog/first-post.html`

## Frontmatter and titles

Pages can optionally start with YAML frontmatter:

```yaml
---
title: My Page
date: 2025-10-06
description: Short summary for social/SEO
---
```

If frontmatter is present and includes `title:`, it will be used. Otherwise the first `# Heading` becomes the page title.

## Templates and theming

- `template.html` contains `{{ Title }}` and `{{ Content }}` placeholders
- `static/index.css` is copied to `docs/index.css`
- Images and static assets live in `static/` and are copied to `docs/`

## Customization ideas

- Add a blog index generator and tag pages
- Generate RSS and sitemap
- Support code blocks with syntax highlighting
- Add a config file for site metadata and navigation

## Deploy

Commit and push the `docs/` folder on `main`, then enable GitHub Pages for `main` → `docs` in the repository settings.


