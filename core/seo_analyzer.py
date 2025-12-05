"""Compute simple SEO metrics and a composite quality score."""
from typing import Dict, Any, List
import math

class SEOAnalyzer:
    def analyze(self, fetched: Dict[str,Any], html_info: Dict[str,Any], broken_links: List[Dict]) -> Dict[str,Any]:
        metrics = {}
        title = html_info.get('title') or ''
        meta_description = html_info.get('meta', {}).get('description','') or ''
        canonical = html_info.get('canonical')
        headings = html_info.get('headings', {})
        num_h1 = len(headings.get('h1', []))
        num_links = len(html_info.get('links', []))
        num_broken = sum(1 for b in broken_links if not b.get('ok'))
        metrics.update({
            'title_len': len(title),
            'has_title': bool(title),
            'meta_description_len': len(meta_description),
            'has_meta_description': bool(meta_description),
            'has_canonical': bool(canonical),
            'num_h1': num_h1,
            'num_h2': len(headings.get('h2', [])),
            'num_links': num_links,
            'num_broken_links': num_broken
        })
        # simple scoring: start at 100 and deduct
        score = 100
        if not metrics['has_title']:
            score -= 25
        else:
            if metrics['title_len'] > 60:
                score -= 5
            elif metrics['title_len'] < 10:
                score -= 5
        if not metrics['has_meta_description']:
            score -= 20
        if not metrics['has_canonical']:
            score -= 10
        score -= min(50, metrics['num_broken_links'] * 5)
        # normalize
        score = max(0, min(100, score))
        metrics['quality_score'] = score
        return metrics
