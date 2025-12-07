import tkinter as tk
import ttkbootstrap as ttk
from gui import InventoryApp

def main():
    root = ttk.Window(themename="flatly")
    root.withdraw()  # hide the main window
    app = InventoryApp(root)
    # Load data (already called in __init__)
    # After loading, print number of items in consolidated view
    count = len(app.tree_cons.get_children())
    print(f"Consolidated view item count: {count}")
    # Optionally, print total units label text
    print(f"Total units label: {app.total_units_label.cget('text')}")
    root.destroy()

if __name__ == "__main__":
    main()
