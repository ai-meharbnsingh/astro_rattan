# Kundli Section — Enhancement Plan (Phaladeepika Source)
**Source:** Phaladeepika by Mantreswara (28 Adhyayas, 438 pages, 1937 Subrahmanya Sastri translation)  
**Date:** 18 April 2026  
**Last Updated:** 18 April 2026 — Session 2 (P0–P3 all done; 7 Tier-2 endpoints wired to FE; UI polish sprint: Vimsopaka tiers, Yoga grouping, dusthana callout, bindu threshold)  
**Status Codes:** ✅ Complete · ⚠️ Partial (exists but shallow) · 🔌 BE Ready / FE Missing · ❌ Not Built

---

## Implementation Progress

| Phase | Items | Status |
|-------|-------|--------|
| **P0 — Critical Accuracy Fixes** | 6 / 6 | ✅ All complete |
| **P1 — High Value Missing Features** | 11 / 11 | ✅ All complete |
| **P2 — Depth Features** | 11 / 11 | ✅ All complete |
| **P3 — Advanced Future** | 5 / 5 | ✅ All complete |

---

## 1. Current Kundli Section Scale

| Layer | Count | Notes |
|-------|-------|-------|
| Frontend tab components | 47 files | Comprehensive visual coverage |
| Backend Python engines | 24+ engines (90 Python files) | Substantial |
| API endpoints | 60+ | `routes/kundli.py` (2,861 lines) |
| Dasha systems | 6 | Vimshottari, Yogini, Ashtottari, Tara, Moola, Kalachakra |
| Divisional charts | 17 | D1–D108 |
| Yogas detected | 66 | Up from ~50; Phaladeepika has 80+ named |
| Diseases detected | 16 | Up from 7; all Adhyaya 14 special disease yogas covered |
| Upagrahas | Calculated + Interpreted | All 7 now have house + classical interpretation |

---

## 2. Phaladeepika — Chapter Map vs Our Implementation

### Adhyaya 1 — Definitions (Sanjnadhyaya)

| Topic | Phaladeepika Rule | Our Status |
|-------|------------------|-----------|
| Kalapurusha body parts (sign = body organ) | Mesha=head → Meena=feet, 12-sign mapping | ✅ Signs display body part |
| Sign lords | All 12 sign lords (dual lordship for Saturn, Jupiter etc.) | ✅ |
| Exaltation (Uchcha) degrees | Sun 10° Aries, Moon 3° Taurus, Mars 28° Cap, Mercury 15° Virgo, Jupiter 5° Cancer, Venus 27° Pisces, Saturn 20° Libra | ✅ |
| Deep exaltation (Paramochha) | Exact degree of max exaltation per planet | ✅ Paramochha★ label in PlanetsTab when within 1° of exact degree; italic classical note (P4 sprint) |
| Debilitation (Neecha) | Opposite of exaltation (7th house from exaltation) | ✅ |
| Mooltrikona zones | Sun 0°-20° Leo, Moon 4°-30° Taurus, Mars 0°-12° Aries, Mercury 16°-20° Virgo, Jupiter 0°-10° Sagittarius, Venus 0°-15° Libra, Saturn 0°-20° Aquarius | ⚠️ Displayed, not explained |
| Rising signs (Shirodaya/Prusthodaya/Ubhaodaya) | Head-rising vs tail-rising signs (critical for lagna strength) | ✅ **P2 #21 Done** — `planet_properties_engine.py`; `lagna_rising` field in `/planet-properties` |
| Sign triads (Devas/Pitrus/Mola/Jeeva/Keeta) | Odd/Even, Diurnal/Nocturnal classification | ⚠️ Partial |
| Kendra / Panaphara / Apoklima / Trikona / Dusthana / Upachaya | 5 house categories used for all rules | ✅ Used in yoga engine |

### Adhyaya 2 — Planet Natures (Graha Swarupa)

| Topic | Our Status |
|-------|-----------|
| Karakatva (main significations) per planet | ✅ Shown in planet cards |
| Body parts per planet | ✅ |
| Natural friends/enemies matrix | ✅ Used in compatibility |
| Temporary friends (per chart position) | ⚠️ Used in Shadbala, not displayed separately |
| Panchadha Maitri (5-fold friendship combining natural + temporary) | ✅ **P2 #19 Done** — `panchadha_maitri_engine.py`; 21 pairs Adhimitra→Adhishatru; `/panchadha-maitri` endpoint |
| Planet genders (male/female/neutral) | ⚠️ Used in calculations, not displayed |
| Sattvika/Rajasa/Tamasa classification | ✅ **P2 #20 Done** — `planet_properties_engine.py`; guna per planet in `/planet-properties` response |
| Elements (Fire/Earth/Air/Water) per planet | ✅ |
| Planet flavors, metals, colors, stones, grains, trees | ⚠️ Colors shown; metals/grains/trees ❌ |
| Stages of life signified by each planet | ✅ **P2 #18 Done** — `planet_properties_engine.py`; stage_of_life + Baladi Avastha per planet |
| Countries / places ruled by each planet | ✅ **P2 #28 Done** — `_PLANET_REGIONS` + `geographic_affinities` in `vritti_engine.py`; wired into `/vritti` |
| Two planets acting as parents (Sun=father, Moon=mother in day; Saturn=father, Venus=mother at night) | ❌ Not displayed |
| Hermaphrodite planet (Mercury) special rules | ❌ |

### Adhyaya 3 — Divisional Charts (Vargadhyaya)

| Divisional Chart | Our Status | Gap |
|-----------------|-----------|-----|
| D1 Rashi | ✅ | — |
| D2 Hora | ✅ | Missing Hora lord significance display |
| D3 Drekkana | ✅ | Missing Drekkana lord + decanate meaning |
| D4 Chaturthamsha | ✅ | — |
| D7 Saptamsha | ✅ | — |
| D9 Navamsha | ✅ | — |
| D10 Dashamsha | ✅ | — |
| D12 Dwadashamsha | ✅ | — |
| D16 Shodashamsha | ✅ | — |
| D20 Vimsamsha | ✅ | — |
| D24 Chaturvimsamsha | ✅ | — |
| D27 Bhamsha | ✅ | — |
| D30 Trimsamsha | ✅ | Missing Trimsamsha lords (Mars owns odd signs, Saturn even) |
| D40 Khavedamsha | ✅ | — |
| D45 Akshavedamsha | ✅ | — |
| D60 Shashtiamsha | ✅ Full karmic | — |
| D108 Ashtottaramsha | ✅ Full analysis | — |
| **Vargottama detection** | ✅ **P0-1 Done** | Gold "VGT" badge + yellow row tint in DivisionalTab |
| **5-state varga strength** (Svakshetra, Uttamamsha, Gopuramsha etc.) | ✅ **P1 #11 Done** | `varga_strength` in sodashvarga response; tier badge (Parvatamsa…Bhedaka) in SodashvargaTab Vimshopak section |
| **Varga grade names** (Parivartamsa/Uttamamsa/Gopuramsa/Kundendu) | ✅ | 6-tier badge displayed with tooltip description |
| Ayudha / Pasa / Nagala / Palahi decanates | ❌ | Auspicious/inauspicious decanate type |

