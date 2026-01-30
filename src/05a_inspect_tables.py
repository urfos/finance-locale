#!/usr/bin/env python3
"""
Diagnostic script to inspect table structure in BP PDFs
Helps understand what tables exist and their structure before parsing
"""

import pdfplumber
from pathlib import Path
import sys

# Configuration
OUTPUT_DIR = Path(__file__).parent.parent / "output"
YEAR = "2024"

def inspect_pdf_tables(pdf_path, region_name):
    """
    Inspect all tables on first page of PDF
    Print detailed structure information
    """
    
    print("\n" + "="*80)
    print(f"REGION: {region_name}")
    print(f"FILE: {pdf_path.name}")
    print("="*80)
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            if len(pdf.pages) == 0:
                print("ERROR: PDF has no pages")
                return
            
            # Inspect first page
            page = pdf.pages[0]
            print(f"\nPage 1 of {len(pdf.pages)} total pages")
            print(f"Page dimensions: {page.width} x {page.height}")
            
            # Extract tables
            tables = page.extract_tables()
            
            if not tables:
                print("WARNING: No tables found on first page")
                return
            
            print(f"\nFound {len(tables)} table(s) on first page\n")
            
            # Inspect each table
            for table_idx, table in enumerate(tables):
                print("-" * 80)
                print(f"TABLE #{table_idx}")
                print("-" * 80)
                
                if not table or len(table) == 0:
                    print("  (empty table)")
                    continue
                
                num_rows = len(table)
                num_cols = len(table[0]) if table else 0
                
                print(f"Dimensions: {num_rows} rows x {num_cols} columns")
                
                # Check if all rows have same column count
                col_counts = [len(row) for row in table]
                if len(set(col_counts)) > 1:
                    print(f"WARNING: Inconsistent column counts: {set(col_counts)}")
                
                # Print first row (potential header)
                print("\nFirst row (potential header):")
                if table:
                    for col_idx, cell in enumerate(table[0]):
                        cell_str = str(cell) if cell else "(empty)"
                        # Truncate long cells and show if multi-line
                        if '\n' in cell_str:
                            lines = cell_str.split('\n')
                            print(f"  Col {col_idx}: {lines[0][:50]}... [{len(lines)} lines]")
                        else:
                            print(f"  Col {col_idx}: {cell_str[:60]}")
                
                # Print first 3 data rows
                print("\nFirst 3 data rows:")
                for row_idx in range(1, min(4, num_rows)):
                    print(f"\n  Row {row_idx}:")
                    row = table[row_idx]
                    for col_idx, cell in enumerate(row):
                        cell_str = str(cell) if cell else "(empty)"
                        # Show if multi-line
                        if '\n' in cell_str:
                            lines = cell_str.split('\n')
                            print(f"    Col {col_idx}: {lines[0][:50]}... [{len(lines)} lines]")
                        else:
                            print(f"    Col {col_idx}: {cell_str[:60]}")
                
                # Check for multi-line cells in entire table
                multiline_count = 0
                for row in table:
                    for cell in row:
                        if cell and '\n' in str(cell):
                            multiline_count += 1
                
                if multiline_count > 0:
                    print(f"\n⚠ WARNING: {multiline_count} cells contain embedded newlines")
                
                print()
    
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

def main():
    """
    Inspect tables from sample PDFs to understand structure
    """
    
    print("="*80)
    print("TABLE STRUCTURE DIAGNOSTIC")
    print("="*80)
    
    # Test on first region from each group
    test_regions = ["Auvergne-Rhone-Alpes", "Bretagne"]
    
    # Find test PDFs
    test_pdfs = []
    for region in test_regions:
        pdf_file = OUTPUT_DIR / f"BP_{YEAR}_{region}_extracted.pdf"
        if pdf_file.exists():
            test_pdfs.append((pdf_file, region))
        else:
            print(f"WARNING: PDF not found for {region}")
    
    if not test_pdfs:
        print("ERROR: No test PDF files found")
        return
    
    print(f"\nInspecting {len(test_pdfs)} region(s)...\n")
    
    for pdf_path, region in test_pdfs:
        inspect_pdf_tables(pdf_path, region)
    
    print("\n" + "="*80)
    print("DIAGNOSTIC COMPLETE")
    print("="*80)
    print("\nNext steps:")
    print("1. Review table structures above")
    print("2. Identify which table(s) contain target data")
    print("3. Define extraction strategy based on findings")

if __name__ == "__main__":
    main()
