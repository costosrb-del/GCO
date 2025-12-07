import json
import os
import sys

def get_data_directory():
    # Try OneDrive first
    try:
        userprofile = os.environ.get('USERPROFILE', '')
        onedrive_path = os.path.join(userprofile, 'OneDrive - Juan Pablo Muñoz Castaño', 'Inventario 2025', 'saldos')
        if os.path.exists(onedrive_path):
            return onedrive_path
    except:
        pass
    
    # Fallback to local data folder
    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    
    local_data = os.path.join(script_dir, 'data')
    if os.path.exists(local_data):
        return local_data
    
    return None

data_dir = get_data_directory()
if not data_dir:
    print("ERROR: No data directory found")
    input("Press Enter...")
    sys.exit(1)

file_path = os.path.join(data_dir, 'consolidated_inventory.json')
print(f"Reading: {file_path}")

if not os.path.exists(file_path):
    print("ERROR: File not found")
    input("Press Enter...")
    sys.exit(1)

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"\nTotal products in file: {len(data)}")

# Find 7416
matches = [p for p in data if p.get('code') == '7416']
print(f"\nFound {len(matches)} entries for product 7416")

for i, p in enumerate(matches, 1):
    print(f"\n--- Entry {i} ---")
    print(f"  Company: {p.get('company_name')}")
    print(f"  Warehouses:")
    total = 0
    for w in p.get('warehouses', []):
        qty = w.get('quantity', 0)
        print(f"    - {w.get('name')}: {qty}")
        total += float(qty)
    print(f"  Total for this entry: {total}")

# Calculate grand total
grand_total = 0
for p in matches:
    for w in p.get('warehouses', []):
        grand_total += float(w.get('quantity', 0))

print(f"\n=== GRAND TOTAL for 7416: {grand_total} ===")

input("\nPress Enter to close...")
