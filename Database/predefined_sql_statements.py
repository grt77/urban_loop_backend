insert_query_intial_login = """
INSERT INTO urbanloop.users (mobile_number, otp, otp_updated_at)
VALUES (%s, %s, NOW())
"""


update_otp_already_existing_user="""
UPDATE urbanloop.users
                SET otp = %s, otp_updated_at = NOW()
                WHERE mobile_number = %s
                """

get_otp_statement="""
SELECT otp, NOW()-otp_updated_at as expiry_time
            FROM urbanloop.users
            WHERE mobile_number = %s
"""


location_creation_query = """
            INSERT INTO urbanloop.locations (id, latitude, longitude, address)
            VALUES (%s, %s, %s, %s)
        """
ride_creation_query = """
        INSERT INTO urbanloop.rides (user_id, driver_id, origin_loc_id, dest_loc_id, ride_status, price)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

driver_status_query = """
            SELECT verified,is_available
            FROM urbanloop.drivers 
            WHERE id = %s   """

get_user_id_stmt="""

SELECT id 
    FROM urbanloop.users 
    WHERE mobile_number = %s

"""