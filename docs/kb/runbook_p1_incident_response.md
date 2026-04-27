### P1 Incident Response Runbook
**Purpose:** Handle platform-critical incidents.  
**Scope:** Revenue-impacting outages and severe data delays.  
**Procedure:**  
1. Declare incident in `#incidents` and assign Incident Commander.  
2. Start timeline and impact statement in first **10 minutes**.  
3. Escalate to on-call engineering, AdOps lead, and status comms owner.  
4. Post update every **15 minutes** until mitigated.  
5. Create postmortem within **48 hours**.  
**Exit Criteria:** Service stable for 30 minutes and backlog cleared.  
**Owner:** SRE  
**Last Updated:** 2026-03-27

**Trigger Conditions:**
- Alert breach, user report, or KPI degradation crossing threshold.

**Roles and Responsibilities:**
- **Primary On-call:** Owns triage and first mitigation.
- **Incident Commander:** Owns coordination and updates.
- **Comms Owner:** Publishes internal/external status messages.

**Decision Points:**
- If customer impact is broad, escalate incident severity.
- If root cause is uncertain, prioritize containment before optimization.

**Verification Checklist:**
- Metrics recovering toward baseline
- Error rate within normal operating range
- Backlog/retry queues drained

**Post-Incident Requirements:**
- Postmortem draft within 48 hours
- At least one prevention action item with owner and deadline

---
