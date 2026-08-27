Customers need to define a widget (signup form, CTA, popover) and embed it on any website with a single 'script' tag. When a visitor on that external site submits the form, the request arrives from a browser this service does not control — it cannot trust the input, control the traffic, or predict the origin. The system validates, rate-limits, spam-filters, geo-enriches, and stores that submission safely, then shows it to the widget's owner in a dashboard.

Data model — three core tables
tenants(id, name, email UNIQUE, password_hash, created_at)

widgets(id, tenant_id FK, type, title, description, fields JSON, button_text, display_options JSON, version, created_at)

submissions(id, widget_id FK, tenant_id FK, payload JSON, ip_address, country, city, is_spam bool, idempotency_key, created_at)

Index submissions(widget_id, created_at) and widgets(tenant_id). submissions.idempotency_key is unique per widget_id (not globally), so a visitor's retried submission is deduplicated without colliding across different widgets. Auth uses email + bcrypt password hash + short-lived JWT — not API keys.

API surface (sketch, build in this order)
POST /auth/register, POST /auth/login → JWT

POST/GET/PUT/DELETE /widgets (authenticated, tenant-scoped)

GET /widgets/{id}/config (public, cached)

GET /widget.js (public, versioned, cached long)

POST /submissions (public, CORS, rate-limited)

GET /dashboard/stats, GET /dashboard/submissions (authenticated)

Layer sketch
text
HTTP layer      app/api/auth.py, widgets.py, submissions.py, delivery.py, dashboard.py
                    ▼
Service layer   app/services/auth.py, geo.py, notify.py
                    ▼
Persistence     app/models/models.py, app/db.py
Routes never call httpx, passlib, or SMTP/notification logic directly — always through the service layer. Swapping the geo provider, email provider, or database engine should not touch route logic.

Non-goal
No real CDN/hosting — customer site is a local HTML file on a second port. No drag-and-drop widget builder UI.