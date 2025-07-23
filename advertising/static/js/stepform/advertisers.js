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

  const accountTypeSelect = document.getElementById('advertiser_account_type');
  const selectedAccountType = accountTypeSelect?.options[accountTypeSelect.selectedIndex]?.text || '—';

  const salesPersonSelect = document.getElementById('sales-person');
  const selectedSalesPerson = salesPersonSelect?.options[salesPersonSelect.selectedIndex]?.text || '—';

  const marketCodeSelect = document.getElementById('advertiser_marketcode');
  const selectedMarketCode = marketCodeSelect?.options[marketCodeSelect.selectedIndex]?.text || '—';

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
  document.getElementById('review-market-code').textContent = selectedMarketCode;
}
