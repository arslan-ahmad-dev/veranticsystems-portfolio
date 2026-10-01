/* VeranticSystems home — theme switcher, navigation, dropdowns, mobile menu, booking modal, scroll reveal, FAQ */
(function () {
  'use strict';

  /* All backend settings live in js/config.js (window.VS_CONFIG). Nothing to edit here. */
  const CFG = Object.assign({ formKey: '', bookingUrl: '', busyUrl: '', endpoints: {}, fallbackEmail: 'hello@veranticsystems.com', careersEmail: 'careers@veranticsystems.com', analytics: {} }, window.VS_CONFIG || {});
  // Cal.com (or any scheduler) link; ask Cal.com for its embed layout and match the site's current theme
  const BOOKING_URL = (() => {
    const u = (CFG.bookingUrl || '').trim(); if (!u) return '';
    if (!/cal\.com/i.test(u)) return u;
    const dark = document.documentElement.getAttribute('data-theme') === 'mono';
    return u + (u.includes('?') ? '&' : '?') + 'embed=true&layout=month_view&theme=' + (dark ? 'dark' : 'light');
  })();
  const FORM_FALLBACK_EMAIL = CFG.fallbackEmail;
  /* Language: the page's <html lang>. English is the default; French strings below are used on /fr/ pages. */
  const LANG = (document.documentElement.getAttribute('lang') || 'en').slice(0, 2);
  const FRS = {
    'Leave this field empty': 'Laissez ce champ vide',
    'Switch to light theme': 'Passer au thème clair',
    'Switch to dark theme': 'Passer au thème sombre',
    'Back to top': 'Retour en haut',
    'Link copied': 'Lien copié',
    'Job application': 'Candidature',
    'Close application form': 'Fermer le formulaire de candidature',
    'Close': 'Fermer',
    'Apply': 'Postuler',
    'Open application': 'Candidature spontanée',
    'A human reads every application and replies within a week.': 'Une vraie personne lit chaque candidature et répond sous une semaine.',
    'Your name': 'Votre nom',
    'Please tell us your name.': 'Merci de nous indiquer votre nom.',
    'Email': 'E-mail',
    'Enter a valid email address.': 'Saisissez une adresse e-mail valide.',
    'CV or LinkedIn link': 'Lien vers votre CV ou LinkedIn',
    'Add a link to your CV or profile.': 'Ajoutez un lien vers votre CV ou votre profil.',
    'Where are you based?': 'Où êtes-vous basé(e) ?',
    '(optional)': '(facultatif)',
    'City, country': 'Ville, pays',
    'Two or three things you\'ve built': 'Deux ou trois réalisations',
    '(links or a few lines)': '(liens ou quelques lignes)',
    'Accounts you set up, workflows you automated, funnels you designed...': 'Comptes configurés, workflows automatisés, tunnels conçus...',
    'Anything else we should know?': 'Autre chose à nous dire ?',
    'Availability, notice period, questions for us': 'Disponibilité, préavis, questions pour nous',
    'Send application': 'Envoyer la candidature',
    'Prefer email?': 'Vous préférez l\'e-mail ?',
    'Application received.': 'Candidature reçue.',
    'Thank you. We read every application ourselves and reply within a week, whatever the answer.': 'Merci. Nous lisons chaque candidature nous-mêmes et répondons sous une semaine, quelle que soit la réponse.',
    'We use a few cookies to measure which pages help. No ads profile, no selling data.': 'Nous utilisons quelques cookies pour mesurer quelles pages sont utiles. Aucun profil publicitaire, aucune revente de données.',
    'Details': 'Détails',
    'Decline': 'Refuser',
    'Accept': 'Accepter',
    'Cookie consent': 'Consentement aux cookies'
  };
  const T = (str) => (LANG === 'fr' && FRS[str]) || str;
  const endpointFor = (kind) => (CFG.endpoints && (CFG.endpoints[kind] || CFG.endpoints.default)) || '';

  /* ---------- Attribution: remember how the visitor arrived so every lead carries its source ---------- */
  const ATTR_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'fbclid', 'msclkid'];
  const store = { get(k) { try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch (e) { return null; } }, set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* storage unavailable */ } } };
  (function captureAttribution() {
    const q = new URLSearchParams(location.search); const touch = {};
    ATTR_KEYS.forEach((k) => { if (q.get(k)) touch[k] = q.get(k).slice(0, 200); });
    const first = store.get('vs-first-touch');
    if (!first) store.set('vs-first-touch', Object.assign({ landing_page: location.pathname, referrer: document.referrer || '', at: new Date().toISOString() }, touch));
    if (Object.keys(touch).length) store.set('vs-last-touch', Object.assign({ at: new Date().toISOString() }, touch));
  })();
  const pageLoadedAt = Date.now();

  /* ---------- Lead submission: one function for every form (contact, booking, newsletter, careers) ----------
     With config.formKey the lead is emailed to the owner through Web3Forms; with config.endpoints it is POSTed as flat JSON to that URL.
     Returns { ok, mode } where mode is 'endpoint' | 'mailto' | 'spam'. Throws only when an endpoint is set and unreachable. */
  async function submitLead(kind, fields, opts) {
    opts = opts || {};
    if (fields._hp) return { ok: true, mode: 'spam' };                      // honeypot filled: pretend success, send nothing
    if (Date.now() - pageLoadedAt < 1500) return { ok: true, mode: 'spam' }; // no human submits a form in under 1.5s
    const first = store.get('vs-first-touch') || {}, last = store.get('vs-last-touch') || {};
    const name = (fields.name || '').trim();
    const payload = Object.assign({
      type: kind, source: 'website', site: location.hostname, page: location.pathname, page_title: document.title,
      submitted_at: new Date().toISOString(), timezone: (Intl.DateTimeFormat().resolvedOptions().timeZone) || '', language: navigator.language || '',
      full_name: name, first_name: name.split(/\s+/)[0] || '', last_name: name.split(/\s+/).slice(1).join(' '),
      landing_page: first.landing_page || '', referrer: first.referrer || '',
      tags: ['website', 'website-' + kind].concat(opts.tags || []).join(','),
    }, fields);
    delete payload._hp; delete payload.name;
    ATTR_KEYS.forEach((k) => { payload[k] = last[k] || first[k] || ''; payload['first_' + k] = first[k] || ''; });
    let url = endpointFor(kind);
    let viaFormService = false;
    if (!url && CFG.formKey) {
      // Web3Forms: free form-to-email delivery. It emails every field it receives, so send a clear subject and drop the empty ones.
      url = CFG.formApi || 'https://api.web3forms.com/submit'; viaFormService = true;
      const who = payload.full_name || payload.email || 'a visitor';
      const subject = opts.subject || { contact: 'New enquiry from ' + who, booking: 'New call booking: ' + who + (fields.owner_time ? ' · ' + fields.owner_time.replace(/\s*\([^)]*\)\s*$/, '') + ' PKT' : ''), newsletter: 'Newsletter signup: ' + (payload.email || ''), careers: 'Job application: ' + (fields.role || 'Open application') + ' · ' + who }[kind] || 'Website form: ' + kind;
      ['source', 'site', 'language', 'page_title', 'submitted_at', 'first_name', 'last_name', 'tags'].forEach((k) => delete payload[k]);   // noise in an email
      if (kind === 'booking') {
        // A person reads this, so lead with the call time in Pakistan time and drop the raw UTC timestamps (they look 5 hours "wrong").
        const pk = (fields.owner_time || '').replace(/\s*\([^)]*\)\s*$/, '');
        const ordered = {
          'Status': fields.booking_status || '',
          'Call time (Pakistan)': pk ? pk + ' PKT' : '',
          'Client local time': (fields.visitor_time || '') + (fields.visitor_timezone ? ' (' + fields.visitor_timezone.split('/').pop().replace(/_/g, ' ') + ')' : ''),
          'Length': (fields.appointment_minutes || 30) + ' minutes',
        };
        ['appointment_start', 'appointment_end', 'appointment_minutes', 'appointment_title', 'owner_time', 'visitor_time', 'visitor_timezone', 'timezone', 'booking_status'].forEach((k) => delete payload[k]);
        const rest = Object.assign({}, payload); Object.keys(payload).forEach((k) => delete payload[k]);
        Object.assign(payload, ordered, rest);
      }
      ATTR_KEYS.forEach((k) => { if (payload['first_' + k] === payload[k]) delete payload['first_' + k]; });
      Object.keys(payload).forEach((k) => { if (payload[k] === '' || payload[k] == null) delete payload[k]; });
      Object.assign(payload, { access_key: CFG.formKey, subject, from_name: 'VeranticSystems website', replyto: payload.email || '' });
    }
    if (!url) return { ok: true, mode: 'mailto', payload };
    const ctrl = ('AbortController' in window) ? new AbortController() : null;
    const timer = ctrl ? setTimeout(() => ctrl.abort(), 12000) : null;
    try {
      const res = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(payload), signal: ctrl ? ctrl.signal : undefined });
      if (!res.ok) throw new Error('HTTP ' + res.status);
      if (viaFormService) { const j = await res.json().catch(() => ({})); if (j && j.success === false) throw new Error(j.message || 'Form service rejected the submission'); }
    } catch (err) {
      if (!(err instanceof TypeError)) throw err;   // a real HTTP error or timeout: let the form show its error state
      // TypeError = network/CORS. Some webhook hosts don't answer CORS preflights, so retry as a "simple" form-encoded request; the reply is opaque, so reaching the server counts as sent.
      await fetch(url, { method: 'POST', mode: 'no-cors', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(payload).toString() });
    } finally { if (timer) clearTimeout(timer); }
    track(kind === 'newsletter' ? 'sign_up' : 'generate_lead', { form: kind });
    return { ok: true, mode: 'endpoint', payload };
  }
  function track(event, params) {
    try {
      if (window.gtag) window.gtag('event', event, params || {});
      if (window.fbq) window.fbq('track', event === 'sign_up' ? 'Subscribe' : event === 'generate_lead' ? 'Lead' : event, params || {});
      if (window.plausible) window.plausible(event, { props: params || {} });
    } catch (e) { /* analytics must never break a form */ }
  }
  const mailtoHref = (to, subject, lines) => 'mailto:' + to + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n'));
  // honeypot: a field humans never see; bots that fill every input give themselves away
  function addHoneypot(form) {
    const w = document.createElement('div'); w.setAttribute('aria-hidden', 'true'); w.style.cssText = 'position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden';
    w.innerHTML = '<label>' + T('Leave this field empty') + '<input type="text" name="_hp" tabindex="-1" autocomplete="off"></label>'; form.appendChild(w);
  }
  function showFormError(form, to) {
    let el = form.querySelector('.form-error');
    if (!el) { el = document.createElement('p'); el.className = 'form-error'; el.setAttribute('role', 'alert'); form.appendChild(el); }
    el.innerHTML = LANG === 'fr'
      ? 'Désolé, l\'envoi n\'a pas abouti. Veuillez réessayer ou écrire à <a href="mailto:' + to + '">' + to + '</a> et nous prendrons le relais.'
      : 'Sorry, that didn\'t go through. Please try again, or email <a href="mailto:' + to + '">' + to + '</a> and we\'ll pick it up from there.';
    el.hidden = false;
  }
  // No delivery configured: never launch an email app on the visitor's machine. Show the address and let them choose.
  function showNotConnected(form, to, href) {
    let el = form.querySelector('.form-error');
    if (!el) { el = document.createElement('p'); el.className = 'form-error'; el.setAttribute('role', 'alert'); form.appendChild(el); }
    el.innerHTML = LANG === 'fr'
      ? 'Ce formulaire n\'est pas encore connecté. Veuillez écrire à <a href="' + href + '">' + to + '</a> et nous répondrons sous un jour ouvré.'
      : 'This form is not connected yet. Please email <a href="' + href + '">' + to + '</a> and we will reply within one working day.';
    el.hidden = false;
  }
  const clearFormError = (form) => { const el = form.querySelector('.form-error'); if (el) el.hidden = true; };
  window.VS = { submitLead, track, config: CFG };

  /* ---------- Theme toggle (header): light = Light Blue "sky", dark = Black & White "mono" ---------- */
  const THEMES = ['sky', 'mono'];
  const toggles = Array.from(document.querySelectorAll('[data-theme-toggle]'));
  function applyTheme(theme, persist) {
    if (!THEMES.includes(theme)) theme = 'sky';
    const html = document.documentElement;
    html.setAttribute('data-theme', theme);
    const dark = theme === 'mono';
    toggles.forEach((b) => { b.setAttribute('aria-label', dark ? T('Switch to light theme') : T('Switch to dark theme')); b.setAttribute('aria-pressed', String(dark)); });
    // favicon + browser chrome colour follow the theme (SVG icon only; the PNG fallbacks stay blue)
    document.querySelectorAll('link[rel="icon"][type="image/svg+xml"]').forEach((l) => { l.setAttribute('href', l.getAttribute('href').replace(/favicon(-mono)?\.svg/, dark ? 'favicon-mono.svg' : 'favicon.svg')); });
    const tc = document.querySelector('meta[name="theme-color"]'); if (tc) tc.setAttribute('content', dark ? '#0B0B0C' : '#FFFFFF');
    if (persist) { try { localStorage.setItem('vs-theme', theme); } catch (e) { /* storage unavailable */ } }
    window.dispatchEvent(new CustomEvent('themechange', { detail: theme }));
  }
  applyTheme(document.documentElement.getAttribute('data-theme') || 'sky', false);
  toggles.forEach((b) => b.addEventListener('click', () => {
    const next = document.documentElement.getAttribute('data-theme') === 'mono' ? 'sky' : 'mono';
    // brief class so the whole page cross-fades instead of snapping
    document.documentElement.classList.add('theme-fading');
    b.classList.remove('is-spin'); void b.offsetWidth; b.classList.add('is-spin');
    applyTheme(next, true);
    setTimeout(() => document.documentElement.classList.remove('theme-fading'), 450);
  }));

  /* ---------- Nav: scrolled state ---------- */
  const nav = document.getElementById('nav');
  function onScroll() { nav.classList.toggle('is-scrolled', window.scrollY > 20); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Nav: dropdowns ---------- */
  const groups = Array.from(document.querySelectorAll('.nav__group'));
  groups.forEach((group) => {
    const btn = group.querySelector('.nav__chev');
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const open = group.classList.contains('is-open');
      groups.forEach((g) => { g.classList.remove('is-open'); g.querySelector('.nav__chev').setAttribute('aria-expanded', 'false'); });
      if (!open) { group.classList.add('is-open'); btn.setAttribute('aria-expanded', 'true'); }
    });
  });
  document.addEventListener('mousedown', (e) => {
    groups.forEach((g) => {
      if (!g.contains(e.target)) { g.classList.remove('is-open'); g.querySelector('.nav__chev').setAttribute('aria-expanded', 'false'); }
    });
  });

  /* ---------- Nav: mobile menu ---------- */
  const burger = document.getElementById('nav-burger');
  const mobileMenu = document.getElementById('mobile-menu');
  function setMobile(open) {
    if (!burger || !mobileMenu) return;
    burger.classList.toggle('is-open', open);
    mobileMenu.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', String(open));
  }
  if (burger) burger.addEventListener('click', () => setMobile(!mobileMenu.classList.contains('is-open')));
  if (mobileMenu) mobileMenu.querySelectorAll('a, button').forEach((el) => el.addEventListener('click', () => setMobile(false)));

  /* ---------- Booking modal ---------- */
  const modal = document.getElementById('booking-modal');
  const modalFrame = modal.querySelector('iframe');
  const modalPlaceholder = modal.querySelector('.modal__placeholder');
  let lastFocus = null;
  let bookingApp = null, bookingLoading = null;
  const scriptBase = (() => { const s = document.querySelector('script[src$="js/main.js"]'); return s ? s.getAttribute('src').replace(/js\/main\.js$/, '') : ''; })();
  function loadBookingCalendar() {
    if (window.VSBooking) return Promise.resolve();
    if (bookingLoading) return bookingLoading;
    bookingLoading = new Promise((resolve, reject) => {
      const s = document.createElement('script'); s.src = scriptBase + 'js/booking.js'; s.onload = resolve; s.onerror = reject; document.head.appendChild(s);
    });
    return bookingLoading;
  }
  function openBooking() {
    lastFocus = document.activeElement;
    const panel = modal.querySelector('.modal__panel');
    if (BOOKING_URL) {
      // external scheduler (Cal.com): themed frame, a loading note until it paints, and the site's current theme passed along
      panel.classList.add('modal__panel--frame');
      if (!modalFrame.getAttribute('src')) {
        panel.classList.add('is-loading');
        modalFrame.addEventListener('load', () => panel.classList.remove('is-loading'), { once: true });
        modalFrame.setAttribute('title', 'Book a call');
        modalFrame.setAttribute('src', BOOKING_URL);
      }
      modalFrame.hidden = false;
      if (modalPlaceholder) modalPlaceholder.hidden = true;
      track('booking_opened', {});
    } else {
      panel.classList.add('modal__panel--bk');
      loadBookingCalendar().then(() => {
        if (!bookingApp) bookingApp = window.VSBooking.mount(modal.querySelector('.modal__body'), { endpoint: endpointFor('booking'), submit: (fields) => submitLead('booking', fields, { tags: ['crm-audit'] }), busyUrl: CFG.busyUrl || '', email: FORM_FALLBACK_EMAIL, reduce: window.matchMedia('(prefers-reduced-motion: reduce)').matches });
        else bookingApp.reset();
      }).catch(() => { if (modalPlaceholder) modalPlaceholder.hidden = false; });
    }
    modal.classList.add('is-open');
    document.body.classList.add('modal-open');
    modal.querySelector('.modal__close').focus();
  }
  if (new URLSearchParams(location.search).get('book') === '1') setTimeout(openBooking, 300);
  function closeBooking() {
    modal.classList.remove('is-open');
    document.body.classList.remove('modal-open');
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  document.querySelectorAll('[data-book]').forEach((el) => el.addEventListener('click', (e) => { e.preventDefault(); openBooking(); }));
  modal.querySelector('.modal__backdrop').addEventListener('click', closeBooking);
  modal.querySelector('.modal__close').addEventListener('click', closeBooking);
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && modal.classList.contains('is-open')) closeBooking(); });

  /* ---------- Scroll reveal ---------- */
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealTargets = Array.from(document.querySelectorAll('[data-reveal], [data-stagger]'));
  document.querySelectorAll('[data-stagger]').forEach((wrap) => {
    const step = parseFloat(wrap.getAttribute('data-stagger')) || 0.08;
    // cap the delay so long lists (36 article cards) never leave items invisible for seconds on a fast scroll
    Array.from(wrap.children).forEach((child, i) => { child.style.transitionDelay = Math.min(i * step, 0.6).toFixed(2) + 's'; });
  });
  if (reduce || !('IntersectionObserver' in window)) {
    revealTargets.forEach((el) => el.classList.add('is-visible'));
  } else {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) { entry.target.classList.add('is-visible'); io.unobserve(entry.target); }
      });
    }, { rootMargin: '0px 0px -60px 0px', threshold: 0 });
    revealTargets.forEach((el) => io.observe(el));
  }

  /* ---------- FAQ accordion ---------- */
  const faqItems = Array.from(document.querySelectorAll('.faq-item'));
  faqItems.forEach((item) => {
    const btn = item.querySelector('.faq-item__btn');
    btn.addEventListener('click', () => {
      const open = item.classList.contains('is-open');
      faqItems.forEach((it) => { it.classList.remove('is-open'); it.querySelector('.faq-item__btn').setAttribute('aria-expanded', 'false'); });
      if (!open) { item.classList.add('is-open'); btn.setAttribute('aria-expanded', 'true'); }
    });
  });

  /* ---------- Contact form ---------- */
  const cform = document.getElementById('contact-form');
  if (cform) {
    // Country dialling-code dropdown (list in js/countries.js), default from data-default (GB)
    const dial = document.getElementById('cf-dial');
    if (dial && Array.isArray(window.VS_COUNTRIES)) {
      const def = dial.getAttribute('data-default') || 'GB';
      window.VS_COUNTRIES.forEach(([name, iso, code]) => {
        const opt = document.createElement('option');
        opt.value = code; opt.textContent = iso + ' ' + code; opt.setAttribute('data-name', name); opt.title = name;
        if (iso === def) opt.selected = true;
        dial.appendChild(opt);
      });
    }
    const fieldOf = (input) => input.closest('.field');
    const validate = () => {
      let ok = true;
      cform.querySelectorAll('input[required], textarea[required]').forEach((input) => {
        const valid = input.type === 'email' ? /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value.trim()) : input.value.trim().length > 0;
        fieldOf(input).classList.toggle('is-invalid', !valid);
        if (!valid && ok) { input.focus(); ok = false; }
      });
      return ok;
    };
    cform.querySelectorAll('input, textarea').forEach((el) => el.addEventListener('input', () => fieldOf(el) && fieldOf(el).classList.remove('is-invalid')));
    addHoneypot(cform);
    cform.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (!validate() || cform.classList.contains('is-sending')) return;
      clearFormError(cform);
      const data = new FormData(cform);
      const needs = data.getAll('need').join(', ') || 'Not specified';
      const rawPhone = (data.get('phone') || '').trim();
      const phone = rawPhone ? ((data.get('dial') || '') + ' ' + rawPhone).replace(/\s+/g, ' ').trim() : '';
      const dialOpt = dial && dial.selectedOptions[0];
      const fields = { _hp: data.get('_hp'), name: data.get('name'), email: (data.get('email') || '').trim(), company: data.get('company') || '', phone, country: (rawPhone && dialOpt && dialOpt.getAttribute('data-name')) || '', needs, budget: data.get('budget') || 'Not specified', timeline: data.get('timeline') || 'Flexible', message: data.get('message') || '' };
      cform.classList.add('is-sending');
      try {
        const res = await submitLead('contact', fields, { tags: needs === 'Not specified' ? [] : needs.split(', ').map((n) => 'need-' + n.toLowerCase().replace(/[^a-z0-9]+/g, '-')) });
        if (res.mode === 'mailto') { showNotConnected(cform, FORM_FALLBACK_EMAIL, mailtoHref(FORM_FALLBACK_EMAIL, 'Project enquiry from ' + fields.name, ['Name: ' + fields.name, 'Email: ' + fields.email, 'Company: ' + (fields.company || '-'), 'Phone: ' + (fields.phone || '-'), 'Needs: ' + fields.needs, 'Budget: ' + fields.budget, 'Timeline: ' + fields.timeline, '', fields.message])); return; }
        cform.classList.add('is-sent');
      } catch (err) {
        showFormError(cform, FORM_FALLBACK_EMAIL);
      } finally {
        cform.classList.remove('is-sending');
      }
    });
  }

  /* ---------- Careers: role accordions + filters ---------- */
  const roles = Array.from(document.querySelectorAll('.role'));
  roles.forEach((role) => {
    const btn = role.querySelector('.role__btn');
    btn.addEventListener('click', () => {
      const open = role.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', String(open));
    });
  });
  const filterBtns = Array.from(document.querySelectorAll('[data-filter]'));
  const rolesEmpty = document.querySelector('.roles__empty');
  filterBtns.forEach((btn) => btn.addEventListener('click', () => {
    const team = btn.getAttribute('data-filter');
    filterBtns.forEach((b) => b.setAttribute('aria-pressed', String(b === btn)));
    let shown = 0;
    roles.forEach((role) => {
      const match = team === 'all' || role.getAttribute('data-team') === team;
      if (match) {
        role.classList.remove('is-hidden'); role.classList.add('is-leaving');
        requestAnimationFrame(() => requestAnimationFrame(() => role.classList.remove('is-leaving')));
        shown++;
      } else {
        role.classList.add('is-hidden'); role.classList.remove('is-open');
        role.querySelector('.role__btn').setAttribute('aria-expanded', 'false');
      }
    });
    if (rolesEmpty) rolesEmpty.hidden = shown > 0;
  }));

  /* ---------- Count-up numbers ---------- */
  const counters = Array.from(document.querySelectorAll('[data-count]'));
  const runCounter = (el) => {
    const target = parseFloat(el.getAttribute('data-count')) || 0;
    const suffix = el.getAttribute('data-suffix') || '';
    const prefix = el.getAttribute('data-prefix') || '';
    const start = performance.now(); const dur = 1200;
    const tick = (now) => {
      const p = Math.min((now - start) / dur, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = prefix + Math.round(target * eased) + suffix;
      if (p < 1) requestAnimationFrame(tick); else el.classList.add('is-done');
    };
    requestAnimationFrame(tick);
  };
  if (counters.length) {
    if (reduce || !('IntersectionObserver' in window)) {
      counters.forEach((el) => { el.textContent = (el.getAttribute('data-prefix') || '') + el.getAttribute('data-count') + (el.getAttribute('data-suffix') || ''); });
    } else {
      const cio = new IntersectionObserver((entries) => {
        entries.forEach((entry) => { if (entry.isIntersecting) { runCounter(entry.target); cio.unobserve(entry.target); } });
      }, { threshold: .4 });
      counters.forEach((el) => cio.observe(el));
    }
  }

  /* ---------- Card tilt (pointer devices only) ---------- */
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  if (finePointer && !reduce) {
    document.querySelectorAll('.card[data-tilt]').forEach((card) => {
      const glare = document.createElement('span');
      glare.className = 'card__glare';
      card.appendChild(glare);
      const MAX = 5; // degrees
      card.addEventListener('pointermove', (e) => {
        const r = card.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
        card.style.setProperty('--ry', ((px - 0.5) * MAX * 2).toFixed(2) + 'deg');
        card.style.setProperty('--rx', ((0.5 - py) * MAX * 2).toFixed(2) + 'deg');
        card.style.setProperty('--gx', (px * 100).toFixed(1) + '%');
        card.style.setProperty('--gy', (py * 100).toFixed(1) + '%');
        card.style.setProperty('--lift', '-4px');
      });
      card.addEventListener('pointerleave', () => {
        card.style.setProperty('--rx', '0deg'); card.style.setProperty('--ry', '0deg'); card.style.setProperty('--lift', '0px');
      });
    });
  }

  /* ---------- Scroll progress bar + back to top ---------- */
  const progress = document.createElement('div');
  progress.className = 'scroll-progress'; progress.setAttribute('aria-hidden', 'true');
  document.body.appendChild(progress);
  const toTop = document.createElement('button');
  toTop.type = 'button'; toTop.className = 'to-top'; toTop.setAttribute('aria-label', T('Back to top'));
  toTop.innerHTML = '<svg class="i" viewBox="0 0 24 24"><path d="m18 15-6-6-6 6"/></svg>';
  toTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }));
  document.body.appendChild(toTop);
  function onProgress() {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    const p = max > 0 ? window.scrollY / max : 0;
    progress.style.transform = 'scaleX(' + p.toFixed(4) + ')';
    toTop.classList.toggle('is-visible', window.scrollY > 600);
  }
  window.addEventListener('scroll', onProgress, { passive: true });
  window.addEventListener('resize', onProgress, { passive: true });
  onProgress();

  /* ---------- Insights: topic filter + search ---------- */
  const posts = Array.from(document.querySelectorAll('[data-post]'));
  if (posts.length) {
    const postFilters = Array.from(document.querySelectorAll('[data-post-filter]'));
    const searchInput = document.getElementById('post-search');
    const postsEmpty = document.querySelector('.posts__empty');
    let topic = 'all', query = '';
    const applyPosts = () => {
      let shown = 0;
      posts.forEach((p) => {
        const inTopic = topic === 'all' || p.getAttribute('data-topic') === topic;
        const hay = (p.textContent + ' ' + (p.getAttribute('data-search-text') || '')).toLowerCase();
        const inQuery = !query || query.split(/\s+/).every((w) => hay.includes(w));
        const show = inTopic && inQuery;
        const wasHidden = p.classList.contains('is-hidden');
        p.classList.toggle('is-hidden', !show);
        if (show) { shown++; if (wasHidden || animateAll) { p.classList.remove('is-entering'); void p.offsetWidth; p.classList.add('is-entering'); } }
      });
      if (postsEmpty) postsEmpty.hidden = shown > 0;
      animateAll = false;
    };
    let animateAll = false;
    const pickTopic = (name) => {
      topic = name; animateAll = true;
      postFilters.forEach((x) => x.setAttribute('aria-pressed', String(x.getAttribute('data-post-filter') === name)));
      applyPosts();
    };
    postFilters.forEach((b) => b.addEventListener('click', () => pickTopic(b.getAttribute('data-post-filter'))));
    document.querySelectorAll('[data-ticker-topic]').forEach((b) => b.addEventListener('click', () => {
      pickTopic(b.getAttribute('data-ticker-topic'));
      const grid = document.getElementById('posts'); if (grid) grid.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    }));
    if (searchInput) {
      searchInput.addEventListener('input', () => { query = searchInput.value.trim().toLowerCase(); applyPosts(); });
      document.addEventListener('keydown', (e) => {
        if (e.key === '/' && document.activeElement !== searchInput && !/input|textarea/i.test(document.activeElement.tagName)) { e.preventDefault(); searchInput.focus(); }
      });
    }
  }

  /* ---------- Newsletter ---------- */
  const nlForm = document.getElementById('newsletter-form');
  if (nlForm) {
    addHoneypot(nlForm);
    nlForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (nlForm.classList.contains('is-sending')) return;
      const input = nlForm.querySelector('input[type="email"]');
      const email = input.value.trim();
      const ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
      input.closest('.field').classList.toggle('is-invalid', !ok);
      if (!ok) { input.focus(); return; }
      clearFormError(nlForm);
      nlForm.classList.add('is-sending');
      try {
        const hp = nlForm.querySelector('[name="_hp"]');
        const res = await submitLead('newsletter', { _hp: hp && hp.value, email }, { tags: ['newsletter'] });
        if (res.mode === 'mailto') { showNotConnected(nlForm, FORM_FALLBACK_EMAIL, mailtoHref(FORM_FALLBACK_EMAIL, 'Newsletter subscription', ['Please add ' + email + ' to the newsletter.'])); return; }
        nlForm.classList.add('is-sent');
        nlForm.querySelector('.newsletter__ok').hidden = false;
      } catch (err) {
        showFormError(nlForm, FORM_FALLBACK_EMAIL);
      } finally { nlForm.classList.remove('is-sending'); }
    });
  }

  /* ---------- Careers: application form (opens from any "Apply" link; the mailto href stays as the no-JS fallback) ---------- */
  const applyLinks = Array.from(document.querySelectorAll('a[href^="mailto:careers@"]'));
  if (applyLinks.length) {
    const dlg = document.createElement('div');
    dlg.className = 'modal apply-modal'; dlg.setAttribute('role', 'dialog'); dlg.setAttribute('aria-modal', 'true'); dlg.setAttribute('aria-label', T('Job application'));
    dlg.innerHTML = '<button type="button" class="modal__backdrop" aria-label="' + T('Close application form') + '"></button>' +
      '<div class="modal__panel apply-modal__panel"><button type="button" class="modal__close" aria-label="' + T('Close') + '"><svg class="i" viewBox="0 0 24 24"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg></button>' +
      '<form class="apply-form cform" novalidate>' +
      '<p class="eyebrow">' + T('Apply') + '</p><h2 class="apply-form__title">' + T('Open application') + '</h2><p class="apply-form__lead">' + T('A human reads every application and replies within a week.') + '</p>' +
      '<div class="cform__row"><div class="field"><label for="ap-name">' + T('Your name') + '</label><input id="ap-name" name="name" type="text" autocomplete="name" placeholder="Emily Carter" required><span class="field__error">' + T('Please tell us your name.') + '</span></div>' +
      '<div class="field"><label for="ap-email">' + T('Email') + '</label><input id="ap-email" name="email" type="email" autocomplete="email" placeholder="you@email.com" required><span class="field__error">' + T('Enter a valid email address.') + '</span></div></div>' +
      '<div class="cform__row"><div class="field"><label for="ap-link">' + T('CV or LinkedIn link') + '</label><input id="ap-link" name="profile_url" type="url" inputmode="url" placeholder="https://linkedin.com/in/..." required><span class="field__error">' + T('Add a link to your CV or profile.') + '</span></div>' +
      '<div class="field"><label for="ap-loc">' + T('Where are you based?') + ' <small>' + T('(optional)') + '</small></label><input id="ap-loc" name="location" type="text" placeholder="' + T('City, country') + '"></div></div>' +
      '<div class="field"><label for="ap-work">' + T('Two or three things you\'ve built') + ' <small>' + T('(links or a few lines)') + '</small></label><textarea id="ap-work" name="work_samples" rows="3" placeholder="' + T('Accounts you set up, workflows you automated, funnels you designed...') + '"></textarea></div>' +
      '<div class="field"><label for="ap-note">' + T('Anything else we should know?') + ' <small>' + T('(optional)') + '</small></label><textarea id="ap-note" name="message" rows="2" placeholder="' + T('Availability, notice period, questions for us') + '"></textarea></div>' +
      '<div class="cform__foot"><button type="submit" class="btn-primary btn-shimmer">' + T('Send application') + '<span aria-hidden="true">→</span></button><p class="cform__note">' + T('Prefer email?') + ' <a data-apply-mail href="#">' + CFG.careersEmail + '</a></p></div>' +
      '<div class="cform__success" role="status" aria-live="polite"><svg class="check" viewBox="0 0 90 90" aria-hidden="true"><circle cx="45" cy="45" r="41"/><path d="M28 46 l11 11 l24 -25"/></svg><h3>' + T('Application received.') + '</h3><p>' + T('Thank you. We read every application ourselves and reply within a week, whatever the answer.') + '</p></div>' +
      '</form></div>';
    document.body.appendChild(dlg);
    const aform = dlg.querySelector('form'); let role = 'Open application', lastApplyFocus = null;
    addHoneypot(aform);
    const closeApply = () => { dlg.classList.remove('is-open'); document.body.classList.remove('modal-open'); if (lastApplyFocus) lastApplyFocus.focus(); };
    applyLinks.forEach((a) => a.addEventListener('click', (e) => {
      e.preventDefault(); lastApplyFocus = a;
      const roleEl = a.closest('.role'); role = roleEl ? roleEl.querySelector('.role__title').textContent.trim() : 'Open application';
      aform.classList.remove('is-sent'); aform.reset(); clearFormError(aform);
      dlg.querySelector('.apply-form__title').textContent = role;
      dlg.querySelector('[data-apply-mail]').setAttribute('href', a.getAttribute('href'));
      dlg.classList.add('is-open'); document.body.classList.add('modal-open');
      setTimeout(() => dlg.querySelector('#ap-name').focus(), 60);
    }));
    dlg.querySelector('.modal__backdrop').addEventListener('click', closeApply);
    dlg.querySelector('.modal__close').addEventListener('click', closeApply);
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && dlg.classList.contains('is-open')) closeApply(); });
    aform.querySelectorAll('input, textarea').forEach((el) => el.addEventListener('input', () => el.closest('.field').classList.remove('is-invalid')));
    aform.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (aform.classList.contains('is-sending')) return;
      let ok = true;
      aform.querySelectorAll('[required]').forEach((input) => {
        const v = input.value.trim();
        const valid = input.type === 'email' ? /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) : input.type === 'url' ? /^(https?:\/\/)?[^\s.]+\.[^\s]{2,}$/i.test(v) : v.length > 0;
        input.closest('.field').classList.toggle('is-invalid', !valid);
        if (!valid && ok) { input.focus(); ok = false; }
      });
      if (!ok) return;
      clearFormError(aform);
      const d = new FormData(aform);
      const fields = { _hp: d.get('_hp'), name: d.get('name'), email: (d.get('email') || '').trim(), role, profile_url: d.get('profile_url'), location: d.get('location') || '', work_samples: d.get('work_samples') || '', message: d.get('message') || '' };
      aform.classList.add('is-sending');
      try {
        const res = await submitLead('careers', fields, { tags: ['applicant', 'role-' + role.toLowerCase().replace(/[^a-z0-9]+/g, '-')] });
        if (res.mode === 'mailto') { showNotConnected(aform, CFG.careersEmail, mailtoHref(CFG.careersEmail, 'Application: ' + role, ['Role: ' + role, 'Name: ' + fields.name, 'Email: ' + fields.email, 'CV / profile: ' + fields.profile_url, 'Location: ' + (fields.location || '-'), '', 'Work samples:', fields.work_samples || '-', '', fields.message])); return; }
        aform.classList.add('is-sent');
      } catch (err) { showFormError(aform, CFG.careersEmail); } finally { aform.classList.remove('is-sending'); }
    });
  }

  /* ---------- Clean URLs for in-page sections ----------
     "Services" and similar links scroll to a section of the page. Scroll there, but keep the address bar clean (no #services).
     Tables of contents in articles and legal pages keep their #anchors on purpose: those are useful to share. */
  (function cleanSectionLinks() {
    const go = (id, smooth) => {
      const el = id && document.getElementById(id); if (!el) return false;
      el.scrollIntoView({ behavior: smooth && !reduce ? 'smooth' : 'auto', block: 'start' });
      return true;
    };
    const strip = () => history.replaceState(null, '', location.pathname + location.search);
    document.addEventListener('click', (e) => {
      const a = e.target.closest && e.target.closest('a[href*="#"]'); if (!a || a.closest('.toc') || a.target === '_blank') return;
      let url; try { url = new URL(a.getAttribute('href'), location.href); } catch (err) { return; }
      if (url.origin !== location.origin || url.pathname !== location.pathname || url.hash.length < 2) return;
      const id = decodeURIComponent(url.hash.slice(1)); if (id === 'main') return;          // the skip link must move focus the normal way
      if (go(id, true)) { e.preventDefault(); strip(); }
    });
    // the # changed without a reload (typed by hand, or a link this handler didn't catch)
    window.addEventListener('hashchange', () => {
      if (location.hash.length < 2 || document.querySelector('.toc')) return;
      const id = decodeURIComponent(location.hash.slice(1)); if (id !== 'main' && go(id, true)) strip();
    });
    // arriving from another page as /#services: land on the section, then tidy the address
    if (location.hash.length > 1 && !document.querySelector('.toc')) {
      const id = decodeURIComponent(location.hash.slice(1));
      if (id !== 'main') {
        let done = false;
        const land = () => { if (done) return; done = true; if (go(id, false)) strip(); };
        // don't depend on the load event alone: a slow font or embed can hold it back for seconds
        if (document.readyState === 'complete') setTimeout(land, 80); else { window.addEventListener('load', () => setTimeout(land, 80)); setTimeout(land, 900); }
      }
    }
  })();

  /* ---------- FAQ page: live search across every question ---------- */
  const faqSearch = document.querySelector('[data-faq-search] input');
  if (faqSearch) {
    const items = Array.from(document.querySelectorAll('[data-faq]')).map((el) => ({ el, q: el.querySelector('h3'), text: el.textContent.toLowerCase(), label: el.querySelector('h3').textContent }));
    const groups = Array.from(document.querySelectorAll('[data-faq-group]')), empty = document.querySelector('[data-faq-empty]');
    const escHtml = (s) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
    faqSearch.addEventListener('input', () => {
      const term = faqSearch.value.trim().toLowerCase(); let shown = 0;
      items.forEach((it) => {
        const match = !term || it.text.includes(term); it.el.hidden = !match; if (match) shown++;
        const i = term ? it.label.toLowerCase().indexOf(term) : -1;
        it.q.innerHTML = i < 0 ? escHtml(it.label) : escHtml(it.label.slice(0, i)) + '<mark>' + escHtml(it.label.slice(i, i + term.length)) + '</mark>' + escHtml(it.label.slice(i + term.length));
      });
      groups.forEach((g) => { g.hidden = !g.querySelector('[data-faq]:not([hidden])'); });
      if (empty) empty.hidden = shown > 0;
    });
  }

  /* ---------- Analytics + cookie consent (only when IDs are set in js/config.js) ---------- */
  (function analytics() {
    const A = CFG.analytics || {};
    const inject = (src, attrs) => { const s = document.createElement('script'); s.async = true; s.src = src; Object.keys(attrs || {}).forEach((k) => s.setAttribute(k, attrs[k])); document.head.appendChild(s); return s; };
    if (A.plausibleDomain) { inject('https://plausible.io/js/script.js', { 'data-domain': A.plausibleDomain, defer: '' }); window.plausible = window.plausible || function () { (window.plausible.q = window.plausible.q || []).push(arguments); }; }
    if (!A.ga4 && !A.metaPixel) return;                              // nothing that needs consent
    const loadTrackers = () => {
      if (A.ga4 && !window.gtag) { window.dataLayer = window.dataLayer || []; window.gtag = function () { window.dataLayer.push(arguments); }; window.gtag('js', new Date()); window.gtag('config', A.ga4, { anonymize_ip: true }); inject('https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(A.ga4)); }
      if (A.metaPixel && !window.fbq) { const n = window.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); }; n.push = n; n.loaded = true; n.version = '2.0'; n.queue = []; inject('https://connect.facebook.net/en_US/fbevents.js'); window.fbq('init', A.metaPixel); window.fbq('track', 'PageView'); }
    };
    let consent = null; try { consent = localStorage.getItem('vs-consent'); } catch (e) { /* storage unavailable */ }
    if (consent === 'yes') return loadTrackers();
    if (consent === 'no') return;
    const bar = document.createElement('div'); bar.className = 'consent'; bar.setAttribute('role', 'region'); bar.setAttribute('aria-label', T('Cookie consent'));
    bar.innerHTML = '<p>' + T('We use a few cookies to measure which pages help. No ads profile, no selling data.') + ' <a href="' + scriptBase + (LANG === 'fr' ? 'fr/' : '') + 'privacy/#cookies">' + T('Details') + '</a></p><div class="consent__actions"><button type="button" class="btn-outline" data-consent="no">' + T('Decline') + '</button><button type="button" class="btn-primary" data-consent="yes">' + T('Accept') + '</button></div>';
    document.body.appendChild(bar);
    requestAnimationFrame(() => bar.classList.add('is-visible'));
    bar.querySelectorAll('[data-consent]').forEach((b) => b.addEventListener('click', () => {
      const v = b.getAttribute('data-consent'); try { localStorage.setItem('vs-consent', v); } catch (e) { /* ignore */ }
      bar.classList.remove('is-visible'); setTimeout(() => bar.remove(), 300); if (v === 'yes') loadTrackers();
    }));
  })();

  /* ---------- Article: table of contents highlight + share ---------- */
  const tocLinks = Array.from(document.querySelectorAll('.toc a[href^="#"]'));
  if (tocLinks.length && 'IntersectionObserver' in window) {
    const headings = tocLinks.map((a) => document.getElementById(a.getAttribute('href').slice(1))).filter(Boolean);
    const setActive = (id) => tocLinks.forEach((a) => a.classList.toggle('is-active', a.getAttribute('href') === '#' + id));
    const tio = new IntersectionObserver((entries) => {
      const visible = entries.filter((en) => en.isIntersecting).sort((x, y) => x.boundingClientRect.top - y.boundingClientRect.top);
      if (visible.length) setActive(visible[0].target.id);
    }, { rootMargin: '-90px 0px -60% 0px', threshold: 0 });
    headings.forEach((h) => tio.observe(h));
    if (headings[0]) setActive(headings[0].id);
    // heading underline draws once each h2 has been seen
    const seen = new IntersectionObserver((entries) => entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add('is-seen'); seen.unobserve(en.target); } }), { rootMargin: '0px 0px -20% 0px' });
    document.querySelectorAll('.prose h2').forEach((h) => seen.observe(h));
  }
  // reading progress ring (article sidebar)
  const ringBar = document.querySelector('.read-ring__bar');
  const ringPct = document.querySelector('.read-ring__pct');
  const body = document.getElementById('article-body');
  if (ringBar && body) {
    const CIRC = 97.4;
    const onRead = () => {
      const r = body.getBoundingClientRect();
      const total = r.height - window.innerHeight * 0.5;
      const done = Math.min(Math.max(-r.top + window.innerHeight * 0.4, 0), Math.max(total, 1));
      const p = total > 0 ? done / total : 1;
      ringBar.style.strokeDashoffset = String(CIRC * (1 - p));
      ringPct.textContent = Math.round(p * 100) + '%';
    };
    window.addEventListener('scroll', onRead, { passive: true }); window.addEventListener('resize', onRead, { passive: true }); onRead();
  }
  document.querySelectorAll('[data-share]').forEach((el) => {
    const kind = el.getAttribute('data-share');
    const url = encodeURIComponent(location.href), title = encodeURIComponent(document.title);
    if (kind === 'linkedin') el.href = 'https://www.linkedin.com/sharing/share-offsite/?url=' + url;
    if (kind === 'x') el.href = 'https://twitter.com/intent/tweet?url=' + url + '&text=' + title;
    if (kind === 'copy') el.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText(location.href); el.setAttribute('aria-label', T('Link copied')); el.style.color = 'var(--accent)'; setTimeout(() => { el.style.color = ''; }, 1200); } catch (err) { /* clipboard unavailable */ }
    });
  });

  /* ---------- Footer year ---------- */
  const year = document.getElementById('year');
  if (year) year.textContent = String(new Date().getFullYear());
})();
