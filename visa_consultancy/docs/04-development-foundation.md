# Phase 4 — Development / Day 4: Foundation

## Goal
Create the module skeleton and the first 3 models: Country, Visa Type, Applicant.

## Development Cycle Followed
```
Model → Security → Views → Menu → Testing → Refactoring
```
Built incrementally — tested after every milestone, never all at once.

## Step 1 — Create Module Directory
```bash
cd ~/odoo19/custom_addons
mkdir visa_consultancy
cd visa_consultancy
```

## Step 2 — Create Module Structure
```bash
mkdir models views security data report wizard controllers static
touch __init__.py
touch __manifest__.py
touch models/__init__.py
```

Resulting structure:
```
visa_consultancy/
├── __init__.py
├── __manifest__.py
├── models/
│   └── __init__.py
├── views/
├── security/
├── data/
├── report/
├── wizard/
├── controllers/
└── static/
```

## Step 3 — Manifest
`__manifest__.py`:
```python
{
    'name': 'Visa Consultancy Management',
    'version': '19.0.1.0.0',
    'category': 'Services',
    'summary': 'Manage visa applications, applicants, documents and payments',
    'description': """
        Visa Consultancy Management System

        Features:
        - Applicant Management
        - Visa Applications
        - Document Tracking
        - Payment Management
        - Appointment Management
    """,
    'author': 'Ilyas Rahman',
    'depends': ['base', 'mail', 'contacts', 'account'],
    'data': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
```

## Step 4 — Initialization Files
Root `__init__.py`:
```python
from . import models
```

`models/__init__.py`:
```python
from . import country
from . import visa_type
from . import applicant
```

## Step 5 — Country Model
`models/country.py`:
```python
from odoo import models, fields


class VisaCountry(models.Model):
    _name = 'visa.country'
    _description = 'Visa Country'

    name = fields.Char(string="Country Name", required=True)
    code = fields.Char(string="Country Code")
    description = fields.Text(string="Description")
    active = fields.Boolean(default=True)
```
Creates table `visa_country` with columns: `id`, `name`, `code`, `description`, `active`, `create_date`, `write_date`.

## Step 6 — Visa Type Model
`models/visa_type.py`:
```python
from odoo import models, fields


class VisaType(models.Model):
    _name = 'visa.type'
    _description = 'Visa Type'

    name = fields.Char(string="Visa Type", required=True)
    country_id = fields.Many2one('visa.country', string="Country")
    description = fields.Text(string="Description")
    active = fields.Boolean(default=True)
```
Relationship: `visa.country` (1) → `visa.type` (many). Example: Canada has Student Visa, Work Visa, Visit Visa.

## Step 7 — Applicant Model
`models/applicant.py`:
```python
from odoo import models, fields


class VisaApplicant(models.Model):
    _name = 'visa.applicant'
    _description = 'Visa Applicant'

    name = fields.Char(string="Full Name", required=True)
    passport_number = fields.Char(string="Passport Number")
    nationality = fields.Char(string="Nationality")
    date_of_birth = fields.Date(string="Date of Birth")
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        string="Gender"
    )
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    address = fields.Text(string="Address")
    notes = fields.Text(string="Notes")
```

## Step 8 — Restart Odoo
```bash
./odoo-bin -c ../conf/odoo.conf
```

## Step 9 — Install Module
1. Open `http://localhost:8069`
2. Activate developer mode
3. Apps → search "Visa Consultancy Management" → Install

## Result
Database now contains `visa_country`, `visa_type`, `visa_applicant` tables — **but no menu yet**, because Odoo separates backend logic (models) from the user interface (XML views). This is expected and is resolved in the next milestone (Security → Views → Menus).

## Next Milestone (Day 4 Part 2)
- `security/security.xml` + `security/ir.model.access.csv`
- Tree/Form/Search views for Country, Visa Type, Applicant
- Menu structure:
```
Visa Consultancy
 ├── Applicants
 └── Configuration
       ├── Countries
       └── Visa Types
```

---
**Previous:** [03-database-architecture.md](03-database-architecture.md) · **Next:** [05-documents-payments.md](05-documents-payments.md)
