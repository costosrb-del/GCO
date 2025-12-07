from config import get_config
from auth import get_auth_token

companies = get_config()

print("=" * 70)
print("VERIFICACION FINAL - TODAS LAS EMPRESAS CONFIGURADAS")
print("=" * 70)
print(f"\nTotal de empresas: {len(companies)}\n")

for i, company in enumerate(companies, 1):
    print(f"{i}. {company['name']}")
    print(f"   Usuario: {company['username']}")
    print(f"   Key: {company['access_key'][:30]}...")
    
    # Probar autenticacion
    token = get_auth_token(company['username'], company['access_key'])
    if token:
        print(f"   Estado: [OK] Autenticacion exitosa")
    else:
        print(f"   Estado: [ERROR] Fallo en autenticacion")
    print()

print("=" * 70)
print("RESUMEN")
print("=" * 70)

successful = sum(1 for c in companies if get_auth_token(c['username'], c['access_key']))
print(f"Empresas configuradas: {len(companies)}")
print(f"Autenticaciones exitosas: {successful}")
print(f"Autenticaciones fallidas: {len(companies) - successful}")

if successful == len(companies):
    print("\n[OK] Todas las empresas estan correctamente configuradas!")
else:
    print("\n[ADVERTENCIA] Algunas empresas tienen problemas de autenticacion")