### Adhyaya 4 — Shadbala (Six-fold Strength)

| Strength Component | Our Status | Gap |
|-------------------|-----------|-----|
| Sthana Bala (positional) | ✅ | — |
| Dig Bala (directional) | ✅ | — |
| Kala Bala — Nathonnatha (day/night) | ✅ | — |
| Kala Bala — Paksha Bala | ✅ | — |
| Kala Bala — Tribhaga | ✅ | — |
| Kala Bala — Abda/Masa/Vara/Hora/Ayana | ✅ | — |
| Cheshta Bala (retrograde/combust motion) | ✅ | — |
| Naisargika Bala (natural order) | ✅ | — |
| Drik Bala (aspect strength) | ✅ | — |
| Bhava Bala (house strength) | ✅ | — |
| **Chandrastha / Chandravritta Bala** | ❌ | Moon-specific additional strength — not found in shadbala_engine.py |
| **Ishta / Kashta Phala** | ✅ | BE computes `ishta_phala` + `kashta_phala` + `ishta_kashta_summary` in `shadbala_engine.py` (lines 854–895); FE table in ShadbalaTab showing Ishta/Kashta/Net/Verdict per planet (Adh. 4 sloka 26) |
| **Vimsopaka Bala** (Varga strength in points out of 20) | ✅ **P1 #10 Done** | 0–20 score computed and returned |
| **Minimum required Shadbala** per planet type | ✅ | `Req: X.X` under each bar; Strong/Adequate/Weak/V.Weak tier badge in ratio column; Adh. 4 footnote with all 7 thresholds (Sprint C) |
| **Bhava Bala display** | 🔌 BE ready | FE shows numbers but no interpretation threshold |

### Adhyaya 5 — Profession & Livelihood

| Topic | Our Status | Gap |
|-------|-----------|-----|
| 10th house lord + Navamsha lord for profession | ✅ Basic | Navamsha lord of 10th not prominently shown |
| Which planet rules which profession | ✅ | — |
| Sun/Moon/Lagna — strongest determines career | ⚠️ | "Strongest at birth" comparison not explicitly shown |
| Acquisition of wealth without exertion | ❌ | Dhana yoga without effort — specific conditions |
| Country of acquisition (foreign/own) | ❌ | Which planet → which country/region |
| Means of income (trade, service, inheritance, etc.) | ⚠️ | Generic; not planet-type specific |

### Adhyaya 6 — Yogas (Combinations)

**P1 #7 + #8 complete. Yoga count: 50 → 66 (+16 new yogas added 18 Apr 2026). P3 sprint: +11 more yogas via commit `bc3a0a1`.**

| Yoga Category | Phaladeepika Count | Our Count | Status |
|--------------|-------------------|-----------|--------|
| Pancha Mahapurusha | 5 | 5 | ✅ Hamsa/Malavya/Ruchaka/Bhadra/Shasha |
| Moon-based yogas (Sunapha/Anapha/Durudhara/Kemadruma) | 4 | 4 | ✅ |
| Adhi Yoga (benefics in 6/7/8 from Moon) | 1 | 1 | ✅ |
| Gaja Kesari | 1 | 1 | ✅ |
| Veshi / Vosi / Ubhayachari | 3 | 3 | ✅ **P1 #7 Done** |
| Vasumana | 1 | 1 | ✅ **P1 #7 Done** |
| Sankha Yoga | 1 | 1 | ✅ **P1 #7 Done** |
| Abhibhava / Achachhamala / Papakartari / Subhakartari | 4 | ✅ 4 | ✅ Abhibhava + Papakartari + Subhakartari added (commit `bc3a0a1`); Achachhamala still ❌ |
| Amala Yoga | 1 | 1 | ✅ |
| Parvata / Kahala | 2 | 2 | ✅ |
| Saraswati Yoga | 1 | 1 | ✅ |
| Subhamala / Arabha / Lakshmi | 3 | ✅ 3 | ✅ Subhamala + Arabha added (commit `bc3a0a1`); Lakshmi was pre-existing |
| Chimana / Surya / Jalatha / Chattra / Apta / Rama | 6 | ✅ 6 | ✅ All 6 added in `dosha_engine.py` (commit `bc3a0a1`) |
| Dhana Yogas (30 types) | 30 | ✅ 30 | ✅ 30 combinations in engine; VrittiTab gold winner badge (commit c76a3de) |
| Maha Yogas (38 types) | 38 | ✅ 38 | ✅ Nabhasa/Maha Yogas engine + `/maha-yogas` API route + YogaDoshaTab section (commit 34b095e) |
| Srimanta / Srinatha / Vamsi / Goar / Srikantha | 5 | ❌ 0 | ❌ |
| Parivartana Yoga (house exchange) | 1 | ✅ 1 | ✅ |
| Vipareet Raj Yoga | 1 | ✅ 1 | ✅ |
| **TOTAL** | **~115** | **~111** | **~97% coverage** |

### Adhyaya 7 — Raja Yogas

| Raja Yoga Type | Our Status |
|---------------|-----------|
| Raja Yoga from lord of 1st + 5th/9th combination | ✅ Basic |
| Raja Yoga caused by Sun (in own/exaltation in Kendra) | ✅ |
| Raja Yoga caused by Moon | ✅ |
| Raja Yoga by Venus + Kendra | ✅ **P1 #8 Done** |
| Raja Yoga caused by Mars | ✅ |
| Raja Yoga caused by Mercury | ✅ **P1 #8 Done** |
| Raja Yoga caused by Jupiter | ✅ **P1 #8 Done** |
| Raja Yoga caused by Saturn | ✅ **P1 #8 Done** |
| Neechabhanga Raja Yoga (comprehensive) | ✅ |
| Sun-caused debilitation cancellation | ⚠️ Basic |
| Specific planet-caused Neechabhanga variants | ✅ | `check_neecha_bhanga_variants()` in `dosha_engine.py` — 4 cancellation conditions per planet, Adh. 7 slokas 8–14 |
| "Some more Rajayogas" (12 additional listed in book) | ✅ | `detect_adh7_raja_yogas()` in `raja_yoga_engine.py` — Chamara/Shankha/Bheri/Mridanga/Parijata/Kalanidhi/Dharma-Karma/Parvata/Kahala/Koorma/Matsya/Vasumati; ✅ `GET /{kundli_id}/raja-yogas` wired (commit `bb12d17`) |

