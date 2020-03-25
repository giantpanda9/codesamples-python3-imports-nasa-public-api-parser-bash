import requests
from datetime import date, timedelta

class parseNASA():
	def __init__(self):
		self.dateDelta = 7
		self.dateToday = date.today()
		self.previousDate = self.dateToday - timedelta(days=self.dateDelta)
		self.APIKey = "DEMO_KEY"
	def getAPIUrl(self):
		return f"https://api.nasa.gov/neo/rest/v1/feed?start_date={self.previousDate}&end_date={self.dateToday}&api_key={self.APIKey}"
	def getResponse(self):
		APIUrl = self.getAPIUrl()
		response = requests.get(APIUrl)
		returned = []
		if response.status_code != 200:
			return []
		responseJSON = response.json()
		currentDelta = timedelta(days=1)
		currentDate = self.previousDate
		while currentDate <= self.dateToday:
			responseJSONCurrent = responseJSON["near_earth_objects"][str(currentDate)]
			for nasaItem in responseJSONCurrent:
				returnedItem = {}
				returnedItem["name"] = nasaItem["name"]
				returnedItem["fromDate"] = str(currentDate)
				returnedItem["diameterEstMin"] = nasaItem["estimated_diameter"]["kilometers"]["estimated_diameter_min"] or 0
				returnedItem["diameterEstMax"] = nasaItem["estimated_diameter"]["kilometers"]["estimated_diameter_max"] or 0
				returnedItem["hazardous"] = "Yes" if nasaItem["is_potentially_hazardous_asteroid"] else "No"
				returnedItem["cameCloser"] = nasaItem["close_approach_data"][0]["close_approach_date"]
				returnedItem["details"] = nasaItem["nasa_jpl_url"]
				returned.append(returnedItem)
			currentDate += currentDelta
		return returned
			
def main():
	parseNASAInstance = parseNASA()
	APIResponse = parseNASAInstance.getResponse()
	if len(APIResponse) > 0:
		for item in APIResponse:
			print(f'Asteroid Name: {item["name"]}')
			print(f'Report Date: {item["fromDate"]}')
			print(f'Diameter Min (Km): {item["diameterEstMin"]}')
			print(f'Diameter Max (Km): {item["diameterEstMax"]}')
			print(f'Destroys Earth?: {item["hazardous"]}')
			print(f'Close Encounter Date: {item["cameCloser"]}')
			print(f'Details: {item["details"]}')
	else:
		print("NASA API is not available or available limit is exceeded. Please try again later.")
if __name__=='__main__': main()

