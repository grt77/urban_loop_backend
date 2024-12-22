from twilio.rest import Client
import random
import os
from  dotenv import load_dotenv
from Database.dbclass import DBService
from Database.predefined_sql_statements import get_otp_statement,get_driver_otp_statement
from datetime import datetime,timedelta
from run import app

def send_text_message(mobile_number, message):
    try:
        load_dotenv()
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_number = os.getenv("TWILIO_PHONE_NUMBER")
        client = Client(account_sid,auth_token)
        message = client.messages.create(
            body=message,
            from_=from_number,
            to=f'+91{mobile_number}'
        )
        return {'success':message.sid,'failure':None}
    except Exception as e:
        return(
            {
                "success":None,
                'failure':str(e)
            }
        )



def send_whatsapp_message(phno, msg):
    try:
        load_dotenv()
        account_sid = os.getenv("TWILIO_ACCOUNT_SID") 
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")    
        from_number = os.getenv("TWILIO_WHATSAPP_NUMBER") 
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
        query = """
        SELECT mobile_number 
        FROM urbanloop.users
        WHERE id = %s
        """
        result = db.fetch_one_record(query, [id])
        if result:
            return result["mobile_number"]
        else:
            print(f"No mobile number found for user with id: {id}")
            return None
    except Exception as e:
        print(f"Error in get_user_mobile_num: {e}")
        return None
    

def get_driver_mobile_num(id):
    try:
        db = DBService()
        query = """
        SELECT mobile_no 
        FROM urbanloop.drivers
        WHERE id = %s
        """
        result = db.fetch_one_record(query, [id])
        if result:
            return result["mobile_no"]
        else:
            print(f"No mobile number found for driver with id: {id}")
            return None
    except Exception as e:
        print(f"Error in get_driver_mobile_num: {e}")
        return None

    
print(get_driver_mobile_num("973239d3-a8f3-11ef-992f-06e09a310733"))
print(get_user_mobile_num("4083a584-beec-11ef-992f-06e09a310733"))