# Instructions
To run the Excel API Chatbot project, follow these steps:

### Ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)


### Setup
1. Clone the repository to your local machine.
2. Navigate to the project directory.

### Install Dependencies
Install the required Python packages using pip:
```
pip install -r requirements.txt
```

### Set Up Environment Variables
Create a `.env` file in the root of the project directory and add your OpenAI API key:
```
OPENAI_API_KEY='your_openai_api_key_here'
```

### Start the Backend Server
Run the FastAPI server using the following command:
```
uvicorn app.main:app --reload
```

### Access the API Interface
Open a web browser and navigate to `http://localhost:8000` to interact with the Excel API Chatbot interface.

### Testing
To run the tests for the project, execute the following command:
```
pytest
```
This will run the tests defined in the `tests/` directory and output the results.

### Interacting with the API
You can interact with the API directly using tools like `curl` or Postman. Here are some example endpoints you can use:
- Add a new row: `POST /rows/`
- Get all rows: `GET /rows/`
- Modify a row: `PUT /rows/{row_id}`
- Delete a row: `DELETE /rows/{row_id}`
Replace `{row_id}` with the actual ID of the row you want to modify or delete.

You may also use the SwaggerUI interface by going to localhost:8000/docs for even easier testing.

### Notes
- The Excel file is located at `data/data.xlsx`. Ensure this file exists or the API will attempt to create it when adding the first row.
- There is also a partially functional user interface to access the AI inside index.html, but unfortunately I did not have time to fully incorporate the the logic into a backend API call. The frontend uses JavaScript functions to send messages and interpret responses from the OpenAI API. Make sure that the backend is running for this.
By following these steps, you should be able to run the Excel API Chatbot project successfully.