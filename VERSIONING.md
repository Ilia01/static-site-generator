# API Version Management

ApiFlow PRO includes powerful version management capabilities, allowing you to document multiple versions of your API in a single, unified interface.

## Overview

Version management enables you to:
- 📚 **Multiple Versions**: Document v1, v2, v3 (or any version scheme) in one place
- 🔄 **Easy Switching**: Users can switch between versions with a dropdown selector
- 💾 **Version Persistence**: Selected version is remembered using localStorage
- 🎯 **Default Version**: Set which version users see first
- 📊 **Version Comparison**: See what changed between versions

## Requirements

**License**: PRO or BUSINESS tier required
**Cost**: $49 one-time or $19/year for PRO

Version management is a premium feature that requires an active PRO or BUSINESS license.

## Usage

### Method 1: Command Line

Generate documentation for multiple API versions using the `--versions` flag:

```bash
python3 generate_api_docs.py \
  --license "YOUR-PRO-LICENSE-KEY" \
  --versions v1 specs/api-v1.yaml "Version 1.0" \
  --versions v2 specs/api-v2.yaml "Version 2.0" \
  --versions v3 specs/api-v3.yaml "Version 3.0 (Latest)" \
  --default-version v3
```

**Arguments**:
- `--versions VERSION SPEC_PATH LABEL`: Add a version (can be repeated)
  - `VERSION`: Version identifier (e.g., "v1", "1.0.0", "v2")
  - `SPEC_PATH`: Path to the OpenAPI spec file for this version
  - `LABEL`: Display name shown in the UI (e.g., "Version 2.0", "Latest")
- `--default-version`: Which version to show by default (optional, defaults to first)

### Method 2: Configuration File

For convenience, configure versions in `apiflow.json`:

```json
{
  "license_key": "APIFLOW-PRO-xxxxxxxxxxxxxxxx",
  "theme": "modern",
  "versions": [
    {
      "version": "v1",
      "spec_path": "specs/api-v1.yaml",
      "label": "Version 1.0 (Legacy)",
      "is_default": false
    },
    {
      "version": "v2",
      "spec_path": "specs/api-v2.yaml",
      "label": "Version 2.0 (Stable)",
      "is_default": false
    },
    {
      "version": "v3",
      "spec_path": "specs/api-v3.yaml",
      "label": "Version 3.0 (Latest)",
      "is_default": true
    }
  ]
}
```

Then generate with:

```bash
python3 generate_api_docs.py
```

### Method 3: Python API

Use the version manager programmatically:

```python
from openapi.generator import OpenAPIDocGenerator
from openapi.version_manager import VersionManager

# Create version manager
version_manager = VersionManager()

# Add versions
version_manager.add_version(
    version="v1",
    spec_path="specs/api-v1.yaml",
    label="Version 1.0",
    is_default=False
)

version_manager.add_version(
    version="v2",
    spec_path="specs/api-v2.yaml",
    label="Version 2.0",
    is_default=True  # This will be shown first
)

# Generate documentation
generator = OpenAPIDocGenerator(
    output_dir="api-docs",
    template_dir="templates/api",
    license_key="YOUR-PRO-LICENSE-KEY",
    version_manager=version_manager
)

generator.generate(static_dir="static")
```

## How It Works

### User Experience

1. **Version Selector**: A dropdown appears in the sidebar
2. **Click to Switch**: Users click the dropdown to see all available versions
3. **Instant Switch**: Content updates instantly without page reload
4. **Persisted Choice**: Selected version is saved in localStorage

### Technical Details

**Frontend**:
- Version switcher UI component in sidebar
- JavaScript manages version visibility with `data-version` attributes
- localStorage preserves user's selection across sessions
- Smooth transitions between versions

**Backend**:
- Each version uses a separate OpenAPI spec file
- Specs are parsed independently
- Documentation is generated with version metadata
- All versions are embedded in the same HTML files

## Version Naming Schemes

ApiFlow supports any version naming scheme:

### Semantic Versioning
```bash
--versions 1.0.0 specs/v1.yaml "v1.0.0" \
--versions 2.0.0 specs/v2.yaml "v2.0.0" \
--versions 2.1.0 specs/v2.1.yaml "v2.1.0 (Latest)"
```

### Simple v-prefix
```bash
--versions v1 specs/v1.yaml "v1" \
--versions v2 specs/v2.yaml "v2" \
--versions v3 specs/v3.yaml "v3"
```

### Named Releases
```bash
--versions alpha specs/alpha.yaml "Alpha (Experimental)" \
--versions beta specs/beta.yaml "Beta (Testing)" \
--versions stable specs/stable.yaml "Stable (Production)"
```

### Date-based
```bash
--versions 2024-01 specs/jan.yaml "January 2024" \
--versions 2024-02 specs/feb.yaml "February 2024" \
--versions 2024-03 specs/mar.yaml "March 2024 (Current)"
```

## Best Practices

### 1. Label Versions Clearly

❌ **Bad**: Generic labels
```bash
--versions v1 api-v1.yaml "Version 1"
--versions v2 api-v2.yaml "Version 2"
```

✅ **Good**: Descriptive labels with context
```bash
--versions v1 api-v1.yaml "v1 (Deprecated - EOL 2024-12)" \
--versions v2 api-v2.yaml "v2 (Stable)" \
--versions v3 api-v3.yaml "v3 (Latest - Recommended)"
```

