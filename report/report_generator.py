"""Generates an HTML report using Jinja2 and writes files to output directory."""
import os, json, logging
from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')

class ReportGenerator:
    def __init__(self, templates_dir: str = None):
        self.templates_dir = templates_dir or TEMPLATES_DIR
        self.env = Environment(
            loader=FileSystemLoader(self.templates_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def generate(self, output_dir: str, task_id: str, url: str, fetched: Dict, robots: Dict, sitemap: List[Dict], html: Dict, broken: List[Dict], seo: Dict) -> str:
        os.makedirs(output_dir, exist_ok=True)
        template = self.env.get_template('report.html.j2')
        context = {
            'task_id': task_id,
            'url': url,
            'fetched': fetched,
            'robots': robots,
            'sitemap': sitemap,
            'html': html,
            'broken': broken,
            'seo': seo
        }
        out_html = template.render(**context)
        out_path = os.path.join(output_dir, 'report.html')
        with open(out_path, 'w', encoding='utf-8') as fh:
            fh.write(out_html)
        # save json summary
        with open(os.path.join(output_dir, 'report.json'), 'w', encoding='utf-8') as fh:
            json.dump(context, fh, ensure_ascii=False, indent=2)
        logger.info("Report written to %s", out_path)
        return out_path
