from flask import Flask
from flask_cors import CORS
from routes.otp_routes import otp_routes
from routes.ride_routes import ride_routes
from routes.fare_routes import fare_routes
from routes.map_routes import map_routes
from routes.driver_route import driver_routes

import logging

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(otp_routes, url_prefix='/otp')
    app.register_blueprint(ride_routes,url_prefix='/ride')
    app.register_blueprint(fare_routes,url_prefix='/fare')
    app.register_blueprint(map_routes,url_prefix='/map')
    app.register_blueprint(driver_routes,url_prefix='/driver')
    return app

app = create_app()
app.logger.setLevel(logging.DEBUG)
    #app.run(host="0.0.0.0",port=8080,debug=True)
