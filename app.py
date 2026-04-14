import os
import io
from flask import Flask, Response
try:
    from PIL import Image as _PILImage
    _PIL_OK = True
except ImportError:
    _PILImage = None
    _PIL_OK = False

app = Flask(__name__)

BUILD_VERSION = "20260414-staticPDF"  # bump this to verify deployment

# Build QR cards PDF from source JPGs on startup so Railway binary cache never stales it
def _load_qr_pdf():
    # Serve pre-built PDF from repo directly — no recompression, no artifacts
    if os.path.exists('qr-cards-4up.pdf'):
        with open('qr-cards-4up.pdf', 'rb') as f:
            data = f.read()
        print(f'QR PDF loaded from file OK ({len(data)} bytes)')
        return data
    print('Warning: qr-cards-4up.pdf not found')
    return None

_QR_PDF = _load_qr_pdf()

@app.route('/_version')
def version():
    return Response(f'{BUILD_VERSION} pillow={_PIL_OK} pdf_built={_QR_PDF is not None}', mimetype='text/plain')

TOKEN           = os.environ.get('AIRTABLE_TOKEN', '')
BASE_ID         = os.environ.get('AIRTABLE_BASE', '')
SHIPMENTS_TOKEN = os.environ.get('SHIPMENTS_TOKEN', '')
SHIPMENTS_BASE  = os.environ.get('SHIPMENTS_BASE', '')
PATTY_TOKEN     = os.environ.get('PATTY_TOKEN', '')

def serve_html(path):
    with open(path, 'r') as f:
        html = f.read()
    html = html.replace('__AIRTABLE_TOKEN__', TOKEN)
    html = html.replace('__AIRTABLE_BASE__', BASE_ID)
    html = html.replace('__SHIPMENTS_TOKEN__', SHIPMENTS_TOKEN)
    html = html.replace('__SHIPMENTS_BASE__', SHIPMENTS_BASE)
    html = html.replace('__PATTY_TOKEN__', PATTY_TOKEN)
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

@app.route('/marketing-v2')
def marketing_v2():
    return serve_html('marketing-v2.html')

@app.route('/training-needs')
def training_needs():
    return serve_html('training-needs.html')

@app.route('/paycom-card.jpg')
def paycom_card():
    with open('paycom-card.jpg', 'rb') as f:
        return Response(f.read(), mimetype='image/jpeg', headers={'Cache-Control': 'no-cache'})

@app.route('/qr-card-<int:num>.jpg')
def qr_card(num):
    fname = f'qr-card-{num}.jpg'
    try:
        with open(fname, 'rb') as f:
            return Response(f.read(), mimetype='image/jpeg', headers={'Cache-Control': 'no-cache'})
    except FileNotFoundError:
        return Response('Not found', status=404)

@app.route('/needs-manager-attention.jpg')
def nma_flowchart():
    with open('needs-manager-attention.jpg', 'rb') as f:
        return Response(f.read(), mimetype='image/jpeg', headers={
            'Cache-Control': 'no-cache',
            'Content-Disposition': 'inline; filename="needs-manager-attention.jpg"',
        })

@app.route('/hosanna-4up.pdf')
def hosanna_pdf():
    with open('hosanna-4up.pdf', 'rb') as f:
        return Response(f.read(), mimetype='application/pdf', headers={
            'Cache-Control': 'no-cache',
            'Content-Disposition': 'inline; filename="hosanna-4up.pdf"',
        })

@app.route('/hosanna-4up.jpg')
def hosanna_jpg():
    with open('hosanna-4up.jpg', 'rb') as f:
        return Response(f.read(), mimetype='image/jpeg', headers={
            'Cache-Control': 'no-cache',
        })

@app.route('/qr-cards-4up.pdf')
def qr_cards_pdf():
    # Served from in-memory bytes built at startup from source JPGs
    # (avoids Railway Docker layer cache serving stale binary PDFs)
    data = _QR_PDF
    if data is None:
        with open('qr-cards-4up.pdf', 'rb') as f:
            data = f.read()
    return Response(data, mimetype='application/pdf', headers={
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Content-Disposition': 'inline; filename="qr-cards-4up.pdf"',
    })

@app.route('/qr-cards-4up.jpg')
def qr_cards_jpg():
    with open('qr-cards-4up.jpg', 'rb') as f:
        return Response(f.read(), mimetype='image/jpeg', headers={'Cache-Control': 'no-cache'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

