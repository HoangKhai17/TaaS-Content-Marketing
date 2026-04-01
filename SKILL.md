---
name: taas-content-marketing
description: Viết và đăng bài blog B2B tự động lên website công ty công nghệ TaaS. Trigger khi người dùng nói "viết bài về [chủ đề]", "tạo case study", "viết insight về [topic]", "đăng bài tin công ty/công nghệ", hoặc cung cấp topic liên quan đến testing, QA, phần mềm, outsourcing. Pipeline đầy đủ: fetch internal links → research → viết → AEO/SEO optimize → format HTML → preview → publish WordPress. Audience chính: CTO, QA Manager, Engineering Lead, Product Manager tại các công ty phần mềm.
---

# TaaS Content Marketing Skill v1.0

Skill viết và đăng bài blog B2B tự động cho website công ty TaaS với đầy đủ tính năng:
- Research tự động từ web (xu hướng ngành, số liệu mới nhất, competitor insight)
- Internal linking tự động từ WordPress REST API
- AEO (Answer Engine Optimization) — viết để AI (ChatGPT, Perplexity) có thể trích dẫn
- SEO B2B tiếng Việt + tiếng Anh cho từ khóa kỹ thuật
- URL slug tối ưu, ngắn gọn
- Ảnh cover từ Nano Banana (Google Gemini) với prompt phù hợp ngành tech
- Ảnh trong bài từ Unsplash → Pexels → Pixabay (fallback tự động)
- Kiểm tra chất lượng E-E-A-T trước khi đăng

---

## INSIGHT THỊ TRƯỜNG 2026 — Tại sao skill này được thiết kế như vậy

> **3 thay đổi lớn nhất về hành vi người đọc B2B tech:**
>
> 1. **89% B2B buyer dùng AI để research** — không phải Google truyền thống. Nội dung phải viết để AI trích dẫn (AEO), không chỉ để rank keyword.
> 2. **Corporate voice mất uy tín** — IT professionals tin bài của Senior Engineer / CTO hơn marketing copy bóng bẩy. Mọi bài phải có góc nhìn expert thực sự.
> 3. **Proof over promise** — Buyer muốn số liệu, case study có kết quả đo được, không phải lời hứa chung chung.

---

## TAGS CÓ SẴN — CHỈ DÙNG CÁC TAG NÀY

```
Tin công ty   → slug: tin-cong-ty
Tin công nghệ → slug: tin-cong-nghe
Case study    → slug: case-study
Insight       → slug: insight
```

**Quy tắc gán tag:**
- Thông báo sản phẩm, milestone, partnership, team → `tin-cong-ty`
- Xu hướng ngành testing/QA, công nghệ mới, phân tích thị trường → `tin-cong-nghe`
- Câu chuyện khách hàng có số liệu cụ thể → `case-study`
- Quan điểm chuyên gia, thought leadership, góc nhìn sâu về TaaS/QA → `insight`

**TUYỆT ĐỐI không tạo tag mới** — WordPress sẽ tự tạo tag nếu truyền tên không khớp chính xác slug.

---

## LOẠI BÀI

```
tin-cong-ty   → Thông báo nội bộ: ra mắt dịch vụ, đối tác mới, sự kiện, giải thưởng
tin-cong-nghe → Phân tích trend: AI in testing, DevOps, agile QA, outsourcing market
case-study    → Câu chuyện khách hàng: vấn đề → giải pháp TaaS → kết quả đo được
insight       → Thought leadership: lý luận chuyên sâu, dự báo ngành, quan điểm CTO/QA Lead
```

---

## XỬ LÝ YÊU CẦU NGẮN GỌN — Tự động điền thông tin còn thiếu

Khi người dùng chỉ nói **"viết bài về [chủ đề]"** mà không cung cấp thêm gì, Claude PHẢI tự suy ra toàn bộ thông tin còn thiếu theo bảng dưới — **không hỏi lại, bắt đầu luôn**.

### Loại bài — mặc định theo từ khóa trong yêu cầu

| Từ khóa người dùng dùng | Loại bài tự chọn |
|---|---|
| "ra mắt", "thông báo", "partnership", "giải thưởng", "sự kiện", "tuyển dụng" | `tin-cong-ty` |
| "xu hướng", "trend", "thị trường", "phân tích", "so sánh", "AI", "DevOps" | `tin-cong-nghe` |
| "case study", "khách hàng", "dự án", "câu chuyện", "kết quả", "tiết kiệm" | `case-study` |
| "insight", "quan điểm", "tôi nghĩ", "tại sao", "tương lai", "chiến lược" | `insight` |
| Không có từ khóa nào → | `insight` (mặc định — phù hợp B2B nhất) |

