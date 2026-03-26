"""Palmistry guide, guided readings, and image-driven palm analysis."""
import io
import os
import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from PIL import Image, ImageFilter, ImageOps, ImageStat
from pydantic import BaseModel, Field
from typing import Optional

from app.auth import get_current_user

router = APIRouter()


class PalmistryAnalysisRequest(BaseModel):
    hand_shape: str  # earth, air, water, fire
    dominant_hand: str  # right, left
    finger_length: str  # long, short, average
    heart_line: str  # long_curved, short_straight, broken, chained, forked
    head_line: str  # long_straight, short, curved, broken, double
    life_line: str  # long_deep, short_shallow, curved, broken, multiple
    fate_line: Optional[str] = None  # deep_clear, broken, starts_life, starts_base, absent
    sun_line: Optional[str] = None  # present, multiple, absent
    mounts_prominent: list[str] = Field(default_factory=list)


PALMISTRY_GUIDE = {
    "meanings": {
        "dominant_hand": "The dominant hand represents the present and future; the non-dominant hand reflects inherited traits and potential.",
        "finger_length": "Long fingers indicate attention to detail; short fingers suggest a preference for quick action.",
        "palm_texture": "Soft palms indicate sensitivity; rough palms suggest a practical, hardworking nature.",
        "line_depth": "Deep lines indicate strong influences; faint lines suggest subtlety or flexibility in that area.",
    },
    "lines": [
        {
            "name": "Heart Line",
            "location": "Runs horizontally across the upper palm, below the fingers",
            "meanings": {
                "long_and_curved": "Warm, expressive personality; freely shows emotions and affection",
                "short_and_straight": "Practical, grounded approach to love; prefers stability over romance",
                "broken": "Emotional trauma or significant relationship upheavals",
                "chained": "Emotional sensitivity; prone to periods of sadness or relationship complexity",
                "forked_at_end": "Balance between head and heart; pragmatic yet loving",
            },
        },
        {
            "name": "Head Line",
            "location": "Runs horizontally across the middle of the palm",
            "meanings": {
                "long_and_straight": "Logical, analytical thinker; detail-oriented and methodical",
                "short": "Prefers physical achievements and action over abstract thinking",
                "curved_or_sloping": "Creative, imaginative mind; artistic and intuitive",
                "broken": "Inconsistencies in thought; mental shifts or breakthroughs",
                "double": "Exceptional mental power and versatility; brilliance",
            },
        },
        {
            "name": "Life Line",
            "location": "Curves around the base of the thumb from between index finger and thumb",
            "meanings": {
                "long_and_deep": "Strong vitality and robust health; full of energy",
                "short_and_shallow": "May be easily influenced by others; moderate energy",
                "curved": "Plenty of energy and enthusiasm for life",
                "close_to_thumb": "Low energy; often tired or cautious",
                "broken": "Major life change, illness, or drastic shift in lifestyle",
                "multiple_lines": "Extra vitality; extremely lively personality",
            },
        },
        {
            "name": "Fate Line (Saturn Line)",
            "location": "Vertical line running from base of palm toward middle finger",
            "meanings": {
                "deep_and_clear": "Strongly controlled by destiny; career success",
                "broken": "Career changes or external forces shaping life path",
                "starts_at_life_line": "Self-made individual; success through personal effort",
                "starts_at_base": "Public life; influenced by external events from early age",
                "absent": "Preplanned life is absent; freedom-loving and unconventional",
            },
        },
        {
            "name": "Sun Line (Apollo Line)",
            "location": "Vertical line running toward the ring finger",
            "meanings": {
                "present_and_clear": "Fame, success, and talent recognition",
                "multiple_lines": "Many interests but scattered focus",
                "absent": "Success still possible but may lack public recognition",
            },
        },
    ],
    "mounts": [
        {
            "name": "Mount of Jupiter",
            "location": "Below the index finger",
            "planet": "Jupiter",
            "meaning": "Leadership, ambition, confidence, religiousness. Well-developed: natural leader. Flat: lack of confidence.",
        },
        {
            "name": "Mount of Saturn",
            "location": "Below the middle finger",
            "planet": "Saturn",
            "meaning": "Responsibility, discipline, wisdom. Well-developed: serious, studious nature. Overly prominent: tendency toward isolation.",
        },
        {
            "name": "Mount of Apollo (Sun)",
            "location": "Below the ring finger",
            "planet": "Sun",
            "meaning": "Creativity, art, happiness, brilliance. Well-developed: charismatic and talented. Flat: lack of imagination.",
        },
        {
            "name": "Mount of Mercury",
            "location": "Below the little finger",
            "planet": "Mercury",
            "meaning": "Communication, wit, commerce. Well-developed: persuasive and clever. Flat: shy, difficulty expressing thoughts.",
        },
        {
            "name": "Mount of Venus",
            "location": "Base of thumb, fleshy area",
            "planet": "Venus",
            "meaning": "Love, sensuality, attraction, vitality. Well-developed: warm, passionate nature. Flat: lack of energy or desire.",
        },
        {
            "name": "Mount of Moon (Luna)",
            "location": "Lower palm, opposite thumb",
            "planet": "Moon",
            "meaning": "Imagination, intuition, travel, subconscious. Well-developed: creative, psychic abilities. Flat: lack of imagination.",
        },
        {
            "name": "Mount of Mars (Upper)",
            "location": "Below Mount of Mercury, above Mount of Moon",
            "planet": "Mars",
            "meaning": "Moral courage, resistance, perseverance. Well-developed: resilient and brave in adversity.",
        },
        {
            "name": "Mount of Mars (Lower)",
            "location": "Between Mount of Jupiter and Mount of Venus",
            "planet": "Mars",
            "meaning": "Physical courage, aggression, boldness. Well-developed: assertive and commanding.",
        },
    ],
    "shapes": [
        {
            "name": "Earth Hand",
            "features": "Square palm, short fingers",
            "meaning": "Practical, grounded, reliable. Prefers tangible results and physical work.",
        },
        {
            "name": "Air Hand",
            "features": "Square palm, long fingers",
            "meaning": "Intellectual, communicative, curious. Thrives on mental stimulation and social interaction.",
        },
        {
            "name": "Water Hand",
            "features": "Rectangular palm, long fingers",
            "meaning": "Emotional, intuitive, artistic. Sensitive to surroundings and deeply empathetic.",
        },
        {
            "name": "Fire Hand",
            "features": "Rectangular palm, short fingers",
            "meaning": "Energetic, confident, risk-taking. Natural leader driven by instinct and enthusiasm.",
        },
    ],
}

_ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
_MAX_UPLOAD_BYTES = 5 * 1024 * 1024
_UPLOAD_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "static",
    "uploads",
)


def _band_strength(image: Image.Image, top: float, bottom: float) -> float:
    height = image.height
    cropped = image.crop((0, int(height * top), image.width, int(height * bottom)))
    return float(ImageStat.Stat(cropped).mean[0])


def _band_segments(image: Image.Image, top: float, bottom: float, segments: int = 4) -> list[float]:
    start_y = int(image.height * top)
    end_y = int(image.height * bottom)
    values: list[float] = []
    for index in range(segments):
        start_x = int(image.width * index / segments)
        end_x = int(image.width * (index + 1) / segments)
        cropped = image.crop((start_x, start_y, end_x, end_y))
        values.append(float(ImageStat.Stat(cropped).mean[0]))
    return values


def _zone_strength(image: Image.Image, left: float, top: float, right: float, bottom: float) -> float:
    cropped = image.crop(
        (
            int(image.width * left),
            int(image.height * top),
            int(image.width * right),
            int(image.height * bottom),
        )
    )
    return float(ImageStat.Stat(cropped).mean[0])


def _save_upload(contents: bytes, ext: str) -> str:
    os.makedirs(_UPLOAD_DIR, exist_ok=True)
    filename = f"palmistry_{uuid.uuid4().hex}{ext}"
    with open(os.path.join(_UPLOAD_DIR, filename), "wb") as handle:
        handle.write(contents)
    return f"/static/uploads/{filename}"


def _parse_image(file: UploadFile) -> tuple[Image.Image, Image.Image, bytes, str]:
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No filename provided")

    _, ext = os.path.splitext(file.filename)
    ext = ext.lower() or ".png"
    if ext not in _ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type '{ext}' not allowed",
        )

    contents = file.file.read()
    if not contents:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty upload")
    if len(contents) > _MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image exceeds 5 MB limit")

    try:
        source = Image.open(io.BytesIO(contents))
        source = ImageOps.exif_transpose(source).convert("RGB")
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image upload") from exc

    if source.width < 160 or source.height < 160:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Palm image is too small")

    prepared = ImageOps.autocontrast(ImageOps.grayscale(source)).resize((240, 320))
    return source, prepared, contents, ext


