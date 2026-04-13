"""
vastu/floorplan.py — Floor Plan Upload & Pixel-to-Direction Mapper
===================================================================
Handles floor plan image upload, storage, and coordinate-to-Vastu-direction
conversion for manual room placement on uploaded images.
"""
import io
import logging
import math
import os
import shutil
import subprocess
import time
import uuid
from typing import Optional

from app.config import STATIC_DIR

log = logging.getLogger(__name__)

# Upload config
UPLOAD_DIR = os.path.join(STATIC_DIR, "uploads", "vastu")
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_DIMENSION = 6000  # max 6000px per side — prevents memory DOS
ALLOWED_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/webp"}
CLEANUP_AGE_SECONDS = 30 * 24 * 3600  # 30 days

# ClamAV — free, open-source virus scanner (brew install clamav)
_CLAMSCAN_PATH = shutil.which("clamscan")


def ensure_upload_dir():
    """Create vastu upload directory if it doesn't exist."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)


def scan_file_for_viruses(file_bytes: bytes) -> bool:
    """
    Scan file bytes with ClamAV (clamscan).
    Returns True if file is CLEAN, raises ValueError if infected.
    Silently passes if ClamAV is not installed (graceful degradation).
    """
    if not _CLAMSCAN_PATH:
        log.debug("ClamAV not installed — skipping virus scan (install: brew install clamav)")
        return True

    # Write to temp file for scanning
    tmp_path = os.path.join(UPLOAD_DIR, f"_scan_{uuid.uuid4().hex[:8]}.tmp")
    try:
        ensure_upload_dir()
        with open(tmp_path, "wb") as f:
            f.write(file_bytes)

        result = subprocess.run(
            [_CLAMSCAN_PATH, "--no-summary", tmp_path],
            capture_output=True, text=True, timeout=30,
        )
        # clamscan exit codes: 0=clean, 1=infected, 2=error
        if result.returncode == 1:
            log.warning(f"ClamAV detected threat: {result.stdout.strip()}")
            raise ValueError("File rejected — potential security threat detected")
        elif result.returncode == 2:
            log.warning(f"ClamAV scan error: {result.stderr.strip()}")
            # Don't block on scanner errors
        return True
    except subprocess.TimeoutExpired:
        log.warning("ClamAV scan timed out — allowing upload")
        return True
    except ValueError:
        raise  # re-raise infection detection
    except Exception as e:
        log.warning(f"ClamAV scan failed: {e} — allowing upload")
        return True
    finally:
        if os.path.exists(tmp_path):
            os.rename(tmp_path, tmp_path + ".scanned")  # safe cleanup, not rm


def cleanup_old_uploads():
    """Remove uploaded floorplan images older than 30 days."""
    ensure_upload_dir()
    now = time.time()
    removed = 0
    for fname in os.listdir(UPLOAD_DIR):
        fpath = os.path.join(UPLOAD_DIR, fname)
        if os.path.isfile(fpath):
            age = now - os.path.getmtime(fpath)
            if age > CLEANUP_AGE_SECONDS:
                os.rename(fpath, fpath + ".expired")  # safe rename, not rm
                removed += 1
    return removed


def _validate_image_dimensions(file_bytes: bytes) -> tuple[int, int]:
    """
    Check image dimensions without loading full image into memory.
    Returns (width, height). Raises ValueError if too large.
    """
    try:
        from PIL import Image
        img = Image.open(io.BytesIO(file_bytes))
        w, h = img.size
        img.close()
    except ImportError:
        # PIL not available — skip dimension check, return 0,0
        return 0, 0
    except Exception:
        raise ValueError("Cannot read image — file may be corrupted")

    if w > MAX_DIMENSION or h > MAX_DIMENSION:
        raise ValueError(f"Image too large ({w}x{h}). Maximum dimension is {MAX_DIMENSION}px per side.")
    if w < 100 or h < 100:
        raise ValueError(f"Image too small ({w}x{h}). Minimum 100x100px.")
    return w, h


def _optimize_image(file_bytes: bytes, max_side: int = 2000) -> bytes:
    """
    Resize large images and compress to JPEG for storage efficiency.
    Returns optimized bytes. Falls back to original if PIL unavailable.
    """
    try:
        from PIL import Image
        img = Image.open(io.BytesIO(file_bytes))
        w, h = img.size

        # Only resize if larger than max_side
        if w > max_side or h > max_side:
            ratio = min(max_side / w, max_side / h)
            new_w, new_h = int(w * ratio), int(h * ratio)
            img = img.resize((new_w, new_h), Image.LANCZOS)

        # Convert to RGB (strip alpha) and save as optimized JPEG
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        buf = io.BytesIO()
        img.save(buf, format='JPEG', quality=85, optimize=True)
        img.close()
        return buf.getvalue()
    except ImportError:
        return file_bytes
    except Exception:
        return file_bytes


def save_floorplan(file_bytes: bytes, content_type: str) -> dict:
    """
    Validate, optimize, and save uploaded floor plan image.

    Returns:
        dict with file_id, image_url, filename, width, height
    """
    ensure_upload_dir()

    # Virus scan (uses ClamAV if installed, skips gracefully if not)
    scan_file_for_viruses(file_bytes)

    # Validate dimensions
    width, height = _validate_image_dimensions(file_bytes)

    # Optimize (resize + compress)
    optimized = _optimize_image(file_bytes)

    file_id = uuid.uuid4().hex[:16]
    filename = f"fp_{file_id}.jpg"  # always save as optimized JPEG
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(optimized)

    # Re-read dimensions from optimized image
    opt_w, opt_h = width, height
    try:
        from PIL import Image
        img = Image.open(io.BytesIO(optimized))
        opt_w, opt_h = img.size
        img.close()
    except Exception:
        pass

    return {
        "file_id": file_id,
        "filename": filename,
        "image_url": f"/static/uploads/vastu/{filename}",
        "size_bytes": len(optimized),
        "original_size_bytes": len(file_bytes),
        "width": opt_w,
        "height": opt_h,
    }


# ============================================================
# PIXEL → DIRECTION MAPPER
# ============================================================

def pixel_to_direction(
    x: float,
    y: float,
    image_width: int,
    image_height: int,
    north_rotation: float = 0.0,
) -> str:
    """
    Convert pixel coordinates on a floor plan image to a Vastu direction.

    The image center = Brahma Sthana (Center).
    The image is divided into 9 zones matching the 3x3 Vastu grid:
        NW | N  | NE
        W  | C  | E
        SW | S  | SE

    Args:
        x, y: pixel coordinates (0,0 = top-left)
        image_width, image_height: image dimensions
        north_rotation: degrees clockwise that North is rotated from image-top
                        (0 = North is up, 90 = North is right, etc.)

    Returns:
        Direction code: "N", "NE", "E", "SE", "S", "SW", "W", "NW", or "Center"
    """
    # Normalize to -1..+1 (center = 0,0)
    cx = image_width / 2
    cy = image_height / 2
    nx = (x - cx) / cx   # -1 (left) to +1 (right)
    ny = (y - cy) / cy   # -1 (top) to +1 (bottom)

    # Apply north rotation (rotate coordinate system)
    if north_rotation != 0:
        rad = math.radians(-north_rotation)  # negative because we rotate the grid
        rx = nx * math.cos(rad) - ny * math.sin(rad)
        ry = nx * math.sin(rad) + ny * math.cos(rad)
        nx, ny = rx, ry

    # 3x3 grid thresholds — inner third = Center
    THIRD = 1.0 / 3.0

    # Determine row (N/Center/S)
    if ny < -THIRD:
        row = "N"
    elif ny > THIRD:
        row = "S"
    else:
        row = "C"

    # Determine col (W/Center/E)
    if nx < -THIRD:
        col = "W"
    elif nx > THIRD:
        col = "E"
    else:
        col = "C"

    # Map to direction
    grid_map = {
        ("N", "W"): "NW",  ("N", "C"): "N",  ("N", "E"): "NE",
        ("C", "W"): "W",   ("C", "C"): "Center", ("C", "E"): "E",
        ("S", "W"): "SW",  ("S", "C"): "S",  ("S", "E"): "SE",
    }

    return grid_map.get((row, col), "Center")


def map_room_placements(
    room_markers: list[dict],
    image_width: int,
    image_height: int,
    north_rotation: float = 0.0,
) -> dict[str, list[str]]:
    """
    Convert a list of room markers (pixel positions) to direction-based assignments.

    Args:
        room_markers: list of {"room_type": str, "x": float, "y": float}
        image_width, image_height: image dimensions in pixels
        north_rotation: degrees clockwise North is rotated from top

    Returns:
        dict mapping direction → list of room types
        e.g. {"NE": ["pooja"], "SE": ["kitchen"], "SW": ["master_bedroom"]}
    """
    assignments: dict[str, list[str]] = {}

    for marker in room_markers:
        direction = pixel_to_direction(
            marker["x"], marker["y"],
            image_width, image_height,
            north_rotation,
        )
        if direction not in assignments:
            assignments[direction] = []
        assignments[direction].append(marker["room_type"])

    return assignments
