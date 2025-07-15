// Sidemenu
const toggle = document.getElementById('sidebarToggle');
toggle.addEventListener('click', () => {
  document.body.classList.toggle('open-sidebar');
  toggle.innerHTML = document.body.classList.contains('open-sidebar') ? '&times;' : '&#9776;';
});
