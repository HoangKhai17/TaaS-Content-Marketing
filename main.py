"""
main.py — Entry point cho TaaS Content Marketing Skill

Pipeline 7 bước:
  1. Nhập topic & thông tin bài
  2. Chuẩn bị: fetch internal links + validate slug
  3. (Bước research & viết do Claude thực hiện trong SKILL.md)
  4. Validate SEO + AEO + E-E-A-T
  5. Tìm ảnh cover + inline
  6. Preview & xác nhận
  7. Publish lên WordPress

Cách dùng:
  python main.py \\
    --file bai_viet.html \\
    --title "Fintech Startup Giảm 40% Chi Phí QA Nhờ TaaS" \\
    --slug "fintech-qa-case-study" \\
    --type case-study \\
    --tag case-study \\
    --excerpt "Câu chuyện thực tế: từ 30 bug/sprint xuống 4..." \\
    --image-queries "software testing team" "QA automation dashboard"

  Thêm --publish để publish ngay thay vì lưu draft.
"""

import os
import sys
import argparse

from utils.wp_client import (
    create_post,
    fetch_published_posts,
    format_posts_for_linking,
    check_slug_exists,
)
from utils.image_generator import search, search_multiple, format_cover_html
from utils.seo_validator import SEOValidator


# ──────────────────────────────────────────────
# Màu terminal (optional, graceful fallback)
# ──────────────────────────────────────────────
def _c(text: str, code: str) -> str:
    """Wrap text với ANSI color nếu terminal hỗ trợ."""
    if sys.stdout.isatty():
        return f"\033[{code}m{text}\033[0m"
    return text

GREEN  = lambda t: _c(t, "32")
YELLOW = lambda t: _c(t, "33")
RED    = lambda t: _c(t, "31")
BOLD   = lambda t: _c(t, "1")
DIM    = lambda t: _c(t, "2")


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────
def _read_html(file_path: str) -> str:
    """Đọc file HTML bài viết."""
    if not os.path.exists(file_path):
        print(RED(f"❌  File không tồn tại: {file_path}"))
        sys.exit(1)
    with open(file_path, encoding="utf-8") as f:
        return f.read()


def _confirm(prompt: str) -> bool:
    """Hỏi xác nhận yes/no."""
    while True:
        ans = input(f"\n{prompt} [y/n]: ").strip().lower()
        if ans in ("y", "yes", "có", "c"):
            return True
        if ans in ("n", "no", "không", "k"):
            return False
        print(DIM("  → Nhập y hoặc n"))


def _print_divider(label: str = ""):
    width = 52
    if label:
        pad = (width - len(label) - 2) // 2
        print(f"\n{'─' * pad} {BOLD(label)} {'─' * pad}")
    else:
        print("─" * width)


# ──────────────────────────────────────────────
# Bước 0 — Chuẩn bị
# ──────────────────────────────────────────────
def step_prepare(slug: str) -> list[dict]:
    """Fetch internal links + kiểm tra slug trùng."""
    _print_divider("BƯỚC 0 — CHUẨN BỊ")

    # Fetch bài đã đăng
    print("⏳  Đang fetch danh sách bài đã đăng...")
    posts = fetch_published_posts(limit=50)
    if posts:
        print(GREEN(f"✅  Tìm thấy {len(posts)} bài — dùng để tạo internal links"))
        print(DIM(format_posts_for_linking(posts)))
    else:
        print(YELLOW("⚠️   Chưa có bài nào — bỏ qua internal linking"))

    # Kiểm tra slug trùng
    print(f"\n⏳  Kiểm tra slug '{slug}'...")
    if check_slug_exists(slug):
        print(RED(f"❌  Slug '{slug}' đã tồn tại trên WordPress!"))
        new_slug = input("   → Nhập slug mới (để trống để thoát): ").strip()
        if not new_slug:
            sys.exit(1)
        return posts, new_slug
    else:
        print(GREEN(f"✅  Slug '{slug}' chưa tồn tại — OK"))

    return posts, slug