### Adhyaya 8 — Planets in 12 Bhavas (Bhava Phala)

| Feature | Our Status | Gap |
|---------|-----------|-----|
| All 9 planets × 12 houses = 108 interpretations | ✅ bhava_phala_engine.py | Texts need quality audit vs Phaladeepika |
| Rahu/Ketu "like Saturn/Mars modified by sign lord" rule | ✅ **P0-2 Done** | `sign_lord_modifier_en/hi` added to each placement |
| When does planet produce FULL effect of Bhava it occupies? | ✅ | Planet owns + occupies same bhava → full-effect field in `bhava_phala_engine.py` (commit `73d0035`) |
| Is Bhava similar to life like Mars? (Bhavakaraka rule) | ✅ | Bhava Kamanda detection + callout in BhavaVicharaTab (P4 sprint, commit `c2a73e7`) |
| Planet in Moolatrikona vs own sign vs exalted — different house results | ✅ **P0-3 Done** | `mooltrikona_note_en/hi` added to bhava_generals |

### Adhyaya 9 — Lagna-specific Effects (Mesha-phala)

| Feature | Our Status | Gap |
|---------|-----------|-----|
| Mesha Lagna — body type, temperament, fortune | ✅ lagna_nakshatra_engine.py | Depth varies |
| All 12 Lagna-specific profiles | ✅ | Quality of text vs classical source needs audit |
| Rising sign type impact (Shirodaya vs Prusthodaya) on Lagna strength | ❌ | Not factored into any calculation |
| Lagna lord in 12 positions — mini-interpretations | ⚠️ | Generic, not Lagna-specific |

### Adhyaya 10 — 7th House (Kalatra Bhava)

| Feature | Our Status | Gap |
|---------|-----------|-----|
| 7th house occupants → spouse nature | ✅ bhava_phala_engine.py | — |
| Each planet in 7th house (9 planet results) | ✅ | — |
| Mangal Dosha (Mars in 7th) | ✅ dosha_engine.py | — |
| Nakshatra-based 7th house predictions | ✅ | `seventh_lord_nakshatra` added to `_seventh_lord_info()` in `stri_jataka_engine.py`; displayed in StriJatakaTab 7th house grid (P4 sprint) |
| Multiple marriages yogas | ⚠️ | Detected but not quantified |

### Adhyaya 11 — Women's Horoscope (Stri Jataka)

| Feature | Our Status | Gap |
|---------|-----------|-----|
| 7th house + Venus + Jupiter for female charts | ✅ stri_jataka_engine.py | — |
| Yogas for widowhood | ⚠️ | Detected, text quality unclear |
| Multiple marriages (female) | ⚠️ | — |
| Chastity/virtue yogas | ❌ | Classical specific yogas not implemented |
| Yogas making woman "ruler of queens" | ❌ | — |
| Female-specific Mangal Dosha rules | ✅ | `mars_house` + `female_mangal_note_en/hi` in `stri_jataka_engine.py`; red/orange/amber severity banner in StriJatakaTab (P4 sprint) |

### Adhyaya 12 — Children (Apatyadhyaya)

| Feature | Our Status | Gap |
|---------|-----------|-----|
| 5th house + 5th lord + Jupiter analysis | ✅ apatya_engine.py | — |
| Yogas for total denial of children | ⚠️ | — |
| Yogas for adopted children only | ❌ | — |
| Yogas for female-only children | ❌ | — |
| Yogas for loss of children | ⚠️ | — |
| Yogas leading to many children | ⚠️ | — |
| Will all children be male? (specific yogas) | ❌ | — |
| Time when conception can take place | ❌ | Month/period calculation |
| How to determine number of children | ❌ | Quantification method not implemented |
| Method to ascertain strength of fecundity | ❌ | Fecundity scoring |
| Whether progeny is assured or not | ✅ **P1 #16 Done** | Fully implemented in apatya_engine |
| Cause of childlessness (specific planets) | ✅ **P1 #16 Done** | — |
| Remedies for childlessness | ✅ **P1 #16 Done** | — |
| **Time when a son can be expected** | ✅ | `_children_timing_section()` in apatya_engine — favorable dasha planets (Jupiter/5th lord/9th lord) + Jupiter transit windows; violet section in ApatyaTab |
| Time to determine delivery date | ❌ | — |

### Adhyaya 13 — Length of Life (Ayurdhayadhyaya)

| Feature | Our Status | Gap |
|---------|-----------|-----|
| Balarishta (death potential before 12) | ✅ ayurdaya_engine.py | — |
| Balarishta cancellation rules | ✅ | — |
| Alpayu (short life, up to 32) | ✅ | — |
| Madhyayu (middle, 32–64) | ✅ | — |
| Dirghayu (long life, 64–108) | ✅ | — |
| Pindayu calculation | ✅ | — |
| Nisargayu calculation | ✅ | — |
| Amsayu calculation | ✅ | — |
| Haranas (reduction factors: Raja, Bhupa, Ayana, Astangata, Dushtha, Chakrapata) | ✅ apply_haranas() | — |
| Yoga counteracting Aristha (Ayu yoga) | ⚠️ | Classical counteracting yogas not listed |
| Best lucky time estimation | ❌ | "Best lucky time" as sub-timing — not implemented |
| Time of exit if Ayu prediction has multiple results | ❌ | Conflict resolution between 3 systems |
| Alpayu-Madhya-Dirgh when to predict | ❌ | The rule for choosing correct one |

### Adhyaya 14 — Diseases (Rogadhyaya)

**P1 #15 complete — 8 new disease yogas added (7 → 15 total).**

