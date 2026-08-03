# Phase 4 — Development / Day 7: ERP Professionalization

## Objective
Move the module from "functional core" to production-grade: secure, automated, user-friendly, reportable. A junior developer makes models and views; a professional developer secures, automates, and reports on them.

## Goals
- Advanced Security (Groups)
- Record Rules
- Email Templates
- Automated Activities
- PDF Report Preparation
- Pivot & Graph Reporting

## Part 1 — Security Architecture
Before: a single flat "Internal User → Full Access" model. After: a role hierarchy.
```
Administrator
   |
Manager
   |
Consultant
   |
Document Officer
   |
Accountant
```

### Step 1 — Create Security Groups
`security/security.xml`
```xml
<?xml version="1.0" encoding="UTF-8"?>
<odoo>

<record id="group_visa_manager" model="res.groups">
    <field name="name">Visa Manager</field>
</record>

<record id="group_visa_consultant" model="res.groups">
    <field name="name">Visa Consultant</field>
</record>

<record id="group_document_officer" model="res.groups">
    <field name="name">Document Officer</field>
</record>

<record id="group_visa_accountant" model="res.groups">
    <field name="name">Visa Accountant</field>
</record>

</odoo>
```

## Part 2 — Access Rights Improvement
Access rights answer: *"Can you open this model at all?"*

Example policy:
- Consultant: Applicant → Create/Read/Edit ✔, Delete ✖
- Accountant: only Payments → Create/Read/Edit ✔, Delete ✖

`security/ir.model.access.csv`
```
access_application_consultant,visa.application,model_visa_application,group_visa_consultant,1,1,1,0
access_payment_accountant,visa.payment,model_visa_payment,group_visa_accountant,1,1,1,0
```

## Part 3 — Record Rules
Record rules answer: *"Which records can you see?"* — row-level security on top of model-level access.

`security/record_rules.xml`
```xml
<?xml version="1.0" encoding="UTF-8"?>
<odoo>

<record id="rule_consultant_application" model="ir.rule">
    <field name="name">Consultant Own Applications</field>
    <field name="model_id" ref="model_visa_application"/>
    <field name="domain_force">[('consultant_id','=',user.id)]</field>
    <field name="groups" eval="[(4,ref('group_visa_consultant'))]"/>
</record>

</odoo>
```
Result: a Consultant only sees Applications where `consultant_id` = the logged-in user.

## Part 4 — Email Templates
Business need: automatically email the customer when a new application is created.

`data/mail_template.xml`
```xml
<odoo>

<record id="email_application_created" model="mail.template">
    <field name="name">Visa Application Confirmation</field>
    <field name="model_id" ref="model_visa_application"/>
    <field name="subject">Visa Application Registered</field>
    <field name="body_html"><![CDATA[
        <p>Dear <t t-out="object.applicant_id.name"/></p>
        <p>Your visa application has been registered.</p>
        <p>Reference: <t t-out="object.name"/></p>
        <p>Thank you.</p>
    ]]></field>
</record>

</odoo>
```

## Part 5 — Send Email Automatically
`models/application.py` — modify `create()`:
```python
record = super().create(vals)

template = self.env.ref('visa_consultancy.email_application_created')
template.send_mail(record.id, force_send=True)

return record
```
Flow: `Save → Application created → Email sent`.

## Part 6 — Automated Activities
Example: after application creation, create a reminder to call the applicant tomorrow.
```python
self.env['mail.activity'].create({
    'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
    'res_id': record.id,
    'res_model_id': self.env['ir.model']._get('visa.application').id,
    'summary': 'Call applicant for document verification',
})
```
Result: the Application form shows an Activities entry — "☎ Call applicant, Due tomorrow".

## Part 7 — PDF Report Design
Business need: a printable Visa Application Receipt.

`report/application_report.xml` (report action)
```xml
<record id="application_report" model="ir.actions.report">
    <field name="name">Visa Application Report</field>
    <field name="model">visa.application</field>
    <field name="report_type">qweb-pdf</field>
    <field name="report_name">visa_consultancy.application_template</field>
</record>
```

`application_template.xml` (QWeb template)
```xml
<t t-name="visa_consultancy.application_template">
  <t t-call="web.external_layout">
    <div class="page">
      <h2>Visa Application</h2>
      <p>Reference: <t t-esc="doc.name"/></p>
      <p>Applicant: <t t-esc="doc.applicant_id.name"/></p>
      <p>Country: <t t-esc="doc.country_id.name"/></p>
    </div>
  </t>
</t>
```

## Part 8 — Reporting Views
### Pivot Report
`views/application_report_views.xml`
```xml
<record id="application_pivot" model="ir.ui.view">
    <field name="name">Visa Application Pivot</field>
    <field name="model">visa.application</field>
    <field name="arch" type="xml">
        <pivot>
            <field name="country_id" row="1"/>
            <field name="state" column="1"/>
        </pivot>
    </field>
</record>
```
Example result:
```
Country       Approved  Rejected
Canada          50        5
Germany         30        2
Australia       20        1
```

### Graph View
```xml
<graph>
    <field name="country_id"/>
    <field name="id" type="measure"/>
</graph>
```
Shows an "Applications by Country" chart.

## Manifest Update
```python
'data': [
    'security/security.xml',
    'security/record_rules.xml',
    'security/ir.model.access.csv',
    'data/mail_template.xml',
    'report/application_report.xml',
    'report/application_template.xml',
    'views/application_report_views.xml',
]
```

## Progress Snapshot After Day 7
| Feature | Status |
|---|---|
| Models | ✅ |
| Views | ✅ |
| Workflow | ✅ |
| Documents | ✅ |
| Payments | ✅ |
| Appointments | ✅ |
| Security Groups | ✅ |
| Record Rules | ✅ |
| Email Automation | ✅ |
| Activities | ✅ |
| PDF Reports | ✅ |
| Pivot Reports | ✅ |
| Graph Reports | ✅ |

---
**Previous:** [06-appointment-management.md](06-appointment-management.md) · **Next:** [08-production-deployment.md](08-production-deployment.md)
