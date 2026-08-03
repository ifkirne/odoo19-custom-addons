# Phase 3 — Database & Architecture

## Objective
Define the concrete database structure and technical architecture that the Odoo ORM will generate, before implementation begins.

## How Odoo Turns Models into Tables
Every `models.Model` class with a `_name` becomes a PostgreSQL table. Odoo automatically adds:

| Column | Purpose |
|---|---|
| `id` | Primary key |
| `create_uid` / `create_date` | Who/when created |
| `write_uid` / `write_date` | Who/when last modified |

## Planned Tables
| Model (technical) | Table | Purpose |
|---|---|---|
| `visa.country` | `visa_country` | Master list of destination countries |
| `visa.type` | `visa_type` | Visa types per country |
| `visa.applicant` | `visa_applicant` | Applicant personal data |
| `visa.application` | `visa_application` | The visa case record |
| `visa.document` | `visa_document` | Documents linked to an application |
| `visa.payment` | `visa_payment` | Payments linked to an application |
| `visa.appointment` | `visa_appointment` | Appointments linked to an application |

## Relationship Types Used
- **Many2one**: `visa.type.country_id → visa.country`, `visa.application.applicant_id → visa.applicant`, `visa.appointment.application_id → visa.application`
- **One2many**: `visa.application.appointment_ids`, `visa.application.document_ids`, `visa.application.payment_ids` (inverse side of the Many2one above)
- **Selection**: used for fixed-choice fields like `state`, `gender`, `appointment_type`

## Sequencing Strategy
Human-readable reference numbers are generated via `ir.sequence`, not raw database IDs:

```
Application : VISA/2026/00001
Appointment : APT/2026/00001
Payment     : PAY/2026/00001
```

Generated in the model's `create()` override, replacing a placeholder value of `"New"`.

## Technical Architecture (Runtime)
```
Browser (User)
     |
   HTTP/HTTPS
     |
Odoo Application Server (Python, ORM)
     |
PostgreSQL Database
     |
Filestore (attachments/documents)
```

## Module Data Loading Order
Odoo loads XML/CSV listed in `__manifest__.py` → `data` in **file order**, and this order matters:
```
1. security/security.xml         (groups must exist before rules/access reference them)
2. security/ir.model.access.csv  (access rights per model/group)
3. security/record_rules.xml     (row-level rules)
4. data/*.xml                    (sequences, mail templates)
5. views/*.xml                   (screens)
6. report/*.xml                  (PDF reports)
```

## Environment / Version
```
Odoo version : 19.0
Python       : 3.10+
Database     : PostgreSQL
Addons path  : custom_addons/visa_consultancy
```

## Deliverable of This Phase
A confirmed table/relationship map and load order that Phase 4 implements directly as Python models and XML data files.

---
**Previous:** [02-system-design.md](02-system-design.md) · **Next:** [04-development-foundation.md](04-development-foundation.md)
