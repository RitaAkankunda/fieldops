# FieldOps — Domain Model

**Project:** FieldOps — Field Service Management System  
**Phase:** Day 2 — Domain Modelling  
**Status:** Initial design — subject to validation  
**Scope:** 30-day MVP

---

## 1. Purpose

This document defines the initial domain model for FieldOps.

It identifies the main business entities, their relationships, business rules, lifecycle states, and exceptional workflows.

The goal is to understand the business domain before implementing Django models, API endpoints, and database constraints.

The model is based on the project's initial requirements and assumptions. It has not yet been validated with real service businesses.

## 2. Domain Overview

FieldOps helps small CCTV, networking, and electrical service businesses manage customer service requests and technician work.

The core business process is:

1. An administrator registers a customer service request.
2. The administrator reviews the request.
3. The request is approved or declined.
4. An approved request may produce a work order.
5. The administrator assigns a technician.
6. The technician performs the work.
7. The technician submits completion notes.
8. The administrator reviews and closes the work order.
9. Important actions are recorded in the audit history.

## 3. Core Domain Entities

### 3.1 ServiceRequest

**Purpose:** Represents a customer's request for service.

**Proposed attributes:**

- `id` — Internal unique identifier
- `reference` — Human-readable unique request reference
- `customer_name`
- `customer_phone`
- `customer_email` — Optional
- `service_location`
- `service_type`
- `description`
- `status`
- `created_by` — Administrator who registered the request
- `created_at`
- `updated_at`

**Possible statuses:**

- `PENDING_REVIEW`
- `APPROVED`
- `DECLINED`

**Responsibilities:**

- Record customer needs.
- Track approval decisions.
- Provide the source for an authorized work order.

**Business rules:**

- A new request starts as `PENDING_REVIEW`.
- Only an administrator can approve or decline a request.
- A declined request cannot produce a work order.
- An approved request can produce at most one work order.

### 3.2 WorkOrder

**Purpose:** Represents authorized service work to be carried out.

**Proposed attributes:**

- `id`
- `reference` — Unique work-order reference
- `service_request_id`
- `assigned_technician_id` — Nullable
- `status`
- `completion_notes` — Nullable until submission
- `created_at`
- `updated_at`
- `started_at` — Optional
- `completion_submitted_at` — Optional
- `closed_at` — Optional

**Possible statuses:**

- `UNASSIGNED`
- `ASSIGNED`
- `IN_PROGRESS`
- `COMPLETION_SUBMITTED`
- `CLOSED`

**Responsibilities:**

- Track authorized work.
- Maintain the current technician assignment.
- Track job progress.
- Capture completion notes.
- Support administrative review and closure.

**Business rules:**

- A work order must belong to an approved service request.
- Each service request can have at most one work order.
- A work order starts as `UNASSIGNED`.
- A work order may have zero or one current technician.
- Only the current assigned technician can perform technician-specific updates.
- Completion requires nonempty notes.
- Completion submission does not automatically close the job.
- Only an administrator can close the work order after review.

### 3.3 User

**Purpose:** Represents a person authorized to access FieldOps.

**Proposed attributes:**

- `id`
- `name`
- `email`
- `password_hash`
- `role`
- `is_active`
- `created_at`

**Roles:**

- `ADMIN`
- `TECHNICIAN`

**Responsibilities:**

- Authenticate to FieldOps.
- Perform actions permitted by the user's role.
- Serve as the actor associated with audit events.

**Business rules:**

- Only active users can perform authenticated actions.
- Only active users with the `TECHNICIAN` role can receive new technician assignments.
- Administrators manage service requests and work orders.
- Technicians access only work orders currently assigned to them.
- Role checks and object-level permissions must be enforced by the backend.

**Design decision:** For the MVP, `Technician` is a role of `User`, not a separate entity.

### 3.4 AuditEvent

**Purpose:** Records important business actions for accountability and traceability.

**Proposed attributes:**

- `id`
- `actor_id`
- `entity_type`
- `entity_id`
- `action`
- `previous_value` — Where applicable
- `new_value` — Where applicable
- `reason` — Where applicable
- `created_at`

**Examples of actions:**

- `REQUEST_CREATED`
- `REQUEST_APPROVED`
- `REQUEST_DECLINED`
- `WORK_ORDER_CREATED`
- `TECHNICIAN_ASSIGNED`
- `TECHNICIAN_REASSIGNED`
- `WORK_STARTED`
- `COMPLETION_SUBMITTED`
- `COMPLETION_REJECTED`
- `WORK_ORDER_CLOSED`

