# 🦇 Arkham Asylum Backend - Digital Forensic Psychiatric Hospital

A robust, Zero-Trust backend system designed for the secure management of Gotham's most dangerous criminals. Operating seamlessly across **25+ distinct API endpoints**, the registry serves as a digital fortress that bridges strict carceral containment with highly sensitive psychiatric care.

<br>

## Technology Stack & AI

**Core Infrastructure...**
*   **Backend Framework:** Python, Django REST Framework (DRF)
*   **Database:** MySQL Workbench 8.0
*   **Authentication:** Djoser, SimpleJWT (JSON Web Tokens)
*   **Architecture Mapping:** Mermaid.js

<br>

**LLM Collaborators...**
*   **AntiGravity (Google AI Pro):** Orchestrated core Backend logics, database structuring, and rigorous backend engine design.
*   **Perplexity Pro:** Utilized for high-level research and requirements extension in a logical, architectural way.
*   **OpenClaw (`openai-gpt5-chat-latest`):** Provided OS-level project control, contextual awareness, and overarching advisory guidance.

<br>

## Key Features

1.  **The Admission Engine:** A robust ingestion guardrail. Employs `transaction.atomic()` to guarantee that an `InmateProfile` and their highly classified `MedicalFile` are created simultaneously with zero ghost records. It natively evaluates live `CellBlock` capacity, outright rejecting an admission if the facility is full.

2.  **Transfer Safety Engine:** A proactive security protocol reading directly from the immutable audit stream. Guards cannot transfer an inmate to a new Cell Block unless a certified Doctor has reviewed their Medical File within 7 days, and a Super Admin within 24 hours.

3.  **Immutable Audit Logging & Zero-Trust:** Every CUD (Create, Update, Delete) operation is captured automatically via `signals.py`. Every READ operation is logged via a custom `@audit_read` decorator. Layered beneath StrictDjangoModelPermissions, Group-based clearances (RBAC) and scoped Throttling.

<br>

## Architecture Documentation

The repository contains three interactive `mermaid.js` diagrams detailing the exact flow and constraints of the system. Open these HTML files directly in any web browser to view the system visualization:

*   **`solution_architecture.html`**: High-level module interaction for Business Stakeholders.
*   **`technical_architecture.html`**: Low-level Django/DRF request lifecycles, middlewares, and throttles.
*   **`database_er_model.html`**: Exact Database Schema, relationships, and constraints.

<br>

## Quick Start & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/arkham-asylum-backend.git
cd arkham-asylum-backend
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup (MySQL 8.0)
Log into your local MySQL workbench and create the database:
```sql
CREATE DATABASE arkham_registry;
```
*Note: Update `arkham_pm/settings.py` with your MySQL credentials.*

### 5. Run Migrations & Start Server
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 8000
```

<br>

## API Endpoints Reference

Base URL: `http://127.0.0.1:8000`

<br>

### 0. Health Check

| # | Method | Endpoint | Authorization | Sample Payload | Description |
|---|--------|----------|---------------|----------------|-------------|
| 1 | `GET` | `/api/v1/root/` | Public | — | Returns a welcome message confirming the server is alive. |

<br>

### 1. Registration

| # | Method | Endpoint | Authorization | Sample Payload | Description |
|---|--------|----------|---------------|----------------|-------------|
| 2 | `POST` | `/api/auth/users/` | Public | <pre>{<br>  "username": "...",<br>  "password": "..."<br>}</pre> | Register a new user account. |

<br>

### 2. Authentication

| # | Method | Endpoint | Authorization | Sample Payload | Description |
|---|--------|----------|---------------|----------------|-------------|
| 3 | `POST` | `/api/auth/jwt/create/` | Registered User | <pre>{<br>  "username": "...",<br>  "password": "..."<br>}</pre> | Login — returns `access` (45 min) and `refresh` (4 days) tokens. |
| 4 | `POST` | `/api/auth/jwt/refresh/` | Registered User | <pre>{<br>  "refresh": "..."<br>}</pre> | Get a new access token. |
| 5 | `POST` | `/api/auth/jwt/verify/` | Registered User | <pre>{<br>  "token": "..."<br>}</pre> | Verify if a token is valid. |

<br>

### 3. Profile & Password Management

| # | Method | Endpoint | Authorization | Sample Payload | Description |
|---|--------|----------|---------------|----------------|-------------|
| 6 | `GET` | `/api/auth/users/me/` | Authenticated | <pre>{<br>  "token": "..."<br>}</pre> | View own profile. |
| 7 | `PATCH` | `/api/auth/users/me/` | Authenticated | <pre>{<br>  "email": "..."<br>}</pre> | Update own profile details. |
| 8 | `POST` | `/api/auth/users/set_password/` | Authenticated | <pre>{<br>  "current_password": "...",<br>  "new_password": "..."<br>}</pre> | Change own password. |

