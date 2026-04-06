"""
wp_client.py — WordPress REST API client cho TaaS Content Marketing

Hỗ trợ:
- Xác thực qua Application Password (Basic Auth)
- Tạo / cập nhật bài viết (draft hoặc publish)
- Upload ảnh lên Media Library
- Fetch danh sách bài đã đăng để tạo internal links
- Gán tag theo 4 danh mục: tin-cong-ty, tin-cong-nghe, case-study, insight
"""

import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

WP_URL         = os.getenv("WP_URL", "").rstrip("/")
WP_USERNAME    = os.getenv("WP_USERNAME", "")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD", "").replace(" ", "")

# ──────────────────────────────────────────────
# TAG MAPPING — 4 tags cố định, KHÔNG tạo thêm
# ──────────────────────────────────────────────
TAG_SLUG_MAP = {
    "tin-cong-ty":        "tin-cong-ty",
    "tin cong ty":        "tin-cong-ty",
    "company":            "tin-cong-ty",

    "tin-cong-nghe":      "tin-cong-nghe",
    "tin cong nghe":      "tin-cong-nghe",
    "tech":               "tin-cong-nghe",
    "technology":         "tin-cong-nghe",

    "case-study":         "case-study",
    "case study":         "case-study",
    "casestudy":          "case-study",

    "insight":            "insight",
    "thought leadership": "insight",

    "kien-thuc":          "kien-thuc",
    "kien thuc":          "kien-thuc",
    "knowledge":          "kien-thuc",
    "beginner":           "kien-thuc",
    "hướng dẫn":          "kien-thuc",
    "huong-dan":          "kien-thuc",
}

TAG_DISPLAY_NAME = {
    "tin-cong-ty":   "Tin Công Ty",
    "tin-cong-nghe": "Tin Công Nghệ",
    "case-study":    "Case Study",
    "insight":       "Insight",
    "kien-thuc":     "Kiến Thức",
}


def _resolve_tag_slug(raw: str) -> str:
    """Chuẩn hóa tag về slug hợp lệ. Raise nếu không tìm thấy."""
    key = raw.strip().lower()
    slug = TAG_SLUG_MAP.get(key)
    if not slug:
        valid = list(TAG_DISPLAY_NAME.keys())
        raise ValueError(
            f"Tag '{raw}' không hợp lệ.\n"
            f"Chỉ dùng một trong: {valid}\n"
            f"TUYỆT ĐỐI không tạo tag mới."
        )
    return slug


def _headers(content_type: str = "application/json") -> dict:
    """Tạo Authorization header từ Application Password."""
    credentials = f"{WP_USERNAME}:{WP_APP_PASSWORD}"
    token = base64.b64encode(credentials.encode()).decode()
    return {
        "Authorization": f"Basic {token}",
        "Content-Type": content_type,
    }


