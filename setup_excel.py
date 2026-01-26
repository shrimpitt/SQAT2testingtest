"""Script to manually create testdata.xlsx"""
import sys
sys.path.insert(0, 'c:\\Users\\bagym\\Documents\\SQAT2testingtest')

from openpyxl import Workbook
from pathlib import Path

wb = Workbook()
ws = wb.active
ws.title = "data"

# Headers
headers = ["test_name", "url", "dropdown_value", "dropdown_text", "expected_selected_text"]
ws.append(headers)

# Sample data
sample = [
    "w3schools_dropdown_test",
    "https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_select",
    "saab",
    "Volvo",
    "Saab"
]
ws.append(sample)

# Column widths
widths = [20, 70, 15, 15, 20]
for i, width in enumerate(widths, 1):
    ws.column_dimensions[chr(64 + i)].width = width

# Save
wb.save('c:\\Users\\bagym\\Documents\\SQAT2testingtest\\testdata.xlsx')
print("✓ testdata.xlsx created")
