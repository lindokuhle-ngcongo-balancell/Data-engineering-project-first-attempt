<h1>API & Data Acquisition</h1>

<h3>Understanding API's and HTTP</h3>

* We're now moving from architecture planning into the technical part of the project. Before writing the ingestion program, you need how our Python application comminicate with the data source.

**Our First milestone** is to Retrieve data from the API and save the original response as a JSON file.

            Jolpica F1 API
            External data source
            HTTP GET request
            Python API client
            Sends request and receives response
            JSON response
            Raw JSON storage
            Original API response preserved

1. What is an API?
* An API (Application Programming Interface) allows two software systems to comminicate through a defined interface.

* In our Project
    * Client: Our Python application
    * Server: The Jolpica F1 API
    * Request: A message asking the server for particalar data.
    * Response: The data and status information returned by server.
* for example, our application might request the 2024 season's rae schedule.
* An API is not necessarily a database. It is an interface through which we access data or functionality.
#
2. Understanding HTTP
- HTTP is a comminication protocol commonly used by REST APIS
- The main HTTP methods include:

            Method          Purpose                 Example
            GET             Retrieve data           Get race results
            POST            Submit data             Create a resource
            PUT             Replace a resource      Replace a configuration
            PATCH           Partially update data   Update a record
            DELETE          Remove a resource       Delete a resource

* For our initial data acqusion, we'll primarily use GET because we're retrieving data
* An HTTP request can be understood through four parts:
    * URL: The location of the resource
    * Method: What we want to do.
    * Headers: Additional information about the request
    * Parameters: Optional filters or pagination instructions
- The server returns as HTTP status code, headers and potentially a response body.
#
3. Understanding endpoints JSON
- An Endpoint is a specitic API URL used to access a resource.
- for example, Jolpica uses an Ergast-compatible API structure. A season schediule can be request using an endpoint like 
    * https://api.jolpi.ca/ergast/f1/2024.json
- Other examples of resources include:
    * /2024/drivers.json
    * /2024/contructors.json
    * /2024/1/results.json
    * /2024/1/qualifing.json
* the URL structure tells the API which season, reace or resource you're requesting.
* The response is commonly formatted as JSON(JavaScript Object Notation), a text format for representing structured data.

- Example of a simplified rsce response:

            {
                "season": "2024",
                "round": "1",
                "raceName": "Bahrain Grand Prix",
                "Circuit": {
                    "circuitName": "Bahrain International Circuit"
                }
            }


- Notice that JSON supports.
    * Objects, represented by curly {}
    * Arrays, respresented by squre []
    * key-value pairs
    * Nested Objects and arrays
- Real API responses have additional metadata may wrap the data inside several nested objects. Our ingestion code must account for that structure.
#
4. HTTP status code
- A successful request doesn't always mean the data you expected. We need to check the status code.

        Status      Meaning                 Typical handling
        200         OK                      Process the response
        400         Bad Request             Check request parameters
        401         Unauthorized            Check authentication
        403         Forbidden               Check permissions
        404         Not Found               Check the endpoint or resource
        429         Too Many Requests       Respect rate limits; retry appropriately
        500         Internal Server Error   Consider retrying
        503         Service Unavailable     Consider retrying

* For our ingestion system, this matters because an API can fail temporarily. We should distinguish a temporary failure from a request that will continue to fail until we fix it.
#
5. Your first API request in Python
* We'll use python's requests library to make an HTTP request
* First, create a project folder and virtual environment:
    * mkdir f1-data-platforn
    * cd f1-data-platforn
    * touch first_request.py
    * python3 -m venv .venv
    * source .venv/bin/activate
    * pip install requests

* edit first_request.py

        import requests

        url = "https://api.jolpi.ca/ergast/f1/2024.json"

        response = requests.get(url, timeout=30)

        print("Status code:", response.status_code)

        response.raise_for_status()

        data = response.json()

        print(data)

* Run it
    * python first_request.py
* Let's understand the important lines.
    * requests.get(...) sends an HTTP GET request.
    * time=30 prevents the request from wating indefinitely
    * response.status_code give us the HTTP status code
    * raise_for_status() raises an exception for unsucceeful HTTP responses
    * response.json() parses the response body into Python objects, typically dictionaries and lists
* The important distinction is that JSON is the response format, while a Python dictionary or list is how the parsed data is represented is your program .
#
6. Inspect the response structure
- Printing the entire response can become inconvenient when the dataset grows. Instead, inspect the nested structure

- And the following the after data = response.json():

        mr_data = data["MRData"]
        
        print("Total races:", mr_data["total"])

        races = mr_data["RaceTable"]["Races"]

        for race in races:
            print(
                race["round"],
                race["raceName"],
                race["date"]
            )