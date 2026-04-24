# Remedy Engine Logic (Vedic / Parashari)

This document explains the logic used in the automated remedy engine. The engine prioritizes actual chart afflictions and uses traditional Vedic remedies, including references from the Narad Puran.

## 1. Planet-Based Logic

Remedies are triggered for any planet that meets one or more of the following criteria:

### A. Weak Shadbala
- **Logic**: Each planet has a "Required Strength" (in Virupas) defined in classical texts (BPHS).
- **Trigger**: If `total_shadbala < required_strength`, a balancing remedy is suggested.
- **Goal**: To strengthen the planet's ability to deliver its positive results.

### B. Combustion (Asta)
- **Logic**: A planet is combust when it is too close to the Sun, losing its independent power.
- **Trigger**: `is_combust == True`.
- **Goal**: To pacify the intense solar influence and restore the planet's symbolic function.

### C. Debilitation (Neecha)
- **Logic**: A planet is at its weakest in its sign of debilitation.
- **Trigger**: `dignity` contains "debilitated" or "neecha".
- **Goal**: To mitigate the internal struggle or "low energy" state of that life area.

---

## 2. Dosha-Based Logic

Specific complex afflictions trigger specialized remedies:

### A. Mangal Dosha
- **Trigger**: Mars in house 1, 2, 4, 7, 8, or 12.
- **Remedy**: Focuses on pacifying Mars through Hanuman worship and behavioral discipline.

### B. Kaal Sarp Dosha
- **Trigger**: All planets hemmed between Rahu and Ketu.
- **Remedy**: Focuses on Lord Shiva to stabilize the Rahu/Ketu axis.

### C. Sade Sati
- **Trigger**: Saturn transiting the natal Moon's sign or adjacent signs.
- **Remedy**: Focuses on discipline, patience, and Shani mantras.

---

## 3. Timing-Based Logic (Yearly)

### A. Mahadasha Lord
- **Logic**: The planet currently ruling the major time period (Mahadasha) has the most significant influence on current events.
- **Remedy**: Strengthening the Dasha lord ensures smoother progress during its entire period.

### B. Varshphal (Year Lord)
- **Logic**: The ruler of the Solar Return chart (Varshesh) defines the flavor of the specific year.
- **Remedy**: Remedies for the Year Lord help overcome specific annual obstacles.

---

## 4. Narad Puran Source Layer

Wherever a remedy aligns with the guidance found in the **Narad Puran tradition**, it is explicitly labeled. This includes:
- Surya Gayatri and Surya Upasana.
- Specific planetary beej mantras.
- Rituals for pacifying Mars and Saturn.
- Dina Charya (Daily Routine) for overall vitality.

*Note: This engine intentionally excludes Lal Kitab remedies to maintain a pure Vedic/Parashari approach for this section.*
