import urllib.request, json


host = 'http://api.weatherapi.com/v1/forecast.json?key=f050f57913a34e3aa3952041231506&q=Bangkok&days=3&aqi=no&alerts=no'

request = urllib.request.Request(host)
response = urllib.request.urlopen(request)
content = response.read()
weather_data = json.loads(content)

weather_code_tomorrow = weather_data['forecast']['forecastday'][1]['day']['condition']['code']
print(weather_code_tomorrow)