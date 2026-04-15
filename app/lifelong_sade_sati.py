from datetime import datetime, timedelta
from typing import Dict, Any

try:
    import swisseph as swe
    import os
    _ephe_path = os.getenv("EPHE_PATH", "")
    if _ephe_path:
        swe.set_ephe_path(_ephe_path)
    _HAS_SWE = True
except ImportError:
    _HAS_SWE = False

# Zodiac signs mapping
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# Detailed phase descriptions matching the PDF format
PHASE_DESCRIPTIONS = {
    "first_dhayya": {
        "title": "First Dhayya (Rising) - 12th from Moon",
        "sanskrit": "Saturn transits in the 12th house from Moon sign",
        "effects": [
            "Saturn resides on the head during this period",
            "Fall in mental and physical happiness",
            "Possibility of eye ailments or weakness of vision",
            "Sudden financial losses and unwanted expenditure",
            "Expenditure may exceed income",
            "Separation from family and domestic unrest",
            "Father may suffer ailments; relations with father may get tense",
            "Fortune might decline slightly",
            "Work may be delayed or problems may arise",
            "Interest in spiritualism increases",
            "Fear of accidents; may wander uselessly",
            "Travel to distant places which may cause hardships",
            "Inauspicious for children (8th from 5th house)"
        ]
    },
    "second_dhayya": {
        "title": "Second Dhayya (Peak) - Over Moon Sign",
        "sanskrit": "Saturn transits over the natal Moon sign",
        "effects": [
            "Saturn is placed in the abdominal area during this period",
            "Possibility of ailments in the entire middle part of the body",
            "Physical energy is affected; mind does not function properly",
            "Wrong decisions may be taken",
            "Disputes with brothers and business partners",
            "Spouse may suffer physical pain or quarrels may arise",
            "Financial problems persist; strong rebellion at mental level",
            "Useless fears cause anxiety",
            "No work is according to one's desires",
            "Obstacles continue; family and business life is unstable",
            "Some relative may die; travels to distant lands may be undertaken",
            "Enemies may inflict harm; separation from near ones",
            "Diseases, loss of wealth, decline in social standing"
        ]
    },
    "third_dhayya": {
        "title": "Third Dhayya (Setting) - 2nd from Moon",
        "sanskrit": "Saturn transits in the 2nd house from Moon sign",
        "effects": [
            "Saturn stays in the legs during this period",
            "Legs may suffer from ailments",
            "Physical weakness; feeling inactive and physically lazy",
            "Happiness faces hurdles; useless disputes occur",
            "Unnecessary conflicts with relatives arise",
            "They may suffer from serious ailment or pain equivalent to death",
            "Happiness is destroyed and position suffers",
            "Expenses increase; money comes but is spent quickly",
            "Lowly people give troubles",
            "Life span may be influenced (aspect on 8th house)",
            "Domestic happiness, mother's health, vehicles face obstacles"
        ]
    },
    "kantak_4th": {
        "title": "Kantaka Saturn - 4th House (Dhaiya)",
        "sanskrit": "Saturn transits in the 4th house from Moon sign",
        "effects": [
            "Called Laghu Kalyani Dhayya when Saturn is in 4th or 8th",
            "Full aspect on Moon lagna, 6th and 10th house from Moon",
            "Change of place or transfer may occur",
            "Housing may become a problem; heart problems may occur",
            "Blood pressure may not be stable",
            "Separation from relatives; family happiness suffers",
            "Opposition from public and government",
            "Obstacles in the work sphere (aspect on 10th house)",
            "Mental fear due to Saturn's aspect on Moon lagna"
        ]
    },
    "kantak_7th": {
        "title": "Kantaka Saturn - 7th House",
        "sanskrit": "Saturn transits in the 7th house from Moon sign",
        "effects": [
            "Full aspect on Moon lagna, 4th and 9th house from Moon",
            "Spouse may suffer from ailments of urinary organs",
            "Mental anxiety increases significantly",
            "Obstacles in favorable fortune (aspect on 9th house)",
            "Father may suffer; name and honor suffer",
            "Upheavals in the work-sphere",
            "Mother's health may suffer (aspect on 4th house)",
            "Vehicle related problems may occur",
            "May have to leave home, stay away for long periods",
            "Hardships in travelling"
        ]
    },
    "ashtam_8th": {
        "title": "Ashtam Shani (Panauti) - 8th House",
        "sanskrit": "Saturn transits in the 8th house from Moon sign",
        "effects": [
            "Called Laghu Kalyani Dhayya along with 4th house transit",
            "Full aspect on 2nd, 5th and 10th house from Moon sign",
            "Possibility of long term ailments and accidents",
            "Fear of being insulted; pain from government servants",
            "Chance of change in work-sphere; business may suffer",
            "Wealth may diminish significantly",
            "Children may suffer pain; possibilities of separation from children",
            "Most challenging period among all Saturn transits"
        ]
    },
    "kantak_10th": {
        "title": "Kantaka Saturn - 10th House",
        "sanskrit": "Saturn transits in the 10th house from Moon sign",
        "effects": [
            "Full aspect on 4th, 7th and 12th houses from Moon",
            "Hurdles in business and career",
            "Source of income may be upset",
            "May face failure in business or defame due to ill deeds",
            "Unnecessary expenditure may be undertaken",
            "Disputes or separation from spouse (aspect on 7th)",
            "Worries regarding home and wealth (aspect on 4th)",
            "Losses and expenses (aspect on 12th)"
        ]
    }
}

