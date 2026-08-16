Setup before recording/presenting
Have three terminals/windows open and ready:

Terminal A — API running: uvicorn app.main:app --reload (port 8000)

Terminal B — customer site running: cd customer_site && python -m http.server 5500

Browser — one tab on http://localhost:5500 (customer site), one tab on API docs http://localhost:8000/docs or a REST client (Postman/curl) for auth calls




Step 1 — Create the widget, show the embed snippet
Log in and create a widget via the authenticated API:

bash
curl -X POST http://localhost:8000/widgets \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "signup_form",
    "title": "GreenLeaf Cafe Newsletter",
    "fields": [{"name":"email","type":"email","required":true}],
    "button_text": "Subscribe"
  }'
  Response includes embed_snippet:

xml
<script src="http://localhost:8000/widget.js?id=8f2a-91cd"></script>
Say out loud: "This one line is the entire product — it's what a real customer pastes into their site."




Step 2 — Show it rendering on a page you didn't build
Paste that exact snippet into customer_site/index.html, save, and reload http://localhost:5500 in the browser.

Point out: the widget form appears — and the page is served on port 5500 while the API is on port 8000, so this is a genuine cross-origin load, not a same-site trick.


Step 3 — Submit the form, show it enriched in the dashboard
Type a real email into the rendered form and submit. Then immediately hit the dashboard:

bash
curl http://localhost:8000/dashboard/submissions -H "Authorization: Bearer $TOKEN"
Point out: the stored row has country and city populated — that's the IP→geo enrichment working live, not mocked.


Step 4 — Attack yourself (this is the part that impresses evaluators)
Do three things back to back, narrating each:

Bad payload: submit the form with the email field empty (or curl -d '{"widget_id":"8f2a-91cd","data":{}}') → show the clean 400 JSON, not a crash.

Disallowed origin: open the browser console on a third origin not in your CORS_ALLOWED_ORIGINS list and try fetch() against /submissions → show the CORS error in the console. Say: "the browser itself refuses this — that's CORS protecting my API before my code even runs."

Burst/rate limit: fire 6+ rapid requests (for i in {1..6}; do curl -s -o /dev/null -w "%{http_code}\n" -X POST ...; done) → show the 429 appear on request 6, then immediately send one more normal request and show it still succeeds. This proves the limiter didn't take the whole service down.




Step 5 — Kill the primary geo provider live
Temporarily break provider A, e.g.:

bash
export GEO_PROVIDER_A_URL=http://localhost:9999/broken/
# restart the server or just patch the env var if hot-reloaded
Submit again. Show: the submission still stores country/city — pulled from provider B this time. Then break provider B too (point it at another dead URL) and submit once more — show: the row still saves, just with country: null. Say the brief's exact line: "degrade, never fail."



Step 6 — Break the email side effect
bash
export FORCE_EMAIL_FAILURE=true
Submit once more. Show: the API still returns 200 {"status": "ok"} and the row is in the dashboard, even though your terminal log shows the fake SMTP throwing an exception. Say: "non-critical failures never break the main path." — this is the exact sentence the brief tells you to say.



Step 7 — Close on the dashboard
bash
curl http://localhost:8000/dashboard/stats -H "Authorization: Bearer $TOKEN"
Show the total, by_widget, and by_country breakdown on screen as your closing shot — "my application safely accepts data from websites you don't own".





