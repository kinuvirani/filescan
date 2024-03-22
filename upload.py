from flask import Flask, request, render_template
from google.cloud import storage
import pyclamd

app = Flask(__name__)

client = storage.Client()

bucket = client.get_bucket('test-upload12')

clamav = pyclamd.ClamdUnixSocket()

@app.route('/')
def upload():
    return render_template("file_upload_form.html")

@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        virus_scan_result = clamav.scan_stream(f.stream)

        if virus_scan_result:
            return "Sorry, File is not virus free, so can't upload it"

        blob = bucket.blob(f.filename)

        blob.upload_from_file(f)

        url = blob.public_url

        return render_template("success.html", name=f.filename, url=url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
