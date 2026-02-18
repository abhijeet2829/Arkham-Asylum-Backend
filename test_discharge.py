import requests

BASE = 'http://localhost:8001'

# Login as bruce (Super Admin)
token = requests.post(f'{BASE}/api/auth/jwt/create/', json={'username': 'bruce', 'password': 'batman'}).json()['access']
headers = {'Authorization': f'Bearer {token}'}

# List all inmates to find Harvey
inmates = requests.get(f'{BASE}/api/v1/default-router/inmates', headers=headers).json()
for i in inmates:
    pid = i["id"]
    name = i["name"]
    status = i["status"]
    print(f"ID:{pid} | {name} | Status: {status}")

# Find Harvey
harvey = [i for i in inmates if 'Harvey' in i['name']]
if harvey:
    hid = harvey[0]['id']
    print(f"\n--- Discharging Harvey (ID:{hid}) ---")
    r = requests.patch(f'{BASE}/api/v1/default-router/inmates/{hid}', json={'status': 'DISCHARGED'}, headers=headers)
    print(f"Response ({r.status_code}): {r.json()}")
else:
    print("Harvey not found in inmates list")
