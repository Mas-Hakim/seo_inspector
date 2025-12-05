"""Robots.txt parser using urllib.robotparser and simple fetch for sitemaps."""
import urllib.robotparser
import requests
from urllib.parse import urljoin, urlparse
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class RobotsParser:
    def __init__(self, user_agent: str = "seo-inspector-mvp"):
        self.user_agent = user_agent

    def get_robots_url(self, url: str) -> str:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    def parse(self, url: str) -> Dict[str, Any]:
        robots_url = self.get_robots_url(url)
        rp = urllib.robotparser.RobotFileParser()
        data = {"robots_url": robots_url, "sitemaps": [], "raw": ""}
        try:
            r = requests.get(robots_url, timeout=8)
            if r.status_code == 200:
                text = r.text
                data["raw"] = text
                # parse sitemaps
                for line in text.splitlines():
                    if line.strip().lower().startswith('sitemap:'):
                        parts = line.split(':', 1)
                        if len(parts) > 1:
                            sm = parts[1].strip()
                            data["sitemaps"].append(sm)
                rp.parse(text.splitlines())
            else:
                rp.set_url(robots_url)
                rp.read()
        except requests.RequestException:
            logger.exception("Unable to fetch robots.txt: %s", robots_url)
        return data
