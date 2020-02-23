# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
from flask import Flask, jsonify
import datetime as dt
import numpy as np

engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)
### Explore Database

Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)


@app.route("/")
def climate_analysis():
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def prcp_analysis():
    last12mos = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    result = (
        session.query(Measurement.date, Measurement.prcp)
        .filter(Measurement.date >= last12mos)
        .all()
    )
    prcp_dict = {}
    for data in result:
        prcp_dict[data[0]] = data[1]
    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    station = session.query(Station.station).all()
    station_list = list(np.ravel(station))
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs_analysis():
    tobs12mos = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    result = (
        session.query(Measurement.date, Measurement.tobs)
        .filter(Measurement.date >= tobs12mos)
        .all()
    )
    tobs_dict = {}
    for data in result:
        tobs_dict[data[0]] = data[1]
    return jsonify(tobs_dict)


@app.route("/api/v1.0/<start>")
def startdate_analysis(start):
    result = (
        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs),
        )
        .filter(Measurement.date >= start)
        .all()
    )
    startdate = list(np.ravel(result))
    return jsonify(startdate)


@app.route("/api/v1.0/<start>/<end>")
def start_to_end(start=None, end=None):
    result = (
        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs),
        )
        .filter(Measurement.date >= start)
        .filter(Measurement.date <= end)
        .all()
    )
    start_to_end = list(np.ravel(result))
    return jsonify(start_to_end)


if __name__ == "__main__":
    app.run(port=5500)
