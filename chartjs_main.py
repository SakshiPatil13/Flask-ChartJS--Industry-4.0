#from flask import Flask, Markup, render_template
from flask import Flask, Markup, render_template, request, redirect, url_for, jsonify
from random import sample
import time
import datetime
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://root:lmtech123@localhost:3306/industry10'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Simulation(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    machine_number = db.Column(db.String(10))
    cycle_time = db.Column(db.Integer)
    number_of_pieces = db.Column(db.Integer)
    running_status = db.Column(db.Integer)
    cycle_time = db.Column(db.Integer)


@app.route('/')
def a():
    return render_template('my_chart.html')


@app.route('/index')
def index():
    pieces = []
    p = []
    time_axis = []
    run = []
    r = []
    cycle = []
    c = []

    all_data = Simulation.query.all()
    for record in all_data:
        if record.machine_number == '1':
            pieces.append(int(record.number_of_pieces))
            p = list(pieces[-6:])
            # p = [5, 3, 6, 7, 3, 20]

            run.append(int(record.running_status))
            r = list(run[-6:])

            cycle.append(int(record.cycle_time))
            c = list(cycle[-6:])

            time_axis.append(str(record.created)[-8:])
            time_ = time_axis[-6:]

            # time_ = ["January", "February", "March",
            #          "April", "May", "June"]

    return jsonify({'results': p, 'time': time_, 'running': r, 'cyc': c})


@app.route('/method', methods=['GET', 'POST'])
def request_check():
    if request.method == 'POST':
        print 'received'
        print 'Post request data:', request.json
        # print type(request.data)
        json_dumps = json.dumps(request.json)
        print 'dumps:', json_dumps
        json_loads = json.loads(str(json_dumps))
        print 'loads:', json_loads

        number_of_pieces = json_loads['number_of_pieces']

        running_status = json_loads['running_status']

        cycle_time = json_loads['cycle_time']

        signature = Simulation(machine_number='1',
                               number_of_pieces=number_of_pieces,
                               running_status=running_status,
                               cycle_time=cycle_time)
        db.session.add(signature)
        db.session.commit()
        return 'Success'

    else:
        return 'Fail'

if __name__ == "__main__":
    app.run(debug=True)
