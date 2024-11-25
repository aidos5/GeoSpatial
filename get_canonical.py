import pandas as pd

canonical_df = pd.read_csv("CanonicalNames.csv")

def find_canonical_name(place):
    """Match extracted name to canonical name table."""
    place_lower = place.lower()  # Normalize case
    for _, row in canonical_df.iterrows():

        # Check canonical name
        if place_lower == row['Canonical Name'].lower():
            return row['Canonical Name'], row['State']
        
        # Check variations
        if pd.notna(row['Variations']):
            variations = row['Variations'].lower().split('|')  # Split variations
            if place_lower in variations:
                return row['Canonical Name'], row['State']
    
    # If no match found
    
    return None, None