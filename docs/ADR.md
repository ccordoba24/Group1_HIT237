
# Architecture Decision Records (ADRs)

**Project:** Housing Repair Request Management System  
**Repository:** https://github.com/ccordoba24/Group1_HIT237/  
**Author:** Gaurab Gaihre   
**Last Updated:** May 2026

This living document records the key architectural and design decisions made throughout the development of the Django-based housing repair request application. Each entry explains the **context**, **alternatives considered**, the **chosen decision with rationale**, exact **code references**, and **consequences**.

The commit history of this file demonstrates how decisions evolved as the project progressed.

---

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
- `proj_1/housing/models.py:6–11` — Community model  
- `proj_1/housing/models.py:14–23` — Dwelling model  
- `proj_1/housing/models.py:26–31` — Tenant model  
- `proj_1/housing/models.py:34–38` — Category model  
- `proj_1/housing/models.py:64–107` — RepairRequest model (including `created_by`)  
- `proj_1/housing/models.py:110–121` — MaintenanceUpdate model

**Consequences**  
**Pros:** Clean domain separation, readable ORM queries, strong data integrity.  
**Cons:** Requires more joins for complex queries — mitigated using `select_related()` and `prefetch_related()` (see ADR 9).

---

### ADR 2 : Use Django ModelForm for Repair Request Input

**Status:** Accepted

**Context**  
Forms for creating and updating repair requests needed to stay in sync with model validation rules without duplicating code. Staff and tenants require different editable fields (e.g. staff can change `status`).

**Alternatives considered**  
- **Manual `forms.Form`**: Full control but requires re-declaring every field, increasing risk of missing validation rules.  
- **Third-party form libraries**: Added unnecessary dependency and learning curve for standard CRUD forms.

**Decision**  
We used Django’s **`ModelForm`** with role-specific variants: `RepairRequestCreateForm`, `RepairRequestUserUpdateForm`, and `RepairRequestStaffUpdateForm`. `RepairRequestUpdateView` selects the form class based on `PermissionService.is_staff_or_superuser()`.

**Code reference**  
- `proj_1/housing/forms.py:8–42` — Repair request ModelForms  
- `proj_1/housing/forms.py:45–50` — MaintenanceUpdateForm  
- `proj_1/housing/views.py:161–165` — Dynamic form class selection

**Consequences**  
**Pros:** Less boilerplate, consistent validation, works seamlessly with `CreateView` and `UpdateView`.  
**Cons:** Reduced flexibility for highly custom input flows (handled via service-layer validation where needed).

---

### ADR 3 : Class-Based Views with QuerySet Optimisation

**Status:** Accepted

**Context**  
List and detail views needed to load related data (category, dwelling, tenant, user, updates) efficiently without causing N+1 query problems.

**Alternatives considered**  
- **Function-based views with manual querysets**: Clear but repetitive and easy to forget eager loading.  
- **Django REST Framework + SPA**: Modern but far beyond the scope of this assignment.

**Decision**  
We adopted Django’s **generic class-based views** (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `TemplateView`) and overrode `get_queryset()` to include `select_related()`, `prefetch_related()`, and custom QuerySet methods.

**Code reference**  
- `proj_1/housing/views.py:93–110` — List view with eager loading and `with_update_count()`  
- `proj_1/housing/views.py:115–130` — Detail view queryset  
- `proj_1/housing/views.py:29–217` — All view class definitions

**Consequences**  
**Pros:** Much less code, consistent patterns across CRUD operations, good performance by default.  
**Cons:** CBVs can obscure control flow — understanding lifecycle methods (`get_queryset`, `form_valid`, `dispatch`, etc.) is important.

---

### ADR 4 : Server-Side Rendering with Django Templates

**Status:** Accepted

**Context**  
We needed a simple, reliable UI that could be quickly built and easily demonstrated during the viva without a complex frontend setup.

**Alternatives considered**  
- **JSON API + Single Page Application**: Better user experience but required serializers, CORS, and a separate frontend framework.  
- **Hybrid SSR + JS enhancement**: Added complexity with little benefit for this project’s scope.

