import PySimpleGUI as sg
import datetime as dt
import json

def printDeltaTime(deltaSeconds = 0):
   t = (dt.datetime.utcnow() + dt.timedelta(seconds = deltaSeconds ))     
   return t.strftime('%a %d %b %Y, %I:%M%p')

def getCoordinates(country, city):
  cities = [c for c in citiesCoordinateDict if c['country']==country]
  selectedCity = [c for c in cities if c['name']==city]
  print(selectedCity[0])
  return selectedCity[0]['lat'], selectedCity[0]['lng']


with open('../data/cities.json') as cities_file:
  cities_file_content = cities_file.read()
citiesCoordinateDict = json.loads(cities_file_content)
countriesList = list(set([c['country'] for c in citiesCoordinateDict]))
countriesList.sort()

selectedCountry = 'GB'
selectedCity = 'Oxford'

lat, lng = getCoordinates('GB','Oxford')


citiesList=[c['name'] for c in citiesCoordinateDict if c['country']==selectedCountry]
citiesList.sort()
layout = [
    [sg.Text("ISS Gazer")],
    [sg.Combo(countriesList, default_value=selectedCountry, s=(15,22), enable_events=True, readonly=True, k='-LOCATION_COUNTRY-')],
    [sg.Combo(citiesList, default_value=selectedCity, s=(15,22), enable_events=True, readonly=True, k='-LOCATION_CITY-')],
    [sg.Text("Coordinates:  " + str(lat )+"  , "+str( lng) , key="coordinatesText" )],
    [sg.Text(""+ printDeltaTime(), key="datetimeText" )], 
    [sg.Button("Reset")],
    [sg.Button("Play")],
    [sg.Button("Next Passover")],
    [sg.Button("Quit")],]
    
window = sg.Window(
    "ISS Gazer",
    layout,
    location=(0, 0),
    finalize=True,
    element_justification="center",
    font="Helvetica 18",
)

timeout = None
issDeltaTime = 0 #dt.timedelta(seconds = 0 )
while True:
    event, values = window.read(timeout = timeout) 
    if event == "__TIMEOUT__":
        issDeltaTime += 10
        text = printDeltaTime(deltaSeconds=issDeltaTime)
        window['datetimeText'].update( text )
        continue
    print ("event loop info: ",event,values)
    if event == "Quit" or event == sg.WIN_CLOSED:
        break
    if event == "Reset" :
        timeout = None 
        issDeltaTime = 0
        window['datetimeText'].update( printDeltaTime(deltaSeconds=issDeltaTime) )   
    if event == "Play":
         timeout = 100
    if event == '-LOCATION_COUNTRY-':
         selectedCountry = values['-LOCATION_COUNTRY-']
         citiesList=[c['name'] for c in citiesCoordinateDict if c['country']==selectedCountry]
         citiesList.sort()
         window['-LOCATION_CITY-'].update(values=citiesList)
    if event == '-LOCATION_CITY-':
         lat, lng = getCoordinates(values['-LOCATION_COUNTRY-'], values['-LOCATION_CITY-'])
         window['coordinatesText'].update("Coordinates:  " + str(lat)+"  , "+str(lng))
print('Shutting down...')       
