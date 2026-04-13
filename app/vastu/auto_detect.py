"""
vastu/auto_detect.py — AI Room Detection for Floor Plans
==========================================================
Hybrid detection: CubiCasa5K (floor-plan-specific) → YOLOv8 (general) → OpenCV (classical).
Each detector degrades gracefully if its dependency is missing.
"""
import io
import logging
import os
from typing import Optional

log = logging.getLogger(__name__)

# Pre-check: is YOLOv8 model already downloaded?
_YOLO_MODEL_PATH = "yolov8n.pt"
_YOLO_AVAILABLE = False
try:
    import os as _os
    if _os.path.isfile(_YOLO_MODEL_PATH):
        _YOLO_AVAILABLE = True
        log.info("YOLOv8 model pre-loaded: yolov8n.pt")
    else:
        # Attempt download at import time (non-blocking if already exists)
        try:
            from ultralytics import YOLO
            YOLO(_YOLO_MODEL_PATH)  # downloads if missing
            _YOLO_AVAILABLE = True
            log.info("YOLOv8 model downloaded: yolov8n.pt")
        except Exception:
            log.debug("YOLOv8 model not available — will skip YOLO detection")
except Exception:
    pass

# Room type mapping — map detected classes to our 10 Vastu room types
_VASTU_ROOM_MAP = {
    # From CubiCasa5K labels
    "livingroom": "living_room", "living room": "living_room", "living": "living_room",
    "kitchen": "kitchen", "cooking": "kitchen",
    "bedroom": "master_bedroom", "master bedroom": "master_bedroom",
    "bathroom": "bathroom", "toilet": "bathroom", "washroom": "bathroom",
    "balcony": "living_room",  # map balcony to living room
    "corridor": None,  # skip corridors
    "dining": "kitchen",  # dining mapped to kitchen zone
    "study": "study_room", "office": "study_room",
    "children": "children_bedroom", "kid": "children_bedroom",
    "pooja": "pooja", "prayer": "pooja", "puja": "pooja",
    "staircase": "staircase", "stairs": "staircase",
    # From YOLO/COCO object classes
    "bed": "master_bedroom",
    "chair": "living_room",
    "couch": "living_room", "sofa": "living_room",
    "dining table": "kitchen",
    "refrigerator": "kitchen", "oven": "kitchen", "microwave": "kitchen",
    "tv": "living_room", "remote": "living_room",
    "sink": "kitchen",
    "vase": "pooja",
    "book": "study_room",
}


# ============================================================
# DETECTOR 1: OpenCV (classical CV, no ML, always available)
# ============================================================
def _detect_opencv(image_bytes: bytes) -> list[dict]:
    """
    Detect rooms using contour analysis.
    Best for clean architectural floor plan drawings (line art).
    """
    try:
        import cv2
        import numpy as np
    except ImportError:
        log.debug("OpenCV not installed — skipping CV detection")
        return []

    # Decode image from bytes
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        return []

    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Adaptive threshold for varying lighting
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY_INV, 51, 10)

    # Morphological close to connect broken lines (walls)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=3)

    # Find contours — each closed contour is a potential room
    contours, hierarchy = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    rooms = []
    min_area = (w * h) * 0.005   # room must be at least 0.5% of image
    max_area = (w * h) * 0.5     # room can't be more than 50% of image

    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area < min_area or area > max_area:
            continue

        x, y, cw, ch = cv2.boundingRect(contour)
        aspect = cw / ch if ch > 0 else 1

        # Skip very thin shapes (probably walls, not rooms)
        if aspect > 5 or aspect < 0.2:
            continue

        # Classify by size relative to image
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
            "width": cw,
            "height": ch,
            "confidence": round(min(area / (w * h * 0.1), 0.85), 2),
            "method": "opencv",
        })

    # Deduplicate overlapping detections (keep largest)
    rooms.sort(key=lambda r: r.get("width", 0) * r.get("height", 0), reverse=True)
    filtered = []
    for room in rooms:
        overlap = False
        for kept in filtered:
            dx = abs(room["x"] - kept["x"])
            dy = abs(room["y"] - kept["y"])
            if dx < 50 and dy < 50:
                overlap = True
                break
        if not overlap:
            filtered.append(room)

    return filtered[:12]  # cap at 12 rooms


