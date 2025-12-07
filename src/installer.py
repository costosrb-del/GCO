import os
import sys
import shutil
from win32com.client import Dispatch
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class InstallerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Instalador - Gestor de Inventarios SIIGO")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Header
        header = tk.Frame(self.root, bg="#007bff", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Instalador Gestor Inventarios", font=("Segoe UI", 16, "bold"), bg="#007bff", fg="white").place(relx=0.5, rely=0.5, anchor="center")
        
        # Content
        self.content = tk.Frame(self.root, padx=20, pady=20)
        self.content.pack(fill="both", expand=True)
        
        tk.Label(self.content, text="Bienvenido al asistente de instalación.", font=("Segoe UI", 12)).pack(pady=(0, 20))
        
        tk.Label(self.content, text="Se instalará la aplicación en:", font=("Segoe UI", 10)).pack(anchor="w")
        
        # Default install path
        self.install_path = os.path.join(os.environ['PUBLIC'], 'GestorInventarioSiigo')
        
        self.path_var = tk.StringVar(value=self.install_path)
        tk.Entry(self.content, textvariable=self.path_var, width=50, state="readonly").pack(pady=(5, 20))
        
        # Options
        self.desktop_shortcut = tk.BooleanVar(value=True)
        tk.Checkbutton(self.content, text="Crear acceso directo en Escritorio", variable=self.desktop_shortcut).pack(anchor="w")
        
        self.start_menu_shortcut = tk.BooleanVar(value=True)
        tk.Checkbutton(self.content, text="Crear acceso directo en Menú Inicio", variable=self.start_menu_shortcut).pack(anchor="w")
        
        # Progress
        self.progress_frame = tk.Frame(self.content)
        self.status_label = tk.Label(self.progress_frame, text="Listo para instalar...", font=("Segoe UI", 9))
        self.status_label.pack(anchor="w")
        self.progress = ttk.Progressbar(self.progress_frame, mode='determinate', length=400)
        self.progress.pack(pady=5)
        
        # Buttons
        self.btn_frame = tk.Frame(self.root, pady=20)
        self.btn_frame.pack(side="bottom", fill="x")
        
        self.install_btn = tk.Button(self.btn_frame, text="INSTALAR", command=self.start_install, 
                                   bg="#28a745", fg="white", font=("Segoe UI", 10, "bold"), padx=20, pady=5, relief="flat")
        self.install_btn.pack()
        
    def start_install(self):
        self.install_btn.config(state="disabled")
        self.progress_frame.pack(pady=20)
        threading.Thread(target=self.run_install, daemon=True).start()
        
    def run_install(self):
        try:
            target_dir = self.path_var.get()
            
            # 1. Create Directory
            self.update_status("Creando carpetas...", 10)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
                
            # 2. Copy Files
            files_to_copy = [
                "GestorInventarioSiigo.exe",
                ".env",
                "README.md",
                "GUIA_INSTALACION_NUEVO_PC.md",
                "app.ico"
            ]
            
            total_files = len(files_to_copy)
            for i, filename in enumerate(files_to_copy):
                self.update_status(f"Copiando {filename}...", 20 + (i / total_files * 50))
                src = resource_path(filename)
                dst = os.path.join(target_dir, filename)
                
                if os.path.exists(src):
                    shutil.copy2(src, dst)
                else:
                    # If file doesn't exist in bundle (e.g. testing), skip or warn
                    print(f"Warning: {filename} not found in bundle")
            
            # 3. Create Shortcuts
            exe_path = os.path.join(target_dir, "GestorInventarioSiigo.exe")
            icon_path = os.path.join(target_dir, "app.ico")
            
            if self.desktop_shortcut.get():
                self.update_status("Creando acceso directo en Escritorio...", 80)
                desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
                path = os.path.join(desktop, "Gestor Inventarios SIIGO.lnk")
                self.create_shortcut(path, exe_path, target_dir, icon_path)
                
            if self.start_menu_shortcut.get():
                self.update_status("Creando acceso directo en Menú Inicio...", 90)
                start_menu = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs')
                path = os.path.join(start_menu, "Gestor Inventarios SIIGO.lnk")
                self.create_shortcut(path, exe_path, target_dir, icon_path)
            
            self.update_status("¡Instalación Completada!", 100)
            messagebox.showinfo("Éxito", "La aplicación se instaló correctamente.")
            self.root.quit()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la instalación:\n{str(e)}")
            self.root.quit()

    def create_shortcut(self, path, target, work_dir, icon):
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = work_dir
        if os.path.exists(icon):
            shortcut.IconLocation = icon
        shortcut.save()

    def update_status(self, text, value):
        self.status_label.config(text=text)
        self.progress['value'] = value
        self.root.update_idletasks()
        time.sleep(0.2)

if __name__ == "__main__":
    app = InstallerApp()
    app.root.mainloop()
