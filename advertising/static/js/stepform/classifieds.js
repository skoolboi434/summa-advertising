function calculateWeeks(startDate, endDate) {
  const oneDay = 24 * 60 * 60 * 1000; // milliseconds in a day
  const start = new Date(startDate);
  const end = new Date(endDate);

  // Calculate total days (+1 to include both start and end)
  const totalDays = Math.round((end - start) / oneDay) + 1;

  // Always at least 1 week
  const weeks = Math.ceil(totalDays / 7);

  // Display in the review section
  document.getElementById('review_weeks').textContent = `${weeks} week${weeks > 1 ? 's' : ''}`;
}

document.addEventListener('DOMContentLoaded', function () {
  const startInput = document.getElementById('start_date');
  const endInput = document.getElementById('end_date');

  function updateWeeks() {
    const startVal = startInput.value;
    const endVal = endInput.value;

    if (startVal && endVal) {
      calculateWeeks(startVal, endVal);
    } else {
      document.getElementById('review_weeks').textContent = '—';
    }
  }

  startInput.addEventListener('change', updateWeeks);
  endInput.addEventListener('change', updateWeeks);
});

document.addEventListener('DOMContentLoaded', function () {
  const salesRepSelect = document.getElementById('salesRep');
  const reviewSalesRep = document.getElementById('review_sales_rep');

  function updateSalesRepReview() {
    const selectedOption = salesRepSelect.options[salesRepSelect.selectedIndex];
    reviewSalesRep.textContent = selectedOption.value ? selectedOption.text : '—';
  }

  salesRepSelect.addEventListener('change', updateSalesRepReview);
});

document.addEventListener('DOMContentLoaded', function () {
  const publicationSelect = document.getElementById('publicationSelect');
  const reviewPublication = document.getElementById('review_publication');

  function updatePublicationReview() {
    const selectedOption = publicationSelect.options[publicationSelect.selectedIndex];
    reviewPublication.textContent = selectedOption.value ? selectedOption.text : '—';
  }

  publicationSelect.addEventListener('change', updatePublicationReview);
});

document.addEventListener('DOMContentLoaded', function () {
  const additionalPublicationSelect = document.getElementById('additional_publications');
  const reviewAdditionalPublication = document.getElementById('review_additional_publication');

  function updateAdditionalPublicationReview() {
    const selectedOption = additionalPublicationSelect.options[additionalPublicationSelect.selectedIndex];
    reviewAdditionalPublication.textContent = selectedOption.value ? selectedOption.text : '—';
  }

  additionalPublicationSelect.addEventListener('change', updateAdditionalPublicationReview);
});

document.getElementById('customerSelect').addEventListener('change', function () {
  let selected = this.options[this.selectedIndex];

  document.getElementById('firstName').value = selected.getAttribute('data-firstname') || '';
  document.getElementById('lastName').value = selected.getAttribute('data-lastname') || '';
  document.getElementById('email').value = selected.getAttribute('data-email') || '';
  document.getElementById('phone').value = selected.getAttribute('data-phone') || '';
});

document.addEventListener('DOMContentLoaded', function () {
  const classifiedTitleInput = document.getElementById('classified_title');
  const previewTitle = document.getElementById('preview_title');
  const previewDescription = document.getElementById('preview_description');

  // Update title dynamically in the preview
  classifiedTitleInput.addEventListener('input', function () {
    previewTitle.textContent = classifiedTitleInput.value.trim() || 'Classified Title';
  });

  // Initialize TinyMCE
  if (typeof tinymce !== 'undefined') {
    tinymce.init({
      selector: '#classified_description',
      resize: false,
      plugins: ['advlist', 'autolink', 'lists', 'link', 'image', 'charmap', 'preview', 'anchor', 'importcss', 'searchreplace', 'visualblocks', 'fullscreen', 'insertdatetime', 'media', 'table', 'help', 'wordcount', 'format'],
      toolbar: 'undo redo | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist | removeformat | code',
      setup: function (editor) {
        const maxWords = 50; // Default word count limit

        // Function to enforce word limit
        const enforceWordLimit = () => {
          const content = editor.getContent({
            format: 'text'
          });
          const words = content
            .trim()
            .split(/\s+/)
            .filter(word => word.length > 0);

          if (words.length > maxWords) {
            const truncatedWords = words.slice(0, maxWords).join(' ');

            editor.setContent(truncatedWords);
            showWordLimitAlert();
          }
        };

        const showWordLimitAlert = () => {
          const alertContainer = document.querySelector('.alert-container');
          if (!alertContainer) return;

          const existingAlert = document.querySelector('.word-limit-alert');
          if (existingAlert) existingAlert.remove();

          const alertDiv = document.createElement('div');
          alertDiv.className = 'alert alert-warning word-limit-alert';
          alertDiv.role = 'alert';
          alertDiv.innerHTML = `
            <strong>Word Limit Reached!</strong> You can only use ${maxWords} words.
          `;

          alertContainer.appendChild(alertDiv);

          setTimeout(() => {
            if (alertDiv.parentElement) {
              alertDiv.parentElement.removeChild(alertDiv);
            }
          }, 5000);
        };

        // Listen for content changes and enforce word limit
        editor.on('keyup', enforceWordLimit);
        editor.on('paste', () => setTimeout(enforceWordLimit, 100));

        // Update preview dynamically
        editor.on('input change keyup', () => {
          const content = editor.getContent().trim();

          // Update live preview on the ad creation tab
          previewDescription.innerHTML = content || "This is where you'll write out and style everything about your ad using the tools above...";

          // Update review tab preview
          const reviewEl = document.getElementById('review_classified_preview');
          if (reviewEl) {
            reviewEl.innerHTML = content || '—';
          }
        });
      }
    });
  }
});

const startDateInput = document.getElementById('start_date');
const endDateInput = document.getElementById('end_date');
const reviewStartDate = document.getElementById('review_start_date');
const reviewEndDate = document.getElementById('review_end_date');

// Function to format the date if needed
function formatDate(value) {
  if (!value) return '—';
  const date = new Date(value);
  return isNaN(date) ? value : date.toLocaleDateString();
}

// Update review fields live
startDateInput.addEventListener('input', () => {
  reviewStartDate.textContent = formatDate(startDateInput.value);
});

endDateInput.addEventListener('input', () => {
  reviewEndDate.textContent = formatDate(endDateInput.value);
});

const reviewSubcategory = document.getElementById('review_subcategory');

// Update the review paragraph when selection changes
subcategorySelect.addEventListener('change', function () {
  const selectedText = this.options[this.selectedIndex]?.text || '—';
  reviewSubcategory.textContent = selectedText;
});

function populateClassifiedReview() {
  const nameEl = document.getElementById('classified_title');
  const reviewEl = document.getElementById('review-classified_title');

  reviewEl.textContent = nameEl?.value || '—';
}

// Listen for changes on the input
const titleInput = document.getElementById('classified_title');
titleInput.addEventListener('input', populateClassifiedReview);

// Optionally, populate initially in case there's a default value
populateClassifiedReview();
