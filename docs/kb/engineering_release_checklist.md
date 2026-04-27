### Engineering Release Checklist
Before release:
- Unit and integration test suites pass.
- Backward compatibility checks pass for public API.
- Rollback plan documented and tested.
- Alert thresholds reviewed with on-call.
- Release note and support macro prepared.
**Owner:** Engineering Enablement  
**Last Updated:** 2026-01-11

**Operational Expectations:**
- Changes must be traceable from ticket -> PR -> deploy.
- Rollback path must be documented before production release.

**Readiness Criteria:**
- On-call aware of release risk and alert changes.
- Dependencies and version constraints documented.

**Metrics to Track:**
- Change failure rate
- Mean time to recovery (MTTR)
- Deployment frequency

---
