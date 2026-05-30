# NT Housing Maintenance System - Entity Relationship Diagram

## ERD Class Diagram by Mermaid tool

```mermaid
erDiagram
    USER ||--|| TENANT : "1:1"
    COMMUNITY ||--o{ DWELLING : "1:N"
    DWELLING ||--o{ TENANT : "1:N"
    DWELLING ||--o{ REPAIR_REQUEST : "1:N"
    TENANT ||--o{ REPAIR_REQUEST : "1:N"
    CATEGORY ||--o{ REPAIR_REQUEST : "1:N"
    USER ||--o{ REPAIR_REQUEST : "1:N"
    REPAIR_REQUEST ||--o{ MAINTENANCE_UPDATE : "1:N"

    USER {
        int id PK
        string username
        string email
        string password
    }

    COMMUNITY {
        int id PK
        string name
        string region
    }

    DWELLING {
        int id PK
        int community_id FK
        string address
        string dwelling_code
        string dwelling_type
    }

    TENANT {
        int id PK
        int user_id FK "1:1"
        int dwelling_id FK
    }

    CATEGORY {
        int id PK
        string name
    }

    REPAIR_REQUEST {
        int id PK
        int dwelling_id FK
        int tenant_id FK
        int category_id FK
        int created_by_id FK "User (nullable)"
        string title
        string description
        string status
        datetime created_at
        datetime updated_at
    }

    MAINTENANCE_UPDATE {
        int id PK
        int repair_request_id FK
        string note
        datetime updated_at
    }
```

## Relationships Summary

| From | To | Type | Description |
|------|-----|------|-------------|
| USER | TENANT | 1:1 | Each user is associated with one tenant profile |
| COMMUNITY | DWELLING | 1:N | A community has many dwellings |
| DWELLING | TENANT | 1:N | A dwelling can have multiple tenants |
| DWELLING | REPAIR_REQUEST | 1:N | A dwelling can have many repair requests |
| TENANT | REPAIR_REQUEST | 1:N | A tenant can submit many repair requests |
| CATEGORY | REPAIR_REQUEST | 1:N | A category can have many repair requests |
| USER | REPAIR_REQUEST | 1:N | A user can create many repair requests (nullable) |
| REPAIR_REQUEST | MAINTENANCE_UPDATE | 1:N | A repair request can have many updates |

## Model Descriptions

### USER
Django built-in User model for authentication.

### COMMUNITY
Represents a remote housing community.

### DWELLING
A residential unit within a community (house, unit, town house, granny flat, room ).

### TENANT
Links a User to a Dwelling (one tenant per user).

### CATEGORY
Categories for repair requests (Electrical, Plumbing, Fittings, Windows and door, Locksmith, Roofing, Walls and Ceilings).

### REPAIR_REQUEST
Main model for tracking repair requests with status tracking (pending, in_progress, completed).

### MAINTENANCE_UPDATE
Tracks updates and notes for each repair request.
