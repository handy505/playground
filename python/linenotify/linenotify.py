import requests
import datetime


def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return r.status_code

msg = 'hihi, it is {}'.format(datetime.datetime.now())
token = 'KfskXUf5dVbAhy5DR6JYH73ib96Nq1qrWbt2fojd4ys'


lineNotifyMessage(token, msg)
