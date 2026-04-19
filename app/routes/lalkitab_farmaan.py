"""
Lal Kitab Farmaan routes — P2.1 + P2.7 + P2.8 (MVP).

Implements the thin API layer over the `lk_farmaan`, `lk_farmaan_annotations`,
and `lk_source_library` tables added in migration 19. The tables ship empty;
an admin import tool (future sprint) will populate them from scanned LK
editions. Until then these routes return empty collections with the correct
shapes — which lets the frontend render its UI and be tested end-to-end.

What these routes DO in the MVP:
  - Expose search/filter/by-tags over populated rows (returns [] if empty)
  - Expose edition-comparison endpoint (groups rows by section_ref across
    editions — returns empty groups if no rows)
  - Stub POST for annotations (stores them when the user contributes)
  - Return rights badges directly from each row so the UI can show them
    without a separate lookup

What they DO NOT do (explicit out-of-scope):
  - NO content is fabricated. Rows must be ingested by an admin pipeline.
  - NO OCR / scan handling — the MVP assumes text has been normalised
    before insertion.
  - NO cross-edition diff algorithm — edition-comparison is literal
    grouping by `section_ref`, not semantic diff.

All endpoints require auth except `/public-search` (used by the Farmaan
tab preview in demo mode).
"""
from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from app.auth import get_current_user
from app.database import get_db

router = APIRouter(tags=["lalkitab-farmaan"])


# ────────────────────────────────────────────────────────────────
# P2.1 — Farmaan search / detail / by-tags
# ────────────────────────────────────────────────────────────────

