"""
Helper script to create testdata.xlsx with sample test data
Run this once to generate the Excel file
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

def create_testdata_excel():
    """Create testdata.xlsx with sample W3Schools dropdown test data"""
    wb = Workbook()
    ws = wb.active
    ws.title = "data"
    
    # Define headers
    headers = ["test_name", "url", "dropdown_value", "dropdown_text", "expected_selected_text"]
    ws.append(headers)
    
    # Style header row
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
    
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
    
    # Save the workbook
    wb.save("testdata.xlsx")
    print("✓ testdata.xlsx created successfully with sample data")

if __name__ == "__main__":
    create_testdata_excel()
