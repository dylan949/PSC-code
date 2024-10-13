from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from forms import CustomerForm

app = Flask(__name__)
app.secret_key = '9OLWxND4o83j4K4iuopO'

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['shipping_db']
routes_collection = db['continent_to_continent']

# Predefined events with choke points and affected ports
events = {
    'earthquake_china': {
        'choke_points': [],
        'affected_ports': [ "Dalian Container Terminal", "Fuzhou Container Terminals",  "Tianjin Terminals", "LYG-PSA Container Terminal", "Guangzhou Container Terminal", "Beibu-Gulf International Container Terminal",]
    },
    'iran_israel_war': {
        'choke_points': ['Red Sea', 'Suez Canal'],
        'affected_ports': ['Saudi Global Ports', "PSA Singapore",  "PSA Sical", "PSA Chennai", "PSA Mumbai" , "PSA Kolkata", "Dalian Container Terminal","Fuzhou Container Terminals", "Tianjin Terminals", "LYG-PSA Container Terminal",  "Guangzhou Container Terminal", "Beibu-Gulf International Container Terminal",
        "Incheon Container Terminal",  "Busan Terminals", "Hibiki Container Terminal" ]
    },
    'panama_canal_block': {
        'choke_points': ['Panama Canal'],
        'affected_ports': ["Dalian Container Terminal","Fuzhou Container Terminals", "Tianjin Terminals", "LYG-PSA Container Terminal",  "Guangzhou Container Terminal", "Beibu-Gulf International Container Terminal",
        "Incheon Container Terminal",  "Busan Terminals", "Hibiki Container Terminal", 'Saudi Global Ports', "PSA Singapore",  "PSA Sical", "PSA Chennai", "PSA Mumbai" , "PSA Kolkata",  ]
    },
    'malacca_strait_tension': {
        'choke_points': ['Strait of Malacca'],
        'affected_ports': ["Dalian Container Terminal", "Tianjin Terminals", "LYG-PSA Container Terminal",  "Guangzhou Container Terminal", "Beibu-Gulf International Container Terminal",
        "Incheon Container Terminal",  "Busan Terminals", "Hibiki Container Terminal" ]
  

    }
} 

