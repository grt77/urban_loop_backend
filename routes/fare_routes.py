from flask import Blueprint,request,jsonify
from Services.fare_services import fare_calc_auto

fare_routes=Blueprint('fare',__name__)


@fare_routes.route('/get_auto_fare',methods=['GET'])
def get_auto_fare():
    try:
        data=request.get_json()
        o_la = data.get('origin_lat')
        o_lo = data.get('origin_lon')
        d_la = data.get('dest_lat')
        d_lo = data.get('dest_lon')
        msg=fare_calc_auto(o_la,o_lo,d_la,d_lo)
        return msg
    except Exception as e:
        return {"message":str(e)}


