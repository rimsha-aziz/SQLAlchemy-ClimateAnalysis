import datetime as dt
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

###########################################
# Setup Database
###########################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

#Create references to Measurement and Station tables

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)
####################################
# Setup Flask app
####################################
app = Flask(__name__)

################################
#Setup Flask Routes
################################

@app.route("/")
def homepage():
    return(
          f"Available Routes:<br/>"
          f"/api/v1.0/precipitation<br/>"
          f"/api/v1.0/stations<br/>"
          f"/api/v1.0/tobs<br/>"
          f"/api/v1.0/<start><br/>"
          f"Returns an Average, Max, and Min temperature for a given start date in format of yyyy-mm-dd.<br/>"
          f"/api/v1.0/<start>/<end><br/>"
          f"Returns an Aveage Max, and Min temperature for a given start -end range in format of yyyy-mm-dd.<br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query all Measurments
    results = session.query(Measurement).all()
    session.close()
    # Create a dictionary
    precip = []
    for result in results:
        precip_dict = {}
        precip_dict["date"] = result.date
        precip_dict["prcp"] = result.prcp
        precip.append(precip_dict)
    # Jsonify summary
    return jsonify (precip)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #Query all Stations
    results = session.query(Station.name).all()
    session.close()
    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Find last date in database then subtract one year
    #Query
    temp_obs = session.query(Measurement.date,Measurement.tobs)\
        .filter(Measurement.station == "USC00519281")\
        .filter(Measurement.date >= "2016-08-23")\
        .order_by(Measurement.date).all()
    # Convert list of tuples into normal list
    t_obs = list(np.ravel(temp_obs))
    return jsonify(t_obs)

@app.route("/api/v1.0/<start>")
def start_day(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #Query of functions
    start_day = session.query(Measurement.date,func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start)\
        .group_by(Measurement.date).all()
     # Convert List of Tuples Into Normal List
    start_tuple = list(start_day)
    # Return JSON List of Min Temp, Avg Temp and Max Temp for a given start date
    return jsonify(start_tuple)

@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #Query of functions
    start_end_day = session.query(Measurement.date,func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start)\
        .filter(Measurement.date <= end)\
        .group_by(Measurement.date).all()
     # Convert List of Tuples Into Normal List
    start_end_tuple = list(start_end_day)
    # Return JSON List of Min Temp, Avg Temp and Max Temp for a given start and end date
    return jsonify(start_end_tuple)

if __name__=='__main__':
    app.run(debug=True)









