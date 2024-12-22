from flask import Blueprint,request,jsonify
from Services.otp_service import send_otp,generate_otp,verify_otp
from Database.dbclass import DBService
from Database.predefined_sql_statements import insert_query_intial_login
from Services.auth_service import get_token
from debug import log_debug_message


otp_routes=Blueprint('otp',__name__)

@otp_routes.route('/send_otp',methods=['POST'])
def send_otp_route():
    try:
        db=DBService()
        data=request.get_json()
        mobile_number=data.get('mobile_number')
        if not mobile_number:
            return jsonify({"error": "Mobile number is required"}), 400
        otp = generate_otp()
        #otp = 123456
        resp=send_otp(mobile_number, otp) 
        result = db.execute_query_insert_otp_login(insert_query_intial_login, [mobile_number,otp])
        resp={'success':result["message"],'failure':None} #need to comment
        if resp['success'] is not None:
            message="Success:-"+resp['success']
        else:
            message="Failure:Msg-"+resp['failure']
        db.close()
        return jsonify({"message": message})
    except Exception as e:
        db.close
        return jsonify({'message':str(e)})

@otp_routes.route('/verify_otp',methods=['POST'])
def verify_otp_route():
    try:
        data=request.get_json()
        mobile_number=data.get('mobile_number')
        otp=data.get('otp')
        log_debug_message(otp)
        resp=verify_otp(mobile_number,otp)
        if resp["message"]=="Validated":
            token=get_token(mobile_number)
            resp["Auth"]=token
        return resp
    except Exception as e:
        return {"message": str(e)}
