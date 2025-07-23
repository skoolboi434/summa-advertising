// Populate Advertiser Review Tab
function populateAdvertiserReview() {
  const firstName = document.getElementById('advertiser_firstname').value.trim();
  const lastName = document.getElementById('advertiser_lastname').value.trim();
  const email = document.getElementById('advertiser_email').value.trim();
  const phone = document.getElementById('advertiser_phone').value.trim();
  const business_name = document.getElementById('business_name').value.trim();
  const advertiser_address = document.getElementById('advertiser_address').value.trim();
  const advertiser_city = document.getElementById('advertiser_city').value.trim();
  const advertiser_state = document.getElementById('advertiser_state').value.trim();
  const advertiser_zipcode = document.getElementById('advertiser_zipcode').value.trim();
  const advertiser_agency = document.getElementById('advertiser_agency').value.trim();
  const advertiser_website = document.getElementById('advertiser_website').value.trim();
  const advertiser_billing_email = document.getElementById('advertiser_billing_email').value.trim();
  const advertiser_billing_contact = document.getElementById('advertiser_billing_contact').value.trim();
  const advertiser_legacy_id = document.getElementById('advertiser_legacy_id').value.trim();

  const accountTypeSelect = document.getElementById('advertiser_account_type');
  const selectedAccountType = accountTypeSelect?.options[accountTypeSelect.selectedIndex]?.text || '—';

  const salesPersonSelect = document.getElementById('sales-person');
  const selectedSalesPerson = salesPersonSelect?.options[salesPersonSelect.selectedIndex]?.text || '—';

  const industryCodeSelect = document.getElementById('advertiser_industry_code');
  const selectedIndustryCode = industryCodeSelect?.options[industryCodeSelect.selectedIndex]?.text || '—';

  document.getElementById('review-first-name').textContent = firstName || '—';
  document.getElementById('review-last-name').textContent = lastName || '—';
  document.getElementById('review-email').textContent = email || '—';
  document.getElementById('review-phone').textContent = phone || '—';
  document.getElementById('review-business-name').textContent = business_name || '—';
  document.getElementById('review-business-address').textContent = advertiser_address || '—';
  document.getElementById('review-business-city').textContent = advertiser_city || '—';
  document.getElementById('review-business-state').textContent = advertiser_state || '—';
  document.getElementById('review-business-zipcode').textContent = advertiser_zipcode || '—';
  document.getElementById('review-business-agency').textContent = advertiser_agency || '—';
  document.getElementById('review-business-website').textContent = advertiser_website || '—';
  document.getElementById('review-billing-email').textContent = advertiser_billing_email || '—';
  document.getElementById('review-billing-contact').textContent = advertiser_billing_contact || '—';
  document.getElementById('review-account-type').textContent = selectedAccountType;
  document.getElementById('review-sales-person').textContent = selectedSalesPerson;
  document.getElementById('review-industry-code').textContent = selectedIndustryCode;
  document.getElementById('review-legacy-id').textContent = advertiser_legacy_id;

  // Billing address radio value
  const billingOption = document.querySelector('input[name="billing_option"]:checked')?.value;

  // Billing address input values
  const billingStreet = document.getElementById('billing_address')?.value.trim();
  const billingCity = document.getElementById('billing_city')?.value.trim();
  const billingState = document.getElementById('billing_state')?.value.trim();
  const billingZip = document.getElementById('billing_zipcode')?.value.trim();

  // Fallback to advertiser (business) address
  const fallbackStreet = advertiser_address || '—';
  const fallbackCity = advertiser_city || '—';
  const fallbackState = advertiser_state || '—';
  const fallbackZip = advertiser_zipcode || '—';

  // Review tab billing section
  document.getElementById('review-billing-address').textContent = (billingOption === 'different' ? billingStreet : fallbackStreet) || '—';
  document.getElementById('review-billing-city').textContent = (billingOption === 'different' ? billingCity : fallbackCity) || '—';
  document.getElementById('review-billing-state').textContent = (billingOption === 'different' ? billingState : fallbackState) || '—';
  document.getElementById('review-billing-zipcode').textContent = (billingOption === 'different' ? billingZip : fallbackZip) || '—';
}

// notes-sync.js

document.addEventListener('DOMContentLoaded', function () {
  const advertiserId = getAdvertiserIdFromURL();

  if (advertiserId) {
    const notes = JSON.parse(localStorage.getItem('advertiserNotes') || '[]');

    if (notes.length > 0) {
      fetch(`/${advertiserId}/add-notes/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken() // Your CSRF helper
        },
        body: JSON.stringify({ notes: notes })
      })
        .then(res => res.json())
        .then(data => {
          console.log('Notes synced:', data);
          localStorage.removeItem('advertiserNotes'); // clear localStorage after sync
        });
    }
  }
});

// Helper functions
function getAdvertiserIdFromURL() {
  const match = window.location.pathname.match(/\/advertisers?\/(\d+)/);
  return match ? match[1] : null;
}

function getCSRFToken() {
  return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
