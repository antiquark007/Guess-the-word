# Manages game creation, guess validation, scoring, and game results.
from datetime import datetime, timedelta
import random

from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.database.models import (Game,Guess,Word,User)

from .logic import evaluate_guess


MAX_GAMES_PER_DAY = 3
MAX_GUESSES_PER_GAME = 5


def get_today_range():

    now = datetime.utcnow()

    start = datetime(
        now.year,
        now.month,
        now.day
    )

    end = start + timedelta(days=1)

    return start, end


def start_game(
    db: Session,
    user: User
):

    start, end = get_today_range()# one day range 

    #total no of the games played today 
    games_today = (
        db.query(Game)
        .filter(
            Game.user_id == user.id,
            Game.started_at >= start,
            Game.started_at < end
        )
        .count()
    )
    
    # test the today limit
    if games_today >= MAX_GAMES_PER_DAY: raise HTTPException(status_code=400, detail="You can play only 3 games per day.")

    words = db.query(Word).all()

    if not words: raise HTTPException(status_code=500, detail="No words available.")

    selected_word = random.choice(words)#pick random word from db words

    game = Game(user_id=user.id,word_id=selected_word.id,status="IN_PROGRESS",number_of_guesses=0)

    db.add(game)
    db.commit()
    db.refresh(game)

    return game# adds and gives the current game ins from the db


def submit_guess(
    db: Session,
    game_id: int,
    user: User,
    guess: str
):

    game = (
        db.query(Game)
        .filter(
            Game.id == game_id,
            Game.user_id == user.id
        )
        .first()
    )


   #few important checks for the current game to be submit
    if not game: raise HTTPException(status_code=404, detail="Game not found.")

    if game.status != "IN_PROGRESS": raise HTTPException(status_code=400, detail="This game is already completed.")

    if len(guess) != 5: raise HTTPException(status_code=400, detail="Guess must contain exactly 5 letters.")

    if not guess.isalpha(): raise HTTPException(status_code=400, detail="Guess must contain only letters.")

    if not guess.isupper(): raise HTTPException(status_code=400, detail="Guess must be uppercase.")

    if game.number_of_guesses >= MAX_GUESSES_PER_GAME: raise HTTPException(status_code=400, detail="Maximum 5 guesses allowed.")

    word = (
        db.query(Word)
        .filter(Word.id == game.word_id)
        .first()
    )

    target = word.word

    result = evaluate_guess(target, guess)#returns a list of five color results after matching each of the digits

    guess_number = game.number_of_guesses + 1

    guess_record = Guess(
        game_id=game.id,
        guessed_word=guess,
        guess_number=guess_number
    )

    db.add(guess_record)

    game.number_of_guesses = guess_number

    won = guess == target

    if won:

        game.status = "WON"
        game.completed_at = datetime.utcnow()

    elif guess_number >= MAX_GUESSES_PER_GAME:

        game.status = "LOST"
        game.completed_at = datetime.utcnow()

    db.commit()

    response = {
        "game_id": game.id,
        "guess": guess,
        "result": result,
        "guess_number": guess_number,
        "status": game.status
    }

    if won:

        response["message"] = "Congratulations!"

    elif game.status == "LOST":

        response["message"] = "Better luck next time!"

    else:

        response["message"] = "Keep guessing!"

    return response