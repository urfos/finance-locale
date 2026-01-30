#!/usr/bin/env python3
"""
Phase 1: Explore BP PDF structure to understand table layouts
Examines sample pages to identify budget table formats
"""

import pdfplumber
import json
import sys
from pathlib import Path

# Configuration
DATA_DIR = Path(__file__).parent.parent / "data"
BP_DIR = DATA_DIR / "Documents BP Collectivités"
OUTPUT_DIR = Path(__file__).parent.parent / "output"

# Sample regions with their page ranges from pages_BP_regions.txt
SAMPLE_REGIONS = {
    "Auvergne-Rhone-Alpes": {"pages": [16, 17, 18]},  # Pages 17-19 (0-indexed)
    "Bretagne": {"pages": [18, 19, 20]}  # Pages 19-21 (0-indexed)
}
PDF_FILE = "BP2024.pdf"

def explore_pdf(region_name, sample_pages):
    """Explore PDF structure and table layouts for a given region"""
    
    pdf_path = BP_DIR / region_name / "BP" / PDF_FILE
    
    if not pdf_path.exists():
        print(f"ERROR: PDF not found at {pdf_path}")
        return False
    
    print(f"\nExploring: {region_name} - {pdf_path}")
    print(f"File size: {pdf_path.stat().st_size / 1024:.1f} KB")
    print(f"Sample pages: {[p+1 for p in sample_pages]}\n")
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total pages in PDF: {len(pdf.pages)}\n")
        
        for page_idx in sample_pages:
            if page_idx >= len(pdf.pages):
                print(f"Page {page_idx + 1} does not exist")
                continue
            
            page = pdf.pages[page_idx]
            print(f"\n{'='*70}")
            print(f"PAGE {page_idx + 1}")
            print(f"{'='*70}")
            print(f"Dimensions: {page.width:.0f}x{page.height:.0f} pt")
            print(f"Rotation: {page.rotation}")
            
            # Extract text
            text = page.extract_text()
            if text:
                lines = text.split('\n')[:10]
                print(f"\nFirst 10 lines of text:")
                for i, line in enumerate(lines, 1):
                    print(f"  {i}: {line[:80]}")
            
            # Extract tables
            tables = page.extract_tables()
            print(f"\nTables found: {len(tables) if tables else 0}")
            
            if tables:
                for t_idx, table in enumerate(tables):
                    print(f"\n  Table {t_idx + 1}:")
                    print(f"    Dimensions: {len(table)} rows x {len(table[0]) if table else 0} cols")
                    if table:
                        print(f"    First row (headers):")
                        for i, cell in enumerate(table[0][:5]):
                            print(f"      Col {i}: {str(cell)[:50]}")
                        if len(table) > 1:
                            print(f"    Second row (sample data):")
                            for i, cell in enumerate(table[1][:5]):
                                print(f"      Col {i}: {str(cell)[:50]}")

if __name__ == "__main__":
    print("="*70)
    print("BP PDF STRUCTURE EXPLORATION")
    print("="*70)
    
    all_success = True
    for region, config in SAMPLE_REGIONS.items():
        try:
            explore_pdf(region, config["pages"])
        except Exception as e:
            print(f"\nERROR exploring {region}: {e}")
            all_success = False
    
    print("\n" + "="*70)
    if all_success:
        print("Exploration complete for all regions")
    else:
        print("Exploration complete with some errors")
