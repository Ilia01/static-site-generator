"""License key validation for ApiFlow."""

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from .features import LicenseTier


class LicenseValidator:
    """
    Validates license keys and manages license state.

    License keys are validated against a signature and cached locally.
    Online validation happens on first use, then cached for offline use.
    """

    CACHE_DIR = Path.home() / ".apiflow"
    CACHE_FILE = CACHE_DIR / "license.json"
    VALIDATION_URL = "https://apiflow-license.vercel.app/api/validate"  # TODO: Deploy this

    def __init__(self, license_key: Optional[str] = None):
        """
        Initialize license validator.

        Args:
            license_key: License key to validate. If None, checks for cached license.
        """
        self.license_key = license_key
        self.tier = LicenseTier.FREE
        self.is_valid = False
        self.cached_data: Optional[Dict[str, Any]] = None

        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)

        if license_key:
            self._validate_license()
        else:
            self._load_cached_license()

    def _validate_license(self) -> None:
        """
        Validate license key.

        For now, uses a simple offline validation scheme.
        In production, this would call the validation API.
        """
        # Try online validation first (if implemented)
        # For MVP, use offline validation based on key format

        if not self.license_key:
            return

        parts = self.license_key.split('-')

        if len(parts) < 3 or parts[0] != 'APIFLOW':
            print("⚠️  Invalid license key format")
            return

        tier_str = parts[1].lower()
        provided_hash = '-'.join(parts[2:])

        # Validate tier
        try:
            tier = LicenseTier(tier_str)
        except ValueError:
            print(f"⚠️  Invalid license tier: {tier_str}")
            return

        # Verify hash length (must be 32 characters for SHA256 truncated)
        # For MVP, we trust the format. In production, verify signature via API.
        if len(provided_hash) >= 32:
            self.is_valid = True
            self.tier = tier
            self._cache_license()
            print(f"✓ License activated: {tier.value.upper()}")
        else:
            print("⚠️  Invalid license key - hash too short")

    def _load_cached_license(self) -> None:
        """Load license from cache if it exists and is valid."""
        if not self.CACHE_FILE.exists():
            return

        try:
            with open(self.CACHE_FILE, 'r') as f:
                self.cached_data = json.load(f)

            # Check if cache is expired (90 days)
            cached_time = self.cached_data.get('cached_at', 0)
            if time.time() - cached_time > 90 * 24 * 60 * 60:
                print("⚠️  License cache expired. Please reactivate your license.")
                return

            # Load cached license
            tier_str = self.cached_data.get('tier', 'free')
            self.tier = LicenseTier(tier_str)
            self.is_valid = self.cached_data.get('is_valid', False)

            if self.is_valid:
                print(f"✓ Using cached license: {self.tier.value.upper()}")

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"⚠️  Error loading cached license: {e}")

    def _cache_license(self) -> None:
        """Cache validated license locally."""
        cache_data = {
            'tier': self.tier.value,
            'is_valid': self.is_valid,
            'cached_at': time.time(),
            'license_key': self.license_key[:20] + '...' if self.license_key else None,
        }

        with open(self.CACHE_FILE, 'w') as f:
            json.dump(cache_data, f, indent=2)

    def _generate_hash(self, tier: str) -> str:
        """
        Generate hash for license key validation.

        In production, this would be replaced with proper cryptographic signing.
        """
        secret = os.environ.get('APIFLOW_LICENSE_SECRET')
        if not secret:
            raise ValueError(
                "APIFLOW_LICENSE_SECRET environment variable not set. "
                "See .env.example for setup instructions."
            )
        data = f"{tier}-{secret}"
        return hashlib.sha256(data.encode()).hexdigest()

    def get_tier(self) -> LicenseTier:
        """Get current license tier."""
        return self.tier

    def is_licensed(self) -> bool:
        """Check if a valid license is active."""
        return self.is_valid and self.tier != LicenseTier.FREE

    @staticmethod
    def generate_license_key(tier: LicenseTier, customer_id: str = "") -> str:
        """
        Generate a license key for a given tier.

        This is used by your license generation system (not by end users).

        Args:
            tier: License tier
            customer_id: Optional customer identifier

        Returns:
            License key string

        Raises:
            ValueError: If APIFLOW_LICENSE_SECRET is not set
        """
        import os
        secret = os.environ.get('APIFLOW_LICENSE_SECRET')
        if not secret:
            raise ValueError(
                "APIFLOW_LICENSE_SECRET environment variable not set.\n"
                "This tool is for the product owner only.\n"
                "See .env.example for setup instructions."
            )

        data = f"{tier.value}-{customer_id}-{secret}-{time.time()}"
        hash_value = hashlib.sha256(data.encode()).hexdigest()

        return f"APIFLOW-{tier.value.upper()}-{hash_value[:32]}"

    def print_status(self) -> None:
        """Print current license status."""
        print("\n" + "="*50)
        print("ApiFlow License Status")
        print("="*50)
        print(f"Tier: {self.tier.value.upper()}")
        print(f"Status: {'✓ Active' if self.is_valid else '✗ Inactive'}")

        if not self.is_licensed():
            print("\n💡 Upgrade to PRO for premium features:")
            print("   • Premium themes")
            print("   • Version management")
            print("   • Remove branding")
            print("   • PDF export")
            print("\nVisit: https://github.com/Ilia01/apiflow#pricing")

        print("="*50 + "\n")