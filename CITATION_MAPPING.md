# Document Title Citation Mapping

## Source Documents - Proper Titles

### Document 1: Annex 7
**File names (INCORRECT):**
- `Annex7`
- `Annex 7`
- `Annex 7_Indonesia Water Tenure Analysis.docx.md`

**Proper title (CORRECT):**
```
Al'Afghani, M.M. (2022). Water Tenure in Indonesia.
```

**Citation format in footnotes:**
```markdown
[^1]: Al'Afghani, M.M. (2022). *Water Tenure in Indonesia*, Section: [Section Name].
```

---

### Document 2: Assessment Guide
**File names (INCORRECT):**
- `Assessment Guide`
- `Water tenure Assessment Guide.pdf`

**Proper title (CORRECT):**
```
FAO. (2016). Water Tenure Assessment Guide. Rome: Food and Agriculture Organization of the United Nations.
```

**Citation format in footnotes:**
```markdown
[^1]: FAO. (2016). *Water Tenure Assessment Guide*, Section: [Section Name].
```

---

## Replacement Rules for Ralph Loop

### Pattern 1: Annex 7 variations
**Find:**
- `Annex7, Section:`
- `Annex 7, Section:`
- `Annex 7_Indonesia Water Tenure Analysis.docx.md, Section:`
- `Annex 7 Indonesia Water Tenure Analysis, bagian`
- `Annex 7, Diagram`

**Replace with:**
```
Al'Afghani, M.M. (2022). *Water Tenure in Indonesia*, Section:
```

### Pattern 2: Assessment Guide variations
**Find:**
- `Assessment Guide, Section:`
- `Water Tenure Assessment Guide, Section:`

**Replace with:**
```
FAO. (2016). *Water Tenure Assessment Guide*, Section:
```

### Pattern 3: Full FAO citation (already correct)
**Keep as is:**
```
FAO. (2016). *Water Tenure Assessment Guide*. Rome: Food and Agriculture Organization of the United Nations.
```

---

## Examples of Correct Citations

### Example 1: Simple section reference
**Before:**
```markdown
[^1]: Annex7, Section: De Minimis Rights
```

**After:**
```markdown
[^1]: Al'Afghani, M.M. (2022). *Water Tenure in Indonesia*, Section: De Minimis Rights.
```

### Example 2: Table reference
**Before:**
```markdown
[^1]: Annex 7_Indonesia Water Tenure Analysis.docx.md, Section: **Table 2: Distribution of responsibilities of river basin territories (WS)27**
```

**After:**
```markdown
[^1]: Al'Afghani, M.M. (2022). *Water Tenure in Indonesia*, Table 2: Distribution of responsibilities of river basin territories (WS).
```

### Example 3: Assessment Guide
**Before:**
```markdown
[^1]: Assessment Guide, Section: Customary Rights
```

**After:**
```markdown
[^1]: FAO. (2016). *Water Tenure Assessment Guide*, Section: Customary Rights.
```

### Example 4: Multiple references (sipa.md example)
**Before:**
```markdown
[^1]: Annex 7, UU 17/2019 Pasal 50
[^2]: Annex 7, UU 17/2019 Pasal 45
[^3]: Annex 7, Permenkes 2/2023 Lampiran I
[^4]: Annex 7 Indonesia Water Tenure Analysis, bagian "Modern permit-based formal water rights"
```

**After:**
```markdown
[^1]: Al'Afghani, M.M. (2022). *Water Tenure in Indonesia*; UU 17/2019 Pasal 50.
[^2]: Al'Afghani, M.M. (2022). *Water Tenure in Indonesia*; UU 17/2019 Pasal 45.
[^3]: Al'Afghani, M.M. (2022). *Water Tenure in Indonesia*; Permenkes 2/2023 Lampiran I.
[^4]: Al'Afghani, M.M. (2022). *Water Tenure in Indonesia*, Section: Modern permit-based formal water rights.
```

---

## Special Cases

### Indonesian language citations (bagian = section)
**Before:**
```markdown
Annex 7, bagian "Modern permit-based formal water rights"
```

**After:**
```markdown
Al'Afghani, M.M. (2022). *Water Tenure in Indonesia*, bagian Modern permit-based formal water rights.
```

### Diagram references
**Before:**
```markdown
Annex 7, Diagram 1. Modul Rencana Alokasi Air Tahunan
```

**After:**
```markdown
Al'Afghani, M.M. (2022). *Water Tenure in Indonesia*, Diagram 1: Modul Rencana Alokasi Air Tahunan.
```

---

## Quality Standards

All citations must:
1. ✅ Use proper document title (not filename)
2. ✅ Include author and year for academic work
3. ✅ Use italics for document title (*Water Tenure in Indonesia*)
4. ✅ Use "Section:" for section references
5. ✅ Use "Table X:" for table references
6. ✅ Use "Figure X:" for figure references
7. ✅ Use "Diagram X:" for diagram references
8. ✅ End with period (.)

---

**Status:** Ready for Ralph Loop batch processing
**Files to process:** 92 articles
**Expected time:** 30-45 minutes
