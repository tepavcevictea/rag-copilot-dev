### Access Control Matrix
Roles:
- `support_read`: read support cases, no billing edits  
- `finance_read_write`: billing adjustments and credits  
- `compliance_sensitive_read`: KYC and sensitive profile access  
- `admin_ops`: incident and platform control actions  
Principle:
- Least privilege by default; temporary elevation requires ticket and expiry.  
**Owner:** Security Governance  
**Last Updated:** 2026-02-08

**Security Controls:**
- Enforce least privilege and time-bounded elevated access.
- Log sensitive operations with immutable audit trail where feasible.

**Review Cadence:**
- Quarterly control review with Security + Engineering + Compliance.
- Immediate review after any incident involving data exposure risk.

**Evidence Requirements:**
- Access logs, approval records, and remediation proof for exceptions.

---