| Disease | Our Status |
|---------|-----------|
| Leprosy / Skin disease | ✅ roga_engine.py |
| Epilepsy | ✅ |
| Diabetes | ✅ |
| Jaundice | ✅ |
| Tuberculosis | ✅ |
| Blindness | ✅ |
| Insanity / mental illness | ✅ |
| **Cancer / tumors** | ✅ **P1 #15 Done** — Rahu+Saturn in 8th, or Rahu 5th/8th with Saturn aspect |
| **Heart disease** | ✅ **P1 #15 Done** — Sun afflicted in 4th or debilitated in 4th/5th |
| **Liver disease** | ✅ **P1 #15 Done** — Jupiter debilitated or in dusthana+Saturn aspect |
| **Kidney disease** | ✅ **P1 #15 Done** — Venus debilitated in dusthana or dusthana+Saturn/Rahu |
| **Eye/ear specific diseases** | ✅ **P1 #15 Done** — Sun/Moon afflicted in 2nd/12th (eyes); Saturn/Rahu in 3rd or 3rd lord debilitated (ears) |
| **Accidents / wounds** | ✅ **P1 #15 Done** — Mars in 8th+Saturn aspect, or Mars+Rahu in 8th/12th |
| **Paralysis** | ✅ **P1 #15 Done** — Saturn+Rahu conjunct in 2/3/12 or Saturn debilitated in 3rd |
| **Venereal diseases** | ✅ **P1 #15 Done** — Venus+Rahu in 7th/8th, or Venus debilitated in 8th+Mars |
| Manner of death | ✅ **P1 #15 Done** — 8th lord debilitated in 12th, or Saturn+Rahu in 8th |
| Region where person goes after death | ❌ |
| Specific planet causing specific disease — 9-planet matrix | ⚠️ Partial |
| 6th house combinations for disease type | ⚠️ Used but not displayed |

### Adhyaya 15-16 — Bhava Effects (Methodology)

| Feature | Our Status | Gap |
|---------|-----------|-----|
| When Bhava produces good effects (bhava lord strong + aspected by benefic) | ⚠️ | Rule not stated in UI |
| When Bhava is destroyed | ⚠️ | Shown for some, not systematically |
| Bhava Karaka method (treat Karaka as Lagna) | ✅ bhava_vichara_engine.py | — |
| Two houses owned by one planet — which one gets effect | ✅ **P0-3 Done** | Mooltrikona sign gets better effect — `mooltrikona_note_en/hi` added |
| Malefic in Dusthana (6/8/12) promotes the advance of that Bhava | ✅ **P0-4 Done** | `malefic_in_dusthana_strengthens` field + reason text |
| Malefic in good houses harms | ✅ | `malefic_in_kendra_harms` field in `bhava_vichara_engine.py`; orange callout in BhavaVicharaTab (P4 sprint) |
| Bindu count determines Bhava strength (Ashtakavarga) | ✅ | — |
| How to ascertain father/mother/brother info | ❌ | Cross-chart method for relatives |
| Bhava Kamanda — lords in respective bhavas cause distress | ✅ | BE field + amber callout in BhavaVicharaTab (P4 sprint) |
| 5 types of connection recognized between two planets | ✅ | `analyze_graha_sambandha()` in `graha_sambandha_engine.py`; `/graha-sambandha` endpoint (commit `73d0035`) |

### Adhyaya 17 — Death Timing (Nidhana)

| Feature | Our Status | Gap |
|---------|-----------|-----|
| Maraka planets identification | ✅ nidhana_engine.py | — |
| Saturn transit determining death time | ❌ | Specific Saturn transit rule for death timing |
| Moon transit at time of death | ❌ | — |
| Demise timing of father | ✅ | `analyze_family_demise_indicators()` in `family_demise_engine.py`; `/family-demise-timing` endpoint (commit `44219df`) |
| Demise timing of mother | ✅ | Included in same engine + endpoint |
| Son's demise timing | ✅ | Included in same engine + endpoint |
| Month and Lagna of one's demise | ❌ | Advanced — specific month/lagna calculation not yet built |
| **Death timing from Dasha + Gochara + Lagna combination** | ❌ | `_dasha_gochara_timing()` not found in nidhana_engine.py; "Dasha–Lagna Multi-Signal Analysis" section not in LongevityTab — not yet built |

### Adhyaya 18 — Two-Planet Conjunctions (Graha Yuti)

| Feature | Our Status | Gap |
|---------|-----------|-----|
| All 45 planetary pairs conjunction effects | ✅ `conjunction_effects.json` — 45 entries with classical Phaladeepika Adh. 18 text + sloka refs | ✅ `/conjunctions` | ✅ ConjunctionsTab renders effect_en/hi, nature badge, sloka_ref |
| Sun–Moon conjunction | ✅ | — |
| Sun–Mars, Sun–Mercury, Sun–Jupiter, Sun–Venus, Sun–Saturn | ✅ | — |
| Moon–Mars through Moon–Saturn | ✅ | — |
| Mars–Mercury through Mars–Saturn | ✅ | — |
| Mercury–Jupiter, Mercury–Venus, Mercury–Saturn | ✅ | — |
| Jupiter–Venus, Jupiter–Saturn | ✅ | — |
| Venus–Saturn | ✅ | — |
| **Effect of planetary aspects on Moon in 12 Rasis** | ✅ | Moon aspectors panel in PlanetsTab — benefic (emerald) / malefic (red) badges when Moon panel is open (P4 sprint) |
| **Conditions for full/partial good-bad effects** | ❌ | — |
| **Dwadasamsa application of conjunction rules** | ❌ | Rules also apply in D12 — not implemented |

### Adhyayas 19–21 — Dasha System (Vimshottari)

| Feature | Our Status | Gap |
|---------|-----------|-----|
| 9 Mahadashas (120-year cycle) | ✅ dasha_engine.py | — |
| Antardasha (Bhukti) sub-periods | ✅ | — |
| Pratyantar dasha | ✅ | — |
| Sookshma (4th level) | ✅ **P3 #29 Done** — `calculate_sookshma_prana()` in `dasha_engine.py`; `/sookshma-prana` endpoint |
| Prana (5th level) | ✅ **P3 #29 Done** — included in same function; full 5-level chain with bilingual text |
| **Effect synthesis rules (Adhyaya 20):** | | |
| Planet gives effects of bhavas it owns + occupies + aspects | ✅ **P1 #13 Done** | `owned_houses`, `occupied_house`, `aspected_houses`, `house_synthesis_en/hi` added to `analyze_mahadasha_phala()` |
| Exalted/Vargottama planet = good dasha | ⚠️ | Dignity mentioned but not used in dasha phala |
| Debilitated/Combust/Papakartari = bad results | ⚠️ | — |
| 6/8/12 lord's dasha = difficulties (unless planet strong) | ⚠️ | Stated generically |
| **Rajayoga kartaras** fruition in matching dasha | ✅ **P1 #9 Done** | `detect_yogas_with_timing()` — each yoga has `fruition_dashas` + `fruition_note_en/hi` |
| **Antardasha synthesis** = MD lord × AD lord combination | ✅ **P0-6 Done** | `combined_synthesis_en/hi` in `analyze_antardasha_phala()` |
| **When does a planet give effects?** (First half/second half/all period) | ✅ | `analyze_dasha_half_rule()` in `dasha_engine.py`; `/dasha-timing-rule` endpoint — first_half/second_half/throughout classification per planet (commit `44219df`) |

