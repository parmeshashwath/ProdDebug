from flask import Flask,request,make_response,send_from_directory,render_template,session,jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import json
app = Flask(__name__)

from SafeRun import *

@app.route('/debug')
def debug():
    a = 1
    b = 2
    c = a + b
    return jsonify({'result':'success'})

@app.route('/get_contract_details')
def getContractDetails():
    contractData = json.load(open('data.json',))
    for data in contractData:
        if data['tramUrl'].lower():
            data['active'] = True
    return jsonify({'contracts': contractData})



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')  # Catch All urls, enabling copy-paste url
def home(path):
    return render_template('index.html')

SafeRun(app,"cerebro")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True, threaded=True)
