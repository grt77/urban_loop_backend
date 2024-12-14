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

update_otp_details = """
UPDATE urbanloop.drivers 
SET otp = %s, 
    otp_CreatedAt = NOW()
WHERE mobile_no = %s;
"""


get_driver_otp_statement="""
SELECT otp, NOW()-otp_CreatedAt as expiry_time
            FROM urbanloop.drivers
            WHERE mobile_no = %s
"""

get_ride_detials="""

SELECT 
    r.id AS ride_id,
    r.ride_status,
    r.price,
    origin.latitude AS origin_latitude, 
    origin.longitude AS origin_longitude, 
    origin.address as orgin_address,
    destination.address as dest_address,
    destination.latitude AS dest_latitude, 
    destination.longitude AS dest_longitude,
    u.mobile_number AS user_mobile,
    d.mobile_no AS driver_mobile
FROM urbanloop.rides r
JOIN urbanloop.drivers d ON r.driver_id = d.id
JOIN urbanloop.users u ON u.id = r.user_id
JOIN urbanloop.locations origin ON r.origin_loc_id = origin.id
JOIN urbanloop.locations destination ON r.dest_loc_id = destination.id
WHERE d.mobile_no = %s
  AND r.ride_status = "requested"
"""
# --AND TIMESTAMPDIFF(MINUTE, r.created_at, NOW()) < 120;


get_requetsed_rides="""
SELECT COUNT(*) AS ride_count 
        FROM urbanloop.rides 
        WHERE id = %s 
          AND ride_status = "requested"
"""

cancel_ride_with_id = """
        UPDATE urbanloop.rides 
        SET ride_status = 'cancelled', 
            cancelled_at = NOW()
        WHERE id = %s;
        """