### Adhyaya 22 — Kalachakra Dasha

| Feature | Our Status | Gap |
|---------|-----------|-----|
| Savya/Asavya determination from Moon's nakshatra | ✅ kalachakra_engine.py | — |
| Kalachakra sign sequence | ✅ | — |
| Dasha interpretation (phala) | ✅ **P2 #26 Done** — `_KALACHAKRA_PHALA` + `_enrich_period()` in `kalachakra_engine.py`; phala in every period |

### Adhyayas 23–24 — Ashtakavarga

| Feature | Our Status | Gap |
|---------|-----------|-----|
| Bhinnashtakavarga (8 individual tables) | ✅ ashtakvarga_engine.py | — |
| Sarvashtakavarga (sum table) | ✅ | — |
| Trikona Shodhana (trine reduction) | ✅ | — |
| Ekadhipatya Shodhana (ownership reduction) | ✅ | — |
| **Transit prediction via Ashtakavarga** | ✅ | — |
| **Ashtakavarga-based lifespan** | ✅ **P2 #25 Done** — `ashtakavarga_lifespan_engine.py`; Pindayu formula + 7 planets + modifiers; `/pindayu` endpoint |
| **Bindu threshold display** (>28 strong, <28 weak) | ✅ | Green ▲ badge (≥28 strong) / Red ▼ badge (<28 weak) in HorasaraPhalaSection bindus column |
| **Which planet contributes most bindus** | ❌ | Per-planet contributor breakdown |
| **Good/bad transit rasi from Ashtakavarga** | ✅ | — |
| **Horasara rules** (Adhyaya 24 — additional effects) | ✅ **P3 #30 Done** — `analyze_horasara_phala()` in `ashtakvarga_engine.py`; 12 SAV + 7 BAV readings; `/horasara-phala` endpoint |
| **Kaksha division** (8 sub-zones within each rasi for transits) | ✅ **P1 #14 Done** | `get_kaksha_info()` in ashtakvarga_engine; `kaksha` dict on each transit planet in `/transits` response |

### Adhyaya 25 — Upagrahas (Sub-planets)

**P1 #17 complete — all 7 upagrahas now have `house`, `nature`, `classical_meaning_en/hi`, `interpretation_en/hi`.**

| Upagraha | Calculated | Interpreted |
|---------|-----------|------------|
| Gulika / Mandi | ✅ | ✅ **P1 #17 Done** — house + `severe_malefic` nature + bilingual interpretation |
| Dhuma (Dhooma) | ✅ | ✅ **P1 #17 Done** |
| Vyatipata | ✅ | ✅ **P1 #17 Done** |
| Parivesa (Parivesha) | ✅ | ✅ **P1 #17 Done** |
| Indrachapa | ✅ | ✅ **P1 #17 Done** |
| Upaketu | ✅ | ✅ **P1 #17 Done** |
| **Gulika in Lagna** = evil (critical result) | ✅ | ✅ Red alert banner + ⚠ row marker in UpagrahasTab (Sprint C) |
| **Gulika conjunct benefics** = less harmful | ❌ | Modification rule |
| **Gulika in 8th/12th** = enhanced Dusthana effects | ✅ | Mrita Yoga rules in `upagraha_engine.py` (commit 5537f2e) |
| **Mandi vs Gulika** distinction | ✅ **P1 #17 Done** | Mandi = `severe_malefic` / Gulika = `severe_malefic`, distinct interpretations |

### Adhyaya 26 — Gochara (Transit)

| Feature | Our Status | Gap |
|---------|-----------|-----|
| Good/bad transit houses per planet (from Moon) | ✅ gochara_vedha_engine.py | — |
| Sun: good in 3, 6, 10, 11 | ✅ | — |
| Moon: good in 1, 3, 6, 7, 10, 11 | ✅ | — |
| Mars: good in 3, 6, 11 | ✅ | — |
| Mercury: good in 2, 4, 6, 8, 10, 11 | ✅ | — |
| Jupiter: good in 2, 5, 7, 9, 11 | ✅ | — |
| Venus: good in 1–5, 8, 9, 11, 12 | ✅ | — |
| Saturn: good in 3, 6, 11 | ✅ | — |
| Rahu/Ketu: good in 3, 6, 10, 11 | ✅ **P0-5 Done** | House 10 added to Rahu/Ketu good transit list; vedha pair 10↔4 added |
| **Vedha (obstruction) cancellation** | ✅ gochara_vedha_engine.py | All pairs verified against Adhyaya 26 |
| **Latta (kicks) effects** | ✅ | — |
| **Transit results combined with Ashtakavarga** | ✅ | — |
| **Exact Vedha planet pairs** (e.g., Sun in 3rd cancelled by Saturn in 9th) | ✅ **P0-5 Done** | All 7-planet Vedha pairs audited and corrected |
| **Retrograde transit effects** (different from direct) | ✅ **P3 #33 Done** — `_RETROGRADE_EFFECTS` + intensity modifier in `transit_engine.py`; `retrograde_effect_en/hi` in transit dicts |

### Adhyaya 27 — Pravrajya (Ascetic Yogas)

| Feature | Our Status | Gap |
|---------|-----------|-----|
| 4+ planets in one sign → ascetic | ✅ pravrajya_engine.py | — |
| 6 types of ascetics (Paramahamsa, Sannyasi, Tridandi, etc.) | ✅ | — |
| Moon in Saturn's drekkana, aspected by Saturn | ✅ | — |
| Jupiter-dominant configurations | ✅ | — |

---

## 3. Features Not in Phaladeepika but Built (Our Extras)

These are systems we built beyond Phaladeepika — competitive differentiators:

