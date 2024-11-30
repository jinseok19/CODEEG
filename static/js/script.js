document.addEventListener('DOMContentLoaded', function () {
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    dropdownToggles.forEach((dropdown) => {
      new bootstrap.Dropdown(dropdown);
    });
  });
  
// Add a click event listener to the button
document.querySelector('.icon-button').addEventListener('click', () => {
    alert('Icon button clicked!');
  });

  

document.querySelector('.dropdown-toggle').addEventListener('click', function () {
  const isExpanded = this.getAttribute('aria-expanded') === 'true';
  this.setAttribute('aria-expanded', !isExpanded);
});
  