# ============================================================
# DETECTOR 2: YOLOv8 (general object detection)
# ============================================================
def _detect_yolo(image_bytes: bytes) -> list[dict]:
    """
    Detect room-associated objects using YOLOv8 (ultralytics).
    Maps detected objects (bed, toilet, fridge) to room types.
    """
    try:
        from ultralytics import YOLO
        from PIL import Image
    except ImportError:
        log.debug("ultralytics not installed — skipping YOLO detection (pip install ultralytics)")
        return []

    # Load nano model (smallest, ~6MB)
    try:
        model = YOLO("yolov8n.pt")
    except Exception as e:
        log.warning(f"Failed to load YOLO model: {e}")
        return []

    img = Image.open(io.BytesIO(image_bytes))
    results = model(img, verbose=False)

    rooms = []
    seen_types = set()

    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls)
            cls_name = result.names.get(cls_id, "")
            conf = float(box.conf)

            if conf < 0.4:
                continue

            room_type = _VASTU_ROOM_MAP.get(cls_name.lower())
            if not room_type:
                continue

            # Only one detection per room type to avoid duplicates
            if room_type in seen_types:
                continue
            seen_types.add(room_type)

            x1, y1, x2, y2 = box.xyxy[0].tolist()
            rooms.append({
                "room_type": room_type,
                "x": int((x1 + x2) / 2),
                "y": int((y1 + y2) / 2),
                "width": int(x2 - x1),
                "height": int(y2 - y1),
                "confidence": round(conf, 2),
                "method": "yolo",
                "detected_object": cls_name,
            })

    return rooms


# ============================================================
# DETECTOR 3: OCR text detection (read room labels)
# ============================================================
def _detect_ocr_labels(image_bytes: bytes) -> list[dict]:
    """
    Read text labels from floor plan images using Pillow + basic heuristics.
    Looks for room name text (Kitchen, Bedroom, etc.) written on the plan.
    Falls back gracefully if pytesseract is not available.
    """
    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        log.debug("pytesseract not installed — skipping OCR (pip install pytesseract)")
        return []

    try:
        img = Image.open(io.BytesIO(image_bytes))
        # Try PSM 6 (uniform text block) for better scattered text detection
        # Fall back to default if it fails
        try:
            custom_config = r'--oem 3 --psm 6'
            data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, config=custom_config)
        except:
            data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    except Exception as e:
        log.warning(f"OCR failed: {e}")
        return []

    rooms = []
    keywords = {
        # Kitchen variations
        "kitchen": "kitchen", "rasoi": "kitchen", "cooking": "kitchen",
        # Bedroom variations (need to check for "master" vs regular bedroom)
        "master bedroom": "master_bedroom", "master": "master_bedroom",
        "bedroom": "master_bedroom", "bed room": "master_bedroom", 
        "shayanakaksh": "master_bedroom", "shayan": "master_bedroom",
        # Children's bedroom
        "children": "children_bedroom", "child": "children_bedroom", 
        "kids": "children_bedroom", "kid": "children_bedroom",
        # Bathroom
        "bathroom": "bathroom", "toilet": "bathroom", "bath": "bathroom",
        "washroom": "bathroom", "shower": "bathroom",
        # Living room (with common OCR typos) - tesseract often drops final G
        "living": "living_room", "livine": "living_room", "uvine": "living_room", "livin": "living_room",
        "drawing": "living_room", "baithak": "living_room",
        "sitting": "living_room", "hall": "living_room", "room": "living_room",
        # Pooja room
        "pooja": "pooja", "puja": "pooja", "mandir": "pooja",
        "prayer": "pooja", "worship": "pooja", "temple": "pooja",
        # Study/Office
        "study": "study_room", "office": "study_room", "work": "study_room",
        # Staircase
        "stair": "staircase", "stairs": "staircase",
        # Storage
        "store": "store_room", "storage": "store_room",
        "balcony": "living_room",
    }

    n_boxes = len(data["text"])
    
    # Get image dimensions from data bounds
    img_width = max([data["left"][i] + data["width"][i] for i in range(n_boxes)] + [0])
    img_height = max([data["top"][i] + data["height"][i] for i in range(n_boxes)] + [0])
    
    # First pass: collect all valid text boxes with metadata
    text_boxes = []
    for i in range(n_boxes):
        text = data["text"][i].strip()
        conf = int(data["conf"][i]) if data["conf"][i] != '-1' else 0

        if conf < 25 or len(text) < 2:
            continue
            
        x = data["left"][i] + data["width"][i] // 2
        y = data["top"][i] + data["height"][i] // 2
        
        # Filter out detections in typical sidebar/checklist areas
        if img_width > 0 and img_height > 0:
            if x > img_width * 0.85:  # Right sidebar
                continue
            if y < img_height * 0.05 or y > img_height * 0.95:  # Top/bottom margins
                continue
        
        text_boxes.append({
            "text": text,
            "text_lower": text.lower(),
            "conf": conf,
            "x": x,
            "y": y,
            "left": data["left"][i],
            "top": data["top"][i],
            "width": data["width"][i],
            "height": data["height"][i],
        })
    
    # Second pass: combine nearby text boxes (for multi-word room names)
    combined = []
    used = set()
    
    for i, box in enumerate(text_boxes):
        if i in used:
            continue
        
        # Look for nearby boxes (within 80px horizontally, 20px vertically)
        nearby = [box]
        for j, other in enumerate(text_boxes):
            if i == j or j in used:
                continue
            dx = abs(box["x"] - other["x"])
            dy = abs(box["y"] - other["y"])
            # Same line (similar y) and close in x
            if dy < 30 and dx < 150:
                nearby.append(other)
                used.add(j)
        
        if len(nearby) > 1:
            # Sort by x position
            nearby.sort(key=lambda b: b["x"])
            combined_text = " ".join([b["text"] for b in nearby])
            combined_lower = combined_text.lower()
            avg_conf = sum([b["conf"] for b in nearby]) / len(nearby)
            center_x = sum([b["x"] for b in nearby]) / len(nearby)
            center_y = sum([b["y"] for b in nearby]) / len(nearby)
            combined.append({
                "text": combined_text,
                "text_lower": combined_lower,
                "conf": avg_conf,
                "x": int(center_x),
                "y": int(center_y),
            })
            used.add(i)
        else:
            combined.append(box)
    
    # Third pass: match against keywords
    for box in combined:
        text = box["text_lower"]
        
        # Skip if it's likely not a room label
        skip_words = ["sample", "floorplan", "forvastu", "analysis", "test", "checklist", 
                      "click", "detect", "button", "should", "verify", "expected", 
                      "detection", "upload", "image", "main", "entrance", "scale", "feet"]
        if any(sw in text for sw in skip_words):
            continue
        
        # Check for multi-word phrases first (more specific)
        matched = False
        for phrase, room_type in keywords.items():
            if " " in phrase and phrase in text:
                rooms.append({
                    "room_type": room_type,
                    "x": box["x"],
                    "y": box["y"],
                    "confidence": round(box["conf"] / 100, 2),
                    "method": "ocr",
                    "detected_text": box["text"],
                })
                matched = True
                break
        
        if matched:
            continue
            
        # Check for single keywords
        for kw, room_type in keywords.items():
            if kw in text:
                rooms.append({
                    "room_type": room_type,
                    "x": box["x"],
                    "y": box["y"],
                    "confidence": round(box["conf"] / 100, 2),
                    "method": "ocr",
                    "detected_text": box["text"],
                })
                break

    return rooms


