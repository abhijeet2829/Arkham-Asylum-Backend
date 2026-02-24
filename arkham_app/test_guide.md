# Transfer Safety Engine — Manual Test Guide

> **Goal:** Verify that the unified `PATCH /inmates/{id}` endpoint correctly enforces the Transfer Safety Engine when Security Staff tries to change an inmate's `cell_block`, while allowing Super Admins to bypass it and non-transfer PATCHes to go through freely.

<br>

## How the Safety Engine Works

When a `PATCH` request hits `/inmates/{id}`, the backend checks two things:

1. **Is the user Security Staff?**
2. **Is `cell_block` in the request body?**

If **both are true**, the Safety Engine activates and demands:

- A **Medical Staff** member has read or updated that inmate's medical file within the **last 7 days**
- A **Super Admin** has read that inmate's medical file within the **last 24 hours**

If either check fails → **403 Forbidden**. If both pass → transfer proceeds normally.

If the user is a **Super Admin**, or the PATCH doesn't touch `cell_block` → Safety Engine **does not fire at all**.

<br>

## Pre-Requisite: Get Auth Tokens

For each user below, send a `POST` to:

```
POST http://127.0.0.1:8000/api/auth/jwt/create/
```

| User | Payload | Role |
|------|---------|------|
| Bruce | `{"username": "bruce", "password": "batman"}` | Super Admin |
| Leland | `{"username": "Leland", "password": "cS4QzQWU'OC"}` | Medical Staff |
| CashAaron | `{"username": "CashAaron", "password": "B10ckC!Duty5"}` | Security Staff |

Copy the `access` token from each response. Use it as: `Authorization: Bearer <token>`

<br>

---

## Test 1: Security Staff patches `cell_block` — No audit trail exists

**Request:**
```
PATCH http://127.0.0.1:8000/api/v1/default-router/inmates/1
Authorization: Bearer <CashAaron_token>
Body: {"cell_block": "Block-C"}
```

**Expected:** `403 Forbidden`

**Why:** CashAaron (Security Staff) is trying to move an inmate. The Safety Engine fires because `cell_block` is in the body AND he's Security Staff. It queries the AuditLog for recent Medical Staff and Super Admin reviews — finds **nothing** — so the transfer is **blocked**.

---

## Test 2: Security Staff patches `status` — Non-cell_block field

**Request:**
```
PATCH http://127.0.0.1:8000/api/v1/default-router/inmates/1
Authorization: Bearer <CashAaron_token>
Body: {"status": "ACTIVE"}
```

**Expected:** `403 Forbidden`

**Why:** CashAaron is patching `status`, NOT `cell_block`. The field restriction layer kicks in — Security Staff is only allowed to update `cell_block`. Any other field gets rejected with "Security Staff can only update cell_block."

---

## Test 3: Create a Medical audit trail, then retry transfer

**Step 3a — Leland reads the medical file:**
```
GET http://127.0.0.1:8000/api/v1/default-router/medical-records/1
Authorization: Bearer <Leland_token>
```

This creates a `DETAILED_READ` entry in the AuditLog with `actor_group = "Medical Staff"`.

**Step 3b — CashAaron retries the transfer:**
```
PATCH http://127.0.0.1:8000/api/v1/default-router/inmates/1
Authorization: Bearer <CashAaron_token>
Body: {"cell_block": "Block-D"}
```

**Expected:** `403 Forbidden`

**Why:** The Safety Engine fires. It finds Leland's recent medical review (check 1 passes), but then checks for a Super Admin read within 24 hours — finds **nothing** — so the transfer is still **blocked**. Both boxes must be ticked.

---

## Test 4: Create an Admin audit trail, then retry transfer

**Step 4a — Bruce reads the same medical file:**
```
GET http://127.0.0.1:8000/api/v1/default-router/medical-records/1
Authorization: Bearer <bruce_token>
```

This creates a `DETAILED_READ` entry in the AuditLog with `actor_group = "Super Admin"`.

**Step 4b — CashAaron retries the transfer:**
```
PATCH http://127.0.0.1:8000/api/v1/default-router/inmates/1
Authorization: Bearer <CashAaron_token>
Body: {"cell_block": "Block-E"}
```

**Expected:** `200 OK`

**Why:** The Safety Engine fires. Check 1: Leland reviewed the file < 7 days ago — **PASS**. Check 2: Bruce reviewed the file < 24 hours ago — **PASS**. Both boxes are ticked, so the transfer is **approved**. The response will show the updated inmate with `cell_block: "Block-E"`.

---

## Test 5: Super Admin patches `cell_block` — Bypass

**Request:**
```
PATCH http://127.0.0.1:8000/api/v1/default-router/inmates/1
Authorization: Bearer <bruce_token>
Body: {"cell_block": "Block-A"}
```

**Expected:** `200 OK`

**Why:** Bruce is a Super Admin, not Security Staff. The Safety Engine's condition (`user is Security Staff AND cell_block is in body`) is **false** on the first check. The engine never fires. Bruce can move anyone, anytime — he's the authority.

---

## Summary Checklist

| # | Scenario | Expected | Reasoning |
|---|----------|----------|-----------|
| 1 | Security PATCH `cell_block` (no audit) | **403** | Engine fires, no audit trail exists |
| 2 | Security PATCH `status` | **403** | Engine doesn't fire, field restriction blocks |
| 3 | Medical reads file → Security retries | **403** | Medical done, Admin missing |
| 4 | Admin reads file → Security retries | **200** | Both checks pass |
| 5 | Admin PATCH `cell_block` directly | **200** | Engine skips for Super Admins |
