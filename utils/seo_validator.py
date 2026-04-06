"""
seo_validator.py — Kiểm tra chất lượng SEO + AEO + E-E-A-T cho TaaS Content

Gồm 4 nhóm kiểm tra:
1. SEO cơ bản  — keyword, slug, excerpt, word count
2. AEO         — cấu trúc để AI (ChatGPT, Perplexity) có thể trích dẫn
3. E-E-A-T     — tín hiệu chuyên môn, bằng chứng, độ tin cậy
4. Format HTML — cấu trúc đúng chuẩn Ghost
"""

import re
from dataclasses import dataclass, field


# ──────────────────────────────────────────────
# Config theo loại bài
# ──────────────────────────────────────────────
WORD_COUNT_RANGE = {
    "tin-cong-ty":   (600,   800),
    "tin-cong-nghe": (1200, 1800),
    "case-study":    (1000, 1500),
    "insight":       (1500, 2500),
    "kien-thuc":     (800,  1200),
}

FORBIDDEN_WORDS = [
    # Marketing sáo rỗng
    "tự hào thông báo", "hân hạnh giới thiệu", "giải pháp toàn diện",
    "tối ưu vượt trội", "hàng đầu việt nam", "đẳng cấp", "tiên phong",
    "cam kết chất lượng", "đội ngũ chuyên nghiệp", "uy tín hàng đầu",
    # Insight forbidden
    "revolutionize", "game-changing", "cutting-edge", "thay đổi cuộc chơi",
    "cách mạng hóa", "đột phá", "tiên tiến nhất", "không thể bỏ qua",
    # Tin công ty forbidden
    "hành trình", "sứ mệnh vĩ đại", "tầm nhìn chiến lược",
]

# Nguồn uy tín ngành testing/tech
AUTHORITY_SOURCES = [
    "gartner", "forrester", "stack overflow", "dora report",
    "thoughtworks", "tricentis", "smartbear", "infoq",
    "state of testing", "ministry of testing",
]

# Từ khóa TaaS B2B cốt lõi
CORE_KEYWORDS = {
    "primary": ["TaaS", "Testing as a Service", "kiểm thử phần mềm"],
    "secondary": [
        "QA", "quality assurance", "test automation", "kiểm thử tự động",
        "outsource testing", "outsource QA", "regression testing",
        "software testing", "CI/CD", "DevOps",
    ],
}

# Từ khóa AEO — dấu hiệu có FAQ/structured answer
AEO_SIGNALS = [
    r"là gì\?", r"tại sao", r"như thế nào\?", r"khi nào",
    r"bao nhiêu", r"có nên", r"nên chọn",
]


# ──────────────────────────────────────────────
# Data class kết quả
# ──────────────────────────────────────────────
@dataclass
class ValidationResult:
    passed: bool = True
    score: int = 100          # 0-100
    issues: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)

    def fail(self, msg: str, deduct: int = 5):
        self.passed = False
        self.score = max(0, self.score - deduct)
        self.issues.append(f"❌ {msg}")

    def warn(self, msg: str, deduct: int = 2):
        self.score = max(0, self.score - deduct)
        self.warnings.append(f"⚠️  {msg}")

    def suggest(self, msg: str):
        self.suggestions.append(f"💡 {msg}")

    def summary(self) -> str:
        lines = [f"{'✅ PASSED' if self.passed else '❌ FAILED'} — Score: {self.score}/100\n"]
        if self.issues:
            lines += ["── Vấn đề cần sửa:"] + self.issues
        if self.warnings:
            lines += ["\n── Cảnh báo:"] + self.warnings
        if self.suggestions:
            lines += ["\n── Gợi ý cải thiện:"] + self.suggestions
        return "\n".join(lines)


# ──────────────────────────────────────────────
# Helper
# ──────────────────────────────────────────────
def _word_count(text: str) -> int:
    """Đếm số từ — tính cả tiếng Việt (split by whitespace)."""
    return len(text.split())


def _strip_html(html: str) -> str:
    """Xóa HTML tags để đếm từ và tìm keyword trong text thuần."""
    return re.sub(r"<[^>]+>", " ", html)


def _count_occurrences(text: str, keyword: str) -> int:
    return len(re.findall(re.escape(keyword.lower()), text.lower()))


def _has_tag(html: str, tag: str) -> bool:
    return bool(re.search(rf"<{tag}[\s>]", html, re.IGNORECASE))


