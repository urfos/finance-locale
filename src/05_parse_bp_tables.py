#!/usr/bin/env python3
"""
BP Table Parser v2 - Row Expansion Edition
Extracts Table 3 from BP PDFs, expands multi-line cells into separate rows
Output: Semicolon-delimited CSV for French Excel compatibility

Test mode: Auvergne-Rhone-Alpes and Bretagne only
"""

import pdfplumber
from pathlib import Path
import sys

OUTPUT_DIR = Path(__file__).parent.parent / "output"
YEAR = "2024"

# Test regions only - do not modify until user approves structure
# UPDATE: User approved - now processing all regions
ALL_REGIONS = [
    "Auvergne-Rhone-Alpes", "Bourgogne-Franche-Comté", "Bretagne", "Centre",
    "Grand Est", "HdF", "IdF", "Normandie", "Nouvelle-Aquitaine", "Occitanie", "PACA"
]


def clean_text(text):
    """
    Clean text cell: remove leading '=' and trim whitespace
    """
    if not text:
        return ''
    text = str(text).strip()
    # Remove leading '=' which causes Excel formula issues
    if text.startswith('='):
        text = text[1:].strip()
    return text


def clean_number(value):
    """
    Convert French number format to R-readable format:
    - Remove spaces (thousands separator)
    - Replace comma with dot (decimal separator)
    Example: "3 926 800 000,00" -> "3926800000.00"
    """
    if not value:
        return ''
    val = str(value).strip()
    if not val:
        return ''
    # Remove all spaces
    val = val.replace(' ', '')
    # Replace comma with dot for decimal
    val = val.replace(',', '.')
    return val


def determine_section(description_text):
    """
    Determine budget section from description.
    Returns: (section_name, is_section_header)
    """
    if not description_text:
        return 'unknown', False
    
    text_upper = description_text.upper()
    
    if "DEPENSES" in text_upper and "INVESTISSEMENT" in text_upper:
        return 'investment_expense', True
    elif "RECETTES" in text_upper and "INVESTISSEMENT" in text_upper:
        return 'investment_revenue', True
    elif "DEPENSES" in text_upper and "FONCTIONNEMENT" in text_upper:
        return 'operating_expense', True
    elif "RECETTES" in text_upper and "FONCTIONNEMENT" in text_upper:
        return 'operating_revenue', True
    
    return 'unknown', False


def expand_multiline_row(row, region, current_section, row_index):
    """
    Expand a row with multi-line cells into multiple rows.
    
    Input row: 6 cells, some may contain newlines
    Returns: list of expanded row dicts
    """
    # Check if first column has newlines (indicates multi-line structure)
    description = str(row[0]) if row[0] else ''
    
    if '\n' not in description:
        # Single-line row - no expansion needed
        section, is_header = determine_section(description)
        if is_header:
            current_section = section
        
        return [{
            'region': region,
            'section': current_section,
            'row_type': 'section_header' if is_header else 'data',
            'level': 0,
            'row_index': row_index,
            'description': clean_text(description),
            'budget_anterieur': clean_number(row[1]),
            'restes_a_realiser_n1': clean_number(row[2]),
            'propositions_nouvelles': clean_number(row[3]),
            'vote_assemblee': clean_number(row[4]),
            'total_budget': clean_number(row[5])
        }], current_section
    
    # Multi-line row - expand each line into separate row
    descriptions = description.split('\n')
    
    # Split all value columns by newline
    col1_values = str(row[1]).split('\n') if row[1] else ['']
    col2_values = str(row[2]).split('\n') if row[2] else ['']
    col3_values = str(row[3]).split('\n') if row[3] else ['']
    col4_values = str(row[4]).split('\n') if row[4] else ['']
    col5_values = str(row[5]).split('\n') if row[5] else ['']
    
    # Determine max lines
    max_lines = max(len(descriptions), len(col1_values), len(col2_values), 
                    len(col3_values), len(col4_values), len(col5_values))
    
    # Pad shorter lists
    def pad_list(lst, length):
        return lst + [''] * (length - len(lst))
    
    descriptions = pad_list(descriptions, max_lines)
    col1_values = pad_list(col1_values, max_lines)
    col2_values = pad_list(col2_values, max_lines)
    col3_values = pad_list(col3_values, max_lines)
    col4_values = pad_list(col4_values, max_lines)
    col5_values = pad_list(col5_values, max_lines)
    
    expanded_rows = []
    for i in range(max_lines):
        desc = descriptions[i].strip()
        
        # Determine level: 0 for first line, 1 for sub-lines
        level = 0 if i == 0 else 1
        
        # Check if this is a section header (only on level 0)
        section, is_header = determine_section(desc) if level == 0 else ('unknown', False)
        if is_header:
            current_section = section
        
        expanded_rows.append({
            'region': region,
            'section': current_section,
            'row_type': 'section_header' if is_header else 'data',
            'level': level,
            'row_index': row_index,
            'description': clean_text(desc),
            'budget_anterieur': clean_number(col1_values[i]),
            'restes_a_realiser_n1': clean_number(col2_values[i]),
            'propositions_nouvelles': clean_number(col3_values[i]),
            'vote_assemblee': clean_number(col4_values[i]),
            'total_budget': clean_number(col5_values[i])
        })
    
    return expanded_rows, current_section


