import requests
import folium
import webbrowser



url = "https://opensky-network.org/api/states/all"

response = requests.get(url)

data = response.json()

# Převod souřadnic získaných z API do seznamu
coordinates = [(item[5], item[6], item[7], item[9], item[10], item[11], item[0], item[3]) for item in data['states'] if (item[5] is not None and item[6] is not None)]
#for item in data['states'] if (item[5] is not None and item[6] is not None)] kontroluje jestli polozky indexu, 
#5 a 6 v položkách seznamu data['states'] nejsou None
# Vytvoření mapy
map = folium.Map(location=[48.8566, 2.3522], zoom_start=6)

# Vložení bodů na mapu
for coord in coordinates:
    latitude = coord[0]  # Zeměpisná šířka
    longitude = coord[1] # Zeměpisná délka
    altitude = coord[2]  # Nadmořská výška
    speed = coord[3]     # Rychlost letadla
    heading = coord[4]   # Směr letadla
    flight = coord[5]    # Pohyb letadla
    ident = coord[6]     # Identifikátor letadla
    timestamp = coord[7] # Časový údaj
    coord = (latitude, longitude)
    
    folium.Marker(location=coord, popup=f"Identifikátor letadla: {ident} <br>Zeměpisná šířka: {latitude} <br>Zeměpisná délka: {longitude} <br>Nadmořská výška: {altitude} <br>Rychlost: {speed} <br>Směr: {heading} <br>Pohyb: {flight} <br>Časový údaj: {timestamp}").add_to(map)
    
webbrowser.open("map.html")
#map.save("map.html")