### Slug — tự generate theo công thức

```
tin-cong-ty   : [ten-su-kien-khong-dau]          → ra-mat-dich-vu-automation-testing
tin-cong-nghe : [trend-chinh-khong-dau]           → ai-testing-xu-huong-2026
case-study    : [ten-kh-khong-dau]-case-study     → fintech-startup-case-study
insight       : [goc-nhin-chinh-khong-dau]        → tai-sao-taas-thay-the-qa-inhouse
```

### Status — mặc định là DRAFT

Luôn đăng **DRAFT** trừ khi người dùng nói rõ "publish luôn" hoặc "đăng luôn".

### Ví dụ thực tế

| Người dùng nói | Claude tự hiểu |
|---|---|
| "viết bài về xu hướng AI testing 2026" | tin-cong-nghe, slug: ai-testing-xu-huong-2026, draft |
| "case study khách hàng fintech tiết kiệm 40% QA cost" | case-study, slug: fintech-startup-case-study, draft |
| "insight tại sao outsource testing lại hiệu quả hơn" | insight, slug: tai-sao-outsource-testing-hieu-qua, draft |
| "thông báo ra mắt dịch vụ automation testing rồi đăng luôn" | tin-cong-ty, slug: ra-mat-automation-testing, published |

---

## BƯỚC 0 — Chuẩn bị trước khi viết

Trước khi viết bài, Claude PHẢI thực hiện 2 việc này:

### 0.1 Fetch danh sách bài viết đã đăng

```bash
python -c "
from utils.wp_client import fetch_published_posts, format_posts_for_linking
posts = fetch_published_posts()
print(format_posts_for_linking(posts))
"
```

Lưu kết quả lại — dùng để tạo internal links ở bước viết bài.

### 0.2 Xác định loại bài và thông tin cần thiết

Tự detect theo bảng **XỬ LÝ YÊU CẦU NGẮN GỌN** — không hỏi lại:
- **Loại bài:** tin-cong-ty / tin-cong-nghe / case-study / insight
- **Chủ đề:** lấy từ yêu cầu
- **Target audience:** CTO / QA Manager / Engineering Lead / Product Manager
- **Image queries:** 2-3 keyword tiếng Anh phù hợp ngành tech

---

## BƯỚC 1 — Research

Dùng `web_search` để tìm theo loại bài:

**Tin công nghệ / Insight:**
- Số liệu mới nhất về chủ đề (market size, growth rate, adoption rate)
- Báo cáo từ nguồn uy tín: Gartner, Forrester, Statista, Stack Overflow Survey
- Quan điểm từ engineering blog của big tech (Netflix, Shopify, Stripe, Atlassian)
- Thảo luận trên Hacker News, Reddit r/QualityAssurance, r/devops

**Case study:**
- Dữ liệu ngành: chi phí QA inhouse vs outsource trung bình
- Số liệu benchmark: bug detection rate, time-to-market improvement
- Nếu là case study thực của công ty → lấy thông tin từ người dùng cung cấp

**Tin công ty:**
- Thông tin từ người dùng cung cấp trực tiếp — không tự suy diễn
- Tìm thêm context ngành nếu cần làm rõ tầm quan trọng của sự kiện

**Quan trọng:** Không bịa số liệu. Ghi "(nguồn cần verify)" nếu không tìm được dẫn chứng cụ thể.

---

## BƯỚC 2 — Viết bài

### Tone & Voice — B2B Tech Expert

- **Expert, không phải marketer** — viết như một Senior QA Engineer / CTO đang chia sẻ kinh nghiệm thực chiến, không phải sales copy
- **Ngôi "bạn" + "chúng tôi"** — "bạn" cho reader, "chúng tôi" khi đề cập đến công ty
- **Proof trước, claim sau** — đưa số liệu / bằng chứng trước, kết luận sau
- **Mỗi H2 phải trả lời một câu hỏi cụ thể** mà CTO/QA Manager thực sự đặt ra
- **Đoạn mở đầu = hook bằng vấn đề** — không mở đầu bằng giới thiệu công ty

### Từ TUYỆT ĐỐI không dùng
"giải pháp toàn diện", "đẳng cấp", "tối ưu vượt trội", "hàng đầu Việt Nam",
"chuyên nghiệp", "uy tín", "cam kết chất lượng", "đội ngũ giàu kinh nghiệm",
"không thể bỏ qua", "revolutionize", "game-changing", "cutting-edge"

### Độ dài theo loại bài

