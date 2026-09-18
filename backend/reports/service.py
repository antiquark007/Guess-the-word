from datetime import datetime, timedelta
from collections import defaultdict

from sqlalchemy.orm import Session

from backend.database.models import (
    User,
    Game
)


def get_day_range(date):

    start = datetime(date.year,
        date.month,
        date.day
    )

    end = start + timedelta(days=1)

    return start, end


def get_daily_report(
    db: Session,
    date
):

    start, end = get_day_range(date)

    number_of_users = (
        db.query(Game.user_id)
        .filter(
            Game.started_at >= start,
            Game.started_at < end
        )
        .distinct()
        .count()
    )

    number_of_correct_guesses = (
        db.query(Game)
        .filter(
            Game.started_at >= start,
            Game.started_at < end,
            Game.status == "WON"
        )
        .count()
    )

    return {
        "date": str(date),
        "number_of_users": number_of_users,
        "number_of_correct_guesses":
            number_of_correct_guesses
    }


def get_user_report(
    db: Session,
    user_id: int
):

    games = (
        db.query(Game)
        .filter(Game.user_id == user_id)
        .order_by(Game.started_at.desc())
        .all()
    )

    daily_totals = defaultdict(
        lambda: {"words_tried": 0, "correct_guesses": 0}
    )

    for game in games:
        day = game.started_at.date().isoformat()
        daily_totals[day]["words_tried"] += 1

        if game.status == "WON":
            daily_totals[day]["correct_guesses"] += 1

    return [
        {
            "date": day,
            **totals
        }
        for day, totals in sorted(
            daily_totals.items(),
            reverse=True
        )
    ]