**Decision**  
We used **Django templates** for all primary views. The UI is fully server-rendered with no additional frontend build tools required. Static informational pages (FAQ, About) live in the `housing.extras` app but share templates under `housing/templates/housing/`.

**Code reference**  
- `proj_1/housing/templates/housing/repair_request_list.html` — List template  
- `proj_1/housing/views.py:29–30` — `HomeView`  
- `proj_1/housing/extras/views.py:4–9` — `FAQView`, `AboutView`  
- All templates extend `housing/base.html` (see ADR 26)

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
We implemented a **clean, resource-centred URL structure** under the `/requests/` namespace for repair request operations, with separate routes for auth, dashboard, and history.

**Code reference**  
- `proj_1/housing/urls.py` — Core urlpatterns including:
  - `/` — HomeView  
  - `/login/`, `/logout/`, `/register/` — Authentication  
  - `/dashboard/` — DashboardView  
  - `/requests/` — list, create, detail, edit  
  - `/requests/<pk>/update/` — maintenance update create  
  - `/history/` — MaintenanceHistoryView  
- `proj_1/housing/extras/urls.py` — `/faq/`, `/about/`  
- `proj_1/proj_1/urls.py` — Includes both `housing.urls` and `housing.extras.urls`

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
- **DRY (Don’t Repeat Yourself)** — Validation logic lives in `ModelForm`, custom QuerySets, and the service layer.  
- **Fat Models, Thin Views** — Domain helpers (e.g. `is_open()`, `open_requests_count()`) reside in models; complex coordination moved to services (ADR 16).  
- **Convention over Configuration** — Standard Django app and template structure is used so the framework auto-discovers files.

**Code reference**  
- DRY & Fat Models: `proj_1/housing/models.py:22–23`, `proj_1/housing/models.py:100–107`, `proj_1/housing/forms.py:8–42`  
- Service layer (complements thin views): `proj_1/housing/services.py`  
- Convention over Configuration: `proj_1/proj_1/settings.py`, `proj_1/housing/templates/housing/`

**Consequences**  
**Pros:** Cleaner, more maintainable code that clearly meets assessment requirements.  
**Cons:** Model-heavy logic plus a service layer means tests require more setup, but this is a worthwhile trade-off.

---

### ADR 7 : Django Design Patterns Used

**Status:** Accepted

**Context**  
We needed to clearly explain which design patterns were used and why they were appropriate for this project.

**Alternatives considered**  
- Service layer or Repository pattern: More explicit separation; we adopted a lightweight service layer (ADR 16) without full repository abstraction.

**Decision**  
We used idiomatic Django patterns plus project-specific extensions:  
- Generic class-based views for CRUD operations  
- ModelForm pattern for DRY form handling  
- QuerySet optimisation with `select_related()` and `prefetch_related()`  
- Custom QuerySet manager for reusable filters (ADR 18)  
- Related-name reverse relations for clean model navigation  
- Service layer for permissions and business operations (ADR 16, ADR 20)

**Code reference**  
- Generic CBVs: `proj_1/housing/views.py:29–217`  
- ModelForms: `proj_1/housing/forms.py:8–50`  
- QuerySet optimisation: `proj_1/housing/views.py:99–110`, `proj_1/housing/views.py:121–130`  
- Reverse relations: `proj_1/housing/models.py:77–83`, `proj_1/housing/models.py:111–115`

**Consequences**  
**Pros:** Patterns are familiar to Django developers and easy to explain in the viva.  
**Cons:** Some abstraction (especially in CBVs and services) requires understanding of Django’s internal lifecycle.

---

### ADR 8 : Explicit Relationship Modelling

**Status:** Accepted

**Context**  
The domain contains natural relationships between tenants, dwellings, communities, and repair requests that must be properly modelled for querying and data integrity.

**Alternatives considered**  
- Storing raw integer foreign keys with manual joins: Error-prone and loses ORM benefits.  
- Using JSON fields for nested data: Flexible but poor for querying and migrations.

