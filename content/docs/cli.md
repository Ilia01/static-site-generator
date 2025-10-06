---
title: CLI Reference
date: 2025-10-06
description: Commands and flags for building and serving the site.
---

# CLI Reference

## Local build + serve

```bash
./main.sh
```

## Production build for GitHub Pages

```bash
./build.sh
```

This runs:

```bash
python3 src/main.py "/REPO_NAME/"
```

If no base path is provided, it defaults to `/`.


