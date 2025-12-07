import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import scrolledtext

class LoadingDialog:
    def __init__(self, parent, title="Actualizando Inventarios"):
        self.dialog = ttk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("600x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center window
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"600x500+{x}+{y}")
        
        self.create_widgets()
        self.summary_data = []
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Actualizando Inventarios desde Siigo API", 
                                font=("Segoe UI", 14, "bold"), bootstyle="primary")
        title_label.pack(pady=(0, 20))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode="indeterminate", length=500, bootstyle="success-striped")
        self.progress.pack(pady=(0, 15))
        self.progress.start(10)
        
        # Current company label
        self.company_label = ttk.Label(main_frame, text="Iniciando...", font=("Segoe UI", 11, "bold"))
        self.company_label.pack(pady=(0, 5))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="", font=("Segoe UI", 10))
        self.status_label.pack(pady=(0, 15))
        
        # Log frame
        log_frame = ttk.Labelframe(main_frame, text="Detalles del Proceso", padding=10)
        log_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Scrolled text for log
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, wrap=tk.WORD, 
                                                   font=("Consolas", 9), state="disabled")
        self.log_text.pack(fill="both", expand=True)
        
        # Summary frame (hidden initially)
        self.summary_frame = ttk.Labelframe(main_frame, text="Resumen de Actualizacion", padding=15)
        self.summary_text = scrolledtext.ScrolledText(self.summary_frame, height=10, wrap=tk.WORD,
                                                       font=("Segoe UI", 9), state="disabled")
        self.summary_text.pack(fill="both", expand=True)
        
        # Close button (hidden initially)
        self.close_btn = ttk.Button(main_frame, text="Cerrar", command=self.close, bootstyle="primary")
        
    def update_company(self, current, total, company_name):
        """Update current company being processed"""
        self.company_label.config(text=f"Empresa {current}/{total}: {company_name}")
        
    def update_status(self, status):
        """Update current operation status"""
        self.status_label.config(text=status)
        
    def add_log(self, message, level="info"):
        """Add message to log"""
        self.log_text.config(state="normal")
        
        # Add timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Color coding
        if level == "error":
            prefix = "[ERROR]"
        elif level == "warning":
            prefix = "[WARN]"
        elif level == "success":
            prefix = "[OK]"
        else:
            prefix = "[INFO]"
            
        self.log_text.insert(tk.END, f"{timestamp} {prefix} {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
        self.dialog.update_idletasks()
        
    def add_company_result(self, company_name, status, details):
        """Store company result for summary"""
        self.summary_data.append({
            "company": company_name,
            "status": status,
            "details": details
        })
        
    def show_summary(self):
        """Show final summary and hide progress elements"""
        self.progress.stop()
        self.progress.pack_forget()
        self.company_label.pack_forget()
        self.status_label.pack_forget()
        
        # Hide log frame to make summary more visible
        for widget in self.dialog.winfo_children():
            for child in widget.winfo_children():
                if isinstance(child, ttk.Labelframe) and child.cget("text") == "Detalles del Proceso":
                    child.pack_forget()
        
        # Build summary text
        summary_lines = []
        summary_lines.append("=" * 60)
        summary_lines.append("RESUMEN DE ACTUALIZACION".center(60))
        summary_lines.append("=" * 60)
        summary_lines.append("")
        
        successful = 0
        failed = 0
        total_products = 0
        failed_companies = []
        
        for result in self.summary_data:
            company = result["company"]
            status = result["status"]
            details = result["details"]
            
            if status == "success":
                successful += 1
                products = details.get("products", 0)
                total_products += products
                summary_lines.append(f"✓ {company}")
                summary_lines.append(f"  {products} productos actualizados")
            else:
                failed += 1
                failed_companies.append(company)
                error = details.get("error", "Error desconocido")
                message = details.get("message", "")
                summary_lines.append(f"✗ {company}")
                summary_lines.append(f"  Error: {error}")
                if message:
                    summary_lines.append(f"  {message}")
            
            summary_lines.append("")
        
        summary_lines.append("=" * 60)
        summary_lines.append(f"Total: {successful}/{len(self.summary_data)} empresas actualizadas")
        if successful > 0:
            summary_lines.append(f"Productos totales: {total_products}")
        summary_lines.append("=" * 60)
        
        # Add warning if some failed
        if failed > 0:
            summary_lines.append("")
            summary_lines.append("⚠️ ADVERTENCIA:")
            for company in failed_companies:
                summary_lines.append(f"Los datos de '{company}' NO estan actualizados.")
            summary_lines.append("Verifique si necesita esa informacion antes de")
            summary_lines.append("tomar decisiones basadas en estos datos.")
        
        # Display summary
        self.summary_text.config(state="normal")
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert("1.0", "\n".join(summary_lines))
        self.summary_text.config(state="disabled")
        
        # Show summary frame and close button
        self.summary_frame.pack(fill="both", expand=True, pady=(0, 15))
        self.close_btn.pack()
        
        # Force update to ensure visibility
        self.dialog.update_idletasks()
        
    def close(self):
        """Close the dialog"""
        self.dialog.destroy()
        
    def get_result(self):
        """Get summary data"""
        return {
            "total": len(self.summary_data),
            "successful": sum(1 for r in self.summary_data if r["status"] == "success"),
            "failed": sum(1 for r in self.summary_data if r["status"] == "error"),
            "details": self.summary_data
        }
