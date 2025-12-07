"""
Script para probar la conexión con cada empresa configurada
"""
from config import get_config
from auth import get_auth_token
import requests

def test_all_companies():
    print("=== PRUEBA DE CONEXION CON EMPRESAS ===\n")
    
    companies = get_config()
    print(f"Total empresas configuradas: {len(companies)}\n")
    
    for i, company in enumerate(companies):
        print(f"\n{'='*60}")
        print(f"EMPRESA {i+1}: {company['name']}")
        print(f"Usuario: {company['username']}")
        print(f"{'='*60}")
        
        # Test 1: Obtener token
        print("\n[TEST 1] Obteniendo token de autenticacion...")
        try:
            token = get_auth_token(company["username"], company["access_key"])
            if token:
                print(f"[OK] Token obtenido: {token[:20]}...")
            else:
                print("[ERROR] No se pudo obtener token")
                continue
        except Exception as e:
            print(f"[ERROR] Excepcion al obtener token: {e}")
            continue
        
        # Test 2: Consultar productos
        print("\n[TEST 2] Consultando productos...")
        try:
            url = "https://api.siigo.com/v1/products"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
                "Partner-Id": "SiigoApi"
            }
            params = {"page": 1, "page_size": 5}
            
            response = requests.get(url, headers=headers, params=params)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                print(f"[OK] Productos encontrados: {len(results)}")
                if results:
                    print(f"Ejemplo: {results[0].get('code')} - {results[0].get('name')}")
            else:
                print(f"[ERROR] Respuesta: {response.text[:200]}")
        except Exception as e:
            print(f"[ERROR] Excepcion: {e}")
        
        print(f"\n{'='*60}\n")

if __name__ == "__main__":
    test_all_companies()
