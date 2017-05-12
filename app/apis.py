import json
import requests
from app import app
import dateutil.parser as dateparser

def checkStatus(apiResponse):
	"""Checks to see if the API's response code is good!~ yay."""
	if (str(apiResponse.status_code)[0] == "2"):
		return json.loads(apiResponse.text)
	return False

def getWeather():
	"""Calls the open weather api and returns a list with the [temperature, icon]; if it receives a redirection, or client error, returns false."""
	# checks for positive status codes
	parsed = checkStatus(requests.get("http://api.openweathermap.org/data/2.5/weather?q=Wellesley,usa&units=imperial&APPID=" + app.config['WEATHER_API_KEY']))
	# if there is something in parsed, returns that data in a list
	if (parsed):
		return [parsed["main"]["temp"],("http://openweathermap.org/img/w/" + parsed["weather"][0]["icon"] + ".png")]
	# if there's nothing in parsed, returns False
	else:
		return parsed

def getVids():
	"""Calls the youtube api and checks for the most recent videos on the WCTV channel.
	Returns a list of lists with [videoId, title, description, py-datetime, thumb_url] data for each individual video."""
	r = requests.get("https://www.googleapis.com/youtube/v3/playlistItems?method=get&part=snippet&key="+ app.config['GOOGLE_API_KEY'] + "&playlistId=UUKojFaXAPAFY2_y1dnnCoDQ")
	parsed = checkStatus(r)
	if parsed != False:
		video_data_list = []
		for i in range(0,5):
			video_data = []
			video_data.append(parsed["items"][i]["snippet"]["resourceId"]["videoId"])
			video_data.append(parsed["items"][i]["snippet"]["title"])
			video_data.append(parsed["items"][i]["snippet"]["description"])
			#converts publishedAt date into python datetime object
			pub_datetime_obj = dateparser.parse(parsed["items"][i]["snippet"]["publishedAt"])
			video_data.append(pub_datetime_obj)
			video_data.append(parsed["items"][i]["snippet"]["thumbnails"]["medium"]["url"])
			video_data_list.append(video_data)
		return video_data_list
	return False