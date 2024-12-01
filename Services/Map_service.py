import requests
from  dotenv import load_dotenv
import os

def get_mapbox_suggestions(query, latitude, longitude, session_token, limit=10):
    load_dotenv()
    access_token = os.getenv("MAP_TOKEN")
    base_url = "https://api.mapbox.com/search/searchbox/v1/suggest"
    params = {
        "q": query,
        "access_token": access_token,  
        "proximity": f"{longitude},{latitude}",
        "limit": limit,
        "country": "IN",  
        "language": "en", 
        "session_token": session_token
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        suggestions = response.json().get("suggestions", [])
        result = [
              {"mapbox_id": item["mapbox_id"], "name_place": f'{item["name"]}, {item["place_formatted"]}'}
               for item in suggestions
                   ]
        return result
    except requests.exceptions.RequestException as e:
        return {"message":str(e)}

def get_location_details(mapbox_id, session_token, language="en", eta_type=None, navigation_profile=None, origin=None):
    load_dotenv()
    access_token = os.getenv("MAP_TOKEN")
    base_url = f"https://api.mapbox.com/search/searchbox/v1/retrieve/{mapbox_id}"
    params = {
        "access_token": access_token,  
        "session_token": session_token,
        "language": language
    }
    if eta_type:
        params["eta_type"] = eta_type
    if navigation_profile:
        params["navigation_profile"] = navigation_profile
    if origin:
        params["origin"] = origin

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() 
        data = response.json()
        if data["features"]:
            coordinates = data["features"][0]["geometry"]["coordinates"]
            return {"longitude": coordinates[0], "latitude": coordinates[1]}
        else:
            return {"error": "No location data found"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}





if __name__ == "__main__":
    pass
    # Example values
    query = "Sasya"
    latitude = 12.9716
    longitude = 77.5946
    session_token = "unique-session-token"  
    #mapbox_id = "dXJuOm1ieHBvaToxMGU0MWRmNy03NGQxLTQyYWEtYTkzZC1hZTM5ZDRmMmEyOWU"
    #result = get_location_details(mapbox_id, session_token, eta_type="navigation", navigation_profile="driving", origin="77.5946,12.9716")
    #print(result)
    suggestions = get_mapbox_suggestions(query, latitude, longitude, session_token)
    print(suggestions)