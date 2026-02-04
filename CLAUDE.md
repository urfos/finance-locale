# CLAUDE Session Notes - Finance Locale Project

**Last Updated**: 2026-02-02
**Status**: Phase 2 - PDF Table Parsing ✅ COMPLETE (11/11 regions)

## Current Task Summary

All 11 regions successfully parsed. HdF extraction corrected (pages 30-42 instead of 25-37). Parser refactored for flexible region selection.

## Parser v2 Features (05_parse_bp_tables.py)

- **Row expansion**: Multi-line PDF cells split into separate CSV rows
- **Level indicator**: `level=0` main row, `level=1` sub-items  
- **R-compatible numbers**: `3926800000.00` (no spaces, dot decimal)
- **Semicolon delimiter**: French Excel compatible
- **UTF-8 with BOM**: Proper encoding
- **Flexible region selection**: Command-line args support (e.g., `python 05_parse_bp_tables.py HdF PACA`)

## Parsing Results

| Region | Status | Rows |
|--------|--------|------|
| Auvergne-Rhone-Alpes | ✅ | 27 |
| Bourgogne-Franche-Comté | ✅ | 27 |
| Bretagne | ✅ | 27 |
| Centre | ✅ | 27 |
| Grand Est | ✅ | 27 |
| HdF | ✅ | 27 |
| IdF | ✅ | 27 |
| Normandie | ✅ | 27 |
| Nouvelle-Aquitaine | ✅ | 27 |
| Occitanie | ✅ | 27 |
| PACA | ⚠️ | 1 (incomplete extraction) |

## Known Issues

### PACA
- Only 1 row extracted (should be 27)
- Table 3 structure differs from other regions

## Recent Fixes

### HdF (Hauts-de-France) ✅ FIXED
- **Issue**: Extraction started at page 25 (empty), but actual budget tables begin at printed "Page 25" (PDF page 30)
- **Root cause**: Page numbering mismatch (PDF internal vs. printed page numbers)
- **Solution**: Updated `regions_config.yaml` to pages_start: 30, pages_end: 42
- **Result**: HdF now extracts correctly with 27 rows, matching other regions

## Output Files

- `output/BP_2024_<region>.csv` - Parsed budget data (11 files) ✅
- `output/BP_2024_<region>_extracted.pdf` - Source extracted pages (11 files) ✅

## Technical Notes

- **Python**: miniconda 3.13.11
- **Key script**: `src/05_parse_bp_tables.py`
- **Diagnostic**: `src/05a_inspect_tables.py` for PDF structure analysis

## Next Steps

1. Investigate PACA PDF structure and fix remaining extraction issue
2. Phase 3: Data harmonization across regions
3. R analysis scripts for budget analysis
