### Incident Postmortem: Delayed Reporting (2026-04-03)
**Summary:** Dashboard reporting delayed up to 52 minutes.  
**Impact:** Support load increased by 31 tickets; delivery unaffected.  
**Root Cause:** Stream processor checkpoint lag after schema migration.  
**Mitigation:** Backfilled with replay window and introduced migration pre-check gate.  
**Action Item:** Alert at 8-minute lag threshold instead of 15 minutes.  
**Owner:** Data Platform  
**Last Updated:** 2026-04-05

**Detection:**
- First detected via monitoring alerts and support ticket spike correlation.

**Timeline Standards:**
- Include detection, declaration, mitigation, and full recovery timestamps.
- Track customer communication timestamps separately.

**Blast Radius Assessment:**
- Region(s) impacted
- Account tiers impacted
- Functional surfaces affected (API, dashboard, billing, delivery)

**Prevention Plan Quality:**
- Every action item needs owner, due date, and validation signal.
- Prefer systemic prevention over manual process reminders.

---
