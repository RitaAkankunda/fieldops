# FieldOps — Business Workflows

## 1. Purpose

This document describes the main business workflows supported by the FieldOps minimum viable product (MVP).

It explains how administrators and technicians interact with the system, from registering a customer service request to completing and closing a work order.

These workflows are based on the proposed functional requirements and will guide domain modelling, system design, implementation, and testing.

## 2. Workflow Actors

### Administrator

The administrator manages incoming service requests, approves or declines requests, creates work orders, assigns technicians, reviews completed work, and formally closes work orders.

### Technician

The technician views assigned work orders, starts assigned jobs, updates work progress, and submits completion notes for administrator review.

## 3. Main Business Process

The proposed FieldOps workflow follows this sequence:

1. An administrator registers a customer service request.
2. The system generates a unique request reference.
3. The administrator reviews the request.
4. The administrator approves or declines the request.
5. If approved, the administrator creates a work order.
6. The administrator assigns an active technician.
7. The technician views their assigned work order.
8. The technician starts work and updates its progress.
9. The technician submits completion notes.
10. The administrator reviews the completion information.
11. The administrator formally closes the work order.

Important changes are recorded in the audit history throughout the process.

The following sections describe each workflow in greater detail.

## 4. Workflow 01 — Register a Service Request

**Primary Actor:** Administrator

**Trigger:** A customer contacts the business to request an installation, repair, or maintenance service.

**Preconditions:**
- The administrator is authenticated.
- The administrator has collected the customer's basic information.

### Main Flow

1. The administrator opens the service request registration form.
2. The administrator enters the customer's name, phone number, and service address.
3. The administrator selects the service type: installation, repair, or maintenance.
4. The administrator enters a description of the customer's problem or requested service.
5. The administrator submits the form.
6. The system validates the required information.
7. The system creates the service request.
8. The system generates a unique request reference.
9. The system sets the request status to `PENDING_REVIEW`.
10. The system records the creation event, administrator, and timestamp.
11. The system displays confirmation with the request reference.

### Alternative Flows

- **A1 — Missing information:** The system rejects the submission and identifies the missing required fields.
- **A2 — Invalid information:** The system displays validation errors and allows the administrator to correct the data.
- **A3 — Registration failure:** The system reports the failure without confirming that the request was saved.

**Postcondition:** A new service request exists in `PENDING_REVIEW` with a unique reference.

**Related Requirements:** FR-01, FR-02, FR-11

---

## 5. Workflow 02 — Review and Decide on a Service Request

**Primary Actor:** Administrator

**Trigger:** An administrator opens a request awaiting review.

**Preconditions:**
- The administrator is authenticated.
- The request exists and is in `PENDING_REVIEW`.

### Main Flow

1. The administrator opens the service request list.
2. The administrator filters or selects a request in `PENDING_REVIEW`.
3. The system displays the request details.
4. The administrator reviews the customer information and service description.
5. The administrator chooses to approve or decline the request.
6. The system validates the decision.
7. The system records the decision, responsible administrator, and timestamp.
8. The system updates the request status.

### Alternative Flows

- **A1 — Approved:** The request status becomes `APPROVED`, making it eligible for work-order creation.
- **A2 — Declined:** The administrator must provide a decline reason. The request status becomes `DECLINED`.
- **A3 — Missing decline reason:** The system rejects the decline action.
- **A4 — Already decided:** The system rejects another decision through the normal review workflow.
- **A5 — Unauthorized user:** The system denies the action.

**Postcondition:** The request is either `APPROVED` or `DECLINED`, with its decision history preserved.

**Related Requirements:** FR-03, FR-04, FR-11

---

## 6. Workflow 03 — Create a Work Order

**Primary Actor:** Administrator

**Trigger:** An administrator decides to prepare an approved service request for execution.

**Preconditions:**
- The administrator is authenticated.
- The service request is `APPROVED`.
- No work order already exists for that request.

### Main Flow

1. The administrator opens the approved service request.
2. The administrator selects the action to create a work order.
3. The system verifies that the request is approved.
4. The system verifies that the request does not already have a work order.
5. The system creates a work order linked to the service request.
6. The system sets the work-order status to `UNASSIGNED`.
7. The system records the creation event.
8. The system displays the new work order.

### Alternative Flows

- **A1 — Request not approved:** The system rejects work-order creation.
- **A2 — Work order already exists:** The system prevents duplicate creation.
- **A3 — Concurrent creation attempts:** The system ensures that at most one work order is created for the request.

**Postcondition:** One unassigned work order exists for the approved service request.

**Related Requirements:** FR-05, FR-11

---

## 7. Workflow 04 — Assign a Technician

**Primary Actor:** Administrator

**Trigger:** A work order is ready to be assigned.

**Preconditions:**
- The administrator is authenticated.
- The work order exists.
- At least one active technician is available for selection.

### Main Flow

1. The administrator opens the work order.
2. The administrator selects the technician assignment action.
3. The system displays eligible active technicians.
4. The administrator selects a technician.
5. The system validates the technician's eligibility.
6. The system assigns the technician to the work order.
7. If the work order was `UNASSIGNED`, its status changes to `ASSIGNED`.
8. The system records the assignment event, responsible administrator, and timestamp.
9. The system displays the updated assignment.

### Alternative Flows

- **A1 — Inactive technician:** The system rejects the assignment.
- **A2 — No technician selected:** The work order remains unassigned.
- **A3 — Reassignment:** The administrator selects a different active technician. The system records the previous and new assignments.
- **A4 — Former technician access:** After reassignment, the former technician can no longer access the work order as an assigned job.

**Postcondition:** The work order is assigned to one active technician, or remains unassigned if no assignment is completed.

