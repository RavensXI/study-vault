# Edexcel GCSE Computer Science (1CP2) — Programming with Python unit v. the Programming Language Subset

Checked 13 Sep 2026 against PLS Version 6 (Summer 2025), the latest issued. Pearson's rule: the PLS "will be valid for the lifetime of the qualification" and any update is published by 31 January of the exam year — so v6 governs summer 2027 unless a v7 appears by 31 Jan 2027. Re-check the Pearson exam-materials page in February 2027.

Sources: PLS v6 https://qualifications.pearson.com/content/dam/pdf/GCSE/Computer%20Science/2020/exam-materials/1cp2-02-programming-language-subset-pls-version-6-summer-2025.pdf · PLS v5 (Summer 2024) · summary of changes 2025.

## Verdict

Not fit for the 2027 series as it stands. The repair is bounded (edits to four lessons), but coverage is about half the PLS by volume. Two-stage fix: correct the errors, then add two lessons (string formatting; library modules incl. turtle).

## Errors — content the PLS does not contain (students taught what Paper 2 never uses)

1. **Dictionaries taught as the record type (L1, L4, L5).** PLS: "record — A sequence of items, usually of mixed data types — list"; "a list of records, each record will have the same number of fields". The word "dictionary" appears in neither the PLS nor the spec. Affects L1 definition, L4's `student = {...}` example, "Worked Example — A List of Records", practice Q2, Q5 (`print(student.name)`), Q6, the match card `record["key"]`, and L5's `users = {...}` login example.
2. **`with open(...) as f:` (L5).** PLS lists `open, close, read, write, append` and `<fileid>.close ()`; no `with`. A practice mark scheme and a knowledge check credit `with`; `close()` is never taught.
3. **Negative indexing (L3, L4).** PLS: "Sequences start with an index of zero"; no negative index anywhere.
4. **`global` keyword (L6).** PLS scopes by indentation and subprogram calls; no keyword.
5. **`print(value, end=" ")` (L4).** PLS gives only `print (<item>)`; no keyword arguments.
6. **`sum()` in a mark scheme (L4 Q3).** PLS built-ins are a closed list: bool, chr, float, input, int, len, ord, print, range, round, str.
7. **`in` as a membership test (L5).** PLS uses `in` only in `for` loops; relational operators are ==, !=, >, >=, <, <=.
8. (minor) Multi-argument and zero-argument `print()` throughout; PLS shows one item. Low priority: the spec still awards marks for valid off-PLS constructs.

## Wrong claims about Python

- L1: "A `char` stores exactly one symbol… written in single quotes." Python has no char type; PLS maps character → str. The match card pairs `'Z'` with "Char".
- L3: "seven arithmetic operators… four familiar… the other two are // and %, plus **" — the count is wrong (three others).
- L3, L4: output comments show quotes (`# "C"`, `# "LONDON"`) that `print` does not produce; the same lesson says Booleans print with no quotes.
- L5 practice Q6 asks for validation v. **verification** and marks "double-entry"; the lesson never defines verification and the spec uses validation (6.4.3) and authentication (6.4.4).

## Gaps — PLS content the unit never mentions

- Conversion: `bool()`, `list()`; character → str mapping.
- Records as lists; "no ragged data structures".
- Three-argument `range(start, stop, step)` and negative step.
- Files: `close()`, `readlines()`, `writelines()`.
- Built-ins: `round(x, n)` ("uses the 0.5 rule"), `chr()`, `ord()`.
- Lists: `del list[i]`, `.insert(i, item)`, `list()`.
- Strings: `.find()`, `.index()`, `.isalnum()`, `.replace()`, `.isupper()`, `.islower()`, `.format()`.
- **String formatting** — the whole section: `{:<align><sign><width>.<precision><type>}`, the `layout = "{:>10} {:^5d} {:7.4f}"` example, `*` for repeated characters.
- **Library modules**: `random.randint`, `random.random`, `math.ceil`, `math.floor`, `math.pi`, `time.sleep` (only `math.sqrt` appears, in one sentence).
- **Turtle graphics** — the whole module (~25 subprograms, three pages of the PLS).
- Line continuation (backslash; inside `()`/`[]`); `"\r"` and the CR/LF table.

## v5 → v6 changes

None breaks the unit: dimensions table expanded (we teach 1D/2D lists correctly), `.format` reworded (we teach no formatting), bracket spacing and turtle wording (we teach no turtle), input/print rewording (no impact).

## Proposed fix (awaiting Tom)

Stage 1 — surgical corrections to L1, L3, L4, L5, L6 via the api_build applyfixes prompt (records → lists, open/close, drop negative indexing / global / end= / sum() / membership `in`, fix char and operator-count claims, fix output comments, replace Q6 verification with authentication). Re-narrate the changed lessons.
Stage 2 — two new lessons: L7 "Formatting Output: .format, Alignment and Precision" and L8 "Library Modules: random, math, time and turtle". Batch API, fact-checked against the PLS text. Estimated spend for both stages: under £6.
