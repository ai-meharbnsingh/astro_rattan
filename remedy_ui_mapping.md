# Remedy UI Mapping

This document maps the backend API response fields to the frontend UI components in the Remedies section.

## 1. General Remedies (`GeneralRemedies.tsx`)

| Backend Field (JSON) | Frontend Component / Label | Purpose |
|:---|:---|:---|
| `category` | Badge (Upper Left) | The name of the planet or dosha being addressed. |
| `problem_detected` | "Problem:" label | Plain English explanation of the chart affliction. |
| `why_it_matters` | Description below problem | Explains the impact of this affliction on life. |
| `remedies[]` | Grid Cards | List of specific actions to take. |
| `rem.title` | Card Header | Name of the remedy (e.g., "Shani Mantra"). |
| `rem.what_to_do` | "What to do" section | The core action or ritual. |
| `rem.how_to_do` | "How to do" section | Step-by-step instructions. |
| `rem.when_to_do` | "When" badge | Best day or time for the remedy. |
| `rem.frequency` | "Frequency" badge | How often to perform the action. |
| `rem.expected_benefit` | "Expected Benefit" footer | Result expected from consistent practice. |
| `rem.source_label` | Icon + Text Footer | Attribution to tradition (e.g., "Narad Puran"). |

## 2. Yearly Remedies (`RemediesTab.tsx`)

| Backend Field (JSON) | Frontend Component / Label | Purpose |
|:---|:---|:---|
| `category` | Header Title | The specific time-based influence (e.g., "Sade Sati"). |
| `based_on` | Upper Right Badge | The timing trigger (e.g., "Active Mahadasha in 2026"). |
| `summary` | Text below header | Why these remedies are important for this specific year. |
| `remedies[]` | Grid Cards | Same as General Remedies cards. |

## 3. Translation Mapping
The system uses the `language` prop to toggle between English and Hindi text. If specific Hindi fields (`_hi`) are missing from the source, the system defaults to English to maintain data integrity.
