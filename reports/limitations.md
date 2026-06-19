# Task 9 Limitations

Generated: 2026-06-19

## 1. NMSF measures only the extreme right tail

National Merit Semifinalist status identifies a very small group of high scorers: more than 16,000 students, representing less than 1% of U.S. graduating seniors nationally, selected on a state-representational basis.[^nmsc] The outcome is useful for studying the extreme academic right tail, but it does not measure median achievement, classroom engagement, research productivity, student well-being, peer norms, or school culture as a whole.

NMSC itself cautions that its qualifying data do not measure the quality or effectiveness of education within a school, district, or state.[^nmsc] A decline in NMSF cannot by itself establish a decline in “academic culture.” It may be consistent with a change in the concentration or production of very high PSAT Selection Index scores, and nothing broader should be inferred without additional outcomes.

## 2. School-level PSAT participation is missing

The denominator is grade-11 enrollment, not the number of eligible juniors who actually took the PSAT/NMSQT. Schools and districts can differ in test-day participation, absenteeism, alternative testing, and whether all juniors are tested. COVID disrupted schooling and test access, and the panel has no school-year PSAT participation control.[^virtual]

Therefore, `NMSF per 100 juniors` is an outcome-rate proxy, not a direct qualification rate among test takers. A school could change its measured rate because participation changed even if the score distribution among test takers did not.

## 3. Virginia cutoff and test-form changes

Virginia's canonical cutoff and statewide-total columns remain blank with `not_sourced` status. Task 9 uses Compass values only as a clearly labeled supplemental check, not as canonical data. NMSC does not publish a convenient official historical cutoff table, and secondary reports may be revised.

The focal policy boundary also coincides with the 2023 move to the digital PSAT/NMSQT.[^digital] Class 2025 is the first policy-affected TJHSST class and the first digital-PSAT NMSF class. That coincidence makes it impossible, with these data alone, to attribute the break uniquely to admissions policy.

A state cutoff does not fully standardize cohorts. The supplemental data show Virginia's cutoff rising from 222 to 224 between Classes 2025 and 2026 while the reported statewide total also rises markedly. Score-distribution and tie effects can change the number of semifinalists at a given cutoff.

## 4. Incomplete and changing source coverage

The panel is explicit about missingness, but the remaining gaps matter:

- In Classes 2019-2022, 48-50 of 76 rows lack source-backed NMSF counts. Full-zone historical totals are therefore not comparable with 2023-2026.
- Private count coverage is 4/16 schools in 2023, 5/16 in 2024, 16/16 in 2025, and 10/16 in 2026.
- Rate-compatible private coverage is two schools in 2023 and zero in Classes 2024-2026.
- The official LCPS Class 2025 release is total-only and cannot establish school-level counts or zeros; some LCPS school rows remain missing.

The balanced panels improve comparability by holding schools fixed, but they answer a narrower question about continuously observed schools and may not represent omitted schools.

## 5. Private-school inference is especially weak

Private-school location does not prove that a student resided in the TJHSST service area, was eligible for TJHSST, applied to TJHSST, or would otherwise have attended a particular base school. The admissions rule places non-public applicants in the unallocated pool rather than assigning them by the private school's location. The private-school analysis is therefore a geographic outcome bucket, not a measured displacement channel.

Four private schools have complete 2023-2026 counts, and no balanced private rate panel exists. The project cannot estimate a complete private-school offset.

## 6. Grade-11 enrollment is not an admissions allocation denominator

The rate denominator measures the size of the outcome cohort at the high school. TJHSST admissions allocations are based on public schools' eighth-grade populations under the post-2020 process, not on high-school grade-11 enrollment.[^current] These denominators serve different purposes and must not be conflated.

The panel also lacks applicants, eligible applicants, offers, waitpool outcomes, acceptances, enrolled students, allocated/unallocated seat status, and the eighth-grade population inputs used in each admissions cycle. Without those data, the analysis cannot quantify how many high scorers were actually redistributed by the policy.

## 7. TJHSST cannot be reassigned to base schools

TJHSST is one regional school row. District announcements sometimes identify TJ students by residence, former middle school, or cooperating division. Adding those subsets to base-school or district counts would double count the same TJHSST students. The manual-review queue correctly excludes such rows.

Likewise, non-roster programs, homeschool/online categories, and duplicate source snapshots are not added unless their scope and duplication can be resolved.

## 8. Program and school-structure differences

H-B Woodlawn is a public secondary program rather than a conventional base high school and lacks a grade-11 denominator. Excluding it barely changes raw counts and does not change covered rates, but the broader roster still mixes school types with different selection, attendance, and program structures.

