from config import get_config

companies = get_config()
print(f'Total companies configured: {len(companies)}\n')

for c in companies:
    print(f'Company {c["id"]}: {c["name"]}')
    print(f'  User: {c["username"]}')
    print(f'  Key: {c["access_key"][:20]}...')
    print()
