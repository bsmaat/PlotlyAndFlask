from flask import Flask, render_template

import json
import plotly

import pandas as pd
import numpy as np

app = Flask(__name__)
app.debug = True

import sqlite3
import numpy as np
import plotly
from plotly import tools
import plotly.graph_objs as go

class SqlReader:

    def getTemperature(self):
        connection = sqlite3.connect('/home/pi/readings/data.db')
        cursor = connection.cursor()

        sql_command = """
        SELECT * from  climate;"""

        cursor.execute(sql_command)
        result = cursor.fetchall()

        cursor.close()
        return result


@app.route('/')
def index():
    sql = SqlReader()
    result = sql.getTemperature()

    numOfPoints = len(result)

    temperature = [yValues[1] for yValues in result]
    humidity = [yValues[2] for yValues in result]
    xValues = [xValues[0] for xValues in result]


    graphs = [
        dict(
            data=[
                dict(
                    x=xValues,
                    y=temperature,
                    type='scatter'
                ),
            ],
            layout=dict(
                title='Temperature vs Time'
            )
        ),

        dict(
            data=[
                dict(
                    x=xValues,
                    y=humidity,
                    type='scatter'
                ),
            ],
            layout=dict(
                title='Humidity vs Time'
            )
        )
    ]

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['Graph {}'.format(i) for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('layouts/index.html',
                           ids=ids,
                           graphJSON=graphJSON)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)
