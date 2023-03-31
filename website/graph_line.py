"""
This is a Flask Blueprint module that generates line charts from data
read from a CSV file.
'read_csv' is a function from the 'website.datas' module that reads
data from a CSV file.
'create_line_chart' is a function from the 'website.create_graph_line'
module that takes in
data and creates a line chart object.
"""
from flask import Blueprint, render_template
from website.datas import read_csv
from website.create_graph_line import create_line_chart

graph_line = Blueprint('graph_line', __name__)


@graph_line.route('/chartJS-line')
def line_graph():
    """
    This function renders the line graph in Chart.js using the CSV file.

    :return: Render in chartJS-line.html template
    """
    datas = read_csv()
    return render_template('chartJS-line.html', data=datas)


@graph_line.route('/chart-line')
def line_chart():
    """
    This function creates a line chart object using the CSV file. The values
    after reading the CSV file separated in year, exports and imports; which
    is then passed as a parameter in 'create_line_chart' function.

    :return: Render in chart-line.html template
    """
    data = read_csv()

    year = [row[0] for row in data]
    exports = [row[1] for row in data]
    imports = [row[2] for row in data]

    chart = create_line_chart(year, exports, imports)

    return render_template('chart-line.html', graph=chart)
