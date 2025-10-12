"""Feature management based on license tier."""

from enum import Enum
from typing import List


class LicenseTier(Enum):
    """Available license tiers."""
    FREE = "free"
    PRO = "pro"
    BUSINESS = "business"


class FeatureManager:
    """
    Manages feature availability based on license tier.
    """

    # Define features available for each tier
    FEATURES = {
        LicenseTier.FREE: {
            'basic_generator',
            'default_theme',
            'basic_search',
        },
        LicenseTier.PRO: {
            'basic_generator',
            'default_theme',
            'basic_search',
            'premium_themes',
            'version_management',
            'advanced_search',
            'remove_branding',
            'pdf_export',
            'priority_support',
        },
        LicenseTier.BUSINESS: {
            'basic_generator',
            'default_theme',
            'basic_search',
            'premium_themes',
            'version_management',
            'advanced_search',
            'remove_branding',
            'pdf_export',
            'priority_support',
            'white_label',
            'custom_themes',
            'commercial_license',
            'postman_export',
        },
    }

    def __init__(self, tier: LicenseTier = LicenseTier.FREE):
        """
        Initialize feature manager with a license tier.

        Args:
            tier: The license tier (FREE, PRO, or BUSINESS)
        """
        self.tier = tier

    def has_feature(self, feature: str) -> bool:
        """
        Check if a feature is available for the current license tier.

        Args:
            feature: Feature name to check

        Returns:
            True if feature is available, False otherwise
        """
        return feature in self.FEATURES.get(self.tier, set())

    def get_available_features(self) -> List[str]:
        """
        Get list of all available features for current tier.

        Returns:
            List of feature names
        """
        return list(self.FEATURES.get(self.tier, set()))

    def require_feature(self, feature: str) -> None:
        """
        Raise an exception if feature is not available.

        Args:
            feature: Feature name to check

        Raises:
            PermissionError: If feature is not available in current tier
        """
        if not self.has_feature(feature):
            tier_name = self.tier.value.upper()
            raise PermissionError(
                f"Feature '{feature}' requires a PRO or BUSINESS license. "
                f"Current tier: {tier_name}. "
                f"Upgrade at: https://github.com/Ilia01/apiflow#pricing"
            )
