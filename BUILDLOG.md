Where AI helped:

Learning FastAPI patterns for public, unauthenticated endpoints. This capstone's public submission endpoint needed patterns I hadn't used before — CORS middleware configuration, slowapi rate limiting decorators, and structuring routes so an anonymous browser request could be safely validated before touching business logic.

JWT-based authentication. I used AI to understand the python-jose pattern for password hashing and how to wire a Depends()-based auth dependency so every authenticated route could resolve "who is calling this" consistently.

I used AI to review my submission-handling logic, CORS setup, and the geo provider fallback chain against the capstone brief's Definition of Done, to catch gaps before considering a phase finished.

Where AI was wrong:
My original app/main.py set up CORS middleware and the rate-limit exception handler, but never actually called app.include_router for any of my route files — widgets, submissions, delivery, and dashboard all existed as fully written files that were never mounted onto the app. Every endpoint would have 404'd. I only caught this by trying to hit the endpoints directly rather than assuming "the file exists" meant "the route works."