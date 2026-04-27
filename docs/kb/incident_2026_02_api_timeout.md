### Incident Postmortem: API Timeout Burst (2026-02-18)
**Summary:** Elevated 504 errors on campaign update endpoint.  
**Impact:** 12% of update requests failed for 23 minutes.  
**Root Cause:** Downstream dependency timeout increased after DNS failover event.  
**Mitigation:** Introduced circuit breaker and adaptive retry with jitter.  
**Action Item:** Add synthetic checks per region every 60 seconds.  
**Owner:** Core API Team  
**Last Updated:** 2026-02-20

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
