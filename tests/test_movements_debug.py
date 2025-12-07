"""
Script de prueba para depurar la funcionalidad de movimientos
"""
from datetime import datetime, timedelta
from config import get_config
from auth import get_auth_token
from movements import get_consolidated_movements

def test_movements_debug():
    print("=== PRUEBA DE MOVIMIENTOS CON DEBUG ===\n")
    
    # Configurar fechas (últimos 7 días para prueba rápida)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    api_start = start_date.strftime("%Y-%m-%d")
    api_end = end_date.strftime("%Y-%m-%d")
    
    print(f"Rango de fechas: {api_start} a {api_end}\n")
    
    # Obtener configuración
    companies = get_config()
    print(f"Empresas configuradas: {len(companies)}\n")
    
    if not companies:
        print("[ERROR] No hay empresas configuradas en .env")
        return
    
    # Probar solo con la primera empresa
    company = companies[0]
    print(f"Probando con: {company['name']}\n")
    
    # Obtener token
    print("1. Obteniendo token...")
    try:
        token = get_auth_token(company["username"], company["access_key"])
        if not token:
            print("[ERROR] No se pudo obtener token")
            return
        print(f"[OK] Token obtenido: {token[:30]}...\n")
    except Exception as e:
        print(f"[ERROR] Excepción al obtener token: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Obtener movimientos
    print("2. Obteniendo movimientos...")
    try:
        def progress(msg):
            print(f"  -> {msg}")
        
        movements = get_consolidated_movements(token, api_start, api_end, progress_callback=progress)
        
        print(f"\n[RESULTADO] Movimientos encontrados: {len(movements)}\n")
        
        if movements:
            print("Primeros 5 movimientos:")
            for m in movements[:5]:
                print(f"  - {m.get('date')} | {m.get('doc_type')} | {m.get('code')} | {m.get('name')} | Qty: {m.get('quantity')}")
        else:
            print("[ADVERTENCIA] No se encontraron movimientos")
            print("Esto puede ser normal si no hay facturas/notas en ese período")
            
    except Exception as e:
        print(f"\n[ERROR] Excepción al obtener movimientos: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_movements_debug()
