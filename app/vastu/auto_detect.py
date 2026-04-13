"""
vastu/auto_detect.py — AI Room Detection for Floor Plans
==========================================================
Hybrid detection: OCR (pytesseract) → YOLOv8 → OpenCV contours.
Each detector degrades gracefully if its dependency is missing.
"""
import io
import logging
from difflib import SequenceMatcher

log = logging.getLogger(__name__)

# Pre-check: YOLOv8 model
_YOLO_MODEL_PATH = "yolov8n.pt"
_YOLO_AVAILABLE = False
try:
    import os as _os
    if _os.path.isfile(_YOLO_MODEL_PATH):
        _YOLO_AVAILABLE = True
    else:
        try:
            from ultralytics import YOLO
            YOLO(_YOLO_MODEL_PATH)
            _YOLO_AVAILABLE = True
        except Exception:
            pass
except Exception:
    pass

# Valid Vastu room types (must match data.py ROOM_PLACEMENT keys)
VALID_ROOM_TYPES = {
    "pooja", "kitchen", "master_bedroom", "living_room", "bathroom",
    "staircase", "water_tank_underground", "water_tank_overhead",
    "study_room", "children_bedroom",
}

# YOLO/CubiCasa object → Vastu room type
_VASTU_ROOM_MAP = {
    "livingroom": "living_room", "living room": "living_room", "living": "living_room",
    "kitchen": "kitchen", "cooking": "kitchen",
    "bedroom": "master_bedroom", "master bedroom": "master_bedroom",
    "bathroom": "bathroom", "toilet": "bathroom", "washroom": "bathroom",
    "balcony": "living_room",
    "corridor": None,
    "dining": "kitchen",
    "study": "study_room", "office": "study_room",
    "children": "children_bedroom", "kid": "children_bedroom",
    "pooja": "pooja", "prayer": "pooja", "puja": "pooja",
    "staircase": "staircase", "stairs": "staircase",
    "bed": "master_bedroom",
    "chair": "living_room", "couch": "living_room", "sofa": "living_room",
    "dining table": "kitchen",
    "refrigerator": "kitchen", "oven": "kitchen", "microwave": "kitchen",
    "tv": "living_room",
    "sink": "bathroom",
    "vase": "pooja",
    "book": "study_room",
}

# OCR keyword → room type.
# RULES: no single generic words like "room", "hall", "home" — they cause false positives.
# Order matters: longer/more-specific phrases are checked first.
_OCR_KEYWORDS: list[tuple[str, str]] = [
    # ── Multi-word phrases (checked first, most specific) ──────────────
    ("master bedroom",      "master_bedroom"),
    ("master bed room",     "master_bedroom"),
    ("bed room 1",          "master_bedroom"),
    ("bedroom 1",           "master_bedroom"),
    ("children bedroom",    "children_bedroom"),
    ("children room",       "children_bedroom"),
    ("child bedroom",       "children_bedroom"),
    ("kids room",           "children_bedroom"),
    ("kid room",            "children_bedroom"),
    ("living room",         "living_room"),
    ("drawing room",        "living_room"),
    ("sitting room",        "living_room"),
    ("family room",         "living_room"),
    ("pooja room",          "pooja"),
    ("prayer room",         "pooja"),
    ("puja room",           "pooja"),
    ("study room",          "study_room"),
    ("work room",           "study_room"),
    ("water tank",          "water_tank_underground"),
    ("overhead tank",       "water_tank_overhead"),
    ("ug tank",             "water_tank_underground"),
    ("oh tank",             "water_tank_overhead"),
    # ── Single-word (checked after phrases) ───────────────────────────
    ("kitchen",             "kitchen"),
    ("rasoi",               "kitchen"),
    ("cooking",             "kitchen"),
    ("bedroom 2",           "children_bedroom"),  # second bedroom → children's
    ("bedroom 3",           "children_bedroom"),
    ("bed room 2",          "children_bedroom"),
    ("bedroom",             "master_bedroom"),   # generic bedroom → master
    ("bed",                 "master_bedroom"),
    ("children",            "children_bedroom"),
    ("child",               "children_bedroom"),
    ("kids",                "children_bedroom"),
    ("bathroom",            "bathroom"),
    ("toilet",              "bathroom"),
    ("washroom",            "bathroom"),
    ("bath",                "bathroom"),
    ("shower",              "bathroom"),
    ("wc",                  "bathroom"),
    ("living",              "living_room"),
    ("drawing",             "living_room"),
    ("baithak",             "living_room"),
    ("lounge",              "living_room"),
    ("pooja",               "pooja"),
    ("puja",                "pooja"),
    ("mandir",              "pooja"),
    ("temple",              "pooja"),
    ("study",               "study_room"),
    ("office",              "study_room"),
    ("library",             "study_room"),
    ("dining room",         "kitchen"),
    ("dining",              "kitchen"),
    ("dine",                "kitchen"),
    ("stair",               "staircase"),
    # OCR typo variants for "living"
    ("livine",              "living_room"),
    ("livin",               "living_room"),
    ("lving",               "living_room"),
    # Hindi
    ("shayanakaksh",        "master_bedroom"),
    ("shayan",              "master_bedroom"),
]

