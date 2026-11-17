# Search-and-Filter-Microservice
# Description

The Search and Filter Microservice is a Flask-based API that allows applications to search, filter, and sort records contained within a dataset. The microservice receives data through an HTTP POST request, validates the request contents, processes the records according to the provided search criteria, and returns the results as JSON.

The microservice supports:

Searching records using a keyword or search term
Filtering records based on specified field values
Sorting returned records by a selected field in ascending or descending order

This microservice is useful because it centralizes search and filtering functions, so multiple applications can reuse the same service without implementing their own search. Changes and improvements can be made to the microservice independently without modifying the applications that use it.

# Requirements

The following software and libraries are required:

Python 3
Flask
A Python module named search_filter.py
An IDE such as Visual Studio Code, PyCharm, or IDLE

The microservice imports the following functions from search_filter.py:

Python
from search_filter import search_data, filter_data, sort_data

# Installation

Install Flask using pip:

Shell
python -m pip install flask

Ensure that the following files are located in the same project directory:

Plain Text
app.py
search_filter.py

# Communication Contract

The microservice communicates using:

Protocol: HTTP
Method: POST
Endpoint: /search
Port: 5001

Full endpoint:

Plain Text
http://localhost:5001/search

# Requesting Data

Another program can communicate with the microservice by sending an HTTP POST request to:

Plain Text
http://localhost:5001/search
Request Fields
Field	Description	Example
data	List of records to search and process	[{"name":"Laptop"}]
search_term	Keyword to search for within records	"laptop"
filters	Dictionary containing filter conditions	{"category":"IT"}
sort_by	Field used to sort results	"price"
order	Sort order	"ascending"
Example Request Body
JSON
{
"data": [
{
"name": "Laptop",
"category": "IT",
"price": 1200
},
{
"name": "Monitor",
"category": "IT",
"price": 300
}
],
"search_term": "laptop",
"filters": {
"category": "IT"
},
"sort_by": "price",
"order": "ascending"
}

# Example Request Using Python
Python
import requests
 
url = "http://localhost:5001/search"
 
data = {
"data": [
{
"name": "Laptop",
"category": "IT",
"price": 1200
},
{
"name": "Monitor",
"category": "IT",
"price": 300
}
],
"search_term": "laptop",
"filters": {
"category": "IT"
},
"sort_by": "price",
"order": "ascending"
}
 
response = requests.post(url, json=data)

The requesting application sends a JSON payload to the /search endpoint using the POST method.

# Receiving Data

After the request is processed, the microservice returns a JSON response containing the matching records and the total number of results.

The response can be accessed using:

Python
result = response.json()
 
if response.status_code == 200:
print(result["results"])
print(result["total"])
else:
print(result["error"])
Example Successful Response
JSON
{
"results": [
{
"name": "Laptop",
"category": "IT",
"price": 1200
}
],
"total": 1
}

# Response Status Codes
Status Code	Meaning
200	Search, filtering, and sorting completed successfully.
400	Invalid request data, missing required fields, incorrect data types, or processing error.
Example Error Responses

Missing data field:

JSON
{
"error": "Missing required field: data"
}

Invalid data type:

JSON
{
"error": "Data must be a list"
}

Invalid search term:

JSON
{
"error": "Search term must be a string"
}

# How to Run the Microservice

Verify that Python 3 is installed.

Install Flask:

Shell
python -m pip install flask

Open a terminal in the project directory.

Ensure the following files exist:

Plain Text
app.py
search_filter.py
Start the microservice:
Shell
python app.py
The Flask server will start on:
Plain Text
http://127.0.0.1:5001

or

Plain Text
http://localhost:5001

Keep this terminal running while client applications send requests to the service.

# How to Test the Microservice

The microservice can be tested using Python scripts or automated unit tests.

Manual Test Using Python
Python
import requests
 
response = requests.post(
"http://localhost:5001/search",
json={
"data": [
{"name": "Laptop", "category": "IT", "price": 1200},
{"name": "Monitor", "category": "IT", "price": 300}
],
"search_term": "laptop",
"filters": {"category": "IT"},
"sort_by": "price",
"order": "ascending"

# UML Image
<img width="722" height="812" alt="search_and_filter" src="https://github.com/user-attachments/assets/ca33cb4f-2f63-4b1e-a08a-73cdd54269dc" />


}
)
 
print(response.status_code)
print(response.json())
