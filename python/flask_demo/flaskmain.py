from flask import Flask
from flask import render_template
from datetime import datetime

from backend import MainThread


app = Flask(__name__)


@app.route('/')
def index():

    records = [inv.get_record() for inv in mthread.inverters]
        
    return render_template('index.html', records=records)


@app.route('/api/datetime')
def api_datetime():
    s = '<h1>{}</h1>'.format(str(datetime.now()))
    return s


if __name__ == '__main__':
    mthread = MainThread()
    mthread.start()
    app.run(debug=False)
