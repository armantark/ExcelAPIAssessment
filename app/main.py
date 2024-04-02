from fastapi import FastAPI, HTTPException, Request
import pandas as pd
from .models.excel_models import create_excel_row_model

app = FastAPI()

EXCEL_FILE_PATH = 'data.xlsx'

# Dependency to dynamically create and return the ExcelRow model
def get_excel_row_model():
    # Read the Excel file to get the column names
    df = pd.read_excel(EXCEL_FILE_PATH)
    column_names = df.columns.tolist()
    # Create and return the dynamic model
    return create_excel_row_model(column_names)

# Add a new row to the Excel file
@app.post("/rows/")
async def add_row(request: Request):
    try:
        # Read the Excel file to get the column names
        df = pd.read_excel(EXCEL_FILE_PATH)
        column_names = df.columns.tolist()

        # Create the dynamic model
        ExcelRowModel = create_excel_row_model(column_names)

        # Parse the request body to the dynamic model
        json_data = await request.json()
        row = ExcelRowModel(**json_data)

        # Append the new row data to the DataFrame
        df = df.append(row.dict(), ignore_index=True)

        # Save the updated DataFrame back to the Excel file
        df.to_excel(EXCEL_FILE_PATH, index=False)
        return {"message": "Row added successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get rows from the Excel file
@app.get("/rows/")
async def get_rows():
    # Logic to retrieve rows from Excel file
    pass

# Modify an existing row in the Excel file
@app.put("/rows/{row_id}")
async def modify_row(request: Request):
    # Logic to modify row in Excel file
    pass

# Delete a row from the Excel file
@app.delete("/rows/{row_id}")
async def delete_row(row_id: int):
    # Logic to delete row from Excel file
    pass