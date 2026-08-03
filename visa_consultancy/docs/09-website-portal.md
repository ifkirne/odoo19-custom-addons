# Phase 6 — Day 9: Customer Website Portal

> **Note:** This phase is part of the recommended post-deployment roadmap. Detailed step-by-step build content wasn't produced yet in this conversation — this document sets the goals and structure for that build. Ask for a fully detailed walkthrough (models/security/views/testing) when you're ready to implement it.

## Objective
Give applicants self-service visibility into their own visa case without contacting the consultancy directly, using Odoo's built-in `portal` app.

## Business Value
```
Before: Applicant calls/emails consultancy → staff checks status manually → staff replies
After:  Applicant logs into portal → sees live status → staff time freed up
```

## Planned Features
- Portal login for applicants (extends `portal.mixin` on `visa.application`)
- "My Applications" page showing application reference, status, country, visa type
- Document upload directly from the portal (maps to `visa.document`)
- Payment status visibility (read-only)
- Appointment upcoming date visibility

## Technical Approach
- Depend on Odoo's `portal` module
- Inherit `portal.mixin` on `visa.application` to get a shareable portal URL and access token
- Add a `controllers/portal.py` using `CustomerPortal` (from `odoo.addons.portal.controllers.portal`) to register routes like `/my/visa-applications`
- Add portal-specific QWeb templates extending `portal.portal_my_home`
- Access control: applicants only ever see their own record (via `sudo()` + explicit ownership checks, not raw model access)

## Suggested Model Change
```python
class VisaApplication(models.Model):
    _name = 'visa.application'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
```

## Suggested Menu/Route Structure
```
/my                         → existing Odoo portal home
/my/visa-applications        → list of the logged-in applicant's applications
/my/visa-applications/<id>   → detail view (status, documents, appointments)
```

## Security Considerations
- Never expose internal consultant notes or other applicants' data
- Use `check_access_rights` / `sudo()` carefully — portal users have very limited base access
- Rate-limit document uploads; validate file types/sizes

## Testing Checklist (when implemented)
- [ ] Applicant receives portal invite email and can log in
- [ ] Applicant sees only their own applications
- [ ] Applicant can upload a document, staff sees it appear in the backend
- [ ] Applicant cannot access another applicant's record by guessing the URL

---
**Previous:** [08-production-deployment.md](08-production-deployment.md) · **Next:** [10-accounting-integration.md](10-accounting-integration.md)