# ──────────────────────────────────────────────
# Bước 4 — Validate SEO / AEO / E-E-A-T
# ──────────────────────────────────────────────
def step_validate(html: str, tag_slug: str, title: str, slug: str, excerpt: str) -> bool:
    """Chạy SEOValidator và in kết quả. Return True nếu đạt."""
    _print_divider("BƯỚC 4 — KIỂM TRA CHẤT LƯỢNG")

    validator = SEOValidator()
    result = validator.validate(
        content_html=html,
        tag_slug=tag_slug,
        title=title,
        slug=slug,
        excerpt=excerpt,
    )

    # In keyword density
    density = validator.keyword_density(html)
    found_kw = {k: v for k, v in density.items() if v > 0}
    print(f"\n📊  Keyword density: {found_kw if found_kw else '(không tìm thấy từ khóa nào)'}")

    # In kết quả validate
    print(f"\n{result.summary()}")

    if not result.passed:
        print(RED("\n❌  Bài chưa đạt tiêu chuẩn — hãy sửa các vấn đề trên trước khi publish."))
        return False

    score_color = GREEN if result.score >= 80 else YELLOW
    print(score_color(f"\n✅  Bài đạt tiêu chuẩn (score: {result.score}/100)"))
    return True


# ──────────────────────────────────────────────
# Bước 5 — Tìm ảnh
# ──────────────────────────────────────────────
def step_images(image_queries: list[str], tag_slug: str) -> dict:
    """
    Tìm ảnh cover + inline.
    Returns {"cover": dict|None, "inline": list[dict]}
    """
    _print_divider("BƯỚC 5 — TÌM ẢNH")

    cover = None
    inline_images = []

    if not image_queries:
        print(YELLOW("⚠️   Không có --image-queries — dùng query mặc định theo loại bài"))
        image_queries = []

    # Ảnh cover — query đầu tiên
    cover_query = image_queries[0] if image_queries else ""
    print(f"⏳  Tìm ảnh cover: '{cover_query or '(default)'}' ...")
    covers = search(cover_query, tag_slug=tag_slug, count=1)
    if covers:
        cover = covers[0]
        print(GREEN(f"✅  Cover: {cover['source']} — {cover['url'][:60]}..."))
        print(DIM(f"   Credit: {cover['credit']}"))
    else:
        print(YELLOW("⚠️   Không tìm được ảnh cover — bài sẽ không có feature image"))

    # Ảnh inline — các query còn lại
    if len(image_queries) > 1:
        print(f"\n⏳  Tìm {len(image_queries) - 1} ảnh inline...")
        inline_images = search_multiple(image_queries[1:], tag_slug=tag_slug)
        print(GREEN(f"✅  Tìm được {len(inline_images)} ảnh inline"))
    else:
        print(DIM("   (Không có query inline — chỉ dùng ảnh cover)"))

    return {"cover": cover, "inline": inline_images}


# ──────────────────────────────────────────────
# Bước 6 — Preview
# ──────────────────────────────────────────────
def step_preview(
    title: str,
    slug: str,
    tag_slug: str,
    excerpt: str,
    html: str,
    images: dict,
    status: str,
):
    """In preview đầy đủ trước khi publish."""
    _print_divider("BƯỚC 6 — PREVIEW")

    word_count = len(html.split())
    cover = images.get("cover")
    inline = images.get("inline", [])

    print(f"""
  Tiêu đề   : {BOLD(title)}
  URL Slug   : /{slug}/
  Loại bài   : {tag_slug}
  Status     : {'🟢 PUBLISHED' if status == 'publish' else '🟡 DRAFT'}
  Số chữ     : ~{word_count:,} từ (HTML)
  Excerpt    : {excerpt[:80]}{'...' if len(excerpt) > 80 else ''}

  🎨 ẢNH
  Cover      : {cover['source'] + ' — ' + cover['url'][:50] + '...' if cover else '(không có)'}
  Inline     : {len(inline)} ảnh
  """)


