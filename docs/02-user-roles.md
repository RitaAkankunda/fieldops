# FieldOps — User Roles and Permissions

## 1. Purpose

This document defines the proposed user roles, responsibilities, and access permissions for the FieldOps MVP.

These permissions are initial design decisions based on our discovery exercise. They have not yet been validated with a real business.

## 2. User Roles

### 2.1 Administrator / Coordinator

The administrator manages customer requests and coordinates field service operations.

**Responsibilities:**
- Register customer service requests.
- View and update requests.
- Approve or decline requests.
- Create work orders for approved requests.
- Register and manage technicians.
- Assign and reassign technicians.
- Monitor work-order progress.
- Review submitted completion notes.
- Close completed work orders.
- View request and work-order history.

### 2.2 Technician

The technician performs assigned field service work.

**Responsibilities:**
- View work orders assigned to them.
- View the customer and site information needed for assigned work.
- Update the progress of assigned jobs.
- Record work performed.
- Submit completion notes.
- Optionally attach job completion photos.

Technicians cannot approve service requests, create work orders, or assign other technicians.

## 3. Proposed Permission Matrix

| Action | Administrator | Technician |
|---|---|---|
| Register service request | Yes | No |
| View all service requests | Yes | No |
| Approve or decline request | Yes | No |
| Create work order | Yes | No |
| Assign technician | Yes | No |
| View all work orders | Yes | No |
| View own assigned work orders | Yes | Yes |
| Update assigned job progress | No | Yes |
| Submit completion notes | No | Yes |
| Review job completion | Yes | No |
| Close work order | Yes | No |
| View request history | Yes | Limited to assigned work |

## 4. Access Control Principles

- Users must authenticate before accessing protected resources.
- Permissions must be enforced on the backend.
- Technicians may access only work orders assigned to them.
- Only administrators may approve or decline service requests.
- Only the assigned technician may submit job completion.
- Important actions should record the responsible user and timestamp.

## 5. Future Roles

The following roles are outside the initial MVP:

- Business owner / manager with separate permissions.
- Customer.
- Storekeeper.
- Accountant.
- Supervisor / team leader.

These roles may be introduced if future requirements justify them.

## 6. Open Questions

- Can an administrator also perform technician duties?
- Can an administrator correct a technician's progress record?
- What happens to job access after technician reassignment?
- Should technicians see customer phone numbers?
- Who manages user accounts and technician activation?

These questions must be resolved before implementing the affected permissions.