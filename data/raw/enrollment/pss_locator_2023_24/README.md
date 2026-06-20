# NCES PSS Private School Search 2023-24 Locator Snapshots

This directory stores archived HTML pages from the official NCES Private School
Search locator. The locator footer identifies the source as `PSS Private School
Universe Survey data for the 2023-24 school year`.

These pages are used only as an interim source for Class 2025 private-school
grade-11 denominators. Detail pages expose the enrollment-by-grade table, mapped
to the locator file-layout field `PSS_ENROLL_11`. The pages do not expose
public-use imputation flags such as `F_P290`, so generated rows record
`pss_imputation_flag=not_available_locator`.

Missing search results and ambiguous search results are preserved as blank
denominator rows. They are not interpreted as zero enrollment and are not used
to infer any NMSF count.
