# Task 9 Robustness Checks

Generated: 2026-06-20

## Scope and analysis rules

This report recomputes every numerical result from `data/processed/analysis_panel.csv` rather than copying the Milestone 8 descriptive report. It treats `missing_source` as missing, never as zero. Two distinct estimands are kept separate:

1. **Observed-count totals** sum all source-backed counts, even where enrollment is unavailable.
2. **Covered rates** sum NMSF counts and grade-11 enrollment only over rows with both inputs, then calculate `100 × NMSF / grade-11 enrollment`.

The primary robustness window is Classes 2023-2026. Full-zone count coverage is too incomplete in Classes 2019-2022 for direct zone-wide pre/post comparisons: those years have 48-50 missing NMSF rows each. TJHSST's own 2019-2026 series is complete and is used separately for trend context.

## 1. Coverage

| Class | Count coverage | Rate-compatible coverage | Observed total | Covered rate /100 |
|---|---|---|---|---|
| 2023 | 63/76 (82.9%) | 60/76 (78.9%) | 312 | 0.987 |
| 2024 | 64/76 (84.2%) | 58/76 (76.3%) | 359 | 1.151 |
| 2025 | 71/76 (93.4%) | 64/76 (84.2%) | 288 | 0.871 |
| 2026 | 69/76 (90.8%) | 58/76 (76.3%) | 379 | 1.089 |

Coverage improved sharply for counts by Class 2025, but rate-compatible coverage did not: private-school denominators remain sparse and several public denominators or school-year observations are unavailable. This is why the balanced panels below are the cleanest like-for-like checks.

## 2. Raw counts, normalized rates, and TJHSST inclusion

The table gives `count / rate per 100 grade-11 students` for balanced public panels. Full observed totals in the first two columns are not rate-compatible totals.

| Class | Observed zone incl. TJ | Observed zone excl. TJ | TJHSST count / rate | Balanced base-public count / rate | Balanced public incl. TJ count / rate |
|---|---|---|---|---|---|
| 2023 | 312 | 180 | 132 / 28.633 | 159 / 0.582 | 291 / 1.048 |
| 2024 | 359 | 194 | 165 / 37.415 | 166 / 0.603 | 331 / 1.184 |
| 2025 | 288 | 207 | 81 / 16.071 | 168 / 0.591 | 249 / 0.861 |
| 2026 | 379 | 266 | 113 / 21.606 | 224 / 0.783 | 337 / 1.157 |

The principal discontinuity is not an enrollment artifact. From Class 2024 to Class 2025, TJHSST fell from **165 to 81 semifinalists (-50.9%)** and from **37.415 to 16.071 per 100 juniors (-57.0%)**. Class 2026 rebounded to **113** and **21.606 per 100**, but remained below Class 2024 by **-31.5% in count** and **-42.3% in rate**.

Excluding TJHSST reverses the raw-count direction: observed non-TJ counts rise from 194 in Class 2024 to 207 in Class 2025 and 266 in Class 2026. Because private and other source coverage changes, that raw reversal is not itself a clean time trend. In the balanced 52-school conventional public rate panel, the immediate Class 2025 change is nearly flat: **0.603 to 0.591 per 100 (-2.0%)**. The larger increase appears in Class 2026, to **0.783 (+32.5% versus 2025)**.

## 3. Balanced-panel sensitivity

The balanced count panel includes **58 schools** with source-backed counts in every focal year: 52 conventional public high schools, one public secondary program, 4 private schools, and TJHSST. The balanced public rate panel includes **53 schools** with both counts and enrollment in every year: 52 conventional base public schools plus TJHSST.

Pooled 2023-2024 versus 2025-2026 rates are secondary summaries because they conceal the very different 2025 and 2026 patterns:

| Balanced group | 2023-24 count | 2025-26 count | Count change | 2023-24 pooled rate | 2025-26 pooled rate | Rate change |
|---|---|---|---|---|---|---|
| Balanced public including TJHSST | 622 | 586 | -36 | 1.116 | 1.009 | -9.6% |
| Balanced conventional base public | 325 | 392 | +67 | 0.593 | 0.687 | +16.0% |
| TJHSST | 297 | 194 | -103 | 32.927 | 18.890 | -42.6% |

