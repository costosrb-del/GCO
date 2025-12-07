import pandas as pd
from io import BytesIO
from fpdf import FPDF
import datetime

def to_excel(df):
    """
    Converts a DataFrame to an Excel file in memory.
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        
        # Format header
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',
            'border': 1
        })
        
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            
        # Auto-adjust columns
        for column in df:
            column_width = max(df[column].astype(str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            worksheet.set_column(col_idx, col_idx, column_width)
            
    return output.getvalue()

class PDF(FPDF):
    def __init__(self, header_title="Reporte de Inventario - Origen Botánico", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header_title = header_title

    def header(self):
        # Professional Banner
        # Dark Green Background
        self.set_fill_color(24, 60, 48) # #183C30
        self.rect(0, 0, 210, 30, 'F') # Full width banner (A4 width approx 210)
        
        # Title Text
        self.set_font('Arial', 'B', 14) # Slightly smaller to fit multiple lines
        self.set_text_color(255, 255, 255) # White
        self.set_xy(10, 5)
        self.multi_cell(190, 8, self.header_title, 0, 'C')
        self.ln(2)
        
        # Reset colors
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Origen Botánico - Página {self.page_no()}/{{nb}}', 0, 0, 'C')

def to_pdf(df, title="Reporte", filters=None, custom_header=None):
    """
    Converts a DataFrame to a simple PDF report with metadata.
    """
    # Use custom header if provided, otherwise default fallback or title
    pdf_title = custom_header if custom_header else "Reporte de Inventario - Origen Botánico"
    pdf = PDF(header_title=pdf_title)
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', '', 10)
    
    # Metadata Section (Below Banner)
    pdf.set_y(35) # Start below banner
    
    # Sub-Title (The 'title' param) and Date
    pdf.set_font('Arial', 'B', 12)
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pdf.cell(0, 8, f"{title}", 0, 1)
    
    pdf.set_font('Arial', '', 9)
    pdf.cell(0, 6, f"Generado el: {current_time}", 0, 1)
    
    # Filters Section
    if filters:
        pdf.ln(2)
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(0, 6, "Filtros Aplicados:", 0, 1)
        pdf.set_font('Arial', '', 8)
        for key, value in filters.items():
            # Handle list values (like multi-select)
            if isinstance(value, list):
                val_str = ", ".join(value) if value else "Todos"
            else:
                val_str = str(value)
            pdf.cell(0, 5, f"- {key}: {val_str}", 0, 1)
    
    pdf.ln(5)
    
    # Table Header
    pdf.set_font('Arial', 'B', 9)
    pdf.set_fill_color(200, 200, 200) # Light Gray Header
    col_width = pdf.w / (len(df.columns) + 1)
    row_height = 8 # Slightly taller
    
    for col in df.columns:
        pdf.cell(col_width, row_height, str(col), 1, 0, 'C', True)
    pdf.ln()
    
    # Table Data
    pdf.set_font('Arial', '', 8)
    fill = False # Alternating row color
    
    for index, row in df.iterrows():
        # Zebra striping
        if fill:
            pdf.set_fill_color(245, 245, 245)
        else:
            pdf.set_fill_color(255, 255, 255)
            
        for item in row:
            text = str(item)[:25] # Truncate check
            # Use 'F' for fill if fill=True in 4th arg? No, in cell() 7th arg is fill boolean
            pdf.cell(col_width, row_height, text, 1, 0, 'L', True)
            
        pdf.ln()
        fill = not fill # Toggle
        
    return pdf.output(dest='S').encode('latin-1', 'replace')
