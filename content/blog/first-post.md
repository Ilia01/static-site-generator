---
title: Building a Static Site Generator in Python
date: 2025-10-06
description: The story and architecture behind my handmade static site generator.
---

# Building a Static Site Generator in Python

I wanted to really understand how content turns into a website. So I built my own static site generator—no frameworks, just Python. Here’s how it works and what I learned along the way.

## The goal

- Convert Markdown into HTML
- Keep the code small and readable
- Deploy cleanly to GitHub Pages

## The approach

I modeled the pipeline with explicit types:

1. Parse Markdown text into `TextNode`s (bold, italic, code, links, images)
2. Convert `TextNode`s into `HTMLNode`s
3. Render `HTMLNode`s into HTML
4. Walk the `content/` directory and write to `docs/`

This separation keeps each step simple and testable.

## A small but solid feature set

- Inline formatting: `**bold**`, `*italic*`, `code`
- Links and images: `[text](url)`, `![alt](url)`
- Title extraction: YAML frontmatter or first `# Heading`
- Base path rewriting so absolute URLs work on GitHub Pages

## Lessons learned

- Don’t skip tests—they made refactors easy
- Build the minimal surface area you’ll actually use
- Favor clarity over cleverness; future you will be grateful

## What’s next

I’d like to add a generated blog index, RSS, and a tiny config file. See the “Future” post for more.


