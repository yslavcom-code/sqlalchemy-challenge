# Import the dependencies.
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///hawaii.sqlite")

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
app = Flask(__main__)

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
    return


@app.route("/api/v1.0/stations")
def stations():
    # return all stations in json
    all_stations = session.query(Station.station).distinct().all()
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    return

if __main__ == '__main__':
    app.run(debug=True)