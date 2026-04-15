
# ADR 1 Title: Use Django ORM for database interaction

## Status
Accepted

## 16 April 2026, first submission

## Context
We needed an efficient way to manage data and encapsulate business logic. By using Django ORM, we can implement Fat Modes, where complex logic like calculating repair urgency is stored within the model layer rather than the views. 

## Alternatives
- Raw SQL (more control but complex)
- Django ORM (simpler and integrated with Django)

## Decision
We chose Django ORM because it simplifies database operations and integrates well with Django.

## Code reference
models.py

## Consequences
Faster development but less control over low-level queries.
- Encapsulation: Business logic is centralized in the models, making it accessible to both the web UI and  
  potential future API endpoints without duplications.
- Data Integrity: Validation logic is tried directly to the database objects. 


# ADR 2: Use Class-Based Views for handling requests

## Status
Accepted

## Context
We needed a structured way to handle application logic and user requests in Django.

## Alternatives
- Function-based views (simpler but less reusable)
- Class-based views (more structured and reusable)

## Decision
We chose class-based Views, specifically Django's generic views becuse it provides a standardised way to handle CRUD operations with minimal code.
- Thin views remain "thin" as they only handle the flow of the requests (dispatching, template rendering), 
  while the heavy lifting is delegated to the models.
- Consistency: Using the built-in CRUD views ensures that the user experience creating, reading, updating  
  and deleting records remains consistent across the app

## Code reference
views.py

## Consequences
More complex initially, but improves maintainability and structure in the long term.