# General results for each Sade Sati cycle
CYCLE_RESULTS = {
    "first": {
        "title": "First Cycle of Sadhesati",
        "description": "The first cycle of Sadhesati of Saturn is extremely intense. During this period you may experience physical pain. There would be obstacles and hardships of various kinds. During this period of Sadhesati, there may also be some troubles to your parents.",
        "severity": "high"
    },
    "second": {
        "title": "Second Cycle of Sadhesati", 
        "description": "In the second cycle of Sadhesati, Saturn exerts mediocre influence compared to first cycle. During this period you succeed through physical struggle and labour. Despite mental unrest, your worldly progress continues. You may suffer separation or loss of parents or other elders in the family.",
        "severity": "medium"
    },
    "third": {
        "title": "Third Cycle of Sadhesati",
        "description": "In the third cycle of Sadhesati, Saturn inflicts extremely harsh results. During this period you may face tremendous physical hardships. There will be illness and even fear of death. During this period only fortunate persons survive.",
        "severity": "extreme"
    }
}

# Remedies in detailed format matching PDF
DETAILED_REMEDIES = {
    "mantra": {
        "title": "Mantra Remedies",
        "items": [
            {
                "name": "Mahamrityunjaya Mantra",
                "text": "ॐ त्र्यम्बकं यजामहे सुगन्धिं पुष्टिवर्धनम् | उर्वारुकमिव बन्धनान्मृत्योर्मुक्षीय मामृतात् ||",
                "instruction": "125,000 times recitations (daily 10 malas for 125 days)"
            },
            {
                "name": "Shani Mantra",
                "text": "ॐ शं शनैश्चराय नमः |",
                "instruction": "Recite 23,000 times in 21 days"
            },
            {
                "name": "Ancient Shani Mantra",
                "text": "ॐ नीलांजनसमाभासं रविपुत्रं यमाग्रजम् | छायामार्तण्डसम्भूतं तं नमामि शनैश्चरम् ||",
                "instruction": "Recite daily on Saturdays"
            }
        ]
    },
    "stotra": {
        "title": "Stotra (Hymns)",
        "items": [
            {
                "name": "Dashratha Stotra",
                "text": "कोणस्थः पिंगलो बभ्रुः कृष्णो रौद्रोऽन्तको यमः | सौरिः शनैश्चरो मन्दः पिप्पलादेन संस्तुतः ||",
                "instruction": "Recite 11 times daily"
            },
            {
                "name": "Shani Stotra",
                "text": "एतानि शनिनामानि प्रातरुत्थाय यः पठेत् | प्रसन्नः तस्य वरदो न कदाचित् भयं भवेत् ||",
                "instruction": "Recite for protection from Saturn's afflictions"
            }
        ]
    },
    "gemstones": {
        "title": "Gems and Metals",
        "items": [
            "Wear an iron ring made from the bottom of a boat or horse's bridle on the middle finger on Saturday",
            "Consider wearing Blue Sapphire (Neelam) after consulting an astrologer",
            "Amethyst can be worn as a substitute after consultation"
        ]
    },
    "vrat": {
        "title": "Vrata (Fasting)",
        "items": [
            "Observe Vrata on Saturdays",
            "Worship Lord Saturn with kavacha, stotra and mantra",
            "Recite Saturday Vrata Katha",
            "Consume milk, curd and fruit juice during daytime",
            "In evening, visit temple of Lord Hanuman or Bhairavji",
            "Take sweet halwa made of Urad pulse or salted Khichari"
        ]
    },
    "donation": {
        "title": "Donation (Daan)",
        "items": [
            "Donate Urad (black pulse) on Saturdays",
            "Donate sesame oil",
            "Donate sapphire (if affordable)",
            "Donate black sesame seeds",
            "Donate Kulathi (horse bean)",
            "Donate iron items",
            "Donate money and black clothes to the needy"
        ]
    },
    "other": {
        "title": "Other Remedies",
        "items": [
            "Wrap a raw cotton thread seven times around a Peepal tree on Saturday evening and light a lamp with mustard oil",
            "Measure a black thread equal to 19 times the length of your hand and wear it like a garland",
            "Bury a sweet made of urad pulse, sesame, oil and jaggery in an un-tilled place on Saturday",
            "Light a mustard oil lamp under a Peepal tree on Saturdays",
            "Recite Hanuman Chalisa on Tuesdays and Saturdays",
            "Worship Lord Shiva daily by doing Jalabhishek"
        ]
    }
}


