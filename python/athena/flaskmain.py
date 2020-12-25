from flask import Flask
from flask import render_template
from datetime import datetime
import threading

from cronscheduler import Scheduler, Job
from dbhandler import DBHandler
from machine import Machine
import commands as cmd


app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello</h1>'
        

@app.route('/user/<username>')
def hello_user(username):
    return '<h1>Hello {}</h1>'.format(username)


@app.route('/records')
def get_records():
    rows = dbhandler.read_unuploaded_rows(500) 
    return render_template('records.html', records=rows)


@app.route('/api/datetime')
def api_datetime():
    s = '<h1>{}</h1>'.format(str(datetime.now()))
    return s


if __name__ == '__main__':

    machines = [Machine(id) for id in range(1,4)]
    commands = [cmd.SyncWithHardwareCommand(m) for m in machines]


    cscheduler = Scheduler()
    [cscheduler.add_job(Job('* * * * *', c)) for c in commands]


    dbhandler = DBHandler()
    c = cmd.InsertAllMachineRecordToDatabaseCommand(machines, dbhandler)
    cscheduler.add_job(Job('* * * * *', c))


    uscheduler = Scheduler()
    uscheduler.add_job(Job('*/3 * * * *', cmd.UploadUnuploadedRecordsCommand(dbhandler)))




    cthread = threading.Thread(target=cscheduler.run)
    cthread.start()

    uthread = threading.Thread(target=uscheduler.run)
    uthread.start()



    app.run(debug=True)
