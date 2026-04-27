### Incident Postmortem: Click Spike (2026-03-12)
**Summary:** Click volume increased 4.2x due to partner traffic misclassification.  
**Impact:** Elevated invalid traffic filtering and delayed spend reconciliation for 73 campaigns.  
**Root Cause:** Rule deployment omitted exclusion for test inventory IDs.  
**Mitigation:** Rolled back filter set and replayed affected event partitions.  
**Follow-ups:** Add canary validation against historical inventory signature set.  
**Owner:** Fraud Engineering  
**Last Updated:** 2026-03-14

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
