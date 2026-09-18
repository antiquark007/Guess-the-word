from fastapi import (APIRouter,Depends)

from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.auth.security import get_current_user
from backend.database.models import User

from .service import (start_game,submit_guess)


router = APIRouter(
    prefix="/api/game",
    tags=["Game"]
)


@router.post("/start")
def start_game_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    game = start_game(db,current_user)

    return {"game_id": game.id,"message": "Game started"}


@router.post("/{game_id}/guess")
def submit_guess_api(
    game_id: int,
    guess: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return submit_guess(
        db,
        game_id,
        current_user,
        guess
    )