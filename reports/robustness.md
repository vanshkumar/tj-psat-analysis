# Task 9 Robustness Checks

Generated: 2026-06-22

## Scope and analysis rules

This report recomputes every numerical result from `data/processed/analysis_panel.csv` rather than copying the Milestone 8 descriptive report. It treats `missing_source` as missing, never as zero. Two distinct estimands are kept separate:

1. **Observed-count totals** sum all source-backed counts, even where enrollment is unavailable.
2. **Covered rates** sum NMSF counts and grade-11 enrollment only over rows with both inputs, then calculate `100 × NMSF / grade-11 enrollment`.

The primary robustness window is Classes 2023-2026. Full-zone count coverage is too incomplete in Classes 2019-2022 for direct zone-wide pre/post comparisons: those years have 48-50 missing NMSF rows each. TJHSST's own 2019-2026 series is complete and is used separately for trend context.

## 1. Coverage

| Class | Count coverage | Rate-compatible coverage | Observed total | Covered rate /100 |
|---|---|---|---|---|
| 2023 | 76/76 (100.0%) | 69/76 (90.8%) | 323 | 0.995 |
| 2024 | 76/76 (100.0%) | 59/76 (77.6%) | 364 | 1.125 |
| 2025 | 71/76 (93.4%) | 64/76 (84.2%) | 288 | 0.871 |
| 2026 | 76/76 (100.0%) | 59/76 (77.6%) | 385 | 1.096 |

The complete Virginia lists close count coverage for Classes 2023, 2024, and 2026, leaving Class 2025 as the only focal count gap. Rate-compatible coverage is still narrower: private-school denominators remain sparse and several public denominators or school-year observations are unavailable. This is why the balanced panels below are the cleanest like-for-like checks.

## 2. Raw counts, normalized rates, and TJHSST inclusion

The table gives `count / rate per 100 grade-11 students` for balanced public panels. Full observed totals in the first two columns are not rate-compatible totals.

| Class | Observed zone incl. TJ | Observed zone excl. TJ | TJHSST count / rate | Balanced base-public count / rate | Balanced public incl. TJ count / rate |
|---|---|---|---|---|---|
| 2023 | 323 | 191 | 132 / 28.633 | 161 / 0.576 | 293 / 1.031 |
| 2024 | 364 | 199 | 165 / 37.415 | 166 / 0.589 | 331 / 1.156 |
| 2025 | 288 | 207 | 81 / 16.071 | 170 / 0.583 | 251 / 0.847 |
| 2026 | 385 | 272 | 113 / 21.606 | 224 / 0.765 | 337 / 1.131 |

The principal discontinuity is not an enrollment artifact. From Class 2024 to Class 2025, TJHSST fell from **165 to 81 semifinalists (-50.9%)** and from **37.415 to 16.071 per 100 juniors (-57.0%)**. Class 2026 rebounded to **113** and **21.606 per 100**, but remained below Class 2024 by **-31.5% in count** and **-42.3% in rate**.

The same break appears as deconcentration within the local public right tail. TJHSST's share of NMSFs in the balanced public panel falls from **49.8% in Class 2024** to **32.3% in Class 2025** and **33.5% in Class 2026**. This is direct evidence that exceptional PSAT outcomes became less concentrated at TJHSST; it is not evidence about median achievement or school culture as a whole.

Excluding TJHSST reverses the raw-count direction: observed non-TJ counts rise from 199 in Class 2024 to 207 in Class 2025 and 272 in Class 2026. Because private and other source coverage changes, that raw reversal is not itself a clean time trend. In the balanced 53-school conventional public rate panel, the immediate Class 2025 change is nearly flat: **0.589 to 0.583 per 100 (-0.9%)**. The larger increase appears in Class 2026, to **0.765 (+31.2% versus 2025)**.

## 3. Balanced-panel sensitivity

The balanced count panel includes **71 schools** with source-backed counts in every focal year: 53 conventional public high schools, one public secondary program, 16 private schools, and TJHSST. The balanced public rate panel includes **54 schools** with both counts and enrollment in every year: 53 conventional base public schools plus TJHSST.

Pooled 2023-2024 versus 2025-2026 rates are secondary summaries because they conceal the very different 2025 and 2026 patterns:

| Balanced group | 2023-24 count | 2025-26 count | Count change | 2023-24 pooled rate | 2025-26 pooled rate | Rate change |
|---|---|---|---|---|---|---|
| Balanced public including TJHSST | 624 | 588 | -36 | 1.094 | 0.989 | -9.6% |
| Balanced conventional base public | 327 | 394 | +67 | 0.582 | 0.674 | +15.8% |
| TJHSST | 297 | 194 | -103 | 32.927 | 18.890 | -42.6% |

