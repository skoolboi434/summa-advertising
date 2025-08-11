document.addEventListener('DOMContentLoaded', function () {
  function isDesktop() {
    return window.innerWidth > 768; // Adjust breakpoint as needed
  }

  // Initialize Flatpickr based on screen size
  function initializeFlatpickr() {
    let startDate = null; // Store the selected start date

    const startOptions = {
      inline: isDesktop(),
      dateFormat: 'Y-m-d',
      altInput: true,
      altFormat: 'F j, Y',
      onChange: function (selectedDates) {
        if (selectedDates.length > 0) {
          startDate = selectedDates[0]; // Save the selected start date
        }
      }
    };

    const endOptions = {
      inline: isDesktop(),
      dateFormat: 'Y-m-d',
      altInput: true,
      altFormat: 'F j, Y',
      onChange: function (selectedDates, dateStr, instance) {
        if (selectedDates.length > 0) {
          const endDate = selectedDates[0];

          if (startDate && startDate.getTime() === endDate.getTime()) {
            showBootstrapAlert('Start and End dates cannot be the same. Please choose different dates.');
            // Clear the end date
            instance.clear();
          }
        }
      }
    };

    // Initialize Flatpickr for Start Date
    flatpickr('#start_date', startOptions);

    // Initialize Flatpickr for End Date
    flatpickr('#end_date', endOptions);
  }

  function showBootstrapAlert(message) {
    const alertPlaceholder = document.getElementById('alert-container');

    if (alertPlaceholder) {
      // Create the alert HTML
      const alertElement = document.createElement('div');
      alertElement.className = 'alert alert-warning alert-dismissible fade show';
      alertElement.setAttribute('role', 'alert');
      alertElement.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;

      // Append the alert to the container
      alertPlaceholder.appendChild(alertElement);

      // Automatically remove the alert after 5 seconds
      setTimeout(() => {
        alertElement.classList.remove('show'); // Fade out
        setTimeout(() => alertElement.remove(), 500); // Remove after fade-out
      }, 5000);
    }
  }

  // Initialize on page load
  initializeFlatpickr();

  // Reinitialize Flatpickr on window resize
  window.addEventListener('resize', function () {
    // Destroy existing instances
    document.querySelector('#start_date')._flatpickr?.destroy();
    document.querySelector('#end_date')._flatpickr?.destroy();

    // Reinitialize with updated settings
    initializeFlatpickr();
  });
});
