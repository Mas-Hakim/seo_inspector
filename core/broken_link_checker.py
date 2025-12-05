"""Checks links with HEAD (falls back to GET). Returns status codes and flags."""
import requests, logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class BrokenLinkChecker:
    def __init__(self, timeout: int = 6):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'seo-inspector-mvp/1.0'})

    def check_link(self, url: str) -> Dict:
        try:
            r = self.session.head(url, timeout=self.timeout, allow_redirects=True)
            status = r.status_code
            if status == 405:  # method not allowed
                r = self.session.get(url, timeout=self.timeout, allow_redirects=True)
                status = r.status_code
            return {'url': url, 'status': status, 'ok': 200 <= status < 400}
        except requests.RequestException as e:
            logger.debug("Link check failed: %s (%s)", url, e)
            return {'url': url, 'status': None, 'ok': False, 'error': str(e)}

    def check_links(self, links: List[Dict]) -> List[Dict]:
        results = []
        for l in links:
            url = l.get('href')
            if not url:
                continue
            results.append(self.check_link(url))
        return results