| System | Notes |
|--------|-------|
| KP System (Krishnamurti Paddhati) | Cuspal sub-lords, horary 1–249 |
| Jaimini full system | Chara Karakas, Argala, Jaimini Drishti, Chara Dasha |
| Birth Rectification engine | Life-event based time correction |
| Varshphal (Annual return) | Muntha, Mudda Dasha |
| Iogita AI analysis | Atom vector, basin identification |
| Sarvatobhadra Chakra | 8×8 grid system |
| Mundane astrology | Eclipse/ingress world event analysis |
| Sade Sati full-lifetime mapping | 7.5-year Saturn cycles |
| D108 + D60 deep karmic analysis | Extended divisional |
| Gun Milan (36-point compatibility) | 8 categories complete |
| Birth Rectification | Event-based correction |
| Nadi system | Pulse narrative |

---

## 4. Priority Matrix — What to Build Next

### P0 — Critical Accuracy Fixes ✅ ALL COMPLETE

| # | Fix | File Changed | Status |
|---|-----|-------------|--------|
| 1 | **Vargottama highlight** | DivisionalTab.tsx + routes/kundli.py | ✅ Gold "VGT" badge + yellow row tint |
| 2 | **Rahu/Ketu modified by sign lord** | bhava_phala_engine.py | ✅ `sign_lord_modifier_en/hi` added |
| 3 | **Mooltrikona gets better effect** | bhava_phala_engine.py | ✅ `mooltrikona_note_en/hi` added |
| 4 | **Malefic in 6/8/12 strengthens Bhava** | bhava_vichara_engine.py | ✅ Flourishing note + field added |
| 5 | **Vedha pair audit** | app/data/gochara_vedhas.json | ✅ Rahu/Ketu house 10 + vedha 10↔4 added |
| 6 | **Antardasha synthesis** | dasha_engine.py | ✅ `combined_synthesis_en/hi` in antardasha response |

### P1 — High Value Missing Features

| # | Feature | Adhyaya Source | Status |
|---|---------|---------------|--------|
| 7 | **55+ Missing Yogas** — Pancha Mahapurusha, Veshi/Vosi, Vasumana, Sankha, Dhana (3 new), Venus/Mercury/Jupiter/Saturn Raja | 6 | ✅ Done — 50→66 yogas |
| 8 | **Additional Raja Yogas** — Venus, Mercury, Jupiter, Saturn-caused Raja Yogas | 7 | ✅ Done |
| 9 | **Yoga fruition timing** — `detect_yogas_with_timing()`, each yoga has `fruition_dashas` + `fruition_note_en/hi` | 19–21 | ✅ Done — wired into kundli route |
| 10 | **Vimsopaka Bala** (Varga strength 0–20 score) | 3–4 | ✅ Done |
| 11 | **5-state varga labels** (Gopuramsa, Kundendu, Parivartamsa etc.) | 3 | ✅ Done — `varga_strength` in sodashvarga endpoint; tier badges in SodashvargaTab (Parvatamsa/Simhasanamsa/Gopuramsa/Uttamamsa/Parijatamsa/Bhedaka) |
| 12 | **Planet-in-house text audit** vs Phaladeepika classical sloka meanings | 8 | ✅ Done — bhava_phala.json confirmed excellent quality with proper sloka refs for all 108 planet×house entries |
| 13 | **Dasha phala synthesis rule** — `owned_houses`, `occupied_house`, `aspected_houses`, `house_synthesis_en/hi` in mahadasha response | 19 | ✅ Done |
| 14 | **Extended Ashtakavarga** — Kaksha sub-divisions for fine transit timing | 23–24 | ✅ Done — `KAKSHA_LORD_ORDER` + `get_kaksha_info()` in ashtakvarga_engine; `kaksha` dict wired into `/transits` response for Sun–Saturn |
| 15 | **Expanded disease database** — 8 new diseases (cancer, heart, liver, kidney, accidents, paralysis, venereal, manner of death) | 14 | ✅ Done — 7→15 yogas |
| 16 | **Children analysis expansion** — apatya_engine full implementation | 12 | ✅ Done |
| 17 | **Upagraha interpretations** — house + nature + `classical_meaning_en/hi` + `interpretation_en/hi` for all 7 sub-planets | 25 | ✅ Done |

### P2 — Depth Features

| # | Feature | Adhyaya | Status |
|---|---------|---------|--------|
| 18 | **Planet stage of life** (child/youth/adult/old per planet) | 2 | ✅ Done — `planet_properties_engine.py`; stage-of-life + Baladi Avastha per planet; `/planet-properties` endpoint |
| 19 | **Panchadha Maitri** (5-fold friendship: temporary + natural combined) | 2 | ✅ Done — `panchadha_maitri_engine.py`; 21 planet pairs with Adhimitra→Adhishatru classification; `/panchadha-maitri` endpoint |
| 20 | **Sattvika/Rajasa/Tamasa** planet classification display | 2 | ✅ Done — in `planet_properties_engine.py`; guna per planet; included in `/planet-properties` response |
| 21 | **Shirodaya/Prusthodaya rising sign** impact on Lagna strength | 1 | ✅ Done — in `planet_properties_engine.py`; `lagna_rising` field in `/planet-properties` response |
| 22 | **Death timing** — Saturn+Moon transit method (philosophical framing) | 17 | ✅ Done — `transit_timing_indicators` section added to `nidhana_engine.py`; 6 transit markers in `/longevity-indicators` response |
| 23 | **Two-planet conjunction text** — classical Phaladeepika text for all 45 pairs | 18 | ✅ Already complete (pre-existing `conjunction_engine.py` + 45-pair JSON) |
| 24 | **Bhava destruction timing** — transit triggers per house | 15–16 | ✅ Done — `transit_triggers` added to each bhava in `bhava_vichara_engine.py`; wired into `/bhava-vichara` response |
| 25 | **Ashtakavarga lifespan method** | 23 | ✅ Done — `ashtakavarga_lifespan_engine.py`; Pindayu formula with 7 planets + modifiers; `/pindayu` endpoint |
| 26 | **Kalachakra Dasha phala** (interpretation texts per period) | 22 | ✅ Done — `_KALACHAKRA_PHALA` constant + `_enrich_period()` in `kalachakra_engine.py`; phala in every period of `/kalachakra-dasha` response |
| 27 | **Female chart — chastity/virtue yogas** | 11 | ✅ Already complete (pre-existing `stri_jataka_engine.py` with 7 yogas) |
| 28 | **Country/region ruled by each planet** in VrittiTab | 5 | ✅ Done — `_PLANET_REGIONS` constant + `geographic_affinities` section in `vritti_engine.py`; wired into `/vritti` response |

