import streamlit as st
from auth_streamlit import check_password, logout
import pandas as pd
import time
from datetime import datetime
from utils import to_excel, to_pdf

# Page Config
st.set_page_config(
    page_title="Gestor de Inventarios - Origen Botánico",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Global Reset & Typography */
    .stApp {
        background-color: var(--background-color);
        color: var(--text-primary);
        font-family: var(--font-family);
    }
    h1, h2, h3, h4, h5, h6, p, div, span {
        font-family: var(--font-family) !important;
        color: var(--text-primary);
    }

    /* --- LAYOUT & CONTAINERS --- */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 95% !important;
    }
    
    /* ERP Card Component */
    .erp-card {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    /* --- HEADER SECTION --- */
    .erp-header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
        background-color: white;
        padding: 16px 24px;
        border-radius: 8px;
        border: 1px solid var(--border-color);
    }
    .erp-breadcrumb {
        font-size: 0.875rem;
        color: var(--text-secondary);
        margin-bottom: 4px;
    }
    .erp-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
    }
    
    /* --- KPI DASHBOARD --- */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 20px;
        margin-bottom: 24px;
    }
    .kpi-card {
        background: white;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid var(--border-color);
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .kpi-label {
        font-size: 0.875rem;
        font-weight: 500;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 1.875rem;
        font-weight: 700;
        color: var(--primary-color);
    }
    .kpi-sub {
        font-size: 0.75rem;
        color: #10B981; /* Success Green */
        margin-top: 4px;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* --- FILTERS & CONTROLS --- */
    .filter-bar {
        background: white;
        padding: 16px;
        border-radius: 8px;
        border: 1px solid var(--border-color);
        margin-bottom: 20px;
    }

    /* --- SIIGO-STYLE SIDEBAR (GREEN CORPORATE) --- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E3A2F 0%, #1A3229 100%) !important;
        border-right: none !important;
    }
    
    /* Sidebar Content */
    section[data-testid="stSidebar"] > div:first-child {
        background-color: transparent !important;
    }
    
    /* Logo/Header Area */
    section[data-testid="stSidebar"] .element-container:first-child {
        padding: 1.5rem 1rem;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Menu Items */
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
        gap: 2px;
        padding: 0.5rem 0;
    }
    section[data-testid="stSidebar"] .stRadio label {
        padding: 14px 20px;
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.8);
        background-color: rgba(255,255,255,0.2);
        transition: all 0.3s ease;
        color: white !important;
        font-weight: 600;
        display: flex;
        align-items: center;
        margin: 2px 12px;
        cursor: pointer;
        min-width: 180px;
        justify-content: center;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        background-color: rgba(255,255,255,0.3);
        color: white !important;
        transform: translateX(4px);
    }
    section[data-testid="stSidebar"] .stRadio label[data-checked="true"] {
        background-color: rgba(255,255,255,0.15);
        color: white !important;
        border-left: 4px solid #4ADE80;
        border-radius: 0 8px 8px 0;
        font-weight: 600;
    }
    section[data-testid="stSidebar"] .stRadio label p {
        font-size: 0.95rem;
        color: inherit !important;
    }
    
    /* Section Dividers */
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.1);
        margin: 1rem 0;
    }
    
    /* Caption/Footer */
    section[data-testid="stSidebar"] .element-container p {
        color: rgba(255,255,255,0.6) !important;
    }

    /* --- BUTTONS (ALL GREEN WITH BOLD WHITE TEXT) --- */
    .stButton button, .stDownloadButton button {
        background-color: var(--primary-color) !important;
        color: white !important;
        border-radius: 6px;
        font-weight: 700 !important;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.2s;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .stButton button p, .stDownloadButton button p,
    .stButton button span, .stDownloadButton button span,
    .stButton button div, .stDownloadButton button div {
        color: white !important;
        font-weight: 700 !important;
    }
    .stButton button:hover, .stDownloadButton button:hover {
        background-color: var(--primary-hover) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    /* Secondary/Ghost Buttons */
    button[kind="secondary"] {
        background-color: white !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
    }

    /* --- DATA TABLE --- */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border-color);
        border-radius: 8px;
        overflow: hidden;
    }
    [data-testid="stDataFrame"] div[role="grid"] {
        background-color: white;
    }
    [data-testid="stDataFrame"] div[role="columnheader"] {
        background-color: #F9FAFB;
        color: var(--text-primary);
        font-weight: 600;
        border-bottom: 1px solid var(--border-color);
    }
    
    /* --- UTILS --- */
    .text-right { text-align: right; }
    .w-full { width: 100%; }
    
