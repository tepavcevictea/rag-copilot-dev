### Product Guide: Targeting Options
**Purpose:** Explain audience and placement targeting controls.  
**Scope:** Campaign creation flow.  
**Options:**  
- Geo (country, region, city for eligible exchanges)  
- Device type, OS, browser version bands  
- Topic segments and exclusion lists  
- Schedule windows in advertiser timezone  
**Notes:** Overly narrow targeting may significantly reduce delivery.  
**Owner:** Product Marketing  
**Last Updated:** 2026-03-11

**Primary Users:**
- Self-serve advertisers, managed service teams, and support agents.

**Configuration Constraints:**
- Validate required fields before save/publish.
- Reject invalid combinations with user-readable reasons.

**Failure Modes to Watch:**
- Silent default values creating unexpected behavior.
- Misaligned timezone assumptions in scheduling/budget resets.

**Telemetry to Track:**
- Feature adoption rate
- Error frequency by configuration field
- Support tickets per feature area

**Related Documents:**
- `faq_data_export.md`
- `support_campaign_rejection_macro.md`

---
