# FieldOps — Architecture Decisions

## 1. Purpose

This document records the initial architecture decisions for the FieldOps minimum viable product (MVP).

It explains the proposed technologies, system structure, security boundaries, and reasons behind key technical choices.

These decisions are provisional and will be reviewed during Day 3 architecture design.

## 2. Architecture Goals

The FieldOps architecture should:

1. Support the core service request and work-order workflows.
2. Enforce business rules consistently.
3. Protect customer and technician information.
4. Separate user interface concerns from business logic.
5. Be practical for a 30-day learning project.
6. Support automated testing.
7. Remain understandable, maintainable, and extendable.

## 3. Proposed Technology Stack

| Layer | Proposed Technology | Reason |
|---|---|---|
| Frontend | React with Next.js | Component-based user interfaces and routing |
| Backend | Python with Django | Structured backend development and mature ecosystem |
| API | Django REST Framework | REST API development, authentication, and permissions |
| Database | PostgreSQL | Relational integrity and transactional consistency |
| Backend Testing | Pytest and pytest-django | Automated testing of business rules and API behavior |
| Frontend Testing | To be selected | Keep the initial setup focused |
| Version Control | Git and GitHub | Change tracking and portfolio visibility |
| Development Environment | VS Code | Editing, debugging, and terminal integration |

These technologies are proposed choices, not a completed or deployed architecture.

## 4. ADR-001 — Use a Web Application

**Status:** Proposed

### Context

Administrators need to manage service requests and work orders, while technicians need to view assignments and submit progress updates.

### Decision

Build FieldOps as a browser-accessible web application.

### Rationale

- One application can support both roles.
- Users do not need separate native mobile applications.
- A responsive interface can support technicians using phones.
- Web development fits the project timeline and learning goals.

### Consequences

- Users generally require internet access.
- Responsive design is important.
- Offline synchronization is outside the initial MVP.

## 5. ADR-002 — Separate Frontend and Backend

**Status:** Proposed

### Context

FieldOps requires a user interface, business rules, authentication, authorization, and persistent storage.

### Decision

Use a Next.js frontend communicating with a Django REST Framework backend through an API.

### Rationale

- Separates presentation from backend responsibilities.
- Makes API authorization rules explicit.
- Allows frontend and backend testing independently.
- Provides experience with a common full-stack architecture.

### Consequences

- Requires API contract design.
- Requires careful configuration of authentication and cross-origin requests.
- Adds some development complexity compared with a single Django-rendered application.

## 6. ADR-003 — Use a Modular Monolith Backend

**Status:** Proposed

### Context

FieldOps is a small MVP with related business processes and a limited development timeline.

### Decision

Build one Django backend organized into clearly separated business modules rather than using microservices.

Potential modules include:

- Accounts and user access.
- Service requests.
- Work orders.
- Audit history.

These are conceptual boundaries; the final Django app structure will be determined during implementation.

### Rationale

- Easier to develop and test.
- Simpler deployment and debugging.
- Supports clear responsibilities without distributed-system complexity.
- Allows future refactoring if the product grows.

### Consequences

- Modules must maintain clear boundaries.
- Business rules should not be scattered across views and serializers.
- Cross-module dependencies require deliberate design.

## 7. ADR-004 — Use PostgreSQL for Persistent Storage

**Status:** Proposed

### Context

FieldOps stores related records, including service requests, work orders, users, assignments, and audit events.

### Decision

Use PostgreSQL as the primary relational database.

### Rationale

- Supports relational constraints.
- Supports database transactions.
- Can enforce uniqueness rules.
- Works well with Django.

### Consequences

- PostgreSQL must be configured for development and deployment.
- Database migrations must be maintained.
- Important integrity rules should be enforced at both application and database levels where appropriate.

## 8. ADR-005 — Enforce Authorization in the Backend

**Status:** Proposed

### Context

Administrators and technicians have different responsibilities.

Technicians must not access work orders assigned to other technicians, even if they guess a URL or API identifier.

### Decision

Enforce authentication, role permissions, and object-level authorization in the backend.

### Rationale

- Frontend restrictions alone do not provide security.
- Backend checks protect API endpoints regardless of the client.
- Permissions can be tested automatically.

### Consequences

- API endpoints require explicit authorization checks.
- Work-order access must account for reassignment.
- Unauthorized requests must not expose protected information.

## 9. ADR-006 — Model Workflows Using Explicit State Transitions

**Status:** Proposed

### Context

Service requests and work orders progress through defined business stages.

Unrestricted status updates could create invalid records.

### Decision

