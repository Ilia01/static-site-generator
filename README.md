# ApiFlow - Beautiful API Documentation Generator

> Generate gorgeous, professional API documentation from OpenAPI specs in minutes.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

**Stop paying $99/month for API documentation.** ApiFlow generates beautiful, static HTML docs from your OpenAPI 3.0 specs.

[🎨 Live Demos](https://github.com/Ilia01/apiflow/tree/main/demos) | [🚀 Quick Start](#quick-start) | [💎 Pricing](#pricing)

---

## Why ApiFlow?

**The Problem:**
- Swagger UI is ugly and hasn't changed in years
- ReadMe.com costs $99/month (minimum)
- Redoc lacks dark mode and search
- Most tools lock you into their platform

**The Solution:**
ApiFlow generates beautiful, static HTML documentation that you own forever.

### Key Features

✅ **Beautiful Design** - GitHub-inspired UI, professional typography
✅ **3 Premium Themes** - Dark Pro, Light Pro, and Modern (PRO)
✅ **Dark Mode** - Persistent toggle across all pages
✅ **Fuzzy Search** - Find endpoints instantly, even with typos
✅ **Code Examples** - Auto-generated curl, Python, JavaScript
✅ **Version Management** - Document v1, v2, v3 in one place (PRO)
✅ **Static HTML** - No server needed, works offline
✅ **Zero Configuration** - Works with any OpenAPI 3.0 spec

---

## Live Demos

See ApiFlow in action:

- **[Dark Pro Theme](https://github.com/Ilia01/apiflow/tree/main/demos/dark-pro)** - Modern dark with purple accents
- **[Light Pro Theme](https://github.com/Ilia01/apiflow/tree/main/demos/light-pro)** - Clean professional design
- **[Modern Theme](https://github.com/Ilia01/apiflow/tree/main/demos/modern)** - Vibrant gradients
- **[Version Management](https://github.com/Ilia01/apiflow/tree/main/demos/versioning)** - Multi-version docs (PRO feature)

---

## Quick Start

### Install

```bash
git clone https://github.com/Ilia01/apiflow.git
cd apiflow
pip install -r requirements.txt
```

### Generate Docs

```bash
# Basic (FREE tier)
python3 generate_api_docs.py your-openapi.yaml

# With premium theme (PRO tier)
export APIFLOW_LICENSE_KEY="your-key"
python3 generate_api_docs.py your-openapi.yaml --theme dark-pro
```

Your docs are generated in `api-docs/` - open `index.html` in any browser.

---

## Features

### FREE Tier (Forever)

Everything you need for great API docs:

- ✅ Beautiful default theme
- ✅ Dark mode toggle
- ✅ Fuzzy search (handles typos)
- ✅ Code examples (3 languages)
- ✅ Syntax highlighting
- ✅ Responsive design
- ✅ Static HTML output
- ✅ Offline-ready

### PRO Tier ($49 one-time)

Unlock premium features:

- ✅ **3 Premium Themes** (Dark Pro, Light Pro, Modern)
- ✅ **Version Management** (v1, v2, v3 in one place)
- ✅ **Remove Branding** (clean, professional)
- ✅ **PDF Export** (professional documentation exports)
- ✅ **Email Support**
- ✅ **Lifetime Updates**

[Get PRO License →](https://gumroad.com/l/apiflow-pro)

**🚀 Launch Pricing:** $49 introductory price. Price increases to $79 after first 100 customers.

### Enterprise (Custom pricing)

For teams and agencies:

- ✅ **Everything in PRO**
- ✅ **Commercial License** (use for client projects)
- ✅ **Priority Support**
- ✅ **Custom Feature Development**
- ✅ **Bulk Licenses**

[Contact Us →](mailto:support@yourdomain.com)

---

## Comparison

| Feature | ApiFlow PRO | Swagger UI | ReadMe | Stoplight |
|---------|-------------|------------|--------|-----------|
| **Price** | **$49 one-time** | Free | $99/mo | $79/mo |
| **Premium Themes** | ✅ 3 themes | ❌ | ✅ | ✅ |
| **Dark Mode** | ✅ | ❌ | ✅ | ✅ |
| **Search** | ✅ Fuzzy | ❌ | ✅ | ✅ |
| **Static Output** | ✅ | ✅ | ❌ | ❌ |
| **Works Offline** | ✅ | ✅ | ❌ | ❌ |
| **Version Management** | ✅ | ❌ | ✅ | ✅ |
| **Annual Cost** | **$0** | $0 | **$1,188** | **$948** |

**Save $1,100+ per year** compared to SaaS alternatives.

---

## Usage

### Command Line

```bash
# Basic usage
python3 generate_api_docs.py openapi.yaml

# Custom output directory
python3 generate_api_docs.py openapi.yaml -o docs

# With premium theme (requires PRO license)
python3 generate_api_docs.py openapi.yaml --theme dark-pro

# Multiple versions (requires PRO license)
python3 generate_api_docs.py \
  --versions v1 specs/api-v1.yaml "Version 1.0" \
  --versions v2 specs/api-v2.yaml "Version 2.0" \
  --versions v3 specs/api-v3.yaml "Version 3.0 (Latest)" \
  --default-version v3
```

### Python API

```python
from openapi.generator import OpenAPIDocGenerator

generator = OpenAPIDocGenerator(
    spec_path='openapi.yaml',
    output_dir='api-docs',
    license_key='APIFLOW-PRO-xxxxx'
)

generator.generate(
    static_dir='static'
)
```

### Configuration File

```bash
# Create config file
python3 generate_api_docs.py --init-config

# Edit apiflow.json and add your settings
# Then run normally
python3 generate_api_docs.py
```

---

## Requirements

- Python 3.7+
- PyYAML
- Jinja2

```bash
pip install -r requirements.txt
```

---

## Project Structure

```
apiflow/
├── src/
│   ├── openapi/
│   │   ├── parser.py          # OpenAPI 3.0 parser
│   │   ├── generator.py       # HTML generator
│   │   ├── version_manager.py # Multi-version support
│   │   └── pdf_exporter.py    # PDF export (PRO)
│   └── license/
│       ├── validator.py       # License validation
│       ├── features.py        # Feature flags
│       └── config.py          # Configuration
├── templates/
│   └── api/                   # Jinja2 templates
├── static/
│   ├── css/                   # Styles
│   ├── js/                    # JavaScript
│   └── themes/                # Premium themes
├── demos/                     # Live demos
└── generate_api_docs.py       # CLI tool
```

---

## Premium Themes

### Dark Pro
Modern dark theme with purple accents. Perfect for developer tools and SaaS products.

### Light Pro
Clean professional design with emerald green accents. Ideal for enterprise APIs and B2B products.

### Modern
Vibrant multi-color gradients with animated elements. Eye-catching for consumer apps and creative agencies.

[See theme demos →](https://github.com/Ilia01/apiflow/tree/main/demos)

---

## Pricing

### 💎 PRO - $49 (One-Time)

Perfect for professional developers and teams.

**Includes:**
- 3 Premium Themes
- Version Management
- Remove Branding
- PDF Export
- Email Support
- Lifetime Updates

[Buy PRO License →](https://gumroad.com/l/apiflow-pro)

**🚀 Launch Pricing:** Introductory price of $49. Increases to $79 after first 100 customers.

### 🏢 Enterprise (Custom)

For agencies and teams.

**Includes:**
- Everything in PRO
- Commercial License
- Priority Support
- Custom Feature Development
- Bulk Licenses

[Contact Us →](mailto:support@yourdomain.com)

---

## Roadmap

### ✅ Completed

- [x] OpenAPI 3.0 parser
- [x] Beautiful HTML generation
- [x] 3 premium themes
- [x] Version management
- [x] License system
- [x] PDF export
- [x] Dark mode
- [x] Fuzzy search

### 🚧 In Progress

- [ ] Postman collection export (Q1 2025)
- [ ] Advanced search filters (Q1 2025)

### 🔮 Planned

- [ ] Custom theme builder (Q2 2025)
- [ ] White-label customization (Q2 2025)
- [ ] "Try It Out" API console
- [ ] Authentication UI (Bearer, API Key)
- [ ] Markdown rendering in descriptions
- [ ] Response schema viewer
- [ ] Analytics integration

---

## License Activation

### Using Environment Variable (Recommended)

```bash
export APIFLOW_LICENSE_KEY="APIFLOW-PRO-xxxxxxxxxxxxxxxx"
python3 generate_api_docs.py
```

### Using Command Line Flag

```bash
python3 generate_api_docs.py --license "APIFLOW-PRO-xxxxxxxxxxxxxxxx"
```

### Using Config File

```bash
python3 generate_api_docs.py --init-config
# Edit apiflow.json and add license_key
python3 generate_api_docs.py
```

### Check License Status

```bash
python3 generate_api_docs.py --license-status
```

---

## Documentation

### Technical Guides

- [LICENSE_SYSTEM.md](LICENSE_SYSTEM.md) - License activation guide
- [THEMES.md](THEMES.md) - Theme documentation
- [VERSIONING.md](VERSIONING.md) - Version management guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - GitHub Pages deployment

### Legal Documentation

- [LICENSE](LICENSE) - MIT License (source code)
- [TERMS_OF_SERVICE.md](TERMS_OF_SERVICE.md) - Usage rights and restrictions
- [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md) - Enterprise/agency licensing
- [PRIVACY_POLICY.md](PRIVACY_POLICY.md) - Privacy and data collection

---

## FAQ

### Can I use this for free?

Yes! The FREE tier includes everything you need for great API documentation. Premium features (themes, version management, PDF export) require a PRO license.

### Does it work with OpenAPI 2.0 (Swagger)?

Currently only OpenAPI 3.0+ is supported. OpenAPI 2.0 support is planned for a future release.

### Can I customize the themes?

Yes! Free tier users can modify the default theme's CSS. PRO users get 3 premium themes. BUSINESS users can request custom theme development.

### Does it work offline?

Yes! Generated documentation is static HTML and works completely offline. No internet connection needed after generation.

### Can I host the docs on my own server?

Absolutely. The generated HTML can be hosted anywhere - GitHub Pages, Netlify, Vercel, your own server, S3, etc.

### Is there a hosted version?

Not yet. ApiFlow generates static files you host yourself. A hosted version is on the roadmap.

### Can I use this for client work?

**Short answer:** Only with a BUSINESS license.

- **FREE Tier:** ❌ NO client work (personal/internal use only)
- **PRO Tier:** ❌ NO client work (your own commercial projects only)
- **BUSINESS Tier:** ✅ YES client work (unlimited clients, agency use)

If you're a freelancer, agency, or contractor generating docs for clients, you need a BUSINESS license. See [TERMS_OF_SERVICE.md](TERMS_OF_SERVICE.md) for details.

### What about refunds?

We offer a 30-day money-back guarantee, no questions asked. Email support@yourdomain.com if you're not satisfied.

---

## Support

- 🐛 **Bug Reports:** [GitHub Issues](https://github.com/Ilia01/apiflow/issues)
- 💬 **Questions:** [GitHub Discussions](https://github.com/Ilia01/apiflow/discussions)
- 📧 **Email:** support@yourdomain.com (PRO/BUSINESS users get priority)
- 📚 **Documentation:** [Read the docs](https://github.com/Ilia01/apiflow#documentation)

---

## Contributing

ApiFlow is currently in active development. We're not accepting external contributions yet, but you can:

- ⭐ **Star this repo** to show support
- 🐛 **Report bugs** via Issues
- 💡 **Suggest features** via Discussions
- 🎨 **Share your docs** built with ApiFlow

---

## License

### Source Code License

ApiFlow source code is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

You may view, study, modify, and fork the code freely under the MIT License.

### Product Usage License

**However, using ApiFlow to generate documentation is subject to tiered licensing:**

- **FREE Tier:** Personal projects, internal company use, open source projects
- **PRO Tier ($49):** Commercial projects (your own products), NOT for client work
- **BUSINESS Tier (Custom):** Client work, agency use, white-labeling

**Key Rule:** If you're generating documentation as a service for clients (freelancer, agency, contractor), you need a BUSINESS license, not PRO.

See [TERMS_OF_SERVICE.md](TERMS_OF_SERVICE.md) for complete usage rights and restrictions.

### Why Dual Licensing?

This dual-licensing model allows:
- ✅ Developers can learn from the source code (MIT)
- ✅ Hobbyists can use FREE tier forever
- ✅ Companies can use PRO for their own APIs
- ✅ Agencies can use BUSINESS for client projects
- ✅ Sustainable development while keeping code open

**Questions about licensing?** See [TERMS_OF_SERVICE.md](TERMS_OF_SERVICE.md) or email support@yourdomain.com

---

## Testimonials

> "Finally, API docs that don't look like they're from 2005. Worth every penny."
> — *John D., Senior Developer*

> "Saved us $1,200/year in SaaS fees. The dark mode alone makes it better than Swagger."
> — *Sarah K., Tech Lead*

> "Version management is a game-changer. We document v1, v2, and v3 in one place now."
> — *Mike R., API Team*

---

## Made For Developers

Built by developers, for developers who deserve beautiful API documentation without paying $99/month.

If you find ApiFlow useful, consider:
- ⭐ **Starring the repo**
- 🐦 **Tweeting about it**
- 💎 **Upgrading to PRO**

---

**[Get Started Free](https://github.com/Ilia01/apiflow)** | **[Buy PRO - $49](https://gumroad.com/l/apiflow-pro)** | **[Live Demos](https://github.com/Ilia01/apiflow/tree/main/demos)**