| Loại bài | Độ dài | Lý do |
|---|---|---|
| Tin công ty | 400-600 chữ | Tin tức — ngắn gọn, đủ ý |
| Tin công nghệ | 1200-1800 chữ | Phân tích cần depth |
| Case study | 1000-1500 chữ | Có cấu trúc rõ + số liệu |
| Insight | 1500-2500 chữ | Thought leadership cần lập luận đầy đủ |

### Cấu trúc theo loại bài

#### Tin Công Ty
```
H1: [Tên sự kiện cụ thể] — [Ý nghĩa/tác động ngắn gọn]

Đoạn mở: Tóm tắt sự kiện + tại sao quan trọng (100 chữ)
H2: [Chi tiết sự kiện]
H2: Điều này có nghĩa gì với [khách hàng / thị trường]
H2: Quote từ leadership (nếu có)
H2: Bước tiếp theo / CTA
```

#### Tin Công Nghệ
```
H1: [Xu hướng/Vấn đề] — [Góc nhìn cụ thể, có số liệu nếu được]

Đoạn mở: Hook bằng số liệu hoặc vấn đề cấp bách (100-150 chữ)
H2: Bức tranh toàn cảnh — thị trường đang đi đến đâu (200-250 chữ)
H2: [Yếu tố 1 đang thay đổi] (200-250 chữ)
  H3: Bằng chứng / case cụ thể
H2: [Yếu tố 2 đang thay đổi] (200-250 chữ)
  H3: Bằng chứng / case cụ thể
H2: Ảnh hưởng đến [CTO / QA team / engineering org] (200 chữ)
H2: Đề xuất hành động cụ thể (150-200 chữ)
H2: Kết luận + góc nhìn của chúng tôi (100 chữ)
```

#### Case Study
```
H1: [Tên công ty / ngành] giảm [X%] chi phí QA nhờ [giải pháp cụ thể]
    (hoặc: Từ [vấn đề] đến [kết quả] — câu chuyện của [công ty])

H2: Thách thức ban đầu (200-250 chữ)
  → Mô tả vấn đề bằng số liệu cụ thể: bao nhiêu bug lọt production, tốc độ release thấp thế nào
H2: Tại sao chọn giải pháp TaaS (150-200 chữ)
  → Các lựa chọn đã cân nhắc, lý do quyết định
H2: Triển khai như thế nào (250-300 chữ)
  H3: Giai đoạn 1: [mô tả]
  H3: Giai đoạn 2: [mô tả]
H2: Kết quả đo được (200-250 chữ)
  → PHẢI có số liệu: %, thời gian, chi phí — không viết chung chung
H2: Bài học và khuyến nghị (150-200 chữ)
```

#### Insight / Thought Leadership
```
H1: [Luận điểm mạnh, có thể gây tranh cãi] — [Góc nhìn cụ thể]
    Ví dụ: "Tại sao QA inhouse không còn là lợi thế cạnh tranh trong thời đại AI"

Đoạn mở: Đặt vấn đề — tại sao đây là câu hỏi quan trọng NOW (150 chữ)
H2: Cách nhìn phổ biến và tại sao nó không còn đúng (200-250 chữ)
H2: [Luận điểm 1 — có bằng chứng] (250-300 chữ)
H2: [Luận điểm 2 — có bằng chứng] (250-300 chữ)
H2: [Luận điểm 3 — có bằng chứng] (250-300 chữ)
H2: Phản biện phổ biến và cách trả lời (200 chữ)
  → Thừa nhận giới hạn — tăng credibility
H2: Hàm ý thực tế cho [CTO / QA Lead] (150-200 chữ)
H2: Kết luận — quan điểm của tác giả (100-150 chữ)
```

---

## BƯỚC 3 — AEO + SEO Optimization

### AEO (Answer Engine Optimization) — Ưu tiên hàng đầu 2026

Mục tiêu: Nội dung được ChatGPT, Perplexity, Google AI trích dẫn khi ai đó hỏi về TaaS/outsource testing.

**Checklist AEO:**
- [ ] Có ít nhất 1 đoạn trả lời trực tiếp câu hỏi dạng "X là gì?" hoặc "Tại sao X?" (40-60 chữ)
- [ ] Có ít nhất 1 danh sách dạng `<ul>` hoặc `<ol>` với 3-7 điểm rõ ràng
- [ ] Có số liệu với nguồn trích dẫn cụ thể
- [ ] H2/H3 viết dưới dạng câu hỏi hoặc câu khẳng định rõ ràng — không viết tối nghĩa
- [ ] Đoạn mở 150 chữ đầu phải tóm tắt được toàn bộ bài

### SEO B2B Tech — từ khóa người thực sự tìm

