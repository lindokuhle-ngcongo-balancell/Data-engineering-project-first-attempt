import requests

url = "http://api.jolpi.ca/ergast/f1/2025.json"
response = requests.get(url, timeout=30)
print("Status Code:", response.status_code)
response.raise_for_status()
data = response.json()
mr_data = data["MRData"]
print("Total Races:", mr_data["total"])
races = mr_data["RaceTable"]["Races"]
for race in races: 
    print(
        race["round"],
        race["raceName"],
        race["date"]
    )
print(data)