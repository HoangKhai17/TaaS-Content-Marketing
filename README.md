# taas-content-marketing

Skill sản xuất nội dung tự động cho website dịch vụ TaaS (Testing as a Service), tích hợp WordPress.

---

## Cấu trúc thư mục

```
taas-content-marketing/
├── SKILL.md                    ← Router chính: detect loại bài, pipeline tổng quát
├── main.py                     ← Entry point
├── requirements.txt
├── env.example
│
├── tin-cong-ty/
│   └── instructions.md                ← Cấu trúc bài: thông báo sản phẩm, milestone, partnership
├── tin-cong-nghe/
│   └── instructions.md                ← Bài phân tích xu hướng testing/QA, tin tức ngành
├── case-study/
│   └── instructions.md                ← Template khách hàng: vấn đề → giải pháp → kết quả
└── insight/
    └── instructions.md                ← Thought leadership: góc nhìn chuyên gia về TaaS/QA
│
└── utils/
    ├── wp_client.py            ← WordPress REST API client
    ├── image_generator.py      ← Tìm ảnh từ Unsplash / Pexels / Pixabay
    └── seo_validator.py        ← Kiểm tra từ khóa TaaS B2B
```

---

## 4 danh mục nội dung

| Thư mục | Tag WordPress | Mô tả |
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
WP_URL=https://your-site.com
WP_USERNAME=your_wp_username
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
UNSPLASH_ACCESS_KEY=your_unsplash_key
```

**Cách lấy Application Password:**
1. Vào **WordPress Admin → Users → Profile**
2. Kéo xuống mục **"Application Passwords"**
3. Nhập tên app: `TaaS Content Skill` → click **"Add New Application Password"**
4. Copy password hiển thị (chỉ hiện 1 lần)

> ⚠️ Website phải bật **HTTPS** để Application Passwords hoạt động.

---

## Sử dụng

```bash
python main.py \
  --file bai_viet.html \
  --title "Fintech Startup Giảm 40% Chi Phí QA Nhờ TaaS" \
  --slug "fintech-qa-case-study" \
  --type case-study \
  --tag case-study \
  --excerpt "Mô tả ngắn 120-155 ký tự" \
  --image-queries "software testing team" "QA automation dashboard"
```

Thêm `--publish` để publish ngay thay vì lưu draft.
