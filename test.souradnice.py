import requests
import folium
import webbrowser

# Stahovaní  dat o letadlech (krajiny pristani)
url = "https://opensky-network.org/api/states/all"
response = requests.get(url)
data = response.json()

# Vyberam si dva body, které budou začáteční a koncovou destinací
start_location = [51.5074, 0.1278] # Londýn, Velká Británie
end_location = [48.8566, 2.3522] # Paříž, Francie

# Vytvořeni mapy a zobrazeni  trasy mezi dvěma body
map = folium.Map(location=start_location, zoom_start=12)
folium.PolyLine(locations=[start_location, end_location], color="red", weight=2.5, opacity=1).add_to(map)

# Uložte mapu do souboru HTML
map.save("route.html")
webbrowser.open("route.html")