**Decision**  
We used `ForeignKey` and `OneToOneField` with `related_name` arguments throughout the models to create clear, enforceable relationships. `RepairRequest.created_by` links each request to the submitting user.

**Code reference**  
- `proj_1/housing/models.py:15` — Dwelling → Community  
- `proj_1/housing/models.py:27` — Tenant → User  
- `proj_1/housing/models.py:73–83` — RepairRequest relationships (dwelling, tenant, category, created_by)  
- `proj_1/housing/models.py:111–115` — MaintenanceUpdate → RepairRequest (`related_name="updates"`)

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
We used the QuerySet API idiomatically with `select_related()` for ForeignKey/OneToOne fields, `prefetch_related()` for reverse many relations (`updates`), `order_by()`, and encapsulated filtering logic in custom QuerySet methods (ADR 18).

**Code reference**  
- `proj_1/housing/views.py:99–110` — `select_related()`, `prefetch_related("updates")`, `with_update_count()`  
- `proj_1/housing/views.py:121–130` — Detail view eager loading  
- `proj_1/housing/models.py:22–23` — Model method using `exclude()`  
- `proj_1/housing/models.py:41–61` — Custom QuerySet methods

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
We used Django’s generic class-based views (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `TemplateView`) and customised them only where necessary by overriding specific methods.

**Code reference**  
- `proj_1/housing/views.py:29–217` — All view classes including auth, dashboard, CRUD, and maintenance updates

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
- `proj_1/housing/models.py:26–31` — Tenant model linking to User

**Consequences**  
**Pros:** Quick to implement, well understood, low maintenance for current scope.  
**Cons:** Future migration to custom user model would require careful handling.

---

### ADR 12 : Permission Handling with LoginRequiredMixin and Access Control

**Status:** Accepted

**Context**  
Different user roles (tenants vs staff) require different levels of access to repair requests. Views must not expose other users’ data.

**Alternatives considered**  
- **Login only**: Insufficient — authenticated tenants could still access others’ requests.  
- **Django built-in permissions only**: Too rigid for object-level ownership without extra packages.  
- **Hardcoded checks in every view**: Repetitive and error-prone.

**Decision**  
We implemented layered access control:  
- `LoginRequiredMixin` on all protected views  
- `RepairRequestAccessMixin` filters querysets so tenants see only their own requests (by `created_by` or linked `tenant__user`); staff see all  
- `PermissionService` centralises rules for updates and maintenance updates (see ADR 20)  
- `MaintenanceUpdateCreateView.dispatch()` blocks non-staff from adding updates

**Code reference**  
- `proj_1/housing/views.py:55–64` — `RepairRequestAccessMixin`  
- `proj_1/housing/views.py:68–217` — Protected views using `LoginRequiredMixin`  
- `proj_1/housing/views.py:200–206` — Staff-only maintenance update check  
- `proj_1/housing/services.py:7–36` — `PermissionService`

**Consequences**  
**Pros:** Login protection plus object-level filtering; staff/tenant form differences enforced in views and services.  
**Cons:** `RepairRequestAccessMixin` must be applied consistently on any new request-scoped views.

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

### ADR 14 : Maintenance History as a Separate Filtered View

**Status:** Accepted

**Context**  
Users need a way to view completed repair requests separately from the active request list. Mixing completed and open requests in one view makes it harder to track ongoing issues vs resolved ones.

**Alternatives considered**  
1. Add a filter parameter to the existing `RepairRequestListView` (e.g. `?status=completed`)  
   - Pros: reuses existing view, fewer URL routes  
   - Cons: adds conditional logic to the view, complicates the template  
2. Dedicated `MaintenanceHistoryView` as a separate `ListView`  
   - Pros: single responsibility, clean URL (`/history/`), tailored template  
   - Cons: slight code duplication (another ListView class)  
3. Handle in the admin panel only  
   - Pros: no extra code  
   - Cons: regular users/tenants cannot access the admin panel

