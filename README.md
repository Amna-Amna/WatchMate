# Watchmate API

A RESTful API built with Django and Django REST Framework for a movie and show tracking application. Users can browse streaming platforms, manage watchlists, and post reviews.

## Demo

https://github.com/user-attachments/assets/5b9406d5-40a9-4515-b041-cfe60442d646

## Key Features

This API was built with a focus on security, performance, and robust functionality.

  * **Token-Based Authentication:** Secure user registration, login, and logout endpoints are handled using DRF's built-in token authentication system.
  * **Custom Permissions:** Granular access control is implemented to protect endpoints.
      * Only **administrators** can create, update, or delete `StreamPlatform` and `WatchList` items.
      * Authenticated **users** can only modify or delete their **own** reviews.
  * **API Throttling & Rate Limiting:** Custom throttling rules are in place to prevent abuse. Different rate limits are applied to anonymous users, authenticated users, and specific actions like creating reviews.
  * **Comprehensive Data Validation:** Serializers include custom validation logic to ensure data integrity, such as confirming passwords and checking for unique usernames and emails upon registration.
  * **Advanced Filtering:** The API provides multiple ways to retrieve data, including endpoints to filter reviews by a specific username.
  * **Full CRUD Functionality:** The API provides complete Create, Read, Update, and Delete operations for streaming platforms, watchlist items, and reviews.

-----

## API Endpoints

The API is organized into two main applications: `account` and `movie`.

#### Authentication (`/account/`)

| Method | Endpoint              | Description                    |
| :----- | :-------------------- | :----------------------------- |
| `POST` | `/register/`          | Register a new user.           |
| `POST` | `/login/`             | Obtain an authentication token.|
| `POST` | `/logout/`            | Invalidate the user's token.   |

#### Watchlist & Reviews (`/movie/`)

| Method              | Endpoint                                      | Description                                  |
| :------------------ | :-------------------------------------------- | :------------------------------------------- |
| `GET`, `POST`       | `/stream/list/`                               | List all or create a new streaming platform. |
| `GET`, `PUT`, `DELETE` | `/stream/<id>/`                               | Retrieve, update, or delete a platform.      |
| `GET`, `POST`       | `/watchlist/`                                 | List all or create a new watchlist item.     |
| `GET`, `PUT`, `DELETE` | `/watchlist/<id>/`                            | Retrieve, update, or delete a watchlist item.|
| `GET`               | `/watchlist/<id>/reviews/`                    | List all reviews for a specific watchlist item.|
| `POST`              | `/watchlist/<id>/create-review/`              | Create a new review for a watchlist item.    |
| `GET`, `PUT`, `DELETE` | `/watchlist/<id>/review/<review_id>/`         | Retrieve, update, or delete a specific review.|
| `GET`               | `/user-reviews/<username>/`                   | List all reviews by a specific user.         |
| `GET`               | `/query-reviews/`                              | List all reviews by a specific user using query params. |       |

-----

## Credits

This project was built entirely by me as part of learning Django Rest Framework. **No AI tools were used.**

I relied on the official **Django** and **Django Rest Framework** documentation, as well as community resources like **Stack Overflow**, for research and troubleshooting.

