"""
seo_validator.py — Kiểm tra từ khóa TaaS B2B trong bài viết
"""


class SEOValidator:
    REQUIRED_KEYWORDS = [
        "TaaS",
        "Testing as a Service",
        "QA",
        "kiểm thử",
    ]

    def validate(self, content: str) -> dict:
        """Kiểm tra các từ khóa bắt buộc có xuất hiện trong nội dung."""
        results = {}
        for kw in self.REQUIRED_KEYWORDS:
            results[kw] = kw.lower() in content.lower()
        return results
