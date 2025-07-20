//Step Form
let currentTab = 0;
const tabs = document.getElementsByClassName('tab');
// Show the initial tab when the page loads
showTab(currentTab);

document.querySelectorAll('.step-next').forEach(btn => {
  btn.addEventListener('click', () => nextPrev(1));
});
document.querySelectorAll('.step-prev').forEach(btn => {
  btn.addEventListener('click', () => nextPrev(-1));
});

function showTab(n) {
  // Show the current tab
  tabs[n].style.display = 'block';

  // Toggle visibility of "Previous" buttons
  document.querySelectorAll('.step-prev').forEach(btn => {
    btn.style.display = n === 0 ? 'none' : 'inline-block';
  });

  // Update text on "Next" buttons
  const isLastTab = n === tabs.length - 1;
  document.querySelectorAll('.step-next').forEach(btn => {
    btn.textContent = isLastTab ? 'Submit' : 'Next';
  });

  // Update step indicator
  fixStepIndicator(n);

  // ✅ Populate the review tab if applicable
  if (tabs[n].classList.contains('review-tab')) {
    populateReview();
  }
}

function nextPrev(n) {
  const steps = document.getElementsByClassName('step');
  const x = document.getElementsByClassName('tab');

  // Hide the current tab
  x[currentTab].style.display = 'none';

  // If moving forward, mark step as finished
  if (n === 1) {
    steps[currentTab].classList.add('finish');
  }

  // If moving backward, remove the finish class
  if (n === -1) {
    steps[currentTab].classList.remove('finish');
  }

  // Change current tab
  currentTab += n;

  // If at the end, submit
  if (currentTab >= x.length) {
    document.querySelector('form').submit();
    return false;
  }

  // Otherwise, show the correct tab
  showTab(currentTab);
}

function validateForm() {
  // This function deals with validation of the form fields
  var x,
    y,
    i,
    valid = true;
  x = document.getElementsByClassName('tab');
  y = x[currentTab].getElementsByTagName('input');
  // A loop that checks every input field in the current tab:
  for (i = 0; i < y.length; i++) {
    // If a field is empty...
    if (y[i].value == '') {
      // add an "invalid" class to the field:
      y[i].className += ' invalid';
      // and set the current valid status to false
      valid = false;
    }
  }
  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
    document.getElementsByClassName('step')[currentTab].className += ' finish';
  }
  return valid; // return the valid status
}

function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i,
    x = document.getElementsByClassName('step');
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(' active', '');
  }
  //... and adds the "active" class on the current step:
  x[n].className += ' active';
}

// function fixMobileStepIndicator(n) {
//   // This function removes the "active" class of all steps...
//   var i,
//     x = document.getElementsByClassName('mobile-step');
//   for (i = 0; i < x.length; i++) {
//     x[i].className = x[i].className.replace(' active', '');
//   }
//   //... and adds the "active" class on the current step:
//   x[n].className += ' active';
// }

// --- populate review ---
function populateReview() {
  const nameEl = document.getElementById('campaign-name');
  const salesEl = document.getElementById('sales-contact');
  const startEl = document.getElementById('start-date');
  const endEl = document.getElementById('end-date');
  const briefEl = document.getElementById('brief');

  document.getElementById('review-campaign-name').textContent = nameEl.value || '—';
  document.getElementById('review-sales-contact').textContent = salesEl.options[salesEl.selectedIndex]?.text || '—';
  document.getElementById('review-start-date').textContent = formatDate(startEl.value);
  document.getElementById('review-end-date').textContent = formatDate(endEl.value) || '—';
  document.getElementById('review-brief').textContent = briefEl.value.trim() || '—';

  console.log('Populating review tab...');

  // If you later wire selected advertisers/products, call helper functions here:
  populateReviewAdvertisers();
  populateReviewProducts();
}

function formatDate(iso) {
  if (!iso) return '';
  // iso expected yyyy-mm-dd
  const [y, m, d] = iso.split('-');
  if (!y || !m || !d) return iso;
  return `${m}/${d}/${y}`;
}

// stubs for now
function populateReviewAdvertisers() {
  const list = document.getElementById('review-advertisers');
  list.innerHTML = '<li class="list-group-item text-muted">None selected</li>';
}

function populateReviewProducts() {
  document.getElementById('review-products').textContent = 'None selected';
}
