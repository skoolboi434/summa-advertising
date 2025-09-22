// Sidemenu
const toggle = document.getElementById('sidebarToggle');
toggle.addEventListener('click', () => {
  document.body.classList.toggle('open-sidebar');
  toggle.innerHTML = document.body.classList.contains('open-sidebar') ? '&times;' : '&#9776;';
});

// Advertising Calendar
document.querySelectorAll('.advertising-calendar').forEach(calendarContainer => {
  const monthSelect = calendarContainer.querySelector('.month-select');
  const yearSelect = calendarContainer.querySelector('.year-select');
  const calendarDates = calendarContainer.querySelector('.calendar-dates');

  const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

  const today = new Date();
  const currentMonth = today.getMonth();
  const currentYear = today.getFullYear();

  // Prevent re-initialization
  if (monthSelect.options.length === 0) {
    months.forEach((month, i) => {
      const opt = document.createElement('option');
      opt.value = i;
      opt.textContent = month;
      if (i === currentMonth) opt.selected = true;
      monthSelect.appendChild(opt);
    });

    for (let y = currentYear - 5; y <= currentYear + 5; y++) {
      const opt = document.createElement('option');
      opt.value = y;
      opt.textContent = y;
      if (y === currentYear) opt.selected = true;
      yearSelect.appendChild(opt);
    }
  }

  function renderCalendar(month, year) {
    calendarDates.innerHTML = '';

    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    for (let i = 0; i < firstDay; i++) {
      calendarDates.appendChild(document.createElement('div'));
    }

    for (let day = 1; day <= daysInMonth; day++) {
      const cell = document.createElement('div');
      cell.textContent = day;
      cell.classList.add('py-2', 'border', 'rounded', 'text-center');

      if (day === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
        cell.classList.add('bg-primary', 'text-white');
      }

      calendarDates.appendChild(cell);
    }
  }

  renderCalendar(currentMonth, currentYear);

  monthSelect.addEventListener('change', () => {
    renderCalendar(+monthSelect.value, +yearSelect.value);
  });

  yearSelect.addEventListener('change', () => {
    renderCalendar(+monthSelect.value, +yearSelect.value);
  });
});
function toggleSearchContainer() {
  var searchContainer = document.getElementById('search-container');
  if (searchContainer.style.display === 'none' || searchContainer.style.display === '') {
    searchContainer.style.display = 'block';
  } else {
    searchContainer.style.display = 'none';
  }
}

// document.querySelectorAll('.item-select-container').forEach(function (container) {
//   const from = container.querySelector('.from-list');
//   const to = container.querySelector('.to-list');

//   container.querySelector('.btn-right').addEventListener('click', () => moveSelected(from, to));
//   container.querySelector('.btn-left').addEventListener('click', () => moveSelected(to, from));
//   container.querySelector('.btn-all-right').addEventListener('click', () => moveAll(from, to));
//   container.querySelector('.btn-all-left').addEventListener('click', () => moveAll(to, from));

//   function moveSelected(fromList, toList) {
//     Array.from(fromList.selectedOptions).forEach(option => {
//       option.selected = false;
//       toList.appendChild(option);
//     });
//   }

//   function moveAll(fromList, toList) {
//     Array.from(fromList.options).forEach(option => {
//       option.selected = false;
//       toList.appendChild(option);
//     });
//   }

//   const form = container.closest('form');
//   if (form) {
//     form.addEventListener('submit', function () {
//       Array.from(to.options).forEach(opt => (opt.selected = true));
//     });
//   }
// });
