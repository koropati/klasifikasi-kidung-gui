import PySimpleGUI as sg

def block_focus(window):
    for key in window.key_dict:    # Remove dash box of all Buttons
        element = window[key]
        if isinstance(element, sg.Button):
            element.block_focus()

def popup_predict_risk(industry):

    col_layout = [[sg.Button("Predict Risk", bind_return_key=True), sg.Button('Cancel')]]
    layout = [
        [sg.Text(f"Industry: {industry}")],
        [sg.Text('Enter Observation/Recommendation: '), sg.InputText(key='Observation')],
        [sg.Column(col_layout, expand_x=True, element_justification='right')],
    ]
    window = sg.Window("Predict Risk", layout, use_default_focus=False, finalize=True, modal=True)
    block_focus(window)
    event, values = window.read()
    window.close()
    return values['Observation'] if event == 'Predict Risk' else None

def popup_prediction(industry, observation):

    col_layout = [[sg.Button('OK')]]
    layout = [
        [sg.Text("Here's the result\n")],
        [sg.Text(f"industry   : {industry}")],
        [sg.Text(f"Observation: {observation}")],
        [sg.Column(col_layout, expand_x=True, element_justification='right')],
    ]
    window = sg.Window("Prediction", layout, use_default_focus=False, finalize=True, modal=True)
    block_focus(window)
    event, values = window.read()
    window.close()
    return None

items = [
    "Automobile", "Chemical", "Engineering/Consulting", "FMCG",
    "Healthcare/Hospitality", "Infrastructue", "IT/Comm/DC", "Manufacturing",
    "Mines", "Energy/Oil & Gas", "Pharma", "Retail", "Cement",
]
length = len(items)
size = (max(map(len, items)), 1)

sg.theme("DarkBlue3")
sg.set_options(font=("Courier New", 11))

column_layout = []
line = []
num = 4
for i, item in enumerate(items):
    line.append(sg.Button(item, size=size, metadata=False))
    if i%num == num-1 or i==length-1:
        column_layout.append(line)
        line = []

layout = [
    [sg.Text('Choose the Industry')],
    [sg.Column(column_layout)],
]
window=sg.Window("Risk Predictor", layout, use_default_focus=False, finalize=True)
block_focus(window)

sg.theme("DarkGreen3")
while True:

    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event in items:
        industry = event
        observation = popup_predict_risk(industry)
        if observation is not None:
            popup_prediction(industry, observation)

window.close()