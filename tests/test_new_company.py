"""
Test script to verify that ALMAVERDE BEAUTY S.A.S. is loaded correctly
"""
from config import get_config

def test_companies():
    companies = get_config()
    print(f"Total companies loaded: {len(companies)}\n")
    
    for company in companies:
        print(f"Company ID: {company['id']}")
        print(f"Name: {company['name']}")
        print(f"Username: {company['username']}")
        print(f"Access Key: {company['access_key'][:20]}...")  # Only show first 20 chars for security
        print("-" * 50)
    
    # Check if ALMAVERDE BEAUTY S.A.S. is loaded
    almaverde = [c for c in companies if "ALMAVERDE" in c['name'].upper()]
    if almaverde:
        print("\n[OK] ALMAVERDE BEAUTY S.A.S. loaded successfully!")
        print(f"  ID: {almaverde[0]['id']}")
        print(f"  Username: {almaverde[0]['username']}")
    else:
        print("\n[ERROR] ALMAVERDE BEAUTY S.A.S. not found!")


if __name__ == "__main__":
    test_companies()
