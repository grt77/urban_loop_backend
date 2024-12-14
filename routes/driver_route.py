from flask import Blueprint,request,jsonify
from Services.otp_service import send_otp,generate_otp,verify_otp,verify_otp_driver
from Database.predefined_sql_statements import update_otp_details
from Database.dbclass import DBService
from Services.auth_service import get_token,token_required
from Services.driver_services import get_ride_details,accept_ride_and_cancel_others,complete_ride,start_ride,get_driverride_info_by_mobile


driver_routes=Blueprint('driver',__name__)

@driver_routes.route('/send_otp',methods=['POST'])
def send_otp_route():
    try:
        db=DBService()
        data=request.get_json()
        mobile_number=data.get('mobile_number')
        if not mobile_number:
            return jsonify({"error": "Mobile number is required"}), 400
        # otp = generate_otp()
        otp = 123456
        #resp=send_otp(mobile_number, otp) 
        result=db.execute_query_with_rowcount(update_otp_details,[otp,mobile_number])
        db.close()
        if result["rowcount"] > 0:
            return jsonify({"message": "Success"}), 200
        else:
            return jsonify({"message": "No driver found"}), 404
    except Exception as e:
        db.close
        return jsonify({'message':str(e)})
    
@driver_routes.route('/verify_otp',methods=['POST'])
def verify_otp_route():
    try:
        data=request.get_json()
        mobile_number=data.get('mobile_number')
        otp=data.get('otp')
        resp=verify_otp_driver(mobile_number,otp)
        if resp["message"]=="Validated":
            token=get_token(mobile_number)
            resp["Auth"]=token
        return resp
    except Exception as e:
        return {"message": str(e)}
    

@driver_routes.route('/get_present_rides',methods=['POST'])
#@token_required
def get_present_rides():
    try:
        data=request.get_json()
        mobile_number=data.get('mobile_number')
        result=get_ride_details(mobile_number)
        return result
    except Exception as e:
        return {"message":str(e)}


@driver_routes.route('/accept_ride_id_reject_rem',methods=['POST'])
def accept_ride_id():
    try:
        data=request.get_json()
        ride_id=data.get('ride_id')
        driver_id=data.get('driver_id')
        result=accept_ride_and_cancel_others(ride_id,driver_id)
        return result
    except Exception as e:
        return {"message":str(e)}
    



@driver_routes.route('/ride_complete',methods=['POST'])
def ride_complete():
    try:
        data=request.get_json()
        ride_id=data.get('ride_id')
        result=complete_ride(ride_id)
        return result
    except Exception as e:
        return {"message":str(e)}
    
@driver_routes.route('/startRide',methods=['POST'])
def startRide():
    try:
        data=request.get_json()
        ride_id=data.get('ride_id')
        result=start_ride(ride_id)
        return result
    except Exception as e:
        return {"message":str(e)}
    

@driver_routes.route('/getdriverride_info',methods=['POST'])
def get_rider_ride_info():
    try:
        data=request.get_json()
        mobile_num=data.get('mobile_num')
        result=get_driverride_info_by_mobile(mobile_num)
        return result
    except Exception as e:
        return {"message":str(e)}