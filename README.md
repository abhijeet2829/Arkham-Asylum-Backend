# 🦇 Arkham Asylum Backend - Digital Forensic Psychiatric Hospital

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.16-ff1709?logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A robust, Zero-Trust backend system designed for the secure management of Gotham's most dangerous criminals. Operating seamlessly across **25+ distinct API endpoints**, the registry serves as a digital fortress that bridges strict carceral containment with highly sensitive psychiatric care.

<br>

## Technology Stack & AI

**Core Infrastructure...**

* **Backend Framework:** Python, Django REST Framework (DRF)
* **Database:** MySQL Workbench 8.0
* **Authentication:** Djoser, SimpleJWT (JSON Web Tokens)
* **Architecture Mapping:** Mermaid.js

<br>

**LLM Collaborators...**

* **AntiGravity (Google AI Pro):** Orchestrated core Backend logics, database structuring, and rigorous backend engine design.
* **Perplexity Pro:** Utilized for high-level research and requirements extension in a logical, architectural way.
* **OpenClaw (`openai-gpt5-chat-latest`):** Provided OS-level project control, contextual awareness, and overarching advisory guidance.

<br>

## Key Features

1. **The Admission Engine:** A robust ingestion guardrail. Employs `transaction.atomic()` to guarantee that an `InmateProfile` and their highly classified `MedicalFile` are created simultaneously with zero ghost records. It natively evaluates live `CellBlock` capacity, outright rejecting an admission if the facility is full.

2. **Transfer Safety Engine:** A proactive security protocol reading directly from the immutable audit stream. Guards cannot transfer an inmate to a new Cell Block unless a certified Doctor has reviewed their Medical File within 7 days, and a Super Admin within 24 hours.

3. **Immutable Audit Logging & Zero-Trust:** Every CUD (Create, Update, Delete) operation is captured automatically via `signals.py`. Every READ operation is logged via a custom `@audit_read` decorator. Layered beneath StrictDjangoModelPermissions, Group-based clearances (RBAC) and scoped Throttling.

<br>

## Security Architecture

The system implements a layered Zero-Trust security model across every request lifecycle — from authentication at the gate to immutable logging of every record touched.

| Security Control | Implementation |
|---|---|
| **Authentication** | Djoser + SimpleJWT — 45-min access token, 4-day refresh token |
| **Authorization** | StrictDjangoModelPermissions + Group-based RBAC across 4 clearance tiers |
| **Audit Trail** | Immutable CUD logging via `signals.py` + `@audit_read` decorator on every READ |
| **Rate Limiting** | Scoped throttles per endpoint group (Medical: 20/min · Audit: 50/min) |
| **Data Integrity** | `transaction.atomic()` on all multi-model writes — zero ghost records |
| **Deployment Hardening** | 7-point Django production security audit with documented mitigations |

> 📄 For the full threat analysis, vulnerability explanations in plain language, and production mitigation code — see [`Security Test Report.md`](./Security%20Test%20Report.md)

<br>

## Project Structure

```
Arkham Asylum Root/
├── arkham_app/                   # Core Django application
│   ├── management/commands/      # Custom management commands (DB seeder)
│   ├── migrations/               # Database migration files
│   ├── models.py                 # CellBlock, InmateProfile, MedicalFile, AuditLog
│   ├── views.py                  # DRF ViewSets & business logic
│   ├── serializers.py            # Request/Response serialization
│   ├── permissions.py            # RBAC & StrictDjangoModelPermissions
│   ├── signals.py                # Immutable CUD audit logging
│   ├── decorators.py             # @audit_read decorator
│   ├── throttles.py              # Scoped rate limiting
│   ├── filters.py                # QuerySet filtering
│   └── middleware.py             # ThreadLocal user tracking
├── arkham_pm/                    # Django project settings & URL config
├── Functional Tests/             # PyTest automation suite (27 test cases)
│   ├── conftest.py               # Fixtures & auth token factories
│   └── Functional test report.md # Terminal output & observations
├── Performance Test/             # Locust load testing suite
│   └── locustfile.py             # Swarm simulation with JWT auth
├── Security Test Report.md       # Django deployment audit & mitigations
├── solution_architecture.html    # High-level system diagram (Mermaid.js)
├── technical_architecture.html   # Low-level request lifecycle diagram
├── database_er_model.html        # ER model & schema visualization
├── creds.md                      # Development user credentials reference
├── requirements.txt              # Python dependencies
├── pytest.ini                    # PyTest configuration
├── LICENSE                       # MIT License
└── SECURITY.md                   # Vulnerability reporting policy
```

<br>

## Architecture Documentation

The repository contains three interactive `mermaid.js` diagrams detailing the exact flow and constraints of the system. Open these HTML files directly in any web browser to view the system visualization:

* **[`solution_architecture.html`](./solution_architecture.html)**: High-level module interaction for Business Stakeholders.
* **[`technical_architecture.html`](./technical_architecture.html)**: Low-level Django/DRF request lifecycles, middlewares, and throttles.
* **[`database_er_model.html`](./database_er_model.html)**: Exact Database Schema, relationships, and constraints.

<br>

## Quick Start & Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/abhijeet2829/Arkham-Asylum-Backend.git
cd Arkham-Asylum-Backend
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

### 4. Database Setup

Log into your local MySQL workbench and create the database:

```sql
CREATE DATABASE arkham_registry;
```

*Note: Update [`arkham_pm/settings.py`](./arkham_pm/settings.py) with your MySQL credentials.*

### 5. Run Migrations & Start Server

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 8000
```

### 6. Populate Baseline Data (Optional)

To prevent manual data entry via Postman, Arkham features an automated database seeder. This will inject 10 comprehensive Inmates, linked Medical Files, 4 Security Clearance Groups, 3 Cell Blocks, and 10 Active Personnel directly into your local database.

```bash
python manage.py seed_arkham
```

<br>

## Testing & Quality Assurance

Arkham Asylum ships with a comprehensive, three-layered testing architecture. Each layer can be executed independently.

| Layer | Tool | Directory | Coverage |
|-------|------|-----------|----------|
| **Functional** | PyTest | [`Functional Tests/`](./Functional%20Tests/) | 27 headless assertions across all 24+ endpoints |
| **Performance** | Locust | [`Performance Test/`](./Performance%20Test/) | Load simulation with 100 concurrent JWT-authenticated users |
| **Security** | Django Native | [`Security Test Report.md`](./Security%20Test%20Report.md) | 7-point deployment configuration audit |

### Run PyTest Functional/Automation Suite (Optional)

To verify the structural integrity of all 24 API endpoints locally, execute the headless PyTest suite against the project.

```bash
pytest -v
```

### Run Performance Test Suite (Optional)

To execute the Arkham Asylum load-testing swarm and monitor response behavior under heavy personnel traffic:

```bash
cd "Performance Test"
locust -f locustfile.py
```

Open `http://localhost:8089` in your local browser to configure the swarm.

**Sample Parameters to input:**

* **Number of users:** `100`
* **Spawn rate:** `10`
* **Host:** `http://127.0.0.1:8000`

Click "Start swarming" to commence load testing. Stop after few secs & analyze the results.

### Run Security Audit (Optional)

To grade the system's Django production settings and view inherently unmitigated local vulnerabilities:

```bash
python manage.py check --deploy
```

*Note: The warnings raised here are intentional for development functionality. For mitigation strategies, refer to the [`Security Test Report.md`](./Security%20Test%20Report.md).*

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

<br>

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
