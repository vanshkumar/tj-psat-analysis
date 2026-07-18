# Targeted Grade 11 Enrollment Sources

This directory archives official local and school-profile PDFs used to fill exact
Grade 11 denominators that are unavailable from the project's default CCD/PSS
workflow.

The canonical transcriptions and source metadata are in
`data/sources/targeted_grade11_enrollment.csv`. The APS reports supply H-B
Woodlawn membership for Classes 2023-2026. The BASIS profiles supply the exact
Grade 11 boxes for Classes 2025 and 2026. The Trinity Christian profile supplies
the Class 2024 end-of-Grade-11 cohort of 91, and the Immanuel Christian profile
supplies 49 juniors for Class 2026.

The Class 2023 Loudoun School for Advanced Studies value comes from the official
NCES PSS 2021-22 public-use ZIP. Both same-address PPIN records report `P290=11`
with no imputation flag, so the duplicate identity does not affect that value.
The ZIP is not duplicated here; its official URL and SHA-256 are recorded in the
targeted source CSV.

Profile archive hashes:

- `trinity_christian_2023_24_profile.pdf`:
  `b6e383ecb5face0e9c873bf08e8e6f1c334e7f85189ff186edd175fbef6f2d88`
- `immanuel_christian_2024_25_profile.pdf`:
  `5688d905b23be2f5cea0963dfc3fcdf3e88f2629365ff40e71259de85d8976fb`

Trinity's profile also reports 89 current seniors, but the mapped denominator is
the separately labeled 91 students at the end of Grade 11. No adjacent-year
value or current senior total is substituted.
