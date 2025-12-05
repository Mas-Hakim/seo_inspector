"""Orchestrator: runs fetch -> robots -> sitemap -> html -> broken -> seo -> report"""
from core.fetcher import Fetcher
from core.robots_parser import RobotsParser
from core.sitemap_loader import SitemapLoader
from core.html_parser import HTMLParser
from core.broken_link_checker import BrokenLinkChecker
from core.seo_analyzer import SEOAnalyzer
from report.report_generator import ReportGenerator
from report.ui_assets_manager import UIAssetsManager
import logging, os, uuid, time
from typing import Dict, Any

logger = logging.getLogger(__name__)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'output')
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output"))

class CrawlerController:
    def __init__(self, url: str, output_dir: str = None):
        self.url = url
        self.fetcher = Fetcher()
        self.robots = RobotsParser()
        self.sitemap = SitemapLoader()
        self.html = HTMLParser()
        self.broken = BrokenLinkChecker()
        self.analyzer = SEOAnalyzer()
        self.reporter = ReportGenerator()
        self.ui_assets = UIAssetsManager()
        self.task_id = uuid.uuid4().hex[:12]
        self.output_dir = output_dir or os.path.join(os.getcwd(), "output", self.task_id)
        os.makedirs(self.output_dir, exist_ok=True)

    def run(self) -> Dict[str, Any]:
        start = time.time()
        logger.info("Starting inspection for %s", self.url)
        fetched = self.fetcher.fetch(self.url)
        robots = self.robots.parse(self.url)
        sitemap_urls = []
        if robots.get("sitemaps"):
            for s in robots["sitemaps"]:
                sitemap_urls.extend(self.sitemap.load(s))
        html_info = self.html.parse(self.url, fetched.get("content") or "")
        links = html_info.get("links", [])
        broken = self.broken.check_links(links)
        seo_metrics = self.analyzer.analyze(fetched, html_info, broken)
        report_path = self.reporter.generate(
            output_dir=self.output_dir,
            task_id=self.task_id,
            url=self.url,
            fetched=fetched,
            robots=robots,
            sitemap=sitemap_urls,
            html=html_info,
            broken=broken,
            seo=seo_metrics
        )
        # copy assets
        self.ui_assets.copy_assets(self.output_dir)
        elapsed = time.time() - start
        result = {
            "task_id": self.task_id,
            "url": self.url,
            "report_path": report_path,
            "elapsed": elapsed
        }
        logger.info("Inspection finished: %s", result)
        return result

if __name__ == '__main__':
    import argparse, logging
    logging.basicConfig(level=logging.INFO)
    p = argparse.ArgumentParser()
    p.add_argument("--url", required=True)
    args = p.parse_args()
    controller = CrawlerController(args.url)
    res = controller.run()
    print(res)
