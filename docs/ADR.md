
# Architecture Decision Records (ADRs)

**Project:** Housing Repair Request Management System  
**Repository:** https://github.com/ccordoba24/Group1_HIT237/  
**Last Updated:** April 2026

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

## ADR 14 — Maintenance history as a separate filtered view

**Status: Accepted**

**Context** 
Users need a way to view completed repair requests separately 
from the active request list. Mixing completed and open requests 
in one view makes it harder to track ongoing issues vs resolved ones.

**Alternatives considered** 
1. Add a filter parameter to the existing RepairRequestListView 
   (e.g., ?status=completed)
   - Pros: reuses existing view, fewer URL routes
   - Cons: adds conditional logic to the view, complicates the 
     template, harder to give the page its own layout and heading

2. Dedicated MaintenanceHistoryView as a separate ListView
   - Pros: single responsibility, clean URL (/history/), 
     template can be tailored specifically for completed requests
   - Cons: slight code duplication (another ListView class)

3. Handle in the admin panel only
   - Pros: no extra code
   - Cons: regular users/tenants can't access the admin panel

**Decision**
We created a separate `MaintenanceHistoryView` that filters 
`RepairRequest` objects by `status="completed"` and orders 
by `-updated_at` so the most recently resolved requests appear 
first. This keeps the view focused and the URL meaningful.

**Code reference**
- `proj_1/housing/views.py` — `MaintenanceHistoryView` 
  (filters: `.filter(status="completed").order_by("-updated_at")`)
- `proj_1/housing/urls.py` — `path("history/", ...)`

**Consequences**
- Pros: clear separation between active and resolved requests, 
  clean dedicated URL, easy to extend (e.g. add date range filters)
- Cons: if filtering logic changes (e.g. adding an "archived" 
  status), both this view and RepairRequestListView may need 
  updating separately

This ADR document reflects genuine consideration of Django’s design philosophies and trade-offs. The commit history shows these decisions were revisited and refined throughout development.

## ADR 15 — AI-Assisted Development with Claude 2.5 Haiku and ChatGPT

**Status: Accepted**

**Context** 
To accelerate the development of the Django application, AI tools are used throughout the project

**Context**  
To accelerate the development lifecycle of the Django application, we required tools that could assist with boilerplate generation, complex ORM query construction, and debugging within the **MS Visual Studio Code** environment.

**Alternatives considered**  
- **Manual Coding Only**: Ensured 100% human-authored logic but significantly slows down the implementation of repetitive patterns

**Decision**  
We integrated **Claude 3.5 Haiku** and **ChatGPT** into our workflow via VS Code extensions and web interfaces. 
- **Claude 3.5 Haiku** was primarily used for rapid code generation and refactoring due to its high speed and concise output.
- **ChatGPT** was utilized for high-level architectural brainstorming and explaining complex Django error traces.
- **GitHub Copilot**: Integrated with VS Code was used for basic setup. 

**Code reference**  
- `proj_1/housing/views.py` — Logic for complex `get_queryset` overrides was refined using AI suggestions.
- `proj_1/housing/management/commands/seed_data.py` — Initial boilerplate for the management command was generated via AI.

**Consequences**  
**Pros:** Significant reduction in development time, improved code documentation through AI-generated comments, and faster resolution of syntax errors.  
**Cons:** Requires rigorous manual review to ensure the AI-generated code adheres to DRY principles and project-specific security requirements; potential for "hallucinations" in less common Django library versions.



---

### ADR 16 : Transition to a Dedicated Service Layer for Business Logic

**Status:** Accepted

**Context**  
While the "Fat Models, Thin Views" approach (ADR 6) worked for simple logic, the system's growth required more complex coordination between permissions, transactional data updates, and validation. Keeping this logic in models made them bloated, and putting it in views made them difficult to test.

**Alternatives considered**  
- **Expanding Model Methods**: Risked creating "God Models" that are hard to maintain.  
- **Logic in ModelForms**: Limits the reuse of business logic to only when a form is present.

**Decision**  
We introduced a **Service Layer (`services.py`)** to encapsulate business operations and permission checks. Views now act as simple coordinators that delegate tasks to `RepairRequestService` or `PermissionService`.

**Code reference**  
- `proj_1/housing/services.py` — Implementation of service classes.
- `proj_1/housing/views.py:86, 111` — Views delegating logic to the service layer.

**Consequences**  
- **Pros:** Clearer separation of concerns; business logic can be unit-tested without HTTP request mocks; centralized permission management.  
- **Cons:** Introduces a new layer of abstraction and an additional file to manage in the app.


---

### ADR 17 : Encapsulation of Query Logic via Custom QuerySets

**Status:** Accepted

**Context**  
As the application grew, several views and services needed to perform the same data operations, such as counting maintenance updates or filtering for completed requests. Writing these `.filter()` and `.annotate()` calls directly in the views was repetitive (violating DRY) and made the views harder to read.

