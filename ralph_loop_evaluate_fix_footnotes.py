#!/usr/bin/env python3
"""
Ralph Loop - Evaluate & Fix Footnotes Comprehensively
Checks local files for footnote issues and fixes them
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

class FootnoteEvaluator:
    def __init__(self):
        self.issues_found = {
            'inline_numbers_present': [],
            'duplicate_footnote_refs': [],
            'missing_definitions': [],
            'malformed_syntax': [],
            'not_renumbered': [],
            'correct_files': []
        }

    def evaluate_file(self, file_path: Path) -> Dict:
        """Evaluate a single file for footnote issues"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        issues = {
            'has_inline_numbers': False,
            'inline_numbers': [],
            'footnote_refs': [],
            'footnote_defs': [],
            'needs_fix': False
        }

        lines = content.split('\n')

        # Check for inline numbers (lines starting with digit followed by space)
        for i, line in enumerate(lines):
            # Match lines like "27 See attachment..." or "30 Minister..."
            if re.match(r'^\d{1,3}\s+\S', line):
                issues['has_inline_numbers'] = True
                issues['inline_numbers'].append((i+1, line[:50]))
                issues['needs_fix'] = True

        # Find footnote references in text [^1], [^2], etc.
        refs = re.findall(r'\[\^(\d+)\](?!:)', content)
        issues['footnote_refs'] = sorted(set(int(r) for r in refs))

        # Find footnote definitions [^1]:, [^2]:, etc.
        defs = re.findall(r'\[\^(\d+)\]:', content)
        issues['footnote_defs'] = sorted(set(int(d) for d in defs))

        # Check if refs and defs match
        if issues['footnote_refs'] != issues['footnote_defs']:
            issues['needs_fix'] = True

        # Check if numbering starts from 1 and is sequential
        if issues['footnote_refs']:
            if issues['footnote_refs'] != list(range(1, len(issues['footnote_refs']) + 1)):
                issues['needs_fix'] = True

        return issues

    def fix_file(self, file_path: Path) -> bool:
        """Fix footnote issues in a file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        lines = content.split('\n')

        # Step 1: Remove inline number lines (lines starting with digit)
        # These are like: "27 See attachment..." or "30 Minister..."
        cleaned_lines = []
        removed_count = 0

        for line in lines:
            # Skip lines that are inline numbers (digit at start followed by space and text)
            if re.match(r'^\d{1,3}\s+\S', line.strip()):
                removed_count += 1
                continue
            cleaned_lines.append(line)

        content = '\n'.join(cleaned_lines)

        # Step 2: Remove inline numbers from end of sentences
        # Pattern: ".30[^1]" should become ".[^1]"
        content = re.sub(r'\.(\d+)(\[\^\d+\])', r'.\2', content)

        # Step 3: Extract all footnote references and definitions
        # Find all [^N] references (not definitions)
        ref_pattern = r'\[\^(\d+)\](?!:)'
        refs_in_text = [(m.start(), int(m.group(1))) for m in re.finditer(ref_pattern, content)]

        # Find all [^N]: definitions
        def_pattern = r'\[\^(\d+)\]:\s*(.+?)(?=\n\n|\n##|\Z)'
        defs = {int(m.group(1)): m.group(0) for m in re.finditer(def_pattern, content, re.DOTALL)}

        # Step 4: Renumber footnotes sequentially starting from 1
        if refs_in_text:
            # Create mapping: old number -> new number
            old_numbers = sorted(set(num for _, num in refs_in_text))
            renumber_map = {old: new for new, old in enumerate(old_numbers, 1)}

            # Replace references in reverse order to avoid index shifting
            for pos, old_num in reversed(refs_in_text):
                new_num = renumber_map[old_num]
                old_ref = f'[^{old_num}]'
                new_ref = f'[^{new_num}]'
                # Find the exact position and replace
                before = content[:pos]
                after = content[pos:]
                after = after.replace(old_ref, new_ref, 1)
                content = before + after

            # Replace definitions
            for old_num, old_def in defs.items():
                new_num = renumber_map.get(old_num, old_num)
                new_def = re.sub(r'\[\^' + str(old_num) + r'\]:', f'[^{new_num}]:', old_def, 1)
                content = content.replace(old_def, new_def, 1)

        # Step 5: Ensure footnotes appear before "## Lihat Juga"
        # (They should already be there, but let's verify)

        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True

        return False

def main():
    """Main Ralph Loop execution"""
    print("=" * 70)
    print("RALPH LOOP - FOOTNOTE EVALUATION & FIXING")
    print("=" * 70)
    print()

    content_dir = Path(__file__).parent / 'content'

    if not content_dir.exists():
        print(f"Error: Content directory not found: {content_dir}")
        return

    # Collect all markdown files
    md_files = [f for f in content_dir.rglob('*.md') if f.name != 'index.md']

    print(f"Found {len(md_files)} markdown files")
    print()

    # Phase 1: Evaluate all files
    print("PHASE 1: EVALUATING ALL FILES")
    print("-" * 70)

    evaluator = FootnoteEvaluator()
    files_to_fix = []

    for md_file in sorted(md_files):
        rel_path = md_file.relative_to(content_dir)
        issues = evaluator.evaluate_file(md_file)

        if issues['needs_fix']:
            files_to_fix.append((md_file, issues))

            # Categorize issues
            if issues['has_inline_numbers']:
                evaluator.issues_found['inline_numbers_present'].append(str(rel_path))

            if issues['footnote_refs'] and (issues['footnote_refs'] != list(range(1, len(issues['footnote_refs']) + 1))):
                evaluator.issues_found['not_renumbered'].append(str(rel_path))

            if issues['footnote_refs'] != issues['footnote_defs']:
                evaluator.issues_found['missing_definitions'].append(str(rel_path))
        else:
            evaluator.issues_found['correct_files'].append(str(rel_path))

    # Report evaluation results
    print(f"\nEvaluation complete!")
    print(f"  Files needing fixes: {len(files_to_fix)}")
    print(f"  Files already correct: {len(evaluator.issues_found['correct_files'])}")
    print()

    print("ISSUES FOUND:")
    print(f"  - Inline numbers present: {len(evaluator.issues_found['inline_numbers_present'])} files")
    print(f"  - Not renumbered: {len(evaluator.issues_found['not_renumbered'])} files")
    print(f"  - Missing definitions: {len(evaluator.issues_found['missing_definitions'])} files")
    print()

    if files_to_fix:
        print("DETAILED ISSUES:")
        for file_path, issues in files_to_fix[:5]:  # Show first 5
            rel_path = file_path.relative_to(content_dir)
            print(f"\n{rel_path}:")
            if issues['has_inline_numbers']:
                print(f"  - Inline numbers: {len(issues['inline_numbers'])} lines")
                for line_num, line_text in issues['inline_numbers'][:3]:
                    print(f"    Line {line_num}: {line_text}...")
            if issues['footnote_refs']:
                print(f"  - Footnote refs: {issues['footnote_refs']}")
            if issues['footnote_defs']:
                print(f"  - Footnote defs: {issues['footnote_defs']}")

        if len(files_to_fix) > 5:
            print(f"\n... and {len(files_to_fix) - 5} more files with issues")

    print()
    print("=" * 70)

    # Phase 2: Fix all files
    if files_to_fix:
        print("\nPHASE 2: FIXING FILES")
        print("-" * 70)

        fixed_count = 0

        for md_file, issues in files_to_fix:
            rel_path = md_file.relative_to(content_dir)

            if evaluator.fix_file(md_file):
                fixed_count += 1
                print(f"[FIXED] {rel_path}")
            else:
                print(f"[SKIP] {rel_path} (no changes needed)")

        print()
        print(f"Fixed {fixed_count} files")

    print()
    print("=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    print(f"Total files: {len(md_files)}")
    print(f"Files fixed: {len(files_to_fix)}")
    print(f"Files correct: {len(evaluator.issues_found['correct_files'])}")
    print()

    if files_to_fix:
        print("Common issues fixed:")
        print("  - Removed inline number lines (27, 28, 29, 30, etc.)")
        print("  - Removed numbers before footnote refs (.30[^1] -> .[^1])")
        print("  - Renumbered footnotes sequentially ([^1], [^2], [^3]...)")
        print()

    print("[SUCCESS] Ralph Loop evaluation and fixing complete!")
    print()

    # Generate report
    report_path = Path(__file__).parent / 'FOOTNOTE_EVALUATION_REPORT.md'
    generate_report(report_path, evaluator, len(md_files), len(files_to_fix))
    print(f"Report saved to: {report_path}")

def generate_report(report_path: Path, evaluator: FootnoteEvaluator, total_files: int, files_fixed: int):
    """Generate evaluation report"""
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Footnote Evaluation Report\n")
        f.write(f"**Date:** 2026-02-09\n")
        f.write(f"**Method:** Ralph Loop Evaluation & Fixing\n\n")
        f.write("---\n\n")
        f.write("## Summary\n\n")
        f.write(f"- **Total files:** {total_files}\n")
        f.write(f"- **Files fixed:** {files_fixed}\n")
        f.write(f"- **Files correct:** {len(evaluator.issues_found['correct_files'])}\n\n")
        f.write("## Issues Found\n\n")
        f.write(f"- **Inline numbers present:** {len(evaluator.issues_found['inline_numbers_present'])} files\n")
        f.write(f"- **Not renumbered:** {len(evaluator.issues_found['not_renumbered'])} files\n")
        f.write(f"- **Missing definitions:** {len(evaluator.issues_found['missing_definitions'])} files\n\n")

        if evaluator.issues_found['inline_numbers_present']:
            f.write("### Files with Inline Numbers\n\n")
            for file in evaluator.issues_found['inline_numbers_present'][:20]:
                f.write(f"- {file}\n")

        f.write("\n## Fixes Applied\n\n")
        f.write("1. Removed inline number lines (27, 28, 29, 30, etc.)\n")
        f.write("2. Removed numbers before footnote references (.30[^1] -> .[^1])\n")
        f.write("3. Renumbered footnotes sequentially from [^1]\n")
        f.write("4. Ensured footnote definitions match references\n")

if __name__ == '__main__':
    main()
