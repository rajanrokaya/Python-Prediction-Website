"""
This code imports 'create_app' function from website module. It creates an instance of a Flask
application by calling the function. The instance is assigned to the variable 'app'.
The web project is hosted in localhost with port 8000.
Debug is set to true, so that any changes made in the python project automatically re-runs the
web server.
"""
from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=8000)
