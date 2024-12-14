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


def check_ride_status(ride_id):
    """
    Checks if a ride is accepted or not based on its ride_status.

    Parameters:
        ride_id (int): The ID of the ride to fetch.

    Returns:
        dict: A message indicating if the ride is accepted or not.
    """
    try:
        # Initialize the database service
        db = DBService()
        
        # SQL query to fetch the ride_status for the given ride_id
        query_get_ride_status = """
        SELECT ride_status 
        FROM urbanloop.rides 
        WHERE ride_id = %s;
        """
        
        # Execute the query
        result = db.fetch_one(query_get_ride_status, [ride_id])
        db.close()
        
        if result:
            ride_status = result[0]
            if ride_status == "accepted":
                return {"message": "The ride is accepted."}
            else:
                return {"message": "The ride is not accepted."}
        else:
            return {"message": f"No ride found with ride_id={ride_id}."}
    
    except Exception as e:
        # Ensure the database connection is closed in case of an error
        if 'db' in locals():
            db.close()
        return {"message": str(e)}



def get_ride_info_by_mobile(mobile_number):
    """
    Fetches the ride information, including origin and destination details
    (latitude, longitude, and address) for a specific ride based on the user's mobile number.

    Parameters:
        mobile_number (str): The mobile number of the user.

    Returns:
        dict: Contains the ride_id, ride_status, origin location details, destination location details,
              or an appropriate message if no data is found.
    """
    try:
        # Initialize the database service
        db = DBService()

        # SQL query to join 'users', 'rides', and 'locations' tables based on provided SQL
        query_get_ride_info_with_locations = f"""
        SELECT r.id AS ride_id, r.ride_status, d.velc_no,d.vel_type,d.mobile_no,d.verified,
               r.origin_loc_id, r.dest_loc_id, r.price, 
               ol.latitude AS origin_latitude, ol.longitude AS origin_longitude, ol.address AS origin_address,
               dl.latitude AS dest_latitude, dl.longitude AS dest_longitude, dl.address AS dest_address
        FROM urbanloop.users u
        INNER JOIN urbanloop.rides r ON u.id = r.user_id
        LEFT JOIN urbanloop.locations ol ON r.origin_loc_id = ol.id
        LEFT JOIN urbanloop.locations dl ON r.dest_loc_id = dl.id
        LEFT JOIN urbanloop.drivers d on r.driver_id= d.id
        WHERE u.mobile_number = %s and r.ride_status="requested" or r.ride_status="accepted"
        """
        
        # Execute the query with the mobile number as input
        result = db.fetch_one_record(query_get_ride_info_with_locations, [mobile_number])
        log_debug_message(result)
        if result:
            {
                "ride_id":result["ride_id"]
            }
            return result
        else:
            return {"message": f"No ride found for mobile number {mobile_number}."}

    except Exception as e:
        # Ensure the database connection is closed in case of an error
        if 'db' in locals():
            db.close()
        return {"message": str(e)}
