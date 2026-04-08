# ADR 1: Use Django ORM for database interaction

## Status
Accepted

## Context
We needed a way to manage and interact with the database efficiently.

## Alternatives
- Raw SQL (more control but complex)
- Django ORM (simpler and integrated with Django)

## Decision
We chose Django ORM because it simplifies database operations and integrates well with Django.

## Code reference
models.py

## Consequences
Faster development but less control over low-level queries.




# ADR 2: Use Class-Based Views for handling requests

## Status
Accepted

## Context
We needed a structured way to handle application logic and user requests in Django.

## Alternatives
- Function-based views (simpler but less reusable)
- Class-based views (more structured and reusable)

## Decision
We chose class-based views because they allow better organisation, code reuse, and scalability.

## Code reference
views.py

## Consequences
More complex initially, but improves maintainability and structure in the long term.