On this fixed 53-school public panel, base-school counts rise by **67**, arithmetically offsetting **65.0%** of TJHSST's **103-student decline**. The combined public count still falls by **36**. This is an accounting decomposition, not proof that the base-school gains consist of students displaced from TJHSST, and it should not replace the year-by-year results.

The base-school increase is heterogeneous rather than universal. Comparing pooled 2023-2024 and 2025-2026 school rates, **26 of 52 schools increase, 18 decrease, and 8 are unchanged**; the median school change is only **0.011 NMSF per 100 juniors**. Pathway aggregates also vary:

| Pathway | Balanced schools | 2024 rate | 2025 rate | 2026 rate |
|---|---|---|---|---|
| Arlington | 2 | 1.010 | 0.745 | 0.994 |
| FCPS Region 1 | 5 | 1.179 | 1.451 | 2.028 |
| FCPS Region 2 | 5 | 0.790 | 0.705 | 1.268 |
| FCPS Region 3 | 5 | 0.039 | 0.146 | 0.109 |
| FCPS Region 4 | 5 | 0.285 | 0.591 | 0.416 |
| FCPS Region 5 | 4 | 1.222 | 0.896 | 1.312 |
| Loudoun | 13 | 0.995 | 0.756 | 0.982 |
| Prince William | 13 | 0.029 | 0.085 | 0.087 |

The Class 2026 increase is strongest in FCPS Regions 1, 2, and 5. FCPS Region 3 remains low, Region 4 falls from its 2025 spike, and Loudoun is close to its 2024 rate. The aggregate base-school gain should therefore not be described as a uniform zone-wide shift.

## 4. Private-school missingness

| Class | Private count rows observed | Missing rows | Full observed total | Balanced 4-school total | Rate-compatible rows |
|---|---|---|---|---|---|
| 2023 | 4/16 | 12 | 13 | 13 | 2 |
| 2024 | 5/16 | 11 | 18 | 15 | 0 |
| 2025 | 16/16 | 0 | 34 | 15 | 10 |
| 2026 | 10/16 | 6 | 34 | 18 | 0 |

The four complete private schools are Bishop O'Connell, Flint Hill, The Potomac School, and The Madeira School. Their total is **15 in 2024, 15 in 2025, and 18 in 2026**. The apparent full-observed increase from 18 to 34 coincides with coverage expanding from 5 to 16 private schools. It therefore cannot be interpreted as a measured private-school offset. No rate-compatible private panel exists for Classes 2024-2026.

## 5. Excluding non-conventional programs

H-B Woodlawn is the only `public_secondary_program` row. It has no grade-11 denominator in the panel, so it never contributes to a covered rate.

| Class | H-B count | Base-public count incl. program | Count excl. program | Covered conventional-public rate |
|---|---|---|---|---|
| 2023 | 3 | 167 | 164 | 0.559 |
| 2024 | 1 | 176 | 175 | 0.601 |
| 2025 | 3 | 173 | 170 | 0.583 |
| 2026 | 6 | 232 | 226 | 0.738 |

Excluding it changes the observed base-public count by only 1-6 students per year and leaves every covered rate unchanged. The main findings are not driven by the program row.

The 140-row manual-review queue includes 76 duplicate public-school source rows, 37 unresolved school-year source gaps, 11 non-roster rows, 7 TJHSST resident subsets, 5 duplicate private-school rows, 3 former-PWCS TJHSST subsets, and 1 unattributed total. They are not added because doing so could double count schools or TJHSST, turn source gaps into zeros, or mix resident totals with school totals.

## 6. Is Class 2025 isolated?

At TJHSST, Class 2025 is the sharpest break, but Class 2026 is not a return to the earlier range. Across Classes 2019-2024, TJHSST averaged **33.296 NMSF per 100 juniors** on a pooled denominator and never fell below **28.633** or **132 semifinalists**. Class 2026's **21.606 per 100** and **113 semifinalists** remain below both pre-policy minima.

For the balanced base-public panel, by contrast, 2023-2025 are nearly flat (0.582, 0.603, 0.591), followed by a distinct 2026 increase to 0.783. Thus, the evidence does **not** show a smooth post-policy trend. It shows a TJHSST break in 2025, a partial TJHSST rebound in 2026, and a base-school rise concentrated in 2026.

