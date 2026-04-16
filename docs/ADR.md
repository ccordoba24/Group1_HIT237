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

### ADR 7 : Django Design Patterns Used

**Status:** Accepted

**Context**  
We needed to clearly explain which design patterns were used and why they were appropriate for this project.

**Alternatives considered**  
- Service layer or Repository pattern: More explicit separation but added abstraction not encouraged by Django’s philosophy.

**Decision**  
We used four idiomatic Django patterns:  
- Generic class-based views for CRUD operations  
- ModelForm pattern for DRY form handling  
- QuerySet optimisation with `select_related()`  
- Related-name reverse relations for clean model navigation

**Code reference**  
- Generic CBVs: `proj_1/housing/views.py:7–45`  
- ModelForm: `proj_1/housing/forms.py:5–12`  
- QuerySet optimisation: `proj_1/housing/views.py:12–17`  
- Reverse relations: `proj_1/housing/models.py:66–71`

**Consequences**  
**Pros:** Patterns are familiar to Django developers and easy to explain in the viva.  
**Cons:** Some abstraction (especially in CBVs) requires understanding of Django’s internal lifecycle.

---

### ADR 8 : Explicit Relationship Modelling

**Status:** Accepted

**Context**  
The domain contains natural relationships between tenants, dwellings, communities, and repair requests that must be properly modelled for querying and data integrity.

**Alternatives considered**  
- Storing raw integer foreign keys with manual joins: Error-prone and loses ORM benefits.  
- Using JSON fields for nested data: Flexible but poor for querying and migrations.

**Decision**  
We used `ForeignKey` and `OneToOneField` with `related_name` arguments throughout the models to create clear, enforceable relationships.

**Code reference**  
- `proj_1/housing/models.py:13–16` — Dwelling → Community  
- `proj_1/housing/models.py:25–27` — Tenant → User  
- `proj_1/housing/models.py:47–51` — RepairRequest relationships  
- `proj_1/housing/models.py:66–71` — MaintenanceUpdate reverse relation

**Consequences**  
**Pros:** Expressive queries, database-enforced integrity, easy reverse lookups.  
**Cons:** Schema changes require migrations; `on_delete` behaviour needs careful consideration.

---

### ADR 9 : QuerySet API Usage and Optimisation

**Status:** Accepted

**Context**  
List and detail views display data from multiple related models. Without optimisation this would lead to the N+1 query problem.

**Alternatives considered**  
- Default lazy loading: Simple but causes performance issues.  
- Raw SQL: Full control but loses readability and portability.  
- `prefetch_related()` for everything: Overkill for single-valued foreign keys.

**Decision**  
We used the QuerySet API idiomatically with `select_related()` for ForeignKey/OneToOne fields, `order_by()`, and encapsulated filtering logic in model methods.

**Code reference**  
- `proj_1/housing/views.py:12–17` — `select_related("category", "dwelling", "tenant__user").order_by("-created_at")`  
- `proj_1/housing/views.py:25–28` — Detail view  
- `proj_1/housing/models.py:21–22` — Model method using `exclude()`

**Consequences**  
**Pros:** Eliminates N+1 queries, improves performance, keeps code readable and reusable.  
**Cons:** Requires understanding when to use `select_related()` vs `prefetch_related()`.

---

### ADR 10 : Class-Based Views for All CRUD Operations

**Status:** Accepted

**Context**  
We wanted consistent create, list, detail, and update flows without repeating boilerplate code.

**Alternatives considered**  
- Pure function-based views: Very explicit but verbose and repetitive.  
- API-first approach: Out of scope for this project.

**Decision**  
We used Django’s generic class-based views (`ListView`, `DetailView`, `CreateView`, `UpdateView`) and customised them only where necessary by overriding specific methods.

**Code reference**  
- `proj_1/housing/views.py:7–45` — All four CBV classes

**Consequences**  
**Pros:** Consistent structure, minimal repetition, easy to extend.  
**Cons:** Higher initial learning curve for those new to CBVs.

---

### ADR 11 : Authentication: Default User Model with Profile

**Status:** Accepted

**Context**  
We needed user authentication together with a Tenant profile. Choosing the right approach early was important because changing it later is disruptive.

**Alternatives considered**  
- Custom user model via `AbstractUser`: Recommended by Django but more upfront work.  
- Third-party packages like django-allauth: Powerful but added complexity not needed here.

**Decision**  
We used Django’s **default `auth.User`** model with a `OneToOneField` to the Tenant model. We documented the path to switch to a custom user model later if requirements change.

**Code reference**  
- `proj_1/housing/models.py:23–31` — Tenant model linking to User

**Consequences**  
**Pros:** Quick to implement, well understood, low maintenance for current scope.  
**Cons:** Future migration to custom user model would require careful handling.

---

### ADR 12 : Permission Handling with LoginRequiredMixin and Planned RBAC

**Status:** Accepted (Partially Implemented)

**Context**  
Different user roles (tenants vs staff) require different levels of access to repair requests.

**What’s implemented**  
`LoginRequiredMixin` is applied to create and update views to protect them from unauthenticated users.

**Planned**  
Full role-based access control using custom mixins (`TenantRequiredMixin`, `StaffRequiredMixin`) and object-level ownership checks.

**Code reference**  
- `proj_1/housing/views.py` — `RepairRequestCreateView` and `RepairRequestUpdateView` inherit `LoginRequiredMixin`

**Consequences**  
**Pros:** Basic protection is in place with minimal code.  
**Cons:** Currently only login protection; full RBAC and ownership checks are still to be implemented for finer control.

---


---

### ADR 13 : Seed Data via Custom Django Management Command

**Status:** Accepted

**Context**  
The application needs realistic demo data for development, testing, and the viva demonstration. Manually entering data through the admin panel after every database reset is time-consuming and error-prone.

**Alternatives considered**  
- **Manual admin entry**: No extra code but slow and not repeatable.  
- **Django fixtures (JSON/YAML)**: Built-in but brittle when models change and lacks logic.  
- **Custom management command**: Version-controlled, idempotent, and extensible.

**Decision**  
We created a custom management command `seed_data` that uses `get_or_create` to safely populate the database. It can be run multiple times without creating duplicates.

**Code reference**  
- `proj_1/housing/management/commands/seed_data.py` — Complete command

**Consequences**  
**Pros:** Repeatable, safe, excellent for demos, clearly documents sample data.  
**Cons:** Must be manually kept in sync with model changes.

---

**Superseded Decisions**

**Superseded: Function-based views → Class-based views**  
**Status:** Superseded by ADR 3  

We initially prototyped with function-based views for quick iteration. As the project grew, we migrated to class-based generic views to reduce duplication and better follow Django conventions (see ADR 3).

---
