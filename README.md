# Static Site Generator

A Python-based static site generator that converts markdown text to HTML using a node-based architecture.

## Highlights

- Configurable base path for GitHub Pages (e.g. `/REPO_NAME/`)
- Generates into `docs/` for zero-config Pages deployments
- Markdown → HTML via typed nodes with thorough unit tests
- Simple zsh scripts for local dev and production builds

## Project Overview

This project implements a markdown-to-HTML converter with a modular design that separates text parsing, node processing, and HTML generation into distinct components.

## Architecture

### Core Components

- **TextNode**: Represents different types of text content (text, bold, italic, code, links, images)
- **HTMLNode**: Base class for HTML elements with tag, value, children, and properties
- **LeafNode**: HTML elements that don't contain children (text, images, links)
- **ParentNode**: HTML elements that contain other HTML elements

### Text Processing Pipeline

1. **Text Parsing**: Raw markdown text is converted to TextNode objects
2. **Node Processing**: TextNodes are processed to handle markdown syntax
3. **HTML Conversion**: TextNodes are converted to HTMLNode objects
4. **HTML Generation**: HTMLNode objects generate final HTML output

## Current Implementation Status

### ✅ Completed Features

- **TextNode System**: Complete implementation with all text types (TEXT, BOLD, ITALIC, CODE, LINK, IMAGE)
- **HTML Node Hierarchy**: Base HTMLNode, LeafNode, and ParentNode classes
- **Markdown Parsing**: 
  - Delimiter-based parsing (`**bold**`, `*italic*`, `` `code` ``)
  - Image parsing (`![alt](url)`)
  - Link parsing (`[text](url)`)
- **Text-to-HTML Conversion**: Complete mapping from TextNode types to HTML elements
- **Test Suite**: Comprehensive unit tests for all components

### 🔧 Core Modules

#### `/src/textnode.py`
- `TextType` enum defining all supported text types
- `TextNode` class for representing text content with type and URL

#### `/src/htmlnode.py`
- `HTMLNode` base class with tag, value, children, and properties
- `props_to_html()` method for converting properties to HTML attributes

#### `/src/leafnode.py`
- `LeafNode` class for HTML elements without children
- Handles text, images, links, and other leaf elements

#### `/src/parentnode.py`
- `ParentNode` class for HTML elements that contain other elements
- Supports nested HTML structure generation

#### `/src/utils/`
- **`extract_markdown.py`**: Regex functions for extracting images and links
- **`split_nodes.py`**: Functions for processing delimiter-based markdown syntax
- **`text_textnodes.py`**: Main text processing pipeline
- **`node_to_html.py`**: Conversion mapping from TextNode to HTMLNode

### 🧪 Testing

The project includes a comprehensive test suite covering:
- TextNode creation and equality
- HTMLNode hierarchy functionality
- Markdown parsing and splitting
- Text-to-HTML conversion
- Edge cases and error handling

Run tests with:
```bash
./test.sh
```

### 🚀 Quickstart

Run the local dev server (serves from `docs/` at http://localhost:8888):
```bash
./main.sh
```

Build for production with a custom base path (for GitHub Pages):
```bash
# Replace REPO_NAME with your GitHub repository name
./build.sh
```
The build script runs:
```bash
python3 src/main.py "/REPO_NAME/"
```
If no base path is provided to `main.py`, it defaults to `/` for local testing.

### Commands

- `./main.sh` — Build to `docs/` with basepath `/`, then serve at `http://localhost:8888`
- `./build.sh` — Build to `docs/` with basepath `"/REPO_NAME/"`
- `./test.sh` — Run unit tests

### Configuration

- Base path: first CLI argument to `src/main.py`. Examples:
  - Local: `python3 src/main.py` → basepath `/`
  - Pages: `python3 src/main.py "/static-site-generator/"`
  - Any: `python3 src/main.py "/my-base/"`

## Project Structure

```
src/
├── textnode.py          # TextNode and TextType definitions
├── htmlnode.py          # Base HTMLNode class
├── leafnode.py          # LeafNode implementation
├── parentnode.py        # ParentNode implementation
├── main.py              # Main application entry point
├── utils/
│   ├── extract_markdown.py  # Markdown parsing utilities
│   ├── split_nodes.py       # Node processing functions
│   ├── text_textnodes.py    # Text processing pipeline
│   └── node_to_html.py      # HTML conversion utilities
└── test/                # Unit test suite

content/                 # Markdown source content
static/                  # Static assets copied to docs/
docs/                    # Generated site output (GitHub Pages root)
template.html            # HTML template with {{ Title }} and {{ Content }}
build.sh                 # Production build (uses basepath "/REPO_NAME/")
main.sh                  # Local build + serve at http://localhost:8888
```

## GitHub Pages Deployment

1. Ensure your site builds into the `docs/` directory:
   - `src/main.py` copies `static/` into `docs/` and generates pages from `content/` into `docs/`.
   - Links and assets using absolute-root paths are rewritten during generation:
     - `href="/..."` becomes `href="{basepath}..."`
     - `src="/..."` becomes `src="{basepath}..."`
2. Build the site with a base path matching your repository name:
   - Example: `python3 src/main.py "/static-site-generator/"`
   - Or simply run: `./build.sh`
3. Push the generated `docs/` to the `main` branch.
4. On GitHub: Settings → Pages → Build and deployment
   - Source: `Deploy from a branch`
   - Branch: `main` and folder `docs`
5. Wait for Pages to deploy. Your site will be available at:
   - `https://<your-username>.github.io/<REPO_NAME>/`

Notes:
- Local development defaults to base path `/`.
- For GitHub Pages, always build with base path `/<REPO_NAME>/` so absolute root references resolve correctly.

## Troubleshooting

- Links/assets 404 on GitHub Pages:
  - Ensure you built with `"/<REPO_NAME>/"` base path.
  - Verify `Settings → Pages` points to `main` / `docs`.
- Local images not loading:
  - Re-run `./main.sh` to rebuild and copy `static/` into `docs/`.
- Tests failing to import modules:
  - Run tests from repo root using `./test.sh` so `src` is on the path.

## Development Status

The core markdown-to-HTML conversion system is complete and functional. The project demonstrates a clean separation of concerns with:

- **Parsing Layer**: Handles markdown syntax recognition
- **Processing Layer**: Converts raw text to structured nodes
- **Generation Layer**: Converts nodes to HTML output

All components are thoroughly tested and ready for integration into a larger static site generation workflow.

## Next Steps

Potential future enhancements could include:
- File system integration for reading/writing markdown files
- Template system for HTML page generation
- Command-line interface for batch processing
- Support for additional markdown features (headers, lists, etc.)
