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
        update_driver_availability_by_ride_False(ride_id)
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
        update_driver_availability_by_ride_True(ride_id)
        db.close()
        return {"message": "Ride marked as completed successfully"}
    except Exception as e:
        if 'db' in locals():
            db.close()
        return {"message": str(e)}


def start_ride(ride_id):
    try:
        # Initialize the database service
        db = DBService()
        
        # SQL query to update the ride status and started_at
        query_start_ride = """
        UPDATE urbanloop.rides
        SET ride_status = 'started', started_at = NOW()
        WHERE id = %s;
        """
        
        # Execute the query with the provided ride_id
        result = db.execute_query(query_start_ride, [ride_id])
        
        # Close the database connection
        db.close()
        
        return {"message": "Ride marked as started successfully"}
    except Exception as e:
        # Ensure the database connection is closed in case of an error
        if 'db' in locals():
            db.close()
        return {"message": str(e)}


def complete_ride(ride_id):
    try:
        # Initialize the database service
        db = DBService()
        
        # SQL query to update the ride status and started_at
        query_start_ride = """
        UPDATE urbanloop.rides
        SET ride_status = 'completed', completed_at = NOW()
        WHERE id = %s;
        """
        
        # Execute the query with the provided ride_id
        result = db.execute_query(query_start_ride, [ride_id])
        update_driver_availability_by_ride_True(ride_id)
        # Close the database connection
        db.close()
        
        return {"message": "Ride marked as started successfully"}
    except Exception as e:
        # Ensure the database connection is closed in case of an error
        if 'db' in locals():
            db.close()
        return {"message": str(e)}
    


def get_driverride_info_by_mobile(mobile_number):
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
        SELECT r.id AS ride_id, r.ride_status, 
               r.origin_loc_id, r.dest_loc_id, r.price, 
               ol.latitude AS origin_latitude, ol.longitude AS origin_longitude, ol.address AS origin_address,
               dl.latitude AS dest_latitude, dl.longitude AS dest_longitude, dl.address AS dest_address
        FROM urbanloop.drivers d
        INNER JOIN urbanloop.rides r ON d.id = r.driver_id
        LEFT JOIN urbanloop.locations ol ON r.origin_loc_id = ol.id
        LEFT JOIN urbanloop.locations dl ON r.dest_loc_id = dl.id
        WHERE d.mobile_no = %s and r.ride_status!="completed" and r.ride_status!="cancelled" and r.ride_status!="requested"
        order by r.created_at desc limit 1

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



def get_driver_id_by_mobile(mobile_number):
    """
    Fetches the driver ID from the drivers table using the mobile number.

    Parameters:
        mobile_number (str): The mobile number of the driver.

    Returns:
        dict: Contains the driver ID or an appropriate message if no record is found.
    """
    try:
        # Initialize the database service
        db = DBService()

        # SQL query to get the driver ID
        query_get_driver_id = """
        SELECT id,velc_no,vel_type
        FROM urbanloop.drivers 
        WHERE mobile_no = %s;
        """

        # Execute the query with the provided mobile number
        result = db.fetch_one_record(query_get_driver_id, [mobile_number])
        

        if result:
            return {"driver_id": result["id"],
                    "vel_no":result["velc_no"],
                    "vel_type":result["vel_type"]
                    }
        else:
            return {"message": f"No driver found with mobile number {mobile_number}."}

    except Exception as e:
        # Ensure the database connection is closed in case of an error
        if 'db' in locals():
            db.close()
        return {"message": str(e)}


def is_driver_id_present(driver_id):
    """
    Checks if a driver ID exists in the drivers table.

    Parameters:
        driver_id (int): The ID of the driver to check.

    Returns:
        dict: Indicates whether the driver ID exists or not.
    """
    try:
        # Initialize the database service
        db = DBService()

        # SQL query to check for driver ID
        query_check_driver_id = """
        SELECT COUNT(1)  as cnt
        FROM urbanloop.drivers 
        WHERE id = %s;
        """

        # Execute the query
        result = db.fetch_one_record(query_check_driver_id, [driver_id])
        

        # Check if the count is greater than zero
        if result and result["cnt"] > 0:
            return {"exists": True, "message": f"Driver ID {driver_id} exists."}
        else:
            return {"exists": False, "message": f"Driver ID {driver_id} does not exist."}

    except Exception as e:
        # Ensure the database connection is closed in case of an error
        if 'db' in locals():
            db.close()
        return {"message": str(e)}



def update_driver_availability_by_ride_False(ride_id):
    try:
        db = DBService()
        query = """
        UPDATE urbanloop.drivers
        SET is_available = FALSE
        WHERE id = (
            SELECT driver_id
            FROM urbanloop.rides
            WHERE id = %s
        );
        """
        db.execute_query(query, [ride_id])
        return {"message": "Driver availability updated successfully."}
    except Exception as e:
        if 'db' in locals():
            db.close()
        return {"message": f"Error updating driver availability: {str(e)}"}


def update_driver_availability_by_ride_True(ride_id):
    try:
        db = DBService()
        query = """
        UPDATE urbanloop.drivers
        SET is_available = True
        WHERE id = (
            SELECT driver_id
            FROM urbanloop.rides
            WHERE id = %s
        );
        """
        db.execute_query(query, [ride_id])
        return {"message": "Driver availability updated successfully."}
    except Exception as e:
        if 'db' in locals():
            db.close()
        return {"message": f"Error updating driver availability: {str(e)}"}
