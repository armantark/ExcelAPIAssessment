from fastapi.testclient import TestClient
from app.main import app
import pandas as pd
import shutil
import os
import pytest

client = TestClient(app)

EXCEL_FILE_PATH = 'data/data.xlsx'
EXCEL_FILE_BACKUP_PATH = 'data/data_backup.xlsx'

def backup_excel_file():
    # Make a backup of the original Excel file
    if os.path.exists(EXCEL_FILE_PATH):
        shutil.copyfile(EXCEL_FILE_PATH, EXCEL_FILE_BACKUP_PATH)

def restore_excel_file():
    # Restore the original Excel file from the backup
    if os.path.exists(EXCEL_FILE_BACKUP_PATH):
        shutil.copyfile(EXCEL_FILE_BACKUP_PATH, EXCEL_FILE_PATH)
        os.remove(EXCEL_FILE_BACKUP_PATH)

def test_add_row():
    # Backup the original Excel file
    backup_excel_file()

    try:
        # Define a sample row data to add
        sample_row_data = {
            "column1": "Sample Data 1",
            "column2": "Sample Data 2",
            # Add other columns as needed
        }

        # Make a POST request to the add_row endpoint
        response = client.post("/rows/", json=sample_row_data)

        # Assert that the response status code is 200 (OK)
        assert response.status_code == 200

        # Assert that the response JSON contains the expected message
        assert response.json() == {"message": "Row added successfully."}

        # Read the Excel file and check if the row was added
        if os.path.exists(EXCEL_FILE_PATH):
            df = pd.read_excel(EXCEL_FILE_PATH)

            # Check that the last row matches the sample data
            assert df.iloc[-1].to_dict() == sample_row_data
        else:
            raise FileNotFoundError(f"Excel file {EXCEL_FILE_PATH} does not exist.")
    finally:
        # Restore the original Excel file
        restore_excel_file()
        

def test_get_rows():
    # Backup the original Excel file
    backup_excel_file()

    try:
        # Make a GET request to the get_rows endpoint
        response = client.get("/rows/")

        # Assert that the response status code is 200 (OK)
        assert response.status_code == 200

        # Read the Excel file directly and compare it to the response
        if os.path.exists(EXCEL_FILE_PATH):
            df = pd.read_excel(EXCEL_FILE_PATH)
            expected_data = df.to_dict(orient='records')

            # Assert that the response data matches the Excel file data
            assert response.json() == expected_data
        else:
            # If the file does not exist, the response should be an empty list
            assert response.json() == []
    finally:
        # Restore the original Excel file
        restore_excel_file()
        

def test_modify_row():
    # Backup the original Excel file
    backup_excel_file()

    try:
        # Define a sample row data to modify
        sample_row_data = {
            "column1": "Modified Data 1",
            "column2": "Modified Data 2",
            # Add other columns as needed
        }

        # Define the row index to modify
        row_id_to_modify = 0  # Assuming we want to modify the first row

        # Make a PUT request to the modify_row endpoint
        response = client.put(f"/rows/{row_id_to_modify}", json=sample_row_data)

        # Assert that the response status code is 200 (OK)
        assert response.status_code == 200

        # Assert that the response JSON contains the expected message
        assert response.json() == {"message": "Row modified successfully."}

        # Read the Excel file and check if the row was modified
        if os.path.exists(EXCEL_FILE_PATH):
            df = pd.read_excel(EXCEL_FILE_PATH)

            # Check that the specified row matches the modified data
            assert df.iloc[row_id_to_modify].to_dict() == sample_row_data
        else:
            raise FileNotFoundError(f"Excel file {EXCEL_FILE_PATH} does not exist.")
    finally:
        # Restore the original Excel file
        restore_excel_file()
        

def test_delete_row():
    # Backup the original Excel file
    backup_excel_file()

    try:
        # Read the current Excel file to determine the last row's index
        if os.path.exists(EXCEL_FILE_PATH):
            df = pd.read_excel(EXCEL_FILE_PATH)

            # If the Excel file is empty, add a row
            if df.empty:
                df = pd.DataFrame([{"column1": "Temporary Data 1", "column2": "Temporary Data 2"}])
                df.to_excel(EXCEL_FILE_PATH, index=False)

            # Now we can be sure there is at least one row to delete
            row_id_to_delete = len(df) - 1

            # Make a DELETE request to the delete_row endpoint
            response = client.delete(f"/rows/{row_id_to_delete}")

            # Assert that the response status code is 200 (OK)
            assert response.status_code == 200

            # Assert that the response JSON contains the expected message
            assert response.json() == {"message": "Row deleted successfully."}

            # Read the Excel file again and check if the row count decreased by 1
            new_df = pd.read_excel(EXCEL_FILE_PATH)
            assert len(new_df) == len(df) - 1

            # Check that the last row is no longer the same if there are still rows left
            if not new_df.empty:
                assert not new_df.iloc[-1].equals(df.iloc[-1])
        else:
            raise FileNotFoundError(f"Excel file {EXCEL_FILE_PATH} does not exist.")
    finally:
        # Restore the original Excel file
        restore_excel_file()