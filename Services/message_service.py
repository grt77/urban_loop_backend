from twilio.rest import Client
import random
import os
from  dotenv import load_dotenv
from Database.dbclass import DBService
from Database.predefined_sql_statements import get_otp_statement,get_driver_otp_statement
from datetime import datetime,timedelta
from debug import log_debug_message

def send_text_message(mobile_number, message):
    try:
        load_dotenv()
        print("mobilenumber",mobile_number)
        log_debug_message(message)
        account_sid = "ACeaba03cb12299f946d5f8727eb3b850c"
        auth_token = "11cee6b8989e1527efbe565e79278474"
        from_number = "+15615302541"
        client = Client(account_sid,auth_token)
        log_debug_message(f'+91{mobile_number}')
        message = client.messages.create(
            body=message,
            from_=from_number,
            to=f'+91{mobile_number}'
        )
        print(message)
        log_debug_message(message)
        return {'success':message.sid,'failure':None}
    except Exception as e:
        log_debug_message(e)
        return(
            {
                "success":None,
                'failure':str(e)
            }
        )



def send_whatsapp_message(phno, msg):
    try:
        load_dotenv()
        account_sid = "ACeaba03cb12299f946d5f8727eb3b850c"
        auth_token = "11cee6b8989e1527efbe565e79278474"
        from_number = "whatsapp:+14155238886"
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=msg,                      
            from_=from_number,             
            to=f'+91{phno}'                
        )
        return {'success': message.sid, 'failure': None}
    except Exception as e:
        return {'success': None, 'failure': str(e)}







def get_user_mobile_num(id):
    try:
        db = DBService()
        query = f"""
        select mobile_number from urbanloop.users
        WHERE id = %s 
        """
        result = db.fetch_one_record(query, [id])
        if result:
            return result["mobile_number"]
        else:
            return None
    except Exception as e:
        return None
    

def get_driver_mobile_num(id):
    try:
        db = DBService()
        query = f"""
        select mobile_no from urbanloop.drivers
        WHERE id = %s 
        """
        result = db.fetch_one_record(query, [id])
        if result:
            return result["mobile_no"]
        else:
            return None
    except Exception as e:
        return None

def get_driver_mobile_from_rides(driver_id):
    try:
          # Push Flask app context
        db = DBService()
        query = """
        SELECT d.mobile_no 
        FROM urbanloop.rides r
        INNER JOIN urbanloop.drivers d ON r.driver_id = d.id
        WHERE r.id = %s
        """
        result = db.fetch_one_record(query, [driver_id])
        if result:
            return result["mobile_no"]
        else:
            print(f"No mobile number found for driver with id: {driver_id}")
            return None
    except Exception as e:
        print(f"Error in get_driver_mobile_from_rides: {e}")
        return None

    
def get_user_mobile_from_rides(user_id):
    try:
        db = DBService()
        query = """
        SELECT u.mobile_number as mobile_number
        FROM urbanloop.rides r
        INNER JOIN urbanloop.users u ON r.user_id = u.id
        WHERE r.id = %s
        """
        result = db.fetch_one_record(query, [user_id])
        if result:
            log_debug_message(result["mobile_number"])
            return result["mobile_number"]
        else:
            print(f"No mobile number found for user with id: {user_id}")
            return None
    except Exception as e:
        print(f"Error in get_user_mobile_from_rides: {e}")
        return None
