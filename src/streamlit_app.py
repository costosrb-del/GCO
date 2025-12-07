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
    /* Removed aggressive global selector for div/span to fix Dataframe Header overlaps */
    h1, h2, h3, h4, h5, h6 {
        font-family: var(--font-family) !important;
        color: var(--text-primary);
        font-weight: 700;
    }

    /* --- LAYOUT & CONTAINERS --- */
    .block-container {
        padding-top: 2rem !important; /* Reduced */
        padding-bottom: 3rem !important;
        max-width: 95% !important;
        gap: 1rem; /* Compact gap */
    }
    
    /* ERP Card Component */
    .erp-card {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 24px; /* Reduced from 32 */
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        margin-bottom: 16px; /* Compact spacing */
    }
    
    /* --- HEADER SECTION --- */
    .erp-header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px; /* Reduced from 40 */
        background-color: white;
        padding: 16px 24px; /* Compact padding */
        border-radius: 12px;
        border: 1px solid var(--border-color);
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        max-height: 80px; /* Force height constraint */
    }
    .erp-breadcrumb {
        font-size: 0.8rem;
        color: var(--text-secondary);
        margin-bottom: 4px;
    }
    .erp-title {
        font-size: 1.5rem; /* Slightly smaller */
        font-weight: 800;
        color: var(--text-primary);
        margin: 0;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }
    
    /* --- KPI DASHBOARD --- */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr); /* Force 4 columns if possible */
        gap: 16px; /* Compact gap */
        margin-bottom: 24px; /* Reduced margin */
    }
    @media (max-width: 1000px) {
        .kpi-grid { grid-template-columns: repeat(2, 1fr); }
    }
    .kpi-card {
        background: white;
        padding: 16px 20px; /* Reduced padding */
        border-radius: 12px;
        border: 1px solid var(--border-color);
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.06);
    }
    .kpi-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px; /* Reduced */
    }
    .kpi-value {
        font-size: 1.75rem; /* Reduced */
        font-weight: 800;
        color: var(--primary-color);
        line-height: 1.1;
    }
    
    /* --- BUTTONS --- */
    /* General Button Styling */
    .stButton button, .stDownloadButton button {
        border-radius: 8px !important;
        padding: 0.6rem 1.25rem !important;
        font-weight: 600 !important;
        text-transform: none !important;
        letter-spacing: 0.3px;
        font-size: 1rem !important;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Text Color Fix: Dark by default (for secondary buttons on white bg) */
    .stButton button p, .stDownloadButton button p,
    .stButton button span, .stDownloadButton button span,
    .stButton button div, .stDownloadButton button div {
        color: #1E3A2F !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }

    /* Primary Button: Green BG, White Text */
    .stButton button[kind="primary"], .stButton button[data-baseweb="button"][kind="primary"] {
        background-color: #1E3A2F !important;
        border: 2px solid #1E3A2F !important;
    }
    /* Force white text on primary buttons */
    .stButton button[kind="primary"] p, 
    .stButton button[kind="primary"] span,
    .stButton button[kind="primary"] div {
        color: white !important;
    }
    
    /* Hover Effects */
    .stButton button:hover, .stDownloadButton button:hover {
        background-color: #4ADE80 !important; /* Light Green on Hover */
        border-color: #4ADE80 !important;
        # transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    /* Ensure text stays dark on hover */
    .stButton button:hover p, .stDownloadButton button:hover p,
    .stButton button:hover span, .stDownloadButton button:hover span,
    .stButton button:hover div, .stDownloadButton button:hover div {
         color: #1E3A2F !important;
    }

    /* --- SIIGO-STYLE SIDEBAR (GREEN) --- */
    section[data-testid="stSidebar"] {
        background-color: #1E3A2F !important; /* Siigo Green */
        border-right: none !important;
    }
    
    /* Sidebar Content */
    section[data-testid="stSidebar"] > div:first-child {
        background-color: transparent !important;
        padding-top: 0px;
    }
    
    /* Logo/Header Area */
    section[data-testid="stSidebar"] .element-container:first-child {
        padding: 1rem;
        background-color: rgba(0,0,0,0.1); /* Slight darkness for header */
        margin-bottom: 2rem;
    }
    
    /* Menu Items Wrapper (Radio) */
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
        background-color: transparent;
        gap: 8px; /* Slight gap */
    }

    /* Menu Item (Label) Styling */
    section[data-testid="stSidebar"] .stRadio label {
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        width: 100% !important;
        padding: 12px 20px !important;
        border-radius: 4px !important;
        border: none !important;
        margin: 0 !important;
        background-color: transparent !important;
        color: white !important;
        transition: background-color 0.2s;
        cursor: pointer;
        position: relative;
    }
    
    /* Hover Effect */
    section[data-testid="stSidebar"] .stRadio label:hover {
        background-color: rgba(255,255,255,0.1) !important;
    }
    
    /* Active/Selected Item */
    section[data-testid="stSidebar"] .stRadio label[data-checked="true"] {
        background-color: rgba(255,255,255,0.2) !important;
        font-weight: 700 !important;
    }
    
    /* Hide Radio Circles - ROBUST METHOD */
    section[data-testid="stSidebar"] .stRadio label > div:first-child {
        display: none !important;
        width: 0 !important;
        margin: 0 !important;
    }
    
    /* Text styling */
    section[data-testid="stSidebar"] .stRadio label p {
        font-size: 1.1rem !important; /* Larger text */
        color: white !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.5 !important;
        font-weight: 500;
        display: flex;
        align-items: center;
        width: 100%;
    }
    
    /* Logout Button Styling in Sidebar */
    .sidebar-logout button {
        background-color: transparent !important;
        border: 1px solid rgba(255,255,255,0.4) !important;
        color: white !important;
        width: 100%;
        text-align: left;
        padding-left: 20px !important;
    }
    .sidebar-logout button:hover {
        background-color: rgba(255,255,255,0.1) !important;
        border-color: white !important;
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
        <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 10px; padding-left: 10px;'>
             <div style='background: white; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px;'>🌿</div>
             <h2 style='color: white; margin: 0; font-size: 1.25rem; font-weight: 700;'>Siigo Nube</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation Menu (Simulating List)
        nav_options = {
            " Inventarios": "📦",   
            " Movimientos": "📋"    
        }
        
        # Reverse map for logic
        display_options = [f"{icon} {label}" for label, icon in nav_options.items()]
        
        selected_display = st.radio(
            "Menú",
            display_options,
            label_visibility="collapsed"
        )
        
        # Map back to simple key
        menu_option = "Inventarios" if "Inventarios" in selected_display else "Movimientos"
        
        # User Profile & Logout (Moved up, closer to menu)
        st.markdown("<br>", unsafe_allow_html=True) # Small spacer
        st.markdown("---")
        
        # Profile Section
        st.markdown(f"""
        <div style='padding: 0 10px; color: white;'>
            <div style='font-size: 0.8rem; opacity: 0.8;'>Usuario Conectado</div>
            <div style='font-weight: 600;'>{st.session_state.get('user_name', 'Admin')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Logout as a discrete item
        st.markdown('<div class="sidebar-logout">', unsafe_allow_html=True)
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
             logout()
        st.markdown('</div>', unsafe_allow_html=True)

    # Main Content
    if menu_option == "Inventarios":
        # --- ERP HEADER ---
        st.markdown("""
        <div class="erp-header-container">
            <div>
                <div class="erp-breadcrumb">Inicio / Inventarios / General</div>
                <h1 class="erp-title">Gestión de Inventario</h1>
            </div>
            <div></div>
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
            
            if total_companies == 0:
                st.error("No se encontraron empresas configuradas. Verifique los Secretos en Streamlit Cloud.")
                return

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
                            # If result is False, it means something failed inside process_company_data but didn't raise
                            errors.append(f"Fallo al obtener datos de {company['name']}")
                    except Exception as e:
                        # This catches crashes in the thread itself
                        errors.append(f"Error crítico en {company['name']}: {str(e)}")
                    
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

        # --- CONTROLS & FILTERS ---
        st.markdown("### Filtros y Control")
        
        # Action Bar & Update
        col_actions_1, col_actions_2 = st.columns([3, 1])
        with col_actions_2:
             if st.button("ACTUALIZAR INVENTARIO", type="primary", use_container_width=True):
                with st.spinner("Sincronizando con SIIGO..."):
                    update_data()
        
        with col_actions_1:
            if "last_updated" in st.session_state:
                st.caption(f"Última actualización: {st.session_state.last_updated}")
            else:
                st.warning("Datos no sincronizados. Por favor actualice.")

        # Ensure proper types for df, handling empty case safely
        if not df.empty:
            if "quantity" in df.columns:
                df["quantity"] = pd.to_numeric(df["quantity"], errors='coerce').fillna(0)

        # --- ADVANCED FILTERS (Always Visible) ---
        with st.expander("Configuración de Filtros", expanded=True):
            # Row 1
            f1, f2, f3 = st.columns(3)
            with f1:
                companies_list = sorted(df["company_name"].unique().tolist()) if not df.empty else []
                selected_companies = st.multiselect("Empresas", companies_list, placeholder="Todas")
            with f2:
                warehouses_list = sorted(df["warehouse_name"].unique().tolist()) if not df.empty else []
                selected_warehouses = st.multiselect("Bodegas", warehouses_list, placeholder="Todas")
            with f3:
                stock_status = st.selectbox("Estado Stock", ["Todos", "Con Stock (>0)", "Sin Stock (0)"])
            
            # Row 2
            f4, f5, f6 = st.columns(3)
            with f4: 
                # Search
                search_term = st.text_input("Búsqueda Rápida", placeholder="SKU o Nombre...", help="Busca coincidencias en código o descripción")
            with f5:
                # Stock Range
                max_q = int(df["quantity"].max()) if not df.empty else 1000
                stock_range = st.slider("Rango de Stock", 0, max_q, (0, max_q), disabled=df.empty)
            with f6:
                # Special Filter
                filter_sales = st.toggle("Solo Productos de Venta", value=False)
                if filter_sales: st.caption("Filtra códigos específicos de venta.")

        # --- ENGINE: APPLY FILTERS ---
        filtered_df = df.copy() if not df.empty else pd.DataFrame(columns=["company_name", "code", "name", "warehouse_name", "quantity"])
        
        if not filtered_df.empty:
            # 1. Sales Filter
            if filter_sales:
                target_codes = ['7007', '7008', '7009', '7957', '7901', '7101', '7210', '3005', '3001', '7416', 'EVO-7701', 'EVO-7702', 'EVO-7703', '3012']
                import re
                escaped_codes = [re.escape(c) for c in target_codes]
                pattern = '|'.join(escaped_codes)
                filtered_df = filtered_df[filtered_df["code"].astype(str).str.contains(pattern, case=False, na=False)]

            # 2. Standard Filters
            if selected_companies:
                filtered_df = filtered_df[filtered_df["company_name"].isin(selected_companies)]
            if selected_warehouses:
                filtered_df = filtered_df[filtered_df["warehouse_name"].isin(selected_warehouses)]
            
            if stock_status == "Con Stock (>0)":
                filtered_df = filtered_df[filtered_df["quantity"] > 0]
            elif stock_status == "Sin Stock (0)":
                filtered_df = filtered_df[filtered_df["quantity"] == 0]
            
            filtered_df = filtered_df[
                (filtered_df["quantity"] >= stock_range[0]) & 
                (filtered_df["quantity"] <= stock_range[1])
            ]

            if search_term:
                filtered_df = filtered_df[
                    filtered_df["name"].astype(str).str.contains(search_term, case=False, na=False) |
                    filtered_df["code"].astype(str).str.contains(search_term, case=False, na=False)
                ]

        # --- KPI DASHBOARD (Always Visible) ---
        if not filtered_df.empty:
            kpi_units = filtered_df["quantity"].sum()
            kpi_active = filtered_df[filtered_df["quantity"] > 0]["code"].nunique()
            kpi_refs = len(filtered_df)
            kpi_whs = filtered_df["warehouse_name"].nunique()
        else:
            kpi_units = 0
            kpi_active = 0
            kpi_refs = 0
            kpi_whs = 0

        st.markdown(f"""
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Total Unidades</div>
                <div class="kpi-value">{kpi_units:,.0f}</div>
                <div class="kpi-sub">Cantidad Filtrada</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Productos Activos</div>
                <div class="kpi-value">{kpi_active:,.0f}</div>
                <div class="kpi-sub">Con Stock > 0</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Referencias</div>
                <div class="kpi-value">{kpi_refs:,.0f}</div>
                <div class="kpi-sub">Líneas Visibles</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Bodegas</div>
                <div class="kpi-value">{kpi_whs}</div>
                <div class="kpi-sub">En Vista</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")

        # --- RESULTS TABS (Always Visible) ---
        tab1, tab2 = st.tabs(["Listado Detallado", "Vista Consolidada"])
        
        with tab1:
            # Options
            t1_col1, t1_col2 = st.columns([1, 1])
            with t1_col1:
                 st.write(f"Mostrando **{len(filtered_df)}** registros")
            
            st.dataframe(
                filtered_df[["company_name", "code", "name", "warehouse_name", "quantity"]],
                column_config={
                    "company_name": "Empresa",
                    "code": "SKU",
                    "name": "Producto",
                    "warehouse_name": "Bodega",
                    "quantity": st.column_config.NumberColumn("Stock", format="%.0f")
                },
                use_container_width=True,
                height=500,
                hide_index=True
            )
            
            # Export Area
            st.markdown("#### Exportar Selección")
            e1, e2 = st.columns(2)
            
            # Context info for export
            filter_info = {
                "Empresas": str(selected_companies) if selected_companies else "Todas",
                "Bodegas": str(selected_warehouses) if selected_warehouses else "Todas",
                "Búsqueda": search_term if search_term else "N/A"
            }
            
            with e1:
                st.download_button(
                    "Descargar Excel",
                    to_excel(filtered_df[["company_name", "code", "name", "warehouse_name", "quantity"]]),
                    "inventario_filtrado.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    disabled=filtered_df.empty
                )
            with e2:
                st.download_button(
                    "Descargar PDF",
                    to_pdf(filtered_df[["code", "name", "quantity"]], "Inventario Filtrado", filters=filter_info),
                    "inventario_filtrado.pdf",
                    "application/pdf",
                    use_container_width=True,
                    disabled=filtered_df.empty
                )

        with tab2:
            if not filtered_df.empty:
                # Group by Code+Name, sum Quantity
                # Robust grouping
                df_cons = filtered_df.copy()
                df_cons["code"] = df_cons["code"].fillna("N/A").astype(str)
                df_cons["name"] = df_cons["name"].fillna("Sin Nombre").astype(str)
                
                consolidated = df_cons.groupby(["code", "name"])["quantity"].sum().reset_index()
                consolidated = consolidated.sort_values(by="quantity", ascending=False)
                
                st.dataframe(
                    consolidated,
                    column_config={
                         "code": "SKU",
                         "name": "Producto",
                         "quantity": st.column_config.NumberColumn("Total Global", format="%.0f")
                    },
                    use_container_width=True,
                    hide_index=True
                )
                
                # Consolidated Export
                col_ce1, col_ce2 = st.columns(2)
                with col_ce1:
                    st.download_button(
                        "Descargar Excel (Consolidado)",
                        to_excel(consolidated),
                        "consolidado.xlsx",
                        use_container_width=True
                    )
                with col_ce2:
                    st.download_button(
                        "Descargar PDF (Consolidado)",
                         to_pdf(consolidated, "Consolidado de Stock"),
                         "consolidado.pdf",
                         use_container_width=True
                    )
            else:
                st.info("No hay datos para consolidar.")

    elif "Movimientos" in menu_option:
        # --- COMPACT HEADER ---
        st.markdown("""
        <div class="erp-header-container">
            <div>
                <div class="erp-breadcrumb">Inicio / Movimientos / Consulta</div>
                <h1 class="erp-title">Movimientos</h1>
            </div>
            <div></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Load and display movements data
        from movements import get_consolidated_movements
        from auth import get_auth_token
        from config import get_config
        import concurrent.futures
        
        # --- PRIMARY FILTERS (Compacted) ---
        c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
        with c1:
            # Date Range
            default_start = pd.to_datetime('today') - pd.Timedelta(days=30)
            default_end = pd.to_datetime('today')
            date_range = st.date_input("Rango de Fechas", (default_start, default_end), label_visibility="collapsed")
            if isinstance(date_range, tuple) and len(date_range) == 2:
                start_date, end_date = date_range
            else:
                start_date, end_date = default_start, default_end
            st.caption("Rango de consulta")
        
        with c2:
             all_comps = [c["name"] for c in get_config()]
             selected_companies_mov = st.multiselect("Empresas", all_comps, default=all_comps, label_visibility="collapsed", placeholder="Seleccionar Empresas")
             st.caption("Empresas Cloud")

        with c3:
             # Document Type PRE-FILTER
             # FV=Factura Venta, FC=Factura Compra, NC=Nota Credito, ND=Nota Debito, CC=Comprobante
             selected_source_types = st.multiselect("Docs", ["FV", "FC", "CC", "NC", "ND"], default=["FV", "FC"], label_visibility="collapsed", placeholder="Tipos Doc")
             st.caption("Tipos a Consultar (FV, FC...)")

        with c4:
             if st.button("CONSULTAR MOVIMIENTOS", type="primary", use_container_width=True):
                 st.session_state.run_mov_query = True
             st.caption("Actualizar Tabla")
        
        # Helper to load movements (No Cache to prevent stuck UI with Progress)
        def load_movements(start, end, selected_comp_names, selected_types):
            all_movs = []
            errors = []
            # Filter config based on selected names
            comps_to_process = [c for c in get_config() if c["name"] in selected_comp_names]
            
            if not comps_to_process:
                st.warning("Por favor seleccione al menos una empresa.")
                return pd.DataFrame()
            
            # Use a container for progress to ensure it clears
            progress_container = st.empty()
            progress_bar = progress_container.progress(0, text="Consultando historial...")
            
            total = len(comps_to_process)
            completed = 0
            
            def process_comp_movs(company):
                try:
                    token = get_auth_token(company["username"], company["access_key"])
                    if token:
                        # PASS SELECTED TYPES TO LOWER LEVEL
                        movs = get_consolidated_movements(token, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"), selected_types=selected_types)
                        for m in movs:
                            m["company"] = company["name"]
                            all_movs.append(m)
                        return True
                    return False
                except Exception as e:
                    errors.append(f"{company['name']}: {str(e)}")
                    return False

            # Sequential processing (User preference for stability)
            for company in comps_to_process:
                success = process_comp_movs(company)
                completed += 1
                progress_bar.progress(completed / total, text=f"Procesando {company['name']} ({completed}/{total})")

            # Parallel processing (Commented out per user request for stability)
            # with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            #     futures = {executor.submit(process_comp_movs, c): c for c in comps_to_process}
            #     for future in concurrent.futures.as_completed(futures):
            #         completed += 1
            #         progress_bar.progress(completed / total, text=f"Procesando {completed}/{total}")
            
            progress_container.empty()
            if errors:
                for e in errors: st.toast(e, icon="⚠️")
            return pd.DataFrame(all_movs)

        # Trigger Load
        if st.session_state.get("run_mov_query", False):
            with st.spinner("Cargando movimientos de SIIGO..."):
                df_movs = load_movements(start_date, end_date, selected_companies_mov, selected_source_types)
                st.session_state.mov_data = df_movs # Cache in session
            # Reset trigger to prevent rerun loop if needed, though streamlit usually handles button state
            st.session_state.run_mov_query = False 
        
        # Ensure session state has data, even if empty
        if "mov_data" not in st.session_state:
             st.session_state.mov_data = pd.DataFrame()
        
        df_movs = st.session_state.mov_data
            
        # --- ADVANCED FILTERS (ALWAYS VISIBLE) ---
        st.markdown("### Filtrar Resultados")
        af_1, af_2, af_3, af_4, af_5, af_6 = st.columns(6)
        
        # Safe filter lists
        warehouses_list = sorted(df_movs["warehouse"].astype(str).unique().tolist()) if not df_movs.empty else []
        doctypes_list = sorted(df_movs["doc_type"].astype(str).unique().tolist()) if not df_movs.empty else []
        movtypes_list = sorted(df_movs["type"].astype(str).unique().tolist()) if not df_movs.empty else []
        comps_list = sorted(df_movs["company"].astype(str).unique().tolist()) if not df_movs.empty else []

        with af_1:
            sel_wh = st.multiselect("Bodegas", warehouses_list, placeholder="Todas")
        with af_2:
            sel_comp = st.multiselect("Empresas", comps_list, placeholder="Todas")
        with af_3:
            sel_dtype = st.multiselect("Tipos de Doc.", doctypes_list, placeholder="Todos")
        with af_4:
            sel_mtype = st.multiselect("Tipo Movimiento", movtypes_list, placeholder="Todos")
        with af_5:
            search_doc = st.text_input("Buscar # Documento", placeholder="Ej: FV-123...")
        with af_6:
            search_text = st.text_input("Buscar Producto/SKU", placeholder="Nombre o Código...")

        # --- APPLY LOCAL FILTERS ---
        filtered_movs = df_movs.copy()
        
        if not filtered_movs.empty:
            if sel_wh: filtered_movs = filtered_movs[filtered_movs["warehouse"].isin(sel_wh)]
            if sel_comp: filtered_movs = filtered_movs[filtered_movs["company"].isin(sel_comp)]
            if sel_dtype: filtered_movs = filtered_movs[filtered_movs["doc_type"].isin(sel_dtype)]
            if sel_mtype: filtered_movs = filtered_movs[filtered_movs["type"].isin(sel_mtype)]
            
            if search_doc:
                filtered_movs = filtered_movs[
                    filtered_movs["doc_number"].astype(str).str.contains(search_doc, case=False)
                ]
            
            if search_text:
                filtered_movs = filtered_movs[
                    filtered_movs["name"].astype(str).str.contains(search_text, case=False) |
                    filtered_movs["code"].astype(str).str.contains(search_text, case=False)
                ]

        # --- METRICS ---
        if not filtered_movs.empty:
            m1, m2, m3, m4, m5 = st.columns(5)
            total_in = filtered_movs[filtered_movs["type"] == "ENTRADA"]["quantity"].sum()
            total_out = filtered_movs[filtered_movs["type"] == "SALIDA"]["quantity"].sum()
            total_adj = filtered_movs[filtered_movs["type"] == "AJUSTE"]["quantity"].sum()
            
            with m1: st.metric("Total Registros", len(filtered_movs))
            with m2: st.metric("Entradas", f"{total_in:,.0f}")
            with m3: st.metric("Salidas", f"{total_out:,.0f}")
            with m4: st.metric("Ajustes", f"{total_adj:,.0f}")
            with m5: st.metric("SKUs Unicos", filtered_movs["code"].nunique())
        else:
             m1, m2, m3, m4, m5 = st.columns(5)
             with m1: st.metric("Total Registros", 0)
             with m2: st.metric("Entradas", "0")
             with m3: st.metric("Salidas", "0")
             with m4: st.metric("Ajustes", "0")
             with m5: st.metric("SKUs Unicos", 0)

        # --- TABLE & EXPORT ---
        st.markdown("---")
        col_exp1, col_exp2 = st.columns([1, 1])
        
        # Prepare Export Data
        if not filtered_movs.empty:
            export_data = filtered_movs[["date", "company", "doc_type", "doc_number", "code", "name", "warehouse", "type", "quantity"]].copy()
            export_data.columns = ["Fecha", "Empresa", "Tipo Doc", "# Documento", "SKU", "Producto", "Bodega", "Movimiento", "Cantidad"]
        else:
             export_data = pd.DataFrame() # Empty for export

        with col_exp1:
            st.download_button(
                "Descargar Excel (Filtrado)",
                to_excel(export_data),
                "movimientos_filtrados.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                disabled=filtered_movs.empty
            )
        with col_exp2:
            current_filters_text = {
                "Bodegas": str(sel_wh) if sel_wh else "Todas",
                "Docs": str(sel_dtype) if sel_dtype else "Todos"
            }
            
            # Custom Header for PDF
            if not filtered_movs.empty:
                # Calculate Summary for Header
                count_fv = len(filtered_movs[filtered_movs["doc_type"] == "FV"])
                # count_sku = filtered_movs["code"].nunique() # Already calculated in metrics
                count_sku = filtered_movs["code"].nunique()
                total_qty = filtered_movs["quantity"].sum()
                
                start_str = start_date.strftime('%Y-%m-%d')
                end_str = end_date.strftime('%Y-%m-%d')
                
                header_text = f"ORIGEN BOTANICO REPORTE DE MOVIMIENTOS DE {start_str} A {end_str}\n({count_fv} FV, {count_sku} SKU, {total_qty:,.0f} UNIDADES)"
            else:
                header_text = "Reporte Vacío"

            # Only enable PDF if NOT empty, otherwise helper fails
            st.download_button(
                "Descargar PDF (Filtrado)",
                to_pdf(filtered_movs[["date", "doc_type", "doc_number", "name", "quantity"]], "Detalle Movimientos", filters=current_filters_text, custom_header=header_text) if not filtered_movs.empty else b"",
                "movimientos_filtrados.pdf",
                "application/pdf",
                use_container_width=True,
                disabled=filtered_movs.empty
            )
        
        # Spacing
        st.markdown("<br>", unsafe_allow_html=True)

        if not filtered_movs.empty:
            st.dataframe(
                filtered_movs[["date", "company", "doc_type", "doc_number", "code", "name", "warehouse", "type", "quantity"]],
                column_config={
                    "date": st.column_config.TextColumn("Fecha", width="small"),
                    "company": st.column_config.TextColumn("Empresa", width="medium"),
                    "doc_type": st.column_config.TextColumn("Tipo Doc", width="medium"),
                    "doc_number": st.column_config.TextColumn("# Doc", width="small"),
                    "code": st.column_config.TextColumn("SKU", width="small"),
                    "name": st.column_config.TextColumn("Producto", width="large"),
                    "warehouse": st.column_config.TextColumn("Bodega", width="medium"),
                    "type": st.column_config.TextColumn("Tipo", width="small"),
                    "quantity": st.column_config.NumberColumn("Cantidad", format="%.2f", width="small")
                },
                use_container_width=True,
                hide_index=True,
                height=600
            )
        else:
            st.info("Sin datos que mostrar. Realiza una connsulta o ajusta los filtros.")

        # --- DIAGNÓSTICO (Visible para depurar) ---
        with st.expander("🛠️ Diagnóstico de Configuración (Si falta alguna empresa, revisa aquí)"):
            st.write("### Empresas Cargadas Exitosamente:")
            loaded_comps = get_config()
            for c in loaded_comps:
                st.success(f"ID: {c['id']} - {c['name']} (Usuario: {c['username']})")
            
            st.write("### Claves Detectadas en Secretos/Variables:")
            found_keys = []
            
            # Check Streamlit Secrets
            if hasattr(st, "secrets"):
                # Root keys
                for k in st.secrets:
                    if "COMPANY" in k: found_keys.append(f"Secrets (Root): {k}")
                # Credentials nested keys
                if "credentials" in st.secrets:
                    for k in st.secrets["credentials"]:
                        if "COMPANY" in k: found_keys.append(f"Secrets (Credentials): {k}")
            
            # Check OS Environment
            for k in os.environ:
                 if "COMPANY" in k: found_keys.append(f"ENV: {k}")
            
            if found_keys:
                st.code("\n".join(sorted(found_keys)))
            else:
                st.warning("No se detectaron claves tipo 'COMPANY_...' en ninguna parte.")
            
            st.info("Nota: Para que una empresa cargue, debe tener obligatoriamente sus 3 claves: _NAME, _USER y _KEY con el mismo número ID.")
