from flask import Blueprint,request,jsonify
from Services.auth_service import token_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from Services.auth_service import token_required
from Services.ride_services import insert_location,insert_ride,get_driver_verified_details
from debug import log_debug_message

ride_routes=Blueprint('ride',__name__)


@ride_routes.route('/create_ride',methods=['POST'])
@token_required
def create_ride():
    try:
        data = request.get_json()
        driver_id = data.get('driver_id')
        o_la = data.get('origin_lat')
        o_lo = data.get('origin_lon')
        o_addr=data.get('origin_addr')
        d_la = data.get('dest_lat')
        d_lo = data.get('dest_lon')
        d_addr=data.get('dest_addr')
        price= data.get('price')
        d_id=data.get('driver_id')
        u_id=data.get('user_id')
        msg=insert_location(o_la,o_lo,o_addr,d_la,d_lo,d_addr)
        if msg["message"]=="Success":
            msg=insert_ride(u_id,d_id,msg["ids"][0],msg["ids"][1],"requested",price)
        return msg
    except Exception as e:
        return {"message":str(e)}

@ride_routes.route('/get_driver_verified_details',methods=['GET'])
def get_driver_details():
    try:
        data = request.get_json()
        d_id=data.get('driver_id')
        msg=get_driver_verified_details(d_id)
        log_debug_message(msg)
        return msg
    except Exception as e:
        return {"message":str(e)}
    
