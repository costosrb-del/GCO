import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import DateEntry
from tkinter import messagebox, Menu, filedialog
import tkinter as tk
import json
import os
import subprocess
import threading
import sys
import csv
import time
from datetime import datetime, timedelta
import calendar

# --- CONFIGURATION & PATHS ---

def get_data_directory():
    """
    Detect the best data directory to use:
    1. Try OneDrive with current user
    2. Fallback to local 'data' folder in same directory as executable
    """
    # Option 1: Try OneDrive with current user
    try:
        userprofile = os.environ.get('USERPROFILE', '')
        onedrive_path = os.path.join(userprofile, 'OneDrive - Juan Pablo Muñoz Castaño', 'Inventario 2025', 'saldos')
        
        onedrive_base = os.path.dirname(onedrive_path)
        if os.path.exists(onedrive_base):
            if not os.path.exists(onedrive_path):
                try:
                    os.makedirs(onedrive_path)
                except:
                    pass
            if os.path.exists(onedrive_path):
                return onedrive_path
    except Exception:
        pass
    
    # Option 2: Use local data folder
    try:
        if getattr(sys, 'frozen', False):
            script_dir = os.path.dirname(sys.executable)
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))
        
        local_data = os.path.join(script_dir, 'data')
        if not os.path.exists(local_data):
            os.makedirs(local_data)
        return local_data
    except Exception:
        import tempfile
        temp_data = os.path.join(tempfile.gettempdir(), 'SiigoInventario')
        if not os.path.exists(temp_data):
            os.makedirs(temp_data)
        return temp_data

DATA_DIR = get_data_directory()
DATA_FILE = os.path.join(DATA_DIR, "consolidated_inventory.json")
IGNORED_FILE = os.path.join(DATA_DIR, "ignored_products.json")
PROJECTIONS_FILE = os.path.join(DATA_DIR, "product_projections.json")

# --- VIEW MANAGER ---

class ViewManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Inventarios - Origen Botánico")
        self.root.geometry("1200x750")
        
        try:
            if os.path.exists("app.ico"):
                self.root.iconbitmap("app.ico")
        except:
            pass

        self.container = ttk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        
        self.current_view = None
        self.show_login()

    def clear_view(self):
        if self.current_view:
            self.current_view.destroy()

    def show_login(self):
        self.clear_view()
        self.current_view = LoginView(self.container, self)
        self.current_view.pack(fill="both", expand=True)

    def show_main_menu(self):
        self.clear_view()
        self.current_view = MainMenuView(self.container, self)
        self.current_view.pack(fill="both", expand=True)

    def show_inventory_menu(self):
        self.clear_view()
        self.current_view = InventoryMenuView(self.container, self)
        self.current_view.pack(fill="both", expand=True)

    def show_inventory_balance(self):
        self.clear_view()
        self.current_view = InventoryBalanceView(self.container, self)
        self.current_view.pack(fill="both", expand=True)

    def show_inventory_movements(self):
        self.clear_view()
        self.current_view = InventoryMovementsView(self.container, self)
        self.current_view.pack(fill="both", expand=True)

# --- VIEWS ---

class LoginView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Configure background color (light gray)
        self.configure(bootstyle="light")
        
        # Right side - Login card
        login_container = ttk.Frame(self)
        login_container.place(relx=0.65, rely=0.5, anchor="center")
        
        # White card for login
        card = ttk.Frame(login_container, padding=40, bootstyle="light")
        card.pack()
        
        # Title
        ttk.Label(card, text="Inicio de sesión", font=("Segoe UI", 18, "bold"), 
                 bootstyle="dark").pack(anchor="w", pady=(0, 5))
        
        # Subtitle with link style
        subtitle_frame = ttk.Frame(card, bootstyle="light")
        subtitle_frame.pack(anchor="w", pady=(0, 25))
        ttk.Label(subtitle_frame, text="¿Aún no tienes una cuenta? ", 
                 font=("Segoe UI", 9), bootstyle="secondary").pack(side="left")
        ttk.Label(subtitle_frame, text="Créala aquí", 
                 font=("Segoe UI", 9), bootstyle="info", cursor="hand2").pack(side="left")
        
        # Email field
        ttk.Label(card, text="Usuario/Email", font=("Segoe UI", 9), 
                 bootstyle="dark").pack(anchor="w", pady=(0, 5))
        email_entry = ttk.Entry(card, width=35, font=("Segoe UI", 10))
        email_entry.pack(fill="x", pady=(0, 15))
        email_entry.insert(0, "usuario@ejemplo.com")
        
        # Password field
        pass_label_frame = ttk.Frame(card, bootstyle="light")
        pass_label_frame.pack(fill="x", pady=(0, 5))
        ttk.Label(pass_label_frame, text="Contraseña", font=("Segoe UI", 9), 
                 bootstyle="dark").pack(side="left")
        
        # Show/hide password toggle
        self.show_password = tk.BooleanVar(value=False)
        show_btn = ttk.Label(pass_label_frame, text="👁", font=("Segoe UI", 10), 
                            cursor="hand2", bootstyle="info")
        show_btn.pack(side="right")
        
        password_entry = ttk.Entry(card, width=35, show="•", font=("Segoe UI", 10))
        password_entry.pack(fill="x", pady=(0, 5))
        password_entry.insert(0, "password")
        
        # Forgot password link
        ttk.Label(card, text="¿Olvidaste tu contraseña?", font=("Segoe UI", 9), 
                 bootstyle="info", cursor="hand2").pack(anchor="e", pady=(0, 20))
        
        # Login button
        login_btn = ttk.Button(card, text="Continuar", command=self.login, 
                              bootstyle="info", width=35)
        login_btn.pack(fill="x", ipady=8)
        
        # Version label at bottom
        ttk.Label(self, text="Gestor de Inventarios v1.3.0 - Origen Botánico", 
                 font=("Segoe UI", 8), bootstyle="secondary").pack(side="bottom", pady=10)

    def login(self):
        # Skip authentication for now
        self.controller.show_main_menu()

class MainMenuView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Header
        header = ttk.Frame(self, bootstyle="primary", padding=20)
        header.pack(fill="x")
        ttk.Label(header, text="Menú Principal", font=("Segoe UI", 18, "bold"), bootstyle="inverse-primary").pack(side="left")
        ttk.Button(header, text="Cerrar Sesión", command=self.controller.show_login, bootstyle="danger-outline").pack(side="right")
        
        # Grid of options
        grid_frame = ttk.Frame(self, padding=40)
        grid_frame.pack(fill="both", expand=True)
        
        # Inventory Button (Active)
        btn_inv = ttk.Button(grid_frame, text="📦\n\nINVENTARIOS", command=self.controller.show_inventory_menu, bootstyle="info", width=20)
        btn_inv.grid(row=0, column=0, padx=20, pady=20, ipady=20)
        
        # Placeholders
        ttk.Button(grid_frame, text="💰\n\nFACTURACIÓN", state="disabled", bootstyle="secondary", width=20).grid(row=0, column=1, padx=20, pady=20, ipady=20)
        ttk.Button(grid_frame, text="👥\n\nCLIENTES", state="disabled", bootstyle="secondary", width=20).grid(row=1, column=0, padx=20, pady=20, ipady=20)
        ttk.Button(grid_frame, text="⚙️\n\nCONFIGURACIÓN", state="disabled", bootstyle="secondary", width=20).grid(row=1, column=1, padx=20, pady=20, ipady=20)

