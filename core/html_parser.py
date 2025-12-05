"""HTML parser using BeautifulSoup4: title, meta, canonical, headings, links."""
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import Dict, Any, List, Set
import logging

logger = logging.getLogger(__name__)

class HTMLParser:
    def __init__(self, base_url: str = None):
        self.base_url = base_url

    def is_internal(self, url: str, base_netloc: str) -> bool:
        try:
            p = urlparse(url)
            return (not p.netloc) or (p.netloc == base_netloc)
        except Exception:
            return False

    def parse(self, base_url: str, html: str) -> Dict[str, Any]:
        soup = BeautifulSoup(html, 'html.parser')
        result: Dict[str, Any] = {"title": None, "meta": {}, "canonical": None, "headings": {}, "links": []}
        # title
        t = soup.find('title')
        if t:
            result['title'] = t.get_text().strip()
        # meta
        for m in soup.find_all('meta'):
            if m.get('name'):
                result['meta'][m.get('name').lower()] = m.get('content', '')
            elif m.get('property'):
                result['meta'][m.get('property').lower()] = m.get('content', '')
        # canonical
        link = soup.find('link', rel='canonical')
        if link and link.get('href'):
            result['canonical'] = urljoin(base_url, link.get('href'))
        # headings
        for i in range(1,7):
            hs = [h.get_text().strip() for h in soup.find_all(f'h{i}')]
            if hs:
                result['headings'][f'h{i}'] = hs
        # links
        base_netloc = urlparse(base_url).netloc
        seen: Set[str] = set()
        for a in soup.find_all('a', href=True):
            href = a['href'].strip()
            full = urljoin(base_url, href)
            if full in seen:
                continue
            seen.add(full)
            internal = self.is_internal(full, base_netloc)
            result['links'].append({
                'href': full,
                'text': a.get_text().strip()[:120],
                'internal': internal
            })
        return result
