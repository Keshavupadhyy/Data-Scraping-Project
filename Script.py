import requests
import json
import time

# Your Google Places API key
API_KEY = 'AIzaSyDeofPwDoKMnyKvjNMS96ZVcQsI1wpjLQ0'

# Define the search parameters
location = '23.2032,77.0844'  # Latitude and longitude of the area you want to search
radius = 1500000  # Radius in meters (50km)
search_type = 'amusement_park'
keyword = 'escape room'

# Function to fetch place details
def get_place_details(place_id):
    try:
        place_url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={'AIzaSyDeofPwDoKMnyKvjNMS96ZVcQsI1wpjLQ0'}'
        response = requests.get(place_url)
        response.raise_for_status()
        place_details = response.json().get('result', {})
        return place_details
    except requests.exceptions.RequestException as e:
        print(f"Error fetching details for place ID {place_id}: {e}")
        return {}

# Function to fetch places
def fetch_places(next_page_token=None):
    try:
        places_url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type={search_type}&keyword={keyword}&key={'AIzaSyDeofPwDoKMnyKvjNMS96ZVcQsI1wpjLQ0'}'
        if next_page_token:
            places_url += f'&pagetoken={next_page_token}'
        response = requests.get(places_url)
        response.raise_for_status()
        places = response.json()
        return places.get('results', []), places.get('next_page_token')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching places: {e}")
        return [], None

# Function to parse the place details
def parse_place_details(place):
    details = get_place_details(place['place_id'])
    return {
        'Escape Room Name': details.get('name', 'N/A'),
        'Address': details.get('formatted_address', 'N/A'),
        'Phone Number': details.get('formatted_phone_number', 'N/A'),
        'URL': details.get('website', 'N/A'),
        'Hours of Operation': details.get('opening_hours', {}).get('weekday_text', 'N/A'),
        'Reviews': details.get('reviews', 'N/A'),
        'Social Media Links': details.get('urls', 'N/A')  # This field might not be available
    }

# Function to validate data
def validate_data(data):
    if not data.get('Escape Room Name') or data['Escape Room Name'] == 'N/A':
        return False
    if not data.get('Address') or data['Address'] == 'N/A':
        return False
    return True

# Main function to scrape data and save to JSON
def main():
    all_places = []
    next_page_token = None

    while len(all_places) < 100:
        places, next_page_token = fetch_places(next_page_token)
        for place in places:
            details = parse_place_details(place)
            if validate_data(details):
                all_places.append(details)
        if not next_page_token:
            break
        time.sleep(2)  # Wait for a short while before fetching the next page

    # Ensure we have at least 100 entries
    if len(all_places) < 100:
        print("Could not fetch at least 100 valid entries.")
    else:
        with open('sample_escape_rooms.json', 'w') as file:
            json.dump(all_places, file, indent=4)
        print('Data saved to escape_rooms.json')

if __name__ == '__main__':
    main()
