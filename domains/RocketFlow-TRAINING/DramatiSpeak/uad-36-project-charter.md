# Project Charter: UAD 3.6 Implementation for Appraisal Orders

## Project Overview

This project covers the implementation of UAD 3.6 appraisal report standards for conventional appraisal orders, including a phased pilot program, mandatory GSE cutover compliance, product naming updates, and assignment requirements.

---

## Problem Statement

The GSEs (Fannie Mae / Freddie Mac) are mandating the transition from UAD 2.6 to UAD 3.6 for all conventional appraisal submissions. Rocket Mortgage and its AMC operations must adapt internal systems, assignment logic, engagement letter workflows, appraiser panels, and product configurations to meet these deadlines while minimizing disruption to appraisal volume and quality.

---

## Goals & Objectives

1. **Pilot Launch (September 2026):** Go live with a UAD 3.6 pilot using existing UAD Limited checkbox as the pilot flag, restricting participating appraisers to 3.6 report submissions and routing 3.6 engagement letters to them.
2. **Mandatory Cutover Compliance (November 1, 2026):** Stop accepting new UAD 2.6 primary orders by November 1, 2026; support revisions only for orders submitted before this date.
3. **Pipeline Clearance (May 3, 2027):** Fully retire UAD 2.6 by May 3, 2027; all active pipeline must be resolved.
4. **Product Name Cleanup:** Remove form numbers from conventional product type names across the system, app, and portal.
5. **Reporting Readiness:** Ensure appraiser profile management reporting includes UAD Limited and UAD 3.6 fields for pilot tracking.
6. **Legal Compliance:** Confirm engagement letter and auto-confirmation language meets legal requirements for the pilot.

---

## Scope

### In Scope
- UAD 3.6 pilot program using the existing UAD Limited checkbox
- Engagement letter updates to show 3.6 requirements post-appraiser assignment
- Product name updates: remove form numbers from conventional product types
- Appraiser panel management: checkbox-based manual opt-in for pilot participation
- Reporting updates to include UAD Limited and UAD 3.6 profile fields
- Appraiser communication plan for pilot and mandatory cutover
- Legal review of pilot agreement, disclosure, and engagement letter language

### Out of Scope
- FHA appraisal orders (remain on UAD 2.6)
- Changes to auto-assignment logic (existing Partner Express checkbox handles exclusion from opportunity)
- New system tiers or logic layers for the two-month pilot period

---

## Timeline & Milestones

| Milestone | Target Date |
|---|---|
| Pilot go-live with UAD 3.6 Limited flag | September 2026 |
| Last date to accept new UAD 2.6 primary orders | November 1, 2026 |
| Retire UAD Limited (pilot) checkbox | November 2, 2026 |
| Full UAD 2.6 retirement / pipeline cleared | May 3, 2027 |

---

## Stakeholders & Roles

| Name | Role | Responsibilities |
|---|---|---|
| DelToro | Product Owner / PM | Product name updates, Rocket pilot structure clarification, appraiser communication, coordinate recruiting backup |
| Johnson | Engineering / QA | Test form number removal in portal & app; update maintenance screen product names; coordinate rollout timing |
| Cantlon | Engineering / Workflow | Confirm engagement letter update trigger in assignment/acceptance workflow; communicate technical requirements |
| Heard | Reporting | Update appraisal profile management report to include UAD Limited and UAD 3.6 fields |
| LaKisha | Operations | Review and verify product list for form number removal; confirm naming conventions |
| Sabbaghzadeh, Judith | AMC Operations Lead | Oversee assignment logic, engagement letter shift to documents team, legal coordination |
| Legal (Bree) | Legal | Review pilot agreement, disclosure, and engagement letter language for auto-confirmed orders |
| Crystal's Team | Reporting / Data | Collaborate on reporting updates for UAD Limited and UAD 3.6 checkbox tracking |
| Davina's Team | Appraiser Recruiting | Backup recruiting plan in the event of appraiser attrition due to UAD 3.6 mandate |

---

## Key Decisions Made

- **No new assignment logic:** Use existing Partner Express (PE) and AutoConfirm checkboxes to control order routing; manually check UAD 3.6 boxes for pilot appraisers.
- **Pilot flag:** Use the existing UAD 3.6 Limited checkbox as the pilot identifier; retire it after November 2, 2026.
- **Engagement letters:** Letters automatically update to show 3.6 requirements after appraiser assignment; no pre-assignment logic change needed.
- **Form numbers:** Remove form numbers from conventional product names in the system and portal; test before deploying.
- **Appraiser choice at cutover:** Appraisers will not have a choice about completing 3.6 orders at mandatory cutover; those who cannot comply must contact the team to be removed from conventional assignments.

---

## Open Questions

| # | Question | Owner | Status |
|---|---|---|---|
| 1 | At what point in the assignment/acceptance workflow does the engagement letter update from 2.6 to 2.6/3.6? | Cantlon | Open |
| 2 | How will Rocket structure the UAD 3.6 pilot — by market, volume, or appraiser selection? What are their specific participation requirements? | DelToro | Open |
| 3 | Is a pilot agreement or formal disclosure required for appraisers participating in the pilot, especially for auto-confirmed orders? | Sabbaghzadeh / Legal (Bree) | Open |
| 4 | What percentage of orders will Rocket require to be UAD 3.6 during the pilot period? | DelToro / Rocket | Open |

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Appraiser attrition due to 3.6 mandate | Medium | High | Coordinate with Davina's team on recruiting contingency plan |
| Hard-coded form numbers not caught in testing | Low | Medium | Johnson to perform thorough testing across portal and app before go-live |
| Legal language gaps in engagement letters for auto-confirmed orders | Medium | High | Sabbaghzadeh to confirm with Bree before pilot launch |
| Rocket pilot structure requirements unknown | Medium | Medium | DelToro to communicate with Rocket early to confirm structure and volume expectations |
| Pipeline not cleared by May 3, 2027 | Low | High | Monitor pipeline from November 2026 onward; escalate early if backlog grows |

---

## Next Steps

- [ ] **Cantlon** — Confirm engagement letter update trigger point and communicate technical requirements to team
- [ ] **DelToro** — Update product names to remove form numbers for conventional products; coordinate with Johnson
- [ ] **DelToro** — Communicate with Rocket to clarify pilot structure and confirm participation requirements
- [ ] **DelToro** — Draft and send appraiser communication regarding mandatory cutover; coordinate with legal for language
- [ ] **DelToro** — Coordinate with Davina's team on recruiting contingency for appraiser attrition
- [ ] **DelToro & Heard** — Schedule working session with Crystal's team to update reporting for UAD Limited and UAD 3.6 fields
- [ ] **Heard** — Update appraisal profile management report to include UAD Limited and UAD 3.6 profile fields
- [ ] **Johnson** — Test form number removal in portal and app; confirm no hard-coded numbers remain
- [ ] **Johnson** — Plan timing for maintenance screen product name updates; coordinate with DelToro
- [ ] **LaKisha** — Review product list from Johnson; verify all relevant types identified and naming is correct
- [ ] **Sabbaghzadeh** — Check with Bree (legal) on pilot agreement/disclosure requirements for auto-confirmed orders
- [ ] **Team** — Discuss UAD 3.6 transition and opt-out process in next webinar or appraiser communication

---

Generated by Rocket Flow · 2.0.9 · 2026-05-26
