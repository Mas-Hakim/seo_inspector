"""CLI entrypoint: python main.py --url https://example.com"""
import argparse, logging, os
from controllers.crawler_controller import CrawlerController

logging.basicConfig(level=logging.INFO)

def main():
    p = argparse.ArgumentParser(description='SEO Inspector MVP')
    p.add_argument('--url', required=True, help='URL to inspect')
    p.add_argument('--out', required=False, help='Output base directory')
    args = p.parse_args()
    out = args.out or os.path.join(os.getcwd(), 'output')
    controller = CrawlerController(args.url, output_dir=os.path.join(out))
    res = controller.run()
    print('Report:', res.get('report_path'))

if __name__ == '__main__':
    main()