**Decision**  
We created a separate `MaintenanceHistoryView` that uses the custom QuerySet `.completed()` method and orders by `-updated_at`. It reuses `RepairRequestAccessMixin` so tenants only see their own completed requests.

**Code reference**  
- `proj_1/housing/views.py:177–189` — `MaintenanceHistoryView`  
- `proj_1/housing/urls.py:68–72` — `path("history/", ...)`  
- `proj_1/housing/templates/housing/maintenance_history.html`

**Consequences**  
**Pros:** Clear separation between active and resolved requests; clean dedicated URL; easy to extend (e.g. date range filters).  
**Cons:** If filtering logic changes, both this view and `RepairRequestListView` may need updating separately.

---

### ADR 15 : AI-Assisted Development

**Status:** Accepted

**Context**  
To accelerate the development lifecycle of the Django application, we used AI tools for boilerplate generation, ORM query construction, debugging, and documentation within the development environment.

**Alternatives considered**  
- **Manual coding only**: Ensured fully human-reviewed logic but significantly slowed repetitive patterns.

**Decision**  
We integrated **Claude** and **ChatGPT** into our workflow for code generation, refactoring, architectural brainstorming, and error explanation. All AI-generated code was manually reviewed before commit.

**Code reference**  
- `proj_1/housing/views.py` — Complex `get_queryset` and mixin patterns refined with AI assistance  
- `proj_1/housing/management/commands/seed_data.py` — Initial management command boilerplate  
- `proj_1/housing/static/housing/css/main.css` — Shared stylesheet structure and layout

**Consequences**  
**Pros:** Significant reduction in development time; faster resolution of syntax and framework errors.  
**Cons:** Requires rigorous manual review to ensure code adheres to DRY principles and project-specific security requirements.

---

### ADR 16 : Transition to a Dedicated Service Layer for Business Logic

**Status:** Accepted

**Context**  
While the "Fat Models, Thin Views" approach (ADR 6) worked for simple logic, the system's growth required more complex coordination between permissions, transactional data updates, and validation. Keeping this logic only in models made them bloated; putting it in views made them difficult to test.

**Alternatives considered**  
- **Expanding model methods**: Risked creating "God Models" that are hard to maintain.  
- **Logic in ModelForms**: Limits the reuse of business logic to only when a form is present.

**Decision**  
We introduced a **Service Layer (`services.py`)** to encapsulate business operations and permission checks. Views delegate create/update flows to `RepairRequestService` and authorization to `PermissionService`.

**Code reference**  
- `proj_1/housing/services.py` — `PermissionService` and `RepairRequestService`  
- `proj_1/housing/views.py:142–147`, `167–172` — Views delegating to the service layer  
- `proj_1/housing/exceptions.py` — Domain exceptions raised by services

**Consequences**  
**Pros:** Clearer separation of concerns; business logic can be unit-tested without HTTP mocks; centralized permission management.  
**Cons:** Additional indirection; service classes must be kept minimal and focused.

---

### ADR 17 : Create Dedicated `extras` App for Static Information Pages

**Status:** Accepted

**Context**  
FAQ and About pages were initially part of the housing app but logically represent static information separate from core repair functionality. That violated single responsibility, so they were moved.

**Decision**  
We created a `housing.extras` sub-app containing `FAQView` and `AboutView`. Templates remain under `housing/templates/housing/` for consistency. The home page links to FAQ and About via navigation cards.

**Code reference**  
- `proj_1/housing/extras/views.py` — FAQ and About views  
- `proj_1/housing/extras/urls.py` — Routing for `/faq/` and `/about/`  
- `proj_1/proj_1/settings.py` — `housing.extras` in `INSTALLED_APPS`  
- `proj_1/housing/templates/housing/faq.html`, `about.html`, `home.html`

**Consequences**  
**Pros:** Better separation of concerns; easier to maintain content-rich pages; reusable structure for future static pages.  
**Cons:** Slight extra folder nesting and URL include configuration.

---

### ADR 18 : Encapsulation of Query Logic via Custom QuerySets

**Status:** Accepted

