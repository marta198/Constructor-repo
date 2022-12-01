# Imports libraries
import requests
import json
import datetime
import time
import yaml

from datetime import datetime
from configparser import ConfigParser

print('Asteroid processing service')

# Initiating and reading config values
print('Loading configuration from file')

try:
      config = ConfigParser()
      config.read('config.ini')

      nasa_api_key = config.get('nasa', 'api_key')
      nasa_api_url = config.get('nasa', 'api_url')
except:
      logger.exception('')
      print('DONE')

# Getting todays date
dt = datetime.now()
request_date = str(dt.year) + "-" + str(dt.month).zfill(2) + "-" + str(dt.day).zfill(2)  
print("Generated today's date: " + str(request_date))

# Requests information from NASA API
print("Request url: " + str(nasa_api_url + "rest/v1/feed?start_date=" + request_date + "&end_date=" + request_date + "&api_key=" + nasa_api_key))
r = requests.get(nasa_api_url + "rest/v1/feed?start_date=" + request_date + "&end_date=" + request_date + "&api_key=" + nasa_api_key)

# Printing information from NASA API
print("Response status code: " + str(r.status_code))
print("Response headers: " + str(r.headers))
print("Response content: " + str(r.text))

# Checks the connection to the NASA API - whether the request is successful (200 means it's successful) and if the condition is true, continues in the 'if' branch, if not - jumps to 'else' branch
if r.status_code == 200:

	# Stores decoded text (from JSON)  from NASA API
	json_data = json.loads(r.text)

	# Creates empty lists
	ast_safe = []
	ast_hazardous = []

	# Checks whether there is an 'element_count' in the decoded dataset
	if 'element_count' in json_data:
		# Takes the asteroid count from the dataset (turns it into type 'int'), saves it in a variable and prints the information
		ast_count = int(json_data['element_count'])
		print("Asteroid count today: " + str(ast_count))

		# Checks whether there are any asteroids
		if ast_count > 0:
			# A for loop that goes through all objects near earth at the request date and stores them temporarily in a variable
			for val in json_data['near_earth_objects'][request_date]:
				# Checks whether there are the given elements
				if 'name' and 'nasa_jpl_url' and 'estimated_diameter' and 'is_potentially_hazardous_asteroid' and 'close_approach_data' in val:
					# Takes elements from the val variable and stores them
					tmp_ast_name = val['name']
					tmp_ast_nasa_jpl_url = val['nasa_jpl_url']
					# If statement that checks whether there is an element 'kilometers' found in the val's element 'estimated_diameter'
					if 'kilometers' in val['estimated_diameter']:
						# Checks whether these elements are found in the 'kilometers' element 
						if 'estimated_diameter_min' and 'estimated_diameter_max' in val['estimated_diameter']['kilometers']:
							# Takes both of the variables (min and max), rounds them to 3 decimals and stores them into variables
							tmp_ast_diam_min = round(val['estimated_diameter']['kilometers']['estimated_diameter_min'], 3)
							tmp_ast_diam_max = round(val['estimated_diameter']['kilometers']['estimated_diameter_max'], 3)
						else:
							# If the condition was false (min and max were not found), default values are given to the variables
							tmp_ast_diam_min = -2
							tmp_ast_diam_max = -2
					else:
						# If the condition is false (no 'kilometers' element found), default values are given to variables
						tmp_ast_diam_min = -1
						tmp_ast_diam_max = -1

					# Takes an element from the val variable and stores it into a different variable
					tmp_ast_hazardous = val['is_potentially_hazardous_asteroid']

					# Checks whether there is any data on close approaches (if there are any)
					if len(val['close_approach_data']) > 0:
						# Checks for elements in an element from 'close_approach_data'
						if 'epoch_date_close_approach' and 'relative_velocity' and 'miss_distance' in val['close_approach_data'][0]:
							# Calculates and writes into a new variable the timestamp
							tmp_ast_close_appr_ts = int(val['close_approach_data'][0]['epoch_date_close_approach']/1000)
							# Calculates and writes into a new variable the datetime in UTC
							tmp_ast_close_appr_dt_utc = datetime.utcfromtimestamp(tmp_ast_close_appr_ts).strftime('%Y-%m-%d %H:%M:%S')
							# Calculates and writes into a new variable the datetime
							tmp_ast_close_appr_dt = datetime.fromtimestamp(tmp_ast_close_appr_ts).strftime('%Y-%m-%d %H:%M:%S')

							# Checks for element 'km/h' in another element 'relative velocity'
							if 'kilometers_per_hour' in val['close_approach_data'][0]['relative_velocity']:
								# Takes speed from the element, turns it into type int and saes it in a variable
								tmp_ast_speed = int(float(val['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']))
							else:
								# If there is no element 'kilometers_per_hour', it writes a default value into the variable
								tmp_ast_speed = -1

							# Checks for element 'kilometers' in the val element 'miss_distance'
							if 'kilometers' in val['close_approach_data'][0]['miss_distance']:
								# Takes the distance, rounds it to 3 decimals and saves it into the variable
								tmp_ast_miss_dist = round(float(val['close_approach_data'][0]['miss_distance']['kilometers']), 3)
							else:
								# If there are no 'kilometers' in 'miss_distance', default value is written to the variable
								tmp_ast_miss_dist = -1
						else:
							# If the if condition is not met (one or more of the phrases are not found), default values are given to the variables
							tmp_ast_close_appr_ts = -1
							tmp_ast_close_appr_dt_utc = "1969-12-31 23:59:59"
							tmp_ast_close_appr_dt = "1969-12-31 23:59:59"
					else:
						# If there is no data on close approaches, prints out information and assigns default values to the respective variables
						print("No close approach data in message")
						tmp_ast_close_appr_ts = 0
						tmp_ast_close_appr_dt_utc = "1970-01-01 00:00:00"
						tmp_ast_close_appr_dt = "1970-01-01 00:00:00"
						tmp_ast_speed = -1
						tmp_ast_miss_dist = -1

					# Creates a line to 'split' the output, mark a new beginning
					print("------------------------------------------------------- >>")
					# Prints information from NASA API about asteroids
					print("Asteroid name: " + str(tmp_ast_name) + " | INFO: " + str(tmp_ast_nasa_jpl_url) + " | Diameter: " + str(tmp_ast_diam_min) + " - " + str(tmp_ast_diam_max) + " km | Hazardous: " + str(tmp_ast_hazardous))
					print("Close approach TS: " + str(tmp_ast_close_appr_ts) + " | Date/time UTC TZ: " + str(tmp_ast_close_appr_dt_utc) + " | Local TZ: " + str(tmp_ast_close_appr_dt))
					print("Speed: " + str(tmp_ast_speed) + " km/h" + " | MISS distance: " + str(tmp_ast_miss_dist) + " km")
					
					# Adding asteroid data to the corresponding array
					if tmp_ast_hazardous == True:
						ast_hazardous.append([tmp_ast_name, tmp_ast_nasa_jpl_url, tmp_ast_diam_min, tmp_ast_diam_max, tmp_ast_close_appr_ts, tmp_ast_close_appr_dt_utc, tmp_ast_close_appr_dt, tmp_ast_speed, tmp_ast_miss_dist])
					else:
						ast_safe.append([tmp_ast_name, tmp_ast_nasa_jpl_url, tmp_ast_diam_min, tmp_ast_diam_max, tmp_ast_close_appr_ts, tmp_ast_close_appr_dt_utc, tmp_ast_close_appr_dt, tmp_ast_speed, tmp_ast_miss_dist])

		else:
			# In case the condition is false (there are no asteroids found), it prints out text about it
			print("No asteroids are going to hit earth today")

	# Prints information from NASA API about asteroids, which are safe and which are not
	print("Hazardous asteorids: " + str(len(ast_hazardous)) + " | Safe asteroids: " + str(len(ast_safe)))

	# If condition which checks whether there are any hazardous asteroids
	if len(ast_hazardous) > 0:

		# Sorts the arguments by 'x' asteroid impact on earth
		ast_hazardous.sort(key = lambda x: x[4], reverse=False)
		print("Today's possible apocalypse (asteroid impact on earth) times:")
		# A for loop that goes through all hazardous asteroids and prints information about each of them
		for asteroid in ast_hazardous:
			print(str(asteroid[6]) + " " + str(asteroid[0]) + " " + " | more info: " + str(asteroid[1]))

		# Sorts the arguments by 'x' distance
		ast_hazardous.sort(key = lambda x: x[8], reverse=False)
		print("Closest passing distance is for: " + str(ast_hazardous[0][0]) + " at: " + str(int(ast_hazardous[0][8])) + " km | more info: " + str(ast_hazardous[0][1]))
	else:
		# If the if condition is false and there are no hazardous asteroids found, it prints out this
		print("No asteroids close passing earth today")

else:
	# If there is no response from the API, it prints out this information
	print("Unable to get response from API. Response code: " + str(r.status_code) + " | content: " + str(r.text))
