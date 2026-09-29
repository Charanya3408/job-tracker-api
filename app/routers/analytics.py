from collections import defaultdict
from datetime import timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Application, Status, User

router = APIRouter(prefix="/analytics", tags=["analytics"])


def _pct(part: int, whole: int) -> float:
    return round(100 * part / whole, 1) if whole else 0.0


@router.get("/summary")
def summary(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    rows = db.execute(
        select(Application.status, func.count())
        .where(Application.user_id == user.id)
        .group_by(Application.status)
    ).all()

    counts = {s.value: 0 for s in Status}
    for status, n in rows:
        counts[status.value] = n

    total = sum(counts.values())
    responded = total - counts["applied"]
    interviewing = counts["interview"] + counts["offer"]

    return {
        "total": total,
        "by_status": counts,
        "response_rate_pct": _pct(responded, total),
        "interview_rate_pct": _pct(interviewing, total),
        "offer_rate_pct": _pct(counts["offer"], total),
    }


@router.get("/by-source")
def by_source(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    responded = func.sum(case((Application.status != Status.applied, 1), else_=0))
    interviewing = func.sum(
        case((Application.status.in_([Status.interview, Status.offer]), 1), else_=0)
    )
    rows = db.execute(
        select(
            Application.source,
            func.count().label("total"),
            responded.label("responded"),
            interviewing.label("interviewing"),
        )
        .where(Application.user_id == user.id)
        .group_by(Application.source)
        .order_by(func.count().desc())
    ).all()

    return [
        {
            "source": r.source,
            "total": r.total,
            "response_rate_pct": _pct(int(r.responded), r.total),
            "interview_rate_pct": _pct(int(r.interviewing), r.total),
        }
        for r in rows
    ]


@router.get("/weekly")
def weekly(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    rows = db.execute(
        select(Application.applied_on, func.count())
        .where(Application.user_id == user.id)
        .group_by(Application.applied_on)
    ).all()

    weeks: dict = defaultdict(int)
    for day, n in rows:
        weeks[day - timedelta(days=day.weekday())] += n  # bucket by Monday

    return [
        {"week_start": d.isoformat(), "applications": n}
        for d, n in sorted(weeks.items())
    ]
