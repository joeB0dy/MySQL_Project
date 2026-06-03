# Smart Drama Filtering

**Author:** MG
**Date:** 2026-03-26
**Status:** Draft

---

## Table of Contents

- [Executive Summary](#executive-summary)
- [Problem Statement](#problem-statement)
  - [Current State & Pain Points](#current-state--pain-points)
  - [Impact](#impact)
  - [Existing Solutions](#existing-solutions)
  - [Urgency](#urgency)
- [Solution Concept](#solution-concept)
  - [Core Concept](#core-concept)
  - [Key Differentiators](#key-differentiators)
  - [Success Factors](#success-factors)
  - [Product Vision](#product-vision)
- [Target Users](#target-users)
  - [Primary User Segment](#primary-user-segment)
  - [Secondary User Segment](#secondary-user-segment)
- [Goals & Success Metrics](#goals--success-metrics)
  - [Business Objectives](#business-objectives)
  - [User Success Metrics](#user-success-metrics)
  - [Key Performance Indicators (KPIs)](#key-performance-indicators-kpis)
- [MVP Scope](#mvp-scope)
  - [Core Features (Must Have)](#core-features-must-have)
  - [Out of Scope for MVP](#out-of-scope-for-mvp)
  - [MVP Success Criteria](#mvp-success-criteria)
- [Constraints & Assumptions](#constraints--assumptions)
  - [Constraints](#constraints)
  - [Key Assumptions](#key-assumptions)
- [Risks & Open Questions](#risks--open-questions)
  - [Key Risks](#key-risks)
  - [Open Questions](#open-questions)
  - [Areas Needing Further Research](#areas-needing-further-research)
- [Appendices](#appendices)
  - [A. Research Summary](#a-research-summary)
  - [B. Ideation Session Context](#b-ideation-session-context)
  - [C. References](#c-references)

---

## Executive Summary

An intelligent notification system for DramatiSpeak that uses personalized filtering, confidence-gated alerts, and user-controlled quiet windows to reduce notification fatigue while maintaining high engagement with dramatic pet moments.

### Problem

DramatiSpeak users are experiencing notification fatigue, with open rates declining from 71% to 52% over six weeks and 38% of users disabling notifications completely. Users receive an average of 16 notifications per day, with morning spikes of 7+ notifications before 9am, causing them to either ignore notifications or turn them off entirely.

### Target Market

Existing DramatiSpeak users, particularly those with highly dramatic pets who generate frequent notifications. This includes all persona types (Alyssa "Cat Interpreter," Jordan "Dog Negotiator," Rodriguez Family, Taylor "Pet Influencer"), with special focus on users at risk of notification burnout.

### Key Value Proposition

- **Personalized intelligence**: Filters notifications based on each pet's unique drama baseline, ensuring even "chill pets" generate meaningful alerts while preventing "drama queens" from overwhelming users
- **Quality over quantity**: Confidence-gated notifications ensure users only receive alerts when the system is 85%+ accurate, rebuilding trust in the system
- **User control without FOMO**: Scheduled quiet windows with optional end-of-window summaries let users batch notifications on their terms while staying connected to their pet's dramatic moments

---

## Problem Statement

### Current State & Pain Points

**Current notification behavior:**
- Every dramatic moment triggers a notification regardless of severity or context
- Users receive an average of 16 notifications per day
- Morning peak: 7+ notifications before 9am (breakfast and departure drama)
- Evening peak: 5-6 notifications between 5-8pm (return home and dinner drama)
- No differentiation between Drama Index 45 and Drama Index 92 moments

**User pain points:**
- "I love the translations, but 7 notifications before 9am is too much. My cat is most dramatic in the morning, but I can't check my phone constantly." - Rachel, 30, NYC
- "The notifications lose their magic when there are too many. I want to be surprised, not spammed." - Alyssa, 29, Portland
- Users want quiet hours but don't want to miss important moments
- No way to control notification frequency without completely disabling them

### Impact

**Quantified metrics:**
- Notification open rate declined 27% (from 71% Week 1 → 52% Week 6)
- 38% of pilot users turned notifications OFF completely
- Notification fatigue cited as top user complaint

**Qualitative impacts:**
- Users missing dramatic moments because they've tuned out notifications
- Product loses entertainment value when users disable notifications entirely
- Trust erosion when low-quality moments interrupt users
- Risk to user retention (notification fatigue contributes to "novelty wore off" dropout reason)

### Existing Solutions

**Within DramatiSpeak:**
- Current system has binary control: notifications ON or OFF
- No filtering, batching, or intelligent prioritization
- No personalization based on individual pet behavior
- No user controls for scheduling or frequency management

**User workarounds:**
- 38% turn notifications off and check app manually (losing real-time engagement)
- Users ignore notifications, causing open rate decline
- Some users miss dramatic moments entirely due to notification blindness

### Urgency

**Why now:**
- Pilot data shows clear trend toward disengagement
- 38% of users already opted out of notifications = core product value broken
- Retention risk: Notification fatigue contributes to user churn
- Critical feature gap must be addressed before full launch
- Without solving this, product cannot scale beyond novelty phase

---

## Solution Concept

### Core Concept

Smart Drama Filtering introduces a three-layer intelligent notification system that transforms how DramatiSpeak delivers dramatic moments to users.

**Layer 1: Personalized Baseline Filtering**
The system learns each pet's unique "drama personality" during a 7-day learning period, establishing what's normal versus exceptional for that specific pet. Notifications are triggered when drama falls in the top 30% of moments for that individual pet. This ensures Oliver the Chill Cat (average Drama Index 30) generates meaningful notifications at Drama Index 45+, while Mittens the Drama Queen (average Drama Index 76) only generates notifications at Drama Index 85+. The percentile-based approach prevents both under-notification (chill pets) and over-notification (dramatic pets).

**Layer 2: Confidence-Gated Alerts**
Even when drama qualifies based on personalized baseline, the system checks ML model confidence before sending notifications. High confidence alerts (85%+ accuracy) are sent immediately. Medium confidence alerts (70-84% accuracy) require exceptionally high drama (top 10%) to warrant interruption. Low confidence alerts (<70% accuracy) are logged in-app only, never sent as notifications. This rebuilds user trust by ensuring only high-quality, accurate moments interrupt users.

**Layer 3: User-Controlled Quiet Windows**
Users create scheduled quiet windows (e.g., "Sleep Time" 11pm-7am, "Work Hours" 8am-6pm) with granular control over notification behavior. Each window includes two toggles: (1) Allow Critical Drama Alerts (Drama Index 95+, Confidence 95%+) to break through, and (2) Send summary when window ends. When quiet windows end, users receive a single batched notification summarizing all dramatic moments that occurred, grouped by drama level. Users also have quick-access snooze controls (30min/1hr/2hrs/rest of day) and per-notification snooze actions for spontaneous quiet needs.

### Key Differentiators

- **Adapts to individual pet personalities**: First notification system that recognizes a Drama Index 45 moment can be significant for one pet but noise for another
- **Quality threshold prevents trust erosion**: Unlike generic "Do Not Disturb" features, confidence gating ensures only accurate moments interrupt users
- **Summary notifications eliminate FOMO**: Users can silence notifications without fear of missing important moments—they get a recap on their schedule
- **Three levels of control**: Scheduled windows (recurring), quick snooze (spontaneous), per-notification actions (immediate)—addresses both planned and unplanned quiet needs
- **Critical alert override**: Users decide whether truly exceptional moments (top 1%) can break through quiet windows

### Success Factors

**Why this approach works:**
- Addresses both volume (too many notifications) and quality (low-accuracy interruptions) problems simultaneously
- Respects user context without requiring manual intervention each time
- Maintains real-time engagement for high-value moments while batching lower-priority ones
- Personalization ensures solution scales across diverse pet personalities (from chill to dramatic)
- User control reduces likelihood of complete notification disable (the current workaround)

**What makes it feasible:**
- Leverages existing Drama Index and ML confidence scores—no new data collection required
- 7-day learning period is acceptable based on pilot retention data (most users stay active through Week 1)
- Summary notification format reuses existing translation display logic
- Quiet window scheduling is standard mobile OS functionality

### Product Vision

Smart Drama Filtering transforms DramatiSpeak notifications from a one-size-fits-all broadcast system into an intelligent, adaptive companion that learns each user's preferences and each pet's personality. Over time, the system becomes increasingly personalized, learning not just pet behavior patterns but also user engagement patterns—when they actually open notifications, which drama categories they care about most, and how they balance real-time alerts with batched summaries.

This foundation enables future enhancements like engagement-based learning (adjusting filters based on which notifications users actually open), context-aware filtering (detecting when users are driving or in meetings), and predictive quiet windows (suggesting schedules based on observed behavior patterns). The vision is a notification system that feels like it "just works"—users rarely think about managing it because it naturally adapts to their lifestyle and their pet's personality.

---

## Target Users

### Primary User Segment

**Profile:**
- Existing DramatiSpeak users with active devices (any persona type)
- Particularly those with highly dramatic pets generating 10+ notifications per day
- Ages 24-42, urban/suburban households
- Tech-comfortable users who expect intelligent mobile experiences
- Pet owners who've invested in premium pet tech ($1,200-$3,000/year pet spend)

**Current behaviors and workflows:**
- Check DramatiSpeak app 2-5 times daily (down from initial engagement)
- Notification open rates declining over time (71% → 52% by Week 6)
- 38% have turned off notifications and check app manually instead
- Experience morning notification spikes (7+ before 9am) and evening spikes (5-6 between 5-8pm)
- Share dramatic moments on social media but frequency declining due to notification blindness

**Needs and pain points:**
- Want to stay connected to pet's dramatic moments without constant interruptions
- Need quiet periods (sleep, work, commute) without completely disabling notifications
- Struggle with "all or nothing" notification control (ON vs OFF)
- Fear missing truly exceptional moments if they disable notifications
- Want notifications that feel "worth it"—high drama, high accuracy
- Need system that respects context (morning rush, bedtime, focused work)

**Goals and objectives:**
- Re-enable notifications without feeling overwhelmed
- Maintain entertainment value of DramatiSpeak without disruption
- Feel confident that notifications are accurate and meaningful
- Control when and how they receive dramatic updates
- Avoid missing the "best" dramatic moments while filtering out noise

### Secondary User Segment

**Profile:**
- New DramatiSpeak users (post-launch wave)
- Proactive about managing phone notifications across all apps
- Ages 28-45, power users of productivity and wellness apps
- Already use Do Not Disturb, Focus modes, or notification management tools

**Current behaviors and workflows:**
- Set up notification preferences before using new apps
- Likely to disable notifications if not customizable from the start
- Research app features before purchase/download
- Compare notification management across competing products

**Needs and pain points:**
- Want notification control on Day 1, not after frustration sets in
- Need confidence that app won't spam them
- Expect intelligent notification systems as standard feature
- Want to see how notification management works before committing

**Goals and objectives:**
- Configure notification preferences during onboarding
- Trust that system respects their time and attention
- Use preset quiet window templates that match their lifestyle
- Enable notifications confidently knowing they won't regret it later

---

## Goals & Success Metrics

### Business Objectives

**1. Reduce notification fatigue and re-engage users**
- Target: Increase notification open rate from 52% to 65-70% within 8 weeks of launch
- Success criteria: Open rate stabilizes or increases over time (no decline pattern)

**2. Re-enable notifications for opted-out users**
- Target: Reduce percentage of users with notifications disabled from 38% to <15% within 12 weeks
- Success criteria: 60% of currently opted-out users re-enable notifications after Smart Drama Filtering launch

**3. Improve user retention**
- Target: Reduce "novelty wore off" dropout rate by 50% (from 22% to <11% of dropouts)
- Success criteria: Week 6 retention rate improves from 69% to 80%+

**4. Reduce notification volume while maintaining engagement**
- Target: Decrease average daily notifications from 16 to 3-5 per user
- Success criteria: Daily Active Translations (DAT) metric remains stable (users still check app frequently despite fewer notifications)

### User Success Metrics

**1. Quiet Window adoption**
- Measurement: Percentage of users who create at least one quiet window within first week
- Target: 70%+ adoption rate
- Success indicator: Users finding value in scheduling controls

**2. Summary notification engagement**
- Measurement: Open rate for summary notifications vs. individual notifications
- Target: Summary open rate ≥ 75% (higher than current 52% individual notification rate)
- Success indicator: Users prefer batched summaries over real-time interruptions

**3. Preset template usage**
- Measurement: Percentage of users who use preset quiet window templates (Work Schedule, Sleep Schedule, Home Schedule)
- Target: 85%+ of quiet window creators use at least one preset
- Success indicator: Templates match user needs effectively

**4. Snooze feature utilization**
- Measurement: Percentage of users who use snooze (quick-access or per-notification) at least once per week
- Target: 40%+ weekly active snooze users
- Success indicator: Users taking control of spontaneous quiet needs

### Key Performance Indicators (KPIs)

**1. Notification Quality Score**
- **Definition:** Percentage of notifications that meet both personalized baseline (top 30%) and confidence threshold (85%+)
- **Target:** 95%+ of sent notifications pass both filters by Week 4
- **Measurement:** Backend tracking of filtering logic execution

**2. Notification Open Rate**
- **Definition:** Percentage of notifications opened within 24 hours of delivery
- **Target:** 65-70% by Week 8 (up from current 52%)
- **Measurement:** App analytics tracking notification taps

**3. Notification Volume per User**
- **Definition:** Average number of notifications delivered per active device per day
- **Target:** 3-5 notifications/day (down from 16)
- **Measurement:** Backend notification delivery logs

**4. Users with Notifications Enabled**
- **Definition:** Percentage of active users with notifications turned ON (not disabled at OS or app level)
- **Target:** 85%+ (up from current 62%)
- **Measurement:** App settings + OS permission tracking

**5. Daily Active Translations (DAT)**
- **Definition:** Average dramatic moments translated per active device per day (regardless of notification delivery)
- **Target:** Maintain current levels (3.2 for single-pet households)
- **Measurement:** Backend drama translation logs

**6. User Satisfaction Score (Notifications)**
- **Definition:** User rating of notification experience on 1-5 scale (in-app survey)
- **Target:** 4.2+ average rating by Week 12
- **Measurement:** In-app survey deployed to random 20% sample monthly

**7. Critical Alert Override Usage**
- **Definition:** Percentage of users who enable "Allow Critical Drama Alerts" on at least one quiet window
- **Target:** 50%+ of quiet window users
- **Measurement:** App settings analytics

**8. Feature Discovery Rate**
- **Definition:** Percentage of users who interact with Smart Drama Filtering features (quiet windows, snooze, or summary notifications) within first 2 weeks
- **Target:** 80%+ discovery rate
- **Measurement:** Feature interaction tracking + onboarding flow analytics

---

## MVP Scope

### Core Features (Must Have)

**1. Personalized Baseline Filtering**
- 7-day learning period that tracks all dramatic moments for each pet
- Calculate personalized drama baseline (average and distribution)
- Apply top 30% percentile threshold for notification eligibility
- Display learning period status to users ("We're learning your pet's personality - 3 days left")
- Store baseline data per pet (support for future multi-pet households)
- **Rationale:** Core layer that solves the "Oliver vs Mittens" problem - ensures all pet personalities generate appropriate notification volume

**2. Confidence-Gated Alert System**
- Check ML model confidence score before sending notifications
- High confidence (85%+): Send notification immediately
- Medium confidence (70-84%): Send only if drama is top 10% for that pet
- Low confidence (<70%): Log in app only, never notify
- Display confidence scores in app (transparency builds trust)
- **Rationale:** Addresses accuracy trust issues identified in pilot research; prevents low-quality moments from interrupting users

**3. Scheduled Quiet Windows**
- Create, edit, delete quiet windows with recurring schedules
- Name windows (e.g., "Sleep Time," "Work Hours")
- Set start/end times and days of week
- Two toggles per window: (1) Allow Critical Drama Alerts, (2) Send summary when window ends
- Support multiple concurrent quiet windows
- **Rationale:** Core user control feature that addresses "too many notifications before 9am" pain point

**4. Summary Notifications**
- Generate batched notification when quiet window ends
- Group dramatic moments by level (🔴 top 10%, 🟡 top 30%)
- Show timestamp, drama category, and Drama Index for each moment
- Tap to view full translation in app
- Only send if there were qualifying moments during window
- **Rationale:** Eliminates FOMO - users can silence notifications without missing anything

**5. Critical Drama Alert System**
- Define critical threshold: Drama Index 95+, Confidence 95%+
- Break through quiet windows only if user has enabled "Allow Critical Drama Alerts" toggle
- Visual indicator on notification (🚨 badge or special styling)
- Track critical alert frequency to prevent overuse
- **Rationale:** Gives users confidence they won't miss truly exceptional moments even during quiet windows

**6. Quick Snooze Controls**
- In-app toggle button for instant snooze
- Duration options: 30 minutes / 1 hour / 2 hours / Rest of day
- Display countdown timer showing when snooze expires
- During snooze: suppress all notifications, log drama in app
- **Rationale:** Addresses spontaneous quiet needs (meetings, errands, focus time)

**7. Per-Notification Snooze Actions**
- Snooze action on each notification (iOS/Android notification actions)
- Same duration options as quick snooze
- Independent from quick snooze (both can coexist)
- **Rationale:** Gives users immediate control without opening app

**8. Preset Quiet Window Templates**
- Three preset templates during onboarding or first quiet window creation:
  - "Work Schedule" (Mon-Fri 8am-6pm, critical alerts ON, summary ON)
  - "Sleep Schedule" (Every day 11pm-7am, critical alerts OFF, summary ON)
  - "Home Schedule" (Mon-Fri 6pm-9am + All day weekends, critical alerts OFF, summary OFF)
- User can customize after selecting template
- **Rationale:** Reduces friction for new users; 85% target adoption validates need for smart defaults

**9. Onboarding & Feature Discovery**
- Notification management setup during app onboarding (for new users)
- In-app prompt for existing users explaining Smart Drama Filtering launch
- Tutorial/tooltips for quiet window creation
- Example scenarios showing how filtering works
- **Rationale:** 80% feature discovery target requires proactive education

### Out of Scope for MVP

**Engagement-Based Learning** - Future enhancement that adjusts filters based on which notifications users actually open. Requires months of behavioral data to train effectively. Deprioritized because personalized baseline + confidence gating already address core problem.

**Context-Aware Filtering** - Detecting when users are driving, in meetings, or otherwise occupied via phone sensors. Complex implementation with privacy considerations. Quiet windows + snooze provide sufficient manual control for MVP.

**Predictive Quiet Windows** - System suggests quiet window schedules based on observed patterns. Requires weeks of usage data per user. Preset templates serve this need for MVP.

**Smart Notification Timing** - Delaying notifications to "better" times within a window. Adds complexity without clear user demand. Real-time delivery (when filters pass) is simpler and expected behavior.

**Notification Preview/Testing** - "Test your settings" feature showing what notifications would have been sent with current filters. Nice-to-have but not essential; users will experience filtering naturally within days.

**Per-Category Filtering** - Letting users set different thresholds for different drama categories (e.g., always notify for "Judgmental Cat Mode," higher threshold for "Dramatic Sighing"). Adds UI complexity; confidence gating already de-prioritizes low-accuracy categories.

**Weekly/Monthly Notification Reports** - Analytics showing notification volume trends, open rates, most dramatic times. Useful for power users but not core to solving notification fatigue.

### MVP Success Criteria

The MVP will be considered successful if, within 12 weeks of launch:

- Notification open rate increases to 65%+ (from current 52%)
- Users with notifications disabled drops to <15% (from current 38%)
- 70%+ of users create at least one quiet window
- Average daily notifications decrease to 3-5 per user (from 16)
- Week 6 retention rate improves to 80%+ (from 69%)
- User satisfaction score for notifications reaches 4.0+ out of 5.0

---

## Constraints & Assumptions

### Constraints

**Timeline:**
- Must launch before full product launch (currently in pilot phase)
- Target: 8-10 weeks from development start to production release
- Critical path: Notification fatigue is blocking pilot-to-launch transition
- Cannot delay beyond Q2 2026 without risking retention goals

**Resources:**
- Small development team (startup-stage resources)
- Must balance Smart Drama Filtering with other roadmap priorities (multi-pet support, drama history)
- Backend infrastructure must handle increased computational load (percentile calculations per pet)
- QA resources limited - need phased rollout strategy

**Technical:**
- Must integrate with existing Drama Index calculation system
- Dependent on ML confidence scores being available for all drama categories
- iOS and Android notification APIs have different capabilities for notification actions
- Backend must support per-pet data storage (baseline, percentile thresholds)
- Real-time filtering logic must execute within <100ms (no notification delay perceived)
- Summary notification generation must compile data within 5 seconds of quiet window end

### Key Assumptions

**User behavior assumptions:**
- Users will understand the concept of "learning period" and tolerate 7 days before full filtering activates
- Preset templates ("Work Schedule," "Sleep Schedule," "Home Schedule") match majority user needs
- Users prefer summary notifications over missing dramatic moments entirely
- 30% percentile threshold is appropriate balance (not too restrictive, not too permissive)
- Users will discover and adopt quiet windows within first 2 weeks (80% target assumes proactive onboarding)

**Technical assumptions:**
- ML confidence scores accurately predict translation accuracy
- Existing Drama Index distribution follows normal pattern (allows percentile calculation)
- 7 days of data is sufficient to establish reliable baseline for each pet
- Backend can handle per-notification filtering logic at scale (potentially thousands of concurrent drama moments)
- Mobile app notification permissions remain enabled by users (not blocked at OS level)

**Product assumptions:**
- Confidence-gated filtering (85%+ threshold) won't over-filter to point of no notifications
- Critical alert threshold (Drama Index 95+, Confidence 95%+) occurs frequently enough to be meaningful but rarely enough to respect quiet windows
- Summary notifications are engaging enough to maintain user interest (not seen as "spam digest")
- Personalized filtering solves the problem for both high-drama and low-drama pets (Oliver and Mittens both satisfied)

**Business assumptions:**
- Solving notification fatigue will measurably improve retention (not other factors causing "novelty wore off")
- Users who currently have notifications disabled will re-enable after Smart Drama Filtering launch
- Notification open rate decline can be reversed (not inevitable user behavior pattern)
- Feature complexity doesn't introduce new friction points that offset benefits

---

## Risks & Open Questions

### Key Risks

**1. Over-Filtering Risk**
- **Description:** The combination of personalized baseline (top 30%) + confidence gate (85%+) may filter too aggressively, resulting in too few notifications
- **Potential Impact:** Users receive 0-1 notifications per day and feel disconnected from their pet; defeats purpose of real-time engagement
- **Mitigation:** Monitor notification volume per user in first 2 weeks post-launch; be prepared to adjust thresholds (e.g., top 40% instead of 30%, or lower confidence gate to 80%+); include override setting for power users who want "all drama"

**2. Learning Period Dropout Risk**
- **Description:** 7-day learning period requires users to tolerate current notification volume before benefits activate; may lose users during this window
- **Potential Impact:** Users churn before experiencing Smart Drama Filtering benefits; metrics don't improve because users don't make it to Day 8
- **Mitigation:** Apply temporary conservative filtering during learning period (e.g., only send top 50% + 75% confidence); communicate learning progress daily ("3 days left until personalized filtering activates"); offer quiet windows immediately (don't wait for learning period to complete)

**3. Complexity Risk**
- **Description:** Three-layer system + quiet windows + snooze + critical alerts + summaries = high cognitive load for users
- **Potential Impact:** Users confused by feature set, don't understand how it works, ignore new features entirely, satisfaction doesn't improve
- **Mitigation:** Simplify onboarding with progressive disclosure (introduce features gradually); use preset templates to hide complexity; provide clear tooltips and examples; A/B test simplified vs. full-featured onboarding

**4. Technical Performance Risk**
- **Description:** Per-notification filtering logic (percentile calculation + confidence check + quiet window check) must execute in <100ms; at scale this could impact backend performance
- **Potential Impact:** Notification delays, system slowdowns, increased infrastructure costs, poor user experience
- **Mitigation:** Pre-calculate percentile thresholds during nightly batch jobs (not real-time); cache quiet window schedules in memory; load test filtering logic before full rollout; implement gradual rollout (10% → 50% → 100% over 2 weeks)

**5. Adoption Risk (Quiet Windows)**
- **Description:** If users don't create quiet windows, we only get benefits from Layer 1 and Layer 2 filtering; Layer 3 value unrealized
- **Potential Impact:** Miss 70% quiet window adoption target; summary notifications never experienced; user control benefits limited
- **Mitigation:** Proactive onboarding that prompts quiet window creation; show preview of what summaries look like; in-app nudge after Day 3 if no quiet windows created ("Want to reduce morning notifications? Set up a quiet window"); make preset templates extremely visible

**6. Critical Alert Dilution Risk**
- **Description:** If critical alerts (Drama Index 95+, Confidence 95+) happen too frequently, they lose "critical" meaning and annoy users during quiet windows
- **Potential Impact:** Users disable critical alerts entirely; quiet windows feel violated; trust erosion
- **Mitigation:** Monitor critical alert frequency (target: <5% of total notifications); if threshold too low, adjust to Drama Index 97+ or top 1% instead of fixed threshold; dashboard showing critical alert frequency to users

**7. Existing User Migration Risk**
- **Description:** Rolling out Smart Drama Filtering to existing pilot users who have established notification behaviors; change could confuse or frustrate
- **Potential Impact:** Negative feedback from pilot users; "I preferred the old way" sentiment; churn during transition
- **Mitigation:** Phased rollout (new users first, then existing users); clear communication about what's changing and why; offer "opt-out" to legacy notification behavior for 30 days; in-app changelog explaining benefits

**8. Baseline Shift Risk**
- **Description:** Pet behavior changes over time (e.g., cat becomes more dramatic with age, dog mellows out); static baseline from Week 1 becomes inaccurate
- **Potential Impact:** Filtering becomes less relevant over months; users get too many or too few notifications as pet personality shifts
- **Mitigation:** Recalculate baseline monthly using rolling 30-day window; detect significant baseline shifts and notify user ("Your pet's drama personality has changed - we've adjusted filtering"); allow manual baseline reset

### Open Questions

**1. Should percentile threshold be user-adjustable?**
- Default to 30%, but allow power users to adjust (e.g., 20% for more notifications, 40% for fewer)?
- Risk: Too many options increases complexity
- Benefit: Accommodates diverse user preferences
- **Needs research:** User testing to determine if this adds value or confusion

**2. What's the fallback if confidence scores unavailable?**
- If ML model fails to provide confidence score for a translation, what happens?
- Option A: Default to high confidence (send notification)
- Option B: Default to low confidence (don't send notification)
- Option C: Send notification but mark as "unverified"
- **Needs decision:** Engineering + product alignment on graceful degradation

**3. How do we handle multi-pet households in MVP?**
- MVP spec says "store baseline per pet" for future, but what's actual behavior if user has 2 pets?
- Do we calculate separate baselines and filter independently?
- Do we combine drama into single notification stream?
- **Needs decision:** Scope this explicitly or defer entirely to post-MVP

**4. Should summary notification content differ from individual notifications?**
- Current spec: summaries show same info as individual (timestamp, category, Drama Index)
- Alternative: summaries show aggregate insights ("Your cat had 4 judgmental moments this morning")
- **Needs research:** User preference testing on summary formats

**5. How do we educate existing users without disrupting experience?**
- In-app modal explaining changes?
- Email announcement?
- Gradual feature reveal (Layer 1 first, then Layer 2, then Layer 3)?
- **Needs decision:** Go-to-market strategy for existing pilot users

**6. What if learning period behavior is highly inconsistent?**
- Example: Pet is dramatic Monday-Friday but chill on weekends; 7-day average doesn't capture this pattern
- Do we detect patterns and apply day-of-week specific baselines?
- Do we extend learning period to 14 days?
- **Needs decision:** How sophisticated should baseline calculation be?

**7. Should we A/B test thresholds before committing?**
- Test 30% vs 40% percentile, 85% vs 80% confidence gate, etc.
- Risk: Fragmented user experience, complex to manage
- Benefit: Data-driven optimization before full rollout
- **Needs decision:** Product experimentation strategy

**8. How do we measure "notification quality" beyond open rate?**
- Open rate measures engagement, but not satisfaction
- Should we add post-notification feedback ("Was this notification worth it?")
- Should we track time-to-open (faster = more interesting?)
- **Needs research:** Define qualitative metrics beyond quantitative KPIs

### Areas Needing Further Research

**User research:**
- Test preset templates with target personas to validate naming, schedules, and toggle defaults
- Test summary notification formats (grouped list vs narrative vs visual chart)
- Validate 7-day learning period tolerance (is it too long? too short?)

**Technical feasibility:**
- Load testing for filtering logic at scale (1000+ concurrent notifications)
- iOS vs Android notification action parity (ensure feature works consistently)
- Backend performance benchmarks for percentile calculations

**Competitive analysis:**
- How do other consumer apps handle intelligent notification filtering?
- What best practices exist for "learning period" communication?
- What summary notification patterns are most engaging?

---

## Appendices

### A. Research Summary

**Pilot Study Overview (Nov 4 - Dec 15, 2025)**
- 42 pilot households across 3 cities (NYC, Austin, Portland)
- Mixed methods: quantitative usage data + qualitative interviews
- Species breakdown: 28 cats, 14 dogs

**Key Findings Related to Notification Fatigue:**

**Finding #5: Notification Strategy Needs Refinement**
- Notification open rate declined from 71% (Week 1) to 52% (Week 6)
- Users report "too many notifications" during peak drama times
- 38% of users turned off notifications and check app manually
- "Do Not Disturb" hours feature requested by 62% of users

**User Quotes:**
> "I love the translations, but 7 notifications before 9am is too much. My cat is most dramatic in the morning, but I can't check my phone constantly." - Rachel, 30, NYC

> "I wish I could set 'quiet hours' so I only get notifications when I'm actually home and able to engage." - Mark, 35, Austin

> "The notifications lose their magic when there are too many. I want to be surprised, not spammed." - Alyssa, 29, Portland

**Dropout Analysis:**
22% of pilot dropouts cited "novelty wore off" as primary reason, correlating with notification fatigue patterns observed in Week 5-6.

**Usage Pattern Data:**
- Peak Drama Times:
  - Morning (6-9am): 38% of translations
  - Evening (5-8pm): 31% of translations
  - Midday (12-2pm): 18% of translations
  - Night (8pm-12am): 13% of translations

**Accuracy Perception:**
- Overall ML accuracy: 78% (user-validated thumbs up/down)
- High Accuracy categories (85%+): Judgmental Cat Mode, Attention Deficit Theater
- Moderate Accuracy categories (70-80%): Fake Hunger Alert, Existential Crisis
- Low Accuracy categories (60-70%): Dramatic Sighing, Seasonal Judgment

User feedback indicated accuracy trust is critical: "When it gets it right, it's REALLY right. But when it's wrong, it breaks the magic."

**Multi-Pet Engagement Insight:**
Multi-pet households (4 total in pilot) showed 2.3x engagement (5.7 DAT vs 3.2 single-pet) and 100% retention through Week 6, indicating personalization by pet is valuable.

### B. Ideation Session Context

This PRD was developed following a User Pain Points ideation session (March 26, 2026) that analyzed pilot research data using the following frameworks:
- Jobs-to-be-Done (JTBD) analysis
- User Journey Mapping
- User Segmentation Analysis

The ideation session explored multiple notification filtering approaches:
1. **Static threshold filtering** - Rejected due to inability to accommodate diverse pet personalities
2. **Personalized percentile-based filtering** - Selected as core approach
3. **Confidence-gated alerts** - Added as quality control layer
4. **Quiet windows with summaries** - Selected to address user control needs

Key insight from ideation: The "Oliver vs Mittens problem" - chill pets (Oliver, Drama Index 30) and dramatic pets (Mittens, Drama Index 76) both need appropriate notification volumes, requiring personalization rather than universal thresholds.

### C. References

**Product Data Files:**
- User Research: `product-data/operations/user-research.md`
- User Personas: `product-data/strategy/personas.md`
- Product Overview: `product-data/overview.md`
- Metrics: `product-data/operations/metrics.md`
- Roadmap: `product-data/operations/roadmap.md`

**Related Pilot Data:**
- Pilot Study Methodology (Nov-Dec 2025)
- NPS Score: 64 (above target of 55)
- Overall product validation: 94% of users report device "made them laugh out loud" within first week

---

Generated by Rocket Flow · 1.0.20 · 2026-03-26
