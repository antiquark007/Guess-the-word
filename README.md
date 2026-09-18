# Guess The Word

A word guessing game built using:

- Django
- FastAPI
- PostgreSQL
- SQLAlchemy
- JavaScript
- pytest

## Architecture

Django -> FastAPI -> PostgreSQL

## Requirements

- Conda
- PostgreSQL
- A Conda environment named `guess_word`

Install the Python dependencies into the environment:

```bash
conda activate guess_word
pip install -r requirements.txt
```

Configure the PostgreSQL connection in `.env`:

```env
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/guess_the_word
SECRET_KEY=secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Run the Project

Run these commands from the project root in separate terminals.

Start the FastAPI backend:

```bash
conda run -n guess_word python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Start the Django frontend:

```bash
conda run -n guess_word python frontend/manage.py runserver 127.0.0.1:8001
```

The services are available at:

- Frontend: http://127.0.0.1:8001/
- FastAPI root: http://127.0.0.1:8000/
- FastAPI documentation: http://127.0.0.1:8000/docs

Before the first frontend start, initialize Django's local database:

```bash
conda run -n guess_word python frontend/manage.py migrate
```

## Tests

Run the available Python tests with:

```bash
conda run -n guess_word python -m pytest -q
```