School openings, renames, relocations, boundary changes, and grade configurations can affect both counts and denominators. History flags are present, but no model adjusts for every local structural change.

## 9. Admissions-policy history is incomplete

The Class 2025 process is documented through the December 2020 Board minutes, an official January 2021 application bulletin, an FCPS court filing containing Regulation 3355.14, contemporaneous FCPS materials, and the 2021-22 TJHSST profile.[^board][^class25][^court][^profile] The best recovered governing regulation for the Class 2026 process is Regulation 3355.15, supplemented by an official October 2021 application bulletin.[^reg15][^class26]

The included Regulation 3355.16 took effect May 17, 2022, after the posted final-notification date for the Class 2026 cycle, and should not be treated as the governing source for either focal class. Archived annual Notice 3355 documents themselves were not recovered. The class-specific bulletins establish key dates and assessment steps, but not necessarily every implementation detail.

The adopted process was not random selection. The Board rejected the proposed hybrid merit-lottery motion and adopted holistic review; applicants were evaluated and ranked within allocated and unallocated pools.[^board]

## 10. The design is descriptive, not causal

There is no untreated comparison region, no student-level counterfactual, and only two policy-exposed cohorts. The analysis cannot separate:

- admissions-policy effects;
- digital-PSAT and scaling effects;
- Virginia cutoff and statewide score-distribution changes;
- PSAT participation changes;
- COVID and recovery effects;
- enrollment and migration changes;
- base-school program changes; or
- ordinary year-to-year sampling variation.

A causal design would require credible comparison schools/regions, pre-trend assessment, consistent outcomes, participation controls, and preferably student-level or applicant-level data.

## 11. Small numbers and uncertainty

Many schools have zero to a few semifinalists. Percentage changes from a small base are unstable, and school-level rankings can be dominated by one or two students. The reports emphasize pooled groups and fixed-school panels, but they do not calculate formal confidence intervals because the data are not a simple random sample and the main uncertainties are measurement and missingness rather than binomial sampling alone.

## 12. Claim boundary

The defensible claim is narrow: the data describe changes in source-backed NMSF counts and NMSF-per-grade-11-enrollment rates across TJHSST, continuously observed public base schools, and a limited private-school subset. They do not establish changes in median academic performance, student quality, teaching quality, school culture, policy merit, or causation.

[^nmsc]: National Merit Scholarship Corporation, *Information about the 2026 National Merit Scholarship Competition*, https://www.nationalmerit.org/s/1758/images/gid2/editor_documents/guide_to_the_national_merit_scholarship_program.pdf?gid=2&pgid=61.
[^virtual]: Fairfax County Public Schools, *FCPS 2020-21 Evaluation Report*, https://www.fcps.edu/sites/default/files/media/pdf/FCPS_2020_21_Evaluation_Report_0.pdf.
[^digital]: College Board, *How to Get Ready for the Digital PSAT/NMSQT*, https://blog.collegeboard.org/how-get-ready-digital-psat-nmsqt.
[^current]: Fairfax County Public Schools, *TJHSST Freshman Application Process*, https://www.fcps.edu/about-fcps/registration/tjhsst-admissions/freshman-application-process.
[^board]: Fairfax County School Board, December 17, 2020 minutes, https://go.boarddocs.com/vsba/fairfax/Board.nsf/files/BY5JH34D3388/%24file/12-17-20%20ERM%20FINAL.pdf.
[^court]: Fairfax County School Board court filing with Regulation 3355.14 and declarations, March 4, 2022, https://www.ffxnow.com/files/2022/03/FCPS-Brief-in-Support-of-Motion-to-Stay-Pending-Appeal.pdf.
[^reg15]: Archived copy of Fairfax County Public Schools Regulation 3355.15, effective November 9, 2021, https://valor-dictus.com/wp-content/uploads/2022/05/R3355.pdf.
[^class25]: Fairfax County Public Schools, *Invitation to Apply to TJHSST—Class of 2025*, January 29, 2021, https://content.govdelivery.com/accounts/VAEDUFCPS/bulletins/2bd3a3b.
[^class26]: Fairfax County Public Schools, *TJ Admissions—Freshman Application Window Opening—Class of 2026*, October 26, 2021, https://content.govdelivery.com/accounts/VAEDUFCPS/bulletins/2f77379.
[^profile]: TJHSST, *School Profile 2021-22*, https://tjhsst.fcps.edu/sites/default/files/media/inline-files/school-profile%202021-22_0.pdf.
