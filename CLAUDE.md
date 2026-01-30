# CLAUDE Session Notes - Finance Locale Project

**Last Updated**: 2026-01-30
**Status**: Phase 2 - PDF Table Parsing ✅ COMPLETE (10/11 regions)

## Current Task Summary

Parsing tables from Budget Primitifs (BP) PDFs complete. New parser with row expansion and R-compatible number format working on 10/11 regions.

## Parser v2 Features (05_parse_bp_tables.py)

- **Row expansion**: Multi-line PDF cells split into separate CSV rows
- **Level indicator**: `level=0` main row, `level=1` sub-items  
- **R-compatible numbers**: `3926800000.00` (no spaces, dot decimal)
- **Semicolon delimiter**: French Excel compatible
- **UTF-8 with BOM**: Proper encoding

## Parsing Results

| Region | Status | Rows |
|--------|--------|------|
| Auvergne-Rhone-Alpes | ✅ | 27 |
| Bourgogne-Franche-Comté | ✅ | 27 |
| Bretagne | ✅ | 27 |
| Centre | ✅ | 27 |
| Grand Est | ✅ | 27 |
| HdF | ❌ | Different PDF structure (1 table) |
| IdF | ✅ | 27 |
| Normandie | ✅ | 27 |
| Nouvelle-Aquitaine | ✅ | 27 |
| Occitanie | ✅ | 27 |
| PACA | ⚠️ | 1 (incomplete extraction) |

## Known Issues

### HdF (Hauts-de-France)
- PDF has different structure: only 1 table detected instead of 4
- Needs manual inspection of source PDF

### PACA
- Only 1 row extracted (should be 27)
- Table 3 structure differs from other regions

## Output Files

- `output/BP_2024_<region>.csv` - Parsed budget data (10 files)
- `output/BP_2024_<region>_extracted.pdf` - Source extracted pages (11 files)

## Technical Notes

- **Python**: miniconda 3.13.11
- **Key script**: `src/05_parse_bp_tables.py`
- **Diagnostic**: `src/05a_inspect_tables.py` for PDF structure analysis

## Next Steps

1. Investigate HdF and PACA PDF structure differences
2. Phase 3: Data harmonization across regions
3. R analysis scripts
