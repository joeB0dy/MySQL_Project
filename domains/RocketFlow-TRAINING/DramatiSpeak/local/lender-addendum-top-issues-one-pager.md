# Lender Addendum Request Analysis — Top Issues One-Pager

**Dataset: 12,016 addendums received over the past 6 months | Sample analyzed: 182 lender messages**

The addendum requests in this dataset are lender-initiated but **driven by Collateral Underwriter (CU) flags** from Fannie Mae. When CU scores a report and flags risk conditions, lenders are required to address those flags before the loan can be sold to the GSE. The patterns in this analysis therefore reflect not just lender preferences but **systemic issues that CU is consistently identifying** across our appraiser panel.

---

## Top 10 Most Frequent Lender Request Categories

**1. Omitted Proximate/Similar Sales (~42%)** — Lender identifies 1-4 sales within the market area that were not used. Appraiser must add them or provide documented exclusion reasons.

**2. Adjustment Derivation — GLA, Site, Condition, View (~38%)** — Appraiser cited experience rather than including actual paired sales/analysis. GSE investors require extracted market data, not opinion-based statements.

**3. Condition Rating & Adjustment Disputes (~35%)** — Subject rated C3 when C4 may apply; comps with updated kitchens/baths receive no condition adjustment; stated updates are not supported by photos.

**4. Inadequate Support — Distant Sales / 1-Mile Radius (~28%)** — All or most comps are beyond 1 mile. Lender requires a minimum of 1 closed sale within the 1-mile radius supporting the opinion.

**5. Value Increase from Prior Sale — Unexplained (~22%)** — Significant appreciation since the prior sale with no updates documented, in a stable or declining market.

**6. 12-Month GSE Market Data Requirement (~20%)** — 1004MC contains fewer than 12 months of data, or page 1 reflects stable/declining while positive time adjustments are applied on the grid.

**7. Comp Weighting/Reconciliation Contradiction (~18%)** — Most weight given to comps that don't support the opinion, or final value concluded outside the adjusted range without justification.

**8. Amenities Not on Grid (~17%)** — Pool, ADU, workshop, guest house, or casita visible in MLS photos but not reflected on the grid.

**9. Location Adjustment — Different Neighborhoods/Markets (~16%)** — Comps from neighborhoods with materially different predominant values; adjustment is missing or unsupported by market data.

**10. Subject/Comp Condition Rating Accuracy (~15%)** — C2 assigned to a 39+ year old home; basement rooms included in above-grade room count; bath count doesn't match photos.

**Other notable issues:** Ratterman GLA challenge (~12%), report typos/errors (~11%), upload errors/missing pages (~8%), ADU classification (~8%), PUD box not checked (~7%), listing used as comp (~5%), safety issues (~5%).

---

## Issue Patterns by Property Type

**Waterfront/Lake** — View and location adjustment derivation; open water vs. cove/channel differences; linear water feet methodology.

**Rural/Acreage** — Land sales required for site adjustment; workshop/outbuilding adjustment derivation; B&B or farm use disclosure.

**Condo/PUD** — In-complex comp required; PUD box; age-restricted community comparability.

**New Construction** — Resale vs. new construction comp selection; 1-mile radius; bracketing value.

**Urban/Dense Market** — Immediate proximity omitted sales; location adjustment between city neighborhoods.

**High-Value ($1M+)** — Closed sale at or above appraised value; comp weighting justification; GSE standards.

---

## IS IT WORTH CREATING RULES? YES.

The top 3 categories alone account for **35–42% of all 12,016 addendums**. These are systemic and preventable. Estimated addendum reduction potential with rules in place: **30–40%**.

### What the Rules Should Cover

Before submitting, appraisers should confirm: all 1-mile sales considered but excluded are documented; no comp GLA exceeds the subject by more than 35% without a bracket comp; GLA, site, and condition adjustments include actual paired sales or Ratterman analysis (not experience-based statements); subject and comp condition ratings match MLS photos; page 1 market trend matches the 1004MC chart and grid time adjustments; the 1004MC covers a minimum of 12 months; all photos uploaded and basement finish % does not exceed 100%; and if the final value is outside the adjusted range, explicit justification is provided.

---

## DECISION REQUIRED: Who Builds and Owns the Rules?

### Critical Constraint — Fannie Mae Requirement

**Fannie Mae prohibits sharing Collateral Underwriter (CU) data with any third party.** This is non-negotiable. This dataset is derived from CU data, meaning any approach that passes this data to ACI or any external vendor is out of compliance. This constraint is the central driver of the decision below.

### The Three Options

**Option 1 — Build Internally (Rocket Mortgage owns it):** We develop and maintain rules using our own CU data. Rules can be highly precise — tied to the exact thresholds and patterns we see triggering addendums. CU data never leaves our environment. Requires internal resources to build and maintain over time.

**Option 2 — ACI Runs Rules Using Public Data:** We share the rule categories and logic (not CU data) with ACI. ACI builds or validates rules using publicly available appraisal data, GSE guidance, UAD definitions, and industry sources. Fannie Mae compliant, and distributes the maintenance burden. Best suited for rules grounded in published standards (e.g., C2 age requirements per UAD, 12-month 1004MC data per selling guide) — less precise for data-derived thresholds.

**Option 3 — No Formal Rules:** The analysis is used for training and coaching only, with no automated or gated enforcement. No resource investment required, but leaves an estimated 30–40% addendum reduction on the table and provides no accountability mechanism for recurring errors.

### Recommendation

We should build our CU-based rules internally and leverage ACI for our non-CU rules. Internal rules will cover the data-derived thresholds tied directly to CU flag patterns (GLA disparity, distance, adjustment size). ACI can own and maintain rules grounded in published GSE/UAD standards that do not require CU data — keeping us compliant with Fannie Mae's third-party data restriction while distributing the maintenance burden. Option 3 is not recommended given the scale of the confirmed problem.

**Next step:** Align on owner, build timeline, and enforcement point (pre-submission checklist, automated flag, or ACI review trigger).

---
Generated by Rocket Flow · 2.0.8 · 2026-05-21
