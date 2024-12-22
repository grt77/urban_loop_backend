from flask import Blueprint,request,jsonify
from Services.auth_service import token_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from Services.auth_service import token_required
from Services.ride_services import insert_location,insert_ride,get_driver_verified_details,get_user_id,get_no_of_requested_ride,cancel_ride,cancel_rides_by_phone_number,check_ride_status,get_ride_info_by_mobile
from debug import log_debug_message
from Services.message_service import send_text_message,send_whatsapp_message,get_driver_mobile_num,get_user_mobile_num,get_user_mobile_from_rides,get_driver_mobile_from_rides

ride_routes=Blueprint('ride',__name__)


@ride_routes.route('/create_ride',methods=['POST'])
#@token_required
def create_ride():
    try:
        data = request.get_json()
        print(data)
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
        user_mobile=data.get('user_mobile')
        if u_id is None:
            u_id=get_user_id(user_mobile)
        print("user_id::::::",u_id)
        send_text_message(str(get_user_mobile_num(u_id)),f"Ride is created for You from {o_addr} to {d_addr} with Rs.{price}")
        send_whatsapp_message(get_user_mobile_num(u_id),f"Ride is created for You from {o_addr} to {d_addr} with Rs.{price}")
        send_text_message(get_driver_mobile_num(d_id),f"New ride for You from {o_addr} to {d_addr} with {price} Rs, please click the link \"http://localhost:5173/driver/login\"")
        send_whatsapp_message(get_driver_mobile_num(d_id),f"New ride for You from {o_addr} to {d_addr} with {price} Rs, please click the link \"http://localhost:5173/driver/login\"")
        msg=insert_location(o_la,o_lo,o_addr,d_la,d_lo,d_addr)
        if msg["message"]=="Success":
            log_debug_message("rideeeeeeee.............")
            msg=insert_ride(u_id,d_id,msg["ids"][0],msg["ids"][1],"requested",price)
        return msg
    except Exception as e:
        return {"message":str(e)}

@ride_routes.route('/get_driver_verified_details',methods=['POST'])
def get_driver_details():
    try:
        data = request.get_json()
        d_id=data.get('driver_id')
        msg=get_driver_verified_details(d_id)
        log_debug_message(msg)
        return msg
    except Exception as e:
        return {"message":str(e)}
    
@ride_routes.route('/get_rider_id',methods=['POST'])
def get_rider_id():
    try:
        data = request.get_json()
        mbno=data.get('mbno')
        msg=get_user_id(mbno)
        return {"id":msg}
    except Exception as e:
        return {"error":str(e)}


@ride_routes.route('/can_ride_created',methods=['POST'])
def can_ride_created():
    try:
        data = request.get_json()
        id=data.get('id')
        result=get_no_of_requested_ride(id)
        return result
    except Exception as e:
        return {"Error":str(e)}
    
@ride_routes.route('/cancel_ride',methods=['POST'])
def cancel_ride_with_id():
    try:
        data = request.get_json()
        id=data.get('ride_id')
        result=cancel_ride(id)
        send_text_message(str(get_user_mobile_from_rides(id)),f"your Ride id is:{id}-Ride is cancelled by driver")
        send_whatsapp_message(str(get_user_mobile_from_rides(id)),f"your Ride id is:{id}-Ride is cancelled by the Driver")
        return result
    except Exception as e:
        return {"Error":str(e)}
    
@ride_routes.route('/cancel_rideby_phno',methods=['POST'])
def cancel_ride_with_phno():
    try:
        data = request.get_json()
        id=data.get('phno')
        result=cancel_rides_by_phone_number(id)
        return result
    except Exception as e:
        return {"Error":str(e)}

@ride_routes.route('/check_rider_status',methods=['POST'])
def check_rider_status():
    try:
        data = request.get_json()
        id=data.get('ride_id')
        result=check_ride_status(id)
        return result
    except Exception as e:
        return {"Error":str(e)}
    
@ride_routes.route('/get_rider_details',methods=['POST'])
def get_rider_details():
    try:
        data = request.get_json()
        id=data.get('mobile_num')
        result=get_ride_info_by_mobile(id)
        #log_debug_message(result)
        return result
    except Exception as e:
        return {"Error":str(e)}