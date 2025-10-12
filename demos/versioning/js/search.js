// Search functionality (requires Fuse.js and endpoints data)
(function () {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    const noResults = document.getElementById('noResults');
    const mainNav = document.getElementById('mainNav');

    if (!searchInput || !searchResults || !noResults || !mainNav) {
        return;
    }

    if (typeof endpoints === 'undefined' || typeof Fuse === 'undefined') {
        console.error('Search requires endpoints data and Fuse.js');
        return;
    }

    // Configure Fuse.js for fuzzy search
    const fuse = new Fuse(endpoints, {
        keys: ['path', 'method', 'summary', 'description', 'tags'],
        threshold: 0.3,
        includeScore: true,
    });

    function getEndpointUrl(endpoint) {
        const method = endpoint.method.toLowerCase();
        const path = endpoint.path
            .replace(/\//g, '_')
            .replace(/[{}]/g, '')
            .replace(/^_/, '');
        return `${method}_${path}.html`;
    }

    function renderSearchResults(results) {
        if (results.length === 0) {
            searchResults.classList.remove('active');
            noResults.classList.add('active');
            mainNav.style.display = 'none';
            return;
        }

        noResults.classList.remove('active');
        searchResults.classList.add('active');
        mainNav.style.display = 'none';

        const html = results.map(result => {
            const endpoint = result.item;
            const url = getEndpointUrl(endpoint);
            const methodClass = `method-${endpoint.method.toLowerCase()}`;

            return `
                <a href="${url}" class="search-result-item">
                    <span class="method-badge ${methodClass}">${endpoint.method}</span>
                    <span>${endpoint.path}</span>
                </a>
            `;
        }).join('');

        searchResults.innerHTML = html;
    }

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.trim();

        if (query === '') {
            searchResults.classList.remove('active');
            noResults.classList.remove('active');
            mainNav.style.display = 'block';
            return;
        }

        const results = fuse.search(query).slice(0, 10); // Limit to 10 results
        renderSearchResults(results);
    });

    // Clear search on Escape key
    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            searchInput.value = '';
            searchResults.classList.remove('active');
            noResults.classList.remove('active');
            mainNav.style.display = 'block';
        }
    });
})();
