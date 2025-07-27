document.addEventListener('DOMContentLoaded', function () {
  const searchInputs = document.querySelectorAll('.table-search');

  searchInputs.forEach(input => {
    input.addEventListener('input', function () {
      const tableId = this.dataset.table;
      const table = document.getElementById(tableId);
      const filter = this.value.toLowerCase();

      if (!table) return;

      const rows = table.querySelectorAll('tbody tr');

      rows.forEach(row => {
        const rowText = row.textContent.toLowerCase();
        row.style.display = rowText.includes(filter) ? '' : 'none';
      });
    });
  });
});
