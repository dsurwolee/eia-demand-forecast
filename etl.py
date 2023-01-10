from requests.auth import HTTPBasicAuth
import json
import requests
import pandas as pd

# (TODO)
# 0. Find the best way to load data. https://www.eia.gov/opendata/browser/electricity/rto/daily-fuel-type-data
# 1. Logging
# 2. Wrap the Request call in a Function

EIA_APIKEY_FILEPATH = './api_key.json'
EIA_API_URL = "https://api.eia.gov/v2/electricity/rto/daily-fuel-type-data/data/"

def fetch_eia_data(url, api_key, headers, params):
	"""This function creates the URL to fetch EIA data"""
	url = f'{url}?api_key={api_key}'
	res = requests.get(url, headers=headers, params=params).json()
	return res['response']['data']

if __name__ == "__main__":
	# Set filepath for the API key
	with open(EIA_APIKEY_FILEPATH) as f:
		api_key = json.load(f)['EIA_API']

	# Pull data from the eia.gov data source via request
	# url = f"https://api.eia.gov/v2/electricity/rto/daily-fuel-type-data/data/?api_key={api_key}"
	headers = {"Accept": "application/json"}
	# auth = HTTPBasicAuth('api_key', api_key)

	params = {
		'frequency':'daily',
		'data[0]': 'value',
		'start':'2022-12-25',
		'end':'2022-12-27',
		'facets[fueltype][]' : 'WND'	
	}

	print(fetch_eia_data(EIA_API_URL, api_key, headers, params))

# https://api.eia.gov/v2/electricity/rto/daily-region-sub-ba-data/data/?frequency=daily
#&data[0]=value
#&start=2023-01-01
#&end=2023-01-01
#sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000

# res = requests.get(url, headers=headers, params=params)
# data = res.json()['response']['data']

# # Normalize into a dataframe
# df = pd.DataFrame(data)
# # df.to_csv('sample.csv', index=False)
# value = df['value'].tolist()

# # Make a post request to the prediction service
# prediction_url = 'http://127.0.0.1:8000/predict'
# model_input = { 'inputs': [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16,
#        17, 18, 19, 20, 21, 22, 23] }

# model_output = requests.post(prediction_url, json=model_input)
# print(model_output.text)


# https://api.eia.gov/v2/electricity/rto/region-data/data/?frequency=hourly&data[0]=value&facets[respondent][]=NY&facets[type][]=D&sort[0][column]=period&sort[0][direction]=desc&offset=65820&length=5000