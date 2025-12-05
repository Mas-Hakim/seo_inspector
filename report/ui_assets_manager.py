"""Copies static CSS and icons into output directory."""
import os, shutil, logging

logger = logging.getLogger(__name__)

ASSETS_SRC = os.path.join(os.path.dirname(__file__), 'assets')

class UIAssetsManager:
    def __init__(self, assets_src: str = None):
        self.assets_src = assets_src or ASSETS_SRC

    def copy_assets(self, output_dir: str):
        dst = os.path.join(output_dir, 'assets')
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(self.assets_src, dst)
        logger.info("Copied UI assets to %s", dst)
