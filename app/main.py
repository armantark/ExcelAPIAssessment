from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from .models.excel_models import create_excel_row_model
from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=openai_key)

app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

EXCEL_FILE_PATH = 'data/data.xlsx'

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
        # Parse the request body to a dictionary
        json_data = await request.json()
        
        # Check if the Excel file exists and has data
        try:
            df = pd.read_excel(EXCEL_FILE_PATH)
            # If the file is empty, create a DataFrame with the keys of the JSON data as columns
            if df.empty:
                df = pd.DataFrame(columns=json_data.keys())
        except FileNotFoundError:
            # If the file does not exist, create a new DataFrame
            df = pd.DataFrame(columns=json_data.keys())
        except ValueError:
            # If the file exists but is empty, create a DataFrame with the keys of the JSON data as columns
            df = pd.DataFrame(columns=json_data.keys())

        # Create a DataFrame from the new row data
        new_row_df = pd.DataFrame([json_data])

        # Concatenate the new row DataFrame to the existing DataFrame
        df = pd.concat([df, new_row_df], ignore_index=True)

        # Save the updated DataFrame back to the Excel file
        df.to_excel(EXCEL_FILE_PATH, index=False)
        return {"message": "Row added successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get rows from the Excel file
@app.get("/rows/")
async def get_rows():
    try:
        # Attempt to read the Excel file
        try:
            df = pd.read_excel(EXCEL_FILE_PATH)
        except FileNotFoundError:
            # If the file does not exist, return an empty list
            return []
        except ValueError:
            # If the file is empty, return an empty list
            return []

        # Convert the DataFrame to a list of row dictionaries
        rows = df.to_dict(orient='records')

        # Return the list of rows
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Modify an existing row in the Excel file
@app.put("/rows/{row_id}")
async def modify_row(row_id: int, request: Request):
    try:
        # Parse the request body to a dictionary
        json_data = await request.json()

        # Read the existing Excel file
        df = pd.read_excel(EXCEL_FILE_PATH)

        # Check if the row_id is valid
        if row_id < 0 or row_id >= len(df):
            raise HTTPException(status_code=404, detail="Row not found")

        # Update the row with the new data
        for key, value in json_data.items():
            df.at[row_id, key] = value

        # Save the updated DataFrame back to the Excel file
        df.to_excel(EXCEL_FILE_PATH, index=False)
        return {"message": "Row modified successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Delete a row from the Excel file
@app.delete("/rows/{row_id}")
async def delete_row(row_id: int):
    try:
        # Read the existing Excel file
        df = pd.read_excel(EXCEL_FILE_PATH)

        # Check if the row_id is valid
        if row_id < 0 or row_id >= len(df):
            raise HTTPException(status_code=404, detail="Row not found")

        # Delete the row
        df = df.drop(df.index[row_id])

        # Save the updated DataFrame back to the Excel file
        df.to_excel(EXCEL_FILE_PATH, index=False)
        return {"message": "Row deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/openai_chat/")
async def openai_chat(request: Request):
    request_data = await request.json()
    prompt = request_data.get("prompt")

    if not prompt:
        raise HTTPException(status_code=400, detail="No prompt provided")

    try:
        openai_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                "role": "system",
                "content": "\"Your goal is to parse a user's natural language input and determine the appropriate backend API call to make. You should reply only with the specific action and data needed for the backend call, formatted as a JSON object that represents the API request. \n\nFor example, if a user says \"I want to add a new row with the following data: Name John Doe, Age 30\", you should reply with:\n{\n  \"action\": \"add_row\",\n  \"data\": {\n    \"col1\": \"John Doe\",\n    \"col2\": \"30\"\n  }\n}\n\nHere is the signature of each backend endpoint to help guide you:\n# Add a new row to the Excel file\n@app.post(\"/rows/\")\nasync def add_row(request: Request):\n\n# Get rows from the Excel file\n@app.get(\"/rows/\")\nasync def get_rows():\n\n# Modify an existing row in the Excel file\n@app.put(\"/rows/{row_id}\")\nasync def modify_row(row_id: int, request: Request):\n\n# Delete a row from the Excel file\n@app.delete(\"/rows/{row_id}\")\nasync def delete_row(row_id: int):"
                },
                {
                "role": "user",
                "content": f"{prompt}"
                }
            ],
            temperature=0.3,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
        # Extract the text from the OpenAI response
        generated_text = openai_response.choices[0].message.content if openai_response.choices else ''
        return {"response": generated_text}
    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=str(e))