# Words that are definitely NOT room labels
_SKIP_WORDS = {
    "sample", "floorplan", "floor plan", "for vastu", "analysis", "test",
    "checklist", "click", "detect", "button", "should", "verify",
    "detection", "upload", "image", "entrance", "scale", "feet", "meter",
    "north", "south", "east", "west", "area", "sq", "ft", "door",
    "window", "wall", "column", "dimension", "total", "plan", "drawing",
    "neighbour", "neighbor", "road", "street", "plot", "compound",
}


def _preprocess_for_ocr(image_bytes: bytes):
    """
    Preprocess floor plan for OCR: grayscale → upscale 2x → sharpen → binarize.
    Returns (pil_image, scale_factor). Falls back to raw PIL image on failure.
    """
    try:
        import cv2
        import numpy as np
        from PIL import Image

        nparr = np.frombuffer(image_bytes, np.uint8)
        img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img_cv is None:
            raise ValueError("cv2 decode failed")

        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        # Upscale 2x — biggest single improvement for OCR on floor plans
        large = cv2.resize(gray, (w * 2, h * 2), interpolation=cv2.INTER_CUBIC)

        # Light denoising
        denoised = cv2.fastNlMeansDenoising(large, h=8)

        # Sharpen to make text edges crisp
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        sharp = cv2.filter2D(denoised, -1, kernel)
        sharp = np.clip(sharp, 0, 255).astype(np.uint8)

        # Otsu binarization: auto-finds the best threshold
        _, binary = cv2.threshold(sharp, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        return Image.fromarray(binary), 2.0

    except Exception as e:
        log.debug(f"Preprocessing fallback (raw PIL): {e}")
        from PIL import Image
        return Image.open(io.BytesIO(image_bytes)), 1.0


def _match_room(text: str) -> str | None:
    """
    Match a text string against OCR keywords.
    Checks multi-word phrases first (more specific), then single words.
    Returns room_type string or None.
    """
    t = text.lower().strip()

    # Skip non-room words
    if any(sw in t for sw in _SKIP_WORDS):
        return None

    # Exact / substring match against keyword list (ordered, phrases first)
    for phrase, room_type in _OCR_KEYWORDS:
        if phrase in t:
            return room_type

    # Fuzzy fallback: catch OCR typos (min similarity 0.75)
    for phrase, room_type in _OCR_KEYWORDS:
        if len(phrase) >= 5:  # only fuzzy-match longer keywords
            ratio = SequenceMatcher(None, phrase, t[:len(phrase) + 3]).ratio()
            if ratio >= 0.75:
                return room_type

    return None


# ============================================================
# DETECTOR 1: OCR text labels
# ============================================================
def _detect_ocr_labels(image_bytes: bytes) -> list[dict]:
    """
    Read room name labels from floor plan using pytesseract.
    Uses PSM 11 (sparse text) — best mode for floor plans.
    Also tries PSM 6 and merges unique results.
    """
    try:
        import pytesseract
    except ImportError:
        log.debug("pytesseract not installed — skipping OCR")
        return []

    preprocessed, scale = _preprocess_for_ocr(image_bytes)
    raw_w, raw_h = preprocessed.width, preprocessed.height

    # Run two PSM modes; PSM 11 is designed for sparse/scattered text (floor plans)
    all_data: list[dict] = []
    for psm in (11, 6):
        try:
            config = f"--oem 3 --psm {psm}"
            data = pytesseract.image_to_data(preprocessed, output_type=pytesseract.Output.DICT, config=config)
            all_data.append(data)
        except Exception as e:
            log.debug(f"OCR PSM {psm} failed: {e}")

    if not all_data:
        return []

    # Merge word boxes from all PSM runs; deduplicate by position
    text_boxes: list[dict] = []
    seen_positions: set[tuple] = set()

    for data in all_data:
        n = len(data["text"])
        for i in range(n):
            word = data["text"][i].strip()
            conf = int(data["conf"][i]) if str(data["conf"][i]) != '-1' else 0

            if conf < 30 or len(word) < 2:
                continue

            # Snap to 20px grid to deduplicate same word from different PSM runs
            x_center = data["left"][i] + data["width"][i] // 2
            y_center = data["top"][i] + data["height"][i] // 2
            snap = (round(x_center / 20) * 20, round(y_center / 20) * 20)
            if snap in seen_positions:
                continue
            seen_positions.add(snap)

            # Margin filter: skip obvious header/footer areas
            if raw_h > 0 and (y_center < raw_h * 0.04 or y_center > raw_h * 0.96):
                continue
            if raw_w > 0 and x_center > raw_w * 0.92:
                continue

            text_boxes.append({
                "word": word,
                "conf": conf,
                "x": x_center,
                "y": y_center,
                "left": data["left"][i],
                "top": data["top"][i],
                "w": data["width"][i],
                "h": data["height"][i],
            })

    # Combine nearby words into phrases (within 120px horizontal, 25px vertical)
    used: set[int] = set()
    phrases: list[dict] = []

    for i, box in enumerate(text_boxes):
        if i in used:
            continue
        group = [box]
        for j, other in enumerate(text_boxes):
            if i == j or j in used:
                continue
            if abs(box["y"] - other["y"]) < 25 and abs(box["x"] - other["x"]) < 120:
                group.append(other)
                used.add(j)
        used.add(i)

        group.sort(key=lambda b: b["x"])
        phrase_text = " ".join(b["word"] for b in group)
        center_x = sum(b["x"] for b in group) // len(group)
        center_y = sum(b["y"] for b in group) // len(group)
        avg_conf = sum(b["conf"] for b in group) / len(group)

        # Scale coordinates back to original image space
        orig_x = round(center_x / scale)
        orig_y = round(center_y / scale)

        phrases.append({
            "text": phrase_text,
            "conf": avg_conf,
            "x": orig_x,
            "y": orig_y,
        })

    # Match phrases → room types
    rooms: list[dict] = []
    for p in phrases:
        room_type = _match_room(p["text"])
        if room_type and room_type in VALID_ROOM_TYPES:
            rooms.append({
                "room_type": room_type,
                "x": p["x"],
                "y": p["y"],
                "confidence": round(p["conf"] / 100, 2),
                "method": "ocr",
                "detected_text": p["text"],
            })

    # Deduplicate: same room_type within 100px → keep highest confidence
    rooms.sort(key=lambda r: r["confidence"], reverse=True)
    deduped: list[dict] = []
    for room in rooms:
        too_close = False
        for kept in deduped:
            if kept["room_type"] == room["room_type"]:
                dx = abs(room["x"] - kept["x"])
                dy = abs(room["y"] - kept["y"])
                if dx < 100 and dy < 100:
                    too_close = True
                    break
        if not too_close:
            deduped.append(room)

    # Cap per room type: most floor plans have max 2 of each type
    type_counts: dict[str, int] = {}
    capped: list[dict] = []
    max_per_type = {"bathroom": 3, "children_bedroom": 3, "master_bedroom": 2}
    for room in deduped:
        rt = room["room_type"]
        limit = max_per_type.get(rt, 1)
        if type_counts.get(rt, 0) < limit:
            capped.append(room)
            type_counts[rt] = type_counts.get(rt, 0) + 1

    log.info(f"OCR: {len(text_boxes)} words → {len(phrases)} phrases → {len(capped)} rooms")
    return capped


# ============================================================
# DETECTOR 2: YOLOv8
# ============================================================
def _detect_yolo(image_bytes: bytes) -> list[dict]:
    """Detect room-associated objects using YOLOv8."""
    try:
        from ultralytics import YOLO
        from PIL import Image
    except ImportError:
        return []

    try:
        model = YOLO("yolov8n.pt")
    except Exception as e:
        log.warning(f"Failed to load YOLO model: {e}")
        return []

    img = Image.open(io.BytesIO(image_bytes))
    results = model(img, verbose=False)

    rooms = []
    seen_types: set[str] = set()

    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls)
            cls_name = result.names.get(cls_id, "")
            conf = float(box.conf)
            if conf < 0.4:
                continue
            room_type = _VASTU_ROOM_MAP.get(cls_name.lower())
            if not room_type or room_type not in VALID_ROOM_TYPES:
                continue
            if room_type in seen_types:
                continue
            seen_types.add(room_type)
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            rooms.append({
                "room_type": room_type,
                "x": int((x1 + x2) / 2),
                "y": int((y1 + y2) / 2),
                "confidence": round(conf, 2),
                "method": "yolo",
                "detected_object": cls_name,
            })

    return rooms