def parse_pdf_to_rows(pdf_path, region):
    """
    Parse PDF Table 3, expand multi-line cells, return list of row dicts
    """
    print(f"\nParsing: {region}")
    print(f"  File: {pdf_path.name}")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            if not pdf.pages:
                print("  ERROR: No pages in PDF")
                return None
            
            page = pdf.pages[0]
            tables = page.extract_tables()
            
            if not tables or len(tables) < 4:
                print(f"  ERROR: Expected 4 tables, found {len(tables) if tables else 0}")
                return None
            
            # Table 3 is the main budget data
            data_table = tables[3]
            if not data_table:
                print("  ERROR: Table 3 is empty")
                return None
            
            print(f"  Found {len(data_table)} rows in Table 3")
            
            all_rows = []
            current_section = 'unknown'
            
            for row_idx, row in enumerate(data_table):
                if not row or len(row) != 6:
                    print(f"  WARNING: Skipping row {row_idx} - expected 6 cols, got {len(row) if row else 0}")
                    continue
                
                expanded, current_section = expand_multiline_row(
                    row, region, current_section, row_idx
                )
                all_rows.extend(expanded)
            
            print(f"  ✓ Expanded to {len(all_rows)} rows")
            
            # Count sections
            sections = set(r['section'] for r in all_rows)
            print(f"  ✓ Sections found: {sorted(sections)}")
            
            return all_rows
            
    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None


def write_csv(rows, output_path):
    """
    Write rows to CSV with semicolon delimiter
    """
    columns = [
        'region', 'section', 'row_type', 'level', 'row_index',
        'description', 'budget_anterieur', 'restes_a_realiser_n1',
        'propositions_nouvelles', 'vote_assemblee', 'total_budget'
    ]
    
    with open(output_path, 'w', encoding='utf-8-sig') as f:
        # Write header
        f.write(';'.join(columns) + '\n')
        
        # Write data rows
        for row in rows:
            values = []
            for col in columns:
                val = str(row.get(col, ''))
                # Escape semicolons in values if present
                if ';' in val:
                    val = f'"{val}"'
                values.append(val)
            f.write(';'.join(values) + '\n')
    
    print(f"  ✓ Saved: {output_path.name}")


def main():
    """
    Parse all 11 regions
    """
    print("=" * 70)
    print("BP TABLE PARSER v2 - ROW EXPANSION")
    print("=" * 70)
    print(f"\nProcessing {len(ALL_REGIONS)} regions")
    print("Delimiter: semicolon (;) for French Excel\n")
    
    success = 0
    failed = 0
    
    for region in ALL_REGIONS:
        pdf_path = OUTPUT_DIR / f"BP_{YEAR}_{region}_extracted.pdf"
        
        if not pdf_path.exists():
            print(f"\nERROR: PDF not found for {region}")
            failed += 1
            continue
        
        rows = parse_pdf_to_rows(pdf_path, region)
        
        if rows:
            output_path = OUTPUT_DIR / f"BP_{YEAR}_{region}.csv"
            write_csv(rows, output_path)
            success += 1
        else:
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"Complete: {success} succeeded, {failed} failed")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
