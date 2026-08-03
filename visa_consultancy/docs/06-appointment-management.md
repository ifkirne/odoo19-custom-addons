# Phase 4 — Development / Day 6: Appointment Management

## Why It Matters
A visa consultancy depends heavily on appointment tracking: embassy interviews, biometrics, medical appointments, passport collection. Missing an appointment can directly affect the customer's visa case.

## Business Flow
```
Visa Application
      |
   Appointment
      |
      ├── Scheduled
      ├── Completed
      └── Cancelled
```

## Goals
- Appointment Model
- Application Relationship
- Appointment Status Workflow
- Calendar View
- Activities Reminder
- Email Notification Preparation

## Step 1 — Database Design
```
visa.application (1) ──< (∞) visa.appointment
```
One application can have: Embassy appointment, Biometric appointment, Medical appointment.

## Step 2 — Appointment Model
`models/appointment.py`
```python
from odoo import models, fields


class VisaAppointment(models.Model):
    _name = 'visa.appointment'
    _description = 'Visa Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'appointment_date desc'

    name = fields.Char(string="Appointment Reference", required=True,
                        copy=False, readonly=True, default="New")
    application_id = fields.Many2one('visa.application', string="Application",
                                      required=True, ondelete='cascade', tracking=True)
    appointment_type = fields.Selection([
        ('embassy', 'Embassy Interview'),
        ('biometric', 'Biometric'),
        ('medical', 'Medical'),
        ('passport', 'Passport Collection'),
    ], string="Appointment Type", required=True)
    embassy = fields.Char(string="Embassy / Center")
    appointment_date = fields.Datetime(string="Appointment Date", required=True)
    location = fields.Char(string="Location")
    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string="Status", default='scheduled', tracking=True)
    notes = fields.Text(string="Notes")
```

## Step 3 — Appointment Sequence
`data/appointment_sequence.xml`
```xml
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
  <record id="sequence_appointment" model="ir.sequence">
    <field name="name">Visa Appointment</field>
    <field name="code">visa.appointment</field>
    <field name="prefix">APT/%(year)s/</field>
    <field name="padding">5</field>
  </record>
</odoo>
```

## Step 4 — Auto-Generate Appointment Number
`models/appointment.py` (add import and method):
```python
from odoo import models, fields, api

@api.model
def create(self, vals):
    if vals.get('name') == 'New':
        vals['name'] = self.env['ir.sequence'].next_by_code('visa.appointment')
    return super().create(vals)
```
Example: `New` → `APT/2026/00001` after save.

## Step 5 — Relationship on Application
`models/application.py`
```python
appointment_ids = fields.One2many('visa.appointment', 'application_id',
                                   string="Appointments")
```

## Step 6 — Workflow Buttons
```python
def action_complete(self):
    for record in self:
        record.state = 'completed'

def action_cancel(self):
    for record in self:
        record.state = 'cancelled'
```
```
Scheduled --[Complete]--> Completed
Scheduled --[Cancel]----> Cancelled
```

## Step 7 — Import Model
`models/__init__.py`
```python
from . import appointment
```

## Step 8 — Views: Tree
`views/appointment_views.xml`
```xml
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
  <record id="view_appointment_tree" model="ir.ui.view">
    <field name="name">visa.appointment.tree</field>
    <field name="model">visa.appointment</field>
    <field name="arch" type="xml">
      <tree>
        <field name="name"/>
        <field name="application_id"/>
        <field name="appointment_type"/>
        <field name="appointment_date"/>
        <field name="state"/>
      </tree>
    </field>
  </record>
```

## Step 8b — Views: Form
```xml
  <record id="view_appointment_form" model="ir.ui.view">
    <field name="name">visa.appointment.form</field>
    <field name="model">visa.appointment</field>
    <field name="arch" type="xml">
      <form>
        <header>
          <button name="action_complete" string="Complete" type="object"/>
          <button name="action_cancel" string="Cancel" type="object"/>
          <field name="state" widget="statusbar"/>
        </header>
        <sheet>
          <group>
            <field name="name"/>
            <field name="application_id"/>
            <field name="appointment_type"/>
            <field name="appointment_date"/>
            <field name="embassy"/>
            <field name="location"/>
          </group>
          <field name="notes"/>
        </sheet>
      </form>
    </field>
  </record>
```

## Step 9 — Calendar View
```xml
  <record id="view_appointment_calendar" model="ir.ui.view">
    <field name="name">visa.appointment.calendar</field>
    <field name="model">visa.appointment</field>
    <field name="arch" type="xml">
      <calendar string="Appointments" date_start="appointment_date"
                color="appointment_type">
        <field name="name"/>
        <field name="application_id"/>
      </calendar>
    </field>
  </record>
</odoo>
```
Users can now see appointments plotted on a monthly calendar, color-coded by type.

## Step 10 — Appointment Tab in Application Form
`application_views.xml` (inside `<notebook>`):
```xml
<page string="Appointments">
  <field name="appointment_ids">
    <tree editable="bottom">
      <field name="name"/>
      <field name="appointment_type"/>
      <field name="appointment_date"/>
      <field name="state"/>
    </tree>
  </field>
</page>
```

## Step 11 — Access Rights
`security/ir.model.access.csv`
```
access_visa_appointment,visa.appointment,model_visa_appointment,base.group_user,1,1,1,1
```

## Step 12 — Manifest Update
```python
'data': [
    'security/security.xml',
    'security/ir.model.access.csv',
    'data/sequence.xml',
    'data/payment_sequence.xml',
    'data/appointment_sequence.xml',
    'views/appointment_views.xml',
]
```

## Step 13 — Testing
```bash
./odoo-bin -c ../conf/odoo.conf
```
1. Upgrade module
2. Create Application `VISA/2026/00001`
3. Add Appointment: Type = Embassy Interview, Date = 10 August 2026, Location = Canadian Embassy → Save
4. Result: `APT/2026/00001`, Status = Scheduled
5. Click **Complete** → Status = Completed

## Planned Enhancements (Production)
- Automated reminder activity 1 day before appointment
- Automatic email notification to the applicant on scheduling

## Progress Snapshot After Day 6
| Feature | Status |
|---|---|
| Applicant | ✅ |
| Countries | ✅ |
| Visa Types | ✅ |
| Applications | ✅ |
| Workflow | ✅ |
| Documents | ✅ |
| Payments | ✅ |
| Appointments | ✅ |

---
**Previous:** [05-documents-payments.md](05-documents-payments.md) · **Next:** [07-professionalization.md](07-professionalization.md)