**Tiếng Việt:**
- "outsource testing là gì" / "TaaS là gì" — informational intent
- "thuê đội QA bên ngoài có đáng không" — decision intent
- "chi phí kiểm thử phần mềm" — comparison intent
- "automation testing vs manual testing" — educational intent
- "kiểm thử phần mềm outsource Việt Nam" — local intent

**Tiếng Anh (nếu target market ngoài VN):**
- "software testing outsourcing cost"
- "TaaS vs inhouse QA team"
- "QA automation for startups"

### URL Slug — QUAN TRỌNG

Claude PHẢI tạo slug thủ công. **Không để WordPress tự generate từ title.**

**Quy tắc:**
- Tối đa 5 từ, lý tưởng 3-4 từ
- Chỉ dùng a-z, 0-9, dấu gạch ngang `-`
- Không dấu tiếng Việt
- Không stop words: `la`, `gi`, `va`, `cho`, `cua`, `tai`, `co`, `den`, `mot`

**Công thức slug:**

```
tin-cong-ty   : [ten-su-kien]                → ra-mat-automation-testing
tin-cong-nghe : [trend-keyword]              → ai-testing-2026
case-study    : [nganh-hoac-kh]-case-study  → fintech-qa-case-study
insight       : [luan-diem-chinh]            → tai-sao-outsource-testing
```

**Ví dụ tốt:**
```
taas-la-gi                   ✅
outsource-testing-chi-phi    ✅
ai-qa-automation-2026        ✅
```

**Ví dụ xấu:**
```
tai-sao-ban-nen-chon-giai-phap-kiem-thu-phan-mem-cua-chung-toi   ❌ quá dài
bai-viet-ve-xu-huong-testing-trong-nam-2026                       ❌ quá dài
```

### Internal linking

- Chèn 2-3 internal links liên quan từ danh sách bài đã đăng (Bước 0)
- Case study → link sang insight liên quan và ngược lại
- Tin công nghệ → link sang case study minh họa
- Format: `<a href="[URL đầy đủ]">[anchor text mô tả — không dùng "click here"]</a>`

---

## BƯỚC 4 — Format HTML

```html
<h2>Câu hỏi hoặc luận điểm rõ ràng</h2>
<p>Nội dung đoạn văn. Mỗi đoạn tối đa 80 chữ — dễ đọc trên mobile.</p>

<h3>Sub-section cụ thể</h3>
<p>Nội dung...</p>

<!-- Danh sách có cấu trúc — tốt cho AEO -->
<ul>
  <li><strong>Điểm chính:</strong> Giải thích ngắn gọn, có thể đo được</li>
  <li><strong>Điểm chính:</strong> Giải thích ngắn gọn, có thể đo được</li>
</ul>

<!-- Key takeaway hoặc expert quote -->
<blockquote>
  Insight quan trọng hoặc số liệu nổi bật mà reader không nên bỏ qua
</blockquote>

<!-- Số liệu có nguồn -->
<p>Theo báo cáo của Gartner 2025, <strong>67% engineering team</strong>
dự kiến tăng ngân sách cho automated testing trong 2026.
<em>(Nguồn: Gartner Magic Quadrant for Software Testing Tools 2025)</em></p>

<!-- Vị trí chèn ảnh — image_generator.py sẽ tự chèn -->
```

**Quy tắc format:**
- `<strong>` cho số liệu, tên công nghệ, kết quả đo được
- `<ul>/<ol>` cho danh sách — KHÔNG viết gạch đầu dòng trong `<p>`
- `<blockquote>` cho insight quan trọng hoặc quote từ expert/khách hàng
- `<em>` cho ghi chú nguồn dữ liệu
- KHÔNG dùng inline CSS
- KHÔNG dùng `<h1>` trong body — chỉ dùng H2 và H3

---

## BƯỚC 5 — Kiểm tra E-E-A-T trước khi Preview

Trước khi hiển thị preview, tự chạy checklist này:

```
✅ Experience  : Bài có ví dụ thực tế / case cụ thể không? (không chỉ lý thuyết)
✅ Expertise   : Bài thể hiện hiểu biết sâu về QA/testing/TaaS không?
✅ Authority   : Có số liệu từ nguồn uy tín (Gartner, Forrester, Stack Overflow) không?
✅ Trust       : Bài thừa nhận giới hạn / không oversell không?
✅ AEO         : Có đoạn trả lời thẳng câu hỏi search intent không?
✅ Hook        : 150 chữ đầu có đủ hấp dẫn để reader tiếp tục không?
```

Nếu bất kỳ mục nào ✗ → sửa trước khi hiển thị preview.

