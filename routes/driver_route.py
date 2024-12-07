from flask import Blueprint,request,jsonify
from Services.otp_service import send_otp,generate_otp,verify_otp
from Database.predefined_sql_statements import update_otp_details
from Database.dbclass import DBService

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