class InventoryMenuView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Header
        header = ttk.Frame(self, bootstyle="info", padding=20)
        header.pack(fill="x")
        ttk.Button(header, text="⬅ Volver", command=self.controller.show_main_menu, bootstyle="light-outline").pack(side="left", padx=(0, 20))
        ttk.Label(header, text="Módulo de Inventarios", font=("Segoe UI", 18, "bold"), bootstyle="inverse-info").pack(side="left")
        
        # Options
        content = ttk.Frame(self, padding=50)
        content.pack(fill="both", expand=True)
        
        # Center container
        center = ttk.Frame(content)
        center.place(relx=0.5, rely=0.5, anchor="center")
        
        # Option 1: Saldos
        btn_saldos = ttk.Button(center, text="📊\n\nVER SALDOS\n(Existencias actuales)", command=self.controller.show_inventory_balance, bootstyle="primary", width=30)
        btn_saldos.pack(pady=20, ipady=15)
        
        # Option 2: Movimientos
        btn_movs = ttk.Button(center, text="📋\n\nVER MOVIMIENTOS\n(Entradas y Salidas)", command=self.controller.show_inventory_movements, bootstyle="success", width=30)
        btn_movs.pack(pady=20, ipady=15)

class InventoryBalanceView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Data structures
        self.products = []
        self.ignored_ids = set()
        self.all_warehouses = []
        self.all_companies = []
        
        # Base product codes (products sold to customers)
        self.base_product_codes = ['7416', '7901', '7957', '7210', '7299', '7007', '3012', '3001', '7101', '7008', 'EVO-7702', 'EVO-7701', 'EVO-7703', '3005', '7009']
        
        # All product codes including variants
        self.final_product_codes = ['3001', '3005', '3012', '7007', '7008', '7009', '7701', '7702', '7703', '7101', '7299', '7210', '7416', '7957', '7901']
        
        # UI Variables
        self.search_var = tk.StringVar()
        self.company_var = tk.StringVar(value="Todas")
        self.show_positive_var = tk.BooleanVar(value=True)
        self.show_zero_var = tk.BooleanVar(value=True)
        self.show_negative_var = tk.BooleanVar(value=True)
        self.show_hidden_var = tk.BooleanVar(value=False)
        self.product_type_var = tk.StringVar(value="Todos")
        self.search_job = None

        self.create_layout()
        self.load_data()

    def create_layout(self):
        # ... (existing header code) ...
        # Header
        header = ttk.Frame(self, bootstyle="primary", padding=10)
        header.pack(fill="x")
        ttk.Button(header, text="⬅ Menú Inventarios", command=self.controller.show_inventory_menu, bootstyle="light-outline").pack(side="left", padx=(0, 15))
        ttk.Label(header, text=f"Consulta de Saldos - Datos: {DATA_DIR}", font=("Segoe UI", 12), bootstyle="inverse-primary").pack(side="left")
        
        # Last update label (right side)
        self.last_update_label = ttk.Label(header, text="", font=("Segoe UI", 9), bootstyle="inverse-primary")
        self.last_update_label.pack(side="right", padx=10)
        
        # Main Pane
        main_pane = ttk.Panedwindow(self, orient="horizontal")
        main_pane.pack(fill="both", expand=True)

        # Sidebar
        sidebar = ttk.Frame(main_pane, padding=10, width=250, bootstyle="secondary")
        main_pane.add(sidebar, weight=0)
        
        ttk.Label(sidebar, text="⚙️ Filtros", font=("Segoe UI", 13, "bold"), bootstyle="inverse-secondary").pack(anchor="w", pady=(0, 10))
        
        # Update Button
        self.update_btn = ttk.Button(sidebar, text="🔄 Actualizar desde API", command=self.start_update, bootstyle="success")
        self.update_btn.pack(fill="x", pady=(0, 15))
        
        # Search
        ttk.Label(sidebar, text="Buscar Producto:", bootstyle="inverse-secondary").pack(anchor="w")
        self.search_var.trace_add("write", lambda *args: self.on_search_change())
        ttk.Entry(sidebar, textvariable=self.search_var).pack(fill="x", pady=(0, 10))
        
        ttk.Label(sidebar, text="Empresa:", bootstyle="inverse-secondary").pack(anchor="w")
        self.company_combo = ttk.Combobox(sidebar, textvariable=self.company_var, state="readonly")
        self.company_combo.pack(fill="x", pady=(0, 10))
        self.company_combo.bind("<<ComboboxSelected>>", self.filter_data)
        
        ttk.Label(sidebar, text="Bodegas:", bootstyle="inverse-secondary").pack(anchor="w")
        self.warehouse_list = tk.Listbox(sidebar, selectmode="multiple", height=6)
        self.warehouse_list.pack(fill="x", pady=(0, 10))
        self.warehouse_list.bind("<<ListboxSelect>>", self.filter_data)
        
        ttk.Label(sidebar, text="Estado:", bootstyle="inverse-secondary").pack(anchor="w")
        ttk.Checkbutton(sidebar, text="Positivos", variable=self.show_positive_var, command=self.filter_data, bootstyle="round-toggle-success").pack(anchor="w")
        ttk.Checkbutton(sidebar, text="Ceros", variable=self.show_zero_var, command=self.filter_data, bootstyle="round-toggle-warning").pack(anchor="w")
        ttk.Checkbutton(sidebar, text="Negativos", variable=self.show_negative_var, command=self.filter_data, bootstyle="round-toggle-danger").pack(anchor="w")
        
        ttk.Separator(sidebar).pack(fill="x", pady=10)
        ttk.Label(sidebar, text="Tipo Producto:", bootstyle="inverse-secondary").pack(anchor="w")
        self.product_type_combo = ttk.Combobox(sidebar, textvariable=self.product_type_var, state="readonly", 
                                                values=["Todos", "Producto Base de Venta", "Producto Exento", "Producto Final", "Insumo", "Otros"])
        self.product_type_combo.pack(fill="x", pady=(0, 10))
        self.product_type_combo.bind("<<ComboboxSelected>>", self.on_product_type_change)
        
        ttk.Button(sidebar, text="💾 Exportar Excel", command=self.export_data, bootstyle="info-outline").pack(fill="x", pady=(20, 0))
        ttk.Button(sidebar, text="📈 Configurar Proyecciones", command=self.open_projections_dialog, bootstyle="warning-outline").pack(fill="x", pady=(10, 0))
        ttk.Button(sidebar, text="📅 Saldos Históricos", command=self.ask_historical_date, bootstyle="primary-outline").pack(fill="x", pady=(10, 0))

        # Content
        content_frame = ttk.Frame(main_pane, padding=10)
        main_pane.add(content_frame, weight=1)
        
        # Top Card
        self.top_card = ttk.Frame(content_frame, bootstyle="info")
        self.top_card.pack(fill="x", pady=(0, 10))
        self.total_units_label = ttk.Label(self.top_card, text="Total unidades: 0", font=("Segoe UI", 11, "bold"), bootstyle="inverse-info")
        self.total_units_label.pack(side="left", padx=10, pady=8)
        
        # Notebook
        self.notebook = ttk.Notebook(content_frame, bootstyle="primary")
        self.notebook.pack(fill="both", expand=True)
        self.notebook.bind("<<NotebookTabChanged>>", self.filter_data)
        
        # Detail Tab
        self.tab_detail = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_detail, text="📋 Detalle por Empresa")
        columns_detail = ("company", "code", "name", "warehouse", "quantity")
        self.tree = ttk.Treeview(self.tab_detail, columns=columns_detail, show="headings", selectmode="extended", bootstyle="primary")
        for col, txt, w in zip(columns_detail, ["Empresa", "Código", "Producto", "Bodega", "Existencia"], [120, 80, 300, 150, 80]):
            self.tree.heading(col, text=txt, command=lambda c=col: self.sort_treeview(self.tree, c, False))
            self.tree.column(col, width=w, anchor="center" if col == "quantity" else "w")
        
        y_scroll = ttk.Scrollbar(self.tab_detail, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=y_scroll.set)
        y_scroll.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)
        
        # Consolidated Tab
        self.tab_consolidated = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_consolidated, text="∑ Consolidado Global")
        columns_cons = ("code", "name", "total_quantity")
        self.tree_cons = ttk.Treeview(self.tab_consolidated, columns=columns_cons, show="headings", selectmode="extended", bootstyle="success")
        self.tree_cons.heading("code", text="Código", command=lambda: self.sort_treeview(self.tree_cons, "code", False))
        self.tree_cons.heading("name", text="Producto", command=lambda: self.sort_treeview(self.tree_cons, "name", False))
        self.tree_cons.heading("total_quantity", text="Total Global", command=lambda: self.sort_treeview(self.tree_cons, "total_quantity", False))
        self.tree_cons.column("code", width=100)
        self.tree_cons.column("name", width=400)
        self.tree_cons.column("total_quantity", width=120, anchor="center")
        
        y_scroll_c = ttk.Scrollbar(self.tab_consolidated, orient="vertical", command=self.tree_cons.yview)
        self.tree_cons.configure(yscroll=y_scroll_c.set)
        y_scroll_c.pack(side="right", fill="y")
        self.tree_cons.pack(side="left", fill="both", expand=True)

        # Status Bar
        self.status_label = ttk.Label(self, text="Listo", relief="sunken", anchor="w")
        self.status_label.pack(side="bottom", fill="x")

    def ask_historical_date(self):
        """Dialog to select a past date for historical stock calculation"""
        dialog = tk.Toplevel(self)
        dialog.title("Saldos Históricos")
        dialog.geometry("300x200")
        
        ttk.Label(dialog, text="Seleccione Fecha de Corte:", font=("Segoe UI", 10, "bold")).pack(pady=10)
        
        date_entry = DateEntry(dialog, bootstyle="primary", startdate=datetime.now() - timedelta(days=1))
        date_entry.pack(pady=10)
        
        def on_confirm():
            target_date = date_entry.entry.get()
            dialog.destroy()
            self.calculate_historical_stock(target_date)
            
        ttk.Button(dialog, text="Calcular Saldos", command=on_confirm, bootstyle="success").pack(pady=20)

    def calculate_historical_stock(self, date_str):
        """
        Calculate stock at a specific past date by reversing movements from now back to that date.
        Formula: Historical = Current + Outputs - Inputs (between Target Date and Now)
        """
        try:
            target_date = datetime.strptime(date_str, "%d/%m/%Y")
            now = datetime.now()
            
            if target_date > now:
                messagebox.showerror("Error", "La fecha no puede ser futura.")
                return

            self.status_label.config(text=f"⏳ Calculando saldos al {date_str}...")
            self.update_idletasks()
            
            # 1. Get all movements from Target Date to Now
            from movements import get_consolidated_movements
            from config import get_config
            from auth import get_auth_token
            
            companies = get_config()
            all_movements = []
            
            # Fetch movements for all companies
            for company in companies:
                token = get_auth_token(company["username"], company["access_key"])
                if token:
                    movs = get_consolidated_movements(token, target_date.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d"))
                    all_movements.extend(movs)
            
            # 2. Calculate Adjustments per Product Code
            adjustments = {} # code -> adjustment value
            
            for mov in all_movements:
                code = mov.get("code")
                qty = float(mov.get("quantity", 0))
                mov_type = mov.get("type") # ENTRADA or SALIDA
                
                if code not in adjustments: adjustments[code] = 0
                
                # To go BACK in time:
                # If it was an OUTPUT (Sale), we ADD it back.
                # If it was an INPUT (Purchase), we SUBTRACT it.
                if mov_type == "SALIDA":
                    adjustments[code] += qty
                elif mov_type == "ENTRADA":
                    adjustments[code] -= qty
            
            # 3. Apply adjustments to current stock (in memory only, don't save to file)
            # We need to refresh the view with these temporary values
            
            # Reload original data first to be sure
            self.load_data() 
            
            # Modify self.products in memory
            for p in self.products:
                code = p.get("code")
                if code in adjustments:
                    # Distribute adjustment across warehouses? 
                    # It's hard to know which warehouse the movement came from without more complex logic.
                    # For now, let's add a "Historical Adj" to the first warehouse or a dummy one, 
                    # OR just update the consolidated view which is what matters most.
                    # Actually, let's try to match warehouse if possible.
                    
                    # Simplified: Just update the consolidated view logic.
                    # But filter_data uses self.products.
                    # Let's add a "virtual" warehouse for adjustment if we can't match.
                    pass

            # Better approach: Create a separate "Historical View" or just update the displayed values?
            # Let's update the displayed values in the TreeView directly or modify the data source temporarily.
            
            # Let's modify the data source temporarily.
            count_modified = 0
            for p in self.products:
                code = p.get("code")
                if code in adjustments:
                    adj = adjustments[code]
                    if adj != 0:
                        # Add to the first warehouse found, or "General"
                        if not p.get("warehouses"):
                            p["warehouses"] = [{"name": "Ajuste Histórico", "quantity": 0}]
                        
                        # Just add to the first one for simplicity in consolidated view
                        p["warehouses"][0]["quantity"] += adj
                        count_modified += 1
            
            # Refresh View
            self.filter_data()
            self.top_card.configure(bootstyle="warning")
            self.total_units_label.configure(bootstyle="inverse-warning", text=f"Total unidades (AL {date_str}): {self.format_number(self.calculate_total_units())}")
            self.status_label.config(text=f"✅ Mostrando saldos al {date_str}. (Se reversaron {len(all_movements)} movimientos)")
            
            messagebox.showinfo("Saldos Históricos", f"Se han calculado los saldos al {date_str}.\n\nNota: Se han reversado los movimientos desde hoy hasta esa fecha.\nPara volver a los saldos actuales, haga clic en 'Actualizar desde API' o reinicie.")

        except Exception as e:
            messagebox.showerror("Error", f"Error calculando históricos: {e}")
            import traceback
            traceback.print_exc()

    def calculate_total_units(self):
        total = 0
        for item in self.tree_cons.get_children():
            val = self.tree_cons.item(item)["values"][2]
            total += float(str(val).replace(".", "").replace(",", "."))
        return total

    def validate_and_fix_number(self, original_val, generated_val_str):
        """
        Validates that the generated string representation matches the original numeric value.
        Rules:
        1. If generated is 10x original, divide by 10.
        2. If generated is 0.1x original, multiply by 10.
        3. If any other discrepancy (formatting, extra chars), revert to original.
        4. Preserve exact original value if validation fails.
        """
        try:
            # Normalize decimal separator for comparison
            gen_float = float(generated_val_str.replace(",", "."))
            orig_float = float(original_val)
            
            if orig_float == 0:
                return "0" if gen_float == 0 else str(orig_float).replace(".", ",")
            
            ratio = gen_float / orig_float
            
            # Case 1: 10x larger (e.g. 39516.0 -> 395160)
            if 9.9 <= ratio <= 10.1:
                print(f"DEBUG: Correction 10x detected. Orig: {orig_float}, Gen: {gen_float}. Fixing...")
                return str(gen_float / 10).replace(".", ",")
                
            # Case 2: 10x smaller
            if 0.09 <= ratio <= 0.11:
                print(f"DEBUG: Correction 0.1x detected. Orig: {orig_float}, Gen: {gen_float}. Fixing...")
                return str(gen_float * 10).replace(".", ",")
                
            # Case 3: Exact match (tolerance for float precision)
            if 0.99 <= ratio <= 1.01:
                return generated_val_str
                
            # Case 4: Other discrepancy - Revert to original
            print(f"DEBUG: Mismatch detected. Orig: {orig_float}, Gen: {gen_float}. Reverting to original.")
            return str(original_val).replace(".", ",")
            
        except Exception as e:
            print(f"DEBUG: Validation error: {e}. Reverting to original.")
            return str(original_val).replace(".", ",")

    def export_data(self):
        items = self.tree_cons.get_children()
        if not items: return
        
        # Ask to update projections first
        if messagebox.askyesno("Exportar", "¿Desea revisar/actualizar las proyecciones antes de exportar?"):
            self.open_projections_dialog()
            items = self.tree_cons.get_children()

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        default_name = f"Exportacion_{timestamp}.csv"
        
        file_path = filedialog.asksaveasfilename(initialfile=default_name, defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                with open(file_path, "w", newline="", encoding="utf-8-sig") as f:
                    writer = csv.writer(f, delimiter=";")
                    writer.writerow([
                        "GRUPO", "SKU", "DETALLE", "COLUMNA D", "CONSUMO (PROYECCION)",
                        "COLUMNA F", "STOCK", "COLUMNA H", "COLUMNA I", "COLUMNA J",
                        "DIAS DE STOCK", "FECHA AGOTAMIENTO"
                    ])
                    
                    selected_company = self.company_var.get()
                    selected_warehouses = [self.warehouse_list.get(i) for i in self.warehouse_list.curselection()]
                    if not selected_warehouses: selected_warehouses = self.all_warehouses
                    
                    for item in items:
                        vals = self.tree_cons.item(item)["values"]
                        code = str(vals[0])
                        name = vals[1]
                        
                        # Calculate stock from raw data
                        stock = 0
                        for p in self.products:
                            if p.get("code") == code:
                                if selected_company != "Todas" and p.get("company_name") != selected_company: continue
                                for wh in p.get("warehouses", []):
                                    if wh.get("name", "Unknown") in selected_warehouses:
                                        stock += float(wh.get("quantity", 0))
                        
                        # Projections
                        proj_data = self.projections.get(code, {})
                        projection = float(proj_data.get("projection", 0))
                        
                        dias_stock = 0
                        fecha_str = "-"
                        if projection > 0:
                            dias_stock = stock / projection
                            future_date = datetime.now() + timedelta(days=dias_stock)
                            fecha_str = future_date.strftime("%d/%m/%Y")
                        
                        # Prepare strings with comma decimal
                        stock_str = str(stock).replace(".", ",")
                        dias_str = str(dias_stock).replace(".", ",")
                        
                        # VALIDATE AND FIX
                        final_stock = self.validate_and_fix_number(stock, stock_str)
                        final_dias = self.validate_and_fix_number(dias_stock, dias_str)
                        
                        writer.writerow([
                            "Origen Botanico", code, name, "0", f"{projection:.0f}", "0",
                            final_stock, "0", "0", "0", final_dias, fecha_str
                        ])
                        
                messagebox.showinfo("Exportar", f"Datos exportados correctamente a:\n{os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Error exportando: {e}")

    # --- Helper Methods (Copied from original InventoryApp) ---
    def format_number(self, num):
        try:
            if isinstance(num, (int, float)):
                return f"{num:,.1f}".replace(",", ".")
            return str(num)
        except:
            return str(num)

    def sort_treeview(self, tree, col, reverse):
        items = [(tree.set(item, col), item) for item in tree.get_children('')]
        try:
            items.sort(key=lambda x: float(x[0].replace('.', '').replace(',', '.')), reverse=reverse)
        except:
            items.sort(key=lambda x: str(x[0]).lower(), reverse=reverse)
        for index, (val, item) in enumerate(items):
            tree.move(item, '', index)
        tree.heading(col, command=lambda: self.sort_treeview(tree, col, not reverse))

    def on_product_type_change(self, event=None):
        """Handle product type selection and auto-select Bodega Principal Rionegro for base products"""
        selected_type = self.product_type_var.get()
        
        # If "Producto Base de Venta" is selected, auto-select only "Bodega Principal Rionegro"
        if selected_type == "Producto Base de Venta":
            # Deselect all warehouses first
            self.warehouse_list.selection_clear(0, tk.END)
            
            # Find and select "Bodega Principal Rionegro" specifically
            for i in range(self.warehouse_list.size()):
                warehouse_name = self.warehouse_list.get(i)
                if "RIONEGRO" in warehouse_name.upper() and "PRINCIPAL" in warehouse_name.upper():
                    self.warehouse_list.selection_set(i)
                    break
        
        # Apply filters
        self.filter_data()

    def classify_product(self, code, name=""):
        """
        Classify products into categories:
        - Producto Base de Venta: Base products without 'exento' or 'EX'
        - Producto Exento: Products with 'exento' or 'EX' in name
        - Insumo: Products with 'INSUMO' in code
        - Otros: Everything else
        """
        if not code:
            return "Otros"
        
        code_upper = code.upper()
        name_upper = name.upper() if name else ""
        
        # Check if it's an exempt/EX variant
        if 'EXENTO' in name_upper or '-EX' in name_upper or 'EX-' in name_upper:
            return "Producto Exento"
        
        # Check if it's an input (INSUMO)
        if 'INSUMO' in code_upper:
            # Even if it matches a base code, if it has INSUMO, it's an input
            return "Insumo"
        
        # Check if it's a base product (for sale)
        for base_code in self.base_product_codes:
            if base_code.upper() in code_upper:
                return "Producto Base de Venta"
        
        # Check if it's any other final product
        for final_code in self.final_product_codes:
            if final_code in code_upper:
                return "Producto Final"
        
        return "Otros"

    def load_data(self):
        # ... (Same logic as original load_data)
        if not os.path.exists(DATA_FILE):
            self.status_label.config(text="No hay datos. Actualice desde API.")
            self.last_update_label.config(text="")
            return
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.products = json.load(f)
            
            # Get file modification time
            mod_time = os.path.getmtime(DATA_FILE)
            from datetime import datetime
            last_update = datetime.fromtimestamp(mod_time)
            update_str = last_update.strftime("%d/%m/%Y %H:%M:%S")
            self.last_update_label.config(text=f"🕐 Última actualización: {update_str}")
            
            # Populate filters
            companies = set()
            warehouses = set()  # Using set automatically consolidates duplicate warehouse names
            for p in self.products:
                companies.add(p.get("company_name", "Desconocida"))
                for w in p.get("warehouses", []):
                    # Add warehouse name to set - duplicates across companies are automatically consolidated
                    warehouses.add(w.get("name", "Unknown"))
            
            self.all_companies = sorted(companies)
            self.company_combo["values"] = ["Todas"] + self.all_companies
            
            # Warehouses are already consolidated (unique names only)
            self.all_warehouses = sorted(warehouses)
            self.warehouse_list.delete(0, tk.END)
            for w in self.all_warehouses:
                self.warehouse_list.insert(tk.END, w)
            if not self.warehouse_list.curselection():
                self.warehouse_list.select_set(0, tk.END)
            
            self.filter_data()
            self.load_projections()
            self.status_label.config(text=f"Datos cargados: {len(self.products)} registros.")
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando datos: {e}")

    def load_projections(self):
        self.projections = {}
        if os.path.exists(PROJECTIONS_FILE):
            try:
                with open(PROJECTIONS_FILE, "r", encoding="utf-8") as f:
                    self.projections = json.load(f)
            except:
                pass

    def save_projections(self):
        try:
            with open(PROJECTIONS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.projections, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando proyecciones: {e}")

    def open_projections_dialog(self):
        # Get currently filtered products
        filtered_items = self.tree_cons.get_children()
        products_to_edit = []
        for item in filtered_items:
            vals = self.tree_cons.item(item)["values"]
            code = str(vals[0])
            name = vals[1]
            products_to_edit.append({"code": code, "name": name})
            
        if not products_to_edit:
            messagebox.showwarning("Aviso", "No hay productos en la lista filtrada para configurar.")
            return

        ProjectionsDialog(self, products_to_edit)

    def filter_data(self, *args):
        # ... (Simplified filter logic for brevity, keeping core functionality)
        search_term = self.search_var.get().lower()
        selected_company = self.company_var.get()
        selected_warehouses = [self.warehouse_list.get(i) for i in self.warehouse_list.curselection()]
        if not selected_warehouses: selected_warehouses = self.all_warehouses
        
        show_pos = self.show_positive_var.get()
        show_zero = self.show_zero_var.get()
        show_neg = self.show_negative_var.get()
        prod_type = self.product_type_var.get()

        self.tree.delete(*self.tree.get_children())
        self.tree_cons.delete(*self.tree_cons.get_children())
        
        consolidated = {}
        total_units = 0
        
        for p in self.products:
            # Filters
            if search_term and (search_term not in p.get("code", "").lower() and search_term not in p.get("name", "").lower()):
                continue
            if selected_company != "Todas" and p.get("company_name") != selected_company:
                continue
            if prod_type != "Todos" and self.classify_product(p.get("code"), p.get("name")) != prod_type:
                continue
                
            # Detail View
            for w in p.get("warehouses", []):
                w_name = w.get("name", "Unknown")
                qty = w.get("quantity", 0)
                
                if w_name not in selected_warehouses: continue
                
                stock_ok = False
                if qty > 0 and show_pos: stock_ok = True
                elif qty == 0 and show_zero: stock_ok = True
                elif qty < 0 and show_neg: stock_ok = True
                
                if stock_ok:
                    self.tree.insert("", "end", values=(p.get("company_name"), p.get("code"), p.get("name"), w_name, self.format_number(qty)))
                    total_units += qty
                    
                    # Consolidated logic
                    code = p.get("code")
                    if code:
                        if code not in consolidated: consolidated[code] = {"name": p.get("name"), "qty": 0}
                        consolidated[code]["qty"] += qty

        # Consolidated View
        for code, data in consolidated.items():
            qty = data["qty"]
            stock_ok = False
            if qty > 0 and show_pos: stock_ok = True
            elif qty == 0 and show_zero: stock_ok = True
            elif qty < 0 and show_neg: stock_ok = True
            
            if stock_ok:
                self.tree_cons.insert("", "end", values=(code, data["name"], self.format_number(qty)))

        self.total_units_label.config(text=f"Total unidades: {self.format_number(total_units)}")

    def on_search_change(self, *args):
        if self.search_job: self.after_cancel(self.search_job)
        self.search_job = self.after(300, self.filter_data)

    def start_update(self):
        from loading_dialog import LoadingDialog
        
        self.update_btn.config(state="disabled")
        
        # Create loading dialog
        self.loading_dialog = LoadingDialog(self.winfo_toplevel(), "Actualizando Inventarios")
        
        # Start update in thread
        threading.Thread(target=self.run_update_script, daemon=True).start()

    def run_update_script(self):
        try:
            sys.argv = ["main.py", "--all"]
            from main import main
            
            # Progress callback
            def progress(msg_type, *args):
                if msg_type == "company":
                    current, total, name = args
                    self.after(0, lambda: self.loading_dialog.update_company(current, total, name))
                elif msg_type == "status":
                    status = args[0]
                    self.after(0, lambda: self.loading_dialog.update_status(status))
                elif msg_type == "log":
                    message = args[0]
                    level = args[1] if len(args) > 1 else "info"
                    self.after(0, lambda: self.loading_dialog.add_log(message, level))
            
            # Run main with progress callback
            result = main(progress_callback=progress)
            
            # Store results for each company
            for detail in result.get("details", []):
                company_name = detail["company"]
                status = detail["status"]
                details = detail["details"]
                self.after(0, lambda c=company_name, s=status, d=details: 
                          self.loading_dialog.add_company_result(c, s, d))
            
            self.after(0, lambda r=result: self.on_update_success(r))
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.after(0, lambda: self.on_update_error(str(e)))

    def on_update_success(self, result):
        # Show summary in dialog
        self.loading_dialog.show_summary()
        
        # Re-enable button
        self.update_btn.config(state="normal")
        
        # Update status based on results
        successful = result.get("successful", 0)
        failed = result.get("failed", 0)
        
        if failed == 0:
            self.status_label.config(text=f"✅ {successful} empresas actualizadas correctamente.")
        else:
            self.status_label.config(text=f"⚠️ {successful} empresas OK, {failed} con errores.")
        
        # Reload data
        self.load_data()

    def on_update_error(self, msg):
        self.status_label.config(text="❌ Error en actualización.")
        self.update_btn.config(state="normal")
        messagebox.showerror("Error", f"Problema al actualizar: {msg}")

    def export_data(self):
        items = self.tree_cons.get_children()
        if not items: return
        
        # Ask to update projections first
        if messagebox.askyesno("Exportar", "¿Desea revisar/actualizar las proyecciones antes de exportar?"):
            self.open_projections_dialog()
            # Reload items in case something changed (though projections are separate)
            items = self.tree_cons.get_children()

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                with open(file_path, "w", newline="", encoding="utf-8-sig") as f:
                    writer = csv.writer(f, delimiter=";")
                    # Header
                    writer.writerow([
                        "GRUPO", "SKU", "DETALLE", "CONSUMO MES ANT.", "CONSUMO MES ANT+PROYECCION",
                        "CONSUMO MES ACTUAL", "STOCK", "EN TRANSITO", "DIAS DE INV STOCK", "FECHA"
                    ])
                    
                    for item in items:
                        vals = self.tree_cons.item(item)["values"]
                        code = str(vals[0])
                        name = vals[1]
                        stock = float(str(vals[2]).replace(".", "").replace(",", "."))
                        
                        # Get projections
                        proj_data = self.projections.get(code, {})
                        last_month = float(proj_data.get("last_month", 0))
                        projection = float(proj_data.get("projection", 0))
                        
                        # Calculations
                        consumo_total = last_month + projection
                        dias_stock = 0
                        fecha_str = "-"
                        
                        if consumo_total > 0:
                            dias_stock = stock / consumo_total * 30 # Assuming monthly consumption
                            # Or is it just stock / consumption? The user said "STOCK / CONSUMO MES ANT+PROYECCION"
                            # Usually consumption is monthly. So days = stock / (consumption/30). 
                            # User formula: "DIAS DE ESTOCK PON LOS DIAS QUE NOS DURARA ELINVENTARIO STOCK/ CONSUMO MES ANT +PROYECCION"
                            # If consumption is monthly, then stock/consumption = months. 
                            # If user means "Consumo Mes Ant" is a quantity, then stock/quantity = ratio.
                            # "DIAS DE INV STOCK" implies days. So (Stock / Monthly_Cons) * 30.
                            # Let's assume the user inputs MONTHLY consumption.
                            dias_stock = (stock / consumo_total) * 30
                            
                            future_date = datetime.now() + timedelta(days=dias_stock)
                            fecha_str = future_date.strftime("%d/%m/%Y")
                        
                        writer.writerow([
                            "Origen Botanico",      # GRUPO
                            code,                   # SKU
                            name,                   # DETALLE
                            f"{last_month:.0f}",    # CONSUMO MES ANT.
                            f"{projection:.0f}",    # CONSUMO MES ANT+PROYECCION (Actually user asked for this column to be input? "CONSUMO MES ANT+PROYECCION ME VAS A PREGUNTAR")
                            # Wait, user said: "CONSUMO MES ANT+PROYECCION ME VAS A PREGUNTAR CUAL ES EL CONSUMO DE ESTOS PRODUCTOS"
                            # It seems "CONSUMO MES ANT+PROYECCION" is a single value the user inputs? 
                            # "CONSUMO MES ANT. PON AUTOMATICMANET 0" -> Wait.
                            # "CONSUMO MES ANT. PON AUTOMATICMANET 0 COMSUMO MES ANT+PROYECCION, ME VAS A PREGUNTAR"
                            # Ah, "CONSUMO MES ANT." -> 0.
                            # "CONSUMO MES ANT+PROYECCION" -> User Input.
                            # Let's re-read carefully: "CONSUMO MES ANT. PON AUTOMATICMANET 0"
                            # "COMSUMO MES ANT+PROYECCION, ME VAS A PREGUNTAR CUAL ES EL CONSUMO DE ESTOS PRODUCTOS"
                            # OK. So:
                            # Col 4: "CONSUMO MES ANT." -> Always 0? Or maybe user wants to input it too? 
                            # "CONSUMO MES ANT. PON AUTOMATICMANET 0" seems clear.
                            # Col 5: "CONSUMO MES ANT+PROYECCION" -> This is the one to ask.
                            
                            # Let's adjust logic.
                            "0",                    # CONSUMO MES ANT. (Requested 0)
                            f"{projection:.0f}",    # CONSUMO MES ANT+PROYECCION (This is what we ask)
                            "0",                    # CONSUMO MES ACTUAL (Requested 0)
                            self.format_number(stock), # STOCK
                            "0",                    # EN TRANSITO (Requested 0)
                            f"{dias_stock:.1f}".replace(".", ","), # DIAS DE INV STOCK
                            fecha_str               # FECHA
                        ])
                        
                messagebox.showinfo("Exportar", "Datos exportados correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error exportando: {e}")

class ProjectionsDialog(tk.Toplevel):
    def __init__(self, parent, products):
        super().__init__(parent)
        self.parent = parent
        self.products = products
        self.title("Configurar Proyecciones")
        self.geometry("600x500")
        
        # Header
        ttk.Label(self, text="Ingrese el Consumo (Mes Ant + Proyección)", font=("Segoe UI", 12, "bold")).pack(pady=10)
        ttk.Label(self, text="Este valor se usará para calcular los días de inventario.", font=("Segoe UI", 9)).pack(pady=(0, 10))
        
        # Scrollable Frame
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Entries
        self.entries = {}
        
        # Headers
        ttk.Label(self.scrollable_frame, text="Código", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self.scrollable_frame, text="Producto", font=("Segoe UI", 9, "bold")).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.scrollable_frame, text="Consumo Proyectado", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, padx=5, pady=5)
        
        for i, prod in enumerate(self.products, 1):
            code = prod["code"]
            name = prod["name"]
            
            ttk.Label(self.scrollable_frame, text=code).grid(row=i, column=0, padx=5, pady=2)
            ttk.Label(self.scrollable_frame, text=name[:40] + "..." if len(name)>40 else name).grid(row=i, column=1, padx=5, pady=2)
            
            current_val = self.parent.projections.get(code, {}).get("projection", 0)
            
            entry = ttk.Entry(self.scrollable_frame, width=15)
            entry.insert(0, str(int(current_val)))
            entry.grid(row=i, column=2, padx=5, pady=2)
            
            self.entries[code] = entry
            
        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=10, padx=10)
        
        ttk.Button(btn_frame, text="Guardar", command=self.save, bootstyle="success").pack(side="right", padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.destroy, bootstyle="secondary").pack(side="right", padx=5)
        
    def save(self):
        for code, entry in self.entries.items():
            try:
                val = float(entry.get())
                if code not in self.parent.projections:
                    self.parent.projections[code] = {}
                self.parent.projections[code]["projection"] = val
                # Also set last_month to 0 as requested
                self.parent.projections[code]["last_month"] = 0
            except ValueError:
                pass # Ignore invalid numbers
        
        self.parent.save_projections()
        self.destroy()

class InventoryMovementsView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.mov_doc_types = {
            "FC": tk.BooleanVar(value=True),
            "FV": tk.BooleanVar(value=True),
            "NC": tk.BooleanVar(value=True),
            "ND": tk.BooleanVar(value=True)
        }
        self.mov_product_type = tk.StringVar(value="Todos")
        self.movements_data = []
        self.final_product_codes = ['3001', '3005', '3012', '7007', '7008', '7009', '7701', '7702', '7703', '7101', '7299', '7210', '7416', '7957', '7901']

        self.create_layout()

    def create_layout(self):
        # Header
        header = ttk.Frame(self, bootstyle="success", padding=10)
        header.pack(fill="x")
        ttk.Button(header, text="⬅ Menú Inventarios", command=self.controller.show_inventory_menu, bootstyle="light-outline").pack(side="left", padx=(0, 15))
        ttk.Label(header, text="Consulta de Movimientos", font=("Segoe UI", 12), bootstyle="inverse-success").pack(side="left")

        # Main Container
        self.main_container = ttk.Frame(self, padding=20)
        self.main_container.pack(fill="both", expand=True)
        
        # --- STATE 1: INITIAL FORM ---
        self.init_frame = ttk.Frame(self.main_container)
        # Use pack instead of place for better visibility guarantee
        self.init_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Center content within init_frame
        center_content = ttk.Frame(self.init_frame)
        center_content.place(relx=0.5, rely=0.4, anchor="center")
        
        ttk.Label(center_content, text="Seleccione Rango de Fechas", font=("Segoe UI", 18, "bold")).pack(pady=(0, 20))
        
        # Quick date range buttons
        quick_frame = ttk.LabelFrame(center_content, text="Rangos Rápidos", padding=15)
        quick_frame.pack(fill="x", pady=(0, 20))
        
        btn_frame = ttk.Frame(quick_frame)
        btn_frame.pack()
        
        ttk.Button(btn_frame, text="📅 Últimos 7 días", command=lambda: self.set_quick_range(7), bootstyle="info-outline", width=15).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="📅 Últimos 15 días", command=lambda: self.set_quick_range(15), bootstyle="info-outline", width=15).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(btn_frame, text="📅 Últimos 30 días", command=lambda: self.set_quick_range(30), bootstyle="info-outline", width=15).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(btn_frame, text="📅 Mes Actual", command=self.set_current_month, bootstyle="info-outline", width=15).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="📅 Mes Anterior", command=self.set_previous_month, bootstyle="info-outline", width=15).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(btn_frame, text="📅 Últimos 90 días", command=lambda: self.set_quick_range(90), bootstyle="info-outline", width=15).grid(row=1, column=2, padx=5, pady=5)
        
        # Custom date range
        custom_frame = ttk.LabelFrame(center_content, text="Rango Personalizado", padding=15)
        custom_frame.pack(fill="x", pady=(0, 20))
        
        dates_grid = ttk.Frame(custom_frame)
        dates_grid.pack()
        
        ttk.Label(dates_grid, text="Desde:", font=("Segoe UI", 10)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.date_start = DateEntry(dates_grid, bootstyle="primary", startdate=datetime.now() - timedelta(days=30), width=15)
        self.date_start.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dates_grid, text="Hasta:", font=("Segoe UI", 10)).grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.date_end = DateEntry(dates_grid, bootstyle="primary", startdate=datetime.now(), width=15)
        self.date_end.grid(row=0, column=3, padx=10, pady=5)
        
        # Consult button
        ttk.Button(center_content, text="CONSULTAR MOVIMIENTOS", command=self.start_fetch, bootstyle="success", width=35).pack(pady=20, ipady=12)

        # --- STATE 2: LOADING ---
        self.loading_frame = ttk.Frame(self.main_container)
        
        ttk.Label(self.loading_frame, text="⏳", font=("Segoe UI", 48)).pack(pady=20)
        self.loading_label = ttk.Label(self.loading_frame, text="Iniciando consulta...", font=("Segoe UI", 14))
        self.loading_label.pack(pady=10)
        self.loading_progress = ttk.Progressbar(self.loading_frame, mode="indeterminate", length=400, bootstyle="success-striped")
        self.loading_progress.pack(pady=20)

        # --- STATE 3: RESULTS ---
        self.results_frame = ttk.Frame(self.main_container)
        
        # Filters Bar
        filter_bar = ttk.Labelframe(self.results_frame, text="Filtros Locales", padding=10)
        filter_bar.pack(fill="x", pady=(0, 10))
        
        ttk.Label(filter_bar, text="Tipo Doc:").pack(side="left", padx=5)
        for dtype, var in self.mov_doc_types.items():
            ttk.Checkbutton(filter_bar, text=dtype, variable=var, command=self.display_movements).pack(side="left", padx=2)
            
        ttk.Label(filter_bar, text=" | Tipo Producto:").pack(side="left", padx=10)
        self.mov_prod_combo = ttk.Combobox(filter_bar, textvariable=self.mov_product_type, values=["Todos", "Producto Final", "Insumo", "Otros"], state="readonly", width=15)
        self.mov_prod_combo.pack(side="left", padx=5)
        self.mov_prod_combo.bind("<<ComboboxSelected>>", lambda e: self.display_movements())
        
        ttk.Button(filter_bar, text="Nueva Consulta", command=self.show_init, bootstyle="secondary-outline").pack(side="right", padx=5)
        ttk.Button(filter_bar, text="💾 Exportar", command=self.export_movements, bootstyle="info-outline").pack(side="right", padx=5)

        # Treeview
        columns_mov = ("date", "company", "doc_type", "doc_number", "code", "name", "warehouse", "quantity", "type")
        self.tree_mov = ttk.Treeview(self.results_frame, columns=columns_mov, show="headings", selectmode="extended", bootstyle="info")
        
        headers_mov = {
            "date": "Fecha", "company": "Empresa", "doc_type": "Tipo", "doc_number": "Número",
            "code": "Código", "name": "Producto", "warehouse": "Bodega", "quantity": "Cantidad", "type": "Movimiento"
        }
        widths_mov = {
            "date": 90, "company": 150, "doc_type": 50, "doc_number": 80,
            "code": 80, "name": 250, "warehouse": 120, "quantity": 80, "type": 80
        }
        
        for col in columns_mov:
            self.tree_mov.heading(col, text=headers_mov[col])
            self.tree_mov.column(col, width=widths_mov[col], anchor="center" if col in ["date", "doc_type", "quantity", "type"] else "w")
            
        y_scroll = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.tree_mov.yview)
        self.tree_mov.configure(yscroll=y_scroll.set)
        y_scroll.pack(side="right", fill="y")
        self.tree_mov.pack(side="left", fill="both", expand=True)
        
        self.tree_mov.tag_configure("entrada", foreground="green")
        self.tree_mov.tag_configure("salida", foreground="red")

    def show_init(self):
        self.loading_frame.place_forget()
        self.results_frame.pack_forget()
        # self.init_frame.place(relx=0.5, rely=0.4, anchor="center")
        self.init_frame.pack(expand=True, fill="both", padx=20, pady=20)

    def show_loading(self):
        self.init_frame.pack_forget()
        self.results_frame.pack_forget()
        self.loading_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.loading_progress.start(10)

    def show_results(self):
        self.init_frame.pack_forget()
        self.loading_frame.place_forget()
        self.loading_progress.stop()
        self.results_frame.pack(fill="both", expand=True)

    def set_quick_range(self, days):
        """Set date range to last N days"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        self.date_start.entry.delete(0, tk.END)
        self.date_start.entry.insert(0, start_date.strftime("%d/%m/%Y"))
        self.date_end.entry.delete(0, tk.END)
        self.date_end.entry.insert(0, end_date.strftime("%d/%m/%Y"))

    def set_current_month(self):
        """Set date range to current month"""
        today = datetime.now()
        start_date = today.replace(day=1)
        last_day = calendar.monthrange(today.year, today.month)[1]
        end_date = today.replace(day=last_day)
        self.date_start.entry.delete(0, tk.END)
        self.date_start.entry.insert(0, start_date.strftime("%d/%m/%Y"))
        self.date_end.entry.delete(0, tk.END)
        self.date_end.entry.insert(0, end_date.strftime("%d/%m/%Y"))

    def set_previous_month(self):
        """Set date range to previous month"""
        today = datetime.now()
        first_day_current = today.replace(day=1)
        last_day_previous = first_day_current - timedelta(days=1)
        first_day_previous = last_day_previous.replace(day=1)
        self.date_start.entry.delete(0, tk.END)
        self.date_start.entry.insert(0, first_day_previous.strftime("%d/%m/%Y"))
        self.date_end.entry.delete(0, tk.END)
        self.date_end.entry.insert(0, last_day_previous.strftime("%d/%m/%Y"))

    def start_fetch(self):
        start_date = self.date_start.entry.get()
        end_date = self.date_end.entry.get()
        
        print(f"DEBUG: start_fetch called with dates: {start_date} to {end_date}")
        
        try:
            d1 = datetime.strptime(start_date, "%d/%m/%Y")
            d2 = datetime.strptime(end_date, "%d/%m/%Y")
            if d1 > d2:
                messagebox.showerror("Error", "Fecha inicio mayor a fecha fin")
                return
            api_start = d1.strftime("%Y-%m-%d")
            api_end = d2.strftime("%Y-%m-%d")
        except Exception as e:
            print(f"DEBUG: Date parsing error: {e}")
            messagebox.showerror("Error", "Formato de fecha inválido")
            return

        print("DEBUG: Showing loading screen...")
        self.show_loading()
        self.update_idletasks()  # Force UI update
        threading.Thread(target=self.run_fetch, args=(api_start, api_end), daemon=True).start()

    def run_fetch(self, start, end):
        try:
            from config import get_config
            from auth import get_auth_token
            from movements import get_consolidated_movements
            from concurrent.futures import ThreadPoolExecutor, as_completed
            
            companies = get_config()
            all_movements = []
            
            def update_progress(msg):
                self.after(0, lambda: self.loading_label.config(text=msg))
            
            # Function to process a single company
            def process_company(idx_company_tuple):
                i, company = idx_company_tuple
                update_progress(f"Consultando empresa {i+1}/{len(companies)}: {company['name']}...")
                
                token = get_auth_token(company["username"], company["access_key"])
                if not token:
                    return []
                
                movements = get_consolidated_movements(token, start, end, progress_callback=update_progress)
                for m in movements:
                    m["company"] = company["name"]
                return movements
            
            # Process companies in parallel
            with ThreadPoolExecutor(max_workers=min(4, len(companies))) as executor:
                future_to_company = {
                    executor.submit(process_company, (i, company)): company 
                    for i, company in enumerate(companies)
                }
                
                for future in as_completed(future_to_company):
                    try:
                        movements = future.result()
                        all_movements.extend(movements)
                    except Exception as e:
                        company = future_to_company[future]
                        print(f"Error procesando {company['name']}: {e}")
            
            self.movements_data = all_movements
            self.after(0, self.on_fetch_success)
        except Exception as e:
            print(f"ERROR in run_fetch: {e}")
            import traceback
            traceback.print_exc()
            self.after(0, lambda: self.on_fetch_error(str(e)))

    def on_fetch_success(self):
        self.display_movements()
        self.show_results()

    def on_fetch_error(self, msg):
        self.show_init()
        messagebox.showerror("Error", f"Error consultando API: {msg}")

    def classify_product(self, code):
        if not code: return "Otros"
        code_upper = code.upper()
        if 'INSUMO' in code_upper:
            for final_code in self.final_product_codes:
                if final_code in code_upper: return "Insumo"
            return "Otros"
        for final_code in self.final_product_codes:
            if final_code in code_upper: return "Producto Final"
        return "Otros"

    def display_movements(self):
        self.tree_mov.delete(*self.tree_mov.get_children())
        selected_types = [dtype for dtype, var in self.mov_doc_types.items() if var.get()]
        prod_type_filter = self.mov_product_type.get()
        
        print(f"DEBUG: Displaying movements. Total loaded: {len(self.movements_data)}")
        print(f"DEBUG: Selected types: {selected_types}")
        print(f"DEBUG: Product filter: {prod_type_filter}")
        
        count_displayed = 0
        
        for m in self.movements_data:
            # Doc Type Filter
            is_match = False
            doc_type = m.get("doc_type")
            
            if doc_type == "invoices" and "FV" in selected_types: is_match = True
            elif doc_type == "purchase-invoices" and "FC" in selected_types: is_match = True
            elif doc_type == "credit-notes" and "NC" in selected_types: is_match = True
            elif doc_type == "debit-notes" and "ND" in selected_types: is_match = True
            
            if not is_match: 
                # print(f"DEBUG: Skipping {doc_type} - No match in {selected_types}")
                continue
            
            # Product Type Filter
            if prod_type_filter != "Todos":
                cls = self.classify_product(m.get("code"))
                if cls != prod_type_filter: 
                    # print(f"DEBUG: Skipping {m.get('code')} - Class {cls} != {prod_type_filter}")
                    continue
            
            # Determine Display Type
            display_type = "OTRO"
            if doc_type == "invoices": display_type = "FV"
            elif doc_type == "purchase-invoices": display_type = "FC"
            elif doc_type == "credit-notes": display_type = "NC"
            elif doc_type == "debit-notes": display_type = "ND"

            # Insert
            vals = (
                m.get("date"),
                m.get("company"),
                display_type,
                m.get("doc_number"),
                m.get("code"),
                m.get("name"),
                m.get("warehouse"),
                f"{m.get('quantity'):,.1f}".replace(",", "."),
                m.get("type")
            )
            tag = "entrada" if m.get("type") == "ENTRADA" else "salida"
            self.tree_mov.insert("", "end", values=vals, tags=(tag,))
            count_displayed += 1
            
        print(f"DEBUG: Displayed {count_displayed} movements.")

    def export_movements(self):
        items = self.tree_mov.get_children()
        if not items: return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            with open(file_path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(["Fecha", "Empresa", "Tipo", "Número", "Código", "Producto", "Bodega", "Cantidad", "Movimiento"])
                for item in items:
                    writer.writerow(self.tree_mov.item(item)["values"])
            messagebox.showinfo("Exportar", "Movimientos exportados.")

if __name__ == "__main__":
    root = ttk.Window(themename="flatly")
    app = ViewManager(root)
    root.mainloop()
