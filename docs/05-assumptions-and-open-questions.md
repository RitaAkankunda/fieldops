# FieldOps — Assumptions and Open Questions

## 1. Purpose

This document records the assumptions, unresolved questions, risks, and provisional decisions identified during the discovery and planning of FieldOps.

FieldOps is a proposed field service management system for small businesses that provide CCTV installation and repair, networking, electrical, and related technical services.

The document helps the project avoid treating unverified beliefs as confirmed business requirements.

It will be updated as new information is gathered through stakeholder feedback, domain modelling, implementation, and testing.

## 2. Project Context

FieldOps aims to help small service businesses manage customer service requests and technician work orders in a more structured and traceable way.

The proposed core workflow is:

1. An administrator registers a service request.
2. The system generates a unique request reference.
3. The administrator reviews and approves or declines the request.
4. An approved request can be converted into a work order.
5. An administrator assigns an active technician.
6. The technician views and starts the assigned job.
7. The technician submits completion notes.
8. The administrator reviews the completion information.
9. The administrator formally closes the work order.

Important changes are recorded in the system's audit history.

This workflow is the proposed MVP design, not a process confirmed through interviews with a real service business.

---

## 3. Assumptions

The following assumptions have not yet been fully validated.

### A-01 — Service Requests Are Currently Managed Across Multiple Channels

**Assumption:**

Small CCTV, networking, and electrical service businesses may receive customer requests through phone calls, WhatsApp, walk-ins, email, social media, or other informal channels.

**Why It Matters:**

Requests received across multiple channels may be difficult to track consistently.

**Validation Needed:**

Interview service business owners or administrators to understand their actual request intake processes.

**Status:** Unvalidated

### A-02 — Some Service Requests May Be Forgotten or Delayed

**Assumption:**

Without a centralized request register, businesses may lose track of requests, delay follow-up, or struggle to determine which jobs are pending.

**Why It Matters:**

This is a central problem that FieldOps intends to address.

**Validation Needed:**

Ask business owners for examples of missed requests, delayed jobs, or difficulties tracking work.

**Status:** Unvalidated

### A-03 — Small Businesses Need a Simple System

**Assumption:**

Small service businesses may prefer a lightweight application over a complex enterprise field service management platform.

**Why It Matters:**

The MVP should prioritize essential workflows and ease of use.

**Validation Needed:**

Ask potential users which existing tools they use and which features they consider essential.

**Status:** Unvalidated

### A-04 — Administrators Manage Incoming Requests

**Assumption:**

An administrator or business owner usually records incoming customer requests and decides which jobs should proceed.

**Why It Matters:**

This assumption influences role permissions and request approval workflows.

**Validation Needed:**

Confirm who handles request intake and approval in actual service businesses.

**Status:** Unvalidated

### A-05 — Technicians Need Access to Assigned Jobs

**Assumption:**

Technicians benefit from being able to view their assigned jobs and report progress without relying entirely on phone calls or messaging.

**Why It Matters:**

This supports the technician work-order interface.

**Validation Needed:**

Ask technicians how they currently receive assignments and report job completion.

**Status:** Unvalidated

### A-06 — One Technician per Work Order Is Sufficient for the MVP

**Assumption:**

Supporting one currently assigned technician per work order will cover enough basic scenarios for an initial prototype.

**Why It Matters:**

It simplifies assignment rules, authorization, and domain modelling.

**Validation Needed:**

Investigate how frequently real jobs require multiple technicians.

**Status:** Provisional MVP simplification

### A-07 — Completion Notes Are Useful for Administrative Review

**Assumption:**

Written completion notes help administrators understand the work performed and decide whether a job can be closed.

**Why It Matters:**

FieldOps requires completion notes before a technician can submit a job for review.

**Validation Needed:**

Ask administrators what evidence they currently require before considering a job complete.

**Status:** Provisional MVP rule; business value unvalidated

### A-08 — Users Will Have Sufficient Internet Access

**Assumption:**

Administrators and technicians will usually have internet access when using FieldOps.

**Why It Matters:**

The proposed MVP is a web application and does not initially include offline synchronization.

**Validation Needed:**

Investigate internet reliability at offices and customer sites.

**Status:** Unvalidated

### A-09 — A Centralized History Will Improve Traceability

**Assumption:**

Recording status changes, assignments, and completion events will help administrators understand job progress and investigate delays.

**Why It Matters:**

This supports audit history as a core requirement.

**Validation Needed:**

Evaluate whether business users can answer operational questions more easily using the proposed history.

**Status:** Unvalidated benefit; audit recording selected for MVP

### A-10 — Manual Request Registration Is Acceptable Initially

**Assumption:**

Administrators can manually register requests received through external channels without requiring immediate WhatsApp, SMS, email, or website integrations.

