---
title: Getting Started
date: 2025-10-06
description: Install, build, and preview the site locally.
---

# Getting Started

## Install

```bash
git clone https://github.com/<you>/static-site-generator
cd static-site-generator
```

Requires Python 3.10+.

## Quickstart

```bash
./main.sh
```

This builds into `docs/` and serves it at `http://localhost:8888`.

## Build for GitHub Pages

```bash
./build.sh
```

Use a base path matching your repo name. Links and assets are rewritten accordingly.

> Tip: Keep content in `content/` and assets in `static/`. They become `docs/` output.


