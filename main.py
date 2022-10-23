#!/usr/bin/python3

##
# TEMPLATE
##
# Execute
##
# ./template.py --help
##
# for the help string.
##
# Authors:
##
# 2019-2020, Miroslav Shaltev, shaltev@l3s.de
##
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
##
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
##
# You should have received a copy of the GNU General Public License
# along with with program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA  02111-1307  USA
##

from optparse import OptionParser
from datetime import datetime
import time
import os
import json


from flask import Flask, request, Response, flash, redirect, url_for, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import pickle
from tests import classify_user

import queue
import threading
import uuid

DEVNULL = "/dev/null"

TEMPLATEHOST = "localhost"
TEMPLATEPORT = 9999
HEADER = "application/json"

UPLOAD_FOLDER = r'./uploads'
ALLOWED_EXTENSIONS = {'p'}


def getcmdline():
    """
    Read command line arguments.
    """
    usage = "usage: %prog [options] arg"
    p = OptionParser()
    p.add_option("--serverhost", action="store", dest="serverhost", help=(
        'Server hostname or ip [default: %s]' % (TEMPLATEHOST)), default=TEMPLATEHOST)
    p.add_option("--serverport", action="store", dest="serverport",
                 help=('Server port [default: %s]' % (TEMPLATEPORT)), default=TEMPLATEPORT)
    p.add_option("--log", action="store", dest="log", help=(
        'Log the processed files, discard input files found in this log [default: %s]' % (DEVNULL)), default=DEVNULL)

    (o, a) = p.parse_args()
    return o


Q = queue.Queue()
R = {}

# load the model in the consctructor


class BotDetection(object):
    def __init__(self, gid, p):
        self.gid = gid
        self.payload = p

# for loop of the prediction
    def process(self):
        results = []
        for user in self.payload:
            result = classify_user(self.payload[user])
            results.append(result)
            # print(user)
            # print(result)
            # print('----')
        R[str(self.gid)] = {'gid': str(self.gid), 'results': results}


app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/h', methods=['GET'])
def home():
    info = {
        'application': "MIRROR TEMPLATE",
        'serverhost': app.config.get('serverhost'),
        'serverport': app.config.get('serverport'),
        'inputqueue': Q.qsize(),
        'outputqueue': len(R)}
    return json.dumps(info)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# make an UI to facilitate the user experience


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            results = process(file_path)
            # return redirect(url_for('upload_file',
            #                         filename=filename))
            return '''
            <!doctype html>
            <title>Result</title>
            <form> '''+str(results)+'''</form>
            '''
    return '''
    <!doctype html>
    <title>Upload User data</title>
    <h1>Upload User Data</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Show Prediction>
    </form>
    '''
# end of the Ui code


@app.route('/process', methods=['GET', 'POST'])
def process():
    if request.method == 'POST':
        # If you wanna be working with json file directly use the follow code
        data = request.files['data']
        d = json.load(data)
        # print(d['94c383089f0dd9993020276bd01113ecb5935ad860bfa61e6079e7d548577f76'])

        for user in d:
            d[user]["crawled_at"] = datetime.strptime(
                d[user]["crawled_at"], '%Y-%m-%d %H:%M:%S')

            d[user]["user_data"]["created_at"] = datetime.strptime(
                d[user]["user_data"]["created_at"], '%Y-%m-%d %H:%M:%S')

            tweets = d[user]["tweets"]
            # print(d[user]["crawled_at"])
            for tweet in tweets:
                tweet["created_at"] = datetime.strptime(
                    tweet["created_at"], '%Y-%m-%d %H:%M:%S')

        p = d
        gid = uuid.uuid4()
        Q.put({'gid': gid, 'payload': p})
        print("queue", Q.qsize())
        # print(gid)

        # If you wanna be working with pickle file directly just uncomment this and the curl command
        # from io import BufferedReader
        # data = request.files['data']
        # data.name = data.filename
        # data = BufferedReader(data)
        # d = pickle.load(data)
        # # p = dict(d['payload'])
        # p = d
        # # print(p.keys())
        # # print(p)
        # gid = uuid.uuid4()
        # Q.put({'gid': gid, 'payload': p})
        # # print(gid)
        # print("queue", Q.qsize())

        analyse_q()

        r = {"id": str(gid)}
        response = app.response_class(response=json.dumps(
            r), status=200, mimetype='application/json')
        return response

    if request.method == 'GET':
        rid = str(request.args.get('id', ''))
        print(rid)
        result = {}
        if rid in R.keys():
            result['status'] = 'ready'
            result['result'] = R[rid]
            del R[rid]
        else:
            result['status'] = ''
        print(R.keys())
        print(result)
        return json.dumps(result, iterable_as_array=True)


def analyse_q():
    # while True:
    time.sleep(1)
    while not Q.empty():
        d = Q.get()
        a = BotDetection(d['gid'], d['payload'])
        a.process()


def main():
    o = getcmdline()
    app.config['SERVER_NAME'] = '%s:%d' % (
        str(o.serverhost), int(o.serverport))
    app.config['serverhost'] = str(o.serverhost)
    app.config['serverport'] = int(o.serverport)
    app.config['log'] = str(o.log)
    print(app.config)

    t = threading.Thread(target=analyse_q)
    t.daemon = True
    t.start()
    app.run(host=app.config.get('serverhost'),
            port=app.config.get('serverpot'))


if __name__ == "__main__":
    app.run(debug=True)
