"""
image_generator.py — Tạo hoặc tìm ảnh đại diện bài viết qua Unsplash
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")


class ImageGenerator:
    def __init__(self):
        self.access_key = UNSPLASH_ACCESS_KEY

    def search(self, query: str) -> str:
        """Trả về URL ảnh từ Unsplash theo từ khóa."""
        # TODO: implement Unsplash search
        raise NotImplementedError
