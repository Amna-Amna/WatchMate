# Watchmate

A small Django + Django REST Framework project for tracking streaming platforms, watchlist items, and user reviews.

User story

- As a regular user, I want to browse streaming platforms and watchlist items, add items to my personal watchlist, and post reviews so I can track and rate what I watch.

Quick setup

1. Create and activate a virtual environment:

   python -m venv .venv
   # Windows
   .\.venv\Scripts\activate

2. Install dependencies:

   pip install -r requirements.txt

3. Apply migrations and run the server:

   python manage.py migrate
   python manage.py runserver

Key notes (short)

- Permissions: Review and watchlist modification endpoints enforce ownership—users can only edit or delete their own reviews. See `watchlist_app/api/permissions.py` for the permission classes.

- Throttling: Custom throttling limits how often clients can create or update reviews to prevent abuse. See `watchlist_app/api/throttling.py` and `watchmate/settings.py` for throttle configuration.

API endpoints and quick curl examples

Base path prefixes defined in `watchmate/urls.py`:
- Watchlist API: `/movie/`
- Account API (register/login/logout): `/account/`

Common endpoints (relative to server root `http://localhost:8000`):

- Register (create user)
  - POST `/account/register/`
  - Example:

    curl -X POST http://localhost:8000/account/register/ -H "Content-Type: application/json" -d '{"username":"alice","email":"alice@example.com","password":"secret123","confirm_password":"secret123"}'

- Login (obtain token)
  - POST `/account/login/`
  - Example:

    curl -X POST http://localhost:8000/account/login/ -H "Content-Type: application/json" -d '{"username":"alice","password":"secret123"}'

  - Response contains `token`; use it for authenticated requests in `Authorization: Token <token>` header.

- List watchlists
  - GET `/movie/watchlist/`
  - Example:

    curl http://localhost:8000/movie/watchlist/

- Watchlist detail
  - GET `/movie/watchlist/<id>/`
  - Example:

    curl http://localhost:8000/movie/watchlist/1/

- Create review for a watchlist item (authenticated)
  - POST `/movie/watchlist/<watchlist_id>/create-review/`
  - Example:

    curl -X POST http://localhost:8000/movie/watchlist/1/create-review/ -H "Content-Type: application/json" -H "Authorization: Token YOUR_TOKEN" -d '{"rating":5,"description":"Loved it!"}'

- List reviews for a watchlist item
  - GET `/movie/watchlist/<watchlist_id>/reviews/`
  - Example:

    curl http://localhost:8000/movie/watchlist/1/reviews/

- Review detail (retrieve/update/delete; authenticated + ownership for unsafe methods)
  - `/movie/watchlist/<watchlist_id>/review/<review_id>/`
  - Example retrieve:

    curl http://localhost:8000/movie/watchlist/1/review/2/

Notes

- Replace `YOUR_TOKEN` with the token returned by the login endpoint.
- Throttling may return HTTP 429 for too many requests; permissions return 403 when actions are not allowed.
