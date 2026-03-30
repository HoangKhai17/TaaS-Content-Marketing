# taas-content-marketing

Skill sản xuất nội dung tự động cho website dịch vụ TaaS (Testing as a Service), tích hợp Ghost CMS.

---

## Cấu trúc thư mục

```
taas-content-marketing/
├── SKILL.md                    ← Router chính: detect loại bài, pipeline tổng quát
├── main.py                     ← Entry point (tái dùng từ skill du lịch, thay config)
├── requirements.txt
├── env.example
│
├── tin-cong-ty/
│   └── SKILL.md                ← Cấu trúc bài: thông báo sản phẩm, milestone, partnership
├── tin-cong-nghe/
│   └── SKILL.md                ← Bài phân tích xu hướng testing/QA, tin tức ngành
├── case-study/
│   └── SKILL.md                ← Template khách hàng: vấn đề → giải pháp → kết quả
└── insight/
    └── SKILL.md                ← Thought leadership: góc nhìn chuyên gia về TaaS/QA
│
└── utils/
    ├── ghost_client.py         ← Tái dùng từ skill du lịch
    ├── image_generator.py      ← Tái dùng
    └── seo_validator.py        ← Mới: kiểm tra từ khóa TaaS B2B
```

---

## 4 danh mục nội dung

| Thư mục | Tag Ghost | Mô tả |
|---|---|---|
| `tin-cong-ty/` | `tin-cong-ty` | Thông báo sản phẩm, milestone, partnership |
| `tin-cong-nghe/` | `tin-cong-nghe` | Phân tích xu hướng testing/QA, tin tức ngành |
| `case-study/` | `case-study` | Câu chuyện khách hàng: vấn đề → giải pháp → kết quả |
| `insight/` | `insight` | Thought leadership, góc nhìn chuyên gia về TaaS/QA |

---

## Pipeline 7 bước

```
1. Nhập topic  →  2. Nghiên cứu  →  3. Lập dàn ý  →  4. Viết bài
                                                            ↓
                           7. Xuất bản  ←  6. SEO + QC  ←  5. Tạo ảnh
```

---

## Setup

```bash
# 1. Cài dependencies
pip install -r requirements.txt

# 2. Tạo file .env từ template
cp env.example .env
```

Điền các giá trị vào `.env`:

```env
GHOST_API_URL=https://your-site.com
GHOST_ADMIN_API_KEY=your_admin_key
GHOST_CONTENT_API_KEY=your_content_key
KIE_API_KEY=your_kie_key
UNSPLASH_ACCESS_KEY=your_unsplash_key
```

---

## Sử dụng

```bash
python main.py \
  --topic "TaaS giúp startup tiết kiệm chi phí QA như thế nào" \
  --type case-study \
  --tag case-study
```
