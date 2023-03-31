"""
This is a Flask Blueprint module that reads data from a CSV file and renders
in an HTML template.
'Blueprint' is a class from the Flask module, used to organize a group of
related views and other code.
'os' module is imported because it is used to work with the file system.
'csv' module is imported because it is used to read the contents of the CSV file.
'current_app' is a global variable used to construct the path to the CSV file.
'render_template' is a function from the Flask module used to render a template
and return the response.
"""
import os
import csv
from flask import Blueprint, current_app, render_template

datas = Blueprint('datas', __name__)


def read_csv():
    """
    This function reads data from 'exports-imports.csv' file located in 'scrapping'
    package, which is created by webscraping.

    The 'os.path.join()' function is used to construct a path to 'exports-imports.csv'
    file by combining the current application's root path, the parent directory of the
    current application, the 'scrapping' package, and the file name.

    The 'csv.reader()' function is used to create a CSV reader object that can be used
    to iterate over the rows of the file, and after reading, returns the rows as list
    of data. If the CSV file has not been created then it will throw an IOError.

    :return: List of lists containing data from the CSV file
    """
    data = []
    path = os.path.join(
        current_app.root_path, os.pardir,
        'scraping', 'exports-imports.csv'
    )
    try:
        with open(path, 'r', encoding='utf-8') as file_pointer:
            reader = csv.reader(file_pointer)
            for row in reader:
                data.append(row)
    except IOError:
        return f"Error: CSV file {path} might not have been created"
    return data


@datas.route('/datas')
def show_data():
    """
    This function renders the data from the CSV file on a template. If the CSV is not
    found, then it will throw a FileNotFoundError.

    :return: Render in data.html template
    """
    try:
        data = read_csv()
        return render_template('datas.html', data=data)
    except FileNotFoundError:
        return f"The file {data} is not found"