# ============================================================
# DETECTOR 3: OpenCV contours
# ============================================================
def _detect_opencv(image_bytes: bytes) -> list[dict]:
    """
    Detect rooms from closed contours (line-art floor plan drawings).
    Classifies by room size and aspect ratio.
    """
    try:
        import cv2
        import numpy as np
    except ImportError:
        return []

    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        return []

    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 51, 10)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=3)
    contours, _ = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    rooms = []
    min_area = (w * h) * 0.005
    max_area = (w * h) * 0.5

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < min_area or area > max_area:
            continue
        x, y, cw, ch = cv2.boundingRect(contour)
        aspect = cw / ch if ch > 0 else 1
        if aspect > 5 or aspect < 0.2:
            continue

        rel_area = area / (w * h)
        if rel_area > 0.1:
            room_type = "living_room" if aspect > 1.3 else "master_bedroom"
        elif rel_area > 0.05:
            room_type = "children_bedroom" if aspect < 1.2 else "kitchen"
        elif rel_area > 0.02:
            room_type = "kitchen" if 0.7 < aspect < 1.5 else "bathroom"
        else:
            room_type = "bathroom"

        rooms.append({
            "room_type": room_type,
            "x": x + cw // 2,
            "y": y + ch // 2,
            "confidence": round(min(area / (w * h * 0.1), 0.85), 2),
            "method": "opencv",
        })

    # Deduplicate overlapping detections
    rooms.sort(key=lambda r: r["confidence"], reverse=True)
    filtered: list[dict] = []
    for room in rooms:
        if not any(abs(room["x"] - k["x"]) < 50 and abs(room["y"] - k["y"]) < 50 for k in filtered):
            filtered.append(room)

    return filtered[:12]


