# Phase 1 — Requirement Analysis

## Project
**Visa Consultancy Management System** — a custom Odoo 19 ERP module for managing visa applications, applicants, documents, payments, and appointments for a visa consultancy business.

## Objective
Identify what the business needs before writing any code, so development follows real business processes rather than guesswork.

## Business Context
A visa consultancy manages the end-to-end journey of a client applying for a visa:

```
Lead / Inquiry
     |
Applicant Registration
     |
Visa Application Created
     |
Document Collection
     |
Payment
     |
Appointments (Embassy / Biometric / Medical)
     |
Application Outcome (Approved / Rejected)
```

## Core Business Entities Identified
| Entity | Purpose |
|---|---|
| Country | Destination country for the visa |
| Visa Type | Type of visa offered per country (Student, Work, Visit, etc.) |
| Applicant | The individual applying for a visa |
| Application | The visa case linking applicant, country, and visa type |
| Document | Required documents per application |
| Payment | Consultancy fees and visa fees tracking |
| Appointment | Embassy interviews, biometrics, medical checks, passport collection |

## Functional Requirements
- Register and manage applicants (personal details, passport info, contact info)
- Maintain a master list of countries and visa types per country
- Create visa applications linked to an applicant, country, and visa type
- Track application status through a workflow (Draft → Submitted → Processing → Approved/Rejected)
- Track required and submitted documents per application
- Record payments against an application
- Schedule and track appointments (embassy, biometric, medical, passport collection)
- Notify/remind staff and applicants about upcoming appointments
- Generate a printable application receipt (PDF)
- Provide management reporting (applications by country, by status)

## Non-Functional Requirements
- Role-based access: Manager, Consultant, Document Officer, Accountant
- Data privacy: consultants should only see their own assigned applications (record rules)
- Auditability: track changes on key records (mail.thread / tracking fields)
- Usability: simple tree/form/calendar views consistent with standard Odoo UX
- Must run on Odoo 19 and be installable as a standard custom addon

## Stakeholders
- **Consultancy Manager** — oversees all applications, needs reporting/dashboards
- **Visa Consultant** — manages assigned applicants and applications
- **Document Officer** — verifies and tracks documents
- **Accountant** — manages payments and invoicing
- **Applicant/Customer** — receives confirmations and status updates (future: portal access)

## Out of Scope (for initial release)
- Customer self-service portal (planned — see Day 9)
- Full accounting/invoicing integration (planned — see Day 10)
- Automated testing suite (planned — see Day 12)

## Deliverable of This Phase
A clear list of entities, relationships, and workflows that directly maps to Phase 2 (System Design) and the Odoo data model.

---
**Next:** [02-system-design.md](02-system-design.md)
