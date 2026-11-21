# FieldOps — System Architecture and Project Structure

**Project:** FieldOps — Field Service Management System  
**Development Day:** Day 3  
**Status:** Initial architecture design  
**Scope:** 30-day MVP

---

## 1. Purpose

This document defines the initial technical architecture for FieldOps.

It describes the technology stack, application modules, responsibilities, security boundaries, business logic organization, and automated testing strategy.

The architecture is based on the requirements and domain model developed during Days 1 and 2.

## 2. Architectural Style

FieldOps will use a **modular monolith** architecture.

The backend will be a single Django application organized into separate Django apps with clearly defined responsibilities.

This approach was chosen because it:

- Keeps deployment simpler than microservices.
- Supports separation of concerns.
- Makes business rules easier to locate and test.
- Fits the scope of a 30-day learning MVP.
- Allows the application to evolve without unnecessary infrastructure complexity.

## 3. Technology Stack

| Layer | Technology | Responsibility |
|---|---|---|
| Frontend | Next.js and React | User interface |
| Backend | Django | Application logic |
| API | Django REST Framework | HTTP/JSON endpoints |
| Database | PostgreSQL | Persistent data storage |
| Testing | pytest and pytest-django | Automated backend tests |
| Version control | Git and GitHub | Track project changes |

The stack remains subject to adjustment during implementation.

## 4. High-Level Architecture

```text
Administrator / Technician
            |
            v
     Next.js Frontend
            |
        HTTP / JSON
            |
            v
 Django REST Framework
            |
     Business Services
            |
       Django Models
            |
            v
       PostgreSQL
```

The frontend communicates with the backend through an API.

The backend validates user identity, permissions, input, and business rules.

The database stores application records and enforces relevant integrity constraints.

## 5. Frontend Responsibilities

The Next.js frontend will:

- Display login and application screens.
- Display service requests and work orders.
- Provide forms for authorized actions.
- Show role-appropriate navigation.
- Send API requests to the backend.
- Display validation errors and operation results.

The frontend must not be treated as the authoritative source for authorization or business rules.

## 6. Backend Responsibilities

The Django backend will:

- Authenticate users.
- Enforce role-based and object-level permissions.
- Validate incoming API data.
- Enforce domain invariants.
- Manage request and work-order state transitions.
- Coordinate database operations.
- Record important audit events.
- Return appropriate API responses.

## 7. Backend Module Structure

The planned Django apps are:

### 7.1 accounts

Responsible for:

- User accounts.
- Authentication.
- Administrator and technician roles.
- Account activation status.
- User-related permissions.

### 7.2 service_requests

Responsible for:

- Registering service requests.
- Viewing and filtering requests.
- Approving or declining requests.
- Enforcing service-request lifecycle rules.

### 7.3 work_orders

Responsible for:

- Creating work orders from approved requests.
- Assigning technicians.
- Managing work-order progress.
- Submitting completion notes.
- Supporting administrator review and closure.
- Enforcing work-order invariants and transitions.

### 7.4 audit

Responsible for:

- Recording important business actions.
- Preserving actor and timestamp information.
- Tracking relevant state and assignment changes.
- Supporting traceability.

## 8. Proposed Project Structure

```text
fieldops/
├── docs/
├── backend/
│   ├── config/
│   ├── accounts/
│   ├── service_requests/
│   ├── work_orders/
│   ├── audit/
│   ├── manage.py
│   ├── conftest.py
│   └── pytest.ini
├── frontend/
└── README.md
```

The folders are being prepared during Day 3.

Django project files and app files will be generated during backend initialization.

## 9. Authentication and Authorization

### 9.1 Authentication

Authentication verifies a user's identity.

FieldOps will use Django's authentication capabilities, with the exact API authentication mechanism selected during implementation.

### 9.2 Role-Based Authorization

The initial roles are:

- `ADMIN`
- `TECHNICIAN`

Administrators manage service requests, assignments, and closure.

Technicians perform authorized actions on their assigned work orders.

