from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_add_row():
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