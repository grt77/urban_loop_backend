from uuid import uuid4
from Database.dbclass import DBService
from Database.predefined_sql_statements import location_creation_query,ride_creation_query,driver_status_query
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



