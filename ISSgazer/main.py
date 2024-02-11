import PySimpleGUI as sg
import datetime as dt
import json
from pathlib import Path
import sys
import PIL.Image
import io
from orbit_predictor.sources import EtcTLESource
from orbit_predictor.locations import Location
source = EtcTLESource(filename="../data/iss.tle")
predictor = source.get_predictor("ISS")

citiesFilePath = Path('..') / 'data' / 'cities.json'
savedLocationFilePath = Path('..') / 'data' / 'savedLocation.json'
worldmapFilePath = Path('..') / 'data' / 'world-map.png'
 
def getXYCoordinates(lat,lng,w,h):
    x= w/360*lng+w/2
    y=-h/180*lat+h/2
    return int(x+0.5),int(y+0.5)

def printDeltaTime(deltaSeconds = 0):
   t = (dt.datetime.utcnow() + dt.timedelta(seconds = deltaSeconds ))     
   return t.strftime('%a %d %b %Y, %I:%M%p')

def getCoordinates(country, city):
  cities = [c for c in citiesCoordinateDict if c['country']==country]
  selectedCity = [c for c in cities if c['name']==city]
  print(selectedCity[0])
  return selectedCity[0]['lat'], selectedCity[0]['lng']
  
def loadWorldMap(lat,lng,lat_ISS=None,lng_ISS=None):
    lat,lng = int(float(lat)),int(float(lng))
    img = PIL.Image.open(worldmapFilePath) 
    cur_width, cur_height = img.size  
    scale = 0.5
    img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.LANCZOS)
                  
    x,y= getXYCoordinates(lat,lng,cur_width*scale-1, cur_height*scale-1)
    for i in range (-5,6):
       
       try:
         img.putpixel((x+i,y), (255,0,0))
         img.putpixel((x,y+i), (255,0,0))
       except IndexError:
         print ("Observer Coordinates out of range!")
    
    if lat_ISS is not None and lng_ISS is not None:
       x,y= getXYCoordinates(lat_ISS,lng_ISS,cur_width*scale-1, cur_height*scale-1)
       for i in range (-5,6):
         try:
           img.putpixel((x+i,y), (255,255,0))
           img.putpixel((x,y+i), (255,255,0))
         except IndexError:
           print ("ISS Coordinates out of range!")
    
       
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()  


with citiesFilePath.open() as cities_file:
  cities_file_content = cities_file.read()
citiesCoordinateDict = json.loads(cities_file_content)
countriesList = list(set([c['country'] for c in citiesCoordinateDict]))
countriesList.sort()
try:
  with savedLocationFilePath.open() as savedLocation_file:
    savedLocation_file_content = savedLocation_file.read()
  savedLocationDict = json.loads(savedLocation_file_content)
  selectedCountry = savedLocationDict["country"]
  selectedCity = savedLocationDict["city"]
except:
  selectedCountry = "GB"
  selectedCity =  "Oxford"

try:
  lat, lng = getCoordinates(selectedCountry,selectedCity)
except IndexError:
  print ("IndexError! Erasing corrupted savedlocation file!")
  savedLocationFilePath.unlink()
  print ("Please restart!")
  sys.exit()

citiesList=[c['name'] for c in citiesCoordinateDict if c['country']==selectedCountry]
citiesList.sort()
layout = [
    [sg.Text("ISS Gazer")],
    [sg.Text("Country: "), sg.Combo(countriesList, default_value=selectedCountry, s=(15,22), \
        enable_events=True, readonly=True, k='-LOCATION_COUNTRY-')],
    [sg.Text("City: "), sg.Combo(citiesList, default_value=selectedCity, s=(15,22), \
        enable_events=True, readonly=True, k='-LOCATION_CITY-')],
    [sg.Text("Coordinates:  " + str(lat )+"  , "+str( lng) , key="coordinatesText" )],
    [sg.Text(""+ printDeltaTime(), key="datetimeText" )],
    [sg.Image(key='-IMAGE-')], 
    [sg.Text("Prediction:"),
    sg.Button("Reset"),
    sg.Button("Play"),
    sg.Button("Next Passover"),
    sg.Button("Quit")],]
    
window = sg.Window(
    "ISS Gazer",
    layout,
    location=(0, 0),
    finalize=True,
    element_justification="center",
    font="Helvetica 18",
)
window['-IMAGE-'].update(data=loadWorldMap(lat,lng))
timeout = None
issDeltaTime = 0 #dt.timedelta(seconds = 0 )
while True:
    event, values = window.read(timeout = timeout) 
    if event == "__TIMEOUT__":
        issDeltaTime += 10
        text = printDeltaTime(deltaSeconds=issDeltaTime)
        window['datetimeText'].update( text )
        # Get ISS position
        issTime = (dt.datetime.utcnow() + dt.timedelta(seconds = issDeltaTime ))
        position = predictor.get_position(issTime)
        llh_tuple=position.position_llh
        issLat=llh_tuple[0]
        issLng=llh_tuple[1]
        window['-IMAGE-'].update(data=loadWorldMap(lat,lng,issLat,issLng))
        continue
    print ("event loop info: ",event,values)
    
    if event == "Reset" :
        timeout = None 
        issDeltaTime = 0
        window['datetimeText'].update( printDeltaTime(deltaSeconds=issDeltaTime) )   
    if event == "Play":
         timeout = 100      
    if event == "Next Passover":
         location = Location("dummy", latitude_deg=float(lat), longitude_deg=float(lng), elevation_m=0.0)
         nextpass = predictor.get_next_pass(location, issTime)     
         issDeltaTime = (nextpass.aos - dt.datetime.utcnow()).total_seconds()
         timeout = 100
    if event == '-LOCATION_COUNTRY-':
         selectedCountry = values['-LOCATION_COUNTRY-']
         citiesList=[c['name'] for c in citiesCoordinateDict if c['country']==selectedCountry]
         citiesList.sort()
         window['-LOCATION_CITY-'].update(values=citiesList)
    if event == '-LOCATION_CITY-':
         lat, lng = getCoordinates(values['-LOCATION_COUNTRY-'], values['-LOCATION_CITY-'])
         window['coordinatesText'].update("Coordinates:  " + str(lat)+"  , "+str(lng))
         window['-IMAGE-'].update(data=loadWorldMap(lat,lng))
         
    if event == "Quit" or event == sg.WIN_CLOSED:
         savedLocation = {'country': values['-LOCATION_COUNTRY-'], 'city': values['-LOCATION_CITY-']}
         savedLocationString = json.dumps(savedLocation)
         with savedLocationFilePath.open('w') as savedLocation_file:
            savedLocation_file.write(savedLocationString)
         break
print('Shutting down...')       
