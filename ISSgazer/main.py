import PySimpleGUI as sg
import datetime as dt

def printDeltaTime(deltaSeconds = 0):
   t = (dt.datetime.utcnow() + dt.timedelta(seconds = deltaSeconds ))     
   return t.strftime('%a %d %b %Y, %I:%M%p')


layout = [
    [sg.Text("ISS Gazer")],
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
print('Shutting down...')       