<br>

### 4. Inmate Management

> **Note:** `PUT` and `DELETE` are blocked. Use `PATCH {"status": "DISCHARGED"}` for soft deletes.

| # | Method | Endpoint | Authorization | Sample Payload | Description |
|---|--------|----------|---------------|----------------|-------------|
| 9 | `GET` | `/api/v1/default-router/inmates` | Any Staff | — | List all inmates. Supports `?cell_block=` filter. |
| 10 | `GET` | `/api/v1/default-router/inmates/{id}` | Any Staff | — | Retrieve single inmate. Authorized clinical/admin staff see nested Medical Record. |
| 11 | `POST` | `/api/v1/default-router/inmates` | Super Admin | <pre>{<br>  "name": "...",<br>  "alias": "...",<br>  "cell_block": "...",<br>  "referral_diagnosis": "..."<br>}</pre> | Admit an inmate. **Admission Engine** enforces Cell capacity and creates a linked MedicalFile atomically. |
| 12 | `PATCH` | `/api/v1/default-router/inmates/{id}` | Admin / Security | <pre>{<br>  "cell_block": "Block-C"<br>}</pre> | Transfer inmate. **Transfer Safety Engine** requires a Doctor to have reviewed the file within 7 days, and an Admin within 24hr. |

<br>

### 5. Medical Records

> **Note:** Enforces Clinical Ownership. Doctors can only read files assigned to them via `assigned_to` foreign key.

| # | Method | Endpoint | Authorization | Sample Payload | Description |
|---|--------|----------|---------------|----------------|-------------|
| 13 | `GET` | `/api/v1/default-router/medical-records` | Admin / Medical | — | List medical records. Throttled (20/min). |
| 14 | `GET` | `/api/v1/default-router/medical-records/{id}`| Admin / Medical | — | Retrieve single record. Triggers immutable `DETAILED_READ` audit log. |
| 15 | `POST`| `/api/v1/default-router/medical-records` | Admin / Medical | <pre>{<br>  "inmate": 4,<br>  "referral_diagnosis": "...",<br>  "assigned_to": 2<br>}</pre> | Explicitly create a file. |
| 16 | `PATCH`| `/api/v1/default-router/medical-records/{id}`| Admin / Medical | <pre>{<br>  "internal_diagnosis": "..."<br>}</pre> | Update in-house assessment or medication. |
| 17 | `DELETE`| `/api/v1/default-router/medical-records/{id}`| Super Admin | — | Hard delete a medical record. |

<br>

### 6. User Group Management

> **Note:** `POST` and `DELETE` are blocked. User creation is handled via Djoser.

| # | Method | Endpoint | Authorization | Sample Payload | Description |
|---|--------|----------|---------------|----------------|-------------|
| 18 | `GET` | `/api/v1/default-router/user-groups` | Super Admin | — | List all registered users and their groups. |
| 19 | `GET` | `/api/v1/default-router/user-groups/{id}` | Super Admin | — | View specific user details. |
| 20 | `PATCH` | `/api/v1/default-router/user-groups/{id}` | Super Admin | <pre>{<br>  "groups": [<br>    "Medical Staff"<br>  ]<br>}</pre> | Assign roles. Sending `[]` revokes all clearance. Sending `{"is_active": false}` soft-deletes the user. |

<br>

### 7. Cell Block Dashboard

| # | Method | Endpoint | Authorization | Sample Payload | Description |
|---|--------|----------|---------------|----------------|-------------|
| 21 | `GET` | `/api/v1/default-router/cell-blocks` | Super Admin | — | List all physical blocks with live `current_count` vs `max_capacity`. |
| 22 | `GET` | `/api/v1/default-router/cell-blocks/{id}` | Super Admin | — | Retrieve specific cell block details. |

<br>

### 8. Audit Logs

> **Note:** Immutable. All write methods are blocked via `http_method_names`.

| # | Method | Endpoint | Authorization | Sample Payload | Description |
|---|--------|----------|---------------|----------------|-------------|
| 23 | `GET` | `/api/v1/default-router/security-logs` | Super Admin | — | List all audit entries. Throttled (50/min). |
| 24 | `GET` | `/api/v1/default-router/security-logs/{id}` | Super Admin | — | Retrieve specific audit log entry. |
