/**
 * Version Switcher for ApiFlow
 * Handles switching between different API versions in the documentation
 */

(function() {
    'use strict';

    // Get current version from localStorage or default
    function getCurrentVersion() {
        return localStorage.getItem('apiflow-selected-version') || null;
    }

    // Save selected version
    function setCurrentVersion(version) {
        localStorage.setItem('apiflow-selected-version', version);
    }

    // Update visibility of version-specific content
    function updateVersionVisibility(selectedVersion) {
        // Hide all version-specific content
        document.querySelectorAll('[data-version]').forEach(element => {
            element.style.display = 'none';
        });

        // Show selected version content
        document.querySelectorAll(`[data-version="${selectedVersion}"]`).forEach(element => {
            element.style.display = '';
        });

        // Update active state in version selector
        document.querySelectorAll('.version-option').forEach(option => {
            if (option.dataset.version === selectedVersion) {
                option.classList.add('active');
            } else {
                option.classList.remove('active');
            }
        });

        // Update version selector button text
        const selectorButton = document.getElementById('versionSelectorButton');
        if (selectorButton) {
            const selectedOption = document.querySelector(`[data-version="${selectedVersion}"]`);
            if (selectedOption) {
                const label = selectedOption.dataset.label || selectedVersion;
                selectorButton.textContent = label;
            }
        }

        // Dispatch custom event for other scripts
        document.dispatchEvent(new CustomEvent('versionChanged', {
            detail: { version: selectedVersion }
        }));
    }

    // Handle version selection
    function handleVersionSelect(version) {
        setCurrentVersion(version);
        updateVersionVisibility(version);

        // Close dropdown if open
        const dropdown = document.querySelector('.version-dropdown');
        if (dropdown) {
            dropdown.classList.remove('active');
        }
    }

    // Toggle dropdown
    function toggleVersionDropdown() {
        const dropdown = document.querySelector('.version-dropdown');
        if (dropdown) {
            dropdown.classList.toggle('active');
        }
    }

    // Close dropdown when clicking outside
    function handleOutsideClick(event) {
        const dropdown = document.querySelector('.version-dropdown');
        const button = document.getElementById('versionSelectorButton');

        if (dropdown && button &&
            !dropdown.contains(event.target) &&
            !button.contains(event.target)) {
            dropdown.classList.remove('active');
        }
    }

    // Get default version from page data
    function getDefaultVersion() {
        const versionData = document.getElementById('versionData');
        if (versionData) {
            const versions = JSON.parse(versionData.textContent || '[]');
            const defaultVersion = versions.find(v => v.is_default);
            return defaultVersion ? defaultVersion.version : (versions[0]?.version || null);
        }
        return null;
    }

    // Initialize version switcher
    function initVersionSwitcher() {
        // Get current or default version
        let selectedVersion = getCurrentVersion();
        if (!selectedVersion) {
            selectedVersion = getDefaultVersion();
            if (selectedVersion) {
                setCurrentVersion(selectedVersion);
            }
        }

        // Show initial version
        if (selectedVersion) {
            updateVersionVisibility(selectedVersion);
        }

        // Setup event listeners
        const selectorButton = document.getElementById('versionSelectorButton');
        if (selectorButton) {
            selectorButton.addEventListener('click', toggleVersionDropdown);
        }

        // Add click handlers to version options
        document.querySelectorAll('.version-option').forEach(option => {
            option.addEventListener('click', () => {
                handleVersionSelect(option.dataset.version);
            });
        });

        // Close dropdown on outside click
        document.addEventListener('click', handleOutsideClick);

        // Handle keyboard navigation
        document.addEventListener('keydown', (e) => {
            const dropdown = document.querySelector('.version-dropdown');
            if (dropdown && dropdown.classList.contains('active') && e.key === 'Escape') {
                dropdown.classList.remove('active');
            }
        });
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initVersionSwitcher);
    } else {
        initVersionSwitcher();
    }

    // Export for external use
    window.ApiFlowVersions = {
        getCurrentVersion,
        setCurrentVersion: handleVersionSelect,
        getDefaultVersion
    };
})();
