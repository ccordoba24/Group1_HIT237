### ADR 1 : Normalised Database Models for Housing and Requests

**Status:** Accepted

**Context**  
We needed to model Communities, Dwellings, Tenants, Categories, Repair Requests, and Maintenance Updates in a maintainable way that supports efficient querying and preserves data relationships.

**Alternatives considered**  
- **Single model with JSON blobs**: Simple initial setup, but searching and maintaining relationships inside JSON becomes difficult and loses database integrity.  
- **Partially denormalised models** (e.g., duplicating address data): Fewer joins but leads to data inconsistency when values need updating in multiple places.

**Decision**  
We chose a **fully normalised relational model** using Django `ForeignKey`, `OneToOneField`, and appropriate relationships. This keeps the domain model clean and allows the database to enforce referential integrity.

**Code reference**  
- `proj_1/housing/models.py:13–22` — Dwelling model  
- `proj_1/housing/models.py:25–31` — Tenant model  
- `proj_1/housing/models.py:40–64` — RepairRequest model  
- `proj_1/housing/models.py:66–76` — MaintenanceUpdate model

**Consequences**  
**Pros:** Clean domain separation, readable ORM queries, strong data integrity.  
**Cons:** Requires more joins for complex queries — mitigated using `select_related()` (see ADR 9).

---

### ADR 2 : Use Django ModelForm for Repair Request Input

**Status:** Accepted

**Context**  
Forms for creating and updating repair requests needed to stay in sync with model validation rules without duplicating code.

**Alternatives considered**  
- **Manual `forms.Form`**: Full control but requires re-declaring every field, increasing risk of missing validation rules.  
- **Third-party form libraries**: Added unnecessary dependency and learning curve for standard CRUD forms.

**Decision**  
We used Django’s **`ModelForm`** so form fields and validation are automatically derived from the model. This keeps the code DRY and integrates perfectly with class-based views.

**Code reference**  
- `proj_1/housing/forms.py:1–12`

**Consequences**  
**Pros:** Less boilerplate, consistent validation, works seamlessly with `CreateView` and `UpdateView`.  
**Cons:** Reduced flexibility for highly custom input flows (handled via `clean_` methods where needed).

---


### ADR 3 : Class-Based Views with QuerySet Optimisation

**Status:** Accepted

**Context**  
List and detail views needed to load related data (category, dwelling, tenant, user) efficiently without causing N+1 query problems.

**Alternatives considered**  
- **Function-based views with manual querysets**: Clear but repetitive and easy to forget eager loading.  
- **Django REST Framework + SPA**: Modern but far beyond the scope of this assignment.

**Decision**  
We adopted Django’s **generic class-based views** (`ListView`, `DetailView`, `CreateView`, `UpdateView`) and overrode `get_queryset()` to include `select_related()` for eager loading.

**Code reference**  
- `proj_1/housing/views.py:12–17` — List view with `select_related()` and `order_by()`  
- `proj_1/housing/views.py:25–28` — Detail view queryset  
- `proj_1/housing/views.py:7–45` — All CBV definitions

**Consequences**  
**Pros:** Much less code, consistent patterns across CRUD operations, good performance by default.  
**Cons:** CBVs can obscure control flow — understanding lifecycle methods (`get_queryset`, `form_valid`, etc.) is important (documented in comments).

---
