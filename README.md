# FlashDeck Backend

FlashDeck is a spaced-repetition study application backend built with Django REST Framework.

## Features

* JWT authentication
* User registration and login
* Deck CRUD API
* Card CRUD API
* Study endpoint
* Review and Box Ladder system
* Statistics API
* Search, filtering and pagination
* User-based data isolation

## Technologies

* Python
* Django
* Django REST Framework
* SimpleJWT
* django-filter
* SQLite
* django-cors-headers

## Setup

Clone the repository and enter the project folder:


cd flashdeck-backend


Create and activate a virtual environment:

python -m venv venv


Windows:


venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


Create `.env` from `.env.example` and configure the required values.

Run migrations:

python manage.py migrate


Create an admin user:

python manage.py createsuperuser


Start the development server:


python manage.py runserver

The API will be available at:


http://127.0.0.1:8000/

## Main API Endpoints

### Authentication


POST /api/register/
POST /api/login/
POST /api/token/refresh/


### Decks


GET    /api/decks/
POST   /api/decks/
GET    /api/decks/<id>/
PATCH  /api/decks/<id>/
DELETE /api/decks/<id>/
GET    /api/decks/<id>/study/


### Cards

GET    /api/cards/
POST   /api/cards/
GET    /api/cards/<id>/
PATCH  /api/cards/<id>/
DELETE /api/cards/<id>/
POST   /api/cards/<id>/review/


### Statistics


GET /api/stats/

## Review System

Cards use five review boxes:


Box 1 → 0 days
Box 2 → 1 day
Box 3 → 3 days
Box 4 → 7 days
Box 5 → 16 days

A correct answer moves a card to the next box.

A wrong answer moves the card back to Box 1.

## Security

* JWT authentication is used for protected endpoints.
* Users can only access their own decks and cards.
* Passwords are stored using Django's password hashing.
* Sensitive environment variables are excluded from Git.



## Frontend

The React frontend is maintained in a separate repository.

flashdeck-frontend - https://github.com/TanzumSamrin/samrin-flashdeck-frontend.git

