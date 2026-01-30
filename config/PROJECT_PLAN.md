# Finance Locale: BP-DGCL Reconciliation Project Plan

## Problem Statement
Reconcile Budget Primitifs (BP - voted budgets by local authorities) with DGCL government agency recaps to understand and calculate deficits of French local public authorities. The project focuses on extracting, harmonizing, and merging budget data from two distinct sources, then analyzing various combinations of columns to match BP data against DGCL data.

## Scope
- **Focus**: Regions (Régions) only
- **Year**: 2024 (initial focus)
- **Output Format**: CSV files
- **Primary Language**: Python (pandas, pdfplumber, PyPDF2, etc.)
- **Final Analysis**: R code for testing column combinations

---

## Data Sources

### 1. Budget Primitifs (BP) - Regions 2024
- Location: `data\Documents BP Collectivités\[Region folders]\BP\BP2024.pdf` (or split files like BP2024_1.pdf, BP2024_2.pdf)
- Contains: Voted budgets with tables showing various financial line items
- Notes: Multiple regions with different PDF structures; some split into multiple parts

### 2. DGCL Government Agency Data
- Location: `data\DGCL\BP2024_Reg.xlsx` and similar
- Contains: Government compiled budget data for regions with official financial summaries
- Notes: Also has Comptes Administratifs (CA) files and historical data

---

## Implementation Workplan

### Phase 1: Setup & Exploration ✅
- [x] Create project directory structure:
  - `src/` - Python scripts
  - `output/` - Extracted tables and CSVs
  - `config/` - Configuration files (region list, column mappings, etc.)
  - `logs/` - Processing logs
- [x] Document all regions included in analysis
- [x] Create configuration file mapping region names to folder paths
- [x] Sample 1-2 BP PDFs (2024) to understand structure and identify key tables
- [x] Sample DGCL spreadsheet (BP2024_Reg.xlsx) to understand columns and structure
- [x] Identify which pages contain the budget summary tables in BP PDFs (reference: pages_BP_regions.txt)

### Phase 2: PDF Extraction & Processing
- [ ] Build Python script to extract specific pages from BP PDFs:
  - Input: Region folder path, year, page ranges
  - Use `PyPDF2` or `pdfplumber` to extract pages
  - Output: Individual region PDFs or temporary page PDFs
- [ ] Merge extracted pages into consolidated PDFs per region-year combination
  - Input: Extracted page PDFs
  - Use `PyPDF2.PdfWriter` to merge
  - Output: `output/BP_2024_[RegionName]_consolidated.pdf`
- [ ] Build PDF table detection & parsing script:
  - Use `pdfplumber` to extract tables from PDFs
  - Parse table structure (identify column headers, data rows)
  - Output: JSON or pickle with raw extracted tables (for debugging)

### Phase 3: Table Harmonization & CSV Creation
- [ ] Document BP table structure for 2024:
  - Identify consistent column names across regions
  - Map region-specific variations to standardized names
  - Create mapping file: `config/bp_column_mappings.csv`
- [ ] Build harmonization script:
  - Input: Extracted tables from Phase 2
  - Standardize column names using mapping file
  - Handle missing/extra columns across regions
  - Clean data (remove formatting, convert to proper types)
  - Output: `output/BP_2024_harmonized.csv` (single consolidated file with region identifier)

### Phase 4: DGCL Data Processing
- [ ] Read DGCL spreadsheets (BP2024_Reg.xlsx):
  - Identify relevant sheets and columns
  - Document DGCL column structure and meaning
  - Create mapping file: `config/dgcl_column_mappings.csv`
- [ ] Build DGCL parsing script:
  - Extract relevant columns
  - Create standardized identifier to match with BP data
  - Output: `output/DGCL_2024_regions.csv`

### Phase 5: Data Integration
- [ ] Build merge script:
  - Input: `BP_2024_harmonized.csv` and `DGCL_2024_regions.csv`
  - Match on region identifier (ensure exact matches or create mapping if names differ)
  - Merge DGCL columns as new columns to BP dataset
  - Output: `output/BP_DGCL_2024_merged.csv`
- [ ] Document any unmatched regions or data quality issues
- [ ] Create data quality report: summary statistics, missing values, etc.

### Phase 6: Testing & Validation
- [ ] Validate merged dataset:
  - Check for completeness (all regions present)
  - Check for missing values
  - Verify data types and formats
- [ ] Create sample R script template:
  - Load CSV from Phase 5
  - Demonstrate basic column combinations (e.g., sum of BP columns vs. DGCL totals)
  - Show how to test various arithmetic combinations
- [ ] Document key findings and any data inconsistencies

### Phase 7: Documentation & Cleanup
- [ ] Create README documenting:
  - How to run the pipeline
  - Column definitions and mappings
  - Known issues and assumptions
  - Year-by-year expansion notes
- [ ] Add error handling and logging throughout scripts
- [ ] Create requirements.txt for Python dependencies
- [ ] Clean up intermediate files (keep only final CSVs and scripts)

---

## Key Assumptions & Notes

1. **Page ranges**: Using `pages_BP_regions.txt` as reference for which pages to extract from each region's BP PDF
2. **Region matching**: Assuming region names in BP folders match those in DGCL files; will create mapping if needed
3. **Table format**: BP tables likely have hierarchical structure (budget codes/classifications); will need to preserve hierarchy
4. **Multiple regions**: Each region may have different PDF structure/table formats requiring custom parsing per region
5. **2024 focus**: Pipeline designed for 2024 but should be extendable to other years by modifying year parameter
6. **Final R analysis**: Separate from Python pipeline; user will create R code to test column combinations

---

## Dependencies to Install
- pandas
- pdfplumber (or PyPDF2)
- openpyxl (for Excel files)
- pyyaml (for config files)

---

## Success Criteria
- ✅ All 11 regions' 2024 BP data successfully extracted and parsed
- ✅ Single harmonized CSV with all BP columns created
- ✅ DGCL 2024 data extracted and merged
- ✅ Final merged CSV with region identifier and all columns
- ✅ Documentation complete with column mappings and data quality notes
- ✅ Ready for R analysis of column combinations

---

## Regions in Scope

1. Auvergne-Rhône-Alpes
2. Bourgogne-Franche-Comté
3. Bretagne
4. Centre-Val de Loire
5. Grand Est
6. Hauts-de-France
7. Île-de-France
8. Normandie
9. Nouvelle-Aquitaine
10. Occitanie
11. Provence-Alpes-Côte d'Azur
