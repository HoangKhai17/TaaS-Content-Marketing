---
name: taas-tin-cong-nghe
description: Viết bài tin công nghệ và phân tích xu hướng ngành cho website công ty TaaS. Dùng khi người dùng muốn viết bài về xu hướng testing/QA, công nghệ mới trong ngành phần mềm, phân tích thị trường, hoặc tin tức ngành có góc nhìn chuyên môn. Trigger khi người dùng nói "viết bài về xu hướng [X]", "phân tích [công nghệ/thị trường]", "tin tức ngành testing", "AI trong QA", "DevOps và testing", "[tool/framework] mới". Khác với insight — bài tin công nghệ bám sát sự kiện/dữ liệu thực tế, không đặt nặng luận điểm cá nhân. Claude tự detect góc khai thác và audience từ yêu cầu — không hỏi lại nếu đã có chủ đề rõ.
---

# Skill: Viết Bài Tin Công Nghệ — TaaS

## Mục tiêu

Tạo bài phân tích công nghệ đủ sâu để CTO, QA Lead, Engineering Manager tin đây là nguồn đáng đọc — không phải bản dịch lại press release hay tổng hợp nông từ vài bài blog.

Bài đọc xong phải đạt được:
- Reader hiểu **tại sao** xu hướng/công nghệ này quan trọng, không chỉ **là gì**
- Reader biết xu hướng này **ảnh hưởng thế nào đến công việc của họ cụ thể**
- Reader có ít nhất **1 action cụ thể** có thể làm ngay

> **Khác biệt với Insight:** Tin công nghệ bám sát dữ liệu và sự kiện thực tế, không đặt nặng quan điểm cá nhân. Insight thì ngược lại — luận điểm cá nhân là trọng tâm. Nếu người dùng yêu cầu bài thiên về quan điểm → chuyển sang `insight/SKILL.md`.

---

## Auto-detect trước khi viết

Claude PHẢI tự phân tích yêu cầu và xác định ngay, **không hỏi lại nếu đã có chủ đề rõ**:

| Cần xác định | Cách detect | Nếu thiếu |
|---|---|---|
| **Chủ đề / công nghệ** | Lấy từ yêu cầu | Hỏi lại — bắt buộc |
| **Góc khai thác** | Detect theo bảng dưới | Mặc định: `phan-tich-xu-huong` |
| **Độ kỹ thuật** | Detect từ context người dùng | Mặc định: mid-level (CTO hiểu được, dev không thấy thừa) |
| **Timeframe** | Detect từ yêu cầu ("2026", "hiện tại", "tương lai") | Mặc định: hiện tại + 12 tháng tới |

### 4 góc khai thác — detect từ yêu cầu

| Từ khóa người dùng dùng | Góc khai thác | Đặc điểm bài |
|---|---|---|
| "xu hướng", "trend", "thị trường đang đi đâu" | `phan-tich-xu-huong` | Data-driven, nhiều số liệu thị trường, dự báo |
| "công cụ mới", "framework", "tool nào tốt", "so sánh" | `danh-gia-cong-cu` | Hands-on, tiêu chí rõ ràng, kết luận không mơ hồ |
| "tại sao [công ty lớn] làm X", "Netflix/Shopify/Google làm gì" | `giai-phau-case` | Phân tích case thực từ engineering blog, rút ra bài học |
| "giải thích [khái niệm kỹ thuật]", "X là gì", "hoạt động như thế nào" | `explainer` | Từ basic đến nâng cao, có ví dụ thực tế, không chỉ định nghĩa |

---

## Bước 1 — Research bắt buộc TRƯỚC khi viết

Khác với case study (dùng data người dùng cung cấp) hay insight (dùng kiến thức nội bộ), **tin công nghệ PHẢI research web trước**. Không viết từ kiến thức có sẵn — thông tin ngành thay đổi liên tục.

### Nguồn ưu tiên theo chủ đề

**Số liệu thị trường & xu hướng:**
- State of Testing Report (Tricentis, SmartBear) — khảo sát ngành hàng năm
- Stack Overflow Developer Survey — developer sentiment thực tế
- Gartner Magic Quadrant / Hype Cycle — enterprise adoption
- DORA Report (Google) — DevOps & delivery performance

**Tin tức công nghệ kỹ thuật:**
- Engineering blog của Shopify, Stripe, Atlassian, Netflix, GitHub
- ThoughtWorks Technology Radar — emerging tech đáng chú ý
- Hacker News (news.ycombinator.com) — community reaction thực tế
- The New Stack, InfoQ — enterprise tech news có chiều sâu

**AI trong testing cụ thể:**
- Applitools, Mabl, Testim blog — vendor nhưng có data thực
- Ministry of Testing community — practitioner perspective
- r/QualityAssurance, r/devops — vấn đề thực tế từ người làm

> **Quan trọng:** Tìm ít nhất **3 nguồn độc lập** trước khi viết. Nếu chỉ có 1 nguồn → ghi rõ "theo [nguồn]" thay vì viết như sự thật hiển nhiên.

---

## Cấu trúc bài viết

### Tiêu đề

