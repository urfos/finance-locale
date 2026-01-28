#!/usr/bin/env python3
"""
Phase 1: Explore DGCL spreadsheet structure
Examines government agency budget data format and columns
"""

import pandas as pd
import sys
from pathlib import Path

# Configuration
DATA_DIR = Path(__file__).parent.parent / "data"
DGCL_DIR = DATA_DIR / "DGCL"

def explore_dgcl():
    """Explore DGCL spreadsheet structure"""
    
    xls_file = DGCL_DIR / "BP2024_Reg.xls"
    
    if not xls_file.exists():
        print(f"ERROR: File not found at {xls_file}")
        sys.exit(1)
    
    print(f"Exploring: {xls_file}\n")
    
    # Read all sheet names
    xls = pd.ExcelFile(xls_file)
    print(f"Sheet names ({len(xls.sheet_names)}):")
    for sheet in xls.sheet_names:
        print(f"  - {sheet}")
    
    print("\n" + "="*70)
    
    # Read first sheet to examine structure
    first_sheet = xls.sheet_names[0]
    print(f"\nExamining sheet: {first_sheet}")
    print("="*70)
    
    df = pd.read_excel(xls_file, sheet_name=first_sheet)
    
    print(f"\nDimensions: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"\nColumn names:")
    for i, col in enumerate(df.columns):
        print(f"  {i}: {col}")
    
    print(f"\nFirst 5 rows:")
    print(df.head().to_string())
    
    print(f"\nData types:")
    print(df.dtypes)
    
    print(f"\nMissing values:")
    missing = df.isnull().sum()
    for col, count in missing[missing > 0].items():
        print(f"  {col}: {count}")

if __name__ == "__main__":
    explore_dgcl()
    print("\n" + "="*70)
    print("Exploration complete")
