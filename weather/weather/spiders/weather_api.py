# -*- coding:utf-8 -*-

import requests
import json

api_url = 'https://www.sojson.com/open/api/weather/json.shtml?city='

city = '深圳'

url = api_url + city

resp = requests.get(url).json()

print(resp['date'])
print(resp['data']['wendu'])
print(resp['data']['shidu'])
