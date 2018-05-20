#Import libraries and dependecies

import numpy as np
import pandas as pd

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask_sqlalchemy import SQLAlchemy
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

app = Flask(__name__)

engine = create_engine('sqlite:///db/belly_button_biodiversity.sqlite', echo=False)
Base = automap_base()
Base.prepare(engine, reflect=True)

OTU = Base.classes.otu
Samples = Base.classes.samples
Metadata = Base.classes.samples_metadata

session = Session(engine)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/names")
def names():
    name_samples = session.query(Sample).statement
    name_samples_df = pd.read_sql_query(name_samples, session.bind)
    name_samples_df.set_indext('otu_id', inplace = True)
    return jsonify(list(all_samples_df.columns))

@app.route("/otu")
def otu():
    otu_query = session.query(OTU)
    otu = pd.read_sql(otu_query.statement, otu_query.session.bind)
    descriptions = otu.lowest_toxonomic_unit_found
    return(jsonify(descriptions.to_dict()))

@app.route("/metadata/<sample>")
def metadata(sample):
    sample_name = sample.replace("BB_", "")
    result = session.query(Samples_metadata.AGE, \
    Samples_metadata.BBTYPE, Samples_metadata.ETHNICITY, \
    Samples_metadata.GENDER, Samples_metadata.LOCATION, \
    Samples_metadata.SAMPLEID).filter_by(SAMPLEID = sample_name).all()
    record = result[0]
    record_dict = {
        "AGE": record[0],
        "BBTYPE": record[1],
        "ETHNICITY": record[2],
        "GENDER": record[3],
        "LOCATION": record[4],
        "SAMPLEID": record[5]
    }
    return jsonify(record_dict)

@app.route('/wfreq/<sample>')
def wash_freq(sample):
    sample_name = sample.replace("BB_", "")
    result = session.query(Samples_metadata.WFREQ).filter_by(SAMPLEID = sample_name).all()
    wash_freq = result[0][0]
    return jsonify(wash_freq)

@app.route('/samples/<sample>')
def otu_data(sample):
    sample_query = "Samples." + sample
    result = session.query(Semples.otu_id, sample_query).orger_by(desc(sample_query)).all()
    otu_ids = [result[x][0] for x in range(len(result))]
    sample_values = [result[x][1] for x in range(len(result))]
    dict_list = [{"otu_ids": otu_ids}, {"sample_values": sample_values}]
    return jsonify(dict_list)

if __name__ == "__main__":
    app.run(debug = True)