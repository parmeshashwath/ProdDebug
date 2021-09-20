from flask import Flask,request,make_response,send_from_directory,render_template,session,jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import traceback
app = Flask(__name__)

from SafeRun import *

@app.route('/debug')
def debug():
    a = 1
    b = 2
    c = a + b
    return jsonify({'result':'success'})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')  # Catch All urls, enabling copy-paste url
def home(path):
    return render_template('index.html')

SafeRun(app,"test")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5081, debug=True, use_reloader=True, threaded=True)
