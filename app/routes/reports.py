"""Paid report request and retrieval routes.

C-05: PDF generation via fpdf2 with paywall enforcement.
"""
import json
import os
import sqlite3
import uuid
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from app.auth import get_current_user
from app.database import get_db
from app.email_service import send_report_ready
from app.models import ReportRequest
from app.config import DB_PATH as _DEFAULT_DB_PATH

router = APIRouter()

# Prices for each report type (in INR)
REPORT_PRICES = {
    "full_kundli": 999.0,
    "marriage": 799.0,
    "career": 799.0,
    "health": 699.0,
    "yearly": 599.0,
}

# Static reports directory
_REPORTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static", "reports"
)
os.makedirs(_REPORTS_DIR, exist_ok=True)


def generate_kundli_pdf(kundli_data: dict, person_name: str, report_type: str) -> str:
    """Generate a PDF report for a kundli and return the filename.

    Uses fpdf2 (lightweight). Returns the filename (not the full path).
    If fpdf2 is not installed, returns None so the caller can handle gracefully.
    """
    try:
        from fpdf import FPDF
    except ImportError:
        return None

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # --- Title Page ---
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 24)
    pdf.cell(0, 20, "AstroVedic Report", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(10)

    pdf.set_font("Helvetica", "", 14)
    pdf.cell(0, 10, f"Report Type: {report_type.replace('_', ' ').title()}", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"Name: {person_name}", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)

    # Birth details from kundli_data
    birth_date = kundli_data.get("birth_date", "N/A")
    birth_time = kundli_data.get("birth_time", "N/A")
    birth_place = kundli_data.get("birth_place", "N/A")

    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, f"Date of Birth: {birth_date}", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(0, 8, f"Time of Birth: {birth_time}", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(0, 8, f"Place of Birth: {birth_place}", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(15)

    # --- Planet Positions Table ---
    chart_data = kundli_data.get("chart_data", {})
    if isinstance(chart_data, str):
        try:
            chart_data = json.loads(chart_data)
        except (json.JSONDecodeError, TypeError):
            chart_data = {}

    planets = chart_data.get("planets", {})
    if planets:
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "Planet Positions", new_x="LMARGIN", new_y="NEXT", align="L")
        pdf.ln(3)

        # Table header
        pdf.set_font("Helvetica", "B", 10)
        col_w = 47
        pdf.cell(col_w, 8, "Planet", border=1, align="C")
        pdf.cell(col_w, 8, "Sign", border=1, align="C")
        pdf.cell(col_w, 8, "Degree", border=1, align="C")
        pdf.cell(col_w, 8, "House", border=1, align="C")
        pdf.ln()

        # Table rows
        pdf.set_font("Helvetica", "", 10)
        for planet_name, planet_info in planets.items():
            if isinstance(planet_info, dict):
                sign = planet_info.get("sign", "N/A")
                degree = str(planet_info.get("degree", "N/A"))
                house = str(planet_info.get("house", "N/A"))
            else:
                sign = str(planet_info)
                degree = "N/A"
                house = "N/A"
            pdf.cell(col_w, 7, planet_name.title(), border=1, align="C")
            pdf.cell(col_w, 7, str(sign).title(), border=1, align="C")
            pdf.cell(col_w, 7, degree, border=1, align="C")
            pdf.cell(col_w, 7, house, border=1, align="C")
            pdf.ln()
        pdf.ln(10)

    # --- Dasha Periods ---
    dashas = chart_data.get("dashas", chart_data.get("dasha", []))
    if dashas:
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "Dasha Periods", new_x="LMARGIN", new_y="NEXT", align="L")
        pdf.ln(3)
        pdf.set_font("Helvetica", "", 10)

        if isinstance(dashas, list):
            for dasha in dashas[:10]:  # Limit to first 10
                if isinstance(dasha, dict):
                    label = dasha.get("planet", dasha.get("name", "N/A"))
                    start = dasha.get("start", "N/A")
                    end = dasha.get("end", "N/A")
                    pdf.cell(0, 7, f"{label}: {start} to {end}", new_x="LMARGIN", new_y="NEXT")
                else:
                    pdf.cell(0, 7, str(dasha), new_x="LMARGIN", new_y="NEXT")
        elif isinstance(dashas, dict):
            for key, val in list(dashas.items())[:10]:
                pdf.cell(0, 7, f"{key}: {val}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(10)

    # --- io-gita Basin Analysis (if available) ---
    iogita = kundli_data.get("iogita_analysis", None)
    if iogita:
        if isinstance(iogita, str):
            try:
                iogita = json.loads(iogita)
            except (json.JSONDecodeError, TypeError):
                iogita = {"analysis": iogita}
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "io-gita Basin Analysis", new_x="LMARGIN", new_y="NEXT", align="L")
        pdf.ln(3)
        pdf.set_font("Helvetica", "", 10)
        if isinstance(iogita, dict):
            for key, val in iogita.items():
                text = f"{key}: {val}"
                pdf.multi_cell(0, 7, text)
        else:
            pdf.multi_cell(0, 7, str(iogita))
        pdf.ln(10)

    # --- Footer ---
    pdf.set_font("Helvetica", "I", 8)
    pdf.cell(0, 10, "Generated by AstroVedic - For personal use only", new_x="LMARGIN", new_y="NEXT", align="C")

    # Save
    report_id = uuid.uuid4().hex[:16]
    filename = f"{report_id}.pdf"
    filepath = os.path.join(_REPORTS_DIR, filename)
    pdf.output(filepath)
    return filename


@router.get("/api/reports", status_code=status.HTTP_200_OK)
def list_my_reports(
    user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """List all reports for the current user."""
    user_id = user.get("sub")
    rows = db.execute(
        "SELECT r.id, r.kundli_id, r.report_type, r.status, r.price, r.created_at, k.person_name as kundli_name "
        "FROM reports r LEFT JOIN kundlis k ON k.id = r.kundli_id WHERE r.user_id = ? ORDER BY r.created_at DESC",
        (user_id,),
    ).fetchall()
    reports = []
    for r in rows:
        report = dict(r)
        # Map to frontend expected fields
        report['type'] = report['report_type']
        report['title'] = f"{report['report_type'].replace('_', ' ').title()} Report"
        if report.get('kundli_name'):
            report['title'] += f" - {report['kundli_name']}"
        reports.append(report)
    return {"reports": reports}


def _background_generate_pdf(report_id: str, kundli_id: str, report_type: str, db_path: str):
    """H-05: Background task — generate PDF and update report status to 'ready'."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        kundli = conn.execute("SELECT * FROM kundlis WHERE id = ?", (kundli_id,)).fetchone()
        if kundli is None:
            conn.execute("UPDATE reports SET status = 'failed' WHERE id = ?", (report_id,))
            conn.commit()
            return

        kundli_data = dict(kundli)
        pdf_filename = generate_kundli_pdf(kundli_data, kundli["person_name"], report_type)

        if pdf_filename:
            pdf_url = f"/static/reports/{pdf_filename}"
            conn.execute(
                "UPDATE reports SET status = 'ready', pdf_url = ? WHERE id = ?",
                (pdf_url, report_id),
            )
            report_row = conn.execute(
                """SELECT r.*, u.email as user_email
                   FROM reports r
                   JOIN users u ON u.id = r.user_id
                   WHERE r.id = ?""",
                (report_id,),
            ).fetchone()
            if report_row and report_row["user_email"]:
                send_report_ready(dict(report_row), report_row["user_email"])
        else:
            # fpdf2 not installed — mark as failed
            conn.execute("UPDATE reports SET status = 'failed' WHERE id = ?", (report_id,))
        conn.commit()
    except Exception:
        conn.execute("UPDATE reports SET status = 'failed' WHERE id = ?", (report_id,))
        conn.commit()
    finally:
        conn.close()


@router.post("/api/reports/request", status_code=status.HTTP_201_CREATED)
def request_report(
    req: ReportRequest,
    background_tasks: BackgroundTasks,
    user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Request a paid astrology report. Requires JWT.

    H-05: Uses BackgroundTasks to generate PDF asynchronously.
    Returns immediately with status='generating'.
    C-05: If payment already completed, triggers background generation.
    """
    user_id = user.get("sub")

    # Verify kundli exists and belongs to user
    kundli = db.execute(
        "SELECT * FROM kundlis WHERE id = ? AND user_id = ?",
        (req.kundli_id, user_id),
    ).fetchone()

    if kundli is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Kundli not found"
        )

    price = REPORT_PRICES.get(req.report_type.value, 999.0)

    cursor = db.execute(
        """
        INSERT INTO reports (user_id, kundli_id, report_type, status, price)
        VALUES (?, ?, ?, 'pending', ?)
        """,
        (user_id, req.kundli_id, req.report_type.value, price),
    )
    rowid = cursor.lastrowid
    report = db.execute(
        "SELECT id, status, price, created_at FROM reports WHERE rowid = ?", (rowid,)
    ).fetchone()
    db.commit()

    report_id = report["id"]

    # Return immediately with status='pending' - PDF will be generated after payment
    full_report = db.execute(
        "SELECT * FROM reports WHERE id = ?", (report_id,)
    ).fetchone()
    return {
        "report": dict(full_report),
        "payment_required": True,
    }


@router.get("/api/reports/{report_id}")
def get_report(
    report_id: str,
    user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Get a report by ID. Must belong to current user.

    C-05 Paywall: Only returns content/pdf_url if report status is 'ready'.
    If status is 'pending' or 'paid' (but not yet generated), content is
    withheld and a payment_required flag is returned instead.
    """
    user_id = user.get("sub")

    report = db.execute(
        "SELECT * FROM reports WHERE id = ? AND user_id = ?",
        (report_id, user_id),
    ).fetchone()

    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Report not found"
        )

    result = dict(report)

    # Paywall: hide content and pdf_url unless report is ready
    if result.get("status") != "ready":
        result.pop("content", None)
        result.pop("pdf_url", None)
        result["payment_required"] = True
    else:
        result["payment_required"] = False

    return result


@router.post("/api/reports/{report_id}/generate")
def generate_report_pdf(
    report_id: str,
    user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db),
):
    """Trigger PDF generation for a paid report.

    C-05: Only generates if the report has been paid for.
    """
    user_id = user.get("sub")

    report = db.execute(
        "SELECT * FROM reports WHERE id = ? AND user_id = ?",
        (report_id, user_id),
    ).fetchone()

    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Report not found"
        )

    if report["status"] == "ready":
        return {"status": "already_generated", "pdf_url": report["pdf_url"]}

    # Check payment -- must be paid or have a completed payment
    payment = db.execute(
        "SELECT id FROM payments WHERE report_id = ? AND status = 'completed'",
        (report_id,),
    ).fetchone()

    if payment is None and report["status"] == "pending":
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Payment required before PDF generation",
        )

    # Fetch kundli data for generation
    kundli = db.execute(
        "SELECT * FROM kundlis WHERE id = ?", (report["kundli_id"],)
    ).fetchone()

    if kundli is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Kundli data not found"
        )

    kundli_data = dict(kundli)
    pdf_filename = generate_kundli_pdf(
        kundli_data, kundli["person_name"], report["report_type"]
    )

    if pdf_filename is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="PDF generation failed — fpdf2 not installed",
        )

    pdf_url = f"/static/reports/{pdf_filename}"
    db.execute(
        "UPDATE reports SET status = 'ready', pdf_url = ? WHERE id = ?",
        (pdf_url, report_id),
    )
    db.commit()

    return {"status": "ready", "pdf_url": pdf_url}
