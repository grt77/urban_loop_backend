from flask import Blueprint,request,jsonify
from Services.Map_service import get_location_details,get_mapbox_suggestions

map_routes=Blueprint('map',__name__)

@map_routes.route('/get_mapbox_suggestions',methods=['POST'])
def get_map_suggestions():
    try:
        data=request.get_json()
        query=data.get('query')
        prox_lat=data.get('proximity_latitude')
        prox_long=data.get('proximity_longitude')
        session_token=data.get('session_token')
        suggestions=get_mapbox_suggestions(query,prox_lat,prox_long,session_token)
        return suggestions
    except Exception as e:
        return {"Error":str(e)}


@map_routes.route('/get_location_details',methods=['POST'])
def get_loc_details():
    try:
        data=request.get_json()
        location_id=data.get('location_id')
        session_id=data.get('session_id')
        return get_location_details(location_id,session_id)
    except Exception as e:
        return {"Error":str(e)}

