from flask import Flask
from flask import render_template

from backend import MainThread


app     = Flask(__name__)
mthread = MainThread()


@app.route('/')
def index():
   
    records = []
    for inv in mthread.inverters:
        rec = inv.get_record()
        records.append(rec)
        
    #return '<p>Hello</p>'
    return render_template('home.html', records=records)


if __name__ == '__main__':
    mthread.start()
    app.run(debug=True)
