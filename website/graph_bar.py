"""
This is a Flask Blueprint module that generates bar charts from data read
from a CSV file.
'read_csv' is a function from the 'website.datas' module that reads data
from a CSV file.
'create_bar_chart' is a function from the 'website.create_graph_bar' module
 that takes in
data and creates a bar chart object.
"""
from flask import Blueprint, render_template
from website.datas import read_csv
from website.create_graph_bar import create_bar_chart

graph_bar = Blueprint('graph_bar', __name__)


@graph_bar.route('/chartJS-bar')
def bar_graph():
    """
    This function renders the bar graph in Chart.js using the CSV file.

    :return: Render in chartJS-bar.html template
    """
    datas = read_csv()
    return render_template('chartJS-bar.html', data=datas)


@graph_bar.route('/chart-bar')
def bar_chart():
    """
    This function creates a bar chart object using the CSV file. The values
    after reading the CSV file is separated in year, exports and imports;
    which is then passed as a parameter in 'create_bar_chart' function.

    :return: Render in chart-bar.html template
    """
    data = read_csv()

    year = [row[0] for row in data]
    exports = [row[1] for row in data]
    imports = [row[2] for row in data]

    chart = create_bar_chart(year, exports, imports)

    return render_template('chart-bar.html', graph=chart)