### 2. Set Default to Latest Stable

Always set `--default-version` to your recommended version:

```bash
--default-version v3  # Users see v3 first
```

### 3. Keep Deprecated Versions

Keep old versions in docs for reference, but mark them:

```json
{
  "version": "v1",
  "spec_path": "specs/api-v1.yaml",
  "label": "v1 (⚠️ Deprecated - Use v3)",
  "is_default": false
}
```

### 4. Organize Spec Files

Keep spec files organized by version:

```
project/
├── specs/
│   ├── v1/
│   │   └── openapi.yaml
│   ├── v2/
│   │   └── openapi.yaml
│   └── v3/
│       └── openapi.yaml
├── generate_api_docs.py
└── apiflow.json
```

### 5. Document Breaking Changes

In your OpenAPI specs, document what changed:

```yaml
info:
  title: My API
  version: "2.0.0"
  description: |
    Version 2.0 introduces breaking changes:
    - Authentication now requires Bearer tokens
    - `/users` endpoint removed (use `/v2/users`)
    - Date format changed to ISO 8601
```

## Examples

### Example 1: Simple Two-Version Setup

```bash
python3 generate_api_docs.py \
  --license "APIFLOW-PRO-abc123" \
  --versions v1 api-v1.yaml "Version 1 (Legacy)" \
  --versions v2 api-v2.yaml "Version 2 (Current)" \
  --default-version v2
```

### Example 2: SemVer with Multiple Minors

```bash
python3 generate_api_docs.py \
  --license "APIFLOW-PRO-abc123" \
  --versions 1.0.0 specs/1.0/api.yaml "1.0.0 (Deprecated)" \
  --versions 1.1.0 specs/1.1/api.yaml "1.1.0 (Stable)" \
  --versions 2.0.0-beta specs/2.0-beta/api.yaml "2.0.0-beta (Preview)" \
  --default-version 1.1.0 \
  --theme modern
```

### Example 3: Configuration File

`apiflow.json`:
```json
{
  "license_key": "APIFLOW-PRO-xyz789",
  "theme": "dark-pro",
  "versions": [
    {
      "version": "legacy",
      "spec_path": "openapi-legacy.yaml",
      "label": "Legacy API (Deprecated)",
      "is_default": false
    },
    {
      "version": "current",
      "spec_path": "openapi-current.yaml",
      "label": "Current API (Stable)",
      "is_default": true
    },
    {
      "version": "next",
      "spec_path": "openapi-next.yaml",
      "label": "Next API (Preview)",
      "is_default": false
    }
  ]
}
```

```bash
# Just run without arguments - reads from config
python3 generate_api_docs.py
```

## Troubleshooting

### "Version management requires PRO license"

**Problem**: You see this warning when trying to use `--versions`

**Solution**:
1. Verify you have a PRO or BUSINESS license
2. Activate it: `python3 generate_api_docs.py --license "YOUR-KEY"`
3. Check status: `python3 generate_api_docs.py --license-status`

### Version switcher not appearing

**Possible causes**:
1. Only one version configured (switcher only shows with 2+ versions)
2. `version-switcher.js` not copied to output
3. Browser cache (hard refresh: Cmd+Shift+R / Ctrl+Shift+R)

**Solution**:
```bash
# Regenerate docs
python3 generate_api_docs.py --versions v1 spec1.yaml "V1" --versions v2 spec2.yaml "V2"

# Clear output directory first if needed
rm -rf api-docs && python3 generate_api_docs.py ...
```

### Versions not switching

**Problem**: Dropdown works but content doesn't change

**Solution**:
1. Check browser console for JavaScript errors
2. Ensure all endpoints have `data-version` attributes
3. Clear localStorage: Open DevTools → Application → Local Storage → Clear

### Wrong default version showing

**Problem**: Version switcher shows wrong default

**Solution**:
```bash
# Explicitly set default
python3 generate_api_docs.py \
  --versions v1 spec1.yaml "V1" \
  --versions v2 spec2.yaml "V2" \
  --default-version v2  # Add this
```

## Upgrade to PRO

Unlock version management and other premium features:

**PRO License - $49 one-time or $19/year**
- ✅ Version management (unlimited versions)
- ✅ 3 premium themes
- ✅ Remove ApiFlow branding
- ✅ Advanced search features
- ✅ PDF export (coming soon)
- ✅ Priority support

[Get PRO License →](https://github.com/Ilia01/apiflow#pricing)

## API Reference

### VersionManager

```python
class VersionManager:
    def add_version(version: str, spec_path: str, label: str = None, is_default: bool = False)
    def get_version(version: str) -> VersionedAPI
    def get_default_version() -> VersionedAPI
    def get_all_versions() -> List[VersionedAPI]
    def get_version_list() -> List[Dict[str, str]]
    def has_multiple_versions() -> bool
```

### Config

```python
class Config:
    def get_versions() -> List[Dict[str, Any]]
    def add_version(version: str, spec_path: str, label: str = None, is_default: bool = False)
    def has_versions() -> bool
```

## Support

Need help with version management?
- Email: support@apiflow.dev (PRO users get priority)
- GitHub Issues: https://github.com/Ilia01/apiflow/issues
- Documentation: https://github.com/Ilia01/apiflow

---

**Made with ApiFlow** 🚀