On this fixed 54-school public panel, base-school counts rise by **67**, arithmetically offsetting **65.0%** of TJHSST's **103-student decline**. The combined public count still falls by **36**. This is an accounting decomposition, not proof that the base-school gains consist of students displaced from TJHSST, and it should not replace the year-by-year results.

Raw counts overstate the offset because grade-11 enrollment grows between the two periods. Applying each group's 2023-2024 pooled rate to its actual 2025-2026 enrollment predicts **338.2 TJHSST NMSFs** and **340.3 base-public NMSFs**. The observed values are 194 and 394, implying a **144.2-student TJHSST shortfall** and a **53.7-student base-school excess**. On that rate-standardized basis, the base excess offsets only **37.3%** of the TJHSST shortfall, leaving a component-standardized public shortfall of **90.4**. Using TJHSST's longer 2019-2024 baseline produces a similar offset estimate of **36.3%**. These are descriptive counterfactuals, not causal estimates.

The base-school increase is heterogeneous rather than universal. Comparing pooled 2023-2024 and 2025-2026 school rates, **26 of 53 schools increase, 19 decrease, and 8 are unchanged**; the median school change is only **0.000 NMSF per 100 juniors**. Pathway aggregates also vary:

| Pathway | Balanced schools | 2024 rate | 2025 rate | 2026 rate |
|---|---|---|---|---|
| Arlington | 3 | 0.644 | 0.581 | 0.675 |
| FCPS Region 1 | 5 | 1.179 | 1.451 | 2.028 |
| FCPS Region 2 | 5 | 0.790 | 0.705 | 1.268 |
| FCPS Region 3 | 5 | 0.039 | 0.146 | 0.109 |
| FCPS Region 4 | 5 | 0.285 | 0.591 | 0.416 |
| FCPS Region 5 | 4 | 1.222 | 0.896 | 1.312 |
| Loudoun | 13 | 0.995 | 0.756 | 0.982 |
| Prince William | 13 | 0.029 | 0.085 | 0.087 |

The Class 2026 increase is strongest in FCPS Regions 1, 2, and 5. FCPS Region 3 remains low, Region 4 falls from its 2025 spike, and Loudoun is close to its 2024 rate. The aggregate base-school gain should therefore not be described as a uniform zone-wide shift.

## 4. Private-school count coverage and denominator limits

| Class | Private count rows observed | Missing rows | Full observed total | Balanced 16-school total | Rate-compatible rows |
|---|---|---|---|---|---|
| 2023 | 16/16 | 0 | 24 | 24 | 10 |
| 2024 | 16/16 | 0 | 23 | 23 | 0 |
| 2025 | 16/16 | 0 | 34 | 34 | 10 |
| 2026 | 16/16 | 0 | 35 | 35 | 0 |

All 16 rostered private-school rows now have source-backed focal-period counts after the complete-list integration. Their observed total is **24 in 2023, 23 in 2024, 34 in 2025, and 35 in 2026**. Pooled private counts therefore rise from **47 in Classes 2023-2024 to 69 in Classes 2025-2026**, a **22-student observed count increase** in the rostered private-school bucket.

That is a real private-sector right-tail count signal. The limitation is narrower: counts alone still do not identify enrollment-normalized rates, residency, TJ eligibility, applications, or counterfactual base schools. No rate-compatible private panel exists for Classes 2024-2026 because private denominators remain unavailable in 2024 and 2026.

## 5. Excluding non-conventional programs

H-B Woodlawn is the only `public_secondary_program` row. It has no grade-11 denominator in the panel, so it never contributes to a covered rate.

| Class | H-B count | Base-public count incl. program | Count excl. program | Covered conventional-public rate |
|---|---|---|---|---|
| 2023 | 3 | 167 | 164 | 0.555 |
| 2024 | 1 | 176 | 175 | 0.588 |
| 2025 | 3 | 173 | 170 | 0.583 |
| 2026 | 6 | 237 | 231 | 0.749 |

Excluding it changes the observed base-public count by only 1-6 students per year and leaves every covered rate unchanged. The main findings are not driven by the program row.

The 108-row manual-review queue includes 76 excluded duplicate public school count; 11 excluded nonroster school; 7 excluded tjhsst resident subset; 5 excluded duplicate private school count; 5 missing school year source; 3 excluded tjhsst former pwcs student; 1 source incomplete unattributed total. They are not added because doing so could double count schools or TJHSST, turn source gaps into zeros, or mix resident totals with school totals.

## 6. Is Class 2025 isolated?

