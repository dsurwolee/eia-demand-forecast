"""
# https://api.eia.gov/v2/electricity/rto/region-data/data/
# ?frequency=hourly
# &data[0]=value
# &facets[respondent][]=NY
# &facets[type][]=D
# &sort[0][column]=period
# &sort[0][direction]=desc
# &offset=65820&length=5000
"""
import json
import logging
import requests
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

from requests.auth import HTTPBasicAuth
from datetime import date, datetime, timedelta
from monthdelta import monthdelta

# (TODO)
# 0. Find the best way to load data. https://www.eia.gov/opendata/browser/electricity/rto/daily-fuel-type-data
# 1. Logging
		# Check for empty data pull
		# Check for request errors 
# 2. Wrap the Request call in a Function

# EIA
CONFIG_FILEPATH = './config.json'

# Data Config 
MONTH_HISTORY = 24
SOURCE = ['NY', 'NE', 'CAL']


import logging
from datetime import datetime

# # create logger
# (logging.basicConfig(
# 	filename='example.log', 
# 	format="%(asctime)s %(levelname)-8s %(message)s",
# 	encoding='utf-8', 
# 	datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO))

# def now():
# 	return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# print(now())

# logging.debug(f'This is debug message')
# logging.info('This is information message')
# logging.warning('This is warning message')
# logging.error('This is warning message')

def extract(url, api_key, headers, params):
	"""This function creates the URL to fetch EIA data"""
	url = f'{url}?api_key={api_key}'
	res = requests.get(url, headers=headers, params=params).json()
	# print(res)
	return res['response']['data']

def transform(data):
	# Cache raw data into dataframe for transformation
	df = pd.DataFrame(data)
	# Map raw field names to 
	name_mapping = ({
		'period': 'datetime',
		'respondent': 'tag',
		'respondent-name': 'source_name',
		'value': 'wattage'
	})
	df = df.rename(columns=name_mapping)
	# Keep only the fields in the name_mapping
	return df[name_mapping.values()]

def load(data, engine):
	# Load data to a postgresql DB
	data.to_sql('demand_history', engine, if_exists='replace')

if __name__ == '__main__':

	# Set up logging
	logging.basicConfig(
		filename='etl_pipeline.log', 
		format="%(asctime)s %(levelname)-8s %(message)s",
		datefmt="%Y-%m-%d %H:%M:%S", 
		level=logging.INFO)

	# Grab the EIA API key from the api_key.json file
	with open(CONFIG_FILEPATH) as f:
		config = json.load(f)

	# Grab EIA config
	eia = config['EIA']
	headers = {"Accept": "application/json"}

	# Connect to PSQL DB
	psql = config['PSQL']
	db_url = psql['URL'] + psql['DBNAME']
	engine = create_engine(db_url)

	# Grab the current date and month
	current_date = datetime.now()
	year = current_date.year
	month = current_date.month
	# Grab the first date of the month
	first_date = datetime(year, month, 1)

	df_store = []
	# Iterate each month per source to fetch data
	for m in range(MONTH_HISTORY): 		

		# Grab the start and last date
		start_date = first_date - monthdelta(m)
		end_date = first_date - monthdelta(m-1)

		# Format dates
		start_date = start_date.strftime("%Y-%m-%d")   # "2023-01-09T00",
		end_date = end_date.strftime("%Y-%m-%d")	   # "2023-01-10T00

		for source_name in SOURCE:


			message = f'Fetching {source_name} for the period: {start_date} - {end_date}'
			logging.info(message)

			# Create parameters to filter data to pull from EIA data source
			params = {
				'frequency':'hourly',
				'data[0]': 'value',
				'start': start_date,
				'end': end_date,
				'facets[respondent][]': source_name,
				'facets[type][]': 'D'
			}

			# Fetch data from EIA data source
			data = extract(eia['URL'], eia['API_KEY'], headers, params)

			# Transform
			df_store.append(transform(data))

	# Load to PSQL database
	df = pd.concat(df_store)
	load(df, engine)

	# Output data locally
	# output_filename = f'eia_{source_name}_{start_date}-{end_date}.csv'
	# df.to_csv(output_filename, index=False)