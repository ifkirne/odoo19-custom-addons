# Phase 6 — Day 11: Dashboard & KPIs

> **Note:** Part of the recommended post-deployment roadmap. This document sets goals/structure; ask for a full step-by-step build when ready to implement.

## Objective
Give the Manager a single-screen overview of consultancy performance, built on top of the Pivot/Graph reporting already added in Day 7.

## Business Value
```
Before: Manager opens Applications list, Pivot, Graph separately to understand the business
After:  Manager opens one Dashboard screen and sees everything at a glance
```

## Planned KPIs
| KPI | Source |
|---|---|
| Total applications this month | `visa.application` count, filtered by `create_date` |
| Applications by status (Draft/Submitted/Processing/Approved/Rejected) | `visa.application` grouped by `state` |
| Applications by country | existing pivot/graph from Day 7 |
| Upcoming appointments (next 7 days) | `visa.appointment` filtered by `appointment_date` |
| Revenue this month | `visa.payment` / `account.move` sum |
| Approval rate (Approved ÷ Total closed) | computed field or SQL view |

## Technical Approach
Two common implementation paths:
1. **Odoo Dashboards app (`board`)**: quickest — assemble existing Pivot/Graph/List views into a custom dashboard via "Add to Dashboard".
2. **Custom OWL dashboard**: a dedicated client action (JS/OWL component) reading aggregated data through a controller or `read_group` calls, for a fully custom look with KPI cards + charts.

### Suggested Minimal Structure (Board approach)
```
1. Build individual Graph/Pivot/List views for each KPI (mostly reuse Day 7's views)
2. Manager clicks "Add to Dashboard" from each view's favorites menu
3. Arrange them under a "Visa Consultancy Dashboard" board
```

### Suggested Advanced Structure (Custom OWL)
```
static/src/js/dashboard.js       → OWL component fetching KPI data
static/src/xml/dashboard.xml     → template with KPI cards + chart.js/recharts-style widgets
views/dashboard_views.xml        → ir.actions.client registering the dashboard
```

## Access
Restrict the dashboard menu item to `group_visa_manager` (from Day 7's security groups) so consultants/accountants don't see company-wide figures.

## Testing Checklist (when implemented)
- [ ] KPI numbers match manual counts from the Applications list
- [ ] Dashboard respects record rules (a Manager sees all; it should never be shown to Consultants with only "own records" access)
- [ ] Dashboard loads within an acceptable time as data grows (add indexes if using custom SQL)

---
**Previous:** [10-accounting-integration.md](10-accounting-integration.md) · **Next:** [12-testing.md](12-testing.md)
