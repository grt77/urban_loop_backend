import pymysql
import os
from dotenv import load_dotenv
from Database.predefined_sql_statements import update_otp_already_existing_user
from debug import log_debug_message

class DBService:
    def __init__(self):
        load_dotenv()  
        self.host = os.getenv("DATABASE_URI")
        self.user = os.getenv("DATABASE_USER")
        self.password = os.getenv("DATABASE_PWD")
        self.db_name = os.getenv("DATABASE_DB")
        self.connection = self.connect()

    def connect(self):
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

    def execute_query_insert_otp_login(self, query, params=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                return {'message': "New user:Otp send to Your mobile number"}
        except pymysql.MySQLError as e:
            if e.args[0] == 1062: #error code 
                with self.connection.cursor() as cursor:
                # If the mobile number already exists, update the OTP and OTP updated timestamp
                    cursor.execute(update_otp_already_existing_user, (params[1], params[0]))  # params[0] = mobile_number, params[1] = otp
                    self.connection.commit()
                    return {'message': "Existing user:OTP sent to your mobile number"}
            else:
                print(f"Error executing query: {e}")
                self.connection.rollback()
                return {'message': "Failure", 'error': str(e)}
    def fetch_one_record(self,query,params=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchone()
                log_debug_message(result)
            return result
        except pymysql.MySQLError as e:
            print(f"Error executing query: {e}")
            return None
    def execute_query(self,query,params=None):
        try:
            with self.connection.cursor() as cursor:
                log_debug_message(query)
                cursor.execute(query, params)
                self.connection.commit()
                return {"message":"Success"}
        except Exception as e:
            return {"message":str(e)}
    def close(self):
        if self.connection:
            self.connection.close()
        else:
            pass