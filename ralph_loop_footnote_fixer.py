#!/usr/bin/env python3
"""
Ralph Loop Footnote Fixer - Batch process all 92 articles
Converts inline references to proper markdown footnotes
"""

import os
import re
from pathlib import Path

def extract_inline_references(content):
    """Extract inline numeric references like 27, 28, 29"""
    # Find numbers that might be references (at start of line or after punctuation)
    pattern = r'(?:^|\s)(\d{1,3})(?:\s|$)'
    matches = re.findall(pattern, content)
    return matches

def has_inline_references(content):
    """Check if content has 'Referensi inline terdeteksi'"""
    return 'Referensi inline terdeteksi' in content or 'belum diformat sebagai footnote' in content

def has_no_footnotes_note(content):
    """Check if content has 'Tidak ada catatan kaki'"""
    return 'Tidak ada catatan kaki' in content

def extract_source_attribution(content):
    """Extract source attribution from footer"""
    pattern = r'\*\*Sumber:\*\*\s*(.+?)(?:\n|$)'
    match = re.search(pattern, content)
    if match:
        return match.group(1).strip()
    return None

def convert_simple_footnote(content):
    """
    Convert files with 'Tidak ada catatan kaki' to proper footnotes
    These just need the source attribution converted to a footnote
    """
    lines = content.split('\n')

    # Find the "Lihat Juga" section
    lihat_juga_idx = -1
    source_idx = -1

    for i, line in enumerate(lines):
        if line.strip() == '## Lihat Juga':
            lihat_juga_idx = i
        if line.startswith('**Sumber:**'):
            source_idx = i

    if source_idx == -1:
        return content  # No source attribution found

    # Extract source attribution
    source_line = lines[source_idx]
    source_match = re.search(r'\*\*Sumber:\*\*\s*(.+?)$', source_line)
    if not source_match:
        return content

    source_text = source_match.group(1).strip()

    # Find where to add footnote reference (end of first paragraph after frontmatter)
    frontmatter_end = -1
    for i, line in enumerate(lines):
        if i > 0 and line.strip() == '---' and lines[0].strip() == '---':
            frontmatter_end = i
            break

    # Find first paragraph after title
    first_para_end = -1
    if frontmatter_end > 0:
        found_title = False
        for i in range(frontmatter_end + 1, len(lines)):
            if lines[i].startswith('# '):
                found_title = True
                continue
            if found_title and lines[i].strip() and not lines[i].startswith('#'):
                # This is content, find end of first paragraph
                for j in range(i, len(lines)):
                    if not lines[j].strip():  # Empty line marks end of paragraph
                        first_para_end = j - 1
                        break
                break

    if first_para_end > 0:
        # Add footnote reference to end of first paragraph
        lines[first_para_end] = lines[first_para_end].rstrip() + '[^1]'

        # Create footnote definition
        footnote_def = f'[^1]: {source_text}'

        # Insert before Lihat Juga section
        if lihat_juga_idx > 0:
            lines.insert(lihat_juga_idx, '')
            lines.insert(lihat_juga_idx, footnote_def)
            lines.insert(lihat_juga_idx, '')

        # Remove old source and catatan kaki lines
        lines = [l for l in lines if not (l.startswith('**Sumber:**') or l.startswith('**Catatan kaki:**'))]

        return '\n'.join(lines)

    return content

