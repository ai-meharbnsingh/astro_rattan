"""Feedback routes — user ratings + text feedback, admin management + word cloud."""
import re
from collections import Counter
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.auth import get_current_user, require_role
from app.database import get_db

router = APIRouter(tags=["feedback"])

# ── Stop words for word cloud ─────────────────────────────────────────────────
_STOP = {
    "the","a","an","and","or","but","in","on","at","to","for","of","with","by",
    "from","as","is","was","are","were","be","been","being","have","has","had",
    "do","does","did","will","would","could","should","may","might","shall",
    "this","that","these","those","it","its","i","me","my","we","our","you",
    "your","he","she","they","them","their","what","which","who","how","when",
    "where","why","not","no","very","so","if","then","than","more","also","just",
    "can","get","got","use","used","using","one","all","app","page","site","please",
    "need","want","like","think","make","good","great","nice","really","work","works",
    "still","even","some","any","yes","but","its","too","much","lot","bit",
}


# ── Payload models ────────────────────────────────────────────────────────────
class FeedbackPayload(BaseModel):
    rating_interface: Optional[int] = None
    rating_reports: Optional[int] = None
    rating_calculations: Optional[int] = None
    feedback_text: Optional[str] = None


class AdminUpdate(BaseModel):
    action_taken: Optional[str] = None   # yes | no | NR
    admin_remarks: Optional[str] = None


# ── User: submit ──────────────────────────────────────────────────────────────
@router.post("/api/feedback", status_code=201)
def submit_feedback(
    payload: FeedbackPayload,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    for r in [payload.rating_interface, payload.rating_reports, payload.rating_calculations]:
        if r is not None and not (1 <= r <= 5):
            raise HTTPException(status_code=422, detail="Ratings must be 1–5")
    if not any([
        payload.rating_interface, payload.rating_reports,
        payload.rating_calculations, payload.feedback_text,
    ]):
        raise HTTPException(status_code=422, detail="Provide at least one rating or comment")

    text = (payload.feedback_text or "").strip()[:2000] or None
    db.execute(
        """INSERT INTO feedback
               (user_id, rating_interface, rating_reports, rating_calculations, feedback_text)
           VALUES (%s, %s, %s, %s, %s)""",
        (current_user["sub"], payload.rating_interface, payload.rating_reports,
         payload.rating_calculations, text),
    )
    db.commit()
    return {"message": {"en": "Feedback submitted — thank you!", "hi": "फीडबैक सबमिट हो गया — धन्यवाद!"}}


# ── User: my history ──────────────────────────────────────────────────────────
@router.get("/api/feedback/my")
def get_my_feedback(
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    rows = db.execute(
        """SELECT id, rating_interface, rating_reports, rating_calculations,
                  feedback_text, status, action_taken, admin_remarks, created_at
           FROM feedback WHERE user_id = %s ORDER BY created_at DESC""",
        (current_user["sub"],),
    ).fetchall()
    return [dict(r) for r in rows]


# ── User: close own feedback ──────────────────────────────────────────────────
@router.patch("/api/feedback/{feedback_id}/close")
def close_feedback(
    feedback_id: str,
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    row = db.execute(
        "SELECT user_id, status FROM feedback WHERE id = %s", (feedback_id,)
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    if row["user_id"] != current_user["sub"]:
        raise HTTPException(status_code=403, detail="Not your feedback")
    if row["status"] == "closed":
        raise HTTPException(status_code=400, detail="Already closed")
    db.execute(
        "UPDATE feedback SET status='closed', updated_at=NOW() WHERE id=%s", (feedback_id,)
    )
    db.commit()
    return {"message": {"en": "Marked as resolved", "hi": "समाधान के रूप में चिह्नित किया गया"}}


# ── Admin: word cloud — OPEN feedback only ────────────────────────────────────
# IMPORTANT: defined before /{feedback_id} to avoid route shadowing
@router.get("/api/admin/feedback/wordcloud")
def get_wordcloud(
    _: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    rows = db.execute(
        "SELECT feedback_text FROM feedback WHERE status='open' AND feedback_text IS NOT NULL"
    ).fetchall()
    wc: Counter = Counter()
    for row in rows:
        for w in re.findall(r"\b[a-zA-Z]{3,}\b", row["feedback_text"].lower()):
            if w not in _STOP:
                wc[w] += 1
    return [{"word": w, "count": c} for w, c in wc.most_common(60)]


# ── Admin: list all feedback with filters ─────────────────────────────────────
@router.get("/api/admin/feedback")
def get_all_feedback(
    status: Optional[str] = None,
    action_taken: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    _: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    conds, params = [], []
    if status:
        conds.append("f.status = %s"); params.append(status)
    if action_taken:
        conds.append("f.action_taken = %s"); params.append(action_taken)
    where = ("WHERE " + " AND ".join(conds)) if conds else ""

    total = db.execute(
        f"SELECT COUNT(*) as c FROM feedback f {where}", params
    ).fetchone()["c"]

    rows = db.execute(
        f"""SELECT f.id, u.name AS user_name, u.email AS user_email,
                   f.rating_interface, f.rating_reports, f.rating_calculations,
                   f.feedback_text, f.status, f.action_taken, f.admin_remarks,
                   f.created_at
            FROM feedback f JOIN users u ON u.id = f.user_id
            {where}
            ORDER BY f.created_at DESC
            LIMIT %s OFFSET %s""",
        params + [limit, (page - 1) * limit],
    ).fetchall()

    return {
        "items": [dict(r) for r in rows],
        "total": total,
        "page": page,
        "pages": max(1, -(-total // limit)),
    }


# ── Admin: update action_taken + remarks ──────────────────────────────────────
@router.patch("/api/admin/feedback/{feedback_id}")
def admin_update_feedback(
    feedback_id: str,
    payload: AdminUpdate,
    _: dict = Depends(require_role("admin")),
    db: Any = Depends(get_db),
):
    if payload.action_taken and payload.action_taken not in ("yes", "no", "NR"):
        raise HTTPException(status_code=422, detail="action_taken must be yes | no | NR")
    if not db.execute("SELECT 1 FROM feedback WHERE id=%s", (feedback_id,)).fetchone():
        raise HTTPException(status_code=404, detail="Not found")

    updates, params = ["updated_at=NOW()"], []
    if payload.action_taken is not None:
        updates.append("action_taken=%s"); params.append(payload.action_taken)
    if payload.admin_remarks is not None:
        updates.append("admin_remarks=%s"); params.append(payload.admin_remarks[:1000])

    db.execute(
        f"UPDATE feedback SET {', '.join(updates)} WHERE id=%s",
        params + [feedback_id],
    )
    db.commit()
    return {"message": {"en": "Updated", "hi": "अपडेट किया गया"}}