def _count_tags(html: str, tag: str) -> int:
    return len(re.findall(rf"<{tag}[\s>]", html, re.IGNORECASE))


# ──────────────────────────────────────────────
# Nhóm kiểm tra 1 — SEO cơ bản
# ──────────────────────────────────────────────
def _check_seo_basic(
    content_html: str,
    tag_slug: str,
    title: str,
    slug: str,
    excerpt: str,
    result: ValidationResult,
):
    plain = _strip_html(content_html)
    words = _word_count(plain)

    # Word count
    lo, hi = WORD_COUNT_RANGE.get(tag_slug, (800, 2000))
    if words < lo:
        result.fail(f"Bài quá ngắn: {words} chữ (tối thiểu {lo} cho loại '{tag_slug}')", deduct=10)
    elif words > hi:
        result.warn(f"Bài hơi dài: {words} chữ (tối đa gợi ý {hi} cho loại '{tag_slug}')", deduct=3)

    # Primary keyword trong tiêu đề
    primary_in_title = any(
        kw.lower() in title.lower()
        for kw in CORE_KEYWORDS["primary"] + CORE_KEYWORDS["secondary"]
    )
    if not primary_in_title:
        result.warn("Tiêu đề không chứa từ khóa TaaS/QA/testing nào", deduct=5)

    # Keyword trong 100 từ đầu
    first_100 = " ".join(plain.split()[:100]).lower()
    has_keyword_early = any(
        kw.lower() in first_100
        for kw in CORE_KEYWORDS["primary"] + CORE_KEYWORDS["secondary"][:3]
    )
    if not has_keyword_early:
        result.warn("Không có từ khóa chính trong 100 từ đầu tiên", deduct=4)

    # Slug
    if not slug:
        result.fail("Thiếu slug — PHẢI truyền slug thủ công", deduct=15)
    else:
        if len(slug.split("-")) > 6:
            result.warn(f"Slug '{slug}' quá dài (hơn 5 từ) — nên rút ngắn", deduct=3)
        if re.search(r"[^a-z0-9-]", slug):
            result.fail(f"Slug '{slug}' chứa ký tự không hợp lệ (chỉ dùng a-z, 0-9, -)", deduct=10)

    # Excerpt
    if not excerpt:
        result.fail("Thiếu excerpt (meta description)", deduct=8)
    elif len(excerpt) < 100:
        result.warn(f"Excerpt quá ngắn: {len(excerpt)} ký tự (nên 120-155)", deduct=3)
    elif len(excerpt) > 160:
        result.warn(f"Excerpt quá dài: {len(excerpt)} ký tự (Google cắt sau 155)", deduct=2)

    # Forbidden words
    for fw in FORBIDDEN_WORDS:
        if fw.lower() in plain.lower():
            result.warn(f"Từ bị cấm: '{fw}'", deduct=3)


# ──────────────────────────────────────────────
# Nhóm kiểm tra 2 — AEO (Answer Engine Optimization)
# ──────────────────────────────────────────────
def _check_aeo(content_html: str, result: ValidationResult):
    plain = _strip_html(content_html)

    # Có đoạn trả lời thẳng câu hỏi (FAQ-style)
    has_question_pattern = any(
        re.search(pattern, plain, re.IGNORECASE)
        for pattern in AEO_SIGNALS
    )
    if not has_question_pattern:
        result.warn(
            "Không tìm thấy pattern câu hỏi trong bài (là gì?, tại sao, như thế nào?) "
            "— AEO yêu cầu ít nhất 1 đoạn trả lời thẳng câu hỏi",
            deduct=5,
        )

    # Có danh sách có cấu trúc
    list_count = _count_tags(content_html, "ul") + _count_tags(content_html, "ol")
    if list_count == 0:
        result.warn("Không có <ul> hay <ol> — danh sách có cấu trúc giúp AI trích dẫn dễ hơn", deduct=4)
    elif list_count == 1:
        result.suggest("Nên có 2-3 danh sách <ul>/<ol> để tối ưu AEO")

    # Có H2/H3 dạng câu — tốt cho AEO
    headings = re.findall(r"<h[23][^>]*>(.*?)</h[23]>", content_html, re.IGNORECASE | re.DOTALL)
    informative_headings = [
        h for h in headings
        if len(_strip_html(h).split()) >= 4  # H2/H3 có ít nhất 4 từ = mang thông tin
    ]
    if len(informative_headings) < 2:
        result.warn(
            "Ít H2/H3 có nội dung đầy đủ — headings ngắn như 'Giới thiệu', 'Kết luận' "
            "không giúp ích cho AEO",
            deduct=3,
        )

    # Đoạn mở đầu ngắn gọn (150 chữ đầu)
    first_150 = " ".join(_strip_html(content_html).split()[:150])
    if len(first_150.split()) < 80:
        result.warn("Đoạn mở quá ngắn — AEO cần 100-150 chữ đầu tóm tắt được toàn bài", deduct=3)


