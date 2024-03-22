from flask import Flask, request, render_template
from google.cloud import storage
import pyclamd

app = Flask(__name__)

# Initialize the GCS client
client = storage.Client()

# Get the GCS bucket
bucket = client.get_bucket('projectdbms')

# Initialize ClamAV scanner
clamav = pyclamd.ClamdUnixSocket()

@app.route('/')
def upload():
    return render_template("file_upload_form.html")

@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        # Get the uploaded file
        f = request.files['file']

        # Perform ClamAV scan
        virus_scan_result = clamav.scan_stream(f.stream)

        # Check if virus was found
        if virus_scan_result:
            return "Virus detected in the file. File not uploaded."

        # Create a blob object in the GCS bucket
        blob = bucket.blob(f.filename)

        # Upload the file to GCS
        blob.upload_from_file(f)

        # Get the public URL of the uploaded file
        url = blob.public_url

        return render_template("success.html", name=f.filename, url=url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
