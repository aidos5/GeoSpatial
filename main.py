from get_canonical import find_canonical_name
from fuzzywuzzy import fuzz
from hugging_face import ner_hugging_face
from geo import get_coordinates
import streamlit as st
import pandas as pd


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

        st.write("Extracted Locations:")
        for place in places:
            st.write(f"- {place}")

if __name__ == '__main__':
    main()