Format tốt nhất cho tin công nghệ B2B:

| Dạng | Ví dụ |
|---|---|
| Con số + hàm ý | "67% Engineering Team Tăng Ngân Sách Test Automation Năm 2026 — Nhưng ROI Vẫn Là Dấu Hỏi" |
| Đặt tên cho trend | "Shift-Left Testing Đã Trở Thành Mainstream — Bước Tiếp Theo Là Gì?" |
| Câu hỏi thực tế | "AI Testing Tools: Hype Hay Thực Sự Tiết Kiệm Được Thời Gian?" |
| Cập nhật có góc nhìn | "Playwright Vượt Cypress Trong Developer Survey 2025 — 3 Lý Do Đằng Sau Con Số" |

Tránh:
- "Xu Hướng Công Nghệ Năm 2026" ❌ — quá chung, không có góc nhìn
- "Giới Thiệu [Tool X]" ❌ — nghe như press release

---

### 1. Context — Tại sao đây là tin đáng đọc ngay bây giờ (100-150 chữ)

Không mở đầu bằng định nghĩa. Mở bằng **lý do urgency**:

- Số liệu mới nhất vừa được công bố
- Một sự kiện / thay đổi vừa xảy ra trong ngành
- Một vấn đề đang ảnh hưởng đến nhiều team hiện tại

Ví dụ:
> "Stack Overflow Developer Survey 2025 vừa công bố: lần đầu tiên trong 5 năm, tỷ lệ developer hài lòng với quy trình QA của team mình giảm xuống dưới 40% — dù đầu tư vào testing tool tăng gấp đôi. Bài viết này phân tích tại sao, và 3 pattern mà các team đang làm sai."

---

### 2. Bức tranh toàn cảnh — thị trường đang ở đâu (200-250 chữ)

Đặt chủ đề vào context rộng hơn để reader thấy tầm quan trọng:

- Quy mô thị trường / tốc độ tăng trưởng (có số liệu)
- Ai đang adopt: startup hay enterprise, ngành nào dẫn đầu
- Điểm inflection: tại sao năm nay khác với 2-3 năm trước
- Vietnam context nếu có: thị trường local đang ở đâu so với global

> **Quy tắc:** Mỗi con số phải có nguồn rõ ràng — ghi inline *(Nguồn: Gartner, Q4 2025)* thay vì để footnote.

---

### 3. Phần chính — theo góc khai thác đã detect

#### Nếu là `phan-tich-xu-huong`

```
H2: [Tín hiệu 1 — bằng chứng xu hướng đang thật] (200-250 chữ)
  H3: Dữ liệu thị trường
  H3: Ví dụ công ty đang làm

H2: [Tín hiệu 2 — cơ chế tại sao xu hướng này tăng tốc] (200-250 chữ)
  H3: Yếu tố công nghệ
  H3: Yếu tố kinh tế / áp lực thị trường

H2: [Tín hiệu 3 — early adopter đang nhận được gì] (150-200 chữ)
  → Kết quả đo được từ những team đi sớm

H2: Những gì chưa chắc chắn — rủi ro và câu hỏi mở (150 chữ)
  → Điều kiện để xu hướng fail hoặc chậm lại
```

#### Nếu là `danh-gia-cong-cu`

```
H2: Bối cảnh — tại sao cần tool này, problem nó giải quyết (150 chữ)

H2: Tiêu chí đánh giá — tại sao dùng các tiêu chí này (100 chữ)
  → Phù hợp với hoàn cảnh nào: startup / scale-up / enterprise

H2: [Tool/Approach A] (200 chữ)
  H3: Làm tốt điều gì, trong hoàn cảnh nào
  H3: Giới hạn thực tế (không phải limitation từ doc)
  H3: Phù hợp với team như thế nào

H2: [Tool/Approach B] (200 chữ)
  H3: Làm tốt điều gì, trong hoàn cảnh nào
  H3: Giới hạn thực tế
  H3: Phù hợp với team như thế nào

H2: Khuyến nghị — chọn gì trong hoàn cảnh nào (150 chữ)
  → Decision matrix cụ thể, không trả lời "tùy"
```

#### Nếu là `giai-phau-case`

```
H2: Bối cảnh — [Công ty] đang giải quyết vấn đề gì (150 chữ)
  → Scale, đặc thù kỹ thuật, constraint của họ

H2: Giải pháp họ chọn và lý do (200-250 chữ)
  → Các option đã cân nhắc + lý do loại
  → Architecture / approach cụ thể

H2: Kết quả và trade-off (200 chữ)
  → Số liệu họ công bố
  → Những gì không hoàn hảo — trade-off thực tế

H2: Bài học có thể áp dụng (200 chữ)
  → Điều gì scale được sang team khác
  → Điều gì chỉ đúng với hoàn cảnh riêng của họ
  → Bắt đầu từ đâu nếu muốn thử
```

#### Nếu là `explainer`

