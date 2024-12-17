from get_canonical import find_canonical_name
from hugging_face import ner_hugging_face
from geo import get_coordinates
import streamlit as st
import pandas as pd
import requests  

API_KEY = "fdf81c335114a30af75af6f2f64b51f3"

def get_weather_data(lat, lon):
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}")
    if response.status_code == 200:
        data = response.json()  # Use response.json() for parsing JSON data
        # Extract relevant weather information
        max_temp_k = data["main"]["temp_max"]
        min_temp_k = data["main"]["temp_min"]
        humidity = data["main"]["humidity"]
        
        # Convert temperatures to Celsius
        max_temp_c = max_temp_k - 273.15
        min_temp_c = min_temp_k - 273.15
        
        return {
            "max_temp": round(max_temp_c, 2),  # Rounded to 2 decimal places
            "min_temp": round(min_temp_c, 2),
            "humidity": humidity
        }
    else:
        print(f"Error fetching weather data: {response.text}")
    return None

 
def main():
    # Sample coordinates for multiple locations
    sentence = st.text_input("Enter a sentence with locations",placeholder="")
    show_map = st.button("Find Locations")
    place_candidates = ner_hugging_face(sentence)

    if(show_map):
        matched_places = {}
        places = []
        for place in place_candidates:
            canonical_name, entity_type = find_canonical_name(place)
            if canonical_name:
                matched_places[place] = {'Canonical Name': canonical_name, 'Entity Type': entity_type}
                places.append(canonical_name)

            else:
                print(f"No canonical match for: {place}")
       

        locations = get_coordinates(places)
        print(locations)
        # Create a DataFrame with the coordinates and location names
        data = pd.DataFrame.from_dict(locations, orient='index', columns=['lat', 'lon'])
        data.reset_index(inplace=True)
        data.rename(columns={'index': 'location'}, inplace=True)

        # Display the map with multiple markers
        st.map(data)
        st.text("Canonical Names found from the entered sentence were")

        for location, coords in locations.items():
            lat, lon = coords
            print(lat)
            # Potential error source: Ensure accurate coordinates from get_coordinates
            print(f"Fetching weather data for {location} ({lat}, {lon})")
            weather_data = get_weather_data(lat, lon)

            if weather_data:
                st.write(f"--- Weather for {location} ---")
                st.write(f"Max Temp: {weather_data['max_temp']}°C")
                st.write(f"Min Temp: {weather_data['min_temp']}°C")
                st.write(f"Humidity: {weather_data['humidity']}%")
            else:
                st.write(f"Error retrieving weather data for {location}")


if __name__ == '__main__':
    main()