# ApiFlow Premium Themes

## Overview

ApiFlow includes 3 stunning premium themes available exclusively to PRO and BUSINESS license holders. Each theme has been carefully designed to provide a unique, professional look for your API documentation.

## Available Themes

### 1. Dark Pro
**Modern dark theme with purple accents**

Features:
- Deep dark backgrounds (#0a0a0f)
- Purple/violet gradient accents
- Glowing hover effects
- Perfect for developer tools and APIs
- Great for reducing eye strain

**Best for:** SaaS products, developer tools, modern tech companies

### 2. Light Pro
**Clean professional light theme with emerald accents**

Features:
- Crisp white backgrounds
- Emerald green accents (#10b981)
- Professional typography
- Subtle shadows and depth
- Corporate-friendly design

**Best for:** Enterprise APIs, financial services, healthcare, B2B products

### 3. Modern
**Contemporary design with vibrant gradients**

Features:
- Vibrant multi-color gradients
- Animated elements
- Backdrop blur effects
- Eye-catching design
- Perfect for consumer products

**Best for:** Consumer apps, creative agencies, startup products, marketing

## How to Use Themes

### Option 1: Command Line
```bash
# Generate with Dark Pro theme
python3 generate_api_docs.py --license "YOUR-LICENSE-KEY" --theme dark-pro

# Generate with Light Pro theme
python3 generate_api_docs.py --license "YOUR-LICENSE-KEY" --theme light-pro

# Generate with Modern theme
python3 generate_api_docs.py --license "YOUR-LICENSE-KEY" --theme modern
```

### Option 2: Configuration File
```bash
# Create config file
python3 generate_api_docs.py --init-config

# Edit apiflow.json
{
  "license_key": "YOUR-LICENSE-KEY",
  "theme": "dark-pro",
  ...
}

# Generate docs
python3 generate_api_docs.py
```

### Option 3: Environment Variable + Config
```bash
export APIFLOW_LICENSE_KEY="YOUR-LICENSE-KEY"
python3 generate_api_docs.py --theme modern
```

## License Requirements

| Feature | FREE | PRO | BUSINESS |
|---------|------|-----|----------|
| Default theme | ✓ | ✓ | ✓ |
| Dark Pro theme | ✗ | ✓ | ✓ |
| Light Pro theme | ✗ | ✓ | ✓ |
| Modern theme | ✗ | ✓ | ✓ |

## Theme Customization

All themes support:
- Dark mode toggle (built-in)
- Responsive design
- Syntax highlighting
- Consistent method badges
- Professional typography

### Want a Custom Theme?

**BUSINESS license holders** get access to our custom theme builder (coming soon), allowing you to:
- Create unlimited custom themes
- Match your brand colors exactly
- White-label completely
- Export and reuse across projects

Contact us for custom theme development.

## Technical Details

### Theme Architecture
- Themes use CSS variables for easy customization
- Base styles in `api-docs.css`
- Theme overrides in `themes/{theme-name}.css`
- No JavaScript required
- Minimal performance impact

### File Structure
```
api-docs/
├── css/
│   └── api-docs.css          # Base styles
├── themes/                    # Premium themes (PRO+)
│   ├── dark-pro.css
│   ├── light-pro.css
│   └── modern.css
└── index.html                 # References theme if selected
```

### Browser Support
- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Preview Themes

To preview themes before purchasing:
1. Visit [apiflow-demo.github.io](https://Ilia01.github.io/apiflow-demo/)
2. Use theme switcher to compare all themes
3. View sample API documentation with each theme

## Upgrade to PRO

Unlock all 3 premium themes + more features:

**PRO License - $49 one-time or $19/year**
- 3 premium themes
- Version management
- Remove branding
- Advanced search
- PDF export
- Priority support

[Get PRO License →](https://github.com/Ilia01/apiflow#pricing)

## Troubleshooting

### Theme Not Applying

**Problem:** Theme CSS not loading

**Solutions:**
1. Verify PRO license is activated:
   ```bash
   python3 generate_api_docs.py --license-status
   ```

2. Check theme file exists:
   ```bash
   ls api-docs/themes/
   ```

3. Clear browser cache and reload

### Theme Looks Different

**Problem:** Theme colors don't match documentation

**Solutions:**
1. Ensure you're using latest version
2. Check for conflicting custom CSS
3. Verify browser supports CSS variables

### License Error

**Problem:** "Premium themes require PRO license"

**Solutions:**
1. Activate your license key
2. Verify license hasn't expired (cached licenses expire after 90 days)
3. Re-activate with `--license` flag

## Support

Need help with themes?
- Email: support@apiflow.dev (PRO+ users get priority)
- GitHub Issues: https://github.com/Ilia01/apiflow/issues
- Documentation: https://github.com/Ilia01/apiflow#themes
