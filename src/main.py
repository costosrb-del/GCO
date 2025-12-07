import argparse
import json
import os
from config import get_config
from auth import get_auth_token
from inventory import get_all_products
from concurrent.futures import ThreadPoolExecutor, as_completed

def main(progress_callback=None):
    parser = argparse.ArgumentParser(description="Siigo API Inventory Fetcher")
    parser.add_argument("--company", type=int, help="Company ID (1-4) to process")
    parser.add_argument("--all", action="store_true", help="Process ALL companies and consolidate")
    args = parser.parse_args()

    companies = get_config()
    
    if not companies:
        if progress_callback:
            progress_callback("error", "No hay empresas configuradas")
        else:
            print("No companies configured. Please check your .env file.")
        return {"successful": 0, "failed": 0, "details": []}

    companies_to_process = []

    if args.all:
        companies_to_process = companies
    elif args.company:
        for c in companies:
            if c["id"] == args.company:
                companies_to_process = [c]
                break
        if not companies_to_process:
            if progress_callback:
                progress_callback("error", f"Empresa {args.company} no encontrada")
            return {"successful": 0, "failed": 0, "details": []}
    else:
        # When called from GUI, process all companies
        companies_to_process = companies

    all_products_consolidated = []
    summary_details = []
    
    # Output directory - Dynamic configuration for portability
    def get_output_directory():
        # Option 1: Try OneDrive with current user
        onedrive_path = os.path.join(os.environ.get('USERPROFILE', ''), 'OneDrive - Juan Pablo Muñoz Castaño', 'Inventario 2025', 'saldos')
        
        if os.path.exists(os.path.dirname(onedrive_path)):
            if not os.path.exists(onedrive_path):
                try:
                    os.makedirs(onedrive_path)
                except OSError:
                    pass
            if os.path.exists(onedrive_path):
                return onedrive_path
        
        # Option 2: Use local data folder
        import sys
        if getattr(sys, 'frozen', False):
            # If frozen (exe), use the directory of the executable
            script_dir = os.path.dirname(sys.executable)
        else:
            # If script, use the directory of the script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
        local_data = os.path.join(script_dir, 'data')
        if not os.path.exists(local_data):
            try:
                os.makedirs(local_data)
            except OSError:
                return None
        return local_data
    
    output_dir = get_output_directory()
    if not output_dir:
        if progress_callback:
            progress_callback("error", "No se pudo crear directorio de salida")
        return {"successful": 0, "failed": 0, "details": []}

    total_companies = len(companies_to_process)
    
    # Function to process a single company
    def process_company(idx_company_tuple):
        idx, company = idx_company_tuple
        company_name = company['name']
        
        if progress_callback:
            progress_callback("company", idx, total_companies, company_name)
            progress_callback("status", "Autenticando...")
        
        # 1. Authenticate
        token = get_auth_token(company["username"], company["access_key"])
        
        if not token:
            error_msg = f"Autenticacion fallida para {company_name}"
            if progress_callback:
                progress_callback("log", error_msg, "error")
            return {
                "company": company_name,
                "status": "error",
                "details": {
                    "error": "Autenticacion fallida",
                    "message": "No se pudo obtener token de acceso. Verifique las credenciales."
                },
                "products": []
            }
        
        if progress_callback:
            progress_callback("log", f"Autenticacion exitosa para {company_name}", "success")
            progress_callback("status", "Obteniendo productos...")
        
        # 2. Fetch Inventory
        def product_progress(msg):
            if progress_callback:
                progress_callback("status", msg)
                progress_callback("log", msg, "info")
        
        try:
            products = get_all_products(token, progress_callback=product_progress)
            
            if products:
                if progress_callback:
                    progress_callback("log", f"Se encontraron {len(products)} productos para {company_name}", "success")
                
                # Add company info to each product
                for p in products:
                    p["company_name"] = company["name"]
                    p["company_id"] = company["id"]
                
                return {
                    "company": company_name,
                    "status": "success",
                    "details": {"products": len(products)},
                    "products": products
                }
            else:
                if progress_callback:
                    progress_callback("log", f"No se encontraron productos para {company_name}", "warning")
                return {
                    "company": company_name,
                    "status": "error",
                    "details": {
                        "error": "Sin productos",
                        "message": "La consulta no retorno productos. Puede ser un error temporal del servidor."
                    },
                    "products": []
                }
        except Exception as e:
            error_msg = str(e)
            if progress_callback:
                progress_callback("log", f"Error obteniendo productos de {company_name}: {error_msg}", "error")
            return {
                "company": company_name,
                "status": "error",
                "details": {
                    "error": "Error en consulta",
                    "message": error_msg
                },
                "products": []
            }
    
    # Process companies in parallel using ThreadPoolExecutor
    # max_workers=4 means up to 4 companies can be processed simultaneously
    with ThreadPoolExecutor(max_workers=min(4, total_companies)) as executor:
        # Submit all companies for processing
        future_to_company = {
            executor.submit(process_company, (idx, company)): company 
            for idx, company in enumerate(companies_to_process, 1)
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_company):
            try:
                result = future.result()
                summary_details.append({
                    "company": result["company"],
                    "status": result["status"],
                    "details": result["details"]
                })
                all_products_consolidated.extend(result["products"])
            except Exception as e:
                company = future_to_company[future]
                if progress_callback:
                    progress_callback("log", f"Error procesando {company['name']}: {str(e)}", "error")

    # 3. Save Consolidated Results
    if all_products_consolidated:
        output_file = os.path.join(output_dir, "consolidated_inventory.json")
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(all_products_consolidated, f, indent=4, ensure_ascii=False)
            if progress_callback:
                progress_callback("log", f"Inventario consolidado guardado: {len(all_products_consolidated)} productos", "success")
        except IOError as e:
            if progress_callback:
                progress_callback("log", f"Error guardando archivo: {e}", "error")
    
    # Return summary
    successful = sum(1 for d in summary_details if d["status"] == "success")
    failed = sum(1 for d in summary_details if d["status"] == "error")
    
    return {
        "successful": successful,
        "failed": failed,
        "total": len(summary_details),
        "details": summary_details
    }

if __name__ == "__main__":
    main()
