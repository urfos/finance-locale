# Phase 1: Exploration & Setup - Findings

## Overview
This document captures findings from Phase 1 exploration of BP PDF structures and DGCL data formats.

## Regions Included (11 official French regions)
1. **Auvergne-Rhône-Alpes** - folder: Auvergne-Rhone-Alpes (pages 17-29)
2. **Bourgogne-Franche-Comté** (pages 271-283)
3. **Bretagne** (pages 19-31)
4. **Centre-Val de Loire** - folder: Centre (pages 31-43)
5. **Grand Est** (pages 17-29)
6. **Hauts-de-France** - folder: HdF (pages 25-37)
7. **Île-de-France** - folder: IdF (pages 39-51)
8. **Normandie** (pages 23-35)
9. **Nouvelle-Aquitaine** (pages 28-40)
10. **Occitanie** (pages 23-35)
11. **Provence-Alpes-Côte d'Azur** - folder: PACA (pages 31-38)

**Note**: Other folders in `Documents BP Collectivités` are departments, cities, or metropolitan areas (not regions).

## Data Files Available

### BP (Budget Primitifs) PDFs
- Location: `data/Documents BP Collectivités/[Region]/BP/`
- Years available: 2018-2025 (focus: 2024)
- Format: PDF, typically 2-5MB each
- Content: Voted budgets with detailed line items and tables

### DGCL Government Recaps
- Location: `data/DGCL/`
- Files for regions: `BP2024_Reg.xls`, `CA2024_Reg.xlsx` (and historical years)
- Files for departments: `BP2024_Dep.xls`, `CA2024_Dep.xlsx`
- Content: Government-compiled budget data with standardized structure

## Reference Data
- `pages_BP_regions.txt`: Maps each region to the page ranges containing budget summary tables
  - These page ranges indicate where the main budget tables are located within PDFs
  - Critical for Phase 2 (PDF extraction)

## Next Steps (Phase 2)
1. Run exploration scripts to understand exact table structures:
   - `src/01_explore_bp_pdfs.py` - Examine table layouts in sample BP PDFs
   - `src/02_explore_dgcl_data.py` - Examine sheet structure in DGCL files
2. Document column names and data types
3. Identify common elements across regions
4. Create column mapping configuration files

## Setup Complete ✓
- Project directory structure created
- Git repository initialized and connected to GitHub
- Regions configuration file created: `config/regions_config.yaml`
- Exploration scripts created
- Ready for Phase 2: PDF extraction and analysis
