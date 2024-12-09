from Database.predefined_sql_statements import get_ride_detials
from Database.dbclass import DBService
from debug import log_debug_message
import json 

def get_ride_details(mobile_num):
    sql_stmt=get_ride_detials
    params=[mobile_num]
    db = DBService()
    results=db.fetch_all_records(sql_stmt,params)
    log_debug_message(results)
    if results:
            return json.dumps(results, default=str)  
    else:
        return json.dumps({"message": "No records found"})


def accept_ride_and_cancel_others(ride_id, driver_id):
    try:
        db = DBService()
        query_accept_ride = """
        UPDATE urbanloop.rides 
        SET ride_status = 'accepted', accepted_at = NOW() 
        WHERE id = %s AND driver_id = %s;
        """
        accept_result = db.execute_query(query_accept_ride, [ride_id, driver_id])
        query_cancel_other_rides = """
        UPDATE urbanloop.rides 
        SET ride_status = 'cancelled', cancelled_at = NOW() 
        WHERE driver_id = %s AND ride_status = 'requested' AND id != %s;
        """
        cancel_result = db.execute_query(query_cancel_other_rides, [driver_id, ride_id])
        db.close()
        return {"message": "Ride accepted and other requested rides cancelled successfully"}
    except Exception as e:
        if 'db' in locals():
            db.close()
        return {"message": str(e)}


def complete_ride(ride_id):
    try:
        db = DBService()
        query_complete_ride = """
        UPDATE urbanloop.rides 
        SET ride_status = 'completed', completed_at = NOW() 
        WHERE id = %s;
        """
        result = db.execute_query(query_complete_ride, [ride_id])
        db.close()
        return {"message": "Ride marked as completed successfully"}
    except Exception as e:
        if 'db' in locals():
            db.close()
        return {"message": str(e)}
