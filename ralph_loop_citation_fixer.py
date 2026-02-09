#!/usr/bin/env python3
"""
Ralph Loop Citation Fixer - Fix all citations to use proper document titles
Converts filenames to proper academic citations
"""

import os
import re
from pathlib import Path

def fix_citations(content):
    """Fix all citation patterns to use proper document titles"""

    modified = False

    # Pattern 1: Annex 7 variations in footnotes
    patterns_annex7 = [
        (r'Annex\s*7_Indonesia Water Tenure Analysis\.docx\.md,\s*Section:\s*',
         r'Al\'Afghani, M.M. (2022). *Water Tenure in Indonesia*, Section: '),
        (r'Annex\s*7_Indonesia Water Tenure Analysis\.docx\.md,\s*Bagian:\s*',
         r'Al\'Afghani, M.M. (2022). *Water Tenure in Indonesia*, bagian '),
        (r'Annex\s*7_Indonesia Water Tenure Analysis\.docx\.md,\s*Table\s*',
         r'Al\'Afghani, M.M. (2022). *Water Tenure in Indonesia*, Table '),
        (r'Annex\s*7_Indonesia Water Tenure Analysis\.docx\.md,\s*Figure\s*',
         r'Al\'Afghani, M.M. (2022). *Water Tenure in Indonesia*, Figure '),
        (r'Annex\s*7 Indonesia Water Tenure Analysis,\s*bagian\s*',
         r'Al\'Afghani, M.M. (2022). *Water Tenure in Indonesia*, bagian '),
        (r'Annex\s*7,\s*Section:\s*',
         r'Al\'Afghani, M.M. (2022). *Water Tenure in Indonesia*, Section: '),
        (r'Annex\s*7,\s*Diagram\s*',
         r'Al\'Afghani, M.M. (2022). *Water Tenure in Indonesia*, Diagram '),
        (r'Annex\s*7,\s*bagian\s*',
         r'Al\'Afghani, M.M. (2022). *Water Tenure in Indonesia*, bagian '),
        (r'Annex7,\s*Section:\s*',
         r'Al\'Afghani, M.M. (2022). *Water Tenure in Indonesia*, Section: '),
    ]

    # Pattern 2: Assessment Guide variations
    patterns_guide = [
        (r'Assessment Guide,\s*Section:\s*',
         r'FAO. (2016). *Water Tenure Assessment Guide*, Section: '),
        (r'Water Tenure Assessment Guide,\s*Section:\s*',
         r'FAO. (2016). *Water Tenure Assessment Guide*, Section: '),
    ]

    # Apply all patterns
    original_content = content

    for pattern, replacement in patterns_annex7 + patterns_guide:
        content = re.sub(pattern, replacement, content)

    if content != original_content:
        modified = True

    # Clean up any remaining issues
    # Remove .docx.md references that might still be there
    content = re.sub(r'\.docx\.md', '', content)

    # Ensure proper punctuation at end of citations
    # Find footnote definitions and ensure they end with period
    def fix_footnote_punctuation(match):
        footnote = match.group(0)
        if not footnote.rstrip().endswith('.'):
            return footnote.rstrip() + '.'
        return footnote

    content = re.sub(r'\[\^\d+\]:.*?(?=\n\n|\n##|\Z)', fix_footnote_punctuation, content, flags=re.DOTALL)

    return content, modified

def process_file(file_path):
    """Process a single markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content, modified = fix_citations(content)

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
    print("RALPH LOOP CITATION FIXER - Fixing Document Title Citations")
    print("=" * 70)
    print()

    # Collect all markdown files
    all_files = []
    for md_file in content_dir.rglob('*.md'):
        if md_file.name != 'index.md':
            all_files.append(md_file)

    print(f"Found {len(all_files)} markdown files to process")
    print()

    # Process files
    fixed = []
    unchanged = []
    errors = []

    for i, file_path in enumerate(sorted(all_files), 1):
        rel_path = file_path.relative_to(content_dir)
        print(f"[{i}/{len(all_files)}] Processing: {rel_path}")

        status = process_file(file_path)

        if status == 'fixed':
            fixed.append(rel_path)
            print(f"  [OK] Fixed - Citations updated")
        elif status == 'unchanged':
            unchanged.append(rel_path)
            print(f"  [SKIP] No citation changes needed")
        else:
            errors.append((rel_path, status))
            print(f"  [ERROR] {status}")
        print()

    # Summary report
    print("=" * 70)
    print("RALPH LOOP COMPLETION SUMMARY")
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
    print("[SUCCESS] Ralph Loop citation fix complete!")
    print("=" * 70)
    print()
    print("Citations now use proper document titles:")
    print("  - Al'Afghani, M.M. (2022). *Water Tenure in Indonesia*")
    print("  - FAO. (2016). *Water Tenure Assessment Guide*")
    print()

if __name__ == '__main__':
    main()
