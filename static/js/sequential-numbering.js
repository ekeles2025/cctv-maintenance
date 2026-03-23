/**
 * Sequential Numbering for All Tables
 * This script automatically adds sequential numbering (1, 2, 3, ...) to all tables
 */
document.addEventListener('DOMContentLoaded', function() {
    // Add sequential numbering to all tables
    function addSequentialNumbering() {
        const tables = document.querySelectorAll('table');
        tables.forEach(table => {
            const tbody = table.querySelector('tbody');
            if (tbody) {
                const rows = tbody.querySelectorAll('tr');
                let visibleIndex = 1;
                
                rows.forEach((row, index) => {
                    // Only number visible rows
                    if (row.style.display !== 'none') {
                        const firstCell = row.querySelector('td:first-child');
                        if (firstCell) {
                            firstCell.innerHTML = `<strong>${visibleIndex}</strong>`;
                        }
                        visibleIndex++;
                    }
                });
            }
        });
    }

    // Initial numbering
    addSequentialNumbering();

    // Re-number when search filters change
    const searchInputs = document.querySelectorAll('input[type="text"], input[type="search"]');
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            // Small delay to allow filtering to complete
            setTimeout(addSequentialNumbering, 100);
        });
    });

    // Re-number when DOM changes (for dynamic content)
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                setTimeout(addSequentialNumbering, 100);
            }
        });
    });

    // Observe all table bodies for changes
    const tableBodies = document.querySelectorAll('table tbody');
    tableBodies.forEach(tbody => {
        observer.observe(tbody, {
            childList: true,
            subtree: true
        });
    });
});

// Export function to manually re-number if needed
window.renumberTables = function() {
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        const tbody = table.querySelector('tbody');
        if (tbody) {
            const rows = tbody.querySelectorAll('tr');
            rows.forEach((row, index) => {
                const firstCell = row.querySelector('td:first-child');
                if (firstCell) {
                    firstCell.innerHTML = `<strong>${index + 1}</strong>`;
                }
            });
        }
    });
};
