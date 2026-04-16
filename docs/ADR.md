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

### ADR 4 : Server-Side Rendering with Django Templates

**Status:** Accepted

**Context**  
We needed a simple, reliable UI that could be quickly built and easily demonstrated during the viva without a complex frontend setup.

**Alternatives considered**  
- **JSON API + Single Page Application**: Better user experience but required serializers, CORS, and a separate frontend framework.  
- **Hybrid SSR + JS enhancement**: Added complexity with little benefit for this project’s scope.

**Decision**  
We used **Django templates** for all primary views. The UI is fully server-rendered with no additional build tools required.

**Code reference**  
- `proj_1/housing/templates/housing/repair_request_list.html:1–35`  
- `proj_1/housing/views.py:7–45` (views referencing templates)
- Additional static pages served as TemplateViews with no model 
  logic: `HomeView`, `RegisterView`, `FAQView`, `AboutView` 
  — confirming the template-first approach throughout the project  
  (`proj_1/housing/views.py` — HomeView, RegisterView, FAQView, AboutView)


**Consequences**  
**Pros:** Fast development, zero frontend dependencies, straightforward to demo live.  
**Cons:** Less dynamic than a modern SPA, but a reasonable trade-off for a backend-focused assignment.

---


### ADR 5 : Resource-Centred URL Structure

**Status:** Accepted

**Context**  
URLs needed to be readable, predictable, and intuitive for both users and future developers.

**Alternatives considered**  
- **Deeply nested URLs** (`/communities/<id>/dwellings/<id>/requests/`): More RESTful but added unnecessary routing complexity.  
- **Flat arbitrary URLs**: Simple but inconsistent and harder to maintain long-term.

**Decision**  
We implemented a **clean, resource-centred URL structure** under the `/requests/` namespace for all repair request operations.

**Code reference**  
- `proj_1/housing/urls.py` — full urlpatterns including:
  - `/` — HomeView  
  - `/requests/` — list, create, detail, edit  
  - `/history/` — completed requests (MaintenanceHistoryView)  
  - `/register/`, `/faq/`, `/about/` — static info pages

**Consequences**  
**Pros:** Easy to understand, maps directly to views, and is REST-friendly.  
**Cons:** May need restructuring later if community- or dwelling-level filtering is required.

---

### ADR 6 : Application of Core Django Design Philosophies

**Status:** Accepted

**Context**  
The assessment required deliberate application and clear documentation of at least three Django design philosophies.

**Decision**  
We applied and documented the following core philosophies:  
- **DRY (Don’t Repeat Yourself)** — Validation logic lives in `ModelForm` and model methods.  
- **Fat Models, Thin Views** — Business logic (e.g. `is_open()`, `open_requests_count`) resides in the models.  
- **Convention over Configuration** — Standard Django app and template structure is used so the framework auto-discovers files.

**Code reference**  
- DRY & Fat Models: `proj_1/housing/models.py:21–22`, `proj_1/housing/models.py:59–63`, `proj_1/housing/forms.py:5–12`  
- Convention over Configuration: `proj_1/proj_1/settings.py:21–29`, `proj_1/housing/templates/housing/repair_request_list.html:1–35`

**Consequences**  
**Pros:** Cleaner, more maintainable code that clearly meets assessment requirements.  
**Cons:** Model-heavy logic means tests require more model setup, but this is a worthwhile trade-off.

---