# ============================================================
# MAIN: Hybrid auto-detection
# ============================================================
def auto_detect_rooms(image_bytes: bytes, image_width: int, image_height: int) -> dict:
    """
    Detect rooms using OCR → YOLOv8 → OpenCV, merge and deduplicate results.
    """
    all_markers: list[dict] = []
    methods_tried: list[str] = []
    primary_method = "manual"

    # Method 1: OCR (most accurate when labels are present)
    ocr_results = _detect_ocr_labels(image_bytes)
    if ocr_results:
        methods_tried.append("ocr")
        all_markers.extend(ocr_results)
        primary_method = "ocr"
        log.info(f"OCR: {len(ocr_results)} rooms")

    # Method 2: YOLOv8
    yolo_results = _detect_yolo(image_bytes)
    if yolo_results:
        methods_tried.append("yolo")
        all_markers.extend(yolo_results)
        if primary_method == "manual":
            primary_method = "yolo"
        log.info(f"YOLO: {len(yolo_results)} rooms")

    # Method 3: OpenCV contours — only if both above found fewer than 3 rooms
    if len(all_markers) < 3:
        cv_results = _detect_opencv(image_bytes)
        if cv_results:
            methods_tried.append("opencv")
            all_markers.extend(cv_results)
            if primary_method == "manual":
                primary_method = "opencv"
            log.info(f"OpenCV: {len(cv_results)} rooms")

    if not methods_tried:
        methods_tried.append("none")

    # Global dedup: same room_type within 80px → keep higher confidence
    deduped: list[dict] = []
    all_markers.sort(key=lambda m: m.get("confidence", 0), reverse=True)
    for marker in all_markers:
        too_close = any(
            abs(marker["x"] - k["x"]) < 80
            and abs(marker["y"] - k["y"]) < 80
            and marker["room_type"] == k["room_type"]
            for k in deduped
        )
        if not too_close:
            deduped.append(marker)

    # Clamp coordinates to image bounds (avoid markers in black border area)
    margin = 0.05  # 5% inset from each edge
    x_min = int(image_width * margin)
    x_max = int(image_width * (1 - margin))
    y_min = int(image_height * margin)
    y_max = int(image_height * (1 - margin))
    for m in deduped:
        m["x"] = max(x_min, min(x_max, m["x"]))
        m["y"] = max(y_min, min(y_max, m["y"]))

    # Add IDs
    for i, m in enumerate(deduped):
        m["id"] = f"auto_{i}"
        m["auto_detected"] = True

    return {
        "markers": deduped[:15],
        "primary_method": primary_method,
        "methods_tried": methods_tried,
        "count": len(deduped[:15]),
    }
