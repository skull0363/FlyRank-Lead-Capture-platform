Embeddable Widget & Lead Capture Platform

A platform that lets a customer define a widget — signup form, CTA, or popover — and embed it on any website with a single <script> tag. Built for the FlyRank Internship Backend Track capstone.

When a visitor on an external site submits the widget's form, the request is validated, rate-limited, spam-filtered with a honeypot, enriched with IP-based geolocation through a two-provider fallback chain, stored, and shown to the widget's owner in an authenticated dashboard — all while the service treats the request as coming from a browser it does not control and cannot trust.

Setup:

git clone <this-repo-url>
cd flyrank-lead-capture-platform
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # fill in DATABASE_URL, JWT_SECRET, CORS_ALLOWED_ORIGINS
docker compose up -d   # starts Postgres

Run the service: 
uvicorn app.main:app --reload

Serve the "customer site" test page on a different origin (a second local port, proving genuine cross-origin behavior):
cd customer_site && python -m http.server 5500

Run the tests:
pytest -v


TRY IT:
# Register and grab a token
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Cafe Owner","email":"owner@example.com","password":"correct-horse-battery-staple"}'

# Create a widget (use the access_token from above)
curl -X POST http://localhost:8000/widgets \
  -H "Authorization: Bearer <token>" -H "Content-Type: application/json" \
  -d '{"type":"signup_form","title":"Newsletter","fields":[{"name":"email","type":"email","required":true}],"button_text":"Subscribe"}'

# Submit the form as a visitor (cross-origin in practice, curl for simplicity here)
curl -X POST http://localhost:8000/submissions \
  -H "Content-Type: application/json" \
  -d '{"widget_id":"<widget-id>","data":{"email":"visitor@example.com"}}'

# View the dashboard
curl http://localhost:8000/dashboard/stats -H "Authorization: Bearer <token>"