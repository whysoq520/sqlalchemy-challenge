import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
# Flask Setup
app = Flask(__name__)

#List all routes that are available.
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> and /api/v1.0/<start>/<end>"
    )
# Flask Setup
app = Flask(__name__)


@app.route("/api/v1.0/precipitation")
def precipitation():
    #query
    session = Session(engine)
    prcp=session.query(Measurement.date, Measurement.prcp).all
    session.close()
    #create dictionary
    precipitation=[]
    for date, prcp in result:
        prcp_dict={date:prcp}
        precipitation.append(dict)
    return jsonify(precipitation)
#using date as the key and prcp as the value.


@app.route("/api/v1.0/stations")
def stations():
    #query
    session=Session(engine)
    station=session.query(Measurement.station).all()
    session.close()
    all_stations = list(np.ravel(station))
    session.close()

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    #query
    session = Session(engine)
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    year_ago =dt.date(2017,8,23)-dt.timedelta(days=365)
  
    results = session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.date<='2017-08-23').\
    filter(Measurement.date>='2016-08-23').all()
    tobs_lastyear = list(np.ravel(results))
    session.close()

    return jsonify(tobs_lastyear)

@app.route("/api/v1.0/startdate")
def weather(start_date):
    session = Session(engine)
    weather_condition = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    weather_since = list(np.ravel(weather_condition))
    session.close() 
    return jsonify(weather_since)

@app.route("/api/v1.0/<start>/<end>")
def weather(start_date, end_date):
    session = Session(engine)
    weather = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    weather_betweendates = list(np.ravel(weather))
        
    return jsonify(weather_betweendates)


if __name__ == "__main__":
    app.run(debug=True)