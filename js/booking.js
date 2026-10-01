/* VeranticSystems — appointment calendar for the booking modal.
   Front-end only for now: picks a date and time, collects details, and produces calendar links.
   Backend settings live in js/config.js: bookingUrl embeds an external scheduler instead; endpoints.booking receives these bookings; busyUrl hides taken slots. */
(function () {
  'use strict';

  const BUSINESS_TZ = 'Europe/London';   // fallback when the browser can't report a zone
  const OWNER_TZ = 'Asia/Karachi';       // the team's own zone, added to every booking request so no conversion is needed
  const SLOT_MINUTES = 30;
  const WEEKS_AHEAD = 8;
  const MIN_NOTICE_HOURS = 24;            // nobody can book a call that starts sooner than this (keep it equal to Cal.com's "Minimum notice")
  const HOURS = Array.from({ length: 48 }, (_, i) => [Math.floor(i / 2), (i % 2) * 30]); // every 30 minutes, around the clock
  const ZONES = [
    'Europe/London', 'Europe/Dublin', 'Europe/Paris', 'Europe/Berlin', 'Europe/Madrid', 'Europe/Rome', 'Europe/Amsterdam', 'Europe/Stockholm', 'Europe/Warsaw', 'Europe/Istanbul',
    'America/New_York', 'America/Chicago', 'America/Denver', 'America/Los_Angeles', 'America/Toronto', 'America/Vancouver', 'America/Mexico_City', 'America/Sao_Paulo', 'America/Argentina/Buenos_Aires',
    'Asia/Dubai', 'Asia/Riyadh', 'Asia/Karachi', 'Asia/Kolkata', 'Asia/Dhaka', 'Asia/Bangkok', 'Asia/Singapore', 'Asia/Hong_Kong', 'Asia/Shanghai', 'Asia/Tokyo', 'Asia/Seoul', 'Asia/Manila', 'Asia/Jakarta',
    'Australia/Perth', 'Australia/Sydney', 'Australia/Melbourne', 'Australia/Brisbane', 'Pacific/Auckland', 'Africa/Johannesburg', 'Africa/Lagos', 'Africa/Nairobi', 'Africa/Cairo',
  ];
  const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

  // ---- time zone helpers -------------------------------------------------
  function wallParts(date, tz) {
    const f = new Intl.DateTimeFormat('en-GB', { timeZone: tz, year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', hour12: false });
    const o = {};
    f.formatToParts(date).forEach((p) => { if (p.type !== 'literal') o[p.type] = parseInt(p.value, 10); });
    return { y: o.year, m: o.month - 1, d: o.day, hh: o.hour % 24, mm: o.minute };
  }
  // Date for wall-clock y/m/d hh:mm in a given zone (handles DST by converging)
  function zonedToUtc(y, m, d, hh, mm, tz) {
    const target = Date.UTC(y, m, d, hh, mm);
    let guess = target;
    for (let i = 0; i < 3; i++) {
      const p = wallParts(new Date(guess), tz);
      guess += target - Date.UTC(p.y, p.m, p.d, p.hh, p.mm);
    }
    return new Date(guess);
  }
  function offsetLabel(tz, at) {
    const p = wallParts(at, tz);
    const diffMin = Math.round((Date.UTC(p.y, p.m, p.d, p.hh, p.mm) - Date.UTC(at.getUTCFullYear(), at.getUTCMonth(), at.getUTCDate(), at.getUTCHours(), at.getUTCMinutes())) / 60000);
    const sign = diffMin >= 0 ? '+' : '-', a = Math.abs(diffMin);
    return 'GMT' + sign + Math.floor(a / 60) + (a % 60 ? ':' + String(a % 60).padStart(2, '0') : '');
  }
  const zoneName = (tz) => tz.split('/').pop().replace(/_/g, ' ');
  const fmtTime = (date, tz) => new Intl.DateTimeFormat('en-US', { timeZone: tz, hour: 'numeric', minute: '2-digit', hour12: true }).format(date).replace(/[\s ]*(AM|PM)/i, ' $1');
  const fmtLong = (date, tz) => new Intl.DateTimeFormat('en-GB', { timeZone: tz, weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }).format(date);
  const pad = (n) => String(n).padStart(2, '0');
  const icsStamp = (d) => d.getUTCFullYear() + pad(d.getUTCMonth() + 1) + pad(d.getUTCDate()) + 'T' + pad(d.getUTCHours()) + pad(d.getUTCMinutes()) + '00Z';

  // ---- availability -------------------------------------------------------
  function isBookableDay(y, m, d, today) {
    const day = Date.UTC(y, m, d), t0 = Date.UTC(today.y, today.m, today.d);
    const daysAhead = Math.round((day - t0) / 86400000);
    return daysAhead >= 1 && daysAhead <= WEEKS_AHEAD * 7;
  }
  function slotsFor(y, m, d, tz) { return HOURS.map(([hh, mm]) => zonedToUtc(y, m, d, hh, mm, tz)); }

  // ---- UI -------------------------------------------------------------------
  function h(html) { const t = document.createElement('template'); t.innerHTML = html.trim(); return t.content.firstElementChild; }

  function mount(body, opts) {
    const cfg = Object.assign({ title: 'Free CRM Audit', minutes: 30, email: 'hello@veranticsystems.com', endpoint: '', reduce: false }, opts || {});
    const now = new Date();
    let tz = (Intl.DateTimeFormat().resolvedOptions().timeZone) || BUSINESS_TZ;
    if (!ZONES.includes(tz)) ZONES.unshift(tz);
    let today = wallParts(now, tz);                 // "today" and every day boundary follow the visitor's zone
    let view = { y: today.y, m: today.m };
    let selDay = null, selSlot = null, step = 1, details = null;
    let busy = []; // [{start, end}] in ms, from cfg.busyUrl

    body.innerHTML = '';
    body.classList.add('modal__body--bk');
    const root = h(`
      <div class="bk">
        <aside class="bk__side">
          <div class="bk__brand">
            <svg class="brand__mark" viewBox="0 0 40 40" aria-hidden="true"><path d="M6 13 L14 30" stroke-width="5" opacity=".35"/><path d="M12 12 L20 31 L35 7" stroke-width="6"/></svg>
            <span class="brand__name">Verantic<span>Systems</span></span>
          </div>
          <p class="bk__eyebrow">Book a call</p>
          <h2 class="bk__title">${cfg.title}</h2>
          <ul class="bk__meta">
            <li><svg class="i" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg><span>${cfg.minutes} minutes</span></li>
            <li><svg class="i" viewBox="0 0 24 24"><rect width="20" height="14" x="2" y="3" rx="2"/><path d="M8 21h8M12 17v4"/></svg><span>Video call, link sent after booking</span></li>
            <li class="bk__tzrow"><svg class="i" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg><label class="sr-only" for="bk-tz">Time zone</label><select id="bk-tz" class="bk__tz"></select></li>
          </ul>
          <ol class="bk__steps">
            <li data-step="1"><span>1</span>Pick a time</li>
            <li data-step="2"><span>2</span>Your details</li>
            <li data-step="3"><span>3</span>Confirmed</li>
          </ol>
          <div class="bk__cover">
            <p class="bk__cover-title">What we'll cover</p>
            <ul class="check-list">
              <li>How leads reach you today and what happens next</li>
              <li>The two or three gaps we see most often</li>
              <li>A prioritised fix list you keep either way</li>
            </ul>
          </div>
        </aside>
        <div class="bk__main">
          <section class="bk__step is-active" data-panel="1">
            <div class="bk__cal">
              <div class="bk__cal-head">
                <button type="button" class="bk__nav" data-nav="-1" aria-label="Previous month"><svg class="i" viewBox="0 0 24 24"><path d="m15 18-6-6 6-6"/></svg></button>
                <h3 class="bk__month" aria-live="polite"></h3>
                <button type="button" class="bk__nav" data-nav="1" aria-label="Next month"><svg class="i" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg></button>
              </div>
              <div class="bk__dow">${DAYS.map((d) => `<span>${d}</span>`).join('')}</div>
              <div class="bk__grid" role="grid"></div>
              <p class="bk__hint">Available every day, around the clock. Times shown in <strong class="bk__tzname"></strong>.</p>
            </div>
            <div class="bk__slots">
              <h3 class="bk__slots-title">Pick a date</h3>
              <p class="bk__slots-sub">Choose a day to see available times.</p>
              <div class="bk__slot-list" role="list"></div>
            </div>
          </section>
          <section class="bk__step" data-panel="2">
            <button type="button" class="bk__back" data-back><svg class="i" viewBox="0 0 24 24"><path d="m15 18-6-6 6-6"/></svg>Change time</button>
            <div class="bk__chosen"></div>
            <form class="bk__form" novalidate>
              <div class="cform__row">
                <div class="field"><label for="bk-name">Your name</label><input id="bk-name" name="name" type="text" autocomplete="name" placeholder="Sarah Mitchell" required><span class="field__error">Please tell us your name.</span></div>
                <div class="field"><label for="bk-email">Work email</label><input id="bk-email" name="email" type="email" autocomplete="email" placeholder="you@company.com" required><span class="field__error">Enter a valid email so we can send the invite.</span></div>
              </div>
              <div class="cform__row">
                <div class="field"><label for="bk-phone">Phone or WhatsApp <small>(optional)</small></label><input id="bk-phone" name="phone" type="tel" autocomplete="tel" placeholder="+44 7400 123456"></div>
                <div class="field"><label for="bk-company">Company <small>(optional)</small></label><input id="bk-company" name="company" type="text" autocomplete="organization" placeholder="Company name"></div>
              </div>
              <div class="field"><label for="bk-notes">Anything we should look at first? <small>(optional)</small></label><textarea id="bk-notes" name="notes" rows="3" placeholder="e.g. We use GoHighLevel but follow-up is manual, and no-shows are high."></textarea></div>
              <div class="bk__actions">
                <button type="submit" class="btn-primary btn-shimmer">Confirm booking<span aria-hidden="true">→</span></button>
                <p class="bk__fine">No card, no obligation. You can reschedule from the confirmation.</p>
              </div>
            </form>
          </section>
          <section class="bk__step bk__done" data-panel="3">
            <svg class="check" viewBox="0 0 90 90" aria-hidden="true"><circle cx="45" cy="45" r="41"/><path d="M28 46 l11 11 l24 -25"/></svg>
            <h3 class="bk__done-title">You're booked in</h3>
            <p class="bk__done-when"></p>
            <p class="bk__done-text">We'll send the video link and a reminder before the call. Add it to your calendar now so it doesn't get lost.</p>
            <div class="bk__done-actions">
              <a class="btn-primary" data-gcal href="#" target="_blank" rel="noopener">Add to Google Calendar</a>
              <a class="btn-outline" data-ics href="#" download="veranticsystems-call.ics">Download .ics</a>
            </div>
            <p class="bk__done-note" data-note></p>
          </section>
        </div>
      </div>`);
    body.appendChild(root);

    const $ = (sel) => root.querySelector(sel);
    const grid = $('.bk__grid'), monthEl = $('.bk__month'), slotList = $('.bk__slot-list'), tzSel = $('.bk__tz');

    // time zone select
    ZONES.forEach((z) => { const o = document.createElement('option'); o.value = z; o.textContent = zoneName(z) + ' (' + offsetLabel(z, now) + ')'; if (z === tz) o.selected = true; tzSel.appendChild(o); });
    tzSel.addEventListener('change', () => {
      tz = tzSel.value; today = wallParts(new Date(), tz);
      if (selDay && !isBookableDay(selDay.y, selDay.m, selDay.d, today)) selDay = null;
      $('.bk__tzname').textContent = zoneName(tz); renderMonth(); renderSlots();
    });
    $('.bk__tzname').textContent = zoneName(tz);

    function setStep(n) {
      step = n;
      root.querySelectorAll('.bk__step').forEach((p) => p.classList.toggle('is-active', p.getAttribute('data-panel') === String(n)));
      root.querySelectorAll('.bk__steps li').forEach((li) => { const s = +li.getAttribute('data-step'); li.classList.toggle('is-current', s === n); li.classList.toggle('is-done', s < n); });
      body.scrollTop = 0;
    }

    function renderMonth(dir) {
      monthEl.textContent = MONTHS[view.m] + ' ' + view.y;
      grid.innerHTML = '';
      grid.classList.remove('slide-l', 'slide-r'); void grid.offsetWidth;
      if (dir) grid.classList.add(dir > 0 ? 'slide-l' : 'slide-r');
      const first = new Date(Date.UTC(view.y, view.m, 1));
      const lead = (first.getUTCDay() + 6) % 7;                    // Monday-first
      const days = new Date(Date.UTC(view.y, view.m + 1, 0)).getUTCDate();
      for (let i = 0; i < lead; i++) grid.appendChild(h('<span class="bk__day bk__day--pad" aria-hidden="true"></span>'));
      for (let d = 1; d <= days; d++) {
        const ok = isBookableDay(view.y, view.m, d, today);
        const isToday = view.y === today.y && view.m === today.m && d === today.d;
        const sel = selDay && selDay.y === view.y && selDay.m === view.m && selDay.d === d;
        const b = h(`<button type="button" class="bk__day${ok ? ' is-open' : ''}${isToday ? ' is-today' : ''}${sel ? ' is-selected' : ''}" role="gridcell" ${ok ? '' : 'disabled'} aria-label="${d} ${MONTHS[view.m]}"><span>${d}</span></button>`);
        if (ok) b.addEventListener('click', () => { selDay = { y: view.y, m: view.m, d }; selSlot = null; renderMonth(); renderSlots(); });
        grid.appendChild(b);
      }
      const minMonth = today.y * 12 + today.m, maxMonth = minMonth + 2;
      root.querySelector('[data-nav="-1"]').disabled = view.y * 12 + view.m <= minMonth;
      root.querySelector('[data-nav="1"]').disabled = view.y * 12 + view.m >= maxMonth;
    }
    root.querySelectorAll('.bk__nav').forEach((b) => b.addEventListener('click', () => {
      const dir = +b.getAttribute('data-nav'); let m = view.m + dir, y = view.y; if (m < 0) { m = 11; y--; } if (m > 11) { m = 0; y++; }
      view = { y, m }; renderMonth(dir);
    }));

    function renderSlots() {
      slotList.innerHTML = '';
      if (!selDay) { $('.bk__slots-title').textContent = 'Pick a date'; $('.bk__slots-sub').textContent = 'Choose a day to see available times.'; return; }
      const dayDate = zonedToUtc(selDay.y, selDay.m, selDay.d, 12, 0, tz);
      $('.bk__slots-title').textContent = fmtLong(dayDate, tz);
      $('.bk__slots-sub').textContent = 'Times in ' + zoneName(tz) + '. Each call is ' + cfg.minutes + ' minutes.';
      // The chosen day runs 12:00 AM to 11:30 PM in the visitor's zone; the Night group wraps past midnight so late slots read in order.
      const groups = [['Morning', 5, 12], ['Afternoon', 12, 17], ['Evening', 17, 21], ['Night', 21, 29]];
      const slots = slotsFor(selDay.y, selDay.m, selDay.d, tz).filter((start) => { const e = start.getTime() + cfg.minutes * 60000; return start.getTime() >= Date.now() + MIN_NOTICE_HOURS * 3600000 && !busy.some((b) => start.getTime() < b.end && e > b.start); });
      if (!slots.length) { slotList.appendChild(h('<p class="bk__group">No times left on this day. Please pick another date.</p>')); return; }
      const hourOf = (start) => { const hh = wallParts(start, tz).hh; return hh < 5 ? hh + 24 : hh; };
      let i = 0;
      groups.forEach(([label, from, to]) => {
        const inGroup = slots.filter((start) => { const hAdj = hourOf(start); return hAdj >= from && hAdj < to; }).sort((a, b) => hourOf(a) - hourOf(b) || a - b);
        if (!inGroup.length) return;
        slotList.appendChild(h(`<p class="bk__group">${label}</p>`));
        const wrap = h('<div class="bk__slot-grid"></div>');
        inGroup.forEach((start) => {
          const b = h(`<button type="button" class="bk__slot" role="listitem" style="animation-delay:${Math.min(i++, 16) * 25}ms"><span>${fmtTime(start, tz)}</span></button>`);
          b.addEventListener('click', () => { selSlot = start; $('.bk__chosen').innerHTML = chosenHtml(); setStep(2); setTimeout(() => $('#bk-name').focus(), 50); });
          wrap.appendChild(b);
        });
        slotList.appendChild(wrap);
      });
    }
    const chosenHtml = () => `<svg class="i" viewBox="0 0 24 24"><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg><div><strong>${fmtLong(selSlot, tz)}</strong><span>${fmtTime(selSlot, tz)} to ${fmtTime(new Date(selSlot.getTime() + cfg.minutes * 60000), tz)} (${zoneName(tz)}) · ${cfg.minutes} min</span></div>`;

    $('[data-back]').addEventListener('click', () => setStep(1));

    // details form
    const form = $('.bk__form');
    { const hp = document.createElement('div'); hp.setAttribute('aria-hidden', 'true'); hp.style.cssText = 'position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden'; hp.innerHTML = '<label>Leave this field empty<input type="text" name="_hp" tabindex="-1" autocomplete="off"></label>'; form.appendChild(hp); }
    form.querySelectorAll('input').forEach((el) => el.addEventListener('input', () => el.closest('.field').classList.remove('is-invalid')));
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      let ok = true;
      form.querySelectorAll('[required]').forEach((input) => {
        const valid = input.type === 'email' ? /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value.trim()) : input.value.trim().length > 0;
        input.closest('.field').classList.toggle('is-invalid', !valid);
        if (!valid && ok) { input.focus(); ok = false; }
      });
      if (!ok) return;
      const fd = new FormData(form);
      details = { _hp: fd.get('_hp'), name: fd.get('name'), email: (fd.get('email') || '').trim(), phone: fd.get('phone'), company: fd.get('company'), notes: fd.get('notes') };
      finish();
    });

    async function finish() {
      const end = new Date(selSlot.getTime() + cfg.minutes * 60000);
      const title = cfg.title + ' with VeranticSystems';
      const desc = `${cfg.minutes}-minute call. We'll look at how leads reach you today and what to automate first.` + (details.notes ? '\n\nNotes: ' + details.notes : '');
      $('.bk__done-when').innerHTML = `<strong>${fmtLong(selSlot, tz)}</strong><br>${fmtTime(selSlot, tz)} to ${fmtTime(end, tz)} (${zoneName(tz)})`;
      $('[data-gcal]').href = 'https://calendar.google.com/calendar/render?action=TEMPLATE&text=' + encodeURIComponent(title) + '&dates=' + icsStamp(selSlot) + '/' + icsStamp(end) + '&details=' + encodeURIComponent(desc);
      const ics = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//VeranticSystems//Booking//EN', 'BEGIN:VEVENT', 'UID:' + Date.now() + '@veranticsystems.com', 'DTSTAMP:' + icsStamp(new Date()), 'DTSTART:' + icsStamp(selSlot), 'DTEND:' + icsStamp(end), 'SUMMARY:' + title, 'DESCRIPTION:' + desc.replace(/\n/g, '\\n'), 'END:VEVENT', 'END:VCALENDAR'].join('\r\n');
      $('[data-ics]').href = 'data:text/calendar;charset=utf-8,' + encodeURIComponent(ics);

      const ownerWhen = fmtLong(selSlot, OWNER_TZ) + ', ' + fmtTime(selSlot, OWNER_TZ) + ' to ' + fmtTime(end, OWNER_TZ) + ' (' + zoneName(OWNER_TZ) + ')';
      // Flat fields so a GoHighLevel inbound webhook can map them straight onto a contact + appointment
      const fields = {
        _hp: details._hp, name: details.name, email: details.email, phone: details.phone || '', company: details.company || '', message: details.notes || '',
        appointment_title: title, appointment_start: selSlot.toISOString(), appointment_end: end.toISOString(), appointment_minutes: cfg.minutes,
        visitor_timezone: tz, visitor_time: fmtLong(selSlot, tz) + ', ' + fmtTime(selSlot, tz) + ' to ' + fmtTime(end, tz), owner_time: ownerWhen,
      };
      const note = $('[data-note]');
      const bodyTxt = ['Booking request', '', 'Client time: ' + fmtLong(selSlot, tz) + ', ' + fmtTime(selSlot, tz) + ' (' + zoneName(tz) + ')', 'Our time: ' + ownerWhen, 'Name: ' + details.name, 'Email: ' + details.email, 'Phone: ' + (details.phone || '-'), 'Company: ' + (details.company || '-'), 'Notes: ' + (details.notes || '-')].join('\n');
      const mailto = 'mailto:' + cfg.email + '?subject=' + encodeURIComponent('Booking request: ' + fmtLong(selSlot, tz) + ' ' + fmtTime(selSlot, tz)) + '&body=' + encodeURIComponent(bodyTxt);
      const btn = form.querySelector('button[type="submit"]');
      btn.disabled = true; form.classList.add('is-sending');
      try {
        const res = cfg.submit ? await cfg.submit(fields) : { mode: 'mailto' };
        if (res.mode === 'mailto') {
          // nothing is configured: never launch the visitor's email app; offer a link they can choose to click
          note.innerHTML = 'Booking delivery isn\'t connected yet, so this time is not confirmed. Please <a href="' + mailto + '">email us the request</a> and we\'ll confirm by reply.';
        } else {
          note.textContent = 'We\'ve got your request. A person will confirm by email at ' + details.email + ' with the video link.';
        }
        setStep(3);
      } catch (err) {
        let er = form.querySelector('.form-error');
        if (!er) { er = document.createElement('p'); er.className = 'form-error'; er.setAttribute('role', 'alert'); form.appendChild(er); }
        er.innerHTML = 'Sorry, the booking didn\'t go through. Please try again, or <a href="' + mailto + '">email the request</a> and we\'ll confirm by reply.';
        er.hidden = false;
      } finally { btn.disabled = false; form.classList.remove('is-sending'); }
    }

    renderMonth();
    renderSlots();
    setStep(1);
    if (cfg.busyUrl) {
      const from = new Date(), to = new Date(Date.now() + (WEEKS_AHEAD * 7 + 2) * 86400000);
      fetch(cfg.busyUrl + (cfg.busyUrl.includes('?') ? '&' : '?') + 'from=' + encodeURIComponent(from.toISOString()) + '&to=' + encodeURIComponent(to.toISOString()), { headers: { Accept: 'application/json' } })
        .then((r) => r.ok ? r.json() : { busy: [] })
        .then((d) => { busy = (d.busy || []).map((b) => ({ start: new Date(b.start).getTime(), end: new Date(b.end).getTime() })).filter((b) => b.start && b.end); renderSlots(); })
        .catch(() => { /* availability is a nicety; the calendar still works without it */ });
    }
    // ?bkday=N preselects the day N days from today (used for previews/testing)
    const pre = parseInt(new URLSearchParams(location.search).get('bkday') || '', 10);
    if (pre > 0) { const t = new Date(Date.UTC(today.y, today.m, today.d + pre)); selDay = { y: t.getUTCFullYear(), m: t.getUTCMonth(), d: t.getUTCDate() }; view = { y: selDay.y, m: selDay.m }; renderMonth(); renderSlots(); }

    return { reset() { selDay = null; selSlot = null; view = { y: today.y, m: today.m }; form.reset(); renderMonth(); renderSlots(); setStep(1); } };
  }

  window.VSBooking = { mount };
})();
