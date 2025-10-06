---
title: About This Project
date: 2025-10-06
description: How I built a Python static site generator from scratch and what I learned.
---

# About

I built this static site generator because I love understanding how things work under the hood. Instead of reaching for a framework, I wanted to design the parsing, node model, and generation pipeline myself in Python.

## Why build my own tool?

- I learn best by making. Building this from scratch forced me to get the details right: parsing, data modeling, HTML generation, link handling, and the overall developer experience.
- I wanted something small, fast, and human. No webpack, no magic—just clean Python and a simple template.

## What I built

- A typed node system that turns Markdown into a structured tree, then into HTML
- A generator that walks the `content/` directory and writes to `docs/`
- A base path rewriter so the site publishes cleanly to GitHub Pages
- A tiny template system with `{{ Title }}` and `{{ Content }}` placeholders

## What I learned

- How to design small, testable units (text nodes → html nodes → renderer)
- The value of predictable content conventions (one heading per page, optional YAML frontmatter)
- The importance of ergonomics: fast rebuilds, friendly errors, and “just works” defaults

## What I’m proud of

- The clarity of the codebase and tests
- The balance of minimalism and capability—there’s enough power to be useful without hiding behavior
- The end-to-end flow: write Markdown, get a polished site, deploy with zero config

If you’re curious, check the Docs for usage details—or read the blog posts to see how I approached the build.


