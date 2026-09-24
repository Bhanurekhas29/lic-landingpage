document.addEventListener('DOMContentLoaded', function () {
  // Mobile number: digits only, max 10
  document.querySelectorAll('#id_mobile_number').forEach(function (input) {
    input.addEventListener('input', function () {
      input.value = input.value.replace(/\D/g, '').slice(0, 10);
    });
  });

  // Consent checkbox must be checked before the application form submits
  document.querySelectorAll('.apply-form').forEach(function (form) {
    var consent = form.querySelector('#id_consent_given');
    var warning = form.querySelector('#consentWarning');
    var consentLabel = form.querySelector('.apply-form__consent');
    if (!consent || !warning) return;

    form.addEventListener('submit', function (e) {
      if (!consent.checked) {
        e.preventDefault();
        warning.hidden = false;
        if (consentLabel) consentLabel.classList.add('has-error');
        consent.focus();
      }
    });
    consent.addEventListener('change', function () {
      if (consent.checked) {
        warning.hidden = true;
        if (consentLabel) consentLabel.classList.remove('has-error');
      }
    });
  });

  // Mobile nav toggle
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      toggle.classList.toggle('is-active');
      nav.classList.toggle('is-open');
    });
    nav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        toggle.classList.remove('is-active');
        nav.classList.remove('is-open');
      });
    });
  }

  // Scroll reveal animations
  var revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && revealEls.length) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    revealEls.forEach(function (el) { observer.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('is-visible'); });
  }

  // Auto-hide flash messages
  document.querySelectorAll('.site-message').forEach(function (msg) {
    setTimeout(function () {
      msg.style.opacity = '0';
      setTimeout(function () { msg.remove(); }, 400);
    }, 6000);
  });

  // Testimonial carousel
  document.querySelectorAll('.testimonial-carousel').forEach(function (carousel) {
    var track = carousel.querySelector('.testimonial-track');
    var slides = Array.prototype.slice.call(carousel.querySelectorAll('.testimonial-slide'));
    var prevBtn = carousel.querySelector('[data-carousel-prev]');
    var nextBtn = carousel.querySelector('[data-carousel-next]');
    if (!track || !slides.length) return;

    function scrollByOne(dir) {
      var slideWidth = slides[0].getBoundingClientRect().width + 24;
      track.scrollBy({ left: dir * slideWidth, behavior: 'smooth' });
    }
    if (prevBtn) prevBtn.addEventListener('click', function () { scrollByOne(-1); });
    if (nextBtn) nextBtn.addEventListener('click', function () { scrollByOne(1); });
  });

  // Legal pages popup (Privacy Policy / Terms & Conditions / Disclaimer)
  var legalModal = document.getElementById('legalModal');
  if (legalModal && window.LEGAL_PAGES) {
    var legalTitle = document.getElementById('legalModalTitle');
    var legalBody = document.getElementById('legalModalBody');

    function openLegalModal(key) {
      var page = window.LEGAL_PAGES[key];
      if (!page) return;
      legalTitle.textContent = page.title;
      legalBody.textContent = page.content || 'This content has not been added yet.';
      legalModal.hidden = false;
      document.body.style.overflow = 'hidden';
    }
    function closeLegalModal() {
      legalModal.hidden = true;
      document.body.style.overflow = '';
    }

    document.querySelectorAll('[data-legal-modal]').forEach(function (link) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        openLegalModal(link.getAttribute('data-legal-modal'));
      });
    });
    document.querySelectorAll('[data-legal-modal-close]').forEach(function (el) {
      el.addEventListener('click', closeLegalModal);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !legalModal.hidden) closeLegalModal();
    });
  }

  // FAQ accordion
  document.querySelectorAll('.faq-item__question').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.closest('.faq-item');
      var wasOpen = item.classList.contains('is-open');
      document.querySelectorAll('.faq-item.is-open').forEach(function (open) {
        open.classList.remove('is-open');
      });
      if (!wasOpen) item.classList.add('is-open');
    });
  });
});
