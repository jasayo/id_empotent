import json
import request

url= 'https://api.openweathermap.org/data/2.5/onecall/timemachine'
r= request.get(url)
data = json.loads(r.text)   
weather_list = []
data = json.load(data)
for item in data:
    average_temperature = item['average_temperature']
    min_temperature = item['min_temperature']
    location = item['location']
    max_temperature = item['max_temperature']

    weather = {
        'average_temperature' :average_temperature,
        'min_temperature' :min_temperature,
        'location' :min_temperature,
        'max_temperature' :max_temperature
    }

    weather_list.append(weather)
