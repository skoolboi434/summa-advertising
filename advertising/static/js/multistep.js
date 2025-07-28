const tabHeading = document.querySelector('#tab-heading h3');
const tabButtons = document.querySelectorAll('[data-bs-toggle="pill"]');
const tabTriggerList = Array.from(tabButtons);

function updateHeading(targetId) {
  const targetPane = document.querySelector(targetId);
  const newHeading = targetPane.dataset.heading;
  tabHeading.textContent = newHeading;
}

// Add event listener to update heading when tab is changed
tabTriggerList.forEach(button => {
  button.addEventListener('shown.bs.tab', e => {
    updateHeading(e.target.dataset.bsTarget);
  });
});

// Handle Next and Prev buttons
document.getElementById('nextTabBtn').addEventListener('click', () => {
  const activeIndex = tabTriggerList.findIndex(btn => btn.classList.contains('active'));
  if (activeIndex < tabTriggerList.length - 1) {
    const nextButton = new bootstrap.Tab(tabTriggerList[activeIndex + 1]);
    nextButton.show();
  }
});

document.getElementById('prevTabBtn').addEventListener('click', () => {
  const activeIndex = tabTriggerList.findIndex(btn => btn.classList.contains('active'));
  if (activeIndex > 0) {
    const prevButton = new bootstrap.Tab(tabTriggerList[activeIndex - 1]);
    prevButton.show();
  }
});
