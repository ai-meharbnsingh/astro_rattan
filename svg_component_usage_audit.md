# SVG Chart Component Usage Audit (PDF)

Generated: 2026-04-21

## Goal

Render report-quality charts in the Kundli PDF using SVG-based vector rendering (no blurry rasterization), with consistent sizing and no clipping.

## Implementation

- SVG generator: `app/reports/kundli_report.py:_north_indian_chart_svg(...)`
- SVG → PDF vector render path: `fpdf2` SVG converter via:
  - `fpdf.svg.SVGObject(...)`
  - `SVGObject.transform_to_rect_viewport(...)`
  - `pdf.draw_path(...)`
- Fallback: if SVG rendering fails, the report falls back to the existing FPDF primitive drawer:
  - `app/reports/kundli_report.py:_draw_north_indian_chart(...)`

## Sections using SVG charts

PDF assembler file: `app/reports/kundli_report.py`

- Core charts
  - `ReportAssembler.render_core_charts()`:
    - Lagna / D1 chart
    - Moon chart
    - Navamsha / D9 chart
  - Chart calls: `_draw_north_indian_chart_svg(...)`

- Bhava chart
  - `ReportAssembler.render_bhava_analysis()`:
    - Bhava (Sripati) chart

- Divisional charts
  - `ReportAssembler.render_divisional_charts()`:
    - D2/D3/... (where available)

- Ashtakavarga summary chart block
  - `ReportAssembler.render_ashtakavarga()`:
    - SAV bindu chart

- Varshphal
  - `ReportAssembler.render_varshphal()`:
    - Annual chart

## Sizing & viewBox handling

- The SVG uses `viewBox="0 0 400 400"`.
- The PDF renderer scales the SVG into an exact square (`w == h == size` in document units) via:
  - `SVGObject.transform_to_rect_viewport(pdf.k, size * pdf.k, size * pdf.k, ignore_svg_top_attrs=True)`
  - This is required because `transform_to_rect_viewport()` expects viewport width/height in PDF points, while `pdf.k` is points-per-document-unit.
- Title/caption is rendered by the PDF layer (text), not inside the SVG, to avoid font/layout drift.

## Known limitations (current state)

- SVG charts currently render:
  - house numbers
  - planet abbreviations per house
- They do not yet render:
  - zodiac sign icons/images (intentionally avoided: external assets + embedding complexity)
  - per-planet status flags (retro/combust markers) inside the SVG (can be added later using existing payload fields)
