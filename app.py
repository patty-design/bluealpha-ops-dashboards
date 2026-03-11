import os
from flask import Flask, Response

app = Flask(__name__)

TOKEN   = os.environ.get('AIRTABLE_TOKEN', '')
BASE_ID = os.environ.get('AIRTABLE_BASE', '')

def serve_html(path):
    with open(path, 'r') as f:
        html = f.read()
    html = html.replace('__AIRTABLE_TOKEN__', TOKEN)
    html = html.replace('__AIRTABLE_BASE__', BASE_ID)
    return Response(html, mimetype='text/html')

@app.route('/production')
def production():
    return serve_html('index.html')

@app.route('/shipments')
def shipments():
    return serve_html('shipments/index.html')

@app.route('/waiting')
def waiting():
    return serve_html('waiting/index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
