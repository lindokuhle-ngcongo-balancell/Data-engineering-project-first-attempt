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
    def get_drivers(self, season: int):
        url = f"{self.base_url}/{season}/drivers.json"
        response = requests.get(
            url,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    def get_results(self, season: int):
        url = f"{self.base_url}/{season}/results.json"
        response = requests.get(
            url,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
        
client = F1Client(
    "http://api.jolpi.ca/ergast/f1"
)
# data = client.get_season(2025)
# data = client.get_drivers(2025)
data = client.get_results(2025)


print(data)