## 7. Virginia cutoff and statewide normalization

More than 16,000 Semifinalists represent less than 1% of U.S. graduating seniors nationally and are named on a state-representational basis.[^nmsc] The canonical panel correctly leaves Virginia cutoff and statewide-total fields as `not_sourced`. For this robustness check only, the following secondary Compass figures are used and kept outside the panel:[^cutoffs][^state]

| Class | VA cutoff | VA total | Balanced public share | Base-public share | TJHSST share |
|---|---|---|---|---|---|
| 2023 | 221 | 397 | 73.3% | 40.1% | 33.2% |
| 2024 | 219 | 467 | 70.9% | 35.5% | 35.3% |
| 2025 | 222 | 394 | 63.2% | 42.6% | 20.6% |
| 2026 | 224 | 489 | 68.9% | 45.8% | 23.1% |

The Class 2026 Virginia cutoff was two Selection Index points higher than Class 2025 (224 versus 222), while the reported statewide semifinalist total rose from 394 to 489. A cutoff-only adjustment is therefore inadequate. On the supplemental statewide denominator, the balanced public share falls from **70.9% in 2024** to **63.2% in 2025** and recovers only to **68.9% in 2026**. TJHSST's share remains far below 2024 (35.3% to 20.6% to 23.1%). These figures strengthen the conclusion that 2026 is a partial, not complete, recovery relative to Virginia, but they remain secondary-source checks.

## 8. COVID, digital testing, and cohort timing

- FCPS provided virtual instruction in spring and fall 2020, then phased in concurrent instruction beginning in February 2021.[^virtual]
- FCPS reopened all schools for five-day in-person learning in August 2021, with 99.5% of students returning in person.[^inperson]
- Class 2025 qualified in fall 2023, the first digital PSAT/NMSQT administration.[^digital]
- Class 2026 qualified in fall 2024, the second digital administration.

The assessment-format break occurs at the same Class 2025 boundary as the TJHSST admissions-policy exposure. Without school-level PSAT participation and score-distribution data, the policy effect cannot be separated cleanly from test-format, participation, cutoff, and cohort-composition changes.

## 9. Admissions mechanism interpretation

The adopted process should not be described as random selection. On December 17, 2020, the Board rejected the proposed “Hybrid Merit Lottery” motion and adopted a holistic-review motion effective for the class entering in fall 2021.[^board] For the Class of 2025, FCPS replaced the prior admissions tests and teacher recommendations, raised the minimum GPA, used essays/holistic review and experience factors, expanded the class toward 550, and provided a 1.5% public-middle-school allocation with remaining seats unallocated.[^court][^profile] An official January 2021 application bulletin confirms the Class 2025 application, eligibility, Student Portrait Sheet, essay, and calendar details.[^class25]

Regulation 3355.14, effective April 28, 2021, is reproduced in the court filing. Regulation 3355.15, effective November 9, 2021, is the best recovered governing regulation for the Class 2026 cycle and explicitly references that class; an official October 2021 bulletin confirms the application window, January 2022 writing administration, and April 29 notification deadline.[^reg15][^class26] The included Regulation 3355.16 became effective May 17, 2022—after the Class 2026 bulletin’s final-notification date—so it should not be applied retroactively to either focal class. The current FCPS process retains holistic evaluation, a 1.5% presumptive allocation, and an unallocated pool.[^current]

The archived annual Notice 3355 documents themselves were not recovered. The official class-specific bulletins recover key calendar and assessment details, while the FCPS index confirms that N3355 exists.[^index] The analysis therefore describes the broad class-specific regimes but does not claim that every implementation detail has been reconstructed or estimate the effect of any single component.

## Robustness conclusion

The TJHSST decline in the first affected class is large in both raw counts and enrollment-normalized rates, and it is not explained by the H-B Woodlawn program or simple enrollment growth. Conventional base-school rates do not show an immediate offset in Class 2025; a substantial increase appears in Class 2026. Combining TJHSST and base schools produces a near return to the 2024 local rate by 2026, but only a partial recovery after supplemental statewide normalization. Private-school data are too incomplete to establish the remaining offset. These are descriptive findings, not causal estimates.

