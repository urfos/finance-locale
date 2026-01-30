#!/usr/bin/env python3
"""
Phase 2: Merge extracted PDF pages
Consolidates extracted pages from multiple regions into two consolidated PDFs based on groupes_BP_regions.txt
Uses PyPDF2 to merge PDFs
"""

from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
import sys
import re

# Configuration
OUTPUT_DIR = Path(__file__).parent.parent / "output"
CONFIG_DIR = Path(__file__).parent.parent / "config"
GROUPES_FILE = Path(__file__).parent.parent / "groupes_BP_regions.txt"
YEAR = "2024"

# Region name mappings from config (for matching with filenames)
REGION_NAMES_MAP = {
    "Auvergne Rhone Alpes": "Auvergne-Rhone-Alpes",
    "Bourgogne Franche Comté": "Bourgogne-Franche-Comté",
    "Bretagne": "Bretagne",
    "Centre VdL": "Centre",
    "Grand Est": "Grand Est",
    "Hauts de France": "HdF",
    "Ile de France": "IdF",
    "Normandie": "Normandie",
    "Nouvelle Aquitaine": "Nouvelle-Aquitaine",
    "Occitanie": "Occitanie",
    "Provence Alpes Cote d'Azur": "PACA"
}

def parse_groupes_file():
    """Parse groupes_BP_regions.txt to get region -> group mapping"""
    region_groups = {}
    
    try:
        with open(GROUPES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # Format: "Region Name GroupNumber"
                parts = line.rsplit(' ', 1)  # Split from right to get last space
                if len(parts) == 2:
                    region_name, group_num = parts
                    region_name = region_name.strip()
                    group_num = group_num.strip()
                    region_groups[region_name] = group_num
    except FileNotFoundError:
        print(f"ERROR: {GROUPES_FILE} not found")
        return {}
    
    return region_groups

def get_region_from_filename(filename):
    """Extract region name from filename like 'BP_2024_Auvergne-Rhone-Alpes_extracted.pdf'"""
    match = re.search(r'BP_\d{4}_(.+)_extracted\.pdf', filename)
    if match:
        return match.group(1)
    return None

def merge_extracted_pages(year=YEAR):
    """Merge all extracted page PDFs by group (1 or 2)"""
    
    print(f"\nMerging extracted pages by group for year {year}...")
    
    # Load region -> group mapping
    region_groups = parse_groupes_file()
    if not region_groups:
        return False
    
    # Group extracted PDFs by their group number (1 or 2)
    group_pdfs = {1: [], 2: []}
    
    for pdf_file in OUTPUT_DIR.glob(f"BP_{year}_*_extracted.pdf"):
        filename_region = get_region_from_filename(pdf_file.name)
        if not filename_region:
            continue
        
        # Find matching region in groupes mapping
        matching_region = None
        for config_region, file_region in REGION_NAMES_MAP.items():
            if file_region == filename_region:
                matching_region = config_region
                break
        
        if matching_region and matching_region in region_groups:
            group_num = int(region_groups[matching_region])
            group_pdfs[group_num].append((pdf_file, matching_region))
        else:
            print(f"WARNING: Could not find group for {filename_region}")
    
    if not any(group_pdfs.values()):
        print("ERROR: No extracted PDF files found")
        return False
    
    success_count = 0
    fail_count = 0
    
    # Merge PDFs for each group
    for group_num in sorted(group_pdfs.keys()):
        pdf_list = group_pdfs[group_num]
        
        if not pdf_list:
            print(f"\nGroup {group_num}: No PDFs found")
            continue
        
        print(f"\nMerging Group {group_num}:")
        print(f"  Regions in group: {', '.join(sorted(set(r for _, r in pdf_list)))}")
        print(f"  Files to merge: {len(pdf_list)}")
        
        try:
            writer = PdfWriter()
            total_pages = 0
            
            # Merge all PDFs for this group
            for pdf_file, region_name in sorted(pdf_list, key=lambda x: x[1]):
                with open(pdf_file, 'rb') as f:
                    reader = PdfReader(f)
                    for page in reader.pages:
                        writer.add_page(page)
                    total_pages += len(reader.pages)
                    print(f"    + {pdf_file.name} ({len(reader.pages)} pages)")
            
            # Save consolidated PDF
            output_filename = f"BP_{year}_Group{group_num}_consolidated.pdf"
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
