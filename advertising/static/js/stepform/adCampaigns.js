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
