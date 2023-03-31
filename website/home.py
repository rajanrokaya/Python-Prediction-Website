from flask import Blueprint, render_template, request
from deep_learning import prediction as pr

views = Blueprint('views', __name__)


@views.route('/', methods=['POST', 'GET'])
@views.route('/home')
def calculator():
    predict_import = ''
    predict_export = ''
    accuracy_import = ''
    accuracy_export = ''
    if request.method == 'POST' and 'year' in request.form:
        year = request.form.get('year')
        prediction = pr.Prediction(year)
        predict = prediction.prediction_calculator()
        predict_import = predict[0]
        predict_export = predict[1]
        accuracy_import = round(predict[2], 2)
        accuracy_export = round(predict[3], 2)
    return render_template('home.html',
                           predict_import=predict_import,
                           predict_export=predict_export,
                           accuracy_import=accuracy_import,
                           accuracy_export=accuracy_export)
