document.addEventListener('DOMContentLoaded', function () {
  const stepContainers = document.querySelectorAll('.stepform');

  stepContainers.forEach(container => {
    let currentTab = 0;
    const tabs = container.querySelectorAll('.tab');
    const steps = container.querySelectorAll('.step');
    const form = container.querySelector('form');

    if (tabs.length === 0) return;

    showTab(currentTab);

    // 👉 STEP BUTTONS
    container.querySelectorAll('.step-next').forEach(btn => {
      btn.addEventListener('click', function () {
        const isFinal = btn.dataset.step === 'final';

        if (isFinal) {
          // Let the fetch() logic handle advertiser creation
          document.getElementById('selected-advertisers').value = JSON.stringify(window.selectedAdvertisers || []);
          document.getElementById('selected-products').value = JSON.stringify(window.selectedProducts || []);
          return; // ❌ Do not move forward here
        } else {
          nextPrev(1); // Normal next
        }
      });
    });

    container.querySelectorAll('.step-prev').forEach(btn => {
      btn.addEventListener('click', () => nextPrev(-1));
    });

    // 👉 DISPLAY TABS
    function showTab(n) {
      tabs.forEach((tab, i) => {
        tab.style.display = i === n ? 'block' : 'none';
      });

      container.querySelectorAll('.step-prev').forEach(btn => {
        btn.style.display = n === 0 ? 'none' : 'inline-block';
      });

      const isReviewTab = tabs[n].classList.contains('review-tab');

      container.querySelectorAll('.step-next').forEach(btn => {
        if (!btn.dataset.step || btn.dataset.step !== 'final') {
          btn.textContent = isReviewTab ? 'Create' : 'Next';
        }
      });

      fixStepIndicator(n);

      if (isReviewTab) {
        if (typeof populateReview === 'function' && container.querySelector('#review-campaign-name')) {
          populateReview();
        }

        if (typeof populateAdvertiserReview === 'function') {
          populateAdvertiserReview();
        }

        populateReviewNotes();
      }

      if (n === tabs.length - 1) {
        localStorage.removeItem('advertiserNotes');
        console.log('🧼 Cleared localStorage from showTab fallback');
      }
    }

    // 👉 NEXT/PREV LOGIC
    function nextPrev(n) {
      tabs[currentTab].style.display = 'none';

      if (n === 1) {
        steps[currentTab]?.classList.add('finish');
      } else {
        steps[currentTab]?.classList.remove('finish');
      }

      currentTab += n;

      if (currentTab >= tabs.length) {
        return false;
      }

      showTab(currentTab);
    }

    // 👉 STEP INDICATORS
    function fixStepIndicator(n) {
      steps.forEach((step, i) => {
        step.classList.toggle('active', i === n);
      });
    }

    // 👉 LISTEN FOR advertiserCreated CUSTOM EVENT
    document.addEventListener('advertiserCreated', function (e) {
      console.log('🎉 Advertiser created:', e.detail.advertiser_id);
      currentTab = tabs.length - 1;
      showTab(currentTab);
    });

    function formatDate(iso) {
      if (!iso) return '';
      const [y, m, d] = iso.split('-');
      if (!y || !m || !d) return iso;
      return `${m}/${d}/${y}`;
    }
  });
});
