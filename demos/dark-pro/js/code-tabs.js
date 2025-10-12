// Code tab switching functionality
function showCode(language) {
    // Hide all code blocks
    document.querySelectorAll('.code-content').forEach(el => {
        el.classList.remove('active');
    });

    // Remove active from all tabs
    document.querySelectorAll('.code-tab').forEach(el => {
        el.classList.remove('active');
    });

    // Show selected code block
    const codeBlock = document.getElementById(language);
    if (codeBlock) {
        codeBlock.classList.add('active');
    }

    // Mark tab as active
    if (event && event.target) {
        event.target.classList.add('active');
    }

    // Re-highlight code when switching tabs (if Prism is available)
    if (typeof Prism !== 'undefined') {
        Prism.highlightAll();
    }
}
