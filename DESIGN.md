Data model — two core tables:

tenants(id, name, api_key_hash, created_at)

widgets(id, tenant_id FK, type, title, description, fields JSONB, button_text, display_options JSONB, created_at, version)

submissions(id, widget_id FK, tenant_id FK, payload JSONB, ip_address, country, city, is_spam bool, created_at)

Index submissions(widget_id, created_at) and widgets(tenant_id).

Embed flow: <script src="/widget.js?id=abc123"> → script fetches GET /widgets/:id/config (cached, CORS-open) → renders a form in a <div> → on submit, POST /submissions (CORS-open, public).

API surface (sketch, build in this order):

POST /auth/register, POST /auth/login → JWT

POST/GET/PUT/DELETE /widgets (authenticated, tenant-scoped)

GET /widgets/{id}/config (public, cached)

GET /widget.js (public, versioned, cached long)

POST /submissions (public, CORS, rate-limited)

GET /dashboard/stats, GET /dashboard/submissions (authenticated)

Explicit non-goal: e.g. "No real CDN/hosting — customer site is a local HTML file on a second port. No drag-and-drop widget builder UI."