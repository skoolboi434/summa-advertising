document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.table-filter').forEach(select => {
    select.addEventListener('change', function () {
      const tableId = this.dataset.table;
      const table = document.getElementById(tableId);
      const tbody = table.querySelector('tbody');
      const rows = Array.from(tbody.querySelectorAll('tr'));
      const sortBy = this.value;

      let key = '';
      let reverse = false;

      switch (sortBy) {
        case 'name':
          key = 'name';
          break;
        case 'name-desc':
          key = 'name';
          reverse = true;
          break;
        case 'contact':
          key = 'contact';
          break;
        case 'recent':
        default:
          key = 'created';
          reverse = true;
          break;
      }

      rows.sort((a, b) => {
        const aVal = a.dataset[key] || '';
        const bVal = b.dataset[key] || '';
        return reverse ? bVal.localeCompare(aVal, undefined, { numeric: true }) : aVal.localeCompare(bVal, undefined, { numeric: true });
      });

      // Re-append sorted rows
      rows.forEach(row => tbody.appendChild(row));
    });
  });
});