**Context**  
As the application grew, several views and services needed to perform the same data operations, such as counting maintenance updates or filtering for completed requests. Writing these `.filter()` and `.annotate()` calls directly in views was repetitive (violating DRY) and made views harder to read.

**Alternatives considered**  
- **Manual filtering in views**: Leads to code duplication and makes it harder to change business rules later.  
- **Python-level filtering**: Is significantly slower than performing these operations at the database level.

**Decision**  
We implemented a custom `RepairRequestQuerySet` with methods such as `.open()`, `.completed()`, `.pending()`, `.in_progress()`, and `.with_update_count()`, exposed via `RepairRequest.objects`.

**Code reference**  
- `proj_1/housing/models.py:41–71` — `RepairRequestQuerySet` and manager  
- `proj_1/housing/views.py:78–79`, `99–110`, `183–189` — Views using custom QuerySet methods

**Consequences**  
**Pros:** Cleaner view logic; reusable query components; business rules for open/completed requests are centralized.  
**Cons:** Requires familiarity with Django’s custom QuerySet and Manager API.

---

### ADR 19 : Centralized Domain Exception Strategy

**Status:** Accepted

**Context**  
As application logic moved into the service layer (ADR 16), we needed a clear way to communicate business-level failures (invalid data, unauthorized actions) back to callers without relying on generic Python errors.

**Alternatives considered**  
- **Returning boolean values**: Tells you if a task failed, but not why.  
- **Raising generic exceptions (`ValueError`)**: Harder to catch specifically.  
- **Handling all errors in views**: Leads to repetitive try/except blocks.

**Decision**  
We implemented a dedicated exception hierarchy in `exceptions.py`. Domain exceptions (`InvalidRepairRequestError`, `UnauthorizedRepairActionError`) are raised by the service layer and can be caught specifically by views or tests.

**Code reference**  
- `proj_1/housing/exceptions.py` — Custom error definitions  
- `proj_1/housing/services.py:44–46`, `52–54`, `64–66`, `74–76`, `78–80` — Services raising domain errors

**Consequences**  
**Pros:** Explicit, self-documenting code; decouples business errors from framework errors.  
**Cons:** Requires defining new exception classes for additional failure types.

---

### ADR 20 : Centralized Permission Handling Service

**Status:** Accepted

**Context**  
Different parts of the application require specific security rules (e.g. only staff can add maintenance updates; tenants can edit their own requests). Scattering these checks across views led to duplication and audit difficulty.

**Alternatives considered**  
- **Hardcoding logic in views**: Difficult to ensure consistency.  
- **Logic in models**: Mixes security with data storage.  
- **Django built-in permissions only**: Too rigid for object-level ownership.

**Decision**  
We implemented `PermissionService` with static methods such as `is_staff_or_superuser`, `can_update_repair_request`, and `can_add_maintenance_update`, used by views, services, and tests.

**Code reference**  
- `proj_1/housing/services.py:7–36` — `PermissionService`  
- `proj_1/housing/views.py:57`, `162`, `201` — Views using permission checks  
- `proj_1/housing/services.py:70–76` — Service-layer authorization on update

**Consequences**  
**Pros:** Single source of truth for security rules; easier to audit; simplifies view logic.  
**Cons:** Requires calling the service whenever a new secure action is implemented.

---

### ADR 21 : Centralized Management Dashboard for Operational Overview

**Status:** Accepted

**Context**  
Tenants and staff needed a high-level summary of request status (totals, open vs completed, breakdown by status) without scanning long list views or using the Django admin.

**Alternatives considered**  
- **Summary cards in list views**: Cluttered the interface.  
- **Admin-only metrics**: Not accessible to regular tenants.

**Decision**  
We implemented `DashboardView` as the post-login landing page. It uses `RepairRequestAccessMixin` and custom QuerySet methods to show scoped metrics and status aggregation.

**Code reference**  
- `proj_1/housing/views.py:68–88` — Dashboard context aggregation  
- `proj_1/housing/templates/housing/dashboard.html` — Dashboard UI  
- `proj_1/housing/urls.py:32–36` — `/dashboard/` route