**Alternatives considered**  
- **Manual Filtering in Views**: Leads to code duplication and makes it harder to change business rules later.
- **Python-level Filtering**: Is significantly slower than performing these operations at the database level.

**Decision**  
We implemented a custom `RepairRequestQuerySet` to encapsulate common domain-specific queries. This allows us to use descriptive methods like `.completed()` or `.with_update_count()` directly in our code.

**Code reference**  
- `proj_1/housing/models.py:41–63` — Implementation of `RepairRequestQuerySet`.
- `proj_1/housing/views.py:43–54, 120–131` — Views using the custom QuerySet methods.

**Consequences**  
- **Pros:** Much cleaner and more readable view logic; reusable query components; business rules for "open" or "completed" requests are centralized in the model layer.
- **Cons:** Requires team familiarity with Django’s custom QuerySet and Manager API.


---

### ADR 18 : Centralized Domain Exception Strategy

**Status:** Accepted

**Context**  
As the application logic moved into the Service Layer (ADR 16), we needed a clear way to communicate specific business-level failures (like "this user isn't allowed to do this" or "this request is missing a title") back to the user interface. Relying on generic Python errors or standard Django error pages made it difficult to provide specific feedback.

**Alternatives considered**  
- **Returning Boolean values**: Tells you if a task failed, but not *why* it failed.
- **Raising Generic Exceptions (ValueError)**: Harder to catch specifically when multiple things could go wrong.
- **Handling all errors in Views**: Leads to repetitive try/except blocks and mixes business rules with web logic.

**Decision**  
We implemented a dedicated exception hierarchy in `exceptions.py`. These "Domain Exceptions" (like `InvalidRepairRequestError`) are raised by the service layer and can be caught specifically by the views to show helpful messages to the user.

**Code reference**  
- `proj_1/housing/exceptions.py` — The custom error definitions.
- `proj_1/housing/services.py:32, 40, 62` — Services raising specific domain errors.

**Consequences**  
- **Pros:** Explicit and self-documenting code; cleaner error handling in the views; decouple business logic errors from framework-specific errors.
- **Cons:** Requires defining new exception classes for different error types, adding a small amount of extra code.


---

### ADR 19 : Centralized Permission Handling Service

**Status:** Accepted

**Context**  
Different parts of the application require specific security rules (e.g., only staff can add maintenance updates, but tenants can edit their own requests). Initially, these checks were planned to be handled by Django Mixins in the views (ADR 12), but as the rules became more complex, this led to repetitive code that was hard to audit and maintain.

**Alternatives considered**  
- **Hardcoding logic in Views**: Makes it difficult to ensure security is consistent and leads to duplication of ownership checks.
- **Logic in Models**: Mixes security rules with data storage logic, making the models harder to maintain and test.
- **Django Built-in Permissions**: Too rigid for object-level ownership checks without adding complex third-party packages.

**Decision**  
We implemented a dedicated `PermissionService` within the service layer. This service contains static methods like `can_update_repair_request` and `can_add_maintenance_update`, which consolidate all authorization rules into a single source of truth.

**Code reference**  
- `proj_1/housing/services.py:7–25` — Implementation of `PermissionService`.
- `proj_1/housing/views.py:103, 143` — Views now call the permission service to verify access.

**Consequences**  
- **Pros:** A single source of truth for all security rules; easier to audit for security vulnerabilities; significantly simplifies view logic.
- **Cons:** Requires a deliberate call to the service whenever a new secure action is implemented.


---

### ADR 20 : Centralized Management Dashboard for Operational Overview

**Status:** Accepted

**Context**  
As the volume of repair requests grew, tenants and staff needed a high-level summary of the system's status (e.g., total requests, open issues vs. completed ones) at a glance. Initially, users had to scan through long list views or use the Django admin panel, which provided a poor user experience for non-technical tenants.

**Alternatives considered**  
- **Summary Cards in List Views**: Adding metrics to the top of the existing list view, but this cluttered the interface and slowed down page loads.
- **Requiring Admin Access for Metrics**: Not feasible for regular tenants who do not have access to the Django backend.

**Decision**  
We implemented a dedicated `DashboardView` as the primary landing page after login. The dashboard uses the custom `RepairRequestQuerySet` (ADR 17) to efficiently fetch real-time metrics and the `PermissionService` (ADR 19) to ensure that tenants only see data relevant to their own requests while staff see a global overview.

**Code reference**  
- `proj_1/housing/views.py:61–86` — Logic for aggregating dashboard metrics.
- `proj_1/housing/templates/housing/dashboard.html` — The new dashboard user interface.

**Consequences**  
- **Pros:** Significantly improved "at-a-glance" visibility for maintenance status; better user engagement; provides a scalable foundation for future reports or charts.
- **Cons:** Adds a new view and template that must be kept in sync with any changes to the underlying model relationships.


---

### ADR 21 : Enhanced Admin Interface for Efficient Data Stewardship

**Status:** Accepted

