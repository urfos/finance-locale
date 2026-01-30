#!/usr/bin/env python3
"""
Phase 2: Parse tables from consolidated BP PDFs
Extracts tables from consolidated PDFs and saves as CSV files
One CSV per region containing all tables from that region's budget document
"""

import pdfplumber
import pandas as pd
from pathlib import Path
import sys
import re

# Configuration
OUTPUT_DIR = Path(__file__).parent.parent / "output"
YEAR = "2024"

def get_region_from_filename(filename):
    """Extract region name from filename like 'BP_2024_Auvergne-Rhone-Alpes_extracted.pdf'"""
    match = re.search(r'BP_\d{4}_(.+)_extracted\.pdf', filename)
    if match:
        return match.group(1)
    return None

def parse_tables_from_pdf(pdf_path, region_name):
    """
    Extract tables from first page of PDF only.
    - Keep only rows with multiple columns (>1)
    - Ensure all rows have same number of columns
    - Skip title lines
    """
    
    print(f"\nParsing: {region_name}")
    print(f"  Source: {pdf_path.name}")
    
    try:
        all_tables = []
        
        with pdfplumber.open(pdf_path) as pdf:
            # Process only first page
            if len(pdf.pages) == 0:
                print(f"  ERROR: PDF has no pages")
                return False
            
            page = pdf.pages[0]
            tables = page.extract_tables()
            
            if not tables:
                print(f"  WARNING: No tables found on first page")
                return False
            
            table_count = 0
            for table_idx, table in enumerate(tables):
                if not table or len(table) == 0:
                    continue
                
                # Filter rows: keep only those with multiple columns (>1)
                filtered_rows = [row for row in table if row and len(row) > 1]
                
                if len(filtered_rows) < 2:  # Need at least header + 1 data row
                    continue
                
                # Get number of columns from header
                header = filtered_rows[0]
                num_cols = len(header)
                
                # Keep only rows that match column count
                valid_rows = [header]
                for row in filtered_rows[1:]:
                    if len(row) == num_cols:
                        valid_rows.append(row)
                
                if len(valid_rows) < 2:  # Need at least header + 1 data row
                    continue
                
                # Make column names unique
                headers = valid_rows[0]
                seen = {}
                unique_headers = []
                for h in headers:
                    h_str = str(h) if h else 'Empty'
                    if h_str in seen:
                        seen[h_str] += 1
                        unique_headers.append(f"{h_str}_{seen[h_str]}")
                    else:
                        seen[h_str] = 0
                        unique_headers.append(h_str)
                
                # Create DataFrame with valid rows
                df = pd.DataFrame(valid_rows[1:], columns=unique_headers)
                
                # Add metadata columns
                df['_source_page'] = 1
                df['_source_region'] = region_name
                df['_table_index'] = table_idx
                
                all_tables.append(df)
                table_count += 1
        
        if not all_tables:
            print(f"  WARNING: No valid tables found on first page")
            return False
        
        # Combine all tables - use outer join to keep all columns
        combined_df = pd.concat(all_tables, axis=0, ignore_index=True, sort=False, join='outer')
        
        # Reorder columns: metadata first (string columns starting with _), then others
        cols = combined_df.columns.tolist()
        metadata_cols = [c for c in cols if isinstance(c, str) and c.startswith('_')]
        data_cols = [c for c in cols if not (isinstance(c, str) and c.startswith('_'))]
        combined_df = combined_df[metadata_cols + data_cols]
        
        # Save to CSV
        output_filename = f"BP_{YEAR}_{region_name}_raw_tables.csv"
        output_path = OUTPUT_DIR / output_filename
        
        combined_df.to_csv(output_path, index=False, encoding='utf-8')
        
        print(f"  ✓ Extracted {table_count} tables from first page")
        print(f"  ✓ Rows: {len(combined_df)}, Columns: {len(combined_df.columns)}")
        print(f"  ✓ Saved to: {output_filename}")
        
        return True
        
    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Parse tables from first page of extracted PDFs - TEST VERSION
    Only tests first region of each group (Auvergne-Rhone-Alpes and Bretagne)
    """
    
    print("="*70)
    print("PHASE 2: PDF TABLE PARSING - TEST MODE")
    print("="*70)
    
    # Test regions: first of each group
    test_regions = ["Auvergne-Rhone-Alpes", "Bretagne"]
    
    # Find test PDFs
    test_pdfs = []
    for pdf_file in OUTPUT_DIR.glob(f"BP_{YEAR}_*_extracted.pdf"):
        region = get_region_from_filename(pdf_file.name)
        if region in test_regions:
            test_pdfs.append(pdf_file)
    
    if not test_pdfs:
        print("ERROR: No test PDF files found")
        return False
    
    print(f"\nTesting on {len(test_pdfs)} region(s): {', '.join(test_regions)}")
    
    success_count = 0
    fail_count = 0
    
    for pdf_path in sorted(test_pdfs):
        region = get_region_from_filename(pdf_path.name)
        if region:
            if parse_tables_from_pdf(pdf_path, region):
                success_count += 1
            else:
                fail_count += 1
        else:
            print(f"WARNING: Could not extract region from {pdf_path.name}")
            fail_count += 1
    
    print("\n" + "="*70)
    print(f"Test complete: {success_count} succeeded, {fail_count} failed")
    print("="*70)
    
    return fail_count == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
