# Import the dependencies.
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

import datetime as dt

import numpy as np
#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# utility code
def get_most_recent_date_dt(session):
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date_dt = dt.datetime.strptime(most_recent_date, "%Y-%m-%d")
    return most_recent_date_dt

def get_start_date(session):
    start_date = get_most_recent_date_dt(session) - dt.timedelta(days=365)
    return start_date
#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
        )

@app.route("/api/v1.0/precipitation")
def precipitations():
    precipitation_data = (
        session.query(Measurement.date, Measurement.prcp)
        .filter(Measurement.date >= get_start_date(session))
        .all()
    )
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    # return all stations in json
    all_stations = session.query(Station.station).distinct().all()
    station_list = [station[0] for station in all_stations]
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    active_stations = (
        session.query(Measurement.station, func.count(Measurement.station).label("count"))
        .group_by(Measurement.station)
        .order_by(sqlalchemy.desc("count"))
        .all()
    )
    most_active_station_id = active_stations[0][0]

    start_date = get_start_date(session)
    
    tobs_data = (
        session.query(Measurement.date, Measurement.tobs)
        .filter(Measurement.station == most_active_station_id)
        .filter(Measurement.date >= start_date)
        .all()
        )
    tobs_list = [{"date": date, "tobs": tobs} for date, tobs in tobs_data]
    return jsonify(tobs_list)

if __name__ == '__main__':
    app.run(debug=True)