**Business rules:**

- Important state changes and assignment changes must be recorded.
- Audit history should not be deleted when an assignment changes.
- Previous completion submissions and rejection decisions should remain traceable.
- The backend, rather than the frontend, is responsible for recording trustworthy audit events.

## 4. Entity Relationships

### 4.1 ServiceRequest and WorkOrder

- One `ServiceRequest` may have zero or one `WorkOrder`.
- One `WorkOrder` belongs to exactly one `ServiceRequest`.
- A work order can be created only when its service request is `APPROVED`.

**Cardinality:** `ServiceRequest (1) → WorkOrder (0..1)`

### 4.2 User and WorkOrder

- One `User` with the `TECHNICIAN` role may be assigned multiple work orders.
- One `WorkOrder` may have zero or one current assigned technician.
- Previous assignments are preserved in audit history.

**Cardinality:** `User (1) → WorkOrder (0..many)`

This relationship applies to the current assignee, not historical assignments.

### 4.3 User and AuditEvent

- One user may perform many audited actions.
- Each audit event identifies the actor responsible for the action.
- Historical records must remain meaningful even when a user becomes inactive.

### 4.4 Initial Relationship Diagram

```text
ServiceRequest
      |
      | 0..1 WorkOrder per ServiceRequest
      v
  WorkOrder -------------------- User
      |                    current technician
      |                    (0..1 per work order)
      |
      v
  AuditEvent ------------------- User
                             actor
```

The diagram is conceptual. Detailed foreign keys and database constraints will be finalized during implementation planning.

## 5. Domain Invariants

The following conditions must always be protected:

**INV-01:** A work order must reference an existing service request.

**INV-02:** A work order can only be created from an approved service request.

**INV-03:** A service request can have at most one work order.

**INV-04:** A work order has at most one current assigned technician.

**INV-05:** A technician assigned to a work order must be an active user with the `TECHNICIAN` role at assignment time.

**INV-06:** Only the current assigned technician may perform technician-specific work-order updates.

**INV-07:** Work-order status changes must follow permitted transitions.

**INV-08:** Completion submission requires nonempty completion notes.

**INV-09:** Completion submission must not automatically close the work order.

**INV-10:** Only an administrator may approve, decline, assign, reassign, review, or close work according to the relevant workflow.

**INV-11:** Important business changes must be recorded in audit history.

**INV-12:** Duplicate work-order creation must be prevented, including concurrent attempts.

These rules should be enforced through backend validation, permissions, transactions, and database constraints where appropriate.

## 6. Service Request State Machine

### 6.1 States

- `PENDING_REVIEW`
- `APPROVED`
- `DECLINED`

### 6.2 Allowed Transitions

```text
                +--> APPROVED
                |
PENDING_REVIEW -+
                |
                +--> DECLINED
```

| From | To | Actor |
|---|---|---|
| New request | `PENDING_REVIEW` | Administrator |
| `PENDING_REVIEW` | `APPROVED` | Administrator |
| `PENDING_REVIEW` | `DECLINED` | Administrator |

For the initial MVP, approved and declined decisions are treated as final. Reversal rules remain open for future validation.

## 7. Work Order State Machine

### 7.1 Happy Path

```text
UNASSIGNED
    |
    v
ASSIGNED
    |
    v
IN_PROGRESS
    |
    v
COMPLETION_SUBMITTED
    |
    v
CLOSED
```

### 7.2 Allowed Happy-Path Transitions

| From | To | Actor | Conditions |
|---|---|---|---|
| Creation | `UNASSIGNED` | Administrator | Request is approved; no existing work order |
| `UNASSIGNED` | `ASSIGNED` | Administrator | Valid active technician |
| `ASSIGNED` | `IN_PROGRESS` | Assigned technician | Technician is authorized |
| `IN_PROGRESS` | `COMPLETION_SUBMITTED` | Assigned technician | Nonempty completion notes |
| `COMPLETION_SUBMITTED` | `CLOSED` | Administrator | Completion reviewed and accepted |

### 7.3 Proposed Rejected-Completion Transition

```text
IN_PROGRESS
    |
    v
COMPLETION_SUBMITTED
    |
    +--> CLOSED
    |
    +--> IN_PROGRESS
         (completion rejected)
```

