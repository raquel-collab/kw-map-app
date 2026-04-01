import http.server
import socketserver
import os
import json
import urllib.request
import urllib.error
import re

PORT = 5000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

SITEMAP_URL = 'https://www.hireoverseas.com/sitemap.xml'

def slug_to_title(slug):
    """Convert a URL slug to a readable title."""
    slug = slug.replace('-', ' ').replace('_', ' ')
    # Capitalise each word but keep short connectors lowercase
    words = slug.split()
    stop = {'a','an','the','and','but','or','for','nor','on','at','to','by','in','of','vs','with'}
    titled = []
    for i, w in enumerate(words):
        titled.append(w if (i > 0 and w in stop) else w.capitalize())
    return ' '.join(titled)

def categorise(path):
    """Return a category string based on URL path."""
    if path.startswith('/blogs/'):
        return 'blog'
    if path.startswith('/roles/'):
        return 'role'
    if path.startswith('/hire-remote'):
        return 'hire'
    if path.startswith('/software-assistant'):
        return 'software'
    if path.startswith('/case-studies'):
        return 'case-study'
    if path.startswith('/courses'):
        return 'course'
    if path.startswith('/playbooks'):
        return 'playbook'
    if path.startswith('/alternatives'):
        return 'alternative'
    if path.startswith('/legal'):
        return 'legal'
    return 'page'

def fetch_sitemap_pages():
    req = urllib.request.Request(
        SITEMAP_URL,
        headers={'User-Agent': 'Mozilla/5.0 (compatible; SitemapBot/1.0)'}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        xml = resp.read().decode('utf-8')

    locs = re.findall(r'<loc>(.*?)</loc>', xml)
    pages = []
    seen = set()
    for loc in locs:
        loc = loc.strip()
        # Normalise to path only
        path = re.sub(r'^https?://(www\.)?hireoverseas\.com', '', loc).rstrip('/')
        if not path:
            path = '/'
        if path in seen:
            continue
        seen.add(path)
        # Derive title from last slug segment
        last_segment = path.rstrip('/').split('/')[-1] or 'Home'
        title = slug_to_title(last_segment) if last_segment else 'Home'
        pages.append({'t': title, 'u': path, 'cat': categorise(path)})

    return pages

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == '/':
            self.path = '/keyword_mapper.html'
            return super().do_GET()
        if self.path == '/api/sitemap':
            self.serve_sitemap()
            return
        return super().do_GET()

    def do_POST(self):
        if self.path == '/api/chat':
            self.proxy_anthropic()
        else:
            self.send_error(404)

    def serve_sitemap(self):
        try:
            pages = fetch_sitemap_pages()
            body = json.dumps({'pages': pages}).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def proxy_anthropic(self):
        api_key = os.environ.get('ANTHROPIC_API_KEY', '')
        if not api_key:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': {'message': 'ANTHROPIC_API_KEY not set'}}).encode())
            return

        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)

        req = urllib.request.Request(
            'https://api.anthropic.com/v1/messages',
            data=body,
            headers={
                'Content-Type': 'application/json',
                'x-api-key': api_key,
                'anthropic-version': '2023-06-01',
            },
            method='POST'
        )

        try:
            with urllib.request.urlopen(req) as resp:
                resp_body = resp.read()
                self.send_response(resp.status)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(resp_body)
        except urllib.error.HTTPError as e:
            resp_body = e.read()
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(resp_body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        print(format % args)

socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
