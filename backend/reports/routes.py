# Provides protected API endpoints for daily and user reports.
from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.models import User
from backend.auth.security import require_admin

from .service import get_daily_report,get_user_report


router = APIRouter(
    prefix="/api/admin",
    tags=["Admin Reports"]
)

@router.get("/report/day")
def daily_report(
    report_date: date,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):

    return get_daily_report( db, report_date )


@router.get("/report/user/{user_id}")
def user_report(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):

    return get_user_report( db, user_id )