**Related Requirements:** FR-06, FR-07, FR-11

**Open Question:** Reassignment of an `IN_PROGRESS` work order requires additional business rules, to be defined during Day 2.

---

## 8. Workflow 05 — View and Start an Assigned Work Order

**Primary Actor:** Technician

**Trigger:** A technician logs in to review their assigned jobs.

**Preconditions:**
- The technician is authenticated.
- The technician has at least one currently assigned work order.

### Main Flow

1. The technician opens their assigned work-order list.
2. The system displays only work orders currently assigned to that technician.
3. The technician selects a work order.
4. The system verifies that the technician is still assigned to it.
5. The system displays the work-order details.
6. If the status is `ASSIGNED`, the technician selects the action to start work.
7. The system validates the status transition.
8. The system changes the status to `IN_PROGRESS`.
9. The system records the technician, previous status, new status, and timestamp.

### Alternative Flows

- **A1 — No assigned jobs:** The system displays an empty assigned-work list.
- **A2 — Another technician's work order:** The system denies access.
- **A3 — Already in progress:** The system does not create a duplicate start event.
- **A4 — Invalid status:** The system rejects the requested transition.

**Postcondition:** The technician can view the assigned job, and a successfully started job is in `IN_PROGRESS`.

**Related Requirements:** FR-07, FR-08, FR-11

---

## 9. Workflow 06 — Submit Job Completion

**Primary Actor:** Technician

**Trigger:** The technician finishes the work and is ready to report completion.

**Preconditions:**
- The technician is authenticated.
- The work order is currently assigned to the technician.
- The work-order status is `IN_PROGRESS`.

### Main Flow

1. The technician opens the work order.
2. The technician selects the completion submission action.
3. The technician enters notes describing the work performed.
4. The technician optionally attaches completion photos, if the photo feature is available.
5. The technician submits the completion information.
6. The system verifies the technician's assignment.
7. The system verifies that the work order is `IN_PROGRESS`.
8. The system validates that completion notes are not empty or whitespace-only.
9. The system saves the completion information.
10. The system changes the status to `COMPLETION_SUBMITTED`.
11. The system records the submitting technician and timestamp.
12. The system confirms that the submission is awaiting administrator review.

### Alternative Flows

- **A1 — Missing notes:** The system rejects submission and requests completion notes.
- **A2 — Invalid status:** The system rejects submission.
- **A3 — Unauthorized technician:** The system denies the action.
- **A4 — No photos:** Submission succeeds without photos.
- **A5 — Duplicate submission:** The system prevents duplicate completion records.

**Postcondition:** The work order is in `COMPLETION_SUBMITTED`, awaiting administrator review.

**Related Requirements:** FR-08, FR-09, FR-11, FR-12 (optional)

---

## 10. Workflow 07 — Review and Close a Work Order

**Primary Actor:** Administrator

**Trigger:** A technician submits a work order for completion review.

**Preconditions:**
- The administrator is authenticated.
- The work-order status is `COMPLETION_SUBMITTED`.

### Main Flow

1. The administrator opens the work order.
2. The system displays the completion notes, responsible technician, and submission timestamp.
3. The administrator reviews the completion information.
4. The administrator decides to accept the reported completion.
5. The system verifies that the work order is eligible for closure.
6. The system changes the status to `CLOSED`.
7. The system records the closing administrator and timestamp.
8. The system preserves the completion notes and history.
9. The system displays the closed work order.

### Alternative Flows

- **A1 — Work order not submitted:** The system rejects closure.
- **A2 — Unauthorized user:** The system denies the closure action.
- **A3 — Already closed:** The system prevents duplicate closure events.
- **A4 — Completion information is unsatisfactory:** The administrator does not close the work order. The procedure for returning work for correction remains an open question for Day 2.

**Postcondition:** The accepted work order is `CLOSED`, with closure information preserved.

**Related Requirements:** FR-10, FR-11

---

## 11. Cross-Cutting Workflow — Record Audit History

**Primary Actor:** System

**Trigger:** An important business event occurs.

### Main Flow

1. A user performs a permitted business action.
2. The system validates the action.
3. The system prepares the corresponding business change.
4. The system records the event type, responsible user, and timestamp.
5. Where relevant, the system records previous and new values.
6. The system saves the business change and its required audit record consistently.
7. An authorized administrator can later view the recorded history.

### Alternative Flows

- **A1 — Invalid action:** The system rejects the action without recording it as a successful business event.
- **A2 — Save failure:** The system must not leave a successful business change without its required audit record.
- **A3 — Unauthorized modification:** The system prevents ordinary users from editing or deleting audit history.

**Postcondition:** Important successful business events remain traceable.

**Related Requirements:** FR-11

---

## 12. Workflow Exceptions and Open Questions

The workflows above describe the proposed MVP's normal business process. The following situations require further analysis:

1. What happens when a customer cancels a request or job?
2. Can a technician pause work that has already started?
3. How should the system handle a job requiring multiple visits?
4. What happens when a technician is reassigned while work is in progress?
5. Can an administrator reject a completion submission and request corrections?
6. Can a closed work order be reopened?
7. Should administrators be able to close a job with additional closure notes?

These questions will be examined during Day 2 domain modelling. They should not be treated as already-decided business rules.

## 13. MVP Scope Notes

The following features are outside the core MVP:

- Automated WhatsApp, email, or SMS integrations.
- Customer self-service portal.
- Inventory and materials management.
- Invoicing and payments.
- GPS technician tracking.
- Automated technician scheduling.
- Multi-technician work-order teams.
- Advanced photo and media management.

Completion photos are a **Should Have** feature and may be implemented after the core workflow is complete.