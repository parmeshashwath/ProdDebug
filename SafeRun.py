import sys
from flask import Flask,render_template,send_from_directory,request,jsonify,Response,session
from collections import defaultdict

from pymongo import *
import inspect
import time
from bson import ObjectId
import traceback
client = MongoClient('mongodb+srv://admin:admin123@cluster0.4zm9y.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client['api_mon']
collection_name = 'prod_debug'





class SafeRun(object):

    def safe_run(self,func,domain):

        def func_wrapper(*args, **kwargs):
            try:
                self.function_line_mapping = defaultdict(lambda: set())
                self.functionline_id_mapping = dict()
                for record in db[collection_name].find({'domain':self.domain,'active':True}):
                    record['line_number'] = str(int(record['line_number']))
                    self.function_line_mapping[record['function_name']].add(record['line_number'])
                    self.functionline_id_mapping[record['function_name']+"#"+record['line_number']] = record['_id']

                if len(self.function_line_mapping.keys())!=0:
                    sys.settrace(self.trace_calls)


                response =  func(*args, **kwargs)


            except Exception as e:

                print(e)

                response = jsonify({'result':'Something went wrong.Please try again..'})

            return response
        func_wrapper.__name__ = func.__name__
        return func_wrapper

    def trace_calls(self,frame, event, arg):

        if frame.f_code.co_name in self.function_line_mapping.keys():
            return self.trace_lines

    def trace_lines(self,frame, event, arg):
        if event != 'line':
            return
        if str(frame.f_lineno) in self.function_line_mapping[frame.f_code.co_name]:
            print(frame.f_code.co_name,frame.f_lineno)
            data = {}


            code = frame.f_code
            data['filename'] = code.co_filename
            data['functioncode'] = inspect.getsourcelines(code)[0]
            data['localvariables'] = frame.f_locals
            data['error_lineno'] = frame.f_lineno
            data['url'] = request.url
            data['function_start_lno'] = code.co_firstlineno
            data['userid'] = session.get("cec")
            data['stacktrace'] = traceback.format_exc()
            object_id = str(ObjectId())
            data['_id'] = object_id
            data['timestamp'] = int(time.time())
            update_object_id = self.functionline_id_mapping[frame.f_code.co_name+"#"+str(frame.f_lineno)]
            print(update_object_id)
            db[collection_name].update({'_id':ObjectId(update_object_id)},{'$push':{'data':data}})
    def __init__(self, app,domain):
        self.function_line_mapping = defaultdict(lambda: set())
        self.functionline_id_mapping = dict()
        self.domain = domain
        with app.app_context():
            for name, func in app.view_functions.items():
                app.view_functions[name] = self.safe_run(func,domain)



        # else:
        #     print("#"*100)
        #     print(frame.f_code.co_name)
