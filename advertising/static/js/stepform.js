document.addEventListener('DOMContentLoaded', function () {
  const stepContainers = document.querySelectorAll('.stepform');

  stepContainers.forEach(container => {
    let currentTab = 0;
    const tabs = container.querySelectorAll('.tab');
    const steps = container.querySelectorAll('.step');
    const form = container.querySelector('form');

    if (tabs.length === 0) return;

    showTab(currentTab);

    // Button listeners
    container.querySelectorAll('.step-next').forEach(btn => {
      btn.addEventListener('click', function () {
        const isFinal = btn.dataset.step === 'final';

        if (isFinal) {
          document.getElementById('selected-advertisers').value = JSON.stringify(window.selectedAdvertisers || []);
          document.getElementById('selected-products').value = JSON.stringify(window.selectedProducts || []);

          // Submit the form
          form.submit();
        } else {
          nextPrev(1);
        }
      });
    });

    container.querySelectorAll('.step-prev').forEach(btn => {
      btn.addEventListener('click', () => nextPrev(-1));
    });

    function showTab(n) {
      tabs.forEach((tab, i) => {
        tab.style.display = i === n ? 'block' : 'none';
      });

      container.querySelectorAll('.step-prev').forEach(btn => {
        btn.style.display = n === 0 ? 'none' : 'inline-block';
      });

      const isReviewTab = tabs[n].classList.contains('review-tab');

      container.querySelectorAll('.step-next').forEach(btn => {
        // If this button is not marked as the final one, update its text
        if (!btn.dataset.step || btn.dataset.step !== 'final') {
          btn.textContent = isReviewTab ? 'Create' : 'Next';
        }
      });

      fixStepIndicator(n);

      if (isReviewTab) {
        populateReview();
      }
    }

    function nextPrev(n) {
      tabs[currentTab].style.display = 'none';

      if (n === 1) {
        steps[currentTab]?.classList.add('finish');
      } else {
        steps[currentTab]?.classList.remove('finish');
      }

      currentTab += n;

      // ✅ Show the success tab *after* the form is submitted
      if (currentTab >= tabs.length) {
        return false;
      }

      showTab(currentTab);
    }

    function fixStepIndicator(n) {
      steps.forEach((step, i) => {
        step.classList.toggle('active', i === n);
      });
    }

    function populateReview() {
      const nameEl = container.querySelector('#campaign-name');
      const salesEl = container.querySelector('#sales-contact');
      const startEl = container.querySelector('#start-date');
      const endEl = container.querySelector('#end-date');
      const briefEl = container.querySelector('#brief');

      container.querySelector('#review-campaign-name').textContent = nameEl?.value || '—';
      container.querySelector('#review-sales-contact').textContent = salesEl?.options[salesEl.selectedIndex]?.text || '—';
      container.querySelector('#review-start-date').textContent = formatDate(startEl?.value);
      container.querySelector('#review-end-date').textContent = formatDate(endEl?.value) || '—';
      container.querySelector('#review-brief').textContent = briefEl?.value?.trim() || '—';

      if (typeof populateReviewAdvertisers === 'function') populateReviewAdvertisers(container);
      if (typeof populateReviewProducts === 'function') populateReviewProducts(container);
    }

    function formatDate(iso) {
      if (!iso) return '';
      const [y, m, d] = iso.split('-');
      if (!y || !m || !d) return iso;
      return `${m}/${d}/${y}`;
    }
  });
});
