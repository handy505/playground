from flask import Flask
from flask import render_template

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

from datetime import datetime
import threading
import sqlite3
import os


from cronscheduler import Scheduler, Job
from dbhandler import DBHandler
from machine import Machine
import commands as cmd


app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'mysecret'



@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


class NameForm(FlaskForm):
    name   = StringField('What is your name ?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/personal', methods=['GET', 'POST'])
def personal():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index2.html', form=form, name=name)
    
    
@app.route('/report/<datetime>')
def report(datetime):
    filename = 'power_curve_2020_0505.png'
    return render_template('report.html', filename=filename)


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/user/<username>')
def hello_user(username):
    return '<h1>Hello {}</h1>'.format(username)


@app.route('/records')
def get_records():
    dirpath = '../data/'
    filenames = [filename for filename in os.listdir(dirpath)]
    names = [os.path.splitext(filename)[0] for filename in filenames]
    names = ['/record/{}'.format(name) for name in names]
    names.sort()
    return render_template('records2.html', records=names)


@app.route('/record/<filename>')
def get_record_by_filename(filename):
    path = '../data/' + filename + '.sqlite'
    conn = sqlite3.connect(path)
    with conn:
        c = conn.cursor()
        sql = '''SELECT * 
                 FROM inverter_minutely '''
        c.execute(sql)
        rows = c.fetchall()

    return render_template('records.html', records=rows)


@app.route('/api/datetime')
def api_datetime():
    s = '<h1>{}</h1>'.format(str(datetime.now()))
    return s


def main():
    cscheduler = Scheduler()
    uscheduler = Scheduler()
    dbhandler  = DBHandler()


    machines = [Machine(id) for id in range(1,4)]
    commands = [cmd.SyncWithHardwareCommand(m) for m in machines]
    [cscheduler.add_job(Job('* * * * *', c)) for c in commands]


    c = cmd.InsertAllMachineRecordToDatabaseCommand(machines, dbhandler)
    cscheduler.add_job(Job('* * * * *', c))


    c = cmd.UploadUnuploadedRecordsCommand(dbhandler)
    uscheduler.add_job(Job('*/3 * * * *', c))


    cthread = threading.Thread(target=cscheduler.run)
    cthread.start()

    uthread = threading.Thread(target=uscheduler.run)
    uthread.start()


    app.run(debug=True)
    

if __name__ == '__main__':
    main()

