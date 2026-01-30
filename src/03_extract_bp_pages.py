#!/usr/bin/env python3
"""
Phase 2: Extract specific pages from BP PDFs
Extracts pages based on page ranges from regions_config.yaml
Uses PyPDF2 to extract and save individual page ranges per region
"""

import yaml
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
import sys

# Configuration
DATA_DIR = Path(__file__).parent.parent / "data"
BP_DIR = DATA_DIR / "Documents BP Collectivités"
CONFIG_DIR = Path(__file__).parent.parent / "config"
OUTPUT_DIR = Path(__file__).parent.parent / "output"

REGIONS_CONFIG = CONFIG_DIR / "regions_config.yaml"
PDF_FILE = "BP2024.pdf"

def load_regions_config():
    """Load regions configuration from YAML"""
    with open(REGIONS_CONFIG, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config['regions']

def extract_pages(region_key, region_config, year="2024"):
    """Extract specific pages from a region's BP PDF"""
    
    region_name = region_config['folder_name']
    pages_start = region_config['pages_start']
    pages_end = region_config['pages_end']
    
    pdf_path = BP_DIR / region_name / "BP" / f"BP{year}.pdf"
    
    if not pdf_path.exists():
        print(f"ERROR: PDF not found at {pdf_path}")
        return False
    
    print(f"\nExtracting: {region_name}")
    print(f"  Source: {pdf_path}")
    print(f"  Pages: {pages_start}-{pages_end}")
    
    try:
        # Open the source PDF
        with open(pdf_path, 'rb') as f:
            reader = PdfReader(f)
            total_pages = len(reader.pages)
            
            if pages_end > total_pages:
                print(f"  WARNING: End page ({pages_end}) exceeds total pages ({total_pages}). Adjusting.")
                pages_end = total_pages
            
            # Create a new PDF with extracted pages
            writer = PdfWriter()
            
            # PyPDF2 uses 0-based indexing, but our config uses 1-based
            for page_num in range(pages_start - 1, pages_end):
                if page_num < len(reader.pages):
                    writer.add_page(reader.pages[page_num])
            
            # Save extracted pages
            output_filename = f"BP_{year}_{region_name}_extracted.pdf"
            output_path = OUTPUT_DIR / output_filename
            
            with open(output_path, 'wb') as out_file:
                writer.write(out_file)
            
            print(f"  ✓ Extracted {pages_end - pages_start + 1} pages")
            print(f"  ✓ Saved to: {output_filename} ({output_path.stat().st_size / 1024:.1f} KB)")
            
            return True
            
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def main():
    """Extract pages for all regions"""
    
    print("="*70)
    print("PHASE 2: PDF PAGE EXTRACTION")
    print("="*70)
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    try:
        regions_config = load_regions_config()
    except Exception as e:
        print(f"ERROR loading config: {e}")
        sys.exit(1)
    
    success_count = 0
    fail_count = 0
    
    for region_key, region_config in regions_config.items():
        if region_key == 'note':
            continue
        
        if extract_pages(region_key, region_config):
            success_count += 1
        else:
            fail_count += 1
    
    print("\n" + "="*70)
    print(f"Extraction complete: {success_count} succeeded, {fail_count} failed")
    print("="*70)
    
    return fail_count == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
