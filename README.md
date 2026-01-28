# Finance Locale: BP-DGCL Reconciliation

Understanding how deficits of French local public authorities can be calculated from budgets they vote (Budget Primitifs - BP) by reconciling them with government agency recaps (DGCL).

## Project Overview

This project aims to:
1. Extract relevant tables from Budget Primitifs (BP) PDFs voted by regional authorities
2. Merge extracted data into harmonized datasets
3. Reconcile with DGCL (Direction Générale des Collectivités Locales) government compilations
4. Test various combinations of BP columns to match DGCL figures

## Current Focus
- **Geography**: French Regions (Régions)
- **Year**: 2024 (expandable to other years)
- **Output Format**: CSV files for R analysis

## Directory Structure

```
.
├── src/                 # Python scripts for data processing
├── output/              # Generated CSV files and data artifacts
├── config/              # Configuration and mapping files
├── logs/                # Processing logs
├── README.md           # This file
└── requirements.txt    # Python dependencies
```

## Data Sources (not in repo)

- **BP PDFs**: `data/Documents BP Collectivités/[Region]/BP/BP2024.pdf`
- **DGCL Spreadsheets**: `data/DGCL/BP2024_Reg.xlsx` and related files
- **Reference**: `pages_BP_regions.txt` lists page ranges for each region's budget tables

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create output directories
mkdir -p output config logs
```

## Pipeline Phases

1. **PDF Extraction**: Extract specific pages from BP PDFs
2. **Table Parsing**: Identify and extract tables from PDFs
3. **Harmonization**: Standardize column names across regions
4. **DGCL Integration**: Merge government agency data
5. **R Analysis**: Test column combinations (see final CSV)

## Usage

See individual script documentation as pipeline develops.
