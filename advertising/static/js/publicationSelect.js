document.querySelectorAll('.item-select-container').forEach(function (container) {
  const from = container.querySelector('.from-list');
  const to = container.querySelector('.to-list');

  container.querySelector('.btn-right').addEventListener('click', () => moveSelected(from, to));
  container.querySelector('.btn-left').addEventListener('click', () => moveSelected(to, from));
  container.querySelector('.btn-all-right').addEventListener('click', () => moveAll(from, to));
  container.querySelector('.btn-all-left').addEventListener('click', () => moveAll(to, from));

  function moveSelected(fromList, toList) {
    Array.from(fromList.selectedOptions).forEach(option => {
      option.selected = false;
      toList.appendChild(option);
    });
  }

  function moveAll(fromList, toList) {
    Array.from(fromList.options).forEach(option => {
      option.selected = false;
      toList.appendChild(option);
    });
  }

  const form = container.closest('form');
  if (form) {
    form.addEventListener('submit', function () {
      Array.from(to.options).forEach(opt => (opt.selected = true));
    });
  }
});
