"""
ghost_client.py — Ghost CMS Admin API client
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

GHOST_API_URL = os.getenv("GHOST_API_URL")
GHOST_ADMIN_API_KEY = os.getenv("GHOST_ADMIN_API_KEY")


class GhostClient:
    def __init__(self):
        self.base_url = GHOST_API_URL
        self.api_key = GHOST_ADMIN_API_KEY

    def create_post(self, title: str, html: str, tags: list[str], status: str = "draft") -> dict:
        # TODO: implement Ghost Admin API post creation
        raise NotImplementedError
