# Guess The Word

Guess The Word is a full-stack five-letter word game. Players receive a limited
number of guesses, while administrators can review daily activity and
individual user reports.

## Features

- Five-letter word guessing with exact, misplaced, and missing-letter feedback
- Up to three games per player per day
- Five guesses per game
- Player and administrator account roles
- JWT-based authentication
- Administrator reports for daily activity and user history
- Seeded word database
- Automated tests for the game-evaluation logic

## Architecture

```text
Django frontend -> FastAPI backend -> PostgreSQL database
```

- **Django** serves the web pages and static assets.
- **FastAPI** provides authentication, gameplay, and reporting APIs.
- **SQLAlchemy** manages database models and sessions.
- **PostgreSQL** stores users, words, games, and guesses.

## Requirements

- Conda
- PostgreSQL
- A Conda environment named `guess_word`

## Installation

From the project root:

```bash
conda activate guess_word
pip install -r requirements.txt
```

Create a `.env` file in the project root and configure the database:

```env
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/guess_the_word
SECRET_KEY=replace-with-a-secure-secret
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Do not commit `.env` or production secrets to version control.

## Database Setup

Initialize the Django database before the first frontend start:

```bash
conda run -n guess_word python frontend/manage.py migrate
```

The FastAPI application creates its SQLAlchemy tables and seeds the default
word list when it starts.

## Running the Project

Run the backend and frontend in separate terminals from the project root.

Start FastAPI:

```bash
conda run -n guess_word python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Start Django:

```bash
conda run -n guess_word python frontend/manage.py runserver 127.0.0.1:8001
```

Available services:

| Service | URL |
| --- | --- |
| Web application | http://127.0.0.1:8001/ |
| FastAPI root | http://127.0.0.1:8000/ |
| API documentation | http://127.0.0.1:8000/docs |

## User Roles

Users select an account type during registration:

- **Player**: starts games and submits guesses.
- **Admin**: accesses daily and per-user reports.

Administrator report endpoints require an authenticated user with the `ADMIN`
role.

## Project Structure

```text
backend/
├── auth/          Authentication routes and security helpers
├── database/      Database connection and SQLAlchemy models
├── game/          Game routes, services, and guess evaluation
├── reports/       Administrator reporting routes and services
├── seed/          Default word data
└── tests/         Python tests

frontend/
├── config/        Django project configuration
├── game/          Django views and URL routes
├── static/        CSS and JavaScript assets
└── templates/     Django HTML templates
```

## Testing

Run the test suite with:

```bash
conda run -n guess_word python -m pytest -q
```

The current tests cover exact matches, misplaced letters, missing letters,
mixed feedback, and duplicate-letter handling.