from flask import Blueprint,request,jsonify
from Services.otp_service import send_otp,generate_otp,verify_otp,verify_otp_driver
from Database.predefined_sql_statements import update_otp_details
from Database.dbclass import DBService
from Services.auth_service import get_token

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
        result=db.execute_query(update_otp_details,[otp,mobile_number])
        resp={'message':result["message"],'failure':None} #need to comment
        db.close()
        return jsonify({"message": resp})
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