Define allowed status transitions and enforce them in backend business logic.

### Proposed Service Request States

- `PENDING_REVIEW`
- `APPROVED`
- `DECLINED`

### Proposed Work-Order States

- `UNASSIGNED`
- `ASSIGNED`
- `IN_PROGRESS`
- `COMPLETION_SUBMITTED`
- `CLOSED`

### Rationale

- Prevents invalid transitions.
- Clarifies responsibilities.
- Makes behavior easier to test.
- Preserves consistency between workflows.

### Consequences

- Transition rules require automated tests.
- Cancellation, reassignment, rejected completion, and reopening require further modelling.
- The state model may change during Day 2.

## 10. ADR-007 — Preserve Important Audit Events

**Status:** Proposed

### Context

Administrators may need to investigate assignment changes, request decisions, and work-order progress.

### Decision

Record important business events with the responsible user, timestamp, and relevant previous and new values.

### Rationale

- Supports traceability.
- Helps explain how records reached their current state.
- Supports administrative review.

### Consequences

- Audit records should not be editable through ordinary application workflows.
- Business changes and required audit records must be saved consistently.
- Audit history access must be restricted appropriately.

## 11. ADR-008 — Use Automated Testing for Business Rules

**Status:** Proposed

### Context

FieldOps has important rules involving permissions, uniqueness, and state transitions.

### Decision

Use automated tests throughout backend development, with a test-driven approach for important business behavior.

### Initial Test Priorities

1. Only administrators can approve or decline requests.
2. Only approved requests can produce work orders.
3. A request cannot produce duplicate work orders.
4. Only active technicians can be assigned.
5. Technicians can access only their assigned work orders.
6. Invalid status transitions are rejected.
7. Completion notes cannot be empty.
8. Only administrators can close submitted work orders.
9. Important successful actions create audit records.

### Rationale

- Helps detect regressions.
- Encourages clear business rules.
- Makes implementation behavior verifiable.

### Consequences

- Tests require development time.
- Test data and database setup must be maintained.
- Business rules should be designed to be testable.

## 12. ADR-009 — Keep Completion Photos Optional

**Status:** Proposed

### Context

Photos may provide useful evidence for installations and repairs, but file uploads introduce storage and security concerns.

### Decision

Treat completion photos as a Should Have feature that will be implemented only after the core MVP is functional.

### Rationale

- Protects the project schedule.
- Prioritizes the main service workflow.
- Avoids introducing unnecessary storage complexity early.

### Consequences

- Completion notes remain mandatory.
- Photo storage and upload validation can be designed later.
- The MVP must work without photos.

## 13. Initial Security Considerations

The architecture must consider:

- Secure authentication and session management.
- Password hashing using established framework mechanisms.
- Backend role and object-level authorization.
- Validation of user-supplied input.
- Protection against unauthorized record access.
- Safe handling of customer contact information.
- Secure configuration of secrets and environment variables.
- Database integrity and transaction handling.
- Audit history access restrictions.
- File upload security if optional photos are implemented.

Specific authentication mechanisms and deployment controls will be selected during architecture design.

## 14. Proposed System Boundaries

### Frontend Responsibilities

- Display forms and work-order information.
- Collect user input.
- Display validation feedback.
- Provide role-appropriate navigation.
- Call backend APIs.

### Backend Responsibilities

- Authenticate users.
- Authorize operations.
- Validate business rules.
- Enforce state transitions.
- Manage service requests and work orders.
- Record important audit events.
- Expose application APIs.

### Database Responsibilities

- Persist business records.
- Maintain relational integrity.
- Enforce appropriate uniqueness constraints.
- Support transactional consistency.

The backend remains the authoritative source for business rules.

## 15. Deferred Architecture Decisions

The following decisions remain open:

1. Exact Django application boundaries.
2. Authentication mechanism and session handling.
3. API endpoint naming and versioning.
4. Database entity relationships.
5. Error response conventions.
6. Frontend testing framework.
7. Deployment platform.
8. Hosting and backup strategy.
9. Audit record retention policy.
10. File storage strategy for optional photos.
11. Monitoring and operational logging.

These topics will be reviewed during Day 2 domain modelling and Day 3 architecture design.

## 16. Next Steps

1. Review the initial architecture proposals against the functional requirements.
2. Model the core domain entities and relationships.
3. Define permitted state transitions and exception workflows.
4. Finalize the main architecture decisions.
5. Create a minimal backend and frontend foundation.
6. Implement the core workflow incrementally with automated tests.

This document is a starting point for technical decision-making and should be updated as the FieldOps architecture evolves.