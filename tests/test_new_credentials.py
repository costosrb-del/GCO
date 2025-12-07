import requests
import base64
import sys

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# NUEVAS Credenciales para GRUPO HUMAN PROJECT
username = "costos@ritualbotanico.com"
access_key = "MDhjYTVmZjEtY2JlOS00NzM4LWFkYmYtZGY0Y2VhY2E5OWI1OkEzfmc5MHY3X1E="

print("=" * 60)
print("PRUEBA CON NUEVAS CREDENCIALES - GRUPO HUMAN PROJECT")
print("=" * 60)
print(f"\nUsuario: {username}")
print(f"Access Key: {access_key}")
print(f"Longitud de la KEY: {len(access_key)} caracteres")

# Verificar que no hay espacios
access_key = access_key.strip()

# Intentar decodificar la KEY para ver si es valida en Base64
try:
    decoded = base64.b64decode(access_key)
    print(f"[OK] La KEY es Base64 valido")
    decoded_str = decoded.decode('utf-8', errors='ignore')
    print(f"Decodificado: {decoded_str[:50]}...")
    if ':' in decoded_str:
        parts = decoded_str.split(':')
        print(f"  - Client ID: {parts[0]}")
        print(f"  - Client Secret: {parts[1]}")
except Exception as e:
    print(f"[ERROR] Error decodificando Base64: {e}")

print("\n" + "=" * 60)
print("INTENTANDO AUTENTICACION CON SIIGO API")
print("=" * 60)

# Llamada directa a la API
try:
    url = "https://api.siigo.com/auth"
    headers = {
        "Content-Type": "application/json",
        "Partner-Id": "SiigoApi"
    }
    payload = {
        "username": username,
        "access_key": access_key
    }
    
    print(f"\nURL: {url}")
    print(f"Payload: {payload}")
    
    response = requests.post(url, json=payload, headers=headers)
    
    print(f"\nCodigo de respuesta: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        token = data.get("access_token")
        print(f"\n*** AUTENTICACION EXITOSA! ***")
        print(f"Token obtenido: {token[:50]}...")
        print(f"Expira en: {data.get('expires_in')} segundos")
        
        # Probar obtener inventario
        print("\n" + "=" * 60)
        print("PROBANDO ACCESO A INVENTARIO")
        print("=" * 60)
        
        inv_url = "https://api.siigo.com/v1/products"
        inv_headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "Partner-Id": "SiigoApi"
        }
        
        inv_response = requests.get(inv_url, headers=inv_headers, params={"page_size": 5, "page": 1})
        print(f"Codigo de respuesta inventario: {inv_response.status_code}")
        
        if inv_response.status_code == 200:
            products = inv_response.json().get("results", [])
            print(f"[OK] Productos obtenidos: {len(products)}")
            if products:
                print(f"Primer producto: {products[0].get('code')} - {products[0].get('name')}")
        else:
            print(f"[ERROR] No se pudo obtener inventario: {inv_response.text[:200]}")
            
    else:
        print(f"\n[ERROR] AUTENTICACION FALLIDA")
        print(f"Respuesta: {response.text}")
        try:
            error_data = response.json()
            for error in error_data.get("errors", []):
                print(f"  - Codigo: {error.get('code')}")
                print(f"  - Mensaje: {error.get('message')}")
        except:
            pass
            
except Exception as e:
    print(f"[ERROR] ERROR en llamada: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("CONCLUSION")
print("=" * 60)
