# Phase 4 — Development / Day 5: Applications, Documents & Payments

> **Note:** This day was referenced in the project checklist (Applications ✅, Documents ✅, Payments ✅ prior to Day 6) but the step-by-step build log wasn't captured turn-by-turn in this conversation. This document reconstructs the expected structure consistent with the rest of the module so the documentation set stays complete. Ask for a fully detailed step-by-step version (matching the style of Day 4/6/7/8) if needed.

## Goal
Build the central **Application** model, plus **Document** and **Payment** models, following the same cycle: Model → Security → Views → Menu → Testing.

## Application Model (expected shape)
`models/application.py`
```python
from odoo import models, fields, api


class VisaApplication(models.Model):
    _name = 'visa.application'
    _description = 'Visa Application'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Reference", required=True, copy=False,
                        readonly=True, default="New")
    applicant_id = fields.Many2one('visa.applicant', string="Applicant", required=True)
    country_id = fields.Many2one('visa.country', string="Country", required=True)
    visa_type_id = fields.Many2one('visa.type', string="Visa Type", required=True)
    consultant_id = fields.Many2one('res.users', string="Consultant")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('processing', 'Processing'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default='draft', tracking=True)

    document_ids = fields.One2many('visa.document', 'application_id', string="Documents")
    payment_ids = fields.One2many('visa.payment', 'application_id', string="Payments")

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('visa.application')
        return super().create(vals)
```
Reference format: `VISA/2026/00001` (via `ir.sequence`, same pattern used later for appointments/payments).

## Document Model (expected shape)
`models/document.py`
```python
from odoo import models, fields


class VisaDocument(models.Model):
    _name = 'visa.document'
    _description = 'Visa Document'

    name = fields.Char(string="Document Name", required=True)
    application_id = fields.Many2one('visa.application', string="Application",
                                      required=True, ondelete='cascade')
    document_type = fields.Selection([
        ('passport', 'Passport Copy'),
        ('photo', 'Photograph'),
        ('bank_statement', 'Bank Statement'),
        ('invitation', 'Invitation Letter'),
        ('other', 'Other'),
    ], string="Document Type")
    attachment = fields.Binary(string="File")
    is_received = fields.Boolean(string="Received")
```

## Payment Model (expected shape)
`models/payment.py`
```python
from odoo import models, fields, api


class VisaPayment(models.Model):
    _name = 'visa.payment'
    _description = 'Visa Payment'

    name = fields.Char(string="Reference", copy=False, readonly=True, default="New")
    application_id = fields.Many2one('visa.application', string="Application",
                                      required=True, ondelete='cascade')
    amount = fields.Monetary(string="Amount", currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self:
                                   self.env.company.currency_id)
    payment_date = fields.Date(string="Payment Date")
    payment_method = fields.Selection([
        ('cash', 'Cash'), ('bank', 'Bank Transfer'), ('card', 'Card'),
    ], string="Method")

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('visa.payment')
        return super().create(vals)
```

## Sequences Required
```
data/sequence.xml          → visa.application  → VISA/%(year)s/
data/payment_sequence.xml  → visa.payment      → PAY/%(year)s/
```

## Views & Menu (expected)
- Application: Tree, Form (with `state` statusbar + notebook tabs: Documents, Payments), Search
- Document: embedded editable tree inside Application form (`Documents` tab)
- Payment: embedded editable tree inside Application form (`Payments` tab)
- Menu:
```
Visa Consultancy
 └── Applications
```

## Access Rights
Add entries to `security/ir.model.access.csv` for `visa.application`, `visa.document`, `visa.payment` following the same pattern as Country/Visa Type/Applicant from Day 4.

## Testing Checklist
- [ ] Create an Applicant, then an Application referencing it → reference auto-generates as `VISA/2026/00001`
- [ ] Add a Document row inside the Documents tab, mark as received
- [ ] Add a Payment row inside the Payments tab, confirm amount/currency display correctly
- [ ] Change `state` through Draft → Submitted → Processing → Approved/Rejected

---
**Previous:** [04-development-foundation.md](04-development-foundation.md) · **Next:** [06-appointment-management.md](06-appointment-management.md)
