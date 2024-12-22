from twilio.rest import Client
import random
import os
from  dotenv import load_dotenv
from Database.dbclass import DBService
from Database.predefined_sql_statements import get_otp_statement,get_driver_otp_statement
from datetime import datetime,timedelta
from debug import log_debug_message


def generate_otp():
    return random.randint(100000, 999999)

def send_otp(mobile_number, otp):
    try:
        load_dotenv()
        log_debug_message(mobile_number)
        log_debug_message(otp)
        account_sid = "ACeaba03cb12299f946d5f8727eb3b850c"
        auth_token = "11cee6b8989e1527efbe565e79278474"
        from_number = "+15615302541"
        client = Client(account_sid,auth_token)
        log_debug_message(client)
        message = client.messages.create(
            body=f"Your OTP from Urbanloop is {otp}. Valid for 5 minutes ,Please do not share it with anyone.",
            from_=from_number,
            to=f'+91{mobile_number}'
        )
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
def verify_otp(mobile_number,otp):
    try:
        db=DBService()
        otp_resp=db.fetch_one_record(get_otp_statement,[mobile_number])
        message="unknown error"
        if int(otp_resp['otp'])==otp:
            if otp_resp['expiry_time']<=350:
                message="Validated"
            else:
                message="Expired"
        else:
            message="Invalid OTP"
        return {"message":message}
    except Exception as e:
        return {message:str(e)}


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



def verify_otp_driver(mobile_number,otp):
    try:
        db=DBService()
        otp_resp=db.fetch_one_record(get_driver_otp_statement,[mobile_number])
        message="unknown error"
        if int(otp_resp['otp'])==otp:
            if otp_resp['expiry_time']<=350:
                message="Validated"
            else:
                message="Expired"
        else:
            message="Invalid OTP"
        return {"message":message}
    except Exception as e:
        return {message:str(e)}
