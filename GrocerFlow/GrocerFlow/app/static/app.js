// GrocerFlow UI helpers

function initChoices() {
  if (typeof Choices === "undefined") return;
  document.querySelectorAll('select.js-choice').forEach((el) => {
    // Avoid double-init
    if (el.dataset.choicesInitialized === "1") return;
    el.dataset.choicesInitialized = "1";

    const placeholder = el.getAttribute('data-placeholder') || 'Select...';
    new Choices(el, {
      searchEnabled: true,
      shouldSort: false,
      itemSelectText: '',
      allowHTML: false,
      placeholder: true,
      placeholderValue: placeholder,
    });
  });
}

function initConfirms() {
  document.querySelectorAll('form[data-confirm]').forEach((form) => {
    form.addEventListener('submit', (e) => {
      const msg = form.getAttribute('data-confirm') || 'Are you sure?';
      if (!window.confirm(msg)) {
        e.preventDefault();
      }
    });
  });
}

function autoDismissAlerts() {
  // Gracefully remove flash alerts after a few seconds
  const alerts = document.querySelectorAll('.alert[data-autodismiss="1"]');
  alerts.forEach((a) => {
    setTimeout(() => {
      a.classList.add('fade');
      a.style.opacity = '0';
      setTimeout(() => a.remove(), 450);
    }, 4200);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initChoices();
  initConfirms();
  autoDismissAlerts();
});