ship_data = [
    {'ship_name': 'Ship-1545', 'event': 'panama_canal_block', 'cargo': 'Electronics', 'departure_port': "PSA Penn Terminals", 'arrival_port': 'Beibu-Gulf International Container Terminal', "Status": "On route", "Recommended_Course_of_Action": "Dock at Exolgan Container Terminal and use its distribution network to bypass the Panama Canal.", 'choke_points': ['Panama Canal']},
    {'ship_name': 'Ship-2903', 'event': 'iran_israel_war', 'cargo': 'Construction Materials', 'departure_port': "PSA Sines", 'arrival_port': 'LYG-PSA Container Terminal', 'choke_points': ['Suez Canal'],"Status":"At Departure Port", "Recommended_Course_of_Action": "Use Cargo Freight with the facilities at the dock to deliver to end destination"},
    {'ship_name': 'Ship-2985', 'event': 'panama_canal_block', 'cargo': 'Construction Materials', 'departure_port': 'PSA Chennai', 'arrival_port': "PSA Penn Terminals", "Status": "On route", "Recommended_Course_of_Action": "Dock at Sociedad Puerto Industrial Aguadulce and use truck freight", 'choke_points': ['Panama Canal']},
    {'ship_name': 'Ship-3573', 'event': 'iran_israel_war', 'cargo': 'Chemicals', 'departure_port': 'Incheon Container Terminal', 'arrival_port': 'Saudi Global Ports', 'choke_points': ['Suez Canal'],"Status":"On route", "Recommended_Course_of_Action": "Take the Cape of Good Hope Route"},
    {'ship_name': 'Ship-5806', 'event': 'earthquake_china', 'cargo': 'Machinery', 'departure_port': 'Guangzhou Container Terminal', 'arrival_port': 'Fuzhou Container Terminals', "Status": "On route", 'choke_points': "-",'Status':"On route", "Recommended_Course_of_Action": "Wait for further instructions as damage is assessed"},
    {'ship_name': 'Ship-6202', 'event': 'panama_canal_block', 'cargo': 'Automobile Parts', 'departure_port': 'LYG-PSA Container Terminal', 'arrival_port': "PSA Halifax", "Status": "On route", "Recommended_Course_of_Action": "Dock at Sociedad Puerto Industrial Aguadulce and use truck freight", 'choke_points': ['Panama Canal']},
    {'ship_name': 'Ship-6866', 'event': 'malacca_strait_tension', 'cargo': 'Furniture', 'departure_port': 'Busan Terminals', 'arrival_port': "PSA Mumbai", 'choke_points': ['Strait of Malacca'], "Status": "On route", "Recommended_Course_of_Action": "Dock at PSA Singapore and use the warehouse"},
    {'ship_name': 'Ship-6902', 'event': 'malacca_strait_tension', 'cargo': 'Oil', 'departure_port': 'Saudi Global Ports', 'arrival_port': 'Dalian Container Terminal', 'choke_points': ['Strait of Malacca'], "Status": "At Departure Port", "Recommended_Course_of_Action": "Dock at PSA Mumbai and wait for further instruction"},
    {'ship_name': 'Ship-3697' ,  'event': 'malacca_strait_tension', 'cargo': 'Food Products', 'departure_port': 'PSA Kolkata', 'arrival_port': 'Busan Terminals', 'choke_points': ['Strait of Malacca'], "Status" : "On route", "Recommended_Course_of_Action": " Use Air Freights to complete the delivery" },
    {'ship_name': 'Ship-9080', 'event': 'earthquake_china', 'cargo': 'Electronics', 'departure_port': 'LYG-PSA Container Terminal', 'arrival_port': 'Tianjin Terminals', "Status": "At departure port", 'choke_points': "-","Status":"At departure port","Recommended_Course_of_Action": "Wait for further instructions as damage is assessed"},
    {'ship_name': 'Ship-9450', 'event': 'iran_israel_war', 'cargo': 'Machinery', 'departure_port': 'Incheon Container Terminal', 'arrival_port': 'PSA Zeebrugge', 'choke_points': ['Suez Canal', 'Red Sea'], "Status" : "On route", "Recommended_Course_of_Action": 'Use Cargo Freight with the facilities at the dock to deliver to end destination'}
]





@app.route('/', methods=['GET'])
def index():
    return render_template('customer_form.html')

@app.route('/customer_form', methods=['GET', 'POST'])
def customer_form():
    form = CustomerForm()
    if form.validate_on_submit():
        selected_event = form.global_event.data
        return redirect(url_for('check_routes', global_event=selected_event))
    return render_template('customer_form.html', form=form)

@app.route('/check_routes', methods=['GET', 'POST'])
def check_routes():
    """Process the form submission and retrieve affected ports from events dict."""
    if request.method == 'POST':
        selected_event = request.form.get('global_event')
    else:
        selected_event = request.args.get('global_event')

    print(f"Selected Event: {selected_event}")  # Debugging statement

    if not selected_event:
        return "No event selected", 400

    # Retrieve the event data based on the selected event
    event_data = events.get(selected_event)
    print(f"Event Data: {event_data}")  # Debugging statement

    if event_data:
        affected_ports = event_data.get('affected_ports', [])
        print(f"Affected Ports: {affected_ports}")  # Debugging statement
        
        # Filter fluff data based on the selected event
        relevant_ships = [ship for ship in ship_data if ship['event'] == selected_event]
        print(f"Relevant Ships: {relevant_ships}")  # Debugging statement
    else:
        return "Invalid event selected", 400

    return render_template('route_results.html', affected_ports=affected_ports, relevant_ships=relevant_ships)

if __name__ == '__main__':
    app.run(debug=True)

