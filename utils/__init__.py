"""
Initialize Excel file with test data automatically when imported
"""
from pathlib import Path

def ensure_testdata_excel():
    """Create testdata.xlsx if it doesn't exist"""
    try:
        from openpyxl import Workbook
    except ImportError:
        # openpyxl not installed yet, will be installed with requirements.txt
        return
    
    excel_path = Path(__file__).parent.parent / "testdata.xlsx"
    
    if excel_path.exists():
        return
    
    wb = Workbook()
    ws = wb.active
    ws.title = "data"
    
    # Define headers
    headers = ["test_name", "url", "dropdown_value", "dropdown_text", "expected_selected_text"]
    ws.append(headers)
    
    # Add sample test data for W3Schools dropdown
    sample_data = [
        [
            "w3schools_dropdown_test",
            "https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_select",
            "saab",
            "Volvo",
            "Saab"
        ]
    ]
    
    for row_data in sample_data:
        ws.append(row_data)
    
    # Auto-adjust column widths
    column_widths = [20, 70, 15, 15, 20]
    for i, width in enumerate(column_widths, 1):
        ws.column_dimensions[chr(64 + i)].width = width
    
    wb.save(str(excel_path))

# Auto-create on import
ensure_testdata_excel()
