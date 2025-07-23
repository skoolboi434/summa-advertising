// Utility to format the date
function formatNoteTimestamp() {
  const date = new Date();
  return date.toLocaleString(undefined, {
    month: 'long',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit'
  });
}

// Save note to localStorage
function saveNote(noteText) {
  const notes = JSON.parse(localStorage.getItem('advertiserNotes') || '[]');
  notes.push({ text: noteText, timestamp: formatNoteTimestamp() });
  localStorage.setItem('advertiserNotes', JSON.stringify(notes));
}

// Render notes into any container
function renderNotes(containerId) {
  const container = document.getElementById(containerId);
  if (!container) {
    console.warn(`Container "${containerId}" not found`);
    return;
  }

  container.innerHTML = ''; // Clear existing
  const notes = JSON.parse(localStorage.getItem('advertiserNotes') || '[]');

  notes.forEach(note => {
    const item = document.createElement('div');
    item.className = 'note-item border rounded mb-3 p-2';
    item.innerHTML = `
      <p class="small">${note.text}</p>
      <p class="text-muted small text-end">${note.timestamp}</p>
    `;
    container.appendChild(item);
  });
}

// Form handler

document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('add-note-btn').addEventListener('click', function () {
    const noteText = document.getElementById('note-text').value.trim();
    if (!noteText) return;

    saveNote(noteText);
    document.getElementById('note-text').value = ''; // clear
    renderNotes('note-preview-list');
  });

  renderNotes('note-preview-list');
});

function populateReviewNotes() {
  renderNotes('review-notes-list');
}
