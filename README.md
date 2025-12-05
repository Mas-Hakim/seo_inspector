# seo_inspector_mvp

Minimal SEO Inspector — Python MVP

Features
- Fetcher (requests)
- Robots parser (urllib.robotparser)
- Sitemap loader (xml.etree)
- HTML parser (BeautifulSoup4)
- Broken link checker (HEAD/GET)
- SEO analyzer (simple scoring)
- Report generator (Jinja2 static HTML)
- Simple REST API (FastAPI)

Installation
```bash
git clone <repo>
cd seo_inspector
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

CLI usage
```bash
python main.py --url https://example.com
# output/<task_id>/report.html
```

Run API
```bash
uvicorn api.server:app --reload
```

Notes
- No JavaScript rendering
- One URL per run
- MIT License