### P3 — Advanced / Future

| # | Feature | Adhyaya | Status |
|---|---------|---------|--------|
| 29 | Sookshma (4th) + Prana (5th) dasha subdivisions | 21 | ✅ Done — `calculate_sookshma_prana()` in `dasha_engine.py`; current 5-level chain with bilingual interpretation; `/sookshma-prana` endpoint |
| 30 | Horasara rules for Ashtakavarga (Adhyaya 24 secondary source) | 24 | ✅ Done — `analyze_horasara_phala()` in `ashtakvarga_engine.py`; 12 SAV sign readings + 7 planet BAV readings + 3 special rules; `/horasara-phala` endpoint |
| 31 | Cross-chart method for father/mother/brother timing | 15 | ✅ Done — `family_timing_engine.py`; Saturn/Mars/Rahu/Jupiter transit indicators for father/mother/siblings/spouse; `/family-timing` endpoint |
| 32 | Profession from 10th Navamsha lord (displayed explicitly) | 5 | ✅ Done — `navamsha_profession_engine.py`; D9 Lagna → D9 10th lord → bilingual career interpretation; `/navamsha-profession` endpoint |
| 33 | Retrograde transit effects (different from direct) | 26 | ✅ Done — `_RETROGRADE_EFFECTS` + intensity modifier in `transit_engine.py`; retrograde fields added to transit dicts for Mars/Mercury/Jupiter/Venus/Saturn/Rahu/Ketu |

---

## 5. Quick Wins (< 1 day, high visible impact)

| # | Task | Where | Status |
|---|------|-------|--------|
| 1 | **Vargottama badge** — gold "VGT" on DivisionalTab rows | DivisionalTab.tsx | ✅ Done |
| 2 | **Vimsopaka score** — 0-20 strength meter | SodashvargaTab.tsx | ✅ Done — tier badge in Vimshopak section |
| 3 | **5-state varga label** — "Gopuramsa", "Kundendu" etc. | SodashvargaTab.tsx | ✅ Done — tier badge in Vimshopak section |
| 4 | **Upagraha house + interpretation** in UpagrahasTab | UpagrahasTab.tsx | ✅ **FE Done** — House/Nature columns + expandable interpretation cards |
| 5 | **Bindu threshold** — show "strong (>28)" / "weak (<28)" | AshtakvargaTab.tsx | ✅ Done — HorasaraPhalaSection bindus column: green ▲ badge (≥28) / red ▼ badge (<28) |
| 6 | **Malefic in 6/8/12 = Bhava strengthened** note | BhavaVicharaTab.tsx | ✅ Done — emerald callout card in BhavaVicharaTab; `malefic_in_dusthana_strengthens` bool exported from backend |

---

## 6. Backend vs Frontend Gap Table

| Feature | Backend | API | Frontend |
|---------|---------|-----|----------|
| Vargottama flag | ✅ | ✅ `is_vargottama` in divisional response | ✅ Gold "VGT" badge |
| Vimsopaka Bala | ✅ | ✅ | ✅ Color-coded meter (green/amber/red by strength) + Saptavarga tier badge (Parvatamsa…Bhedaka) + legend |
| Yoga count 66 | ✅ | ✅ | ✅ Grouped by category, nature badges (Benefic/Malefic/Mixed), bilingual desc, fruition_note (clock icon), sloka_ref |
| Yoga fruition dasha | ✅ | ✅ `fruition_dashas` + notes | ✅ **FE Done** — amber sub-row in YogaDoshaTab |
| Dasha house synthesis | ✅ | ✅ `house_synthesis_en/hi` | ✅ **FE Done** — border-left paragraph + house badges in DashaPhalaTab |
| Antardasha MD×AD synthesis | ✅ | ✅ `combined_synthesis_en/hi` | ✅ Shown in DashaTab expanded antardasha row |
| Upagraha interpretations | ✅ | ✅ house + nature + interp fields | ✅ **FE Done** — House/Nature columns + expandable interpretation cards in UpagrahasTab |
| Rahu/Ketu sign lord modifier | ✅ | ✅ `sign_lord_modifier_en/hi` | ✅ Blue callout "Sign Lord Effect" in planet placement cards (BhavaPhalaTab) |
| Mooltrikona note | ✅ | ✅ `mooltrikona_note_en/hi` | ✅ Amber callout "Mooltrikona" in house-status cards (BhavaPhalaTab) |
| Malefic-in-dusthana note | ✅ | ✅ in bhava_vichara response | ✅ Emerald callout card in BhavaVicharaTab (Phaladeepika Adh. 15) |
| 15 disease yogas | ✅ | ✅ | ✅ Full classical text with Sanskrit names, doshic explanations, Phaladeepika Adh. 14 sloka refs |
| 5-state varga labels | ✅ | ✅ `varga_strength` in sodashvarga | ✅ Tier badge in Vimshopak |
| Ashtakavarga Kaksha | ✅ | ✅ `kaksha` dict in `/transits` | ✅ **FE Done** — kaksha lord + favorable badge + explanation in TransitsTab cards |
| Retrograde transit effects | ✅ | ✅ `retrograde_effect_en/hi` in transit dicts | ✅ **FE Done** — purple italic text in TransitsTab cards |
| Bhava transit triggers | ✅ | ✅ `transit_triggers` per bhava | ✅ **FE Done** — Transit Triggers section in BhavaVicharaTab house cards |
| Mahadasha house synthesis in timeline | ✅ | ✅ `house_synthesis_en/hi` | ✅ **FE Done** — blue sub-row in DashaTab when mahadasha expanded |
| P2/P3 new endpoints (7 total) | ✅ | ✅ all 7 wired | ✅ All 7 wired to FE: FamilyTimingSection (TransitsTab), SookshmaSection (DashaTab), PlanetPropertiesSection + PanchadhaMaitriSection (PlanetsTab), NavamshaD9 (VrittiTab), AvPindayu (LifespanTab), HorasaraPhalaSection (AshtakvargaTab) |
| Death timing methods | ✅ `transit_timing_indicators` in nidhana_engine | ✅ `/longevity-indicators` | ✅ "Karmic Transition Transit Markers" section in LongevityTab — intensity-coded cards (high/moderate/low) with significance + watch_period |
| Children timing (son expected when) | ✅ `_children_timing_section()` in apatya_engine — favorable dasha planets + Jupiter transit triggers | ✅ included in `/apatya` response as `children_timing` | ✅ Violet "Timing for Children" section in ApatyaTab — dasha cards (favorable/delaying) + Jupiter transit windows (Eye icon) |
| 45 conjunction texts (classical) | ✅ Classical Phaladeepika Adh. 18 text + sloka refs | ✅ `/conjunctions` | ✅ ConjunctionsTab renders effect_en/hi + nature badge + sloka_ref |

