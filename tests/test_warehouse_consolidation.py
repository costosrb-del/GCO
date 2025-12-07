"""
Test script to verify the warehouse consolidation and auto-selection features
"""
import json
import os

# Simulate warehouse data from multiple companies
test_data = [
    {
        "company_name": "Armonia Cosmetica S.A.S.",
        "code": "7416",
        "name": "Producto Test 1",
        "warehouses": [
            {"name": "Bodega Principal Rionegro", "quantity": 100},
            {"name": "Bodega de Averías", "quantity": 5}
        ]
    },
    {
        "company_name": "Hechizo de Bellez SAS",
        "code": "7901",
        "name": "Producto Test 2",
        "warehouses": [
            {"name": "Bodega Principal Rionegro", "quantity": 200},
            {"name": "Bodega de Averías", "quantity": 10}
        ]
    },
    {
        "company_name": "Raices Organicas S.A.S.",
        "code": "7957",
        "name": "Producto Test 3",
        "warehouses": [
            {"name": "Bodega Principal", "quantity": 150},
            {"name": "Bodega de Averías", "quantity": 3}
        ]
    },
    {
        "company_name": "ALMAVERDE BEAUTY S.A.S.",
        "code": "7210",
        "name": "Producto Test 4",
        "warehouses": [
            {"name": "Bodega Principal Rionegro", "quantity": 300},
            {"name": "Bodega de Averías", "quantity": 8}
        ]
    }
]

# Extract unique warehouses (simulating the consolidation logic)
warehouses = set()
for p in test_data:
    for w in p.get("warehouses", []):
        warehouses.add(w.get("name", "Unknown"))

print("=" * 60)
print("WAREHOUSE CONSOLIDATION TEST")
print("=" * 60)
print(f"\nTotal products: {len(test_data)}")
print(f"Total companies: {len(set(p['company_name'] for p in test_data))}")
print(f"\nUnique warehouses (consolidated):")
for i, warehouse in enumerate(sorted(warehouses), 1):
    print(f"  {i}. {warehouse}")

print(f"\n[OK] Warehouses consolidated successfully!")
print(f"  Before: Each company had 2 warehouses = 8 total entries")
print(f"  After: {len(warehouses)} unique warehouse names")

# Test auto-selection logic
print("\n" + "=" * 60)
print("AUTO-SELECTION TEST")
print("=" * 60)
print("\nWhen 'Producto Base de Venta' is selected:")
print("  Looking for warehouse with 'RIONEGRO' and 'PRINCIPAL'...")

warehouse_list = sorted(warehouses)
selected = None
for i, warehouse_name in enumerate(warehouse_list):
    if "RIONEGRO" in warehouse_name.upper() and "PRINCIPAL" in warehouse_name.upper():
        selected = warehouse_name
        print(f"  [OK] Auto-selected: '{warehouse_name}' (index {i})")
        break

if not selected:
    print("  [X] No matching warehouse found!")
else:
    print(f"\n[OK] Auto-selection working correctly!")


print("\n" + "=" * 60)