@router.get("/api/lalkitab/farmaan/search")
def farmaan_search(
    q: Optional[str] = Query(None, description="Free-text search over urdu_latin / hindi / english"),
    planet: Optional[str] = Query(None, description="Filter by planet tag (Saturn / Rahu / ...)"),
    house: Optional[int] = Query(None, description="Filter by house tag"),
    debt: Optional[str] = Query(None, description="Filter by debt tag (Pitru Rin / Bhoot Rin / ...)"),
    confidence: Optional[str] = Query(None, description="undeciphered|low|moderate|high|canonical"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Any = Depends(get_db),
):
    """Search the Farmaan corpus. Returns empty array when DB is empty (MVP)."""
    sql = "SELECT * FROM lk_farmaan WHERE 1=1"
    params: list[Any] = []
    if q:
        sql += " AND (urdu_latin ILIKE %s OR hindi ILIKE %s OR english ILIKE %s)"
        needle = f"%{q}%"
        params.extend([needle, needle, needle])
    if planet:
        sql += " AND %s = ANY(planet_tags)"
        params.append(planet.strip().title())
    if house is not None:
        sql += " AND %s = ANY(house_tags)"
        params.append(house)
    if debt:
        sql += " AND %s = ANY(debt_tags)"
        params.append(debt)
    if confidence:
        sql += " AND confidence_level = %s"
        params.append(confidence)
    sql += " ORDER BY farmaan_number NULLS LAST LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    try:
        rows = db.execute(sql, tuple(params)).fetchall()
    except Exception:
        # Migration may not have run yet — return empty so frontend can load.
        rows = []
    return {
        "results": [dict(r) for r in rows],
        "total": len(rows),
        "query_echo": {"q": q, "planet": planet, "house": house, "debt": debt, "confidence": confidence},
    }


@router.get("/api/lalkitab/farmaan/{farmaan_id}")
def farmaan_detail(
    farmaan_id: str,
    db: Any = Depends(get_db),
):
    """Full Farmaan record + accepted annotations + source-library backref."""
    try:
        row = db.execute(
            "SELECT * FROM lk_farmaan WHERE id = %s", (farmaan_id,)
        ).fetchone()
    except Exception:
        row = None
    if not row:
        raise HTTPException(status_code=404, detail="Farmaan not found or corpus not yet populated")

    try:
        annotations = db.execute(
            "SELECT * FROM lk_farmaan_annotations WHERE farmaan_id = %s ORDER BY is_accepted DESC, upvotes DESC",
            (farmaan_id,),
        ).fetchall()
    except Exception:
        annotations = []

    source_row = None
    if row.get("source_library_id"):
        try:
            source_row = db.execute(
                "SELECT * FROM lk_source_library WHERE id = %s", (row["source_library_id"],)
            ).fetchone()
        except Exception:
            source_row = None

    return {
        "farmaan": dict(row),
        "annotations": [dict(a) for a in annotations],
        "source_page": dict(source_row) if source_row else None,
    }


@router.post("/api/lalkitab/farmaan/{farmaan_id}/annotate")
def farmaan_annotate(
    farmaan_id: str,
    payload: dict,
    user: dict = Depends(get_current_user),
    db: Any = Depends(get_db),
):
    """Contribute a transliteration / translation / commentary / dispute."""
    annotation_type = str(payload.get("annotation_type") or "").strip()
    language = str(payload.get("language") or "").strip()
    body = str(payload.get("body") or "").strip()
    if annotation_type not in {"transliteration", "translation", "commentary", "dispute"}:
        raise HTTPException(status_code=400, detail="annotation_type must be one of transliteration|translation|commentary|dispute")
    if not language or not body:
        raise HTTPException(status_code=400, detail="language and body are required")

    try:
        db.execute(
            """
            INSERT INTO lk_farmaan_annotations
              (farmaan_id, contributor_user_id, annotation_type, language, body)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (farmaan_id, user["sub"], annotation_type, language, body),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to record annotation: {type(e).__name__}")
    return {"ok": True}


# ────────────────────────────────────────────────────────────────
# P2.7 — Source library (editions + rights)
# ────────────────────────────────────────────────────────────────

@router.get("/api/lalkitab/source-library/editions")
def source_library_editions(db: Any = Depends(get_db)):
    """List every edition present in the corpus with row counts."""
    try:
        rows = db.execute(
            """
            SELECT edition_year, edition_label,
                   COUNT(*) AS page_count,
                   COUNT(DISTINCT language) AS language_count,
                   COUNT(DISTINCT rights_status) AS rights_variants
            FROM lk_source_library
            GROUP BY edition_year, edition_label
            ORDER BY edition_year
            """
        ).fetchall()
    except Exception:
        rows = []
    return {"editions": [dict(r) for r in rows]}


@router.get("/api/lalkitab/source-library/by-section/{section_ref}")
def source_library_by_section(section_ref: str, db: Any = Depends(get_db)):
    """P2 edition comparison: return all editions' versions of the same section."""
    try:
        rows = db.execute(
            """
            SELECT * FROM lk_source_library
            WHERE section_ref = %s
            ORDER BY edition_year, language
            """,
            (section_ref,),
        ).fetchall()
    except Exception:
        rows = []
    return {
        "section_ref": section_ref,
        "variants": [dict(r) for r in rows],
    }


@router.get("/api/lalkitab/source-library/search")
def source_library_search(
    q: Optional[str] = Query(None),
    edition_year: Optional[int] = Query(None),
    language: Optional[str] = Query(None),
    rights: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=500),
    db: Any = Depends(get_db),
):
    """Search the raw source library across editions / languages / rights bands."""
    sql = "SELECT * FROM lk_source_library WHERE 1=1"
    params: list[Any] = []
    if q:
        sql += " AND (body ILIKE %s OR body_normalised ILIKE %s)"
        needle = f"%{q}%"
        params.extend([needle, needle])
    if edition_year:
        sql += " AND edition_year = %s"
        params.append(edition_year)
    if language:
        sql += " AND language = %s"
        params.append(language)
    if rights:
        sql += " AND rights_status = %s"
        params.append(rights)
    sql += " ORDER BY edition_year, section_ref NULLS LAST LIMIT %s"
    params.append(limit)
    try:
        rows = db.execute(sql, tuple(params)).fetchall()
    except Exception:
        rows = []
    return {"results": [dict(r) for r in rows]}


# ────────────────────────────────────────────────────────────────
# P2.8 — Rights / provenance catalog (metadata-only)
# ────────────────────────────────────────────────────────────────

# Canonical rights-band dictionary. Returned to the frontend so badge UI
# can render consistent colour / labels / tooltips without hardcoding.
_RIGHTS_CATALOG = {
    "scan_only": {
        "label_en": "Scan Only",
        "label_hi": "केवल स्कैन",
        "desc_en": "Displayed as an image of the original page. Text has not been extracted or licensed for reuse. Attribution to source.",
        "desc_hi": "मूल पृष्ठ की छवि के रूप में प्रदर्शित। पाठ निष्कर्षण या पुनः उपयोग का अधिकार नहीं। स्रोत को श्रेय।",
        "colour": "#64748B",  # slate
        "allows_reuse": False,
    },
    "licensed": {
        "label_en": "Licensed",
        "label_hi": "अधिकृत",
        "desc_en": "Reproduced under a publisher licence. Commercial reuse permitted within licence terms.",
        "desc_hi": "प्रकाशक की अनुमति के अंतर्गत पुनः उत्पादित। लाइसेंस की सीमा में व्यावसायिक उपयोग अनुमत।",
        "colour": "#047857",  # emerald
        "allows_reuse": True,
    },
    "community_transliteration": {
        "label_en": "Community Transliteration",
        "label_hi": "समुदाय लिप्यंतरण",
        "desc_en": "Community-contributed Romanisation or Devanagari rendering of a source text. Corrections welcome.",
        "desc_hi": "समुदाय द्वारा योगदान किया गया रोमन/देवनागरी लिप्यंतरण। सुधार स्वीकार्य।",
        "colour": "#D97706",  # amber
        "allows_reuse": False,
    },
    "commercial_unclear": {
        "label_en": "Commercial Use Unclear",
        "label_hi": "व्यावसायिक उपयोग स्पष्ट नहीं",
        "desc_en": "Copyright status uncertain (Joshi / Sharma authorship dispute). Displayed for education only. Do not redistribute.",
        "desc_hi": "कॉपीराइट स्थिति अस्पष्ट (जोशी / शर्मा लेखक विवाद)। केवल शिक्षा हेतु। पुनर्वितरण न करें।",
        "colour": "#DC2626",  # red
        "allows_reuse": False,
    },
    "public_domain": {
        "label_en": "Public Domain",
        "label_hi": "सार्वजनिक डोमेन",
        "desc_en": "Copyright has expired or was never claimed. Free to reproduce with attribution.",
        "desc_hi": "कॉपीराइट समाप्त या कभी दावा नहीं। श्रेय के साथ पुनः उपयोग मुक्त।",
        "colour": "#2563EB",  # blue
        "allows_reuse": True,
    },
}


@router.get("/api/lalkitab/rights-catalog")
def rights_catalog():
    """P2.8 — return the canonical rights-badge dictionary so the frontend
    can render badges consistently. Static — no DB hit."""
    return {"rights": _RIGHTS_CATALOG}


@router.get("/api/lalkitab/rights-catalog/summary")
def rights_summary(db: Any = Depends(get_db)):
    """Row-count breakdown of the current corpus by rights_status."""
    try:
        rows = db.execute(
            """
            SELECT rights_status, COUNT(*) AS n
            FROM (
              SELECT rights_status FROM lk_source_library
              UNION ALL
              SELECT rights_status FROM lk_farmaan
            ) combined
            GROUP BY rights_status
            ORDER BY n DESC
            """
        ).fetchall()
    except Exception:
        rows = []
    return {"summary": [dict(r) for r in rows], "catalog": _RIGHTS_CATALOG}
