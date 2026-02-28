# Arkham Asylum Functional Test Report

<br>

## Executive Summary

This document serves as the official operational report for the headless Functional Testing suite executing against the Django REST Framework backend.

<br>

## Test Environment

- **Frameworks:** PyTest, PyTest-Django
- **Architecture:** Headless execution targeting a synchronized dummy SQLite database.
- **Coverage:** 24 Discrete API Endpoints encompassing Authentication, Profiles, Inmates, Medical Records, and System Management.

<br>

## Terminal Output & Observations

```text
plugins: locust-2.43.3, django-4.12.0, html-4.2.0, metadata-3.1.1
collecting ... collected 27 items

Functional Tests/audits.py::TestAuditLogs::test_audit_log_list <- tests\audits.py PASSED [  3%]
Functional Tests/audits.py::TestAuditLogs::test_audit_immutable <- tests\audits.py PASSED [  7%]
Functional Tests/health_and_auth.py::TestHealthAndAuth::test_health_check_endpoint <- tests\health_and_auth.py PASSED [ 11%]
Functional Tests/health_and_auth.py::TestHealthAndAuth::test_user_registration <- tests\health_and_auth.py PASSED [ 14%]
Functional Tests/health_and_auth.py::TestHealthAndAuth::test_jwt_create <- tests\health_and_auth.py PASSED [ 18%]
Functional Tests/health_and_auth.py::TestHealthAndAuth::test_jwt_refresh <- tests\health_and_auth.py PASSED [ 22%]
Functional Tests/health_and_auth.py::TestHealthAndAuth::test_jwt_verify <- tests\health_and_auth.py PASSED [ 25%]
Functional Tests/inmates.py::TestInmateManagement::test_inmate_list <- tests\inmates.py PASSED [ 29%]
Functional Tests/inmates.py::TestInmateManagement::test_inmate_retrieve <- tests\inmates.py PASSED [ 33%]
Functional Tests/inmates.py::TestInmateManagement::test_inmate_retrieve_public <- tests\inmates.py PASSED [ 37%]
Functional Tests/inmates.py::TestInmateManagement::test_inmate_admission_success <- tests\inmates.py PASSED [ 40%]
Functional Tests/inmates.py::TestInmateManagement::test_inmate_admission_full_capacity <- tests\inmates.py PASSED [ 44%]
Functional Tests/inmates.py::TestInmateManagement::test_inmate_transfer_success <- tests\inmates.py PASSED [ 48%]
Functional Tests/inmates.py::TestInmateManagement::test_inmate_transfer_blocked_no_admin_review <- tests\inmates.py PASSED [ 51%]
Functional Tests/medical.py::TestMedicalRecords::test_medical_list_filtering <- tests\medical.py PASSED [ 55%]
Functional Tests/medical.py::TestMedicalRecords::test_medical_detailed_read_audit <- tests\medical.py PASSED [ 59%]
Functional Tests/medical.py::TestMedicalRecords::test_medical_update <- tests\medical.py PASSED [ 62%]
Functional Tests/medical.py::TestMedicalRecords::test_medical_delete_forbidden_for_staff <- tests\medical.py PASSED [ 66%]
Functional Tests/medical.py::TestMedicalRecords::test_medical_hard_delete_admin <- tests\medical.py PASSED [ 70%]
Functional Tests/profiles.py::TestProfiles::test_get_own_profile <- tests\profiles.py PASSED [ 74%]
Functional Tests/profiles.py::TestProfiles::test_update_own_profile <- tests\profiles.py PASSED [ 77%]
Functional Tests/profiles.py::TestProfiles::test_set_password <- tests\profiles.py PASSED [ 81%]
Functional Tests/system_management.py::TestSystemManagement::test_cell_blocks_dashboard <- tests\system_management.py PASSED [ 85%]
Functional Tests/system_management.py::TestSystemManagement::test_cell_blocks_unauthorized <- tests\system_management.py PASSED [ 88%]
Functional Tests/system_management.py::TestSystemManagement::test_user_groups_list <- tests\system_management.py PASSED [ 92%]
Functional Tests/system_management.py::TestSystemManagement::test_user_groups_update <- tests\system_management.py PASSED [ 96%]
Functional Tests/system_management.py::TestSystemManagement::test_user_groups_unauthorized <- tests\system_management.py PASSED [100%]

======================= 27 passed, 4 warnings in 56.91s =======================
```

<br>

## Observations

1. **Absolute Confinement:** All 27 assertions passed successfully without a single leakage or unhandled exception.
2. **Transaction Safety:** The Admission Engine correctly mapped atomic relationships. The dummy `InmateProfile` instances sequentially generated their expected `MedicalFile` siblings and natively printed `AuditLog` footprints to the database.
3. **Capacity Logic:** The system strictly enforced the `max_capacity` constraints of the `CellBlock` model, cleanly returning HTTP `400 Bad Request` exceptions upon overflow rather than throwing database-level 500 crashes.

<br>

*Report signed by the Batcomputer.*
