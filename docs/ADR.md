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
