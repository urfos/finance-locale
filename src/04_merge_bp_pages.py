#!/usr/bin/env python3
"""
Phase 2: Merge extracted PDF pages
Consolidates extracted pages from multiple PDFs into single consolidated PDFs per region
Uses PyPDF2 to merge PDFs
"""

from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
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

def merge_extracted_pages(year=YEAR):
    """Merge all extracted page PDFs by region"""
    
    print(f"\nMerging extracted pages for year {year}...")
    
    # Group extracted PDFs by region
    region_pdfs = {}
    
    for pdf_file in OUTPUT_DIR.glob(f"BP_{year}_*_extracted.pdf"):
        region = get_region_from_filename(pdf_file.name)
        if region:
            if region not in region_pdfs:
                region_pdfs[region] = []
            region_pdfs[region].append(pdf_file)
    
    if not region_pdfs:
        print("ERROR: No extracted PDF files found")
        return False
    
    success_count = 0
    fail_count = 0
    
    for region, pdf_files in sorted(region_pdfs.items()):
        print(f"\nMerging: {region}")
        print(f"  Files to merge: {len(pdf_files)}")
        
        try:
            writer = PdfWriter()
            total_pages = 0
            
            # Merge all PDFs for this region
            for pdf_file in sorted(pdf_files):
                with open(pdf_file, 'rb') as f:
                    reader = PdfReader(f)
                    for page in reader.pages:
                        writer.add_page(page)
                    total_pages += len(reader.pages)
                    print(f"    + {pdf_file.name} ({len(reader.pages)} pages)")
            
            # Save consolidated PDF
            output_filename = f"BP_{year}_{region}_consolidated.pdf"
            output_path = OUTPUT_DIR / output_filename
            
            with open(output_path, 'wb') as out_file:
                writer.write(out_file)
            
            print(f"  ✓ Consolidated to: {output_filename} ({output_path.stat().st_size / 1024:.1f} KB)")
            print(f"  ✓ Total pages: {total_pages}")
            success_count += 1
            
        except Exception as e:
            print(f"  ERROR: {e}")
            fail_count += 1
    
    return fail_count == 0

def main():
    """Main merge function"""
    
    print("="*70)
    print("PHASE 2: PDF PAGE MERGING")
    print("="*70)
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    success = merge_extracted_pages(YEAR)
    
    print("\n" + "="*70)
    if success:
        print("Merging complete: all regions consolidated")
    else:
        print("Merging complete with some errors")
    print("="*70)
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
