# AGENTS.md

## Memory and Learning

Before starting any task:
- At repo root, read `LEARNINGS.md` in full, or create it if it does not exist.
- Apply all entries under `What Has Worked` and `Patterns and Preferences`.
- Avoid all patterns listed under `What Has Failed`.

After completing any task:
- Update `LEARNINGS.md` with new project-specific observations using this format:

```markdown
**[Date] - [Task type]**
- Observation: [what you noticed]
- Action: [what to do or avoid going forward]
- Confidence: [high / medium / low]
```

Do not add:
- Observations already captured in the file.
- General best practices.
- Redundant restatements of existing entries.

## Data Rules

- Do not guess or fabricate data.
- Treat `docs/source_notes/tj psat investigation.xlsx` as seed data.
- Treat the workbook sheet `nsmf 2019` as scratch/untrusted unless a count is independently source-backed.
- A missing school in an incomplete article is not zero.
- Use `verified_zero` only when the source is a complete named list for the relevant geography and class year.
- Treat TJHSST as a single row; do not split TJ students back to base schools.
- Preserve school renames and openings in notes.
- Every numeric NMSF count, including zero, must have source URL, title, date, and source hash.

## Class-Year Mapping

- Class 2019 -> 2017-18 grade 11 enrollment
- Class 2020 -> 2018-19 grade 11 enrollment
- Class 2021 -> 2019-20 grade 11 enrollment
- Class 2022 -> 2020-21 grade 11 enrollment
- Class 2023 -> 2021-22 grade 11 enrollment
- Class 2024 -> 2022-23 grade 11 enrollment
- Class 2025 -> 2023-24 grade 11 enrollment
- Class 2026 -> 2024-25 grade 11 enrollment