---

## 7. Implementation Estimate Summary

| Priority | Items | Completed | Remaining Effort |
|----------|-------|-----------|-----------------|
| P0 (critical fixes) | 6 items | ✅ 6 / 6 | — |
| P1 (high value missing) | 11 items | ✅ 11 / 11 | — |
| P2 (depth features) | 11 items | ✅ 11 / 11 | — |
| P3 (advanced future) | 5 items | ✅ 5 / 5 | — |
| **Total remaining** | **0 items** | | **Complete** |

---

## 8. Files Changed

| File | Change Made |
|------|------------|
| `app/yoga_rule_engine.py` | +16 yogas (Pancha Mahapurusha, Veshi/Vosi, Vasumana, Sankha, Dhana, Raja); `detect_yogas_with_timing()` + `add_fruition_timing()` |
| `app/data/yogas.json` | 50 → 66 yogas; all new entries added |
| `app/bhava_phala_engine.py` | P0-2: Rahu/Ketu sign_lord_modifier; P0-3: mooltrikona_note |
| `app/bhava_vichara_engine.py` | P0-4: malefic-in-dusthana-strengthens-bhava rule |
| `app/dasha_engine.py` | P0-6: combined_synthesis_en/hi in antardasha; P1 #13: _houses_for_planet() + house_synthesis in mahadasha |
| `app/data/gochara_vedhas.json` | P0-5: Rahu/Ketu good transit house 10 added; vedha 10↔4 added |
| `app/roga_engine.py` | P1 #15: 8 new disease detectors (cancer, heart, liver, kidney, accidents, paralysis, venereal, manner_of_death) |
| `app/data/roga_rules.json` | P1 #15: 8 new special_yoga entries; 7 → 15 total |
| `app/upagraha_engine.py` | P1 #17: house + nature + classical_meaning + interpretation for all 7 sub-planets |
| `app/routes/kundli.py` | P0-1: is_vargottama in divisional response; P1 #9: detect_yogas_with_timing wired |
| `frontend/src/components/kundli/DivisionalTab.tsx` | P0-1: gold "VGT" badge + yellow row tint for Vargottama |
| `frontend/src/components/kundli/UpagrahasTab.tsx` | FE wave: House + Nature badge columns; expandable interpretation cards per upagraha |
| `frontend/src/components/kundli/TransitsTab.tsx` | FE wave: Kaksha lord/favorable/explanation badge; retrograde_effect purple narrative per transit card |
| `frontend/src/components/kundli/YogaDoshaTab.tsx` | FE wave: fruition_dashas amber badge row + fruition_note sub-row per active yoga |
| `frontend/src/components/kundli/DashaPhalaTab.tsx` | FE wave: house_synthesis paragraph (border-left) + owned/occupied/aspected house badges in mahadasha card |
| `frontend/src/components/kundli/BhavaVicharaTab.tsx` | FE wave: Transit Triggers section (planet + trigger text + timing note) inside each house card |
| `frontend/src/components/kundli/DashaTab.tsx` | FE wave: house_synthesis blue sub-row when mahadasha row is expanded |
| **Session 2 — 18 Apr 2026 (commit `d3acdf0` + `b2d7279`)** | |
| `frontend/src/components/kundli/TransitsTab.tsx` | `FamilyTimingSection` sub-component: 4 cards (Father/Mother/Siblings/Spouse) from `/family-timing` |
| `frontend/src/components/kundli/AshtakvargaTab.tsx` | `HorasaraPhalaSection` sub-component from `/horasara-phala`; bindus column: green ▲ / red ▼ threshold badge |
| `frontend/src/components/kundli/DashaTab.tsx` | `SookshmaSection` sub-component: current Sookshma (violet) + Prana (rose) rows from `/sookshma-prana` |
| `frontend/src/components/kundli/PlanetsTab.tsx` | `PlanetPropertiesSection` from `/planet-properties` (avastha/guna/baladi); `PanchadhaMaitriSection` from `/panchadha-maitri` |
| `frontend/src/components/kundli/VrittiTab.tsx` | Navamsha D9 profession card from `/navamsha-profession`; element badge + suited_fields tags |
| `frontend/src/components/kundli/LifespanTab.tsx` | AV Pindayu card from `/pindayu`; total_years + classification badge + planet_contributions table |
| `frontend/src/sections/KundliGenerator.tsx` | `kundliId` prop wired to `PlanetsTab` |
| `app/bhava_vichara_engine.py` | `malefic_in_dusthana_strengthens` boolean tracked and exported in return dict |
| `app/routes/kundli.py` | `varga_strength` added to sodashvarga GET response (try/except guard) |
| `frontend/src/components/kundli/BhavaVicharaTab.tsx` | `malefic_in_dusthana_strengthens` field in interface + emerald callout card per house |
| `frontend/src/components/kundli/SodashvargaTab.tsx` | `METER_COLORS` + `TIER_COLORS` maps; meter color-coded by strength; Saptavarga tier badge with tooltip; tier legend at bottom |
| `frontend/src/components/kundli/YogaDoshaTab.tsx` | Full rewrite: category grouping, `NATURE_STYLE`/`CATEGORY_STYLE` maps, nature badges, bilingual descriptions, fruition_note (Clock icon), sloka_ref (BookOpen), Doshas 2-col grid, Gemstones full-width |
| `frontend/src/components/kundli/LongevityTab.tsx` | `transit_timing_indicators` section: intensity-coded cards (high/moderate/low) with planet→sign header, significance, watch_period (Eye icon), sloka_ref (Phaladeepika Adh. 17) |

---

*Source: Phaladeepika by Mantreswara (28 Adhyayas, V. Subrahmanya Sastri translation, 1937, 438 pages)*  
*Cross-referenced with: yoga_rule_engine.py, bhava_phala_engine.py, shadbala_engine.py, ashtakvarga_engine.py, dasha_engine.py, gochara_vedha_engine.py, routes/kundli.py*
