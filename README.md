# Guess The Word
Guess The Word is a full-stack five-letter word game. Players receive a limited number of guesses, while administrators can review daily activity and individual user reports.

## Features

- Five-letter word guessing with exact, misplaced, and missing-letter feedback
- Up to three games per player per day
- Five guesses per game
- Player and administrator account roles
- JWT-based authentication in FastAPI and session-compatible authentication in Java
- Administrator reports for daily activity and user history
- Seeded word database
- Automated tests for the game-evaluation logic

## Architecture

```text
Django frontend -> Java backend (preferred when available)
				-> FastAPI backend (fallback)
```

- **Django** serves the web pages and static assets.
- **Java/Spring Boot** provides authentication, gameplay, and reporting APIs on port `8081`.
- **FastAPI** provides the Python implementation on port `8000`.
- **PostgreSQL** stores the Python backend's users, words, games, and guesses.
- **H2** is the default local database for the Java backend.

The frontend automatically checks the Java backend first. If Java is not
running, requests use FastAPI instead. Users do not need to select a backend.

## Requirements

- Conda
- PostgreSQL for the FastAPI backend
- A Conda environment named `guess_word`
- Java 17 or newer and Maven for the Java backend

## Installation

From the project root:

```bash
conda activate guess_word
pip install -r requirements.txt
conda install -n guess_word openjdk=21 -y
```

Create a `.env` file in the project root and configure the FastAPI database:

```env
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/guess_the_word
SECRET_KEY=replace-with-a-secure-secret
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Database Setup

Initialize the Django database before the first frontend start:

```bash
conda run -n guess_word python frontend/manage.py migrate
```

The FastAPI application creates its SQLAlchemy tables and seeds the default
word list when it starts. The Java backend creates its JPA tables and seeds the
same word list when it starts. Its local H2 database is stored under
`java-backend/data/`.

## Running the Project

Run the backend and frontend in separate terminals from the project root.

Start FastAPI:

```bash
conda run -n guess_word python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Start the Java backend:

```bash
cd java-backend
conda run -n guess_word mvn spring-boot:run
```

Start Django in another terminal:

```bash
conda run -n guess_word python frontend/manage.py runserver 127.0.0.1:8001
```

Java backend configuration is in
`java-backend/src/main/resources/application.properties`. Set
`SPRING_DATASOURCE_URL`, `SPRING_DATASOURCE_USERNAME`, and
`SPRING_DATASOURCE_PASSWORD` to use PostgreSQL instead of local H2.

Available services:

| Service | URL |
| --- | --- |
| Web application | http://127.0.0.1:8001/ |
| FastAPI root | http://127.0.0.1:8000/ |
| Java backend root | http://127.0.0.1:8081/ |
| FastAPI API documentation | http://127.0.0.1:8000/docs |

Both backends expose these frontend API routes:

- `POST /api/register`
- `POST /api/login`
- `POST /api/game/start`
- `POST /api/game/{game_id}/guess`
- `GET /api/admin/report/day`
- `GET /api/admin/report/user/{user_id}`

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

java-backend/
├── src/main/java/com/guesstheword/
│   ├── auth/       Authentication endpoints
│   ├── game/       Game models, routes, and word seeding
│   ├── reports/    Administrator report endpoints
│   └── user/       User entity and repository
├── src/main/resources/application.properties
└── pom.xml

frontend/
├── config/        Django project configuration
├── game/          Django views and URL routes
├── static/        CSS and JavaScript assets
└── templates/     Django HTML templates
```

## Testing

Run the Python test suite with:

```bash
conda run -n guess_word python -m pytest -q
```

Run the Java backend tests/build with:

```bash
cd java-backend
conda run -n guess_word mvn test
```

The Python tests cover exact matches, misplaced letters, missing letters,
mixed feedback, and duplicate-letter handling.