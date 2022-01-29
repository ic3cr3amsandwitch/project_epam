import os
import sys
import time

from flask import Flask, render_template, request

from Blocker import ContentBlocker

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/runcode', methods=['POST'])
def runcode():

    if request.method == 'POST':
        code_area_data_from_input = request.form.get('input')
        # code_area_data_from_stdin = request.form.get('stdin')
        time_right_now = int(round(time.time()*1000))
        filename = f'file_{time_right_now}.txt'
        try:
            sys.stdout = open(filename, 'w')
            ContentBlocker.check_content(code_area_data_from_input)
            exec(code_area_data_from_input)
            sys.stdout.close()
            output = open(filename, 'r').read()
        except Exception as e:
            output = e
        finally:
            os.remove(filename)

    return render_template('index.html', code=code_area_data_from_input, output=output)
