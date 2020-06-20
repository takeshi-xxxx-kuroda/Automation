# coding: UTF-8
import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','json'])
ALLOWED_EXTENSIONS = set(['json'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            
            import json
            f = open(os.path.join(UPLOAD_FOLDER, filename), 'r')
            json_data = json.load(f)
            
            #for DPE
            x = len(json_data["Structures"][0]["Bases"][0]["Modules"])
            x = x + 1
            DPE_list = [[] for i in range(x)]

            DPE_list[0].append(json_data["Structures"][0]["Bases"][0]["Id"])
            DPE_list[0].append(json_data["Structures"][0]["Bases"][0]["Qty"])

            for i in range(1,x):
                DPE_list[i].append(json_data["Structures"][0]["Bases"][0]["Modules"][i-1]["Options"][0]["Id"])  # Add model number
                DPE_list[i].append(json_data["Structures"][0]["Bases"][0]["Modules"][i-1]["Options"][0]["Qty"])  # Add qty

            #for DAE
            y = len(json_data["Structures"][0]["Bases"])
            if y > 1:
                y = y -1
                DAE_list = [[] for i in range(y)]
                for j in range(0,y):
                    DAE_list[j].append(json_data["Structures"][0]["Bases"][j+1]["Id"])
                    DAE_list[j].append(json_data["Structures"][0]["Bases"][j+1]["Qty"])

            #import DB
            import psycopg2
            conn = psycopg2.connect(host='xx.xxx.x.xx', dbname='powercalcmaster', user='postgres', password='xxxxxxx', port=5432)

            for i in range(0,x):
                strCur = "SELECT * FROM master_tb where model_number = '" + DPE_list[i][0] + "';"
                cur = conn.cursor()
                cur.execute(strCur)
                for row in cur:
                    DPE_list[i].append(row)
            
            y = len(json_data["Structures"][0]["Bases"])
            if y > 1:
                y = y -1
                for j in range(0,y):
                    strCur = "SELECT * FROM master_tb where model_number = '" + DAE_list[j][0] + "';"
                    cur = conn.cursor()
                    cur.execute(strCur)
                    for row in cur:
                        DAE_list[j].append(row)

            cur.close()
            conn.close()
            f.close()
            os.remove(os.path.join(UPLOAD_FOLDER, filename))

            #for HTML
            #DPE_model = DPE_list[0][0]
            #DPE_Qty = DPE_list[0][1]
            html_DPE = ""
            for temp in DPE_list[0][2]:
                temp1 = str(temp)
                temp1 = "<td>" + temp1 + "</td>"
                html_DPE = html_DPE + temp1
            
            y = len(json_data["Structures"][0]["Bases"])
            if y > 1:
                y = y -1
                html_DAE = "<tr>"
                for j in range(0,y):
                    #DAE_model = DAE_list[j][0]
                    #DAE_Qty = DAE_list[j][1]        
                    for buf in DAE_list[j][2]:
                        temp2 = str(buf)
                        temp2 = "<td>" + temp2 + "</td>"
                        html_DAE = html_DAE + temp2
            else:
                html_DAE = ""

            ans = "<link rel=\"stylesheet\" type=\"text/css\" \
                  href=\"/static/css/example.css\"> \
                  <h1>Created specifications from JSON file.</h1> \
                  <table><tr> \
                  <th>Model Nunber</th><th>Product</th><th>Component</th> \
                  <th>PowerConsumption(W)</th> \
                  <th>PowerConsumption(VA)</th><th>Heat dissipation(BTU/hr)</th> \
                  <th>Heat dissipation(KJ/hr)</th><th>Width</th><th>Depth</th> \
                  <th>Height</th><th>Height(U value)</th><th>Weight(kg)</th> \
                  <th>100V　Current(A)</th><th>200V　Current(A)</th><th>Voltage(V)</th> \
                  <th>Temperature(C)</th><th>Humidity(percent)noncondensing</th><th>Power cord Qty</th> \
                  <th>Plug Type</th><th>Note</th> \
                  </tr><tr>" + html_DPE + html_DAE + "</tr></table>"
            
            return ans
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
    app.run(debug=True, host='0.0.0.0', port=80)