## BƯỚC 5 (tiếp) — Preview và xác nhận

```
📋 PREVIEW BÀI VIẾT
═══════════════════════════════════════════
Tiêu đề     : [title]
URL Slug    : [slug]            ← tối đa 5 từ
Loại bài    : [tag]
Số chữ      : [count]
H2 headings : [count]
Internal    : [count] links
Số liệu     : [count] điểm có nguồn trích dẫn
Excerpt     : [text 120-155 ký tự — phải có từ khóa chính]

🎨 ẢNH
Cover       : Nano Banana — [prompt tiếng Anh ngắn, phong cách tech/professional]
Inline      : [count] ảnh
Queries     : [keywords tiếng Anh]

✅ E-E-A-T   : [Pass / cần chỉnh — liệt kê vấn đề nếu có]
═══════════════════════════════════════════
```

Hỏi người dùng: **"Bài đã sẵn sàng. Bạn muốn publish không?"**

---

## BƯỚC 6 — Publish

```bash
# Insight
python main.py \
  --file ten_file.html \
  --title "Tại sao QA Inhouse Không Còn Là Lợi Thế Cạnh Tranh Trong Thời Đại AI" \
  --slug "tai-sao-outsource-testing" \
  --type insight \
  --tag "insight" \
  --excerpt "Mô tả ngắn 120-155 ký tự, có từ khóa chính" \
  --image-queries "software testing team" "QA automation dashboard"

# Case study
python main.py \
  --file ten_file.html \
  --title "Fintech Startup Giảm 40% Chi Phí QA Nhờ TaaS" \
  --slug "fintech-qa-case-study" \
  --type case-study \
  --tag "case-study" \
  --excerpt "Mô tả ngắn" \
  --image-queries "fintech software testing" "QA cost reduction"

# Tin công nghệ
python main.py \
  --file ten_file.html \
  --title "AI Testing 2026: 5 Xu Hướng Sẽ Thay Đổi Cách Bạn Làm QA" \
  --slug "ai-testing-2026" \
  --type tin-cong-nghe \
  --tag "tin-cong-nghe" \
  --excerpt "Mô tả ngắn" \
  --image-queries "AI software testing automation" "machine learning QA"
```

**Lưu ý:**
- Luôn truyền `--tag` với slug chính xác từ danh sách có sẵn
- Luôn truyền `--slug` thủ công — không để auto-generate
- Mặc định đăng **DRAFT** — vào WordPress Admin xem lại trước khi publish
- Thêm `--publish` để publish luôn

---

## Cấu trúc file

```
taas-content-marketing/
├── SKILL.md                      ← File này (router + pipeline tổng quát)
├── main.py                       ← Entry point
├── requirements.txt
├── env.example
│
├── tin-cong-ty/
│   └── instructions.md           ← Chi tiết: thông báo sản phẩm, milestone, partnership
├── tin-cong-nghe/
│   └── instructions.md           ← Chi tiết: phân tích trend testing/QA, tin tức ngành
├── case-study/
│   └── instructions.md           ← Chi tiết: template khách hàng với số liệu đo được
└── insight/
    └── instructions.md           ← Chi tiết: thought leadership, lập luận chuyên sâu
│
└── utils/
    ├── wp_client.py              ← WordPress REST API client
    ├── image_generator.py        ← Tái dùng
    └── seo_validator.py          ← Mới: kiểm tra AEO + từ khóa TaaS B2B
```

---

## Setup lần đầu

```bash
# 1. Cài dependencies
pip install -r requirements.txt

# 2. Tạo .env từ template
cp env.example .env

# 3. Điền vào .env:
# WP_URL=https://your-company.com
# WP_USERNAME=your_wp_username
# WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
# UNSPLASH_ACCESS_KEY=your_unsplash_key
# PEXELS_API_KEY=your_pexels_key
# PIXABAY_API_KEY=your_pixabay_key
```

---

## Lưu ý quan trọng

- **Không bao giờ bịa số liệu** — ghi "(nguồn cần verify)" nếu không tìm được dẫn chứng
- **Tags** chỉ dùng 4 tag có sẵn — tuyệt đối không tự tạo tag mới
- **URL slug** phải tạo thủ công — không để auto-generate
- **Ảnh** dùng query tiếng Anh, tránh ảnh generic — ưu tiên ảnh mang tính kỹ thuật, professional
- **Mọi claim marketing** phải có bằng chứng kèm theo — buyer B2B tech không tin lời hứa suông
- **E-E-A-T** là tiêu chuẩn tối thiểu — không đăng bài nếu thiếu bất kỳ yếu tố nào