```
H2: [Khái niệm] thực sự là gì — không phải định nghĩa sách giáo khoa (150 chữ)
  → Giải thích bằng vấn đề nó giải quyết, không phải bằng thuật ngữ

H2: Hoạt động như thế nào — từng bước (250-300 chữ)
  H3: Bước 1 / Layer 1
  H3: Bước 2 / Layer 2
  → Dùng analogy nếu cần, nhưng analogy phải chính xác kỹ thuật

H2: Khi nào nên dùng / không nên dùng (150-200 chữ)
  → Use case thực tế trong ngành testing/QA
  → Anti-pattern phổ biến

H2: Bắt đầu từ đâu nếu muốn thử (150 chữ)
  → Resource cụ thể: doc, repo, tutorial đáng tin
  → Bước nhỏ nhất có thể làm trong 1 sprint
```

---

### 4. Ảnh hưởng với QA / Engineering team Việt Nam (150-200 chữ)

Đây là phần tạo differentiation — hầu hết bài tiếng Anh không có góc nhìn này:

- Xu hướng global này đang ở giai đoạn nào tại thị trường Việt Nam / Southeast Asia?
- Đặc thù nào của team Việt Nam ảnh hưởng đến cách adopt (budget, talent pool, client requirement)?
- Timeline thực tế: khi nào nên bắt đầu để không quá sớm, không quá muộn?

> **Nếu không có data Việt Nam cụ thể** → dùng SEA context hoặc so sánh với thị trường tương đương. Không bịa số liệu — ghi "chưa có khảo sát riêng cho thị trường Việt Nam" nếu cần.

---

### 5. Khuyến nghị thực tế — làm gì với thông tin này (150-200 chữ)

Phân loại theo tình huống của reader — không viết một lời khuyên chung cho tất cả:

```
Nếu team bạn đang ở giai đoạn [X]:
→ Ưu tiên làm [action cụ thể] trong [timeframe]
→ Chỉ số để biết đang đi đúng hướng: [metric]

Nếu team bạn đã làm [Y] rồi:
→ Bước tiếp theo là [action]
→ Tránh bẫy phổ biến: [warning cụ thể]
```

---

### 6. Tóm tắt và nguồn tham khảo (100 chữ + link)

```
📌 3 điểm chính cần nhớ:
• [Điểm 1 — ngắn gọn, có thể tweet được]
• [Điểm 2]
• [Điểm 3]

📚 Nguồn tham khảo:
• [Tên báo cáo] — [Link hoặc mô tả nơi tìm]
• [Engineering blog] — [Link bài cụ thể]
• [Survey / Report] — [Link]
```

---

## Quy tắc viết

**PHẢI:**
- Research web **trước khi viết** — không viết từ kiến thức có sẵn với chủ đề thay đổi nhanh
- Có **ít nhất 4 số liệu từ nguồn cụ thể** — ghi nguồn inline, không để footnote
- Có **phần khuyến nghị theo tình huống** — không một lời khuyên chung cho tất cả
- Có **phần ảnh hưởng với thị trường Việt Nam / SEA** — đây là differentiation
- Phân biệt rõ **fact vs opinion** — dùng "theo [nguồn]" cho fact, "chúng tôi cho rằng" cho opinion
- Độ dài: **1200-1800 chữ**

**TRÁNH:**
- Copy-paste thông tin từ press release hoặc vendor blog mà không có góc nhìn phản biện
- Liệt kê tool/trend mà không nói tại sao quan trọng với reader
- Kết luận mơ hồ kiểu "hãy chờ xem xu hướng này phát triển thế nào"
- Số liệu không có nguồn hoặc nguồn không rõ năm xuất bản
- Từ bị cấm: "cách mạng hóa", "thay đổi cuộc chơi", "đột phá", "tiên tiến nhất", "leading-edge"

---

## Checklist chất lượng trước khi xuất bài

```
✅ Research    : Đã tìm ít nhất 3 nguồn độc lập chưa?
✅ Số liệu     : Mỗi con số có nguồn và năm xuất bản không?
✅ Depth       : Bài có nói được "tại sao" quan trọng, không chỉ "là gì" không?
✅ Local angle : Có phần ảnh hưởng với team Việt Nam / SEA không?
✅ Action      : Reader biết làm gì cụ thể sau khi đọc xong không?
✅ Neutral     : Bài có đang vô tình quảng cáo cho vendor nào không?
```

Nếu bất kỳ mục nào ✗ → bổ sung trước khi xuất bài.

---

## Format output cuối

Xuất bài dưới dạng HTML với:
- `<h2>` cho các section chính — viết dạng câu có thông tin, không chỉ là label
- `<h3>` cho sub-section trong phần phân tích chính
- `<strong>` cho số liệu, tên tool/framework, kết quả đo được
- `<ul>/<ol>` cho danh sách — dùng `<ol>` khi có thứ tự ưu tiên
- `<blockquote>` cho quote từ báo cáo hoặc engineering blog
- `<em>` cho ghi chú nguồn trích dẫn inline
- `<table>` cho bảng so sánh tool (nếu là `danh-gia-cong-cu`)
- Internal link sang 1-2 case study liên quan — dẫn chứng thực tế
- Ghi rõ số chữ ước tính và danh sách nguồn tham khảo ở cuối

## Tags Ghost
`tin-cong-nghe`