**Consequences**  
**Pros:** Improved at-a-glance visibility; better user engagement; foundation for future reports.  
**Cons:** Must stay in sync with model and permission changes.

---

### ADR 22 : Enhanced Admin Interface for Efficient Data Stewardship

**Status:** Accepted

**Context**  
Staff and administrators needed a granular tool for managing data relationships. The default Django admin was difficult to use for searching through records or finding tenant-to-dwelling connections.

**Alternatives considered**  
- **Custom staff portal**: Significantly more development time.  
- **Default Django admin unconfigured**: Poor usability.

**Decision**  
We customized the Django Admin via `admin.py` with `list_display`, `list_filter`, and `search_fields` across core models.

**Code reference**  
- `proj_1/housing/admin.py:1–102` — Admin configurations for all housing models

**Consequences**  
**Pros:** Improved administrative efficiency; fast search and filter.  
**Cons:** Model schema changes require corresponding admin updates.

---

### ADR 23 : Expanded Automated Test Suite Covering All Architecture Layers

**Status:** Accepted

**Context**  
As the codebase grew with a service layer (ADR 16), custom QuerySets (ADR 18), and permission service (ADR 20), it became critical to verify each layer independently.

**Alternatives considered**  
- **Manual testing only**: Unreliable and does not scale.  
- **End-to-end browser testing**: Slower and requires additional tools.

**Decision**  
We expanded the Django test suite into five focused test classes:  
- `RepairRequestModelTests` — Model behaviour  
- `RepairRequestQuerySetTests` — Custom QuerySet logic  
- `RepairRequestServiceTests` — Service layer including auth errors  
- `PermissionServiceTests` — Authorization rules  
- `RepairRequestViewPermissionTests` — HTTP-level access control

**Code reference**  
- `proj_1/housing/tests.py:11–502` — Complete test suite

**Consequences**  
**Pros:** High confidence per layer; security rules verified automatically.  
**Cons:** Tests must be maintained when models or services change.

---

### ADR 24 : Custom Authentication Flow with Auto-Login on Registration

**Status:** Accepted

**Context**  
The application needed a user-friendly login and registration experience for tenants, not the Django admin login page.

**Alternatives considered**  
- **Django admin login for all users**: Poor UX and exposes admin URL to non-staff.  
- **Third-party packages (django-allauth)**: Unnecessary complexity for current scope.

**Decision**  
We implemented `UserLoginView` (extending `LoginView`) and `RegisterView` (extending `CreateView`) with dedicated templates. Registration auto-logs in the user via `login()` and redirects to the dashboard. Logout uses `LogoutView` with `next_page="login"`.

**Code reference**  
- `proj_1/housing/views.py:35–50` — `RegisterView`, `UserLoginView`  
- `proj_1/housing/templates/housing/login.html`, `register.html`  
- `proj_1/housing/urls.py:20–30`, `74–78` — Login, logout, register routes

**Consequences**  
**Pros:** Seamless tenant UX; no admin exposure for regular users.  
**Cons:** Custom templates and views must be maintained alongside Django auth.

---

### ADR 25 : Custom User Registration Form via UserCreationForm Extension

**Status:** Accepted

**Context**  
Django's default `UserCreationForm` only includes username and password fields. The application needed to optionally collect an email address while reusing Django's secure password validation.

**Alternatives considered**  
- **Default `UserCreationForm`**: No email field.  
- **Manual `forms.Form`**: Error-prone and a security risk for passwords.

**Decision**  
We extended `UserCreationForm` to create `UserRegisterForm` with an optional `email` field.

**Code reference**  
- `proj_1/housing/forms.py:53–63` — `UserRegisterForm`  
- `proj_1/housing/views.py:35–43` — `RegisterView` using the custom form

**Consequences**  
**Pros:** Inherits Django password validation; minimal extra code.  
**Cons:** Future Django `UserCreationForm` API changes may require updates.

---

### ADR 26 : Shared Base Template for Consistent UI Layout