def calculate_lifelong_sade_sati(birth_dt: datetime, moon_sign_index: int, moon_sign_name: str = "") -> Dict[str, Any]:
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
    
    # Kantaka Shani signs (4th, 7th, 10th from Moon)
    kantaka_signs = [
        (moon_sign_index + 3) % 12,   # 4th
        (moon_sign_index + 6) % 12,   # 7th
        (moon_sign_index + 9) % 12    # 10th
    ]
    
    phases = []
    
    # Trace for 100 years
    current_dt = birth_dt
    end_dt = birth_dt + timedelta(days=365.25 * 100)
    
    current_sign = -1
    phase_start_dt = None
    phase_type = None
    phase_sub_type = None
    phase_key = None

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
                phase_desc = PHASE_DESCRIPTIONS.get(phase_key, {})
                phases.append({
                    "phase": phase_type,
                    "sub_phase": phase_sub_type,
                    "phase_key": phase_key,
                    "start_date": phase_start_dt.strftime("%Y-%m-%d"),
                    "end_date": transit_dt.strftime("%Y-%m-%d"),
                    "sign_index": current_sign,
                    "sign_name": ZODIAC_SIGNS[current_sign],
                    "description": phase_desc
                })
            
            # Start new phase tracking
            current_sign = s
            phase_start_dt = transit_dt
            
            if s == sade_sati_signs[0]:
                phase_type = "Sade Sati"
                phase_sub_type = "Rising (12th from Moon)"
                phase_key = "first_dhayya"
            elif s == sade_sati_signs[1]:
                phase_type = "Sade Sati"
                phase_sub_type = "Peak (1st from Moon)"
                phase_key = "second_dhayya"
            elif s == sade_sati_signs[2]:
                phase_type = "Sade Sati"
                phase_sub_type = "Setting (2nd from Moon)"
                phase_key = "third_dhayya"
            elif s == dhaiya_signs[0]:
                phase_type = "Dhaiya"
                phase_sub_type = "Kantak Shani (4th from Moon)"
                phase_key = "kantak_4th"
            elif s == dhaiya_signs[1]:
                phase_type = "Panauti"
                phase_sub_type = "Ashtam Shani (8th from Moon)"
                phase_key = "ashtam_8th"
            elif s == kantaka_signs[1]:  # 7th from Moon
                phase_type = "Kantaka"
                phase_sub_type = "Kantaka Saturn (7th from Moon)"
                phase_key = "kantak_7th"
            elif s == kantaka_signs[2]:  # 10th from Moon
                phase_type = "Kantaka"
                phase_sub_type = "Kantaka Saturn (10th from Moon)"
                phase_key = "kantak_10th"
            else:
                phase_type = None
                phase_sub_type = None
                phase_key = None
                
        jd += step_days

    # Close the last phase if open
    if phase_start_dt and phase_type:
        phase_desc = PHASE_DESCRIPTIONS.get(phase_key, {})
        phases.append({
            "phase": phase_type,
            "sub_phase": phase_sub_type,
            "phase_key": phase_key,
            "start_date": phase_start_dt.strftime("%Y-%m-%d"),
            "end_date": end_dt.strftime("%Y-%m-%d"),
            "sign_index": current_sign,
            "sign_name": ZODIAC_SIGNS[current_sign],
            "description": phase_desc
        })

    # Organize phases by Sade Sati cycles
    sade_sati_phases = [p for p in phases if p["phase"] == "Sade Sati"]
    cycles = []
    current_cycle = []
    cycle_count = 0
    
    for phase in sade_sati_phases:
        if phase["phase_key"] == "first_dhayya":
            if current_cycle:
                cycle_count += 1
                cycle_key = ["first", "second", "third"][(cycle_count - 1) % 3]
                cycle_info = CYCLE_RESULTS.get(cycle_key, {})
                ordinals = {1: "First", 2: "Second", 3: "Third", 4: "Fourth", 5: "Fifth", 6: "Sixth"}
                cycle_title = f"{ordinals.get(cycle_count, f'{cycle_count}th')} Cycle of Sadhesati"
                cycles.append({
                    "cycle_number": cycle_count,
                    "start_date": current_cycle[0]["start_date"],
                    "end_date": current_cycle[-1]["end_date"],
                    "phases": current_cycle,
                    "title": cycle_title,
                    "description": cycle_info.get("description", ""),
                    "severity": cycle_info.get("severity", "medium")
                })
            current_cycle = [phase]
        else:
            current_cycle.append(phase)
    
    # Add the last cycle
    if current_cycle:
        cycle_count += 1
        cycle_key = ["first", "second", "third"][(cycle_count - 1) % 3]
        cycle_info = CYCLE_RESULTS.get(cycle_key, {})
        ordinals = {1: "First", 2: "Second", 3: "Third", 4: "Fourth", 5: "Fifth", 6: "Sixth"}
        cycle_title = f"{ordinals.get(cycle_count, f'{cycle_count}th')} Cycle of Sadhesati"
        cycles.append({
            "cycle_number": cycle_count,
            "start_date": current_cycle[0]["start_date"],
            "end_date": current_cycle[-1]["end_date"],
            "phases": current_cycle,
            "title": cycle_title,
            "description": cycle_info.get("description", ""),
            "severity": cycle_info.get("severity", "medium")
        })

    # Get other phases (Dhaiya, Panauti, Kantaka)
    other_phases = [p for p in phases if p["phase"] != "Sade Sati" and p["phase"] is not None]

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
        "cycles": cycles,
        "other_phases": other_phases,
        "remedies": remedies,
        "detailed_remedies": DETAILED_REMEDIES,
        "moon_sign": moon_sign_name or ZODIAC_SIGNS[moon_sign_index],
        "moon_sign_index": moon_sign_index,
        "explanation": {
            "sadesati": "The seven and a half year period during which Saturn transits in the twelfth, first and second houses from the birth rashi (Moon sign) is called the Sadhesati of Saturn.",
            "dhayya": "One Sadhesati is made up of three periods of approximately two and a half years each, because Saturn travels in one rashi for two and a half years.",
            "cycles": "Normally in the lifetime of a person, the Sadhesati of Saturn occurs three times.",
            "kantaka": "Transit of Saturn in the fourth, seventh and tenth house from the Moon is called Kantaka Saturn.",
            "laghu_kalyani": "Transit of Saturn in fourth and eighth house from the Moon sign is called Laghu Kalyani Dhayya."
        }
    }
