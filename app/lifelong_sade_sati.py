from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any
import math

try:
    import swisseph as swe
    import os
    _ephe_path = os.getenv("EPHE_PATH", "")
    if _ephe_path:
        swe.set_ephe_path(_ephe_path)
    _HAS_SWE = True
except ImportError:
    _HAS_SWE = False

def calculate_lifelong_sade_sati(birth_dt: datetime, moon_sign_index: int) -> Dict[str, Any]:
    """
    Calculate lifelong Sade Sati, Dhaiya (Ashtamesh/Kantak), and Panauti phases.
    moon_sign_index is 0 to 11 (0=Aries).
    We calculate up to 100 years from birth.
    """
    if not _HAS_SWE:
        return {"error": "Swisseph is required for lifelong transit calculations."}

    swe.set_sid_mode(swe.SIDM_LAHIRI)

    # 12th, 1st, 2nd from Moon (Sade Sati)
    sade_sati_signs = [
        (moon_sign_index - 1) % 12,
        moon_sign_index,
        (moon_sign_index + 1) % 12
    ]
    # 4th and 8th from Moon (Dhaiya / Panauti)
    dhaiya_signs = [
        (moon_sign_index + 3) % 12,  # 4th sign (index is 0-based, so +3)
        (moon_sign_index + 7) % 12   # 8th sign (index is 0-based, so +7)
    ]
    
    phases = []
    
    # Trace for 100 years
    current_dt = birth_dt
    end_dt = birth_dt + timedelta(days=365.25 * 100)
    
    current_sign = -1
    phase_start_dt = None
    phase_type = None
    phase_sub_type = None

    jd = swe.julday(current_dt.year, current_dt.month, current_dt.day, current_dt.hour + current_dt.minute/60.0)
    
    # Step size: 5 days for rough scan, then fine tune
    step_days = 5.0
    
    def _get_saturn_sign(test_jd):
        pos, _ = swe.calc_ut(test_jd, swe.SATURN)
        aya = swe.get_ayanamsa(test_jd)
        sid_lon = (pos[0] - aya) % 360.0
        return int(sid_lon // 30.0)

    while jd < swe.julday(end_dt.year, end_dt.month, end_dt.day, 0):
        s = _get_saturn_sign(jd)
        
        if s != current_sign:
            # We entered a new sign!
            # Fine tune exact time
            start_jd = jd - step_days
            end_jd = jd
            
            while (end_jd - start_jd) > 0.05: # roughly 1 hour precision
                mid_jd = (start_jd + end_jd) / 2
                if _get_saturn_sign(mid_jd) == current_sign:
                    start_jd = mid_jd
                else:
                    end_jd = mid_jd
                    
            exact_jd = end_jd
            # Convert JD to datetime (approximate)
            # JD to y,m,d,h
            y, m, d, h = swe.revjul(exact_jd, swe.GREG_CAL)
            hours = int(h)
            minutes = int((h - hours) * 60)
            transit_dt = datetime(y, m, d, hours, minutes)
            
            # Save previous phase if any
            if phase_start_dt and phase_type:
                phases.append({
                    "phase": phase_type,
                    "sub_phase": phase_sub_type,
                    "start_date": phase_start_dt.strftime("%Y-%m-%d"),
                    "end_date": transit_dt.strftime("%Y-%m-%d"),
                    "sign_index": current_sign
                })
            
            # Start new phase tracking
            current_sign = s
            phase_start_dt = transit_dt
            
            if s == sade_sati_signs[0]:
                phase_type = "Sade Sati"
                phase_sub_type = "Rising (12th from Moon)"
            elif s == sade_sati_signs[1]:
                phase_type = "Sade Sati"
                phase_sub_type = "Peak (1st from Moon)"
            elif s == sade_sati_signs[2]:
                phase_type = "Sade Sati"
                phase_sub_type = "Setting (2nd from Moon)"
            elif s == dhaiya_signs[0]:
                phase_type = "Dhaiya"
                phase_sub_type = "Kantak Shani (4th from Moon)"
            elif s == dhaiya_signs[1]:
                phase_type = "Panauti"
                phase_sub_type = "Ashtam Shani (8th from Moon)"
            else:
                phase_type = None
                phase_sub_type = None
                
        jd += step_days

    # Close the last phase if open
    if phase_start_dt and phase_type:
        phases.append({
            "phase": phase_type,
            "sub_phase": phase_sub_type,
            "start_date": phase_start_dt.strftime("%Y-%m-%d"),
            "end_date": end_dt.strftime("%Y-%m-%d"),
            "sign_index": current_sign
        })

    # Remedies list for Sade Sati / Dhaiya / Panauti 
    remedies = [
        "Light a mustard oil lamp under a Peepal tree on Saturdays.",
        "Recite Hanuman Chalisa or Shani Chalisa on Tuesdays and Saturdays.",
        "Donate black sesame, black cloth, or iron on Saturdays.",
        "Avoid eating non-vegetarian food and consuming alcohol.",
        "Worship Lord Shiva daily by doing Jalabhishek.",
        "Consider wearing a Blue Sapphire (Neelam) or Amethyst after consulting a professional astrologer.",
        "Chant Shani Beej Mantra: Om Praam Preem Proum Sah Shanishcharaya Namah."
    ]

    return {
        "phases": phases,
        "remedies": remedies
    }
