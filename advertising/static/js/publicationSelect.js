document.querySelectorAll('.item-select-container').forEach(function (container) {
  const from = container.querySelector('.from-list');
  const to = container.querySelector('.to-list');

  const btnRight = container.querySelector('.btn-right');
  const btnLeft = container.querySelector('.btn-left');
  const btnAllRight = container.querySelector('.btn-all-right');
  const btnAllLeft = container.querySelector('.btn-all-left');

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

  // Attach listeners only if the buttons exist
  if (btnRight) btnRight.addEventListener('click', () => moveSelected(from, to));
  if (btnLeft) btnLeft.addEventListener('click', () => moveSelected(to, from));
  if (btnAllRight) btnAllRight.addEventListener('click', () => moveAll(from, to));
  if (btnAllLeft) btnAllLeft.addEventListener('click', () => moveAll(to, from));

  const form = container.closest('form');
  if (form && to) {
    form.addEventListener('submit', function () {
      Array.from(to.options).forEach(opt => (opt.selected = true));
    });
  }
});
