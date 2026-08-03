# Phase 6 — Day 12: Automated Testing

> **Note:** Part of the recommended post-deployment roadmap. This document sets goals/structure; ask for a full step-by-step build when ready to implement.

## Objective
Move from manual click-testing (as done after every Day 4/6/7/8 milestone) to automated Python tests using Odoo's `TransactionCase`, so regressions are caught before deployment.

## Why This Matters
```
Manual testing → works today, but doesn't scale, easy to forget edge cases
Automated tests → run in seconds, run on every change, protect against regressions
```

## Folder Structure
```
visa_consultancy/
└── tests/
    ├── __init__.py
    ├── test_application.py
    ├── test_appointment.py
    └── test_security.py
```
`tests/__init__.py` must be imported from the module's `__init__.py` only during test runs (Odoo handles this automatically when the module is loaded with `--test-enable`).

## Suggested Test Coverage

### 1. Sequence Generation
```python
from odoo.tests import TransactionCase


class TestApplication(TransactionCase):

    def test_reference_auto_generated(self):
        applicant = self.env['visa.applicant'].create({'name': 'Test Applicant'})
        country = self.env['visa.country'].create({'name': 'Canada'})
        visa_type = self.env['visa.type'].create({'name': 'Student', 'country_id': country.id})

        application = self.env['visa.application'].create({
            'applicant_id': applicant.id,
            'country_id': country.id,
            'visa_type_id': visa_type.id,
        })

        self.assertTrue(application.name.startswith('VISA/'))
```

### 2. Workflow Transitions
```python
def test_appointment_workflow(self):
    appointment = self.env['visa.appointment'].create({...})
    self.assertEqual(appointment.state, 'scheduled')

    appointment.action_complete()
    self.assertEqual(appointment.state, 'completed')
```

### 3. Record Rules (Security)
```python
def test_consultant_only_sees_own_applications(self):
    consultant_user = self.env['res.users'].create({...})
    other_application = self.env['visa.application'].create({...})  # different consultant

    applications = self.env['visa.application'].with_user(consultant_user).search([])
    self.assertNotIn(other_application, applications)
```

### 4. Email Automation
```python
def test_email_sent_on_application_create(self):
    with self.mock_mail_gateway():
        application = self.env['visa.application'].create({...})
        # assert a mail.message / mail.mail was created referencing the template
```

## Running Tests
```bash
./odoo-bin -c /etc/odoo19.conf \
  -d test_db \
  -i visa_consultancy \
  --test-enable \
  --stop-after-init
```

## CI Recommendation
Add a GitHub Actions / GitLab CI job that:
1. Spins up PostgreSQL as a service
2. Installs Odoo + the module
3. Runs `--test-enable --stop-after-init`
4. Fails the pipeline on any test failure — before merging to `main`/production

## Testing Checklist (when implemented)
- [ ] Sequence generation tested for Application, Appointment, Payment
- [ ] Every state-machine transition has a test
- [ ] Record rules tested for each security group
- [ ] Email/activity automation tested
- [ ] PDF report generation doesn't raise errors (`report.render_qweb_pdf`)

---
**Previous:** [11-dashboard-kpi.md](11-dashboard-kpi.md) · **Next:** [13-project-handover.md](13-project-handover.md)