**Why It Matters:**

Manual registration reduces implementation complexity.

**Validation Needed:**

Determine whether manual entry is practical given the number of requests a business receives.

**Status:** Provisional MVP decision

---

## 4. Confirmed Project Decisions

The following decisions have been selected for the proposed MVP. They are confirmed as current project scope decisions, but they are not necessarily validated real-world business practices.

| ID | Decision | Rationale |
|---|---|---|
| D-01 | The MVP supports Administrator and Technician roles. | Keeps authorization manageable. |
| D-02 | Administrators register service requests manually. | Avoids early integration complexity. |
| D-03 | Every registered request receives a unique reference. | Supports identification and tracking. |
| D-04 | New requests begin in `PENDING_REVIEW`. | Establishes a clear review stage. |
| D-05 | Administrators approve or decline requests. | Separates request intake from execution. |
| D-06 | Only approved requests can produce work orders. | Prevents unauthorized progression. |
| D-07 | Each request produces at most one work order in the MVP. | Prevents duplicate jobs and simplifies modelling. |
| D-08 | Each work order has at most one currently assigned technician. | Simplifies assignment and access control. |
| D-09 | Only active technicians can be assigned. | Prevents assignment to inactive accounts. |
| D-10 | Technicians can access only their currently assigned work orders. | Protects job information. |
| D-11 | Work-order status changes follow permitted transitions. | Preserves workflow consistency. |
| D-12 | Technicians must submit nonempty completion notes. | Provides basic evidence for review. |
| D-13 | Administrators formally close completed work orders. | Separates reporting from approval. |
| D-14 | Important business changes are recorded in audit history. | Supports traceability. |
| D-15 | Completion photos are optional. | Protects the core MVP schedule. |

These decisions may be revised if domain modelling or stakeholder validation reveals important limitations.

---

## 5. Open Business Questions

### OQ-01 — Customer Cancellation

**Question:** Can a customer cancel a service request after it has been registered or approved?

**Why It Matters:** Cancellation affects request status, work-order status, and audit history.

**Provisional Approach:** Do not introduce cancellation transitions until the rules are clarified.

**Target:** Day 2 domain modelling

### OQ-02 — Work-Order Cancellation

**Question:** Can an administrator cancel a work order after a technician has been assigned or started work?

**Why It Matters:** The system must distinguish cancelled work from completed work.

**Target:** Day 2 domain modelling

### OQ-03 — Paused or Blocked Jobs

**Question:** What should happen when a technician cannot continue because of missing materials, customer unavailability, or technical difficulties?

**Why It Matters:** The normal workflow currently moves from `ASSIGNED` to `IN_PROGRESS` to `COMPLETION_SUBMITTED`.

**Target:** Day 2 domain modelling

### OQ-04 — Multiple Site Visits

**Question:** How should FieldOps represent a job that requires more than one customer visit?

**Why It Matters:** A single work order may not always correspond to one visit.

**Target:** Day 2 domain modelling

### OQ-05 — Reassignment During Active Work

**Question:** What happens if an administrator reassigns a work order while it is `IN_PROGRESS`?

**Why It Matters:** The system must preserve previous assignment history, enforce current access permissions, and decide whether the status changes.

**Target:** Day 2 domain modelling

### OQ-06 — Rejected Completion Reports

**Question:** Can an administrator reject a technician's completion submission and return the work order for corrections?

**Why It Matters:** The current normal workflow describes approval and closure but not the correction process.

**Target:** Day 2 domain modelling

### OQ-07 — Reopening Closed Work Orders

**Question:** Can a closed work order be reopened if the customer reports that the problem persists?

**Why It Matters:** Reopening affects status transitions, audit history, and responsibility for follow-up work.

**Target:** Day 2 domain modelling

### OQ-08 — Request Reference Format

**Question:** What format should unique service request references use?

**Examples:** `REQ-0001`, `REQ-2026-0001`

**Why It Matters:** The format affects readability, uniqueness, and possible future scaling.

**Target:** Domain and technical design

### OQ-09 — Technician Scheduling Conflicts

**Question:** Should the system warn administrators when a technician is assigned overlapping jobs?

**Why It Matters:** Scheduling conflicts may affect service delivery.

**Provisional Approach:** Automatic conflict detection is outside the core MVP.

**Target:** Future validation

### OQ-10 — Completion Evidence

**Question:** What information should technicians provide beyond completion notes?

**Examples:** Photos, time spent, materials used, customer signature.

**Why It Matters:** Different service businesses may require different evidence.

**Target:** Stakeholder validation

### OQ-11 — Customer Information

**Question:** Which customer details are essential, and how should repeated customers be handled?

**Why It Matters:** The system must balance practical request registration with avoiding unnecessary duplicate data.

**Target:** Day 2 domain modelling