**Context**  
While the user-facing dashboard (ADR 20) provides a high-level overview, internal staff and housing administrators required a more granular tool for managing complex data relationships. The default Django admin was difficult to use for searching through hundreds of records or finding specific tenant-to-dwelling connections.

**Alternatives considered**  
- **Custom Staff Portal**: Building a completely separate frontend for staff management, which would have significantly increased development time and complexity.
- **Default Django Admin**: Leaving the admin panel unconfigured, which led to poor usability and inefficiency in finding specific repair requests.

**Decision**  
We heavily customized the Django Admin interface through a tailored `admin.py` configuration. By implementing `list_display`, `list_filter`, and `search_fields` across all core models, we converted the generic admin panel into a purpose-built back-office management system.

**Code reference**  
- `proj_1/housing/admin.py:14–102` — Custom admin configurations for Communities, Dwellings, Tenants, and Repair Requests.

**Consequences**  
- **Pros:** Dramatic improvement in administrative efficiency; staff can now search and filter data in seconds; reduces the risk of data entry errors.
- **Cons:** Any changes to the model schema now require corresponding updates in the admin classes to maintain the dashboard's effectiveness.



---

### ADR 22 : Expanded Automated Test Suite Covering All Architecture Layers

**Status:** Accepted

**Context**  
As the codebase grew with a Service Layer (ADR 16), Custom QuerySets (ADR 17), and a Permission Service (ADR 19), it became critical to verify that each layer works correctly and does not break when other parts change. The initial test file only covered basic model behaviour, leaving services and permissions untested.

**Alternatives considered**  
- **Manual Testing Only**: Quick in the short term but unreliable and does not scale with the number of features.
- **End-to-End Browser Testing**: Provides full user-journey coverage but requires additional tools and is slower to run.

**Decision**  
We expanded the Django test suite into four focused test classes, each targeting a specific architecture layer:
- `RepairRequestModelTests` — Model method correctness.
- `RepairRequestQuerySetTests` — Custom QuerySet filtering logic.
- `RepairRequestServiceTests` — Business logic in the service layer, including blocking anonymous users.
- `RepairRequestViewPermissionTests` — HTTP-level security, ensuring tenants cannot access other users' requests.

**Code reference**  
- `proj_1/housing/tests.py:11–364` — The complete test suite.

**Consequences**  
- **Pros:** High confidence in the correctness of each layer independently; security rules (ADR 19) are verified automatically; regressions are caught before deployment.
- **Cons:** Tests must be maintained when models or services change; slightly increases development time per feature.

---

### ADR 23 : Custom Authentication Flow with Auto-Login on Registration

**Status:** Accepted

**Context**  
The original application relied on the Django admin login page for user authentication, which was unsuitable for regular tenants who are not staff and should not access the admin panel. A user-friendly login and registration experience was needed for the public-facing application.

**Alternatives considered**  
- **Django Admin Login for All Users**: Simple to implement but exposes the admin interface URL to non-staff users and provides a poor user experience.
- **Third-party packages (django-allauth)**: Feature-rich but adds unnecessary complexity and dependencies for the current scope.

**Decision**  
We implemented a custom `UserLoginView` (extending Django's built-in `LoginView`) with a dedicated template and a `RegisterView` (extending `CreateView`) that automatically logs the user in upon successful registration using Django's `login()` function.

**Code reference**  
- `proj_1/housing/views.py:33–48` — `RegisterView` and `UserLoginView` implementations.
- `proj_1/housing/templates/housing/login.html` — Custom login template.
- `proj_1/housing/urls.py:21–25` — URL route for the login view.

**Consequences**  
- **Pros:** Seamless user experience; tenants are redirected to the dashboard immediately after registering; no exposure of the admin panel to regular users.
- **Cons:** Requires maintaining custom templates and views alongside Django's built-in auth system.



---

### ADR 24 : Custom User Registration Form via UserCreationForm Extension

**Status:** Accepted

**Context**  
Django's default `UserCreationForm` only includes username and password fields. The application needed to optionally collect an email address during registration while still leveraging Django's built-in password validation and user creation logic.

**Alternatives considered**  
- **Default `UserCreationForm`**: No email field — insufficient for future contact functionality.
- **Manual `forms.Form`**: Requires re-implementing password hashing and validation from scratch, which is error-prone and a security risk.

**Decision**  
We extended Django's `UserCreationForm` to create `UserRegisterForm`, adding an optional `email` field. This approach reuses all of Django's secure password handling while allowing the form to be customised.

**Code reference**  
- `proj_1/housing/forms.py:27–39` — `UserRegisterForm` definition.
- `proj_1/housing/views.py:33–41` — `RegisterView` using the custom form.

**Consequences**  
- **Pros:** Inherits all of Django's built-in password validation and security; minimal extra code; easily extensible with additional fields in the future.
- **Cons:** Any future changes to Django's `UserCreationForm` API may require corresponding updates to this subclass.

---

