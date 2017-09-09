from flask import Flask, render_template, request, send_file
import pandas
from datetime import datetime
from geopy.geocoders import Nominatim
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success-table',methods=['POST'])
def success():
    global filename
    if request.method=='POST':
        fil = request.files['file']
        try:
            df=pandas.read_excel(fil)
            geo=Nominatim(scheme='http')
            df["Coordinates"]=df["Address"].apply(geo.geocode)
            df["Latitiude"]=df["Coordinates"].apply(lambda x: x.latitude if x!=None else None)
            df["Longitude"]=df["Coordinates"].apply(lambda x: x.longitude if x!=None else None)
            filename=datetime.now().strftime("sample_files/%Y-%m-%d-%H-%M-%S-%f"+".csv")
            df.to_csv(filename)
            return render_template('index.html', text=df.to_html(), btn="download.html")
        except Exception as e:
            return render_template('index.html', text=str(e))
@app.route('/download-table')
def download():
    return send_file(filename, attachment_filename='yourfile.csv', as_attachment=True)

if __name__=='__main__':
    app.debug=True
    app.run()

