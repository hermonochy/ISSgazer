import PySimpleGUI as sg


layout = [
    [sg.Text("ISS Gazer")],
    [sg.Text("")], 
    [sg.Button("Reset")],
    [sg.Button("Play")],
    [sg.Button("Next Passover")],]
    
window = sg.Window(
    "ISS Gazer",
    layout,
    location=(0, 0),
    finalize=True,
    element_justification="center",
    font="Helvetica 18",
)
while True:
    event, values = window.read()
    print ("event loop info: ",event,values)
    if event == "Quit" or event == sg.WIN_CLOSED:
        break