# ──────────────────────────────────────────────
# Bước 7 — Publish
# ──────────────────────────────────────────────
def step_publish(
    title: str,
    html: str,
    tag_slug: str,
    slug: str,
    excerpt: str,
    cover_url: str,
    status: str,
) -> dict:
    """Gọi WordPress REST API để tạo bài."""
    _print_divider("BƯỚC 7 — PUBLISH")
    print(f"⏳  Đang đăng bài lên WordPress ({status})...")

    result = create_post(
        title=title,
        html=html,
        tag_slug=tag_slug,
        slug=slug,
        excerpt=excerpt,
        feature_image=cover_url,
        status=status,
    )

    print(GREEN(f"\n✅  Đăng thành công!"))
    print(f"   ID     : {result['id']}")
    print(f"   Status : {result['status']}")
    print(f"   URL    : {BOLD(result['url'])}")

    return result


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────
def build_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="TaaS Content Marketing — Publish bài viết lên WordPress",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--file", required=True,
        metavar="FILE.html",
        help="Path đến file HTML bài viết (Claude xuất ra)",
    )
    parser.add_argument(
        "--title", required=True,
        help="Tiêu đề bài viết",
    )
    parser.add_argument(
        "--slug", required=True,
        help="URL slug — tối đa 5 từ, chỉ a-z 0-9 dấu gạch ngang\n"
             "Ví dụ: fintech-qa-case-study",
    )
    parser.add_argument(
        "--type", required=True,
        choices=["tin-cong-ty", "tin-cong-nghe", "case-study", "insight"],
        dest="post_type",
        help="Loại bài viết",
    )
    parser.add_argument(
        "--tag", required=True,
        help="Tag WordPress — phải khớp với --type\n"
             "Hợp lệ: tin-cong-ty | tin-cong-nghe | case-study | insight",
    )
    parser.add_argument(
        "--excerpt", default="",
        help="Meta description (120-155 ký tự)",
    )
    parser.add_argument(
        "--image-queries", nargs="+", default=[],
        metavar="QUERY",
        help='Query tìm ảnh bằng tiếng Anh\n'
             'Query đầu = ảnh cover, query sau = ảnh inline\n'
             'Ví dụ: --image-queries "software testing" "QA dashboard"',
    )
    parser.add_argument(
        "--publish", action="store_true",
        help="Publish ngay (mặc định là lưu draft)",
    )
    parser.add_argument(
        "--skip-validate", action="store_true",
        help="Bỏ qua bước kiểm tra SEO/AEO (không khuyến khích)",
    )

    return parser.parse_args()


def main():
    args = build_args()

    print(BOLD("\n🚀  TaaS Content Marketing — Pipeline bắt đầu"))
    print(DIM(f"   File: {args.file} | Type: {args.post_type} | Slug: {args.slug}"))

    # Đọc file HTML
    html = _read_html(args.file)

    status = "publish" if args.publish else "draft"

    # ── Bước 0: Chuẩn bị ──────────────────────
    posts, final_slug = step_prepare(args.slug)

    # ── Bước 4: Validate ──────────────────────
    if not args.skip_validate:
        passed = step_validate(
            html=html,
            tag_slug=args.post_type,
            title=args.title,
            slug=final_slug,
            excerpt=args.excerpt,
        )
        if not passed:
            if not _confirm(YELLOW("⚠️   Bài chưa đạt tiêu chuẩn. Vẫn tiếp tục?")):
                print(RED("   → Đã hủy. Sửa bài và chạy lại."))
                sys.exit(0)
    else:
        print(YELLOW("⚠️   Bỏ qua bước validate (--skip-validate)"))

    # ── Bước 5: Tìm ảnh ───────────────────────
    images = step_images(args.image_queries, args.post_type)
    cover_url = images["cover"]["url"] if images.get("cover") else ""

    # ── Bước 6: Preview ───────────────────────
    step_preview(
        title=args.title,
        slug=final_slug,
        tag_slug=args.post_type,
        excerpt=args.excerpt,
        html=html,
        images=images,
        status=status,
    )

    action = "PUBLISH" if status == "publish" else "lưu DRAFT"
    if not _confirm(f"Xác nhận {action} bài này lên WordPress?"):
        print(DIM("   → Đã hủy. Không có thay đổi nào được thực hiện."))
        sys.exit(0)

    # ── Bước 7: Publish ───────────────────────
    step_publish(
        title=args.title,
        html=html,
        tag_slug=args.post_type,
        slug=final_slug,
        excerpt=args.excerpt,
        cover_url=cover_url,
        status=status,
    )

    _print_divider()
    print(GREEN("✅  Hoàn tất!\n"))

    if status == "draft":
        print(DIM("   → Vào WordPress Admin để xem lại trước khi publish chính thức."))


if __name__ == "__main__":
    main()
