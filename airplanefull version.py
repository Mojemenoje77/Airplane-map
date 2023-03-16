import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import requests
import folium
import webbrowser


# Vytvoření hlavního okna
root = tk.Tk()
root.title("Mapa letadel")
root.resizable(False,False)
root.minsize(500,200)
root.config(bg="#4169E1")
root.iconbitmap("icon.ico")


 #Načtení obrázku
image = Image.open("img/air.jpg")
photo = ImageTk.PhotoImage(image)

 #Vytvoření canvasu a zobrazení obrázku
canvas = tk.Canvas(root, width=image.width, height=image.height)
canvas.pack()
canvas.create_image(image.width//2, image.height//2, image=photo)




# Získání dat z API
url = "https://opensky-network.org/api/states/all"
response = requests.get(url)
data = response.json()

# Převod souřadnic získaných z API do seznamu
coordinates = [(item[5], item[6], item[7], item[9], item[10], item[11], item[0], item[3]) for item in data['states'] if (item[5] is not None and item[6] is not None)]

# Vytvoření seznamu s informacemi o letadlech
flights = []
for coord in coordinates:
    latitude = coord[0] # Zeměpisná šířka
    longitude = coord[1] # Zeměpisná délka
    altitude = coord[2] # Nadmořská výška
    speed = coord[3] # Rychlost letadla
    heading = coord[4] # Směr letadla
    flight = coord[5] # Pohyb letadla
    ident = coord[6] # Identifikátor letadla
    timestamp = coord[7] # Časový údaj
    flights.append((ident, latitude, longitude, altitude, speed, heading, flight, timestamp))
    
    
def show_map():
    # Vytvoření mapy
    m = folium.Map(location=[48.8566, 2.3522], zoom_start=4)

    # Zobrazování letadel na mapě
    for flight in flights:
        ident = flight[0] # Identifikátor letadla
        latitude = flight[1] # Zeměpisná šířka
        longitude = flight[2] # Zeměpisná délka
        altitude = flight[3] # Nadmořská výška
        speed = flight[4] # Rychlost letadla
        heading = flight[5] # Směr letadla
        flight_path = flight[6] # Pohyb letadla
        timestamp = flight[7] # Časový údaj

        folium.Marker(location=[latitude, longitude], 
                      popup=f"Identifikátor: {ident}\nZeměpisná šířka: {latitude}\nZeměpisná délka: {longitude}\nNadmořská výška: {altitude}\nRychlost: {speed}\nSměr: {heading}\nPohyb: {flight_path}\nČas: {timestamp}").add_to(m)

        folium.CircleMarker(location=[latitude, longitude], radius=3, color="red").add_to(m)
        
    m.save("flights_map.html")
    webbrowser.open("flights_map.html")

def update_map():
    # Získání dat z API
    url = "https://opensky-network.org/api/states/all"
    response = requests.get(url)
    data = response.json()

    # Převod souřadnic získaných z API do seznamu
    coordinates = [(item[5], item[6], item[7], item[9], item[10], item[11], item[0], item[3]) for item in data['states'] if (item[5] is not None and item[6] is not None)]

    # Aktualizace seznamu s informacemi o letadlech
    flights.clear()
    for coord in coordinates:
        latitude = coord[0] # Zeměpisná šířka
        longitude = coord[1] # Zeměpisná délka
        altitude = coord[2] # Nadmořská výška
        speed = coord[3] # Rychlost letadla
        heading = coord[4] # Směr letadla
        flight = coord[5] # Pohyb letadla
        ident = coord[6] # Identifikátor letadla
        timestamp = coord[7] # Časový údaj
        flights.append((ident, latitude, longitude, altitude, speed, heading, flight, timestamp))

    show_map()
    
    

# Vytvoření tlačítka pro zobrazení mapy
show_map_button = Button(root, text="Zobrazit mapu", command=show_map)
show_map_button.pack()


# Vytvoření tlačítka pro aktualizaci mapy
update_map_button = Button(root, text="Aktualizovat mapu", command=update_map)
update_map_button.pack()

root.mainloop()