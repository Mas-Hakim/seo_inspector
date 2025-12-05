"""Sitemap loader and parser for sitemap index and sitemap files."""
import requests
import xml.etree.ElementTree as ET
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

class SitemapLoader:
    def __init__(self, timeout: int = 8):
        self.timeout = timeout

    def load(self, sitemap_url: str) -> List[dict]:
        result = []
        try:
            r = requests.get(sitemap_url, timeout=self.timeout)
            if r.status_code != 200:
                return result
            root = ET.fromstring(r.content)
            # detect sitemapindex
            tag = root.tag.lower()
            if 'sitemapindex' in tag:
                for sm in root.findall('.//{*}sitemap'):
                    loc = sm.find('{*}loc')
                    lastmod = sm.find('{*}lastmod')
                    if loc is not None:
                        result.extend(self.load(loc.text))
            else:
                for url in root.findall('.//{*}url'):
                    loc = url.find('{*}loc')
                    lastmod = url.find('{*}lastmod')
                    entry = {"loc": loc.text if loc is not None else None,
                             "lastmod": lastmod.text if lastmod is not None else None}
                    result.append(entry)
        except Exception:
            logger.exception("Failed to load sitemap: %s", sitemap_url)
        return result
