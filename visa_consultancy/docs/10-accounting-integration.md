# Phase 6 — Day 10: Accounting Integration

> **Note:** Part of the recommended post-deployment roadmap. This document sets goals/structure; ask for a full step-by-step build when ready to implement.

## Objective
Replace the standalone `visa.payment` tracking model with real Odoo Accounting (`account.move` / `account.payment`) so the consultancy gets proper invoicing, receivables, and financial reporting — since the module already depends on `account`.

## Business Value
```
Before: visa.payment is just a log, disconnected from real accounting
After:  Every application generates a real customer invoice with proper
        journal entries, aged receivables, and tax handling
```

## Planned Features
- Generate a customer Invoice (`account.move`, `move_type = 'out_invoice'`) directly from a Visa Application
- Link `visa.application` to an `account.move` via a Many2one (`invoice_id`) or a One2many (`invoice_ids`)
- Register payments through `account.payment` (reconciled against the invoice) instead of the standalone `visa.payment` model
- Smart button on the Application form: "Invoices" showing count + quick access
- Automatic invoice line generation based on Visa Type fee (requires adding a `fee` field to `visa.type`)

## Suggested Model Change
```python
class VisaApplication(models.Model):
    _inherit = 'visa.application'

    invoice_ids = fields.One2many('account.move', 'visa_application_id', string="Invoices")
    invoice_count = fields.Integer(compute='_compute_invoice_count')

    def action_create_invoice(self):
        self.ensure_one()
        move = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.applicant_id.partner_id.id,
            'invoice_line_ids': [(0, 0, {
                'name': self.visa_type_id.name,
                'quantity': 1,
                'price_unit': self.visa_type_id.fee,
            })],
            'visa_application_id': self.id,
        })
        return move
```
```python
class AccountMove(models.Model):
    _inherit = 'account.move'
    visa_application_id = fields.Many2one('visa.application', string="Visa Application")
```

## Data Model Requirement
`visa.applicant` should have (or link to) a `res.partner` record, since `account.move` requires a `partner_id`. This likely means extending the Applicant model to inherit or auto-create a linked partner on creation.

## Reporting Value Unlocked
- Aged receivables per applicant
- Revenue by country / visa type (via accounting analytics, not just the custom pivot)
- Standard Odoo invoicing PDF instead of a custom one

## Testing Checklist (when implemented)
- [ ] Creating an invoice from an Application creates a correctly-linked `account.move`
- [ ] Invoice total matches the Visa Type fee
- [ ] Registering a payment reconciles against the invoice and updates payment status
- [ ] Smart button count updates correctly

---
**Previous:** [09-website-portal.md](09-website-portal.md) · **Next:** [11-dashboard-kpi.md](11-dashboard-kpi.md)