def _infer_visual_traits(prepared: Image.Image) -> dict:
    edges = prepared.filter(ImageFilter.FIND_EDGES)
    brightness = float(ImageStat.Stat(prepared).mean[0])
    contrast = float(ImageStat.Stat(prepared).stddev[0])
    edge_density = float(ImageStat.Stat(edges).mean[0])
    aspect_ratio = prepared.height / max(prepared.width, 1)

    upper_band = _band_strength(edges, 0.16, 0.33)
    middle_band = _band_strength(edges, 0.38, 0.56)
    lower_band = _band_strength(edges, 0.58, 0.85)
    heart_segments = _band_segments(edges, 0.16, 0.33)
    head_segments = _band_segments(edges, 0.38, 0.56)
    life_segments = _band_segments(edges, 0.58, 0.85)
    fate_band = _zone_strength(edges, 0.45, 0.15, 0.56, 0.88)
    sun_band = _zone_strength(edges, 0.60, 0.14, 0.72, 0.82)
    venus_zone = _zone_strength(edges, 0.04, 0.44, 0.32, 0.92)
    moon_zone = _zone_strength(edges, 0.70, 0.48, 0.98, 0.95)
    jupiter_zone = _zone_strength(edges, 0.10, 0.02, 0.28, 0.22)
    saturn_zone = _zone_strength(edges, 0.32, 0.02, 0.50, 0.22)
    apollo_zone = _zone_strength(edges, 0.52, 0.02, 0.70, 0.22)
    mercury_zone = _zone_strength(edges, 0.72, 0.04, 0.96, 0.24)
    mars_upper_zone = _zone_strength(edges, 0.68, 0.30, 0.96, 0.56)
    mars_lower_zone = _zone_strength(edges, 0.18, 0.24, 0.44, 0.58)

    if aspect_ratio >= 1.42 and contrast < 42:
        hand_shape = "water"
    elif aspect_ratio >= 1.38:
        hand_shape = "air"
    elif contrast >= 48 or edge_density >= 26:
        hand_shape = "fire"
    else:
        hand_shape = "earth"

    if aspect_ratio >= 1.45:
        finger_length = "long"
    elif contrast >= 50 and aspect_ratio < 1.3:
        finger_length = "short"
    else:
        finger_length = "average"

    heart_spread = max(heart_segments) - min(heart_segments)
    head_spread = max(head_segments) - min(head_segments)
    life_spread = max(life_segments) - min(life_segments)

    if upper_band < edge_density * 0.8:
        heart_line = "short_straight"
    elif heart_spread > 12:
        heart_line = "broken"
    elif heart_segments[-1] > heart_segments[0] + 6:
        heart_line = "forked"
    elif contrast > 52:
        heart_line = "chained"
    else:
        heart_line = "long_curved"

    if middle_band < edge_density * 0.82:
        head_line = "short"
    elif head_spread > 11:
        head_line = "broken"
    elif aspect_ratio >= 1.4 or contrast < 40:
        head_line = "curved"
    elif edge_density > 30:
        head_line = "double"
    else:
        head_line = "long_straight"

    if lower_band < edge_density * 0.8:
        life_line = "short_shallow"
    elif life_spread > 13:
        life_line = "broken"
    elif lower_band > edge_density * 1.18 and contrast > 48:
        life_line = "multiple"
    elif lower_band > edge_density:
        life_line = "long_deep"
    else:
        life_line = "curved"

    if fate_band < 10:
        fate_line = "absent"
    elif max(_band_segments(edges, 0.18, 0.88, segments=3)) - min(_band_segments(edges, 0.18, 0.88, segments=3)) > 12:
        fate_line = "broken"
    elif aspect_ratio >= 1.45:
        fate_line = "starts_base"
    elif fate_band > edge_density:
        fate_line = "deep_clear"
    else:
        fate_line = "starts_life"

    if sun_band < 9:
        sun_line = "absent"
    elif sun_band > edge_density * 1.15 and contrast > 45:
        sun_line = "multiple"
    else:
        sun_line = "present"

    mount_scores = {
        "jupiter": jupiter_zone,
        "saturn": saturn_zone,
        "apollo": apollo_zone,
        "mercury": mercury_zone,
        "venus": venus_zone,
        "moon": moon_zone,
        "mars_upper": mars_upper_zone,
        "mars_lower": mars_lower_zone,
    }
    average_mount_score = sum(mount_scores.values()) / len(mount_scores)
    mounts_prominent = [
        name
        for name, score in sorted(mount_scores.items(), key=lambda item: item[1], reverse=True)
        if score >= average_mount_score + 2.5
    ][:3]
    if not mounts_prominent:
        mounts_prominent = [max(mount_scores, key=mount_scores.get)]

    quality_points = 0
    if 70 <= brightness <= 210:
        quality_points += 1
    if contrast >= 28:
        quality_points += 1
    if edge_density >= 12:
        quality_points += 1
    if prepared.width >= 240 and prepared.height >= 320:
        quality_points += 1

    if quality_points >= 4:
        image_quality = "excellent"
        confidence = "high"
    elif quality_points == 3:
        image_quality = "good"
        confidence = "medium"
    else:
        image_quality = "fair"
        confidence = "low"

    observations = [
        f"Line visibility appears {('strong' if edge_density >= 24 else 'moderate' if edge_density >= 14 else 'subtle')} across the palm image.",
        f"The upper palm pattern suggests a {heart_line.replace('_', ' ')} heart-line signature.",
        f"The central palm contrast suggests a {head_line.replace('_', ' ')} mental pattern.",
        f"The lower palm structure suggests a {life_line.replace('_', ' ')} vitality pattern.",
    ]
    if mounts_prominent:
        observations.append(
            "Most visually active mount zones: " + ", ".join(mount.replace("_", " ").title() for mount in mounts_prominent) + "."
        )

    return {
        "image_quality": image_quality,
        "confidence": confidence,
        "visual_observations": observations,
        "derived_traits": {
            "hand_shape": hand_shape,
            "finger_length": finger_length,
            "heart_line": heart_line,
            "head_line": head_line,
            "life_line": life_line,
            "fate_line": fate_line,
            "sun_line": sun_line,
            "mounts_prominent": mounts_prominent,
        },
        "metrics": {
            "brightness": round(brightness, 1),
            "contrast": round(contrast, 1),
            "edge_density": round(edge_density, 1),
        },
    }


