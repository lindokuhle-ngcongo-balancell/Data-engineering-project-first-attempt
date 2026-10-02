Our current code is a one-off script 
requests.get(url)

where we want:

                F1 API
                   │
                   ▼
             ┌───────────┐
             │ F1 Client │
             └─────┬─────┘
                   │
                   ▼
             Raw Response
                   │
                   ▼
             Raw Storage

The API client should be respoble for communicating with the external API

* it should not be responsible for :
    * creating database tables
    * calculating business metrics
    * building Power Bi reports
    * transforming everything into analytical models

* Thats separation of responsibilities again.
* A simple first version could look like:

            import requests

            class F1Client:

                def __init__(self, base_url: str):
                    self.base_url = base_url

                def get_season(self, season: int):
                    url = f"{self.base_url}/{season}.json"

                    response = requests.get(
                        url,
                        timeout=30
                    )

                    response.raise_for_status()

                    return response.json()

* Then: 

        client = F1Client(
            "https://api.jolpi.ca/ergast/f1"
        )

        data = client.get_season(2024)

        print(data)


            F1Client
            │
            ├── Connect to API
            ├── Set timeout
            ├── Handle temporary failures
            ├── Retry failed requests
            ├── Handle pagination
            └── Return the requested data