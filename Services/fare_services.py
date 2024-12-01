import requests
import math
from  dotenv import load_dotenv
import os

def fare_calc_auto(o_la, o_lo, d_la, d_lo):
    try:
        load_dotenv()
        base_url = "https://api.mapbox.com/directions/v5/mapbox/driving"
        coordinates = f"{o_lo},{o_la};{d_lo},{d_la}"
        access_token = os.getenv("MAP_TOKEN")
        url = f"{base_url}/{coordinates}?access_token={access_token}"
        response = requests.get(url)
        if response.status_code != 200:
            return {"message": "Failed to fetch data from Mapbox API", "error": response.text}
        data = response.json()
        if not data["routes"]:
            return {"message": "No routes found between the given coordinates","error":"no route found"}
        route = data["routes"][0]
        distance_meters = route["distance"]  
        duration_seconds = route["duration"] 
        # Fare Calculation
        base_fare = 25
        rate_first_3km = 15
        rate_above_3km = 12
        distance_km = distance_meters / 1000
        
        # Calculate fare
        if distance_km <= 3:
            distance_fare = distance_km * rate_first_3km
        else:
            distance_fare = (3 * rate_first_3km) + ((distance_km - 3) * rate_above_3km)

        total_fare = math.ceil(base_fare + distance_fare)
        result = {
            "fare_amount": total_fare,
            "distance_km": round(distance_km, 2),
            "duration_minutes": round(duration_seconds / 60, 2),
        }

        return result

    except Exception as e:
        return {"message": "An error occurred", "error": str(e)}

