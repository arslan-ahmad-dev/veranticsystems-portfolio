"""Sample content for every portfolio screen. All names, numbers and amounts are invented for illustration.
SCREENS[slug] = [(kind, caption, address-bar text, spec), ...]  (three per project; the first is shown wide)."""

ST = lambda t, tone: (t, tone)
k1 = lambda v: f"{v:.1f}"

SCREENS = {
 "podagain": [
  ("player", "Generated two-host podcast with transcript", "app.podagain.example/episodes/attention", dict(
     title="How Attention Actually Works", sub="Generated from 3 sources · 12 min", hosts=("Maya", "Theo"), time=("04:36", "12:08"), status="Ready",
     lines=[("Maya", ["So the model doesn't read left to right,", "it weighs every word against the rest."], False),
            ("Theo", ["Right, and that weighting is what the", "paper calls attention."], True),
            ("Maya", ["Which is why long documents used to", "break older models."], False),
            ("Theo", ["Let's walk through a small example."], False)])),
  ("table", "Learning library: feeds, blogs, PDFs, documents", "app.podagain.example/library", dict(
     nav=["Library", "Sources", "Episodes", "Jobs", "Billing", "Settings"], title="Learning library", sub="86 items indexed",
     filters=["All", "Podcasts", "Blogs", "PDFs", "Docs"], search="Search library",
     cols=[("Title", 3), ("Type", 1.2), ("Length", 1, "r"), ("Status", 1.5)],
     rows=[("Scaling queues in production", "Podcast", "58 min", ST("Indexed", "ok")), ("Attention Is All You Need.pdf", "PDF", "15 pp", ST("Indexed", "ok")),
           ("Postgres internals series", "Blog", "12 posts", ST("Indexing", "info")), ("Q3 research notes", "Doc", "24 pp", ST("Indexed", "ok")),
           ("AI compute, long-form", "Podcast", "2 h 41", ST("Transcribing", "warn")), ("Vector search primer", "Blog", "9 min", ST("Indexed", "ok")),
           ("Hiring playbook.docx", "Doc", "31 pp", ST("Queued", "muted")), ("Founder stories feed", "RSS", "214 eps", ST("Indexed", "ok"))])),
  ("flow", "Background job pipeline and GPU status", "app.podagain.example/admin/jobs", dict(
     title="Job pipeline", sub="Queue-based workers, GPU server on demand",
     nodes=[("Frontend", "React app: upload and play", ST("Live", "ok")), ("Node API", "auth, billing, job creation"), ("Queue", "Celery + Redis", ST("Busy", "info"), "14 jobs"),
            ("Workers", "ingest, transcribe, embed"), ("GPU server", "starts on demand", ST("Idle in 8 min", "warn")), ("Vector DB", "Pinecone semantic search", ST("Healthy", "ok"))])),
 ],
 "ai-support-copilot": [
  ("chat", "Ticket view with a cited, suggested reply", "support.example.com/tickets/4821", dict(
     inbox="Inbox", threads=[("Maria L.", "Order arrived damaged", "2m"), ("Daniel K.", "Cracked screen, refund?", "14m"), ("Priya S.", "Where is my invoice?", "1h"), ("Tom B.", "Cancel subscription", "3h"), ("Anna R.", "SSO setup question", "5h")],
     subject="Refund for a damaged item", badge="Open",
     messages=[("Daniel K.", ["Hi, my order arrived with a cracked screen.", "Can I get a refund or a replacement?"])],
     reply=["Hi Daniel, I'm sorry about the cracked screen. We can", "refund the full amount or send a replacement within", "3 days. Which would you prefer?"], cites=["Refund policy §3", "Damaged goods FAQ"])),
  ("table", "Knowledge sources and indexing status", "support.example.com/knowledge", dict(
     nav=["Tickets", "Knowledge", "Sources", "Quality", "Team", "Settings"], active=2, title="Knowledge sources", sub="6 sources · last sync 4 min ago",
     filters=["All", "Help centre", "PDFs", "Tickets"], search="Search sources",
     cols=[("Source", 3), ("Type", 1.3), ("Chunks", 1, "r"), ("Status", 1.6)],
     rows=[("help.acme-store.com", "Help centre", "1,284", ST("Indexed", "ok")), ("Returns policy 2026.pdf", "PDF", "42", ST("Indexed", "ok")), ("Shipping guide.pdf", "PDF", "67", ST("Indexed", "ok")),
           ("Closed tickets (2025)", "Tickets", "9,410", ST("Indexing 72%", "info")), ("Billing FAQ", "Help centre", "96", ST("Indexed", "ok")), ("Product manuals", "PDF", "588", ST("Needs review", "warn"))])),
  ("dash", "Quality dashboard: accepted vs edited replies", "support.example.com/quality", dict(
     nav=["Tickets", "Knowledge", "Sources", "Quality", "Team", "Settings"], active=3, title="Reply quality", sub="Suggestions by your agents",
     kpis=[("Accepted as is", "58%", "+6%"), ("Edited, then sent", "31%", "-2%", "muted"), ("Discarded", "11%", "-4%")],
     chart=dict(title="Accepted replies per week", vals=[41, 44, 47, 46, 52, 55, 58, 61], labels=["W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8"], unit="%"),
     list=dict(title="Top knowledge gaps", items=[("Warranty claims", 42), ("Intl. shipping", 31), ("Invoice corrections", 24), ("Gift cards", 17), ("Account merge", 11)]))),
 ],
 "booking-subscription-platform": [
  ("cal", "Staff calendar with live bookings", "studionova.example/admin/calendar", dict(
     nav=["Calendar", "Clients", "Services", "Staff", "Plans", "Reports"], title="Staff calendar", sub="Studio Nova · 17 to 22 March",
     days=[("Mon", "17"), ("Tue", "18"), ("Wed", "19"), ("Thu", "20"), ("Fri", "21"), ("Sat", "22")], today=2,
     hours=["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"],
     events=[(0, 0.5, 1.5, ("Sofia R.", "Deep tissue · Anna"), "info"), (0, 3, 1, ("Liam P.", "Facial · Maya"), "ok"), (1, 1, 1, ("Noor A.", "Hot stone · Anna"), "info"),
             (1, 4, 2, ("Group class", "Yoga flow · Ben"), "warn"), (2, 0, 1, ("Emma W.", "Sports · Ben"), "ok"), (2, 2, 1.5, ("Dev K.", "Deep tissue · Anna"), "info"),
             (3, 1.5, 1, ("Hana T.", "Facial · Maya"), "ok"), (4, 0.5, 2, ("Couples", "Massage · Anna + Ben"), "info"), (4, 5, 1, ("Ravi S.", "Sports · Ben"), "ok"), (5, 1, 2, ("Workshop", "Breathwork · Maya"), "warn")])),
  ("cards", "Services and membership plans", "studionova.example/admin/plans", dict(
     variant="plans", nav=["Calendar", "Clients", "Services", "Staff", "Plans", "Reports"], active=4, title="Memberships", sub="3 plans · 214 active members", right="New plan",
     cards=[dict(name="Starter", price="$29", per="per month", bullets=["2 sessions a month", "Online booking", "Cancel any time"], cta="Edit plan"),
            dict(name="Regular", price="$79", per="per month", bullets=["6 sessions a month", "Priority booking", "10% off retail"], hot=True, cta="Edit plan"),
            dict(name="Unlimited", price="$149", per="per month", bullets=["Unlimited sessions", "Free guest pass", "Member events"], cta="Edit plan")])),
  ("dash", "Owner dashboard: revenue and bookings", "studionova.example/admin", dict(
     nav=["Calendar", "Clients", "Services", "Staff", "Plans", "Reports"], active=5, title="Owner dashboard", sub="Studio Nova", range="Last 6 weeks",
     kpis=[("Revenue", "$18,420", "+12.4%"), ("Bookings", "612", "+8.1%"), ("No-show rate", "3.2%", "-1.1%")],
     chart=dict(kind="bars", title="Revenue by week ($k)", vals=[3.6, 4.1, 4.4, 4.0, 4.9, 5.2], labels=["W1", "W2", "W3", "W4", "W5", "W6"], fmt=k1),
     list=dict(title="Top services", items=[("Deep tissue 60", 118), ("Facial glow", 96), ("Sports recovery", 74), ("Hot stone", 52), ("Couples", 31)]))),
 ],
 "logistics-dispatch-dashboard": [
  ("map", "Live map with vehicles and routes", "dispatch.example.com/live", dict(
     panel="Active jobs", jobs=[("JOB-2041", "Out for delivery", "12 min", "ok"), ("JOB-2044", "Picked up", "28 min", "info"), ("JOB-2047", "Delayed: traffic", "+9 min", "warn"), ("JOB-2050", "Assigned", "41 min", "muted")],
     route=[(300, 340), (350, 300), (410, 262), (470, 222), (540, 160), (590, 112)], pins=[(300, 340, "A", "ok"), (470, 222, "2", "warn"), (590, 112, "B", "info")],
     vehicles=[(372, 282, "Van 12"), (500, 186, "Bike 3")])),
  ("table", "Job list with status and ETA", "dispatch.example.com/jobs", dict(
     nav=["Live map", "Jobs", "Drivers", "Customers", "Reports", "Settings"], active=1, title="Jobs", sub="Today · 38 jobs", filters=["All", "In transit", "Delayed", "Done"], search="Search jobs",
     cols=[("Job", 1.2), ("Customer", 2), ("Driver", 1.4), ("ETA", 0.9, "r"), ("Status", 1.5)],
     rows=[("JOB-2041", "Northwind Foods", "R. Khan", "12 min", ST("In transit", "info")), ("JOB-2042", "Bright Dental", "S. Ortiz", "Done", ST("Delivered", "ok")), ("JOB-2044", "Harbor Cafe", "M. Lee", "28 min", ST("Picked up", "info")),
           ("JOB-2047", "Oakline Pharmacy", "T. Novak", "+9 min", ST("Delayed", "warn")), ("JOB-2048", "City Florist", "R. Khan", "1 h 05", ST("Assigned", "muted")), ("JOB-2050", "Metro Print", "S. Ortiz", "41 min", ST("Assigned", "muted")),
           ("JOB-2051", "Greenleaf Market", "A. Diaz", "Done", ST("Delivered", "ok"))])),
  ("kanban", "Dispatch board by job state", "dispatch.example.com/board", dict(
     title="Dispatch board", sub="Drag a job to assign it",
     cols=[("Unassigned", 3, [("JOB-2052", "Harbor St to 5th Ave", ST("Urgent", "bad")), ("JOB-2053", "Mill Rd to Park Lane", ST("Today", "info")), ("JOB-2054", "Dock 4 to Unit 9", ST("Today", "info"))]),
           ("In transit", 3, [("JOB-2041", "R. Khan · ETA 12 min", ST("On time", "ok")), ("JOB-2044", "M. Lee · ETA 28 min", ST("On time", "ok")), ("JOB-2047", "T. Novak · ETA +9 min", ST("Delayed", "warn"))]),
           ("Delivered", 3, [("JOB-2042", "Bright Dental", ST("POD saved", "ok")), ("JOB-2051", "Greenleaf Market", ST("POD saved", "ok")), ("JOB-2039", "Metro Print", ST("POD saved", "ok"))])])),
 ],
 "restaurant-ordering-kds": [
  ("cards", "Guest menu on a phone, with modifiers", "order.baoandco.example/t/12", dict(
     variant="phone", title="Guest menu", sub="Scan the table QR code, order and pay from your phone", phone_title="Table 12 · Bao & Co", phone_sub="Order for 2 guests",
     items=[("Spicy pork bao", "Steamed, chilli crisp", "$9"), ("Crispy tofu bowl", "Rice, greens, sesame", "$13"), ("Iced jasmine tea", "Refills included", "$4"), ("Mango sticky rice", "Coconut cream", "$7")],
     mod_title="Spicy pork bao", mod_sub="Customise your order",
     mods=[("Spice level", [("Mild", False), ("Medium", True), ("Hot", False)]), ("Extras", [("Extra bao", False), ("Pickles", True), ("Chilli oil", True)]), ("Allergies", [("No peanuts", True), ("No gluten", False)])],
     cta="Add to order  ·  $10.50")),
  ("kanban", "Kitchen display: new, preparing, ready", "kds.baoandco.example/wok", dict(
     title="Kitchen display", sub="Station: Wok · 7 open tickets",
     cols=[("New", 3, [("#112 · Table 4", "2× Spicy bao, 1× Tea", ST("0:45", "info")), ("#113 · Takeaway", "1× Tofu bowl", ST("0:20", "info")), ("#114 · Table 9", "3× Bao, 2× Rice", ST("0:05", "info"))]),
           ("Preparing", 2, [("#109 · Table 2", "1× Tofu bowl, 1× Tea", ST("4:10", "warn")), ("#110 · Table 7", "2× Spicy bao", ST("2:35", "ok"))]),
           ("Ready", 2, [("#106 · Table 5", "Runner: Sam", ST("Ready", "ok")), ("#107 · Takeaway", "Pick-up: J. Ortiz", ST("Ready", "ok"))])])),
  ("dash", "Owner reports: sales and prep time", "admin.baoandco.example/reports", dict(
     nav=["Orders", "Menu", "Reports", "Staff", "Settings"], active=2, title="Owner reports", sub="Bao & Co · today", range="Today",
     kpis=[("Sales", "$2,184", "+9%"), ("Avg prep time", "11m 20s", "-1m 05s"), ("Orders", "163", "+14")],
     chart=dict(title="Sales by hour ($)", vals=[120, 210, 380, 560, 420, 310, 480, 640, 520, 300], labels=["11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]),
     list=dict(title="Top items", items=[("Spicy pork bao", 212), ("Crispy tofu bowl", 148), ("Iced jasmine tea", 131), ("Mango sticky rice", 96), ("Edamame", 64)]))),
 ],
 "property-listings-marketplace": [
  ("map", "Map search with listing cards", "homes.example.com/search?beds=3", dict(
     panel="Homes in view", jobs=[("$425,000", "3 bed · Oakridge", "New", "ok"), ("$310,000", "2 bed · Linden Park", "", "info"), ("$515,000", "4 bed · Hillcrest", "Reduced", "warn"), ("$289,500", "2 bed · Millbrook", "", "muted")],
     route=[], pins=[(320, 300, "1", "ok"), (430, 220, "2", "info"), (520, 150, "3", "warn"), (380, 130, "4", "muted"), (560, 280, "5", "info")], vehicles=[])),
  ("cards", "Listing grid with filters", "homes.example.com/listings", dict(
     variant="grid", title="Listings", sub="128 homes · 3+ beds · under $600k", right="Filters (3)",
     cards=[dict(name="Oakridge Villa", meta="4 bed · 3 bath · 2,140 sq ft", price="$515,000", badge="Reduced", tag="NEW", bullets=["Garden and garage", "Open house Sat 11:00"]),
            dict(name="Linden Park Flat", meta="2 bed · 1 bath · 860 sq ft", price="$310,000", badge="", tag="", bullets=["Balcony, lift", "Near station"]),
            dict(name="Hillcrest Cottage", meta="3 bed · 2 bath · 1,320 sq ft", price="$425,000", badge="New", tag="NEW", bullets=["Renovated 2025", "Private garden"])])),
  ("table", "Agent enquiries inbox", "homes.example.com/agent/enquiries", dict(
     nav=["Listings", "Enquiries", "Viewings", "Agents", "Reports"], active=1, title="Enquiries", sub="Inbox · 9 unread", filters=["All", "New", "Viewing booked"], search="Search enquiries",
     cols=[("Name", 1.8), ("Property", 2.2), ("Received", 1.1), ("Status", 1.6)],
     rows=[("Amelia Brooks", "Oakridge Villa", "10 min", ST("New", "info")), ("Chen Wei", "Linden Park Flat", "42 min", ST("New", "info")), ("Marcus Hale", "Hillcrest Cottage", "2 h", ST("Viewing booked", "ok")),
           ("Sana Iqbal", "Oakridge Villa", "5 h", ST("Replied", "muted")), ("Tomas Ruiz", "Millbrook Terrace", "Yesterday", ST("Viewing booked", "ok")), ("Julia Park", "Linden Park Flat", "Yesterday", ST("Replied", "muted"))])),
 ],
 "telehealth-video-consult": [
  ("video", "Video consultation with notes panel", "care.example.com/visit/8f2a", dict(
     who="Dr. Amara Singh", timer="12:04", strip="Reason: follow-up · blood pressure review",
     details=[("Patient", "J. Alvarez, 47"), ("Appointment", "Tue 10:30 · 20 min"), ("Reason", "Follow-up review"), ("Last visit", "14 Feb 2026")],
     notes=["BP trending down since", "March.", "Continue current dose.", "Book review in 6 weeks."])),
  ("cal", "Clinician calendar", "care.example.com/clinic/calendar", dict(
     nav=["Calendar", "Patients", "Visits", "Billing", "Settings"], title="Clinician calendar", sub="Dr. Amara Singh", range="Week view",
     days=[("Mon", "17"), ("Tue", "18"), ("Wed", "19"), ("Thu", "20"), ("Fri", "21")], today=1, hours=["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"],
     events=[(0, 0, 1, ("A. Khan", "Check-up"), "info"), (0, 2, 1, ("L. Moreau", "Follow-up"), "ok"), (1, 1.5, 1, ("J. Alvarez", "BP review"), "info"), (1, 4, 1, ("P. Singh", "New patient"), "warn"),
             (2, 0.5, 1, ("D. Okoye", "Follow-up"), "ok"), (2, 3, 2, ("Admin block", "Notes and results"), "muted"), (3, 1, 1, ("E. Rossi", "Check-up"), "info"), (4, 0, 1, ("M. Lund", "Follow-up"), "ok"), (4, 3, 1, ("R. Das", "Check-up"), "info")])),
  ("table", "Patient appointments and payments", "care.example.com/clinic/visits", dict(
     nav=["Calendar", "Patients", "Visits", "Billing", "Settings"], active=2, title="Visits and payments", sub="This week · 34 visits", filters=["All", "Upcoming", "Completed"], search="Search patients",
     cols=[("Patient", 2), ("Time", 1.3), ("Type", 1.3), ("Fee", 0.9, "r"), ("Payment", 1.4)],
     rows=[("J. Alvarez", "Tue 10:30", "Video", "$60", ST("Paid", "ok")), ("P. Singh", "Tue 14:00", "Video", "$85", ST("Pending", "warn")), ("D. Okoye", "Wed 09:30", "Video", "$60", ST("Paid", "ok")),
           ("E. Rossi", "Thu 10:00", "In person", "$95", ST("Paid", "ok")), ("M. Lund", "Fri 09:00", "Video", "$60", ST("Refunded", "muted")), ("R. Das", "Fri 13:00", "Video", "$60", ST("Pending", "warn"))])),
 ],
 "invoicing-expense-saas": [
  ("dash", "Cash-flow dashboard", "books.example.com/overview", dict(
     nav=["Overview", "Invoices", "Expenses", "Clients", "Reports", "Settings"], title="Cash flow", sub="Northstar Studio", range="Last 8 weeks",
     kpis=[("Outstanding", "$24,310", "7 invoices", "muted"), ("Overdue", "$3,940", "2 invoices", "bad"), ("Paid this month", "$18,760", "+14%")],
     chart=dict(title="Cash in vs cash out ($)", vals=[8200, 9100, 7800, 11200, 10400, 12800, 12100, 14300], second=[7400, 7900, 8300, 8800, 9400, 9900, 10300, 10900], labels=["W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8"]),
     list=dict(title="Biggest clients", items=[("Brightside Dental", 9400), ("Harbor Cafe", 6200), ("Oakline Pharmacy", 4800), ("City Florist", 2900), ("Metro Print", 1700)]))),
  ("doc", "Branded invoice preview", "books.example.com/invoices/INV-1048", dict(
     doc=dict(**{"from": "Northstar Studio"}, from_sub="hello@northstar.example", title="INVOICE", number="INV-1048", to="Brightside Dental", to_sub="12 Park Lane", date="12 Mar 2026", due="Due 26 Mar 2026",
              cols=["Description", "Qty", "Rate", "Amount"], rows=[("Brand identity", "1", "$2,400", "$2,400"), ("Website design", "1", "$1,200", "$1,200"), ("Social templates", "6", "$100", "$600")],
              totals=[("Subtotal", "$4,200.00", False), ("Tax 20%", "$840.00", False), ("Total due", "$5,040.00", True)]))),
  ("table", "Invoices: paid, due and overdue", "books.example.com/invoices", dict(
     nav=["Overview", "Invoices", "Expenses", "Clients", "Reports", "Settings"], active=1, title="Invoices", sub="42 this quarter", filters=["All", "Paid", "Due", "Overdue"], search="Search invoices",
     cols=[("Invoice", 1.2), ("Client", 2.2), ("Issued", 1.1), ("Amount", 1.1, "r"), ("Status", 1.4)],
     rows=[("INV-1048", "Brightside Dental", "12 Mar", "$5,040", ST("Due", "info")), ("INV-1047", "Harbor Cafe", "08 Mar", "$1,860", ST("Paid", "ok")), ("INV-1046", "Oakline Pharmacy", "02 Mar", "$3,200", ST("Paid", "ok")),
           ("INV-1044", "Metro Print", "21 Feb", "$1,150", ST("Overdue", "bad")), ("INV-1043", "City Florist", "18 Feb", "$2,790", ST("Overdue", "bad")), ("INV-1041", "Greenleaf Market", "10 Feb", "$960", ST("Paid", "ok"))])),
 ],
 "amazon-price-seller-monitor": [
  ("table", "Tracked listings with price and Buy Box", "monitor.example.com/tracked", dict(
     nav=["Tracked", "Alerts", "Sellers", "History", "Settings"], title="Tracked listings", sub="1,248 ASINs · refreshed 6 min ago", filters=["All", "Ours", "Lost Buy Box"], search="Search ASIN or title",
     cols=[("Product", 3), ("ASIN", 1.4), ("Price", 1, "r"), ("Buy Box", 1.6), ("Sellers", 0.8, "r")],
     rows=[("Bamboo cutting board set", "B0C4XK91TQ", "$24.99", ST("Ours", "ok"), "7"), ("Insulated bottle 750 ml", "B09ZPL27MD", "$18.50", ST("Competitor", "warn"), "12"), ("USB-C hub 7-in-1", "B0B7N3RQ5K", "$32.00", ST("Ours", "ok"), "5"),
           ("Silicone baking mats (2)", "B08GHT3KWY", "$14.95", ST("Suppressed", "bad"), "9"), ("Desk cable organiser", "B07QV8D1FZ", "$11.20", ST("Ours", "ok"), "4"), ("LED strip lights 10 m", "B09LM2X6RJ", "$21.90", ST("Competitor", "warn"), "15")])),
  ("dash", "Price history and seller count", "monitor.example.com/history", dict(
     nav=["Tracked", "Alerts", "Sellers", "History", "Settings"], active=3, title="Price history", sub="Insulated bottle 750 ml", range="Last 30 days",
     kpis=[("Tracked ASINs", "1,248", "+36"), ("Alerts today", "19", "+4", "warn"), ("Buy Box share", "71%", "+3%")],
     chart=dict(title="Our price vs lowest competitor ($)", vals=[19.9, 19.9, 19.5, 19.0, 19.0, 18.5, 18.5, 18.9, 18.5], second=[18.9, 18.9, 18.9, 18.2, 18.2, 18.2, 18.0, 18.0, 18.0], labels=["1", "4", "8", "12", "16", "20", "24", "28", "30"], fmt=k1),
     list=dict(title="Sellers on listing", items=[("BrightHome", 18.0), ("Us", 18.5), ("QuickKitchen", 18.9), ("OutdoorHub", 19.4), ("ValuePlus", 19.9)]))),
  ("flow", "Collection and alert pipeline", "monitor.example.com/admin/pipeline", dict(
     title="Collection and alert pipeline", sub="Runs every 15 minutes, with jitter",
     nodes=[("Tracked list", "ASINs from CSV or API"), ("Scheduler", "jittered, per marketplace"), ("Collectors", "rotating proxies, retries", ST("Healthy", "ok")), ("Parser", "price, Buy Box, sellers"), ("History store", "PostgreSQL"), ("Alerts", "email and Slack", ST("3 sent today", "info"))])),
 ],
 "walmart-catalogue-scraper": [
  ("table", "Collected catalogue with normalised fields", "data.example.com/catalogue", dict(
     nav=["Catalogue", "Crawls", "Exports", "API keys", "Settings"], title="Collected catalogue", sub="Home & Kitchen · 48,210 items", filters=["All", "In stock", "Changed today"], search="Search SKU or title",
     cols=[("Product", 3), ("SKU", 1.3), ("Price", 1, "r"), ("Stock", 1.3), ("Rating", 0.8, "r")],
     rows=[("Ceramic mug set (4)", "WM-118204", "$19.97", ST("In stock", "ok"), "4.6"), ("Non-stick pan 12 in", "WM-220931", "$27.44", ST("In stock", "ok"), "4.4"), ("Glass storage jars (6)", "WM-310882", "$16.88", ST("Low stock", "warn"), "4.7"),
           ("Chef knife 8 in", "WM-407153", "$22.00", ST("In stock", "ok"), "4.5"), ("Silicone spatula set", "WM-512640", "$9.48", ST("Out of stock", "bad"), "4.3"), ("Bamboo drawer organiser", "WM-633017", "$13.25", ST("In stock", "ok"), "4.8")])),
  ("flow", "Crawl, clean and serve pipeline", "data.example.com/admin/pipeline", dict(
     title="Crawl, clean and serve", sub="Spiders only collect; a separate pipeline validates",
     nodes=[("Crawl plan", "categories and sellers"), ("Spiders", "Scrapy, throttled retries"), ("Cleaning", "typing and de-duplication"), ("PostgreSQL", "products and prices"), ("FastAPI", "private data API", ST("200 OK", "ok")), ("Exports", "scheduled CSV to storage")])),
  ("dash", "Run report: coverage and failures", "data.example.com/runs/2841", dict(
     nav=["Catalogue", "Crawls", "Exports", "API keys", "Settings"], active=1, title="Run report", sub="Run #2841 · completed in 41 min", range="Last run",
     kpis=[("Pages crawled", "48,210", "+4%"), ("Coverage", "98.6%", "+0.4%"), ("Failures", "1.1%", "-0.3%")],
     chart=dict(kind="bars", title="Items collected per run (thousands)", vals=[38.9, 41.5, 43.8, 45.9, 47.1, 48.2], labels=["#2836", "#2837", "#2838", "#2839", "#2840", "#2841"], fmt=k1),
     list=dict(title="Errors by type", items=[("Timeouts", 212), ("Blocked", 96), ("Parse errors", 41), ("Not found", 27)]))),
 ],
 "cross-marketplace-repricer": [
  ("dash", "Margin and price-change overview", "repricer.example.com/overview", dict(
     nav=["Overview", "Rules", "Review", "SKUs", "Audit log"], title="Margin overview", sub="3 marketplaces · 2,860 SKUs", range="Last 14 days",
     kpis=[("Average margin", "18.4%", "+1.2%"), ("Price changes", "342", "today", "muted"), ("Held by rules", "27", "review", "warn")],
     chart=dict(title="Average margin (%)", vals=[16.4, 16.9, 17.1, 16.8, 17.6, 17.9, 18.2, 18.0, 18.4], labels=["1", "3", "5", "7", "9", "11", "13", "14", "15"], unit="%", fmt=k1),
     list=dict(title="Rules fired today", items=[("Beat lowest by 1%", 148), ("Match Buy Box", 96), ("Floor price hold", 54), ("Stock-low raise", 31), ("Max change cap", 13)]))),
  ("table", "Proposed vs current price per SKU", "repricer.example.com/review", dict(
     nav=["Overview", "Rules", "Review", "SKUs", "Audit log"], active=2, title="Proposed vs current", sub="27 changes need review", filters=["All", "Needs review", "Auto-approved"], search="Search SKU",
     cols=[("SKU", 1.3), ("Item", 2.4), ("Current", 1, "r"), ("Proposed", 1, "r"), ("Rule", 1.7)],
     rows=[("HK-1042", "Pan set, 3 piece", "$41.90", "$39.99", ST("Beat by 1%", "info")), ("HK-2210", "Kettle 1.7 L", "$29.00", "$31.50", ST("Stock-low raise", "ok")), ("HK-0877", "Cutlery set (24)", "$34.20", "$34.20", ST("Floor price", "warn")),
           ("HK-3315", "Storage tubs (5)", "$18.99", "$17.49", ST("Match Buy Box", "info")), ("HK-1190", "Towel set", "$22.40", "$22.40", ST("Hold", "muted")), ("HK-2764", "Lunch box", "$12.60", "$11.99", ST("Beat by 1%", "info"))])),
  ("flow", "Rule evaluation pipeline", "repricer.example.com/admin/engine", dict(
     title="Rule evaluation pipeline", sub="Every proposed price passes guardrails before it is pushed",
     nodes=[("Price feed", "competitor prices in"), ("Rule engine", "floors, ceilings, margins"), ("Guardrails", "max change per hour", ST("12 held", "warn")), ("Review queue", "approve large moves"), ("Marketplace API", "push new prices", ST("Synced", "ok")), ("Audit log", "every change recorded")])),
 ],
 "invoice-document-extraction": [
  ("doc", "Invoice with extracted fields highlighted", "extract.example.com/documents/20931", dict(
     doc=dict(**{"from": "Meridian Supplies Ltd"}, from_sub="Wholesale stationery", title="INVOICE", number="INV-20931", to="Acme Retail", to_sub="Accounts payable", date="08 Feb 2026", due="Net 30",
              cols=["Description", "Qty", "Price", "Total"], rows=[("A4 paper, 5 reams", "20", "$18", "$360"), ("Ink cartridges", "12", "$24", "$288"), ("Archive boxes", "9", "$12", "$108")],
              totals=[("Subtotal", "$756.00", False), ("Total", "$756.00", True)]),
     marks=["vendor", "number", "date", "total"], side_badge="JSON",
     fields=[("Vendor", "Meridian Supplies Ltd", 98), ("Invoice number", "INV-20931", 99), ("Invoice date", "2026-02-08", 97), ("Due date", "Net 30 → 2026-03-10", 81), ("Tax", "$126.00", 93), ("Total", "$756.00", 99)])),
  ("table", "Batch results with confidence scores", "extract.example.com/batches/118", dict(
     nav=["Batches", "Review", "Webhooks", "API keys", "Settings"], title="Batch #118", sub="240 documents · completed", filters=["All", "Needs review", "Delivered"], search="Search file",
     cols=[("File", 2.2), ("Vendor", 2), ("Total", 1, "r"), ("Confidence", 1.1, "r"), ("Status", 1.4)],
     rows=[("inv_20931.pdf", "Meridian Supplies", "$756.00", "97%", ST("Delivered", "ok")), ("inv_20932.pdf", "Orbit Freight", "$1,240.50", "99%", ST("Delivered", "ok")), ("scan_0417.jpg", "Pinecrest Foods", "$318.20", "78%", ST("Review", "warn")),
           ("inv_20934.pdf", "Lumen Energy", "$402.00", "96%", ST("Delivered", "ok")), ("receipt_88.png", "Corner Cafe", "$24.80", "84%", ST("Review", "warn")), ("inv_20936.pdf", "BlueRiver IT", "$2,150.00", "98%", ST("Delivered", "ok"))])),
  ("flow", "Queued extraction pipeline", "extract.example.com/admin/pipeline", dict(
     title="Queued extraction pipeline", sub="Batches scale by adding workers",
     nodes=[("Upload API", "FastAPI + S3"), ("Queue", "Celery workers", ST("22 waiting", "info")), ("OCR", "text and layout"), ("Extraction", "rules + LLM fields"), ("Review queue", "low-confidence items", ST("5 to review", "warn")), ("Webhook", "JSON to your system", ST("Delivered", "ok"))])),
 ],
 "county-surplus-list-pipeline": [
  ("table", "Imported cases with flags and gate result", "pipeline.example.com/cases", dict(
     nav=["Cases", "Sources", "Verify", "Audit log", "Reports"], title="Imported cases", sub="3 official sources · 351 cases", filters=["All", "Blocked", "Custodian-listed", "Flagged"], search="Search parcel",
     cols=[("Parcel", 1.5), ("Jurisdiction", 1.7), ("Reported excess", 1.3, "r"), ("Funds gate", 2)],
     rows=[("5123-004-017", "County A, CA", "$18,420.50", ST("Blocked: unverified", "bad")), ("118-221-09", "County B, NV", "$41,288.10", ST("Blocked: unverified", "bad")), ("07 112 03 045", "County C, GA", "$2,970.00", ST("Held: custodian-listed", "warn")),
           ("07 114 01 009", "County C, GA", "$925.40", ST("Held: possible estate", "warn")), ("5123-009-002", "County A, CA", "$7,310.00", ST("Blocked: unverified", "bad")), ("SAMPLE-0001", "Test (synthetic)", "$10,137.00", ST("Verified (test)", "ok"))])),
  ("flow", "Retrieval, import and audit pipeline", "pipeline.example.com/admin/pipeline", dict(
     title="Retrieval, import and audit", sub="Collecting never decides; the gate decides",
     nodes=[("Official county pages", "published lists"), ("Retrieval", "download, hash, log source"), ("Parsers", "per-source layouts", ST("3 sources", "ok")), ("Case store", "duplicates flagged"), ("Funds gate", "blocked until verified", ST("Strict", "warn")), ("Audit log", "tamper-evident hash chain", ST("Intact", "ok"))])),
  ("dash", "Acceptance results: 32 of 32 checks", "pipeline.example.com/acceptance", dict(
     nav=["Cases", "Sources", "Verify", "Audit log", "Reports"], active=4, title="Acceptance results", sub="Demonstration run on official sources", range="Latest run",
     kpis=[("Checks passed", "32 / 32", "all pass", "ok"), ("Cases imported", "351", "3 sources", "muted"), ("Cleared by gate", "0", "unverified", "warn")],
     chart=dict(kind="bars", title="Rows imported per source", vals=[136, 30, 174, 11], labels=["List A", "List B", "List C", "List D"]),
     list=dict(title="Checks by group", items=[("Funds gate", 9), ("AI case analysis", 6), ("Retrieval and import", 5), ("Evidence log", 5), ("Duplicates", 4)]))),
 ],
 "school-management-system": [
  ("dash", "Admin dashboard: attendance and fees", "school.example.com/admin", dict(
     nav=["Overview", "Students", "Attendance", "Fees", "Exams", "Timetable"], title="Admin dashboard", sub="Greenfield School · Term 2", range="This term",
     kpis=[("Students", "1,284", "+32"), ("Attendance today", "94.2%", "+0.8%"), ("Fees collected", "$61.4k", "+9%")],
     chart=dict(title="Attendance this term (%)", vals=[92.1, 93.4, 92.8, 94.0, 93.6, 94.8, 94.2], labels=["W1", "W2", "W3", "W4", "W5", "W6", "W7"], unit="%", fmt=k1),
     list=dict(title="Fees by class ($k)", items=[("Grade 8", 9.8), ("Grade 7", 9.1), ("Grade 9", 8.4), ("Grade 6", 7.9), ("Grade 10", 7.2)]))),
  ("table", "Fee vouchers and defaulters", "school.example.com/fees", dict(
     nav=["Overview", "Students", "Attendance", "Fees", "Exams", "Timetable"], active=3, title="Fee vouchers", sub="Term 2 · 312 outstanding", filters=["All", "Paid", "Unpaid", "Overdue"], search="Search student",
     cols=[("Student", 2.2), ("Class", 0.9), ("Voucher", 1.3), ("Due", 1, "r"), ("Status", 1.4)],
     rows=[("Ayesha Rahman", "8-B", "V-20418", "$240", ST("Paid", "ok")), ("Omar Siddiqui", "7-A", "V-20419", "$240", ST("Overdue", "bad")), ("Zara Ali", "9-C", "V-20420", "$260", ST("Unpaid", "warn")),
           ("Hamza Khan", "6-B", "V-20421", "$220", ST("Paid", "ok")), ("Maryam Noor", "10-A", "V-20422", "$280", ST("Unpaid", "warn")), ("Bilal Ahmed", "8-A", "V-20423", "$240", ST("Overdue", "bad"))])),
  ("doc", "Report card preview", "school.example.com/students/24/report", dict(
     doc=dict(**{"from": "Greenfield School"}, from_sub="Term 2 · 2025-26", title="REPORT CARD", number="Grade 8-B", to="Ayesha Rahman", to_sub="Roll no. 24", date="Term 2", due="Class teacher: Ms. Khan",
              cols=["Subject", "Marks", "Max", "Grade"], rows=[("Mathematics", "88", "100", "A"), ("English", "84", "100", "A"), ("Science", "91", "100", "A+"), ("History", "79", "100", "B+"), ("Computer Science", "96", "100", "A+")],
              totals=[("Total", "438 / 500", False), ("Percentage", "87.6%", False), ("Result", "Pass · A", True)]))),
 ],
 "multi-vendor-marketplace": [
  ("cards", "Storefront with products from many vendors", "shop.example.com", dict(
     variant="grid", title="Storefront", sub="1,240 products from 86 vendors", right="Cart (2)",
     cards=[dict(name="Handwoven basket", meta="by Terra Home · 4.8 rating", price="$24.00", badge="Free shipping", tag="NEW", bullets=["Natural fibre", "Ships in 2 days"]),
            dict(name="Ceramic pour-over set", meta="by Kiln & Co · 4.9 rating", price="$48.00", badge="", tag="", bullets=["Dishwasher safe", "Gift boxed"]),
            dict(name="Linen throw blanket", meta="by Nordic Loom · 4.7 rating", price="$62.00", badge="-15%", tag="SALE", bullets=["100% linen", "Three colours"])])),
  ("table", "Vendor orders and payouts", "shop.example.com/admin/payouts", dict(
     nav=["Orders", "Vendors", "Payouts", "Products", "Reports"], active=2, title="Vendor orders and payouts", sub="This week", filters=["All", "Pending", "Paid out"], search="Search order",
     cols=[("Order", 1.2), ("Vendor", 2), ("Total", 1, "r"), ("Commission", 1.1, "r"), ("Payout", 1.4)],
     rows=[("#10482", "Terra Home", "$96.00", "$9.60", ST("Paid out", "ok")), ("#10483", "Kiln & Co", "$148.00", "$14.80", ST("Pending", "warn")), ("#10484", "Nordic Loom", "$62.00", "$6.20", ST("Paid out", "ok")),
           ("#10485", "Terra Home", "$24.00", "$2.40", ST("Pending", "warn")), ("#10486", "Studio Sage", "$215.00", "$21.50", ST("Paid out", "ok")), ("#10487", "Kiln & Co", "$48.00", "$4.80", ST("Pending", "warn"))])),
  ("dash", "Admin: commissions and sales", "shop.example.com/admin", dict(
     nav=["Orders", "Vendors", "Payouts", "Products", "Reports"], active=4, title="Marketplace overview", sub="All vendors", range="Last 30 days",
     kpis=[("Gross sales", "$184k", "+11%"), ("Commission", "$18.4k", "+11%"), ("Active vendors", "86", "+5")],
     chart=dict(title="Gross sales per week ($k)", vals=[38, 41, 39, 46, 44, 52, 48, 56], labels=["W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8"]),
     list=dict(title="Top vendors", items=[("Studio Sage", 31), ("Kiln & Co", 27), ("Terra Home", 22), ("Nordic Loom", 18), ("Field & Fern", 12)]))),
 ],
 "inventory-order-management": [
  ("table", "Stock by warehouse and product", "stock.example.com/inventory", dict(
     nav=["Stock", "Orders", "Purchasing", "Warehouses", "Reports"], title="Stock by warehouse", sub="3 warehouses · 2,410 SKUs", filters=["All", "Low stock", "Out of stock"], search="Search product or SKU",
     cols=[("Product", 2.4), ("SKU", 1.2), ("Warehouse", 1.4), ("On hand", 0.9, "r"), ("Status", 1.4)],
     rows=[("Steel water bottle", "SB-1001", "Main", "412", ST("In stock", "ok")), ("Canvas tote bag", "CT-2208", "East", "38", ST("Low stock", "warn")), ("Desk lamp, black", "DL-3310", "Main", "96", ST("In stock", "ok")),
           ("Notebook A5 (10 pk)", "NB-4402", "West", "0", ST("Out of stock", "bad")), ("Ceramic mug", "CM-5517", "Main", "220", ST("In stock", "ok")), ("Phone stand", "PS-6021", "East", "24", ST("Low stock", "warn"))])),
  ("kanban", "Orders by status", "stock.example.com/orders", dict(
     title="Orders", sub="Today · 28 open orders",
     cols=[("New", 4, [("SO-5821", "Harbor Cafe · 6 lines", ST("Today", "info")), ("SO-5822", "Metro Print · 2 lines", ST("Today", "info")), ("SO-5823", "City Florist · 9 lines", ST("Tomorrow", "muted"))]),
           ("Picking", 3, [("SO-5817", "Greenleaf Market · 12 lines", ST("Picker: Sam", "warn")), ("SO-5818", "Oakline Pharmacy · 4 lines", ST("Picker: Ana", "ok")), ("SO-5819", "Bright Dental · 3 lines", ST("Picker: Sam", "ok"))]),
           ("Shipped", 3, [("SO-5810", "Northwind Foods", ST("Tracking sent", "ok")), ("SO-5811", "Harbor Cafe", ST("Tracking sent", "ok")), ("SO-5812", "Metro Print", ST("Delivered", "ok"))])])),
  ("dash", "Low stock and reorder suggestions", "stock.example.com/reports/reorder", dict(
     nav=["Stock", "Orders", "Purchasing", "Warehouses", "Reports"], active=4, title="Reorder suggestions", sub="Based on 90 days of sales", range="Last 90 days",
     kpis=[("Stock value", "$212k", "+3%"), ("Low-stock SKUs", "46", "+8", "warn"), ("Suggested POs", "9", "to review", "muted")],
     chart=dict(kind="bars", title="Units sold per month", vals=[1840, 1960, 2210, 2050, 2380, 2540], labels=["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]),
     list=dict(title="Suggested reorders", items=[("Notebook A5 (10 pk)", 400), ("Canvas tote bag", 250), ("Phone stand", 180), ("Desk lamp, black", 120), ("Ceramic mug", 90)]))),
 ],
 "hr-leave-payroll-portal": [
  ("cal", "Team leave calendar", "people.example.com/leave/calendar", dict(
     mode="rows", nav=["Overview", "People", "Leave", "Attendance", "Payroll", "Reports"], active=2, title="Team leave", sub="Operations · March", range="Week view",
     days=[("Mon", "17"), ("Tue", "18"), ("Wed", "19"), ("Thu", "20"), ("Fri", "21")], today=2, hours=["Ana F.", "Ben T.", "Chloe M.", "Dev K.", "Elena R.", "Farid S."],
     events=[(0, 0, 3, ("Annual leave", ""), "info"), (1, 2, 1, ("Sick", ""), "bad"), (2, 1, 4, ("Annual leave", ""), "info"), (3, 3, 2, ("Training", ""), "warn"), (4, 0, 1, ("Half day", ""), "ok"), (5, 4, 1, ("Leave", ""), "info")])),
  ("table", "Payroll run with totals", "people.example.com/payroll/runs/2026-03", dict(
     nav=["Overview", "People", "Leave", "Attendance", "Payroll", "Reports"], active=4, title="Payroll run · March 2026", sub="42 employees · status: ready to approve", filters=["All", "Operations", "Sales", "Finance"], search="Search employee",
     cols=[("Employee", 2.2), ("Department", 1.4), ("Gross", 1, "r"), ("Deductions", 1.1, "r"), ("Net pay", 1, "r")],
     rows=[("Ana Ferreira", "Operations", "$4,820", "$1,106", "$3,714"), ("Ben Tran", "Sales", "$5,200", "$1,248", "$3,952"), ("Chloe Martin", "Finance", "$6,100", "$1,520", "$4,580"),
           ("Dev Kapoor", "Operations", "$4,300", "$980", "$3,320"), ("Elena Rossi", "Sales", "$4,950", "$1,150", "$3,800"), ("Farid Said", "Finance", "$5,600", "$1,360", "$4,240"), ("Total (42)", "", "$198,400", "$46,210", "$152,190")])),
  ("doc", "Payslip preview", "people.example.com/payslips/2026-03", dict(
     doc=dict(**{"from": "Harbor & Co"}, from_sub="Payslip", title="PAYSLIP", number="March 2026", to="L. Ferreira", to_sub="Operations · ID 0231", date="Pay date 28 Mar", due="Paid by bank transfer",
              cols=["Earnings", "Hours", "Amount"], rows=[("Basic salary", "160", "$4,200"), ("Overtime", "12", "$420"), ("Allowances", "", "$200"), ("Tax and insurance", "", "-$1,106")],
              totals=[("Gross pay", "$4,820.00", False), ("Deductions", "$1,106.00", False), ("Net pay", "$3,714.00", True)]))),
 ],
}
