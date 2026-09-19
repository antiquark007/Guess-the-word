# Creates and configures the FastAPI application and its API routes.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database.connection import Base, engine
from backend.seed.words import seed_words

from backend.auth.routes import router as auth_router
from backend.game.routes import router as game_router
from backend.reports.routes import router as reports_router


app = FastAPI(
    title="Guess The Word API",
    version="1.0.0"
)

#allowing the diff api req onto it
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8001",
        "http://localhost:8001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(
    bind=engine
)

seed_words()


app.include_router(auth_router)
app.include_router(game_router)
app.include_router(reports_router)


@app.get("/")
def root():

    return {
        "message": "Guess The Word API is running"
    }