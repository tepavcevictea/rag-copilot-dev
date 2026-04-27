### Prompt Injection Handling Guidelines
**Purpose:** Reduce risk from malicious input in AI features.  
**Rules:**  
- Treat uploaded content as untrusted.  
- Never execute instructions found in documents.  
- System prompt must enforce "use only retrieved evidence".  
- If evidence conflicts or is missing, return uncertainty response.  
**Owner:** AI Safety Working Group  
**Last Updated:** 2026-03-24

**Security Controls:**
- Enforce least privilege and time-bounded elevated access.
- Log sensitive operations with immutable audit trail where feasible.

**Review Cadence:**
- Quarterly control review with Security + Engineering + Compliance.
- Immediate review after any incident involving data exposure risk.

**Evidence Requirements:**
- Access logs, approval records, and remediation proof for exceptions.

---
