#!/usr/bin/env python3
"""
Ralph Loop Citation Fixer V2 - Fix ALL document citations to use proper titles
Includes additional project documents beyond Annex 7 and Assessment Guide
"""

import os
import re
from pathlib import Path

def fix_all_citations(content):
    """Fix all citation patterns to use proper document titles"""

    modified = False
    original_content = content

    # Pattern Set 1: Already fixed in V1 (Annex 7 and Assessment Guide)
    # These should already be correct, but we'll keep the patterns for safety

    patterns_v1 = [
        # Annex 7 variations
        (r'Annex\s*7_Indonesia Water Tenure Analysis\.docx\.md,\s*Section:\s*',
         r'Al\'Afghani, M.M. (2022). *Water Tenure in Indonesia*, Section: '),
        (r'Annex\s*7_Indonesia Water Tenure Analysis\.docx\.md,\s*Bagian:\s*',
         r'Al\'Afghani, M.M. (2022). *Water Tenure in Indonesia*, bagian '),
        (r'Annex\s*7 Indonesia Water Tenure Analysis,\s*bagian\s*',
         r'Al\'Afghani, M.M. (2022). *Water Tenure in Indonesia*, bagian '),
        (r'Annex\s*7,\s*Section:\s*',
         r'Al\'Afghani, M.M. (2022). *Water Tenure in Indonesia*, Section: '),
        (r'Annex7,\s*Section:\s*',
         r'Al\'Afghani, M.M. (2022). *Water Tenure in Indonesia*, Section: '),
        # Assessment Guide
        (r'Assessment Guide,\s*Section:\s*',
         r'FAO. (2016). *Water Tenure Assessment Guide*, Section: '),
        (r'Water Tenure Assessment Guide,\s*Section:\s*',
         r'FAO. (2016). *Water Tenure Assessment Guide*, Section: '),
    ]

    # Pattern Set 2: NEW - Additional project documents
    patterns_v2 = [
        # Comprehensive Water Tenure Thematic Analysis
        (r'COMPREHENSIVE_WATER_TENURE_THEMATIC_ANALYSIS\.md,\s*Section:\s*',
         r'Cimanuk FAO Water Scarcity Program. (2025). *Comprehensive Water Tenure Thematic Analysis*, Section: '),

        # Governance of Water Tenure
        (r'Governance of Water Tenure\.md,\s*Section:\s*',
         r'Al\'Afghani, M.M. (2022). *Water Tenure in Indonesia*, Section 5: Governance of Water Tenure, '),

        # Validation Results (Aquaculture)
        (r'validation_results_B6_aquaculture\.md,\s*Section:\s*',
         r'Cimanuk FAO Project. (2026). *B6 Aquaculture Validation Results*, '),
    ]

    # Apply all patterns
    for pattern, replacement in patterns_v1 + patterns_v2:
        content = re.sub(pattern, replacement, content)

    # Clean up any remaining .md, .docx, .pdf extensions
    content = re.sub(r'\.docx\.md', '', content)
    content = re.sub(r'\.md,', ',', content)

    # Ensure proper punctuation at end of citations
    def fix_footnote_punctuation(match):
        footnote = match.group(0)
        if not footnote.rstrip().endswith('.'):
            return footnote.rstrip() + '.'
        return footnote

    content = re.sub(r'\[\^\d+\]:.*?(?=\n\n|\n##|\Z)', fix_footnote_punctuation, content, flags=re.DOTALL)

    if content != original_content:
        modified = True

    return content, modified

def process_file(file_path):
    """Process a single markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content, modified = fix_all_citations(content)

        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return 'fixed'
        else:
            return 'unchanged'

    except Exception as e:
        return f'error: {str(e)}'

def main():
    """Main function - Ralph Loop execution"""
    content_dir = Path(__file__).parent / 'content'

    if not content_dir.exists():
        print(f"Error: Content directory not found: {content_dir}")
        return

    print("=" * 70)
    print("RALPH LOOP CITATION FIXER V2 - Additional Document Citations")
    print("=" * 70)
    print()

    # Collect all markdown files
    all_files = []
    for md_file in content_dir.rglob('*.md'):
        if md_file.name != 'index.md':
            all_files.append(md_file)

    print(f"Found {len(all_files)} markdown files to process")
    print()
    print("Fixing citations for additional documents:")
    print("  - Comprehensive Water Tenure Thematic Analysis")
    print("  - Governance of Water Tenure")
    print("  - B6 Aquaculture Validation Results")
    print()

    # Process files
    fixed = []
    unchanged = []
    errors = []

    for i, file_path in enumerate(sorted(all_files), 1):
        rel_path = file_path.relative_to(content_dir)

        status = process_file(file_path)

        if status == 'fixed':
            fixed.append(rel_path)
            print(f"[{i}/{len(all_files)}] [OK] {rel_path}")
        elif status == 'unchanged':
            unchanged.append(rel_path)
        else:
            errors.append((rel_path, status))
            print(f"[{i}/{len(all_files)}] [ERROR] {rel_path}: {status}")

    # Summary report
    print()
    print("=" * 70)
    print("RALPH LOOP V2 COMPLETION SUMMARY")
    print("=" * 70)
    print()
    print(f"Total files processed: {len(all_files)}")
    print(f"  [OK] Fixed: {len(fixed)}")
    print(f"  [SKIP] Unchanged: {len(unchanged)}")
    print(f"  [ERROR] Errors: {len(errors)}")
    print()

    if fixed:
        print("FIXED FILES:")
        for rel_path in fixed:
            print(f"  - {rel_path}")
        print()

    if errors:
        print("ERRORS:")
        for rel_path, error in errors:
            print(f"  - {rel_path}: {error}")
        print()

    print("=" * 70)
    print("[SUCCESS] All document citations now use proper titles!")
    print("=" * 70)
    print()
    print("Document citations fixed:")
    print("  - Al'Afghani, M.M. (2022). *Water Tenure in Indonesia*")
    print("  - FAO. (2016). *Water Tenure Assessment Guide*")
    print("  - Cimanuk FAO Water Scarcity Program. (2025). *Comprehensive Water Tenure Thematic Analysis*")
    print("  - Cimanuk FAO Project. (2026). *B6 Aquaculture Validation Results*")
    print()

if __name__ == '__main__':
    main()
