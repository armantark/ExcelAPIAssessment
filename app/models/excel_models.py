from pydantic import create_model

def create_excel_row_model(column_names: list):
    fields = {name: (str, ...) for name in column_names}  # Assuming all columns are of type str for simplicity
    return create_model('ExcelRow', **fields)
