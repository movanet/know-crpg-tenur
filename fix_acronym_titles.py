#!/usr/bin/env python3
"""
Fix Acronym Titles - Convert all-caps acronym titles to italic format
Example: # Bbws → # *BBWS*
"""

import os
import re
from pathlib import Path

# List of known acronyms (2-6 letters, all caps)
KNOWN_ACRONYMS = [
    'BBWS', 'BWS', 'PDAM', 'P3A', 'GP3A', 'PUPR', 'KLHK',
    'TKPSDA', 'HIPPAM', 'AMDAL', 'SIPA', 'SIPPA',
    'RTRW', 'RTTG', 'RAAT', 'MSP', 'KOMIR', 'TPOP'
]

def is_acronym_title(title):
    """Check if title is an acronym (2-6 uppercase letters)"""
    # Remove markdown heading markers and strip
    clean_title = title.replace('#', '').strip()

    # Check if it's 2-6 uppercase letters
    if re.match(r'^[A-Z]{2,6}$', clean_title):
        return True

    # Also check against known acronyms (case-insensitive)
    if clean_title.upper() in KNOWN_ACRONYMS:
        return True

    return False

def fix_acronym_in_file(file_path):
    """Fix acronym titles in a markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    modified = False

    # Track frontmatter
    in_frontmatter = False
    frontmatter_end = -1

    for i, line in enumerate(lines):
        if i == 0 and line.strip() == '---':
            in_frontmatter = True
            continue

        if in_frontmatter and line.strip() == '---':
            frontmatter_end = i
            in_frontmatter = False
            continue

        # Find H1 title (first # after frontmatter)
        if not in_frontmatter and frontmatter_end > 0 and line.startswith('# '):
            title_text = line[2:].strip()

            # Check if it's an acronym
            if is_acronym_title(line):
                # Convert to uppercase and italic
                acronym = title_text.upper()
                new_line = f'# *{acronym}*'

                if line != new_line:
                    print(f"  Fixing: {line.strip()} → {new_line}")
                    lines[i] = new_line
                    modified = True

                    # Also fix in frontmatter title
                    for j in range(frontmatter_end):
                        if lines[j].startswith('title:'):
                            # Update YAML title
                            old_yaml = lines[j]
                            lines[j] = f'title: "*{acronym}*"'
                            print(f"  Updating frontmatter: {old_yaml.strip()} → {lines[j]}")

                            # Add both italic and non-italic to aliases
                            # Find aliases section
                            for k in range(j, frontmatter_end):
                                if lines[k].startswith('aliases:'):
                                    # Check if aliases already exist
                                    alias_start = k
                                    # Find end of aliases
                                    alias_end = k + 1
                                    while alias_end < frontmatter_end and lines[alias_end].startswith('  -'):
                                        alias_end += 1

                                    # Add italic version if not present
                                    italic_alias = f'  - "*{acronym}*"'
                                    non_italic_alias = f'  - "{acronym}"'

                                    has_italic = any(italic_alias.lower() in l.lower() for l in lines[alias_start:alias_end])
                                    has_non_italic = any(f'- "{acronym}"' in l or f"- '{acronym}'" in l for l in lines[alias_start:alias_end])

                                    if not has_italic:
                                        lines.insert(alias_end, italic_alias)
                                        print(f"  Adding alias: {italic_alias}")
                                        modified = True
                                        alias_end += 1

                                    if not has_non_italic:
                                        lines.insert(alias_end, non_italic_alias)
                                        print(f"  Adding alias: {non_italic_alias}")
                                        modified = True

                                    break
                            break
                break

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        return True

    return False

def main():
    """Main function to process all markdown files"""
    content_dir = Path(__file__).parent / 'content'

    if not content_dir.exists():
        print(f"Error: Content directory not found: {content_dir}")
        return

    print(f"Scanning for acronym titles in: {content_dir}")
    print("=" * 60)

    files_modified = 0
    files_scanned = 0

    # Process all markdown files
    for md_file in content_dir.rglob('*.md'):
        if md_file.name == 'index.md':
            continue

        files_scanned += 1
        print(f"\nChecking: {md_file.relative_to(content_dir)}")

        if fix_acronym_in_file(md_file):
            files_modified += 1

    print("\n" + "=" * 60)
    print(f"Scan complete!")
    print(f"Files scanned: {files_scanned}")
    print(f"Files modified: {files_modified}")

    if files_modified > 0:
        print("\n✅ Acronym titles have been converted to italic format")
        print("   Example: # Bbws → # *BBWS*")
    else:
        print("\n✅ No acronym titles found that needed fixing")

if __name__ == '__main__':
    main()