### OQ-12 — Audit History Visibility

**Question:** Should technicians be able to view the history of their assigned work orders, or should history be restricted to administrators?

**Why It Matters:** This affects permissions and information visibility.

**Target:** Security and domain design

### OQ-13 — Data Retention and Privacy

**Question:** How long should customer contact details, work-order history, and completion photos be retained?

**Why It Matters:** The system handles customer information that should be protected and retained only as needed.

**Target:** Security design and stakeholder validation

### OQ-14 — User Account Management

**Question:** Who creates technician accounts, deactivates users, and resets access credentials?

**Why It Matters:** User lifecycle management affects authentication, authorization, and operational security.

**Target:** Architecture and security design

---

## 6. Project Risks

| ID | Risk | Potential Impact | Mitigation |
|---|---|---|---|
| R-01 | Requirements are based on unvalidated assumptions. | The application may not match real business needs. | Seek stakeholder feedback and document findings. |
| R-02 | Scope expands beyond the 30-day MVP. | Core functionality may remain unfinished. | Prioritize Must Have requirements. |
| R-03 | Work-order status rules become inconsistent. | Jobs may enter invalid states. | Define and test permitted transitions. |
| R-04 | Authorization is implemented only in the frontend. | Users may access or modify unauthorized work orders. | Enforce permissions in the backend. |
| R-05 | Duplicate work orders are created concurrently. | A single request may produce multiple jobs. | Enforce uniqueness at the database level. |
| R-06 | Audit history is incomplete. | Administrators may be unable to trace important changes. | Save business changes and audit records consistently. |
| R-07 | File uploads introduce security or storage problems. | Sensitive files may be exposed or uploads may fail. | Keep photos optional and validate access, type, and size. |
| R-08 | Development time is underestimated. | Planned features may not be completed. | Deliver a working vertical slice before optional features. |
| R-09 | Internet access is unreliable at customer sites. | Technicians may be unable to update jobs immediately. | Validate connectivity assumptions; defer offline support unless essential. |

---

## 7. MVP Scope Boundaries

### Included in the Core MVP

- Administrator and Technician roles.
- Manual service request registration.
- Unique service request references.
- Request listing and filtering.
- Request approval and decline.
- Work-order creation from approved requests.
- Manual technician assignment.
- Technician access to assigned work orders.
- Work-order progress updates.
- Mandatory completion notes.
- Administrator completion review and closure.
- Audit history for important business events.

### Optional If Time Allows

- Completion photo uploads.

### Excluded from the Core MVP

- Automated WhatsApp, SMS, and email integrations.
- Customer self-service portal.
- Invoicing and payment processing.
- Inventory management.
- GPS tracking.
- Automated technician scheduling.
- Multi-technician work-order teams.
- AI-based dispatch or job recommendations.
- Advanced reporting and analytics.
- Offline synchronization.

Excluded features may be considered in future versions after the core workflow is implemented and evaluated.

---

## 8. Validation Plan

To improve confidence in the proposed requirements, the project should seek feedback from potential users.

### Suggested Stakeholders

- Owners of small CCTV or networking service businesses.
- Administrators who register and coordinate customer jobs.
- Field technicians who perform installation, repair, and maintenance work.

### Suggested Interview Questions

1. How do customers usually contact your business to request service?
2. How do you currently record incoming requests?
3. Have requests ever been forgotten or delayed? What caused that?
4. Who decides whether a request should become a job?
5. How are technicians assigned to jobs?
6. How do technicians report that work has started or finished?
7. What happens when a job cannot be completed during the first visit?
8. What information must a technician provide before a job can be closed?
9. What problems do you experience with your current process?
10. Which three features would be most valuable in a simple job-tracking application?

### Validation Approach

1. Interview potential users when possible.
2. Record observations separately from assumptions.
3. Identify where actual workflows differ from the proposed FieldOps workflow.
4. Update requirements and domain rules based on credible findings.
5. Keep a record of significant decisions and their rationale.

No stakeholder interviews or validation results are claimed in this document.

---

## 9. Decision and Question Tracking

Open questions should be reviewed before their associated functionality is implemented.

When an open question is resolved, record:

- The question identifier.
- The chosen decision.
- The reason for the decision.
- The date of the decision.
- Any affected functional requirements or workflows.

Decisions that change the MVP scope should also be reflected in the functional requirements and business workflows documents.

---

## 10. Next Steps

The immediate next steps are:

1. Review and finalize the initial discovery documentation.
2. Model the main FieldOps domain entities and their relationships.
3. Define service request and work-order state transitions.
4. Resolve high-priority workflow exceptions.
5. Establish the initial system architecture and security boundaries.
6. Begin implementation using small, testable development increments.

This document is a living record and should evolve as FieldOps is designed, implemented, and evaluated.