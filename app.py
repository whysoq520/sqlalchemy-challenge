import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine =create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"/api/v1.0/start/<start><br/>"
        f"/api/v1.0/start/end/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #query
    session = Session(engine)
    result =session.query(Measurement.date, Measurement.prcp).all()
    prcp = dict(result)
    session.close()    
    return jsonify(prcp)
#using date as the key and prcp as the value.

@app.route("/api/v1.0/stations")
def stations():
    #query
    session=Session(engine)
    station=session.query(Measurement.station).all()
    
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

@app.route("/api/v1.0/start/<start_date>")
def weather(start_date):
    session = Session(engine)
    weather_condition = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    weather_since = list(np.ravel(weather_condition))
    session.close() 
    return jsonify(weather_since)





@app.route("/api/v1.0/start/end/<start>/<end>")
def condition(start, end):
    session = Session(engine)
    weather = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    weather_betweendates = list(np.ravel(weather))
        
    return jsonify(weather_betweendates)


if __name__ == "__main__":
    app.run(debug=True)