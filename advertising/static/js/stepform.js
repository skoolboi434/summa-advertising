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
