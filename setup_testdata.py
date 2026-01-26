#!/usr/bin/env python
"""
Setup script to create testdata.xlsx with sample test data
Run this after installing requirements
"""

def create_test_data_excel():
    """Create testdata.xlsx with sample data"""
    try:
        from openpyxl import Workbook
    except ImportError:
        print("ERROR: openpyxl not installed. Run: pip install openpyxl")
        return False
    
    from pathlib import Path
    
    excel_path = Path(__file__).parent / "testdata.xlsx"
    
    # Create workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "data"
    
    # Headers
    headers = ["test_name", "url", "dropdown_value", "dropdown_text", "expected_selected_text"]
    ws.append(headers)
    
    # Sample row for W3Schools dropdown
    ws.append([
        "w3schools_dropdown_test",
        "https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_select",
        "saab",
        "Volvo",
        "Saab"
    ])
    
    # Set column widths
    widths = [20, 70, 15, 15, 20]
    for i, width in enumerate(widths, 1):
        ws.column_dimensions[chr(64 + i)].width = width
    
    # Save file
    wb.save(excel_path)
    print(f"✓ Created {excel_path} with sample test data")
    return True

if __name__ == "__main__":
    create_test_data_excel()