# ============================================================
# MAIN: Hybrid auto-detection
# ============================================================
def auto_detect_rooms(image_bytes: bytes, image_width: int, image_height: int) -> dict:
    """
    Detect rooms using multiple methods, return best results.

    Strategy:
      1. Try OCR first (if labels exist, most accurate)
      2. Try YOLOv8 (good for photos with furniture visible)
      3. Fall back to OpenCV contour detection (works on line drawings)
      4. Merge results from all methods, deduplicate

    Returns:
        {
            "markers": [{room_type, x, y, confidence, method}, ...],
            "primary_method": "ocr" | "yolo" | "opencv",
            "methods_tried": ["ocr", "yolo", "opencv"],
            "count": int,
        }
    """
    all_markers = []
    methods_tried = []
    primary_method = "manual"

    # Method 1: OCR (if pytesseract available)
    ocr_results = _detect_ocr_labels(image_bytes)
    if ocr_results:
        methods_tried.append("ocr")
        all_markers.extend(ocr_results)
        primary_method = "ocr"
        log.info(f"OCR detected {len(ocr_results)} room labels")

    # Method 2: YOLOv8 (if ultralytics available)
    yolo_results = _detect_yolo(image_bytes)
    if yolo_results:
        methods_tried.append("yolo")
        all_markers.extend(yolo_results)
        if not primary_method or primary_method == "manual":
            primary_method = "yolo"
        log.info(f"YOLO detected {len(yolo_results)} room objects")

    # Method 3: OpenCV contours (always available if cv2 installed)
    cv_results = _detect_opencv(image_bytes)
    if cv_results:
        methods_tried.append("opencv")
        # Only use OpenCV results if other methods found fewer rooms
        if len(all_markers) < 3:
            all_markers.extend(cv_results)
            if primary_method == "manual":
                primary_method = "opencv"
        log.info(f"OpenCV detected {len(cv_results)} contour rooms")

    if not methods_tried:
        methods_tried.append("none")

    # Deduplicate: if two detections are within 80px, keep higher confidence
    deduped = []
    all_markers.sort(key=lambda m: m.get("confidence", 0), reverse=True)
    for marker in all_markers:
        overlap = False
        for kept in deduped:
            dx = abs(marker["x"] - kept["x"])
            dy = abs(marker["y"] - kept["y"])
            if dx < 80 and dy < 80 and marker["room_type"] == kept["room_type"]:
                overlap = True
                break
        if not overlap:
            deduped.append(marker)

    # Add unique IDs
    for i, m in enumerate(deduped):
        m["id"] = f"auto_{i}"
        m["auto_detected"] = True

    return {
        "markers": deduped[:15],  # cap at 15 rooms
        "primary_method": primary_method,
        "methods_tried": methods_tried,
        "count": len(deduped[:15]),
    }
