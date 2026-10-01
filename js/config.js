/* VeranticSystems — site configuration.
   This is the ONLY file you edit to make the forms and the booking window work. Both services below are free and need no server. */
window.VS_CONFIG = {

  /* ---- 1. Forms → your inbox (Web3Forms, free) -------------------------------------------------------------------
     Go to https://web3forms.com, enter the email address that should receive enquiries, and paste the access key they send you.
     Contact form, newsletter signup, job applications and custom-calendar bookings then arrive in that inbox.
     Empty = the visitor's own email app opens instead (fine for a demo, not for a live site). */
  formKey: '80af99a5-2255-4edc-9446-50fbcd3fa288',

  /* ---- 2. Booking → your calendar (Cal.com, free) ----------------------------------------------------------------
     Create a free account at https://cal.com, make a 30-minute event, and paste its link, e.g. 'https://cal.com/veranticsystems/crm-audit'
     The "Book a Call" window then shows that scheduler: it blocks taken slots, emails the confirmation and sends reminders.
     Empty = the built-in calendar is used and each booking is emailed to you through formKey (no double-booking protection). */
  bookingUrl: 'https://cal.com/veranticsystems/free-audit-call',

  /* ---- Inboxes shown to visitors and used as the fallback ---- */
  fallbackEmail: 'hello@veranticsystems.com',
  careersEmail: 'careers@veranticsystems.com',

  /* ---- Analytics (all optional) -----------------------------------------------------------------------------------
     ga4 / metaPixel load only after the visitor accepts the cookie banner. plausibleDomain needs no banner. */
  analytics: {
    ga4: '',               // e.g. 'G-XXXXXXXXXX'
    metaPixel: '',         // e.g. '1234567890'
    plausibleDomain: '',   // e.g. 'veranticsystems.com'
  },

  /* ---- Advanced, normally left empty ------------------------------------------------------------------------------
     Send a form to your own URL instead of Web3Forms (any endpoint that accepts a JSON POST). `default` applies to every form. */
  endpoints: { default: '', contact: '', booking: '', newsletter: '', careers: '' },
  busyUrl: '',             // built-in calendar only: URL returning { "busy": [ { "start": ISO, "end": ISO } ] }
};
