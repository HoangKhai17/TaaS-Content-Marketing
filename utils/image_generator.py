"""
image_generator.py — Tìm ảnh cho bài viết TaaS

Fallback chain: Unsplash → Pexels → Pixabay
Ưu tiên ảnh có phong cách professional / tech / B2B.
Query PHẢI bằng tiếng Anh để tìm được ảnh chất lượng hơn.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY", "")
PEXELS_API_KEY      = os.getenv("PEXELS_API_KEY", "")
PIXABAY_API_KEY     = os.getenv("PIXABAY_API_KEY", "")

# ──────────────────────────────────────────────
# Query gợi ý theo loại bài — dùng khi Claude
# không truyền query cụ thể
# ──────────────────────────────────────────────
DEFAULT_QUERIES = {
    "tin-cong-ty":   ["tech team collaboration", "software company office", "startup team meeting"],
    "tin-cong-nghe": ["software development", "coding laptop", "technology abstract"],
    "case-study":    ["business results growth", "team success dashboard", "software testing"],
    "insight":       ["strategic thinking", "technology leadership", "engineering whiteboard"],
}


def _unsplash_search(query: str, per_page: int = 5) -> list[dict]:
    """
    Tìm ảnh trên Unsplash.
    Returns list of {"url": ..., "alt": ..., "credit": ..., "source": "unsplash"}
    """
    if not UNSPLASH_ACCESS_KEY:
        return []

    try:
        resp = requests.get(
            "https://api.unsplash.com/search/photos",
            params={
                "query":       query,
                "per_page":    per_page,
                "orientation": "landscape",
                "content_filter": "high",
            },
            headers={"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"},
            timeout=10,
        )
        resp.raise_for_status()
        results = resp.json().get("results", [])
        return [
            {
                "url":    r["urls"]["regular"],
                "alt":    r.get("alt_description") or query,
                "credit": f"Photo by {r['user']['name']} on Unsplash",
                "source": "unsplash",
            }
            for r in results
            if r.get("urls", {}).get("regular")
        ]
    except Exception as e:
        print(f"[Unsplash] Lỗi: {e}")
        return []


def _pexels_search(query: str, per_page: int = 5) -> list[dict]:
    """
    Tìm ảnh trên Pexels.
    Returns list of {"url": ..., "alt": ..., "credit": ..., "source": "pexels"}
    """
    if not PEXELS_API_KEY:
        return []

    try:
        resp = requests.get(
            "https://api.pexels.com/v1/search",
            params={
                "query":       query,
                "per_page":    per_page,
                "orientation": "landscape",
            },
            headers={"Authorization": PEXELS_API_KEY},
            timeout=10,
        )
        resp.raise_for_status()
        photos = resp.json().get("photos", [])
        return [
            {
                "url":    p["src"]["large"],
                "alt":    p.get("alt") or query,
                "credit": f"Photo by {p['photographer']} on Pexels",
                "source": "pexels",
            }
            for p in photos
            if p.get("src", {}).get("large")
        ]
    except Exception as e:
        print(f"[Pexels] Lỗi: {e}")
        return []


def _pixabay_search(query: str, per_page: int = 5) -> list[dict]:
    """
    Tìm ảnh trên Pixabay.
    Returns list of {"url": ..., "alt": ..., "credit": ..., "source": "pixabay"}
    """
    if not PIXABAY_API_KEY:
        return []

    try:
        resp = requests.get(
            "https://pixabay.com/api/",
            params={
                "key":          PIXABAY_API_KEY,
                "q":            query,
                "per_page":     per_page,
                "image_type":   "photo",
                "orientation":  "horizontal",
                "safesearch":   "true",
                "min_width":    1280,
            },
            timeout=10,
        )
        resp.raise_for_status()
        hits = resp.json().get("hits", [])
        return [
            {
                "url":    h["largeImageURL"],
                "alt":    query,
                "credit": "Image via Pixabay",
                "source": "pixabay",
            }
            for h in hits
            if h.get("largeImageURL")
        ]
    except Exception as e:
        print(f"[Pixabay] Lỗi: {e}")
        return []


# ──────────────────────────────────────────────
# PUBLIC API
# ──────────────────────────────────────────────

def search(
    query: str,
    tag_slug: str = "",
    count: int = 1,
) -> list[dict]:
    """
    Tìm ảnh từ query tiếng Anh.
    Fallback tự động: Unsplash → Pexels → Pixabay.

    Args:
        query:    Từ khóa tiếng Anh (ví dụ: "software testing automation")
        tag_slug: Loại bài — dùng để chọn DEFAULT_QUERIES nếu query trống
        count:    Số ảnh cần tìm (mặc định 1 cho cover)

    Returns:
        list of dict: [{"url": ..., "alt": ..., "credit": ..., "source": ...}]
        Trả về list rỗng nếu tất cả nguồn đều thất bại.
    """
    if not query and tag_slug:
        queries = DEFAULT_QUERIES.get(tag_slug, ["software testing professional"])
        query = queries[0]

    if not query:
        query = "software testing professional"

    # Thử lần lượt từng nguồn
    for search_fn in [_unsplash_search, _pexels_search, _pixabay_search]:
        results = search_fn(query, per_page=max(count + 2, 5))
        if results:
            print(f"[Image] Tìm được {len(results)} ảnh từ {results[0]['source']} — query: '{query}'")
            return results[:count]

    print(f"[Image] Không tìm được ảnh nào cho query: '{query}'")
    return []


def search_multiple(queries: list[str], tag_slug: str = "") -> list[dict]:
    """
    Tìm ảnh từ nhiều query — mỗi query lấy 1 ảnh tốt nhất.
    Dùng cho bài cần nhiều ảnh inline (không chỉ cover).

    Args:
        queries:  Danh sách query tiếng Anh
        tag_slug: Loại bài — dùng làm fallback nếu query rỗng

    Returns:
        list of dict, mỗi phần tử là ảnh tốt nhất cho query đó
    """
    results = []
    for q in queries:
        imgs = search(q, tag_slug=tag_slug, count=1)
        if imgs:
            results.extend(imgs)
    return results


def format_cover_html(image: dict) -> str:
    """Tạo HTML tag cho ảnh cover — dùng khi chèn vào Ghost HTML."""
    if not image:
        return ""
    return (
        f'<figure class="kg-card kg-image-card">'
        f'<img src="{image["url"]}" alt="{image["alt"]}" loading="lazy"/>'
        f'<figcaption>{image["credit"]}</figcaption>'
        f'</figure>'
    )


def format_inline_html(image: dict, caption: str = "") -> str:
    """Tạo HTML tag cho ảnh inline trong bài viết."""
    if not image:
        return ""
    display_caption = caption or image["credit"]
    return (
        f'<figure class="kg-card kg-image-card">'
        f'<img src="{image["url"]}" alt="{image["alt"]}" loading="lazy"/>'
        f'<figcaption>{display_caption}</figcaption>'
        f'</figure>'
    )


# ──────────────────────────────────────────────
# PLACEHOLDER INJECTION
# ──────────────────────────────────────────────

def extract_queries_from_html(html: str) -> list[str]:
    """
    Trích xuất danh sách query từ các placeholder trong HTML.
    Placeholder format: <!-- IMAGE: english query here -->

    Ví dụ: <!-- IMAGE: software testing automation workflow -->
    """
    import re
    return re.findall(r'<!--\s*IMAGE:\s*(.+?)\s*-->', html)


def inject_images_into_html(html: str, images: list[dict]) -> str:
    """
    Thay thế các placeholder <!-- IMAGE: ... --> trong HTML bằng <figure> thật.

    - Nếu số ảnh >= số placeholder: thay tất cả
    - Nếu ảnh ít hơn placeholder: thay được bao nhiêu hay bấy nhiêu,
      placeholder còn lại bị xóa (không để comment rác trong HTML)

    Args:
        html:   Nội dung HTML có chứa placeholder
        images: Danh sách ảnh trả về từ search() / search_multiple()

    Returns:
        HTML đã được chèn ảnh thật
    """
    import re
    pattern = re.compile(r'<!--\s*IMAGE:\s*.+?\s*-->')
    matches = pattern.findall(html)

    for i, match in enumerate(matches):
        if i < len(images):
            replacement = format_inline_html(images[i])
        else:
            replacement = ""  # Xóa placeholder thừa
        html = html.replace(match, replacement, 1)

    return html
