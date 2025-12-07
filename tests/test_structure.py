import requests
import json
from config import get_config
from auth import get_auth_token

def test_invoice_structure():
    """Test to see actual structure of invoice data"""
    print("=== ANALIZANDO ESTRUCTURA DE FACTURAS ===\n")
    
    companies = get_config()
    company = companies[0]
    
    token = get_auth_token(company["username"], company["access_key"])
    if not token:
        print("[ERROR] No token")
        return
        
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "Partner-Id": "SiigoApi"
    }
    
    url = "https://api.siigo.com/v1/invoices"
    params = {"page": 1, "page_size": 1}
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])
        
        if results:
            invoice = results[0]
            print("ESTRUCTURA DE UNA FACTURA:")
            print(json.dumps(invoice, indent=2, ensure_ascii=False))
            
            print("\n\n=== CLAVES PRINCIPALES ===")
            for key in invoice.keys():
                print(f"- {key}: {type(invoice[key])}")
                
            print("\n\n=== ITEMS ===")
            items = invoice.get("items", [])
            print(f"Total items: {len(items)}")
            if items:
                print("\nPrimer item:")
                print(json.dumps(items[0], indent=2, ensure_ascii=False))
        else:
            print("[INFO] No hay facturas")
    else:
        print(f"[ERROR] {response.status_code}: {response.text}")

if __name__ == "__main__":
    test_invoice_structure()
