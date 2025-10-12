document.addEventListener('DOMContentLoaded', function () {
  const checkboxes = document.querySelectorAll('.schedule-option input[type="checkbox"]');
  const calendarInput = document.getElementById('publishing-calendar');

  const dayMap = {
    Sunday: 0,
    Monday: 1,
    Tuesday: 2,
    Wednesday: 3,
    Thursday: 4,
    Friday: 5,
    Saturday: 6
  };

  // Initialize Flatpickr
  const fp = flatpickr(calendarInput, {
    inline: true,
    mode: 'multiple',
    dateFormat: 'Y-m-d',
    defaultDate: []
  });

  function updateCalendar() {
    const selectedDays = Array.from(checkboxes)
      .filter(cb => cb.checked)
      .map(cb => dayMap[cb.value]); // Convert names → numbers

    const today = new Date();
    const year = today.getFullYear();
    const month = today.getMonth();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    const matchingDates = [];
    for (let day = 1; day <= daysInMonth; day++) {
      const date = new Date(year, month, day);
      if (selectedDays.includes(date.getDay())) {
        matchingDates.push(date.toISOString().split('T')[0]);
      }
    }

    fp.setDate(matchingDates, true);
  }

  checkboxes.forEach(cb => cb.addEventListener('change', updateCalendar));
});

document.addEventListener('DOMContentLoaded', function () {
  const dayCheckboxes = document.querySelectorAll('.schedule-options input[type="checkbox"]');
  const tabList = document.getElementById('dayTabs');
  const tabContent = document.getElementById('dayTabContent');

  function updateTabs() {
    // Clear old tabs and content
    tabList.innerHTML = '';
    tabContent.innerHTML = '';

    const checkedDays = Array.from(dayCheckboxes).filter(cb => cb.checked);

    checkedDays.forEach((checkbox, index) => {
      const day = checkbox.value;
      const dayId = day.toLowerCase();

      // ✅ Create tab button
      const tabButton = document.createElement('button');
      tabButton.className = 'nav-link-custom' + (index === 0 ? ' active' : '');
      tabButton.id = `${dayId}-tab`;
      tabButton.dataset.bsToggle = 'pill';
      tabButton.dataset.bsTarget = `#${dayId}-tab-pane`;
      tabButton.type = 'button';
      tabButton.role = 'tab';
      tabButton.setAttribute('aria-controls', `${dayId}-tab-pane`);
      tabButton.setAttribute('aria-selected', index === 0 ? 'true' : 'false');
      tabButton.textContent = day;

      // ✅ Wrap button in li.nav-item
      const li = document.createElement('li');
      li.className = 'nav-item';
      li.setAttribute('role', 'presentation');
      li.appendChild(tabButton);
      tabList.appendChild(li);

      // ✅ Create matching tab pane
      const pane = document.createElement('div');
      pane.className = 'tab-pane fade' + (index === 0 ? ' show active' : '');
      pane.id = `${dayId}-tab-pane`;
      pane.role = 'tabpanel';
      pane.setAttribute('aria-labelledby', `${dayId}-tab`);

      // Each department row
      const departments = ['Sales', 'PrePress', 'Publishing', 'Press', 'Pagination', 'Graphics'];
      departments.forEach(dept => {
        const deptId = dept.toLowerCase();

        const listItem = document.createElement('div');
        listItem.className = 'list-group-item d-flex align-items-center justify-content-between flex-wrap py-3';

        listItem.innerHTML = `
          <strong class="me-3">${dept}</strong>
          <div class="form-check form-switch me-3">
            <input class="form-check-input" type="checkbox" id="${dayId}-${deptId}-toggle">
          </div>
          <div class="form-group d-flex align-items-center">
            <label for="${dayId}-${deptId}-due" class="me-2 fw-semibold">Due By:</label>
            <input type="date" class="form-control w-50" id="${dayId}-${deptId}-due" disabled >
          </div>
          <div class="d-flex align-items-center">
            <input type="text" class="form-control me-1" placeholder="HH" id="${dayId}-${deptId}-hour" style="width: 60px" disabled>
            <span>:</span>
            <input type="text" class="form-control ms-1 me-2" placeholder="MM" id="${dayId}-${deptId}-minute" style="width: 60px" disabled>
            <select class="form-select" id="${dayId}-${deptId}-ampm" disabled>
              <option>AM</option>
              <option>PM</option>
            </select>
          </div>
        `;

        // Toggle enable/disable on switch
        listItem.querySelector(`#${dayId}-${deptId}-toggle`).addEventListener('change', function () {
          const disabled = !this.checked;
          listItem.querySelectorAll('input, select').forEach(el => {
            if (el !== this) el.disabled = disabled;
          });
        });

        pane.appendChild(listItem);
      });

      tabContent.appendChild(pane);
    });

    // ✅ Ensure the first tab is shown immediately
    if (checkedDays.length > 0) {
      const firstTabTrigger = document.querySelector(`#dayTabs .nav-link.active`);
      const firstTab = new bootstrap.Tab(firstTabTrigger);
      firstTab.show();
    }
  }

  dayCheckboxes.forEach(cb => cb.addEventListener('change', updateTabs));
});