# ──────────────────────────────────────────────
# Nhóm kiểm tra 3 — E-E-A-T
# ──────────────────────────────────────────────
def _check_eeat(content_html: str, tag_slug: str, result: ValidationResult):
    plain = _strip_html(content_html).lower()

    # Authority — có nguồn uy tín không
    found_sources = [s for s in AUTHORITY_SOURCES if s in plain]
    if tag_slug in ("tin-cong-nghe", "insight"):
        if len(found_sources) < 2:
            result.fail(
                f"Chỉ tìm thấy {len(found_sources)} nguồn uy tín "
                f"(Gartner, Forrester, Stack Overflow...) — cần ít nhất 2 cho loại '{tag_slug}'",
                deduct=10,
            )
        elif len(found_sources) < 3:
            result.warn("Nên có ít nhất 3 nguồn uy tín cho bài phân tích/insight", deduct=3)
    elif tag_slug == "kien-thuc":
        # Bài kiến thức ưu tiên analogy và ví dụ thực tế, không bắt buộc nguồn học thuật
        analogy_signals = ["hãy hình dung", "hãy nghĩ", "giống như", "ví như", "tương tự"]
        has_analogy = any(sig in plain for sig in analogy_signals)
        if not has_analogy:
            result.warn(
                "Bài kiến thức nên có ít nhất 1 analogy đời thường — "
                "giúp người mới dễ hiểu hơn",
                deduct=5,
            )
    elif tag_slug == "case-study":
        # Case study cần số liệu, không nhất thiết cần nguồn ngoài
        pass

    # Expertise — có số liệu % hay con số cụ thể không
    has_numbers = bool(re.search(r"\d+\s*%|\d{2,}(?:\s*triệu|\s*nghìn|\s*USD|\s*VND)?", plain))
    if not has_numbers:
        result.warn("Không tìm thấy số liệu cụ thể (%, triệu, USD...) — E-E-A-T yêu cầu bằng chứng đo được", deduct=5)

    # Trust — có thừa nhận giới hạn/ngoại lệ không (insight/tin-cong-nghe)
    trust_signals = ["không áp dụng", "ngoại lệ", "tuy nhiên", "nhưng", "giới hạn", "lưu ý"]
    has_trust = any(sig in plain for sig in trust_signals)
    if tag_slug in ("insight", "tin-cong-nghe") and not has_trust:
        result.suggest(
            "Thêm phần thừa nhận ngoại lệ hoặc giới hạn — giúp tăng Trust trong E-E-A-T"
        )

    # Experience — có ví dụ thực tế không
    example_signals = ["ví dụ", "chẳng hạn", "cụ thể", "thực tế", "case", "dự án"]
    has_example = any(sig in plain for sig in example_signals)
    if not has_example:
        result.warn("Không tìm thấy ví dụ thực tế — E-E-A-T yêu cầu 'Experience'", deduct=4)


# ──────────────────────────────────────────────
# Nhóm kiểm tra 4 — Format HTML
# ──────────────────────────────────────────────
def _check_html_format(content_html: str, result: ValidationResult):
    # Không được dùng H1 trong body
    if _has_tag(content_html, "h1"):
        result.fail("Bài chứa <h1> — không dùng H1 trong body, chỉ dùng H2 và H3", deduct=8)

    # Phải có ít nhất 2 H2
    h2_count = _count_tags(content_html, "h2")
    if h2_count < 2:
        result.fail(f"Chỉ có {h2_count} thẻ <h2> — cần ít nhất 2 để có cấu trúc rõ ràng", deduct=8)

    # Paragraph không quá dài
    paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", content_html, re.IGNORECASE | re.DOTALL)
    long_paras = [
        i + 1 for i, p in enumerate(paragraphs)
        if _word_count(_strip_html(p)) > 100
    ]
    if long_paras:
        result.warn(
            f"Đoạn văn {long_paras} có hơn 100 chữ — nên tách nhỏ để dễ đọc trên mobile",
            deduct=2,
        )

    # Inline CSS bị cấm
    if re.search(r'style\s*=\s*["\']', content_html):
        result.warn("Phát hiện inline CSS (style='...') — không dùng inline CSS", deduct=3)

    # Internal link
    internal_links = re.findall(r'<a\s+href=["\'](?!http)', content_html)
    if not internal_links:
        result.suggest("Thêm 2-3 internal links sang bài liên quan (case study ↔ insight)")

    # Blockquote — tín hiệu tốt cho AEO và E-E-A-T
    if not _has_tag(content_html, "blockquote"):
        result.suggest("Thêm <blockquote> cho quote hoặc insight nổi bật — tốt cho AEO")


