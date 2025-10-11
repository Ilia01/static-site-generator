# OpenAPI Docs Generator

> Beautiful API documentation from your OpenAPI spec in 5 minutes.

A Python tool that generates gorgeous, interactive API documentation from OpenAPI 3.0 specifications. No server required, works offline, looks amazing.

## Why This Exists

**The Problem:**
- Swagger UI is ugly
- ReadMe.com costs $99/month minimum
- Redoc lacks interactivity (no search, no dark mode)
- GitBook is slow and expensive

**The Solution:**
Static HTML docs that are:
- ✨ Beautiful (GitHub-inspired design)
- 🚀 Fast (static files, no server)
- 🔍 Searchable (fuzzy search built-in)
- 🌙 Dark mode (persists across pages)
- 💻 Code examples (curl, Python, JavaScript)
- 🆓 Free forever

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Generate docs
python3 generate_api_docs.py

# View docs
open api-docs/index.html
```

That's it. Your docs are ready.

## Demo

**Input:** `example-api.yaml` (Pet Store API)
**Output:** `api-docs/` directory with:
- Main overview page
- Individual endpoint pages
- Search functionality
- Dark mode toggle
- Code examples

## Features

### 🎨 Beautiful Design
- Clean, GitHub-style UI
- Color-coded HTTP methods
- Responsive layout
- Smooth transitions

### 🔍 Smart Search
- Fuzzy search (finds results with typos)
- Search by path, method, description
- Real-time results
- Keyboard shortcuts (Esc to clear)

### 🌙 Dark Mode
- One-click toggle
- Persists preference
- Works on all pages
- Smooth transitions

### 💻 Code Examples
- Auto-generated for every endpoint
- cURL, Python (requests), JavaScript (fetch)
- Tab switching
- Syntax highlighting (Prism.js)

### ⚡ Zero Configuration
- Works with any OpenAPI 3.0 spec
- No config files needed
- No build tools required
- Offline-ready

## Usage

### Basic

```bash
# Generate from your OpenAPI spec
python3 generate_api_docs.py
```

### Custom

```python
from openapi.generator import OpenAPIDocGenerator

generator = OpenAPIDocGenerator(
    spec_path='your-api.yaml',
    output_dir='docs',
    template_dir='templates/api'
)
generator.generate(static_dir='static')
```

## Project Structure

```
src/openapi/
  ├── parser.py           # OpenAPI 3.0 parser
  └── generator.py        # HTML generator

templates/api/
  ├── api_index.html      # Overview page
  └── api_endpoint.html   # Endpoint detail page

static/
  ├── css/
  │   └── api-docs.css    # All styles
  └── js/
      ├── theme.js        # Dark mode
      ├── search.js       # Search
      └── code-tabs.js    # Code examples

example-api.yaml          # Sample spec
generate_api_docs.py      # CLI tool
requirements.txt          # Dependencies
```

## Requirements

```
Python 3.7+
PyYAML>=6.0
Jinja2>=3.1.0
```

## How It Works

1. **Parse** OpenAPI spec (YAML/JSON)
2. **Extract** endpoints, parameters, responses
3. **Generate** HTML pages with Jinja2 templates
4. **Copy** static assets (CSS, JS)
5. **Done** Open in browser

## Customization

### Change Theme Colors

Edit `static/css/api-docs.css`:

```css
:root {
    --accent-primary: #0366d6;  /* Change this */
    --bg-primary: #ffffff;       /* And this */
}
```

### Add Your Logo

Edit templates:
```html
<h2>
    <img src="your-logo.png" alt="Logo">
    {{ info.title }}
</h2>
```

### Modify Templates

Templates are in `templates/api/`:
- `api_index.html` - Overview page
- `api_endpoint.html` - Endpoint detail page

Standard Jinja2 syntax.

## Roadmap

### Next (Week 2)
- [ ] "Try It Out" API console
- [ ] Authentication support (Bearer, API Key)
- [ ] Response schema viewer
- [ ] Markdown in descriptions

### Future
- [ ] Version switcher (v1, v2 docs)
- [ ] Custom themes
- [ ] Hosted version
- [ ] Analytics integration

## Comparison

| Feature | This | Swagger UI | ReadMe | Redoc |
|---------|------|------------|--------|-------|
| Price | Free | Free | $99/mo | Free |
| Dark mode | ✅ | ❌ | ✅ | ❌ |
| Search | ✅ | ❌ | ✅ | ✅ |
| Static output | ✅ | ❌ | ❌ | ✅ |
| Beautiful | ✅ | ❌ | ✅ | ✅ |
| Offline | ✅ | ❌ | ❌ | ✅ |
| Code examples | ✅ | ✅ | ✅ | ✅ |

## License

MIT

## Contributing

This is a solo project for now, but open to contributions once it's more mature.

## Support

Found a bug? Want a feature? Open an issue.

---

**Made with ❤️ for developers who deserve beautiful docs without paying $99/month.**
