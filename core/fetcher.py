"""Fetcher: download page via requests and collect metadata."""
import requests, time, logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class Fetcher:
    def __init__(self, timeout: int = 10, user_agent: str = None):
        self.timeout = timeout
        self.user_agent = user_agent or "seo-inspector-mvp/1.0 (+https://example.com)"
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})

    def fetch(self, url: str) -> Dict[str, Any]:
        result: Dict[str, Any] = {"url": url}
        try:
            start = time.time()
            resp = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            elapsed = time.time() - start
            result.update({
                "status_code": resp.status_code,
                "headers": dict(resp.headers),
                "final_url": resp.url,
                "elapsed": elapsed,
                "content": resp.text,
                "content_bytes_len": len(resp.content),
                "history": [r.status_code for r in resp.history] if resp.history else []
            })
        except requests.RequestException as e:
            logger.exception("Fetcher error for %s", url)
            result.update({
                "status_code": None,
                "error": str(e),
                "content": ""
            })
        return result
