from urllib.request import Request, urlopen,  URLError
from urllib.parse import urlencode, quote
from flask import Flask

import simplejson as json
import globs

# Accuweather API key
#set in globs.py
api_key = globs.API_KEY
# Developer URL
base_url = "http://dataservice.accuweather.com"

# API endpoints
loc_call = "/locations/v1/search"
loc_cur ="/currentconditions/v1/"
loc_fore="/forecasts/v1/daily/1day/"

app = Flask(__name__)

@app.route('/City/<city>')
def city(city):

    sp = quote(city)# encode and quote input string

    # Build URLs
    url_loc = base_url + loc_call
    url_cur = base_url + loc_cur
    url_for = base_url + loc_fore

    #Search for location id and store
    urlsend = url_loc + "?"  + "apikey=" + api_key + "&q=" + sp
    myURL = urlopen(urlsend).read()
    results = json.loads(myURL)[0]
    name = results.get('LocalizedName')
    country = results.get('Country').get('EnglishName')
    region = results.get('AdministrativeArea').get('EnglishName')
    location = results.get('Key')

    # Use location id found above to return temp in metric units
    urlcur = url_cur  + location + "?apikey=" + api_key
    conURL = urlopen(urlcur).read()
    cond = json.loads(conURL)[0]
    temp = cond.get('Temperature').get('Metric').get('Value')
    unit = cond.get('Temperature').get('Metric').get('Unit')
    info = cond.get('WeatherText')

    # Use location and forecast API to get weather for upcoming days
    urlfor = url_for  + location + "?apikey=" + api_key + "&metric=true"
    forURL = urlopen(urlfor).read()
    forecast = json.loads(forURL)
    overview = forecast.get('Headline').get('Text')
    mini = forecast.get('DailyForecasts')[0].get('Temperature').get('Minimum').get('Value')
    maxi = forecast.get('DailyForecasts')[0].get('Temperature').get('Maximum').get('Value')
    day = forecast.get('DailyForecasts')[0].get('Day').get('IconPhrase')
    night = forecast.get('DailyForecasts')[0].get('Night').get('IconPhrase')
    minmax = "With a Min of {0}{2} and Max of {1}{2}".format(mini, maxi, unit)

    weatherdata = [ {'name':name},
                    {'region':region},
                    {'country':country},
                    {'temprature':temp},
                    {'unit':unit},
                    {'info':info},
                    {'today':day},
                    {'tonight':night},
                    {'minmax':minmax}
                  ]

    return json.dumps(weatherdata, separators=(',', ':'), sort_keys=True)

if __name__ == '__main__':
    app.run()


