import requests
import base64
import sys

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Credenciales exactas
username = "yuranigomez@tclasesores.com"
access_key = "NjlhMzBjM2QtYzkzNy00YmFjLWI2ZjktMzZjMmI5ZWE0ZTU0Om4vezxKJTdvMFQ="

print("=" * 60)
print("PRUEBA DE AUTENTICACION - GRUPO HUMAN PROJECT S.A.S.")
print("=" * 60)
print(f"\nUsuario: {username}")
print(f"Access Key: {access_key}")
print(f"Longitud de la KEY: {len(access_key)} caracteres")

# Verificar que no hay espacios
if access_key != access_key.strip():
    print("[!] ADVERTENCIA: La KEY tiene espacios al inicio o final")
    access_key = access_key.strip()
    print(f"KEY limpia: {access_key}")

# Intentar decodificar la KEY para ver si es valida en Base64
try:
    decoded = base64.b64decode(access_key)
    print(f"[OK] La KEY es Base64 valido")
    decoded_str = decoded.decode('utf-8', errors='ignore')
    print(f"Decodificado (primeros 50 chars): {decoded_str[:50]}...")
    # La KEY decodificada debe tener formato: client_id:client_secret
    if ':' in decoded_str:
        parts = decoded_str.split(':')
        print(f"  - Client ID: {parts[0][:20]}...")
        print(f"  - Client Secret: {parts[1][:10]}...")
    else:
        print("[!] ADVERTENCIA: La KEY decodificada no tiene el formato esperado (client_id:client_secret)")
except Exception as e:
    print(f"[ERROR] Error decodificando Base64: {e}")

print("\n" + "=" * 60)
print("INTENTANDO AUTENTICACION CON SIIGO API")
print("=" * 60)

# Metodo 1: Usando el modulo auth.py
print("\n[Metodo 1] Usando auth.py del sistema...")
try:
    from auth import get_auth_token
    token = get_auth_token(username, access_key)
    if token:
        print(f"[OK] EXITO con auth.py")
        print(f"Token: {token[:50]}...")
    else:
        print("[ERROR] FALLO con auth.py - Token es None")
except Exception as e:
    print(f"[ERROR] ERROR con auth.py: {e}")

# Metodo 2: Llamada directa a la API
print("\n[Metodo 2] Llamada directa a SIIGO API...")
try:
    url = "https://api.siigo.com/auth"
    headers = {
        "Content-Type": "application/json",
        "Partner-Id": "ORIGEN_BOTANICO"
    }
    payload = {
        "username": username,
        "access_key": access_key
    }
    
    print(f"URL: {url}")
    print(f"Headers: {headers}")
    print(f"Payload: {payload}")
    
    response = requests.post(url, json=payload, headers=headers)
    
    print(f"\nCodigo de respuesta: {response.status_code}")
    print(f"Respuesta completa:")
    print(response.text)
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"\n[OK] AUTENTICACION EXITOSA!")
        print(f"Token: {token[:50]}...")
    else:
        print(f"\n[ERROR] AUTENTICACION FALLIDA")
        print(f"Detalles del error:")
        try:
            error_data = response.json()
            for error in error_data.get("errors", []):
                print(f"  - Codigo: {error.get('code')}")
                print(f"  - Mensaje: {error.get('message')}")
                print(f"  - Detalle: {error.get('detail')}")
        except:
            pass
            
except Exception as e:
    print(f"[ERROR] ERROR en llamada directa: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("RECOMENDACIONES")
print("=" * 60)
print("""
Si la autenticacion falla:
1. Verifica en el portal de SIIGO que estas credenciales esten activas
2. Confirma que el usuario tiene permisos de API
3. Verifica que la empresa este activa en SIIGO
4. Intenta regenerar la ACCESS KEY desde el portal de SIIGO
5. Contacta con soporte de SIIGO si el problema persiste
""")