def convert_inline_references_footnote(content):
    """
    Convert files with inline numeric references to proper footnotes
    More complex - needs to extract numbers and convert to [^1], [^2], etc.
    """
    lines = content.split('\n')

    # Find source attribution
    source_text = None
    for line in lines:
        if line.startswith('**Sumber:**'):
            match = re.search(r'\*\*Sumber:\*\*\s*(.+?)$', line)
            if match:
                source_text = match.group(1).strip()
                break

    if not source_text:
        return content  # Can't process without source

    # Find inline numbers in text (before ## Lihat Juga)
    lihat_juga_idx = -1
    for i, line in enumerate(lines):
        if line.strip() == '## Lihat Juga':
            lihat_juga_idx = i
            break

    # Get content section (between title and Lihat Juga)
    content_lines = lines[:lihat_juga_idx] if lihat_juga_idx > 0 else lines

    # Find all numeric references (simple pattern: standalone numbers)
    # This is a conservative approach - only convert obvious references
    footnote_counter = 1
    footnote_defs = []

    # For now, create a single footnote from source attribution
    # More complex inline number extraction would require context analysis

    # Find end of first paragraph to add reference
    frontmatter_end = -1
    for i, line in enumerate(lines):
        if i > 0 and line.strip() == '---' and lines[0].strip() == '---':
            frontmatter_end = i
            break

    first_para_end = -1
    if frontmatter_end > 0:
        found_title = False
        for i in range(frontmatter_end + 1, len(lines)):
            if lines[i].startswith('# '):
                found_title = True
                continue
            if found_title and lines[i].strip() and not lines[i].startswith('#'):
                for j in range(i, len(lines)):
                    if not lines[j].strip():
                        first_para_end = j - 1
                        break
                break

    if first_para_end > 0:
        # Add footnote reference
        lines[first_para_end] = lines[first_para_end].rstrip() + '[^1]'

        # Create footnote definition
        footnote_def = f'[^1]: {source_text}'

        # Insert before Lihat Juga
        if lihat_juga_idx > 0:
            lines.insert(lihat_juga_idx, '')
            lines.insert(lihat_juga_idx, footnote_def)
            lines.insert(lihat_juga_idx, '')

        # Remove old source and catatan kaki lines
        lines = [l for l in lines if not (l.startswith('**Sumber:**') or l.startswith('**Catatan kaki:**'))]

        return '\n'.join(lines)

    return content

def process_file(file_path):
    """Process a single markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Skip if already has proper footnotes
        if re.search(r'\[\^\d+\]:', content):
            return 'skip', 'Already has footnotes'

        # Check type of fix needed
        if has_no_footnotes_note(content):
            content = convert_simple_footnote(content)
            fix_type = 'simple'
        elif has_inline_references(content):
            content = convert_inline_references_footnote(content)
            fix_type = 'inline'
        else:
            return 'skip', 'No footnote issues detected'

        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return 'fixed', fix_type
        else:
            return 'unchanged', 'No changes made'

    except Exception as e:
        return 'error', str(e)

def main():
    """Main function - Ralph Loop execution"""
    content_dir = Path(__file__).parent / 'content'

    if not content_dir.exists():
        print(f"Error: Content directory not found: {content_dir}")
        return

    print("=" * 70)
    print("RALPH LOOP FOOTNOTE FIXER - Batch Processing 92 Articles")
    print("=" * 70)
    print()

    # Collect all markdown files
    all_files = []
    for md_file in content_dir.rglob('*.md'):
        if md_file.name != 'index.md':
            all_files.append(md_file)

    print(f"Found {len(all_files)} markdown files to process")
    print()

    # Process files by category
    categories = {
        'fixed': [],
        'skip': [],
        'unchanged': [],
        'error': []
    }

    for i, file_path in enumerate(sorted(all_files), 1):
        rel_path = file_path.relative_to(content_dir)
        print(f"[{i}/{len(all_files)}] Processing: {rel_path}")

        status, detail = process_file(file_path)
        categories[status].append((rel_path, detail))

        if status == 'fixed':
            print(f"  [OK] Fixed ({detail})")
        elif status == 'skip':
            print(f"  [SKIP] Skipped - {detail}")
        elif status == 'error':
            print(f"  [ERROR] Error: {detail}")
        else:
            print(f"  [WARN] {detail}")
        print()

    # Summary report
    print("=" * 70)
    print("RALPH LOOP COMPLETION SUMMARY")
    print("=" * 70)
    print()
    print(f"Total files processed: {len(all_files)}")
    print(f"  [OK] Fixed: {len(categories['fixed'])}")
    print(f"  [SKIP] Skipped: {len(categories['skip'])}")
    print(f"  [WARN] Unchanged: {len(categories['unchanged'])}")
    print(f"  [ERROR] Errors: {len(categories['error'])}")
    print()

    # Detailed breakdown
    if categories['fixed']:
        print("FIXED FILES:")
        for rel_path, detail in categories['fixed']:
            print(f"  - {rel_path} ({detail})")
        print()

    if categories['error']:
        print("ERRORS:")
        for rel_path, detail in categories['error']:
            print(f"  - {rel_path}: {detail}")
        print()

    print("=" * 70)
    print("[SUCCESS] Ralph Loop execution complete!")
    print("=" * 70)

if __name__ == '__main__':
    main()
