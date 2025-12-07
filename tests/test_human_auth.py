from auth import get_auth_token
from config import get_config

# Get all companies
companies = get_config()

# Find GRUPO HUMAN PROJECT
human_company = None
for c in companies:
    if "HUMAN" in c["name"].upper():
        human_company = c
        break

if human_company:
    print(f"Empresa encontrada: {human_company['name']}")
    print(f"Usuario: {human_company['username']}")
    print(f"Access Key: {human_company['access_key']}")
    print("\nIntentando autenticar...")
    
    token = get_auth_token(human_company['username'], human_company['access_key'])
    
    if token:
        print(f"✅ Autenticación EXITOSA!")
        print(f"Token obtenido: {token[:50]}...")
    else:
        print("❌ Error en la autenticación")
        print("\nVerifica que:")
        print("1. El email sea correcto: yuranigomez@tclasesores.com")
        print("2. La KEY sea correcta (sin espacios adicionales)")
        print("3. La empresa esté activa en SIIGO")
else:
    print("❌ No se encontró la empresa GRUPO HUMAN PROJECT")
