# Phase 2 — System Design

## Objective
Translate the requirements from Phase 1 into a concrete Odoo module design: entity relationships, workflows, and screen structure — before writing a single model.

## Module Identity
```
Technical name : visa_consultancy
Display name   : Visa Consultancy Management
Category       : Services
Depends on     : base, mail, contacts, account
```

## Entity Relationship Design
```
visa.country  (1) ────< (∞)  visa.type
visa.country  (1) ────< (∞)  visa.application
visa.type     (1) ────< (∞)  visa.application
visa.applicant(1) ────< (∞)  visa.application
visa.application(1) ──< (∞)  visa.document
visa.application(1) ──< (∞)  visa.payment
visa.application(1) ──< (∞)  visa.appointment
```

## Application Workflow (State Machine)
```
Draft
  |
Submitted
  |
Processing
  |
  ├── Approved
  └── Rejected
```

## Appointment Workflow (State Machine)
```
Scheduled
  |
  ├── Completed
  └── Cancelled
```

## Screen / Menu Design
```
Visa Consultancy
 ├── Applications
 ├── Applicants
 ├── Appointments (Tree / Form / Calendar)
 ├── Reporting
 │     ├── Pivot (Applications by Country/Status)
 │     └── Graph (Applications by Country)
 └── Configuration
       ├── Countries
       └── Visa Types
```

## Security Design (High Level)
```
Administrator
   |
Manager        → full access, sees all records, reporting
   |
Consultant     → own assigned applications only (record rule)
   |
Document Officer → document-related access
   |
Accountant     → payment-related access
```

## Module Folder Design
```
visa_consultancy/
├── __init__.py
├── __manifest__.py
├── models/
├── views/
├── security/
├── data/
├── report/
├── wizard/
├── controllers/
└── static/
```

## Design Principles Followed
- **Separation of concerns**: business logic (models) is kept separate from UI (views), matching Odoo's MVC-like architecture.
- **Incremental build**: model → security → views → menu → test → refactor, repeated per feature, never "big bang" development.
- **Extensibility**: workflows and security are designed so document/payment/appointment modules can be added without redesigning the core.

## Deliverable of This Phase
An entity-relationship map, state machines, and a menu/screen blueprint that Phase 3 turns into an actual PostgreSQL/Odoo data model.

---
**Previous:** [01-requirement-analysis.md](01-requirement-analysis.md) · **Next:** [03-database-architecture.md](03-database-architecture.md)
