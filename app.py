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
    return Response(html, mimetype='text/html', headers={
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
    })

@app.route('/production')
def production():
    return serve_html('index.html')

@app.route('/shipments')
def shipments():
    return serve_html('shipments/index.html')

@app.route('/waiting')
def waiting():
    return serve_html('waiting/index.html')

@app.route('/time-calculator')
def time_calculator():
    return serve_html('time-calculator.html')

@app.route('/needs-manager-attention.jpg')
def nma_flowchart():
    with open('needs-manager-attention.jpg', 'rb') as f:
        return Response(f.read(), mimetype='image/jpeg', headers={
            'Cache-Control': 'no-cache',
            'Content-Disposition': 'inline; filename="needs-manager-attention.jpg"',
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
