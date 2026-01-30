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
    """Extract region name from filename like 'BP_2024_Auvergne-Rhone-Alpes_consolidated.pdf'"""
    match = re.search(r'BP_\d{4}_(.+)_consolidated\.pdf', filename)
    if match:
        return match.group(1)
    return None

def parse_tables_from_pdf(pdf_path, region_name):
    """Extract and save tables from a consolidated PDF"""
    
    print(f"\nParsing: {region_name}")
    print(f"  Source: {pdf_path.name}")
    
    try:
        all_tables = []
        page_count = 0
        table_count = 0
        
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"  Total pages: {total_pages}")
            
            for page_idx, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                
                if tables:
                    for table_idx, table in enumerate(tables):
                        if table and len(table) > 0:
                            # Convert table to DataFrame
                            # First row is usually headers
                            if len(table) > 1:
                                # Handle duplicate column names by making them unique
                                headers = table[0]
                                # Make column names unique to avoid concat issues
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
                                
                                df = pd.DataFrame(table[1:], columns=unique_headers)
                            else:
                                df = pd.DataFrame(table)
                            
                            # Add metadata columns
                            df['_source_page'] = page_idx + 1
                            df['_source_region'] = region_name
                            df['_table_index'] = table_idx
                            
                            all_tables.append(df)
                            table_count += 1
            
            page_count = total_pages
        
        if not all_tables:
            print(f"  WARNING: No tables found in PDF")
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
        
        print(f"  ✓ Extracted {table_count} tables from {page_count} pages")
        print(f"  ✓ Rows: {len(combined_df)}, Columns: {len(combined_df.columns)}")
        print(f"  ✓ Saved to: {output_filename}")
        
        return True
        
    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Parse tables from all consolidated PDFs"""
    
    print("="*70)
    print("PHASE 2: PDF TABLE PARSING")
    print("="*70)
    
    # Find all consolidated PDFs
    consolidated_pdfs = list(OUTPUT_DIR.glob(f"BP_{YEAR}_*_consolidated.pdf"))
    
    if not consolidated_pdfs:
        print("ERROR: No consolidated PDF files found")
        print(f"Looking in: {OUTPUT_DIR}")
        return False
    
    print(f"\nFound {len(consolidated_pdfs)} consolidated PDF(s)")
    
    success_count = 0
    fail_count = 0
    
    for pdf_path in sorted(consolidated_pdfs):
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
    print(f"Parsing complete: {success_count} succeeded, {fail_count} failed")
    print("="*70)
    
    return fail_count == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
