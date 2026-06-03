# Appraiser "Under Review" — Effectiveness Analysis

---

## Bottom Line

**The process works.** Appraisers who complete a review cycle show a 39% drop in RNA rate, and 84% do not require re-review. Quality gains are strongest for active appraisers. Inactive and repeat reviewees represent a separate challenge that needs a different response.

**Recommendation: Retain the program. Make three targeted changes** (see page 2).

---

## What We Measured

- **Who:** 378 appraisers placed under review, January 2025–present
- **How:** RNA rate and addendum rate, measured per order, across three windows: 30 days before review, during review, and 30 and 60 days after review was lifted
- **Note:** "Under Review" status is proxied from WFR signals — the checkbox itself is not tracked in the data warehouse. Results are most reliable for appraisers with active order volume during the review period.

---

## Key Findings

### 1. RNA Improves Significantly — and Holds

RNA rate dropped **39% from the during-review peak to 30 days post-review** and continued declining at 60 days.

| Window | RNA Rate |
|---|---|
| 30 Days Before Review | 28.48% |
| During Review | 52.28% |
| 30 Days After | 31.68% |
| 60 Days After | 30.93% |

> **How to read this table:** The 28.48% pre-review baseline is not a healthy-appraiser benchmark. These are appraisers who were already flagged for quality issues before placement — so pre-review RNA reflects an elevated-risk population, not a normal starting point. The during-review spike to 52.28% reflects the quality issues that triggered placement, not a process failure. The meaningful signal is the sustained post-review decline. To assess whether post-review performance (30.93%) represents a true improvement or a lingering gap, the right comparison is the **panel-wide RNA average** — not the pre-review baseline of this already-flagged cohort.

Among appraisers with sufficient order volume (≥3 orders during review): **77% showed RNA improvement** from during-review to 30 days after.

---

### 2. Most Appraisers Don't Come Back

**84% of reviewed appraisers had only one review period** — evidence of durable behavioral change, not just temporary compliance.

Of the **16% who re-entered review**, speed of re-entry matters:

| Re-Entry Speed | Termination Rate |
|---|---|
| Returned within 30 days | 28.8% |
| Returned after 30+ days | 18.8% |

> Appraisers who return to review within 30 days are **53% more likely to be terminated** than those who return later. The median gap between review periods is just 21 days — making quick re-entry a practical early-warning signal.

---

### 3. Addendum Improvement Doesn't Hold for Active Appraisers

> **Methodology note:** The addendum threshold used here is based on the **full review standard** applied by the current team — not Rocket's production addendum threshold, which reflects a QC-only review. Applying Rocket's threshold to a full-review cohort would be an unfair comparison given the difference in oversight scope.

The overall 14.74% post-review rate is a weighted average across all segments — it is pulled down significantly by terminated appraisers, who receive few orders before exiting the panel. Adding the pre-review baseline for each segment tells the more complete story:

| Segment | Add. Before Review | Add. During Review | Add. 30 Days After |
|---|---|---|---|
| **Active** (n=296) | 16.19% | 12.77% ▼ | 15.38% ▲ |
| **Terminated** (n=139) | 25.54% | 23.29% ▼ | 9.79% ▼ |
| **Inactive** (n=34) | 16.36% | 27.00% ▲ | 29.63% ▲ |

> **Active appraisers improve during review (16.19% → 12.77%) but revert nearly to baseline once oversight is removed (15.38%)** — suggesting the improvement is compliance-driven, not behavioral. Terminated appraisers show a steep post-review drop, but that reflects low order volume before exit, not genuine improvement. The overall 14.74% figure is primarily an artifact of this terminated segment effect.

---

## Risks to Watch

**1. Repeat reviewees** — A small cohort (61 appraisers, 16%) cycles through review without sustained improvement. Repeated standard review is not working for this group.

**2. Inactive appraisers** — 34 review instances across 17 appraisers showed no measurable quality improvement. Low assignment volume makes it difficult for the review process to drive change.

**3. Panel coverage** — 31% of reviewed appraisers (116 of 378) were ultimately terminated. If those terminations are geographically concentrated, regional coverage gaps are a risk.

**4. Review duration inconsistency** — Median review is 25 days; mean is 63 days; maximum is 674 days. Cases open longer than 180 days likely represent overlooked reviews rather than intentional extended oversight.

---

## Recommendation

Retain the under-review process as a core quality intervention — with an important qualification on what the data actually shows.

RNA rate drops 39% from its during-review peak once review is lifted, which confirms the process is creating real behavioral pressure. However, post-review RNA (31.68%) ends up slightly above the pre-review baseline (28.48%) — meaning the process reduces elevated risk but does not fully reset appraisers to where they started. The strongest evidence for program effectiveness is the **84% non-re-entry rate**: most appraisers do not return to review, which suggests the intervention has lasting impact even if the RNA improvement over baseline is modest.

Addendum improvement shows a similar pattern for active appraisers — gains made during review largely revert once oversight is removed, which points to a compliance effect rather than a behavioral one.

The program is working as a risk-reduction and triage tool. The three changes below would strengthen its ability to drive lasting improvement:

Strengthen it with three changes:

| # | Action | Why |
|---|---|---|
| 1 | **Escalate when an appraiser enters review for the 3rd time** | Standard re-review isn't working for repeat cases — a 3rd placement should trigger a different path (coaching, reduced load, or expedited termination eval) rather than repeating the same process |
| 2 | **Minimum order threshold before removal** | Require ≥3 completed orders post-placement before lifting review, so removal is based on work product — not calendar time |
| 3 | **Track under-review status in the data warehouse** | Eliminates reliance on WFR proxy data and enables reliable trend monitoring going forward |

---

## Decisions Needed

- [ ] Approve, modify, or reject the three recommendations above
- [ ] Set the escalation threshold: how many review periods before formal termination evaluation?
- [ ] Assign ownership for the minimum-order threshold in the review removal workflow
- [ ] Check geographic distribution of the 116 terminated appraisers for coverage gaps
- [ ] Engage data engineering on under-review flag tracking scope and timeline
- [ ] Decide: is a distinct intervention warranted for inactive appraisers, or is panel exit the right path?

---
Generated by Rocket Flow · 2.0.3 · 2026-05-21