**Provisional rules:**

- Only an administrator can reject submitted completion.
- A rejection reason is mandatory.
- The work order returns to `IN_PROGRESS`.
- The current technician may correct the work and submit again.
- Previous completion submissions and rejection reasons remain traceable.

This exception is documented for design completeness. Its implementation priority will be reviewed against the 30-day MVP scope.

## 8. Technician Assignment and Reassignment

### 8.1 Initial Assignment

- A work order may be created without a technician.
- An administrator assigns an active technician.
- The work order moves from `UNASSIGNED` to `ASSIGNED`.
- The assignment is recorded in audit history.

### 8.2 Reassignment

A work order may need a new technician when the current technician becomes unavailable.

**Provisional rules:**

1. Only an administrator can reassign.
2. The replacement must be an active technician.
3. The replacement becomes the sole current assignee.
4. The previous technician loses update access.
5. The work-order status does not automatically change.
6. The previous and new assignees are recorded in audit history.
7. A reason is required when reassigning an `IN_PROGRESS` job.
8. A `CLOSED` work order cannot be reassigned in the MVP.

**Example:**

```text
Work order: WO-0012
Status: IN_PROGRESS

Previous technician: Daniel
New technician: Grace

Status after reassignment: IN_PROGRESS
Current assignee: Grace
Daniel's update permission: Revoked
Audit event: TECHNICIAN_REASSIGNED
```

### 8.3 Open Reassignment Questions

- Should reassignment be allowed during `COMPLETION_SUBMITTED`?
- Should an administrator be able to unassign an in-progress job?
- Should the replacement technician explicitly acknowledge the handover?
- Should the work order return to `ASSIGNED` when no actual work has begun?

These questions remain unresolved and require further design or stakeholder validation.

## 9. State Versus Event

A **state** describes the current condition of an entity.

An **event** records something that happened.

| State | Example event |
|---|---|
| `ASSIGNED` | `TECHNICIAN_ASSIGNED` |
| `IN_PROGRESS` | `WORK_STARTED` |
| `IN_PROGRESS` | `TECHNICIAN_REASSIGNED` |
| `COMPLETION_SUBMITTED` | `COMPLETION_SUBMITTED` |
| `CLOSED` | `WORK_ORDER_CLOSED` |

Reassignment is an event and does not require a separate `REASSIGNED` status.

## 10. MVP Scope and Deferred Decisions

### Core MVP Domain Rules

- Service request registration and review
- Approval and decline
- One work order per approved request
- Technician assignment
- Technician-specific access control
- Work-order progress tracking
- Completion submission with notes
- Administrator review and closure
- Audit history

### Proposed Extensions to Prioritize Later

- Rejected completion and resubmission
- Reassignment after work begins
- Cancellation workflows
- `ON_HOLD` status
- Reopening closed work orders
- Multiple technicians on one work order
- Multiple work orders per service request
- Multiple service visits

The initial implementation should prioritize the happy path and the invariants that protect it.

## 11. Testing Implications

The domain rules will guide test-driven development.

Initial test scenarios include:

1. A new service request starts as `PENDING_REVIEW`.
2. A declined request cannot produce a work order.
3. An approved request can produce one work order.
4. Creating a second work order for the same request fails.
5. A new work order starts as `UNASSIGNED`.
6. An inactive technician cannot receive a new assignment.
7. An administrator can assign an active technician.
8. An unassigned work order cannot be started.
9. An unrelated technician cannot update another technician's job.
10. The assigned technician can start an assigned work order.
11. Completion submission without notes fails.
12. Valid completion submission moves the job to `COMPLETION_SUBMITTED`.
13. A technician cannot directly close a work order.
14. An administrator can close a reviewed completion.
15. Invalid state transitions are rejected.
16. Important state changes produce audit events.

Additional tests will be defined if exceptional workflows are included in the MVP.

## 12. Design Status

This is the **initial FieldOps domain model**, not the final database schema.

The proposed entities and business rules will inform:

- Django models
- Database relationships and constraints
- DRF serializers and permissions
- Domain services and transition methods
- Automated tests
- API design

The design may change after stakeholder feedback and implementation discoveries.

---

**Day 2 deliverable:** Initial domain model documenting entities, relationships, invariants, state transitions, and exceptional workflows.