### 9.3 Object-Level Authorization

A technician must not access or modify another technician's work order.

The backend must enforce this rule through appropriate query filtering and object-level permission checks.

Frontend visibility restrictions are for usability, not security enforcement.

### 9.4 Active Account Checks

Inactive users must not perform authenticated business actions.

Only active technicians can receive new assignments.

## 10. Business Logic Organization

Important business operations will be implemented through clearly named service functions or equivalent domain-oriented application methods.

Examples include:

- `create_work_order()`
- `assign_technician()`
- `start_work()`
- `submit_completion()`
- `close_work_order()`

API views should coordinate HTTP requests and responses without duplicating complex business rules.

Serializers should validate API input.

Models should represent data and relationships.

Database constraints should protect structural invariants.

## 11. Data Integrity and Transactions

The backend must protect important invariants, including:

- A work order must belong to an approved service request.
- A service request may produce at most one work order.
- A work order may have at most one current technician.
- Invalid state transitions must be rejected.

A unique database relationship or constraint will protect against duplicate work orders.

Operations that update business records and create corresponding audit events should use database transactions where appropriate.

## 12. API Design Principles

The API will:

- Use clear, resource-oriented URLs.
- Accept and return JSON.
- Require authentication for protected operations.
- Validate all user input.
- Return appropriate HTTP status codes.
- Enforce permissions on the backend.
- Avoid exposing records that a user is not authorized to access.

Example planned resources:

```text
/api/service-requests/
/api/work-orders/
/api/users/
```

The exact endpoint names and actions will be finalized during API implementation.

## 13. Testing Strategy

FieldOps will use pytest and pytest-django for backend testing.

### 13.1 Unit Tests

Test isolated business rules and state transition logic.

### 13.2 Integration Tests

Test interactions involving Django models, database constraints, and business services.

### 13.3 API Tests

Test HTTP endpoints, authentication, permissions, input validation, and responses.

### 13.4 Test-Driven Development

Development will follow the Red → Green → Refactor cycle where practical:

1. Write a failing test.
2. Implement the smallest change that makes it pass.
3. Refactor while keeping tests passing.

### 13.5 Priority Test Cases

- Declined requests cannot produce work orders.
- Approved requests cannot produce duplicate work orders.
- Inactive technicians cannot be assigned.
- Unassigned work orders cannot be started.
- Technicians cannot modify other technicians' work orders.
- Invalid state transitions are rejected.
- Completion submissions require notes.
- Technicians cannot close work orders.
- Important business actions create audit events.

## 14. Security Principles

FieldOps will follow these initial security principles:

1. Enforce authentication and authorization on the backend.
2. Apply least-privilege access.
3. Validate all API inputs.
4. Protect sensitive customer information.
5. Avoid storing passwords or secrets in Git.
6. Use environment variables for sensitive configuration.
7. Record important business actions.
8. Test unauthorized access attempts.

## 15. Architecture Decisions and Trade-Offs

| Decision | Reason |
|---|---|
| Modular monolith | Simpler development and deployment |
| Next.js frontend | Component-based web interface |
| Django REST Framework | Structured backend API development |
| PostgreSQL | Relational data integrity |
| Backend authorization | Security cannot depend on frontend controls |
| Service-oriented business operations | Centralized and testable workflows |
| pytest | Supports automated testing and TDD |
| Separate audit module | Improves accountability and traceability |

## 16. Open Architecture Questions

The following decisions will be finalized during implementation:

- Session-based versus token-based API authentication.
- Development and production environment configuration.
- Deployment platform.
- File storage for optional completion photos.
- Exact API endpoint structure.
- Logging and error-reporting strategy.
- Frontend data-fetching approach.

## 17. Day 3 Outcome

The initial FieldOps architecture has been planned.

The main architectural boundaries, backend modules, security responsibilities, and testing strategy are documented.

The next development phase will initialize Django, install dependencies, configure the backend, and begin implementing features using automated tests.

---

**Next Phase:** Backend setup and initial implementation.