def _build_reading(req: PalmistryAnalysisRequest) -> dict:
    reading = {
        "hand_type": {},
        "personality": {},
        "life_path": {},
        "relationships": {},
        "career": {},
        "health": {},
        "challenges": [],
        "strengths": [],
        "overall": "",
    }

    hand_meanings = {
        "earth": "Practical, grounded, and reliable. You prefer tangible results and physical work.",
        "air": "Intellectual, communicative, and curious. You thrive on mental stimulation.",
        "water": "Emotional, intuitive, and artistic. You are deeply empathetic and sensitive.",
        "fire": "Energetic, confident, and risk-taking. You are a natural leader driven by instinct.",
    }
    reading["hand_type"] = {
        "type": req.hand_shape,
        "meaning": hand_meanings.get(req.hand_shape, "Balanced personality"),
    }

    head_meanings = {
        "long_straight": "Logical, analytical thinker with great attention to detail.",
        "short": "Action-oriented, prefers doing over analyzing.",
        "curved": "Creative, imaginative mind with artistic tendencies.",
        "broken": "Adaptive thinker who embraces mental shifts and breakthroughs.",
        "double": "Exceptional mental power and versatility.",
    }
    reading["personality"]["mental_approach"] = head_meanings.get(req.head_line, "Balanced thinker")

    heart_meanings = {
        "long_curved": "Warm, expressive, and freely shows emotions and affection.",
        "short_straight": "Practical approach to love; prefers stability over romance.",
        "broken": "Has experienced emotional growth through relationship challenges.",
        "chained": "Deeply sensitive with complex emotional landscape.",
        "forked": "Balances head and heart; pragmatic yet loving.",
    }
    reading["relationships"]["emotional_style"] = heart_meanings.get(req.heart_line, "Balanced emotional approach")

    life_meanings = {
        "long_deep": "Strong vitality and robust health; full of energy for life's journey.",
        "short_shallow": "Moderate energy; may be more easily influenced by circumstances.",
        "curved": "Enthusiastic approach to life with plenty of energy.",
        "broken": "Major life changes have shaped your path; adaptable and resilient.",
        "multiple": "Extra vitality and extremely lively personality.",
    }
    reading["life_path"]["vitality"] = life_meanings.get(req.life_line, "Steady life energy")

    fate_meanings = {
        "deep_clear": "Strong career path with clear direction and destiny.",
        "broken": "Multiple career changes or shifts in life direction.",
        "starts_life": "Self-made success through personal effort and determination.",
        "starts_base": "Public life or career influenced by external events.",
        "absent": "Freedom-loving; you create your own path unconventionally.",
    }
    reading["career"]["destiny"] = (
        fate_meanings.get(req.fate_line, "Flexible career path")
        if req.fate_line
        else "Career path is self-directed and evolving."
    )

    sun_meanings = {
        "present": "Potential for recognition, success, and talent appreciation.",
        "multiple": "Many interests with potential for diverse achievements.",
        "absent": "Success comes through steady effort rather than public recognition.",
    }
    if req.sun_line:
        reading["career"]["success"] = sun_meanings.get(req.sun_line, "Moderate recognition")

    mount_meanings = {
        "jupiter": "Leadership and ambition",
        "saturn": "Wisdom and discipline",
        "apollo": "Creativity and charisma",
        "mercury": "Communication and wit",
        "venus": "Love and vitality",
        "moon": "Imagination and intuition",
        "mars_upper": "Moral courage",
        "mars_lower": "Physical courage",
    }
    if req.mounts_prominent:
        reading["strengths"] = [mount_meanings.get(mount, mount) for mount in req.mounts_prominent]

    reading["overall"] = (
        f"Your {req.hand_shape} hand reveals a {reading['personality']['mental_approach'].lower()} "
        f"In relationships, you are {reading['relationships']['emotional_style'].lower()} "
        f"Your life path shows {reading['life_path']['vitality'].lower()}"
    )

    if req.heart_line == "broken" and req.life_line == "broken":
        reading["challenges"].append("Major life transitions may affect emotional stability")
    if req.head_line == "short" and req.hand_shape == "air":
        reading["challenges"].append("May struggle to follow through on intellectual pursuits")
    if req.fate_line == "absent":
        reading["challenges"].append("Creating structure and direction independently")

    if req.dominant_hand == "right":
        reading["overall"] += " Your right (dominant) hand shows your present path, shaped by your choices."
    else:
        reading["overall"] += " Your left (dominant) hand reveals your inherited potential and inner nature."

    return reading