**Status:** Accepted

**Context**  
As templates grew (home, list, detail, dashboard, forms, FAQ, etc.), maintaining a consistent navigation bar and page structure in every file was repetitive and error-prone.

**Alternatives considered**  
- **Copying HTML across templates**: Violates DRY.  
- **JavaScript-rendered navigation**: Overkill for server-side rendering (ADR 4).

**Decision**  
We implemented `base.html` with shared header, navigation, footer, and `{% block content %}`. All application templates extend it via `{% extends "housing/base.html" %}` including repair and maintenance forms (previously standalone HTML pages).

**Code reference**  
- `proj_1/housing/templates/housing/base.html` — Shared layout and navigation  
- All templates under `proj_1/housing/templates/housing/` — Extend the base template

**Consequences**  
**Pros:** One change updates navigation site-wide; consistent branding.  
**Cons:** Structural base changes may require updating child template blocks.

---

### ADR 27 : Centralised Static CSS for Consistent Visual Design

**Status:** Accepted

**Context**  
After introducing `base.html` (ADR 26), styling was initially inline or duplicated per template (e.g. maintenance history). That produced an inconsistent look and made global design changes difficult.

**Alternatives considered**  
- **Inline styles per template**: Fast initially but inconsistent and hard to maintain.  
- **Third-party CSS frameworks (Bootstrap, Tailwind)**: Extra dependency and build steps beyond project scope.  
- **Copy-pasted `<style>` blocks**: Duplicated rules across pages.

**Decision**  
We added a single stylesheet at `housing/static/housing/css/main.css` loaded from `base.html` via `{% load static %}`. Shared CSS classes cover layout (`.container`, `.page-card`), forms (`.form-card`), buttons (`.btn`), tables (`.data-table`), lists (`.request-list`), dashboard stats (`.stats-grid`), and status badges (`.badge`).

**Code reference**  
- `proj_1/housing/static/housing/css/main.css` — Shared design system  
- `proj_1/housing/templates/housing/base.html:1–9` — Static file inclusion  
- `proj_1/proj_1/settings.py` — `STATIC_URL` and `django.contrib.staticfiles`

**Consequences**  
**Pros:** Consistent UI across all pages; one place to update colours, spacing and components; no build toolchain required.  
**Cons:** Custom CSS must be maintained manually; no component library out of the box.

---

### ADR 28 : Refinement of Domain Models and Dynamic Input Handling

**Status:** Accepted (Refines ADR 1 and ADR 2)

**Context**  
As we moved from prototyping to a production-ready system, the generic data models and forms (ADR 1, ADR 2) became insufficient. Specifically, we needed better asset classification for dwellings and stricter field-level security for repair requests based on user roles (staff vs. tenant).

**Alternatives considered**  
- **Continue with generic forms**: Simpler code but allowed tenants to potentially edit their own status or internal staff notes.  
- **Overwriting initial ADRs**: Faster documentation but loses the history of the project’s evolution and the rationale behind later improvements.

**Decision**  
We implemented **Granular Domain Modelling** by adding a `dwelling_type` categorization to the `Dwelling` model. Simultaneously, we replaced the single `RepairRequestForm` with a **Three-Tier Form Architecture** (`Create`, `UserUpdate`, `StaffUpdate`). This ensures that only staff can access the "Status" and "Management" fields, while tenants are restricted to basic request details.

**Code reference**  
- `proj_1/housing/models.py:15–33` — Dwelling Type categorization refinement.  
- `proj_1/housing/forms.py:8–42` — Three-tier form implementation.  
- `proj_1/housing/views.py:161–165` — View-level logic for role-based form selection.

**Consequences**  
- **Pros:** Improved data classification; better security at the UI layer; demonstrates clear architectural progression.  
- **Cons:** Requires maintaining three form variants instead of one; slightly more logic in the view controllers.

---

This ADR document reflects genuine consideration of Django’s design philosophies and trade-offs. Decisions were revisited and refined as the project evolved from basic CRUD through services, permissions, testing, authentication and UI consistency.

