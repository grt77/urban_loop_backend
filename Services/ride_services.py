from uuid import uuid4
from Database.dbclass import DBService
from Database.predefined_sql_statements import location_creation_query,ride_creation_query,driver_status_query,get_user_id_stmt,get_requetsed_rides,cancel_ride_with_id
from debug import log_debug_message


def insert_location(o_la,o_lo,o_addr,d_la,d_lo,d_addr):
    try:
        db=DBService()
        o_id=str(uuid4())
        d_id=str(uuid4())
        query=location_creation_query
        o_msg=db.execute_query(query,[o_id,o_la,o_lo,o_addr])
        d_msg=db.execute_query(query,[d_id,d_la,d_lo,d_addr])
        log_debug_message(o_msg)
        db.close()
        if o_msg["message"]=="Success" and d_msg["message"]=="Success":
            return {"message":"Success","ids":[o_id,d_id]}
        return {"message":"Success"}
    except Exception as e:
        return {"message":"Success"}
    
def insert_ride(u_id,d_id,o_id,did,r_status,price):
    try:
        db=DBService()
        query=ride_creation_query
        msg=db.execute_query(query,[u_id,d_id,o_id,did,r_status,price])
        db.close()
        return msg
    except Exception as e:
        return {"message":str(e)}


def get_driver_verified_details(d_id):
    try:
        db=DBService()
        query=driver_status_query
        msg=db.fetch_one_record(query,[d_id])
        if msg is None:
            msg={"message":"Driver not found"}
        else:
            msg = {key: (True if value == 1 else False if value == 0 else value) for key, value in msg.items()}
        log_debug_message(msg)
        db.close()
        return msg
    except Exception as e:
        return {"message":str(e)}


def get_user_id(mobile_num):
    try:
        log_debug_message(mobile_num)
        db=DBService()
        sql_stmt=get_user_id_stmt
        msg=db.fetch_one_record(sql_stmt,[mobile_num])
        log_debug_message(msg)
        db.close()
        return msg
    except Exception as e:
        return {"error":str(e)}
    
def get_no_of_requested_ride(id):
    try:
        db=DBService()
        sql_stmt=get_requetsed_rides
        result=db.fetch_one_record_with_result(sql_stmt,[id])
        if result and "ride_count" in result:
            return {"ride_count": result["ride_count"]}
        else:
            return {"ride_count": 0}
    except Exception as e:
        return {"ride_count": 0,"Error":str(e)}

def cancel_ride(ride_id):
    try:
        db = DBService()
        query = cancel_ride_with_id
        result = db.execute_query_with_rowcount(query, [ride_id])
        db.close()
        if result["rowcount"] > 0:
            return {"message": "success"}
        else:
            return {"message": "No ride found with the provided ID"}
    except Exception as e:
        if 'db' in locals():
            db.close()
        return {"error": str(e)}
def cancel_rides_by_phone_number(phone_number):
    try:
        db = DBService()
        query_get_user_id = """
        SELECT id FROM urbanloop.users 
        WHERE mobile_number = %s;
        """
        user_result = db.fetch_one_record(query_get_user_id, [phone_number])
        if not user_result:
            db.close()
            return {"message": "No user found with the provided phone number"}
        user_id = user_result["id"]
        query_update_rides = """
        UPDATE urbanloop.rides 
        SET ride_status = 'cancelled', cancelled_at = NOW() 
        WHERE user_id = %s AND ride_status != 'cancelled';
        """
        update_result = db.execute_query(query_update_rides, [user_id])
        db.close()
        return {"message": "success"}
    except Exception as e:
        if 'db' in locals():
            db.close()
        return {"message": str(e)}