# ──────────────────────────────────────────────
# Case study specific checks
# ──────────────────────────────────────────────
def _check_case_study(content_html: str, result: ValidationResult):
    plain = _strip_html(content_html).lower()

    # Phải có pattern trước/sau
    has_before_after = (
        ("trước" in plain and "sau" in plain) or
        ("before" in plain and "after" in plain) or
        ("từ" in plain and "xuống" in plain) or
        ("tăng" in plain or "giảm" in plain)
    )
    if not has_before_after:
        result.fail(
            "Case study thiếu so sánh Trước/Sau — đây là yếu tố bắt buộc",
            deduct=12,
        )

    # Phải có ít nhất 4 con số
    numbers = re.findall(r"\d+\s*%|\d{2,}", plain)
    if len(numbers) < 4:
        result.fail(
            f"Case study chỉ có {len(numbers)} con số — cần ít nhất 4 số liệu đo được",
            deduct=10,
        )

    # Phải có phần kết quả
    result_signals = ["kết quả", "result", "đạt được", "cải thiện", "giảm", "tăng", "tiết kiệm"]
    if not any(sig in plain for sig in result_signals):
        result.fail("Không tìm thấy section kết quả — case study bắt buộc phải có", deduct=12)


# ──────────────────────────────────────────────
# PUBLIC API
# ──────────────────────────────────────────────

class SEOValidator:
    """
    Validator tổng hợp cho tất cả loại bài TaaS.

    Sử dụng:
        validator = SEOValidator()
        result = validator.validate(
            content_html=html_string,
            tag_slug="case-study",
            title="Fintech Startup Giảm 40% Chi Phí QA",
            slug="fintech-qa-case-study",
            excerpt="Mô tả ngắn 120-155 ký tự...",
        )
        print(result.summary())
        if not result.passed:
            # Sửa bài trước khi publish
    """

    def validate(
        self,
        content_html: str,
        tag_slug: str,
        title: str = "",
        slug: str = "",
        excerpt: str = "",
    ) -> ValidationResult:
        """
        Chạy toàn bộ kiểm tra và trả về kết quả tổng hợp.

        Args:
            content_html: HTML body của bài viết (không bao gồm <html>, <body>)
            tag_slug:     Loại bài: tin-cong-ty | tin-cong-nghe | case-study | insight
            title:        Tiêu đề bài viết
            slug:         URL slug
            excerpt:      Meta description

        Returns:
            ValidationResult với score, issues, warnings, suggestions
        """
        result = ValidationResult()

        valid_tags = list(WORD_COUNT_RANGE.keys())
        if tag_slug not in valid_tags:
            result.fail(
                f"tag_slug '{tag_slug}' không hợp lệ. Chỉ dùng: {valid_tags}",
                deduct=20,
            )
            return result

        # Chạy từng nhóm kiểm tra
        _check_seo_basic(content_html, tag_slug, title, slug, excerpt, result)
        _check_aeo(content_html, result)
        _check_eeat(content_html, tag_slug, result)
        _check_html_format(content_html, result)

        # Kiểm tra thêm cho case study
        if tag_slug == "case-study":
            _check_case_study(content_html, result)

        # Tổng kết passed/failed
        result.passed = len(result.issues) == 0

        return result

    def quick_check(self, content_html: str, tag_slug: str) -> bool:
        """Trả về True nếu bài đạt tối thiểu (không có issues critical)."""
        result = self.validate(content_html, tag_slug)
        return result.passed

    def keyword_density(self, content_html: str) -> dict:
        """
        Báo cáo density của các từ khóa TaaS chính.
        Trả về dict: {keyword: count}
        """
        plain = _strip_html(content_html).lower()
        all_keywords = CORE_KEYWORDS["primary"] + CORE_KEYWORDS["secondary"]
        return {
            kw: _count_occurrences(plain, kw)
            for kw in all_keywords
        }
