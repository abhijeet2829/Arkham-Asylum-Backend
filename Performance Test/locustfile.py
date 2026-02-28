from locust import HttpUser, task, between
import random

class ArkhamStaffUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        super_admins = ["bruce_admin", "alfred_admin"]
        doctors = ["dr_thompson", "dr_leland", "dr_crane"]
        guards = ["guard_gordon", "guard_cash", "guard_bules"]
        
        username = random.choice(super_admins + doctors + guards)
        
        response = self.client.post("/api/auth/jwt/create/", json={
            "username": username,
            "password": "arkham1234"
        })
        
        if response.status_code == 200:
            token = response.json().get("access")
            self.client.headers.update({"Authorization": f"Bearer {token}"})
        else:
            print(f"Failed to authenticate user {username}. Check if DB is seeded.")

    @task(3)
    def view_inmates(self):
        self.client.get("/api/v1/default-router/inmates", name="Get Inmates List")

    @task(1)
    def view_cell_blocks(self):
        self.client.get("/api/v1/default-router/cell-blocks", name="Get Cell Blocks Dashboard")

    @task(1)
    def view_medical_records(self):
        self.client.get("/api/v1/default-router/medical-records", name="Get Medical Records")

    @task(1)
    def view_audit_logs(self):
        self.client.get("/api/v1/default-router/security-logs/", name="Get Audit Logs")

    @task(1)
    def admit_inmate(self):
        uid = random.randint(100000, 999999)
        self.client.post("/api/v1/default-router/inmates/", json={
            "name": f"Swarm Dummy {uid}",
            "alias": f"Subject {uid}",
            "cell_block": random.choice([1, 2, 3])
        }, name="Admit Inmate (POST)")

    @task(1)
    def transfer_inmate(self):
        target_id = random.randint(1, 10)
        self.client.patch(f"/api/v1/default-router/inmates/{target_id}/transfer/", json={
            "new_cell_block": random.choice([1, 2, 3])
        }, name="Transfer Inmate (PATCH)")