# coding: UTF-8
import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = r'C:\Users\mengs\Desktop\Automation\docker\uploads'
#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','json'])
ALLOWED_EXTENSIONS = set(['json'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def json_import(UPLOAD_FOLDER, filename):
    import json
    f = open(os.path.join(UPLOAD_FOLDER, filename), 'r')
    json_data = json.load(f)
    f.close()
    return(json_data)

def get_DPE_from_json(json_data):
    x = len(json_data["Structures"][0]["Bases"][0]["Modules"])
    x = x + 1
    DPE_list = [[] for i in range(x)]
    DPE_list[0].append(json_data["Structures"][0]["Bases"][0]["Id"])
    DPE_list[0].append(json_data["Structures"][0]["Bases"][0]["Qty"])
    for i in range(1,x):
        DPE_list[i].append(json_data["Structures"][0]["Bases"][0]["Modules"][i-1]["Options"][0]["Id"])  # Add model number
        DPE_list[i].append(json_data["Structures"][0]["Bases"][0]["Modules"][i-1]["Options"][0]["Qty"])  # Add qty
    return(DPE_list)

def get_DAE_from_json(json_data):
    y = len(json_data["Structures"][0]["Bases"])
    if y > 1:
        y = y -1
        DAE_list = [[] for i in range(y)]
        for j in range(0,y):
            DAE_list[j].append(json_data["Structures"][0]["Bases"][j+1]["Id"])
            DAE_list[j].append(json_data["Structures"][0]["Bases"][j+1]["Qty"])
        return(DAE_list)




@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            
            json_data = json_import(UPLOAD_FOLDER, filename) 
            os.remove(os.path.join(UPLOAD_FOLDER, filename))

            DPE_list = get_DPE_from_json(json_data)
            DAE_list = get_DAE_from_json(json_data)

            print(json_data)
            print(DPE_list[0])
            print(DAE_list[0])



        #return(temp[0],temp[1],temp[2])
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
@app.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=80)