At TJHSST, Class 2025 is the sharpest break, but Class 2026 is not a return to the earlier range. Across Classes 2019-2024, TJHSST averaged **33.296 NMSF per 100 juniors** on a pooled denominator and never fell below **28.633** or **132 semifinalists**. Class 2026's **21.606 per 100** and **113 semifinalists** remain below both pre-policy minima.

For the balanced base-public panel, by contrast, 2023-2025 are nearly flat (0.576, 0.589, 0.583), followed by a distinct 2026 increase to 0.765. Thus, the evidence does **not** show a smooth post-policy trend. It shows a TJHSST break in 2025, a partial TJHSST rebound in 2026, and a base-school rise concentrated in 2026.

## 7. Virginia cutoff and statewide normalization

More than 16,000 Semifinalists represent less than 1% of U.S. graduating seniors nationally and are named on a state-representational basis.[^nmsc] The canonical panel now carries source-backed Virginia statewide totals for Classes 2023, 2024, and 2026 from complete NMSC Virginia media lists; the Class 2025 statewide total remains unsourced in the panel. Virginia cutoff values are still supplemental secondary-source checks.[^cutoffs][^state]

| Class | VA cutoff | VA total | Total status | Balanced public share | Base-public share | TJHSST share |
|---|---|---|---|---|---|---|
| 2023 | 221 | 400 | source-backed | 73.2% | 40.2% | 33.0% |
| 2024 | 219 | 470 | source-backed | 70.4% | 35.3% | 35.1% |
| 2025 | 222 | 394 | secondary | 63.7% | 43.1% | 20.6% |
| 2026 | 224 | 494 | source-backed | 68.2% | 45.3% | 22.9% |

Class 2026 statewide-denominator caveat: the committed supplied-list snapshot totals 494, while the public 2026 NMSC guide lists Virginia at 489 semifinalists. Treat statewide shares using the 2026 denominator as provisional until reconciled; local school counts and focal coverage are unchanged.

The Class 2026 Virginia cutoff was two Selection Index points higher than Class 2025 (224 versus 222), while the statewide semifinalist total used here rises from the secondary Class 2025 value of 394 to the source-backed Class 2026 value of 494. A cutoff-only adjustment is therefore inadequate. On this mixed-source statewide denominator, the balanced public share falls from **70.4% in 2024** to **63.7% in 2025** and recovers only to **68.2% in 2026**. TJHSST's share remains far below 2024 (35.1% to 20.6% to 22.9%). These figures strengthen the conclusion that 2026 is a partial, not complete, recovery relative to Virginia, with Class 2025 still relying on a secondary statewide denominator.

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

The TJHSST decline in the first affected class is large in both raw counts and enrollment-normalized rates, and it is not explained by the H-B Woodlawn program or simple enrollment growth. Conventional base-school rates do not show an immediate offset in Class 2025; a substantial increase appears in Class 2026. Combining TJHSST and base schools produces a near return to the 2024 local rate by 2026, but only a partial recovery after supplemental statewide normalization. Private-school counts are now complete and show a material post-period increase, but denominator and eligibility limits prevent interpreting that count increase as a measured displacement offset. These are descriptive findings, not causal estimates.

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
- `reports/tables/task9_rate_standardized_offset_decomposition.csv`
- `reports/tables/task9_public_concentration.csv`
- `reports/tables/task9_state_normalization_supplemental.csv`
- `reports/tables/task9_cohort_timing.csv`
- `reports/tables/task9_change_summary.csv`
- `reports/tables/task9_balanced_base_school_changes.csv`
- `reports/tables/task9_school_pooled_changes.csv`
- `reports/tables/task9_pathway_rate_sensitivity.csv`

[^nmsc]: National Merit Scholarship Corporation, *Information about the 2026 National Merit Scholarship Competition*, https://www.nationalmerit.org/s/1758/images/gid2/editor_documents/guide_to_the_national_merit_scholarship_program.pdf?gid=2&pgid=61.
[^cutoffs]: Compass Education Group, *Historical National Merit Cutoffs 2008 to Present*, https://www.compassprep.com/historical-national-merit-cutoffs/. Secondary source; not written into the canonical panel.
[^state]: Source-backed statewide totals for Classes 2023, 2024, and 2026 come from the complete NMSC Virginia media-list snapshots recorded in `data/sources/virginia_statewide_totals.csv`; Class 2025 uses Compass Education Group's secondary statewide total, https://www.compassprep.com/national-merit-semifinalists-by-state/, only for this supplemental sensitivity table. The 2026 statewide total is pending reconciliation against the public NMSC guide total.
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