## Generated supporting tables

- `reports/tables/task9_group_year_summary.csv`
- `reports/tables/task9_coverage_2023_2026.csv`
- `reports/tables/task9_balanced_count_panel.csv`
- `reports/tables/task9_balanced_rate_panel.csv`
- `reports/tables/task9_balanced_panel_membership.csv`
- `reports/tables/task9_private_sensitivity.csv`
- `reports/tables/task9_program_sensitivity.csv`
- `reports/tables/task9_manual_review_issue_counts.csv`
- `reports/tables/task9_offset_decomposition.csv`
- `reports/tables/task9_state_normalization_supplemental.csv`
- `reports/tables/task9_cohort_timing.csv`
- `reports/tables/task9_change_summary.csv`
- `reports/tables/task9_balanced_base_school_changes.csv`
- `reports/tables/task9_school_pooled_changes.csv`
- `reports/tables/task9_pathway_rate_sensitivity.csv`

[^nmsc]: National Merit Scholarship Corporation, *Information about the 2026 National Merit Scholarship Competition*, https://www.nationalmerit.org/s/1758/images/gid2/editor_documents/guide_to_the_national_merit_scholarship_program.pdf?gid=2&pgid=61.
[^cutoffs]: Compass Education Group, *Historical National Merit Cutoffs 2008 to Present*, https://www.compassprep.com/historical-national-merit-cutoffs/. Secondary source; not written into the canonical panel.
[^state]: Compass Education Group, *National Merit Semifinalists and Commended Students by State*, https://www.compassprep.com/national-merit-semifinalists-by-state/. Secondary source; not written into the canonical panel.
[^virtual]: Fairfax County Public Schools, *FCPS 2020-21 Evaluation Report*, https://www.fcps.edu/sites/default/files/media/pdf/FCPS_2020_21_Evaluation_Report_0.pdf.
[^inperson]: Fairfax County Public Schools, *FCPS This Week — August 25, 2021*, https://www.fcps.edu/sites/default/files/2022-02/Award%20Vax%20Up%20FCPS%20This%20Week%20-%20August%2025%2C%202021.pdf.
[^digital]: College Board, *How to Get Ready for the Digital PSAT/NMSQT*, https://blog.collegeboard.org/how-get-ready-digital-psat-nmsqt.
[^board]: Fairfax County School Board, December 17, 2020 minutes, https://go.boarddocs.com/vsba/fairfax/Board.nsf/files/BY5JH34D3388/%24file/12-17-20%20ERM%20FINAL.pdf.
[^court]: Fairfax County School Board court filing with the Jeremy Shughart declaration and Regulation 3355.14 exhibit, March 4, 2022, https://www.ffxnow.com/files/2022/03/FCPS-Brief-in-Support-of-Motion-to-Stay-Pending-Appeal.pdf.
[^reg15]: Archived copy of Fairfax County Public Schools Regulation 3355.15, effective November 9, 2021, https://valor-dictus.com/wp-content/uploads/2022/05/R3355.pdf. A local copy is archived at `docs/source_notes/FCPS Regulation 3355.15 TJHSST Admissions.pdf`.
[^class25]: Fairfax County Public Schools, *Invitation to Apply to TJHSST—Class of 2025*, January 29, 2021, https://content.govdelivery.com/accounts/VAEDUFCPS/bulletins/2bd3a3b.
[^class26]: Fairfax County Public Schools, *TJ Admissions—Freshman Application Window Opening—Class of 2026*, October 26, 2021, https://content.govdelivery.com/accounts/VAEDUFCPS/bulletins/2f77379.
[^profile]: TJHSST, *School Profile 2021-22*, https://tjhsst.fcps.edu/sites/default/files/media/inline-files/school-profile%202021-22_0.pdf.
[^current]: Fairfax County Public Schools, *TJHSST Freshman Application Process*, https://www.fcps.edu/about-fcps/registration/tjhsst-admissions/freshman-application-process.
[^index]: Fairfax County School Board, numeric policy index listing R3355 and N3355, https://insys.fcps.edu/schoolboardapps/report_policy/cache/numeric-3000.htm.