def _get_or_create_tag(tag_slug: str) -> int:
    """
    Lấy hoặc tạo tag WordPress theo slug. Trả về tag ID.
    """
    tag_name = TAG_DISPLAY_NAME[tag_slug]

    # Tìm tag theo slug
    resp = requests.get(
        f"{WP_URL}/wp-json/wp/v2/tags",
        params={"slug": tag_slug},
        headers=_headers(),
        timeout=15,
    )
    resp.raise_for_status()
    tags = resp.json()
    if tags:
        return tags[0]["id"]

    # Tạo mới nếu chưa có
    resp = requests.post(
        f"{WP_URL}/wp-json/wp/v2/tags",
        json={"name": tag_name, "slug": tag_slug},
        headers=_headers(),
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()["id"]


def _upload_image(image_url: str) -> int | None:
    """
    Download ảnh từ URL và upload lên WordPress Media Library.
    Trả về media ID, hoặc None nếu thất bại.
    """
    try:
        img_resp = requests.get(image_url, timeout=30)
        img_resp.raise_for_status()

        # Xác định content-type và tên file
        content_type = img_resp.headers.get("Content-Type", "image/jpeg").split(";")[0]
        ext = content_type.split("/")[-1]
        filename = f"cover.{ext}"

        credentials = f"{WP_USERNAME}:{WP_APP_PASSWORD}"
        token = base64.b64encode(credentials.encode()).decode()
        upload_headers = {
            "Authorization": f"Basic {token}",
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Type": content_type,
        }

        resp = requests.post(
            f"{WP_URL}/wp-json/wp/v2/media",
            headers=upload_headers,
            data=img_resp.content,
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()["id"]

    except Exception as e:
        print(f"[WARN] Upload ảnh thất bại: {e}")
        return None


# ──────────────────────────────────────────────
# PUBLIC API
# ──────────────────────────────────────────────

def create_post(
    title: str,
    html: str,
    tag_slug: str,
    slug: str,
    excerpt: str = "",
    feature_image: str = "",
    status: str = "draft",
) -> dict:
    """
    Tạo bài viết mới trên WordPress.

    Args:
        title:         Tiêu đề bài viết
        html:          Nội dung HTML đã format
        tag_slug:      Một trong 4 tag hợp lệ (tin-cong-ty, tin-cong-nghe, case-study, insight)
        slug:          URL slug — PHẢI truyền thủ công, không để WordPress tự generate
        excerpt:       Meta description (120-155 ký tự)
        feature_image: URL ảnh cover (sẽ upload lên Media Library tự động)
        status:        "draft" (mặc định) hoặc "publish"

    Returns:
        dict chứa thông tin bài vừa tạo (id, url, slug, status)
    """
    resolved_slug = _resolve_tag_slug(tag_slug)

    # Lấy/tạo tag và lấy ID
    tag_id = _get_or_create_tag(resolved_slug)

    # Upload ảnh cover lên Media Library
    featured_media_id = None
    if feature_image:
        featured_media_id = _upload_image(feature_image)

    payload = {
        "title":   title,
        "content": html,
        "slug":    slug,
        "excerpt": excerpt[:155] if excerpt else "",
        "status":  status,
        "tags":    [tag_id],
    }
    if featured_media_id:
        payload["featured_media"] = featured_media_id

    resp = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts",
        json=payload,
        headers=_headers(),
        timeout=30,
    )

    if not resp.ok:
        raise RuntimeError(
            f"WordPress API lỗi {resp.status_code}: {resp.text[:500]}"
        )

    post = resp.json()
    return {
        "id":     post["id"],
        "title":  post["title"]["rendered"],
        "slug":   post["slug"],
        "status": post["status"],
        "url":    post.get("link", f"{WP_URL}/?p={post['id']}"),
    }


def update_post(post_id: int, updates: dict) -> dict:
    """
    Cập nhật bài viết đã có (ví dụ: đổi status draft → publish).

    Args:
        post_id: WordPress post ID
        updates: dict các field muốn cập nhật

    Returns:
        dict thông tin bài sau khi cập nhật
    """
    resp = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts/{post_id}",
        json=updates,
        headers=_headers(),
        timeout=30,
    )
    if not resp.ok:
        raise RuntimeError(
            f"Update thất bại {resp.status_code}: {resp.text[:500]}"
        )

    post = resp.json()
    return {
        "id":     post["id"],
        "slug":   post["slug"],
        "status": post["status"],
        "url":    post.get("link", ""),
    }


def fetch_published_posts(limit: int = 50) -> list[dict]:
    """
    Lấy danh sách bài đã đăng — dùng để tạo internal links.

    Returns:
        list of dict: [{"title": ..., "slug": ..., "url": ..., "tag": ...}]
    """
    resp = requests.get(
        f"{WP_URL}/wp-json/wp/v2/posts",
        params={
            "per_page": limit,
            "status":   "publish",
            "_fields":  "id,title,slug,link,tags",
            "_embed":   "wp:term",
        },
        headers=_headers(),
        timeout=15,
    )

    if not resp.ok:
        print(f"[WARN] Không fetch được danh sách bài: {resp.status_code}")
        return []

    posts = resp.json()
    result = []
    for p in posts:
        title = p.get("title", {}).get("rendered", "")

        # Lấy tag slug từ _embedded
        tag_slug = "unknown"
        for term_group in p.get("_embedded", {}).get("wp:term", []):
            for term in term_group:
                if term.get("taxonomy") == "post_tag":
                    tag_slug = term.get("slug", "unknown")
                    break

        result.append({
            "title": title,
            "slug":  p["slug"],
            "url":   p.get("link", f"{WP_URL}/?p={p['id']}"),
            "tag":   tag_slug,
        })

    return result


def format_posts_for_linking(posts: list[dict]) -> str:
    """
    Format danh sách bài thành text dễ đọc để Claude dùng khi tạo internal links.

    Output ví dụ:
        [case-study] Fintech Startup Giảm 40% Chi Phí QA
            URL: https://example.com/fintech-qa-case-study/

        [insight] Tại Sao Outsource Testing Hiệu Quả Hơn
            URL: https://example.com/tai-sao-outsource-testing/
    """
    if not posts:
        return "(Chưa có bài nào được đăng — bỏ qua bước internal linking)"

    lines = ["=== DANH SÁCH BÀI ĐÃ ĐĂNG (dùng để tạo internal links) ===\n"]
    for p in posts:
        lines.append(f"[{p['tag']}] {p['title']}")
        lines.append(f"    URL: {p['url']}\n")

    return "\n".join(lines)


def check_slug_exists(slug: str) -> bool:
    """Kiểm tra slug đã tồn tại trên WordPress chưa."""
    resp = requests.get(
        f"{WP_URL}/wp-json/wp/v2/posts",
        params={"slug": slug, "_fields": "id,slug"},
        headers=_headers(),
        timeout=10,
    )
    if not resp.ok:
        return False
    return len(resp.json()) > 0
