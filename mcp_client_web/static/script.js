// Global JavaScript for the Graphiti MCP Client Web Interface

// Add any global functions or event listeners here

document.addEventListener('DOMContentLoaded', function() {
    console.log('Graphiti MCP Client Web Interface loaded');
});

// Function to show loading spinner
function showLoading(element) {
    element.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>';
}

// Function to format JSON data for display
function formatJson(data) {
    if (typeof data === 'string') {
        try {
            data = JSON.parse(data);
        } catch (e) {
            // If parsing fails, return as is
            return data;
        }
    }
    return JSON.stringify(data, null, 2);
}

// Function to copy text to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        console.log('Text copied to clipboard');
    }).catch(function(err) {
        console.error('Could not copy text: ', err);
    });
}