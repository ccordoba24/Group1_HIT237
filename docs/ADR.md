Architecture Decision Records (ADRs)
Project: Housing Repair Request Management System
Repository: 
Last Updated: April 2026

This living document records the key architectural and design decisions made throughout the development of the Django-based housing repair request application. Each entry explains the context, alternatives considered, the chosen decision with rationale, exact code references, and consequences.

The commit history of this file demonstrates how decisions evolved as the project progressed.

ADR 1 : Normalised Database Models for Housing and Requests
Status: Accepted

Context
We needed to model Communities, Dwellings, Tenants, Categories, Repair Requests, and Maintenance Updates in a maintainable way that supports efficient querying and preserves data relationships.

Alternatives considered

Single model with JSON blobs: Simple initial setup, but searching and maintaining relationships inside JSON becomes difficult and loses database integrity.
Partially denormalised models (e.g., duplicating address data): Fewer joins but leads to data inconsistency when values need updating in multiple places.
Decision
We chose a fully normalised relational model using Django ForeignKey, OneToOneField, and appropriate relationships. This keeps the domain model clean and allows the database to enforce referential integrity.

Code reference

proj_1/housing/models.py:13–22 — Dwelling model
proj_1/housing/models.py:25–31 — Tenant model
proj_1/housing/models.py:40–64 — RepairRequest model
proj_1/housing/models.py:66–76 — MaintenanceUpdate model
Consequences
Pros: Clean domain separation, readable ORM queries, strong data integrity.
Cons: Requires more joins for complex queries — mitigated using select_related() (see ADR 9).