</style>
""", unsafe_allow_html=True)

if check_password():
    # --- AUTHENTICATED AREA ---
    
    # Force Altair/Vega Theme to Light
    try:
        import altair as alt
        alt.themes.enable("default")
    except:
        pass

    # SIIGO-Style Sidebar
    with st.sidebar:
        # Logo/Header
        st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h2 style='color: white; margin: 0; font-size: 1.5rem; font-weight: 700;'>🌿 Origen Botánico</h2>
            <p style='color: rgba(255,255,255,0.7); font-size: 0.85rem; margin-top: 0.25rem;'>Sistema ERP</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Main Navigation
        st.markdown("<p style='color: rgba(255,255,255,0.5); font-size: 0.75rem; text-transform: uppercase; padding: 0 1rem; margin-bottom: 0.5rem;'>Menú Principal</p>", unsafe_allow_html=True)
        menu_option = st.radio(
            "Navegación",
            ["Inicio", "Inventarios", "Movimientos", "Configuración"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Secondary Navigation
        st.markdown("<p style='color: rgba(255,255,255,0.5); font-size: 0.75rem; text-transform: uppercase; padding: 0 1rem; margin-bottom: 0.5rem;'>Herramientas</p>", unsafe_allow_html=True)
        secondary_option = st.radio(
            "Secundario",
            ["📊 Reportes", "🤝 Alianzas", "🛒 Tienda"],
            label_visibility="collapsed",
            key="secondary_nav"
        )
        
        # Spacer
        st.markdown("<br>" * 5, unsafe_allow_html=True)
        
        # User Info & Logout
        st.markdown(f"<p style='color: rgba(255,255,255,0.6); font-size: 0.85rem; padding: 0 1rem;'>👤 {st.session_state.get('user_name', 'Usuario')}</p>", unsafe_allow_html=True)
        if st.button("CERRAR SESIÓN", use_container_width=True):
            logout()
            
        st.caption(f"v1.4.0 | {datetime.now().strftime('%d/%m/%Y')}")

    # Main Content
    if menu_option == "Inventarios":
        # --- ERP HEADER ---
        st.markdown("""
        <div class="erp-header-container">
            <div>
                <div class="erp-breadcrumb">Inicio / Inventarios / General</div>
                <h1 class="erp-title">Gestión de Inventario</h1>
            </div>
            <div>
                <!-- Primary Action Placeholder -->
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # --- DATA LOADING ---
        from config import get_config
        from auth import get_auth_token
        from inventory import get_all_products
        import concurrent.futures
        
        # Initialize session state for data if not present
        if "inventory_data" not in st.session_state:
            st.session_state.inventory_data = pd.DataFrame()
        
        def update_data():
            companies = get_config()
            all_data = []
            errors = []
            
            # Progress Container
            progress_container = st.empty()
            progress_bar = progress_container.progress(0, text="Iniciando actualización masiva...")
            status_text = st.empty()
            
            total_companies = len(companies)
            completed = 0
            
            # Use max_workers = total_companies to run ALL in parallel
            with concurrent.futures.ThreadPoolExecutor(max_workers=total_companies) as executor:
                future_to_company = {executor.submit(process_company_data, c): c for c in companies}
                
                for future in concurrent.futures.as_completed(future_to_company):
                    company = future_to_company[future]
                    try:
                        result, company_data = future.result()
                        if result:
                            all_data.extend(company_data)
                        else:
                            errors.append(f"Error en {company['name']}")
                    except Exception as e:
                        errors.append(f"Excepción en {company['name']}: {str(e)}")
                    
                    completed += 1
                    progress_bar.progress(completed / total_companies, text=f"Procesando... ({completed}/{total_companies})")
            
            progress_container.empty()
            status_text.empty()
            
            if errors:
                for err in errors: st.toast(err, icon="⚠️")
                st.error(f"Se encontraron errores en: {', '.join(errors)}")
            else:
                st.toast("Datos actualizados correctamente", icon="✅")
            
            # SAVE DATA BEFORE RERUN
            st.session_state.inventory_data = pd.DataFrame(all_data)
            st.session_state.last_updated = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            time.sleep(1)
            st.rerun()

        def process_company_data(company):
            # Helper function for parallel execution
            c_data = []
            try:
                token = get_auth_token(company["username"], company["access_key"])
                if token:
                    products = get_all_products(token)
                    if products:
                        for p in products:
                            p["company_name"] = company["name"]
                            if "warehouses" in p:
                                for wh in p["warehouses"]:
                                    item = p.copy()
                                    item["code"] = item.get("code", "N/A")
                                    item["name"] = item.get("name", "Sin Nombre")
                                    item["warehouse_name"] = wh.get("name", "Unknown")
                                    item["quantity"] = float(wh.get("quantity", 0))
                                    if "warehouses" in item: del item["warehouses"]
                                    c_data.append(item)
                            else:
                                p["code"] = p.get("code", "N/A")
                                p["name"] = p.get("name", "Sin Nombre")
                                p["warehouse_name"] = "N/A"
                                p["quantity"] = 0.0
                                c_data.append(p)
                    return True, c_data
                else:
                    return False, []
            except Exception as e:
                return False, []

        df = st.session_state.inventory_data

        if df.empty:
            st.info("Presiona **ACTUALIZAR** para cargar los datos desde la API.")
            # Initialize empty DataFrame with correct types
            df = pd.DataFrame({
                "company_name": pd.Series(dtype='str'),
                "code": pd.Series(dtype='str'),
                "name": pd.Series(dtype='str'),
                "warehouse_name": pd.Series(dtype='str'),
                "quantity": pd.Series(dtype='float')
            })

        if True: # Always run to show table
            # Ensure quantity is float
            if "quantity" in df.columns:
                df["quantity"] = pd.to_numeric(df["quantity"], errors='coerce').fillna(0)

            # --- KPI DASHBOARD ---
            if not df.empty:
                total_products = len(df)
                total_units = df["quantity"].sum()
                active_skus = df[df["quantity"] > 0]["code"].nunique()
                total_warehouses = df["warehouse_name"].nunique()
            else:
                # Show zeros when no data
                total_products = 0
                total_units = 0
                active_skus = 0
                total_warehouses = 0
                
                # Welcome message
                st.info("👋 **Bienvenido al Sistema de Gestión de Inventarios**\n\nPresiona el botón **ACTUALIZAR** para cargar los datos desde las APIs de SIIGO.")
            
            st.markdown(f"""
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-label">Total Unidades</div>
                    <div class="kpi-value">{total_units:,.0f}</div>
                    <div class="kpi-sub">📦 En todas las bodegas</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Productos Activos</div>
                    <div class="kpi-value">{active_skus:,.0f}</div>
                    <div class="kpi-sub">✅ Con stock disponible</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Total Referencias</div>
                    <div class="kpi-value">{total_products:,.0f}</div>
                    <div class="kpi-sub">📋 SKUs registrados</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Bodegas</div>
                    <div class="kpi-value">{total_warehouses}</div>
                    <div class="kpi-sub">🏭 Centros de distribución</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # --- CONTROLS & FILTERS ---
            with st.container():
                # Action Bar
                c_search, c_update, c_last_update = st.columns([3, 1, 2])
                with c_search:
                    search_term = st.text_input("Buscar", placeholder="Buscar por nombre, SKU...", label_visibility="collapsed")
                with c_update:
                    if st.button("ACTUALIZAR", type="primary", use_container_width=True):
                        with st.spinner("Actualizando inventario..."):
                            update_data()
                with c_last_update:
                    if "last_updated" in st.session_state:
                        st.caption(f"Última sincronización: {st.session_state.last_updated}")
                    else:
                        st.caption("Datos no sincronizados")

                # Collapsible Advanced Filters
                with st.expander("⚙️ Filtros Avanzados", expanded=True):
                    st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
                    
                    # Row 1
                    f1, f2, f3 = st.columns(3)
                    with f1:
                        companies_list = sorted(df["company_name"].unique().tolist()) if not df.empty else []
                        selected_companies = st.multiselect("Empresas", companies_list, placeholder="Filtrar por empresa")
                    with f2:
                        warehouses_list = sorted(df["warehouse_name"].unique().tolist()) if not df.empty else []
                        selected_warehouses = st.multiselect("Bodegas", warehouses_list, placeholder="Filtrar por bodega")
                    with f3:
                        stock_status = st.selectbox("Estado de Stock", ["Todos", "Con Stock (>0)", "Sin Stock (0)"])
                    
                    st.markdown("<hr style='margin: 10px 0; border-color: #eee;'>", unsafe_allow_html=True)
                    
                    # Row 2
                    f4, f5, f6 = st.columns(3)
                    with f4:
                        max_qty = int(df["quantity"].max()) if not df.empty else 1000
                        stock_range = st.slider("Rango de Cantidad", 0, max_qty, (0, max_qty))
                    with f5:
                        top_n = st.number_input("Top N Productos", min_value=0, value=0)
                    with f6:
                        analysis_mode = st.selectbox("Análisis Rápido", ["Normal", "Bajo Stock (<5)", "Sobrestock (>100)"])
                    
                    # Row 3
                    f7, f8 = st.columns(2)
                    with f7:
                        prefix_filter = st.text_input("Prefijo SKU", placeholder="Ej: 700...")
                    with f8:
                        filter_sales = st.toggle("Solo Productos de Venta", value=False)
                        
                    st.markdown('</div>', unsafe_allow_html=True)

                # --- APPLY FILTERS ---
                filtered_df = df.copy()
                
                if not filtered_df.empty:
                    # Logic implementation (same as before, just cleaner code structure)
                    if filter_sales:
                        target_codes = ['7007', '7008', '7009', '7957', '7901', '7101', '7210', '3005', '3001', '7416', 'EVO-7701', 'EVO-7702', 'EVO-7703', '3012']
                        pattern = '|'.join(target_codes)
                        filtered_df = filtered_df[filtered_df["code"].str.contains(pattern, case=False, na=False)]
                    
                    if selected_companies: filtered_df = filtered_df[filtered_df["company_name"].isin(selected_companies)]
                    if selected_warehouses: filtered_df = filtered_df[filtered_df["warehouse_name"].isin(selected_warehouses)]
                    
                    if stock_status == "Con Stock": filtered_df = filtered_df[filtered_df["quantity"] > 0]
                    elif stock_status == "Sin Stock": filtered_df = filtered_df[filtered_df["quantity"] == 0]

                    # Advanced
                    filtered_df = filtered_df[(filtered_df["quantity"] >= stock_range[0]) & (filtered_df["quantity"] <= stock_range[1])]
                    if prefix_filter: filtered_df = filtered_df[filtered_df["code"].astype(str).str.startswith(prefix_filter)]
                    
                    if analysis_mode == "Bajo Stock (<5)": filtered_df = filtered_df[(filtered_df["quantity"] < 5) & (filtered_df["quantity"] > 0)]
                    elif analysis_mode == "Sobrestock (>100)": filtered_df = filtered_df[filtered_df["quantity"] > 100]

                    if search_term:
                        filtered_df = filtered_df[
                            filtered_df["name"].str.contains(search_term, case=False, na=False) | 
                            filtered_df["code"].str.contains(search_term, case=False, na=False)
                        ]
                    
                    if top_n > 0: filtered_df = filtered_df.nlargest(top_n, "quantity")

                # --- TABS CONTENT ---
                tab1, tab2 = st.tabs(["📋 Listado Detallado", "📊 Vista Consolidada"])
                
                with tab1:
                    # Expand table option
                    col_toggle, col_spacer = st.columns([2, 8])
                    with col_toggle:
                        expand_table = st.toggle("⤢ Expandir Tabla", value=False)
                    
                    if expand_table:
                        st.markdown("""
                        <style>
                            .block-container {
                                max-width: 98% !important;
                                padding-left: 0.5rem !important;
                                padding-right: 0.5rem !important;
                            }
                            [data-testid="stSidebar"] {
                                display: none !important;
                            }
                        </style>
                        """, unsafe_allow_html=True)
                    
                    st.dataframe(
                        filtered_df[["company_name", "code", "name", "warehouse_name", "quantity"]],
                        column_config={
                            "company_name": "Empresa",
                            "code": "SKU",
                            "name": "Producto",
                            "warehouse_name": "Bodega",
                            "quantity": st.column_config.NumberColumn("Stock", format="%.0f")
                        },
                        width='stretch',
                        height=800 if expand_table else 500,
                        hide_index=True
                    )
                    
                    # Prepare Export Data
                    export_df = filtered_df[["company_name", "code", "name", "warehouse_name", "quantity"]].copy()
                    export_df.columns = ["Empresa", "SKU", "Producto", "Bodega", "Stock"]
                    # Ensure integer for export
                    export_df["Stock"] = export_df["Stock"].fillna(0).astype(int)
                    
                    # Prepare Filters for PDF
                    current_filters = {
                        "Empresas": selected_companies if selected_companies else "Todas",
                        "Bodegas": selected_warehouses if selected_warehouses else "Todas",
                        "Estado Stock": stock_status,
                        "Solo Venta": "Sí" if filter_sales else "No",
                        "Búsqueda": search_term if search_term else "N/A"
                    }


                    # Exports
                    st.markdown("---")
                    st.markdown("**📤 Exportar Datos**")
                    col_exp1, col_exp2 = st.columns(2)
                    with col_exp1:
                        st.download_button(
                            "📊 Descargar Excel", 
                            to_excel(export_df), 
                            "inventario.xlsx", 
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                    with col_exp2:
                        st.download_button(
                            "📄 Descargar PDF", 
                            to_pdf(filtered_df[["code", "name", "quantity"]], "Inventario Detallado", filters=current_filters), 
                            "inventario.pdf", 
                            "application/pdf",
                            use_container_width=True
                        )


                with tab2:
                    if not filtered_df.empty:
                        try:
                            # Ensure numeric before grouping
                            filtered_df["quantity"] = pd.to_numeric(filtered_df["quantity"], errors='coerce').fillna(0)
                            
                            # Fill NaNs in grouping columns to avoid errors
                            filtered_df["code"] = filtered_df["code"].fillna("N/A").astype(str)
                            filtered_df["name"] = filtered_df["name"].fillna("Sin Nombre").astype(str)
                            
                            consolidated_df = filtered_df.groupby(["code", "name"])["quantity"].sum().reset_index().sort_values(by="quantity", ascending=False)
                            st.dataframe(
                                consolidated_df,
                                column_config={
                                    "code": "SKU",
                                    "name": "Producto",
                                    "quantity": st.column_config.NumberColumn("Total Consolidado", format="%.0f")
                                },
                                width='stretch',
                                hide_index=True
                            )
                        except Exception as e:
                            st.error(f"Error calculando consolidado: {e}")
                        
                        # Prepare Export Data Consolidado
                        export_cons = consolidated_df.copy()
                        export_cons.columns = ["SKU", "Producto", "Total Consolidado"]
                        export_cons["Total Consolidado"] = export_cons["Total Consolidado"].fillna(0).astype(int)
                        
                        # Exports Consolidado
                        col_exp1, col_exp2 = st.columns([1, 1])
                        with col_exp1:
                            st.download_button("Descargar Excel", to_excel(export_cons), "consolidado.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="xls_cons")
                        with col_exp2:
                            st.download_button("Descargar PDF", to_pdf(consolidated_df, "Inventario Consolidado"), "consolidado.pdf", "application/pdf", key="pdf_cons")
                    else:
                        st.dataframe(
                            pd.DataFrame(columns=["code", "name", "quantity"]),
                            column_config={
                                "code": "SKU",
                                "name": "Producto",
                                "quantity": st.column_config.NumberColumn("Cantidad", format="%d")
                            },
                            width='stretch',
                            hide_index=True
                        )

    elif "Movimientos" in menu_option:
        st.title("Movimientos")
        # Load and display movements data
        from movements import get_consolidated_movements
        from auth import get_auth_token
        import concurrent.futures
        
        # Parameters (you can adjust date range as needed)
        start_date = pd.to_datetime('today') - pd.Timedelta(days=30)
        end_date = pd.to_datetime('today')
        selected_company_mov = "Todas"
        
        @st.cache_data(ttl=300)
        def load_movements(start, end, selected_comp_name):
            all_movs = []
            errors = []
            comps_to_process = get_config() if selected_comp_name == "Todas" else [c for c in get_config() if c["name"] == selected_comp_name]
            my_bar = st.progress(0, text="Consultando...")
            total = len(comps_to_process)
            completed = 0
            def process_comp_movs(company):
                try:
                    token = get_auth_token(company["username"], company["access_key"])
                    if token:
                        movs = get_consolidated_movements(token, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
                        for m in movs:
                            m["company"] = company["name"]
                            all_movs.append(m)
                        return True
                    return False
                except Exception as e:
                    errors.append(f"{company['name']}: {str(e)}")
                    return False
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                futures = {executor.submit(process_comp_movs, c): c for c in comps_to_process}
                for future in concurrent.futures.as_completed(futures):
                    completed += 1
                    my_bar.progress(completed / total, text=f"Procesando {completed}/{total}")
            my_bar.empty()
            if errors:
                for e in errors:
                    st.toast(e, icon="⚠️")
            return pd.DataFrame(all_movs)
        
        df_movs = load_movements(start_date, end_date, selected_company_mov)
        if not df_movs.empty:
            # --- MOVIMIENTOS TABLE UI ---
            col_toggle, col_exp1, col_exp2 = st.columns([2, 1, 1])
            with col_toggle:
                expand_mov = st.toggle("⤢ Expandir Tabla", value=False)
            with col_exp1:
                st.download_button(
                    "Descargar Excel",
                    to_excel(df_movs),
                    "movimientos.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            with col_exp2:
                st.download_button(
                    "Descargar PDF",
                    to_pdf(df_movs, "Movimientos"),
                    "movimientos.pdf",
                    "application/pdf",
                    use_container_width=True
                )
            if expand_mov:
                st.markdown("""
                <style>
                    .block-container {max-width: 98% !important; padding-left: 0.5rem !important; padding-right: 0.5rem !important;}
                    [data-testid=\"stSidebar\"] {display: none !important;}
                </style>
                """, unsafe_allow_html=True)
            st.dataframe(df_movs)
        else:
            st.warning("No se encontraron movimientos.")
            
    elif "Configuración" in menu_option:

        if st.button("Consultar Movimientos"):
            from movements import get_consolidated_movements
            from auth import get_auth_token
            import concurrent.futures
            
            @st.cache_data(ttl=300)
            def load_movements(start, end, selected_comp_name):
                all_movs = []
                errors = []
                comps_to_process = companies if selected_comp_name == "Todas" else [c for c in companies if c["name"] == selected_comp_name]
                
                my_bar = st.progress(0, text="Consultando...")
                total = len(comps_to_process)
                completed = 0
                
                def process_comp_movs(company):
                    try:
                        token = get_auth_token(company["username"], company["access_key"])
                        if token:
                            movs = get_consolidated_movements(token, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
                            for m in movs:
                                m["company"] = company["name"]
                                all_movs.append(m)
                            return True
                        return False
                    except Exception as e:
                        errors.append(f"{company['name']}: {str(e)}")
                        return False

                with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                    futures = {executor.submit(process_comp_movs, c): c for c in comps_to_process}
                    for future in concurrent.futures.as_completed(futures):
                        completed += 1
                        my_bar.progress(completed / total, text=f"Procesando {completed}/{total}")
                
                my_bar.empty()
                if errors:
                    for e in errors: st.toast(e, icon="⚠️")
                return pd.DataFrame(all_movs)

            with st.spinner("Cargando movimientos..."):
                df_movs = load_movements(start_date, end_date, selected_company_mov)
            
            if not df_movs.empty:
                # Metrics
                total_in = df_movs[df_movs["type"] == "ENTRADA"]["quantity"].sum()
                total_out = df_movs[df_movs["type"] == "SALIDA"]["quantity"].sum()
                
                c1, c2, c3 = st.columns(3)
                with c1: st.markdown(f'<div class="metric-card"><div class="metric-value">{len(df_movs)}</div><div class="metric-label">Total Movimientos</div></div>', unsafe_allow_html=True)
                with c2: st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:green">+{total_in:,.0f}</div><div class="metric-label">Total Entradas</div></div>', unsafe_allow_html=True)
                with c3: st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:red">-{total_out:,.0f}</div><div class="metric-label">Total Salidas</div></div>', unsafe_allow_html=True)
                
                st.markdown("### Detalle de Transacciones")
                st.dataframe(
                    df_movs[["date", "company", "doc_type", "doc_number", "code", "name", "warehouse", "type", "quantity"]],
                    column_config={
                        "date": "Fecha",
                        "company": "Empresa",
                        "doc_type": "Tipo",
                        "doc_number": "# Doc",
                        "code": "SKU",
                        "name": "Producto",
                        "warehouse": "Bodega",
                        "type": "Movimiento",
                        "quantity": st.column_config.NumberColumn("Cantidad", format="%.2f")
                    },
                    width='stretch',
                    hide_index=True
                )
                
                # Prepare Export Data Movimientos
                export_movs = df_movs[["date", "company", "doc_type", "doc_number", "code", "name", "warehouse", "type", "quantity"]].copy()
                export_movs.columns = ["Fecha", "Empresa", "Tipo", "# Doc", "SKU", "Producto", "Bodega", "Movimiento", "Cantidad"]
                # Ensure integer for export (or float with 2 decimals if preferred, but user asked for NO decimals in general context, though movements might need them. Let's stick to user request: "cantidades sin decimales")
                export_movs["Cantidad"] = export_movs["Cantidad"].fillna(0).astype(int)

                # Exports
                col_exp1, col_exp2 = st.columns([1, 1])
                with col_exp1:
                    st.download_button("Descargar Excel", to_excel(export_movs), "movimientos.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="mov_xls")
                with col_exp2:
                    st.download_button("Descargar PDF", to_pdf(df_movs[["date", "doc_number", "name", "quantity"]], "Reporte Movimientos"), "movimientos.pdf", "application/pdf", key="mov_pdf")

            else:
                st.warning("No se encontraron movimientos.")
            
    elif menu_option == "Configuración":
        st.title("Configuración")
        st.markdown("### 🔐 Credenciales de API")
        
        # Secure display of configuration
        if "siigo" in st.secrets:
            config_data = st.secrets["siigo"]
            secure_config = []
            for company in config_data:
                secure_config.append({
                    "Empresa": company.get("name", "N/A"),
                    "Usuario": company.get("username", "N/A"),
                    "Access Key": "●●●●●●●●" + company.get("access_key", "")[-4:] if company.get("access_key") else "N/A"
                })
            st.table(secure_config)
            st.info("Las credenciales están cargadas de forma segura desde `secrets.toml`.")
        else:
            st.error("No se encontraron credenciales en `secrets.toml`.")
