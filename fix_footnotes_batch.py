#!/usr/bin/env python3
"""
Ralph Loop Iteration 4: Batch Footnote Fixer
Systematically fixes footnotes in all 92 markdown files in know-crpg-tenur/content
"""

import os
import re
from pathlib import Path

# Base directory
BASE_DIR = Path(r"C:\Users\mova\obsidian\OneNoteExport\01-Projects\07-CimanukFAO\know-crpg-tenur\content")

def fix_no_footnotes(content):
    """
    Fix files with 'Tidak ada catatan kaki' - convert source to footnote
    """
    # Pattern: **Sumber:** ... \n**Catatan kaki:** Tidak ada catatan kaki
    pattern = r'---\s*\n\s*\*\*Sumber:\*\*\s*([^\n]+)\s*\n\s*\*\*Catatan kaki:\*\*\s*Tidak ada catatan kaki\s*$'

    match = re.search(pattern, content, re.MULTILINE)
    if not match:
        return content, False

    source_text = match.group(1).strip()

    # Clean up source text
    source_text = re.sub(r'_Indonesia Water Tenure Analysis\.docx\.md', '', source_text)
    source_text = re.sub(r'Section:\s*\*\*(.+?)\*\*', r'Section: \1', source_text)

    # Find the position before "## Lihat Juga"
    lihat_juga_match = re.search(r'\n## Lihat Juga', content)
    if not lihat_juga_match:
        return content, False

    # Insert position is right before ## Lihat Juga
    insert_pos = lihat_juga_match.start()

    # Get the last sentence before ## Lihat Juga
    before_lihat = content[:insert_pos].rstrip()

    # Add footnote reference to last sentence
    if not before_lihat.endswith('[^1]'):
        before_lihat = before_lihat.rstrip('.') + '.[^1]'

    # Create footnote definition
    footnote_def = f"\n\n[^1]: {source_text}\n"

    # Reconstruct content
    new_content = before_lihat + footnote_def + content[insert_pos:]

    # Remove the old footer
    new_content = re.sub(pattern, '', new_content, flags=re.MULTILINE)

    return new_content, True

def fix_inline_references(content):
    """
    Fix files with 'Referensi inline terdeteksi' - convert inline numbers to footnotes
    """
    # Check if file has inline reference marker
    if 'Referensi inline terdeteksi' not in content:
        return content, False

    # Pattern to find source attribution
    source_pattern = r'\*\*Sumber:\*\*\s*([^\n]+)\s*\n\s*\*\*Catatan kaki:\*\*\s*Referensi inline terdeteksi'
    source_match = re.search(source_pattern, content)

    if not source_match:
        return content, False

    source_text = source_match.group(1).strip()

    # Find inline numbers (looking for standalone numbers like 27, 28, 29, 30)
    # Pattern: number at end of sentence or number followed by space and text
    inline_numbers = re.findall(r'(?<=[.\s])\d{2,3}(?=[\s\n]|$)', content)

    if not inline_numbers:
        # Try alternate pattern - numbers in middle of text
        inline_numbers = re.findall(r'(?<=\s)\d{2,3}(?=\s)', content)

    # Remove duplicates and sort
    inline_numbers = sorted(set(inline_numbers), key=lambda x: int(x))

    # Convert inline numbers to footnote markers
    new_content = content
    for i, num in enumerate(inline_numbers, start=1):
        # Replace the inline number with [^i]
        pattern = rf'(\w+)\s+{num}(?=\s|$|\n)'
        new_content = re.sub(pattern, rf'\1[^{i}]', new_content, count=1)

    # Find position before ## Lihat Juga
    lihat_juga_match = re.search(r'\n## Lihat Juga', new_content)
    if not lihat_juga_match:
        return content, False

    insert_pos = lihat_juga_match.start()

    # Create footnote definitions
    footnote_defs = "\n\n"
    for i, num in enumerate(inline_numbers, start=1):
        footnote_defs += f"[^{i}]: {source_text}, footnote {num}\n"

    # Insert footnotes
    new_content = new_content[:insert_pos] + footnote_defs + new_content[insert_pos:]

    # Remove old footer
    new_content = re.sub(source_pattern, '', new_content)
    new_content = re.sub(r'\n---\s*$', '', new_content)

    return new_content, True

def fix_needs_translation(content):
    """
    Fix files with [NEEDS_TRANSLATION] tag - just add note for manual translation
    """
    if '[NEEDS_TRANSLATION]' not in content:
        return content, False

    # Add note that this file needs manual translation
    note = "\n\n> **Note:** This file contains English text that needs translation to Indonesian.\n"

    # Insert note after frontmatter
    frontmatter_end = content.find('---', 3)
    if frontmatter_end > 0:
        insert_pos = frontmatter_end + 3
        new_content = content[:insert_pos] + note + content[insert_pos:]
        return new_content, True

    return content, False

def process_file(file_path):
    """Process a single markdown file"""
    print(f"Processing: {file_path.relative_to(BASE_DIR)}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        modified = False

        # Try each fix method in order
        content, was_fixed = fix_no_footnotes(content)
        if was_fixed:
            print(f"  ✓ Fixed 'Tidak ada catatan kaki'")
            modified = True

        if not modified:
            content, was_fixed = fix_inline_references(content)
            if was_fixed:
                print(f"  ✓ Fixed inline references")
                modified = True

        if not modified:
            content, was_fixed = fix_needs_translation(content)
            if was_fixed:
                print(f"  ✓ Added translation note")
                modified = True

        # Write back if modified
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        else:
            print(f"  - No changes needed")
            return False

    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        return False

def main():
    """Main execution function"""
    print("=" * 80)
    print("RALPH LOOP ITERATION 4: Batch Footnote Fixer")
    print("=" * 80)
    print()

    # Find all markdown files
    md_files = list(BASE_DIR.rglob("*.md"))
    md_files = [f for f in md_files if f.name != 'index.md']

    print(f"Found {len(md_files)} markdown files to process\n")

    modified_count = 0
    for file_path in sorted(md_files):
        if process_file(file_path):
            modified_count += 1
        print()

    print("=" * 80)
    print(f"COMPLETE: {modified_count} files modified out of {len(md_files)} total")
    print("=" * 80)

if __name__ == '__main__':
    main()
