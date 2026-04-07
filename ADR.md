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
