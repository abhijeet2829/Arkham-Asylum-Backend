## 🔌 API Endpoints

Base URL: `http://127.0.0.1:8001`

<br>

### 0. Health Check

| # | Method | Endpoint | Who Can Call | Sample Payload | Description |
|---|--------|----------|-------------|----------------|-------------|
| 0 | `GET` | `/api/v1/root/` | Anyone (public) | — | Returns a welcome message confirming the server is alive. |

<br>

### 1. Registration

| # | Method | Endpoint | Who Can Call | Sample Payload | Description |
|---|--------|----------|-------------|----------------|-------------|
| 1 | `POST` | `/api/auth/users/` | Anyone (public) | `{"username": "JohnDoe", "email": "john@gotham.com", "password": "SecureP@ss1"}` | Register a new user account. User starts with zero group clearance (orphan). |

<br>

### 2. Authentication

| # | Method | Endpoint | Who Can Call | Sample Payload | Description |
|---|--------|----------|-------------|----------------|-------------|
| 2 | `POST` | `/api/auth/jwt/create/` | Any registered user | `{"username": "JohnDoe", "password": "SecureP@ss1"}` | Login — returns `access` (45 min) and `refresh` (4 days) tokens. |
| 3 | `POST` | `/api/auth/jwt/refresh/` | Any registered user | `{"refresh": "<refresh_token>"}` | Get a new access token using a valid refresh token. |
| 4 | `POST` | `/api/auth/jwt/verify/` | Any registered user | `{"token": "<access_token>"}` | Verify if a given token is still valid. Returns 200 or 401. |

<br>

### 3. Profile & Password

| # | Method | Endpoint | Who Can Call | Sample Payload | Description |
|---|--------|----------|-------------|----------------|-------------|
| 5 | `GET` | `/api/auth/users/me/` | Any authenticated user | — | View own profile (username, email, id). |
| 6 | `PATCH` | `/api/auth/users/me/` | Any authenticated user | `{"email": "new@gotham.com"}` | Update own profile details (username, email). |
| 7 | `POST` | `/api/auth/users/set_password/` | Any authenticated user | `{"current_password": "OldP@ss", "new_password": "NewP@ss1"}` | Change own password. Requires current password for identity verification. |

<br>

### 4. Inmate Management

| # | Method | Endpoint | Who Can Call | Sample Payload | Description |
|---|--------|----------|-------------|----------------|-------------|
| 8 | `GET` | `/api/v1/default-router/inmates` | Super Admin, Security Staff, Medical Staff, Public Visitor | — | List all inmates with name, alias, cell block, and status. |
| 9 | `GET` | `/api/v1/default-router/inmates/{id}` | Super Admin, Security Staff, Medical Staff, Public Visitor | — | Retrieve a single inmate's full details. Triggers audit log. |
| 10 | `POST` | `/api/v1/default-router/inmates` | Super Admin | `{"name": "Bane", "alias": "The Man Who Broke the Bat", "cell_block": "Block-D"}` | Admit a new inmate. Status defaults to `ACTIVE`. |
| 11 | `PATCH` | `/api/v1/default-router/inmates/{id}` | Super Admin, Security Staff | `{"status": "DISCHARGED"}` | Update inmate details or soft-delete via status change. |
| 12 | `POST` | `/api/v1/default-router/inmates/{id}/transfer` | Super Admin, Security Staff | `{"cell_block": "Block-C"}` | Transfer inmate to a different cell block. Throttled (10/min). |

> **Note:** `PUT` and `DELETE` are blocked via `http_method_names`. Inmates are never hard-deleted — use `PATCH {"status": "DISCHARGED"}` for soft-delete (FPH standard).

<br>

### 5. Medical Records

| # | Method | Endpoint | Who Can Call | Sample Payload | Description |
|---|--------|----------|-------------|----------------|-------------|
| 13 | `GET` | `/api/v1/default-router/medical-records` | Super Admin, Medical Staff | — | List all medical records. Throttled (20/min). |
| 14 | `GET` | `/api/v1/default-router/medical-records/{id}` | Super Admin, Medical Staff | — | Retrieve a single medical record. Triggers audit log. |
| 15 | `POST` | `/api/v1/default-router/medical-records` | Super Admin, Medical Staff | `{"inmate": 4, "diagnosis": "DID", "meds": "Risperidone"}` | Create a medical file for an existing inmate. |
| 16 | `PATCH` | `/api/v1/default-router/medical-records/{id}` | Super Admin, Medical Staff | `{"meds": "Updated prescription"}` | Update diagnosis or medication. |
| 17 | `DELETE` | `/api/v1/default-router/medical-records/{id}` | Super Admin | — | Delete a medical record. |

> **Note:** `PUT` is blocked via `http_method_names`. Use `PATCH` for partial updates — overwriting an entire medical record in one shot is not a safe practice in an FPH.

<br>

### 6. User Group Management

| # | Method | Endpoint | Who Can Call | Sample Payload | Description |
|---|--------|----------|-------------|----------------|-------------|
| 18 | `GET` | `/api/v1/default-router/user-groups` | Super Admin | — | List all registered users with their group assignments and active status. |
| 19 | `GET` | `/api/v1/default-router/user-groups/{id}` | Super Admin | — | View a specific user's details (username, email, groups, is_active). |
| 20 | `PATCH` | `/api/v1/default-router/user-groups/{id}` | Super Admin | `{"groups": ["Medical Staff"]}` | Assign/change a user's group clearance. |
| 21 | `PATCH` | `/api/v1/default-router/user-groups/{id}` | Super Admin | `{"groups": []}` | Revoke all group clearance (make user an orphan). |
| 22 | `PATCH` | `/api/v1/default-router/user-groups/{id}` | Super Admin | `{"is_active": false}` | Soft-delete a user (blocks login while preserving records). |

> **Note:** `POST` and `DELETE` are blocked via `http_method_names`. User creation is handled via Djoser registration (#1). Users are never hard-deleted.

<br>

### 7. Audit Logs

| # | Method | Endpoint | Who Can Call | Sample Payload | Description |
|---|--------|----------|-------------|----------------|-------------|
| 23 | `GET` | `/api/v1/default-router/security-logs` | Super Admin | — | List all audit entries (sorted newest first). Throttled (50/min). |
| 24 | `GET` | `/api/v1/default-router/security-logs/{id}` | Super Admin | — | Retrieve a specific audit log entry. |

> **Note:** Audit logs are auto-generated and **immutable**. All write methods (`POST`, `PUT`, `PATCH`, `DELETE`) are blocked via `http_method_names`. CUD operations are logged via Django Signals; Read operations via the `@audit_read` decorator.
