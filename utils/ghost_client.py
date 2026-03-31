"""
ghost_client.py — Ghost CMS Admin API client cho TaaS Content Marketing

Hỗ trợ:
- Xác thực JWT từ Admin API Key
- Tạo / cập nhật bài viết (draft hoặc published)
- Fetch danh sách bài đã đăng để tạo internal links
- Gán tag theo 4 danh mục: tin-cong-ty, tin-cong-nghe, case-study, insight
"""

import os
import jwt
import time
import requests
from dotenv import load_dotenv

load_dotenv()

GHOST_API_URL = os.getenv("GHOST_API_URL", "").rstrip("/")
GHOST_ADMIN_API_KEY = os.getenv("GHOST_ADMIN_API_KEY", "")

# ──────────────────────────────────────────────
# TAG MAPPING — 4 tags cố định, KHÔNG tạo thêm
# ──────────────────────────────────────────────
TAG_SLUG_MAP = {
    "tin-cong-ty":   "tin-cong-ty",
    "tin cong ty":   "tin-cong-ty",
    "company":       "tin-cong-ty",

    "tin-cong-nghe": "tin-cong-nghe",
    "tin cong nghe": "tin-cong-nghe",
    "tech":          "tin-cong-nghe",
    "technology":    "tin-cong-nghe",

    "case-study":    "case-study",
    "case study":    "case-study",
    "casestudy":     "case-study",

    "insight":       "insight",
    "thought leadership": "insight",
}

TAG_DISPLAY_NAME = {
    "tin-cong-ty":   "Tin Công Ty",
    "tin-cong-nghe": "Tin Công Nghệ",
    "case-study":    "Case Study",
    "insight":       "Insight",
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


def _generate_jwt() -> str:
    """
    Tạo JWT token từ Ghost Admin API Key.
    Format key: "key_id:secret_hex"
    """
    if ":" not in GHOST_ADMIN_API_KEY:
        raise ValueError(
            "GHOST_ADMIN_API_KEY sai format. "
            "Phải là 'key_id:secret' — lấy từ Ghost Admin → Settings → Integrations."
        )

    key_id, secret = GHOST_ADMIN_API_KEY.split(":", 1)
    secret_bytes = bytes.fromhex(secret)

    payload = {
        "iat": int(time.time()),
        "exp": int(time.time()) + 300,  # hết hạn sau 5 phút
        "aud": "/admin/",
    }

    token = jwt.encode(
        payload,
        secret_bytes,
        algorithm="HS256",
        headers={"alg": "HS256", "typ": "JWT", "kid": key_id},
    )

    return token


def _headers() -> dict:
    return {
        "Authorization": f"Ghost {_generate_jwt()}",
        "Content-Type": "application/json",
        "Accept-Version": "v5.0",
    }


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
    Tạo bài viết mới trên Ghost.

    Args:
        title:         Tiêu đề bài viết
        html:          Nội dung HTML đã format
        tag_slug:      Một trong 4 tag hợp lệ (tin-cong-ty, tin-cong-nghe, case-study, insight)
        slug:          URL slug — PHẢI truyền thủ công, không để Ghost tự generate
        excerpt:       Meta description (120-155 ký tự)
        feature_image: URL ảnh cover
        status:        "draft" (mặc định) hoặc "published"

    Returns:
        dict chứa thông tin bài vừa tạo (id, url, slug, status)
    """
    resolved_slug = _resolve_tag_slug(tag_slug)
    tag_name = TAG_DISPLAY_NAME[resolved_slug]

    payload = {
        "posts": [
            {
                "title": title,
                "html": html,
                "slug": slug,
                "custom_excerpt": excerpt[:155] if excerpt else "",
                "feature_image": feature_image,
                "status": status,
                "tags": [
                    {"slug": resolved_slug, "name": tag_name}
                ],
            }
        ]
    }

    url = f"{GHOST_API_URL}/ghost/api/admin/posts/?source=html"
    resp = requests.post(url, json=payload, headers=_headers(), timeout=30)

    if not resp.ok:
        raise RuntimeError(
            f"Ghost API lỗi {resp.status_code}: {resp.text[:500]}"
        )

    post = resp.json()["posts"][0]
    return {
        "id":     post["id"],
        "title":  post["title"],
        "slug":   post["slug"],
        "status": post["status"],
        "url":    post.get("url", f"{GHOST_API_URL}/{post['slug']}/"),
    }


def update_post(post_id: str, updates: dict) -> dict:
    """
    Cập nhật bài viết đã có (ví dụ: đổi status draft → published).

    Args:
        post_id: Ghost post ID
        updates: dict các field muốn cập nhật

    Returns:
        dict thông tin bài sau khi cập nhật
    """
    # Ghost yêu cầu truyền updated_at để tránh conflict
    get_url = f"{GHOST_API_URL}/ghost/api/admin/posts/{post_id}/"
    get_resp = requests.get(get_url, headers=_headers(), timeout=15)
    if not get_resp.ok:
        raise RuntimeError(f"Không lấy được bài {post_id}: {get_resp.text[:300]}")

    current = get_resp.json()["posts"][0]
    updates["updated_at"] = current["updated_at"]

    put_url = f"{GHOST_API_URL}/ghost/api/admin/posts/{post_id}/"
    put_resp = requests.put(
        put_url,
        json={"posts": [updates]},
        headers=_headers(),
        timeout=30,
    )

    if not put_resp.ok:
        raise RuntimeError(
            f"Update thất bại {put_resp.status_code}: {put_resp.text[:500]}"
        )

    post = put_resp.json()["posts"][0]
    return {
        "id":     post["id"],
        "slug":   post["slug"],
        "status": post["status"],
        "url":    post.get("url", ""),
    }


def fetch_published_posts(limit: int = 50) -> list[dict]:
    """
    Lấy danh sách bài đã đăng — dùng để tạo internal links.

    Returns:
        list of dict: [{"title": ..., "slug": ..., "url": ..., "tag": ...}]
    """
    url = (
        f"{GHOST_API_URL}/ghost/api/admin/posts/"
        f"?limit={limit}&filter=status:published&fields=id,title,slug,url,tags"
    )
    resp = requests.get(url, headers=_headers(), timeout=15)

    if not resp.ok:
        print(f"[WARN] Không fetch được danh sách bài: {resp.status_code}")
        return []

    posts = resp.json().get("posts", [])
    result = []
    for p in posts:
        tags = p.get("tags", [])
        tag_slug = tags[0]["slug"] if tags else "unknown"
        result.append({
            "title": p["title"],
            "slug":  p["slug"],
            "url":   p.get("url", f"{GHOST_API_URL}/{p['slug']}/"),
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
    """Kiểm tra slug đã tồn tại trên Ghost chưa."""
    url = f"{GHOST_API_URL}/ghost/api/admin/posts/slug/{slug}/"
    resp = requests.get(url, headers=_headers(), timeout=10)
    return resp.ok  # 200 = tồn tại, 404 = chưa có
