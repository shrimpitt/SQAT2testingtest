from openpyxl import Workbook

# Создаем книгу
wb = Workbook()
ws = wb.active
ws.title = 'data'

# Заголовки
ws.append(['test_name', 'url', 'dropdown_value', 'dropdown_text', 'expected_selected_text'])

# Тестовые данные
ws.append([
    'w3schools_dropdown_test',
    'https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_select',
    'saab',
    'Volvo',
    'Saab'
])

# Ширина колонок
widths = [20, 70, 15, 15, 20]
for i, width in enumerate(widths, 1):
    ws.column_dimensions[chr(64 + i)].width = width

# Сохраняем
wb.save('testdata.xlsx')
print('testdata.xlsx создан успешно!')
