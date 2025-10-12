# ApiFlow License System

## Overview

ApiFlow uses a simple license key system to enable premium features. The system works offline after initial activation and caches the license locally.

## License Tiers

### FREE (Default)
- Basic documentation generator
- Default theme
- Basic search
- "Generated with ApiFlow" footer

### PRO ($49 one-time or $19/year)
- All FREE features plus:
- Premium themes
- Version management
- Advanced search
- Remove branding
- PDF export
- Priority support

### BUSINESS ($199 one-time)
- All PRO features plus:
- White-label (full rebrand)
- Custom theme slots
- Commercial license
- Postman collection export

## For Customers

### Activating Your License

There are three ways to activate your license:

#### 1. Environment Variable (Recommended)
```bash
export APIFLOW_LICENSE_KEY="APIFLOW-PRO-xxxxxxxxxxxxxxxx"
python3 generate_api_docs.py
```

#### 2. Command-Line Flag
```bash
python3 generate_api_docs.py --license "APIFLOW-PRO-xxxxxxxxxxxxxxxx"
```

#### 3. Configuration File
```bash
# Create config file
python3 generate_api_docs.py --init-config

# Edit apiflow.json and add your license key
# Then run normally
python3 generate_api_docs.py
```

### Checking License Status
```bash
python3 generate_api_docs.py --license-status
```

### How It Works
1. First time: License is validated and cached locally
2. Subsequent uses: Cached license is used (works offline)
3. Cache expires after 90 days (reactivation required)
4. Cache location: `~/.apiflow/license.json`

## For Product Owner (License Generation)

### Generating License Keys

Use the `generate_license_key.py` script to create keys for customers:

```bash
# Generate a PRO license
python3 generate_license_key.py pro --customer-id "customer@example.com"

# Generate a BUSINESS license
python3 generate_license_key.py business --customer-id "order-12345"

# Generate multiple keys
python3 generate_license_key.py pro --customer-id "bulk-customer" --count 10
```

### Integration with Payment Processors

#### Gumroad Integration
1. Create products in Gumroad:
   - ApiFlow PRO - $49 (one-time) or $19 (yearly)
   - ApiFlow BUSINESS - $199 (one-time)

2. Set up webhook to generate and deliver license keys:
   - On purchase → generate key → email to customer
   - Use generate_license_key.py in webhook handler

#### LemonSqueezy Integration
Similar setup:
1. Create products
2. Configure webhook
3. Auto-generate and deliver keys

### License Key Format

```
APIFLOW-{TIER}-{HASH}
```

Example:
```
APIFLOW-PRO-cf11dfcbe303bec42fbbaed7e3c4f107
APIFLOW-BUSINESS-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

- Tier: PRO or BUSINESS
- Hash: 32-character SHA256 hash (truncated)

### Validation Logic

**Current (MVP):**
- Validates format and tier
- Checks hash length
- Works offline

**Future (Production):**
- Add API endpoint for online validation
- Implement proper cryptographic signing
- Add license usage tracking
- Add license revocation

### Security Notes

1. **Secret Key:** Change `apiflow-secret-2024` in production
   - Use environment variable
   - Never commit to repository

2. **Validation API:** Deploy the validation endpoint
   - Use Vercel/Netlify serverless function
   - Implement rate limiting
   - Log validation attempts

3. **License Sharing:** Keys are single-use but not enforced
   - Trust-based system for MVP
   - Can add activation limits later

## Development Roadmap

### Phase 1: MVP (Complete)
- [x] License key generation
- [x] License validation (offline)
- [x] Feature flags based on tier
- [x] License caching
- [x] CLI integration

### Phase 2: Production
- [ ] Deploy validation API endpoint
- [ ] Add online validation
- [ ] Implement proper cryptographic signing
- [ ] Add license analytics dashboard
- [ ] Add license revocation capability

### Phase 3: Enhanced Features
- [ ] Usage tracking per license
- [ ] Activation limits (e.g., 3 machines per license)
- [ ] License transfer capability
- [ ] Team management for BUSINESS tier
- [ ] Auto-renewal for yearly subscriptions

## Testing

```bash
# Generate test key
python3 generate_license_key.py pro --customer-id "test"

# Test validation
python3 generate_api_docs.py --license "APIFLOW-PRO-xxxxx" --license-status

# Test doc generation
python3 generate_api_docs.py --license "APIFLOW-PRO-xxxxx"

# Test cached license
python3 generate_api_docs.py --license-status

# Clear cache
rm ~/.apiflow/license.json
```

## Support

If customers have issues with their license:

1. Check license key format
2. Verify tier matches purchase
3. Clear cache: `rm ~/.apiflow/license.json`
4. Reactivate with `--license` flag
5. If still failing, generate new key

## Files

- `src/license/validator.py` - License validation logic
- `src/license/features.py` - Feature flags and tier management
- `src/license/config.py` - Configuration management
- `generate_license_key.py` - Key generation tool (owner only)
- `generate_api_docs.py` - Main CLI with license support