def _build_ai_insights(reading: dict, image_prefix: str | None = None) -> dict:
    summary = reading["overall"]
    if image_prefix:
        summary = f"{image_prefix} {summary}"
    return {
        "summary": summary,
        "key_traits": reading["strengths"][:3] if reading["strengths"] else ["Adaptability", "Self-awareness", "Personal growth"],
        "focus_areas": reading["challenges"] if reading["challenges"] else ["Continued self-discovery"],
    }


@router.get("/api/palmistry/guide")
def palmistry_guide():
    """Return static palmistry reference data."""
    return PALMISTRY_GUIDE


@router.post("/api/palmistry/analyze")
def analyze_palmistry(
    req: PalmistryAnalysisRequest,
    user: dict = Depends(get_current_user),
):
    """Guided palmistry analysis using explicit user selections."""
    reading = _build_reading(req)
    return {"reading": reading, "ai_insights": _build_ai_insights(reading)}


@router.post("/api/palmistry/analyze-image")
def analyze_palm_image(
    file: UploadFile = File(...),
    dominant_hand: str = Form("right"),
    user: dict = Depends(get_current_user),
):
    """Heuristic image-driven palm analysis from an uploaded palm photo."""
    source, prepared, contents, ext = _parse_image(file)
    image_analysis = _infer_visual_traits(prepared)
    image_analysis["image_url"] = _save_upload(contents, ext)
    image_analysis["image_size"] = {"width": source.width, "height": source.height}

    derived = image_analysis["derived_traits"]
    req = PalmistryAnalysisRequest(
        hand_shape=derived["hand_shape"],
        dominant_hand=dominant_hand if dominant_hand in {"left", "right"} else "right",
        finger_length=derived["finger_length"],
        heart_line=derived["heart_line"],
        head_line=derived["head_line"],
        life_line=derived["life_line"],
        fate_line=derived["fate_line"],
        sun_line=derived["sun_line"],
        mounts_prominent=derived["mounts_prominent"],
    )
    reading = _build_reading(req)
    reading["overall"] = (
        "This photo-based reading is built from visible contrast, line depth, and mount activity patterns. "
        + reading["overall"]
    )
    return {
        "reading": reading,
        "image_analysis": image_analysis,
        "ai_insights": _build_ai_insights(reading, image_prefix="Photo-derived insight:"),
    }
