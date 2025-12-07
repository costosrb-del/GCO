"""
Script de prueba simple para verificar que los movimientos funcionan
"""
from datetime import datetime, timedelta
from config import get_config
from auth import get_auth_token
from movements import get_consolidated_movements

def test_movements():
    print("=== PRUEBA DE MOVIMIENTOS ===\n")
    
    # Configurar fechas (últimos 30 días)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    api_start = start_date.strftime("%Y-%m-%d")
    api_end = end_date.strftime("%Y-%m-%d")
    
    print(f"Rango de fechas: {api_start} a {api_end}\n")
    
    # Obtener configuración
    companies = get_config()
    print(f"Empresas configuradas: {len(companies)}\n")
    
    all_movements = []
    
    for i, company in enumerate(companies):
        print(f"\n--- Empresa {i+1}/{len(companies)}: {company['name']} ---")
        
        # Obtener token
        token = get_auth_token(company["username"], company["access_key"])
        if not token:
            print("[ERROR] No se pudo obtener token")
            continue
        
        print("[OK] Token obtenido")
        
        # Obtener movimientos
        def progress(msg):
            print(f"  {msg}")
        
        movements = get_consolidated_movements(token, api_start, api_end, progress_callback=progress)
        
        print(f"\n[RESULTADO] Movimientos encontrados: {len(movements)}")
        
        if movements:
            print("\nPrimeros 3 movimientos:")
            for m in movements[:3]:
                print(f"  - {m.get('date')} | {m.get('code')} | {m.get('name')} | Qty: {m.get('quantity')}")
        
        # Agregar empresa al movimiento
        for m in movements:
            m["company"] = company["name"]
            all_movements.append(m)
    
    print(f"\n\n=== RESUMEN FINAL ===")
    print(f"Total movimientos consolidados: {len(all_movements)}")
    
    if all_movements:
        print("\nDistribución por tipo de documento:")
        doc_types = {}
        for m in all_movements:
            dt = m.get("doc_type", "unknown")
            doc_types[dt] = doc_types.get(dt, 0) + 1
        
        for dt, count in doc_types.items():
            print(f"  {dt}: {count}")
    else:
        print("\n[ADVERTENCIA] No se encontraron movimientos en el rango de fechas especificado")
        print("Esto puede ser normal si no hay facturas/notas en ese período")

if __name__ == "__main__":
    test_movements()
