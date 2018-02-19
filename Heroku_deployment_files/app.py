# Import dependencies
from flask import Flask, render_template, jsonify, request, redirect

import os
import pandas as pd

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

app = Flask(__name__)
#############################################################################
# USING PANDAS TO COLLECT DATA
#############################################################################
# _csvpath = os.path.join('DataSets', 'belly_button_biodiversity_samples.csv')
# #_csvpath = os.path.join('belly_button_biodiversity_samples.csv')
# _data = pd.read_csv(_csvpath)
# column_names = list(_data.columns)
# del column_names[0]
#############################################################################
# USING SQLALCHEMY TO FIND THE sample names -- **IMPORTANT NOTE** - if running
# queries OUTSIDE of app function, it will create a different thread, thereby
# running another query INSIDE the app function will require another connection
# to the DB.  **IMPORTANT NOTE**
##############################################################################

if not os.path.exists('DataSets/belly_button_biodiversity.sqlite'):
    raise FileNotFoundError("The bb-sqlite-file does not exist")
engine = create_engine("sqlite:///DataSets/belly_button_biodiversity.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Samples = Base.classes.samples
Samples_meta = Base.classes.samples_metadata
Samples_otu = Base.classes.otu

session = Session(engine)

# sample_names = Samples.__table__.columns.keys()
# del sample_names[0]

##############################################################################
# USING SQLALCHEMY TO FIND THE sample otu
# **IMPORTANT NOTE** - if running
# queries OUTSIDE of app function, it will create a different thread, thereby
# running another query INSIDE the app function will require another connection
# to the DB.  **IMPORTANT NOTE**
##############################################################################

# Samples_otu = Base.classes.otu
# otu_query = session.query(Samples_otu.lowest_taxonomic_unit_found)

# otu_list = []
# for each in otu_query:
#     otu_list.append(each[0])

#################################################
# Flask Setup
#################################################


#################################################
# Routes
#################################################

# Main route 
@app.route('/')
def home():
    return render_template('index.html', text = "Use the interactive charts to explore the dataset", 
    text2 = "Belly Button Analysis")

@app.route('/names')
def names():

    sample_names = Samples.__table__.columns.keys()
    del sample_names[0]
    return jsonify(sample_names)

@app.route('/otu')
def otu_names():

    otu_query = session.query(Samples_otu.lowest_taxonomic_unit_found).all()

    otu_list = []

    for each in otu_query:
        otu_list.append(each[0])
    return jsonify(otu_list)


@app.route('/metadata/<sample>')
def metasample(sample):
#################################################################################
    # **See important notes above**
    # engine = create_engine("sqlite:///DataSets/belly_button_biodiversity.sqlite")
    # session = Session(engine)
    # Base = automap_base()
    # Base.prepare(engine, reflect=True)
    # Samples_meta = Base.classes.samples_metadata
    # **See important notes above**
#################################################################################
    sample_split = sample.split("_")
    sample_num = int(sample_split[1])

    results = (session.query(Samples_meta.AGE, Samples_meta.BBTYPE, Samples_meta.ETHNICITY, 
                        Samples_meta.GENDER, Samples_meta.LOCATION, Samples_meta.SAMPLEID).filter(
                            Samples_meta.SAMPLEID == sample_num).all())

    sample_result_list = []
    for result in results:
        result_dict = {}
        result_dict["age"] = int(result[0])
        result_dict["bbtype"] = result[1]
        result_dict["ethnicity"] = result[2]
        result_dict["gender"] = result[3]
        result_dict["location"] = result[4]
        result_dict["sampleid"] = result[5]
        sample_result_list.append(result_dict)
    
    return jsonify(sample_result_list)

@app.route('/wfreq/<sample>')
def washingfreq(sample):
    sample_split = sample.split("_")
    sample_num = int(sample_split[1])

    results = (session.query(Samples_meta.WFREQ, Samples_meta.SAMPLEID).filter(
                            Samples_meta.SAMPLEID == sample_num).all())

    wfreq_result_list = []
    for result in results:
        result_dict = {}
        result_dict[sample] = int(result[0])
        wfreq_result_list.append(result_dict)

    return jsonify(result_dict)

@app.route('/samples/<sample>')
def samples(sample):
    csvpath = os.path.join('DataSets', 'belly_button_biodiversity_samples.csv')
    data_df = pd.read_csv(csvpath)
    data_df = data_df[['otu_id', sample]]
    data_df = data_df.loc[data_df[sample] > 0]
    data_df.reset_index(inplace = True)
    data_df = data_df.sort_values(sample, ascending=False)
    data_df_dict = {}
    data_df_dict["otu_ids"] = data_df['otu_id'].tolist()
    data_df_dict["sample_values"] = data_df[sample].tolist()

    return jsonify([data_df_dict])



if __name__ == "__main__":
    app.run(debug=True)
