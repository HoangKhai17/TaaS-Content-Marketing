---
name: taas-tin-cong-ty
description: Viết bài tin tức nội bộ công ty cho website TaaS. Dùng khi người dùng muốn thông báo sự kiện, cột mốc, partnership, ra mắt dịch vụ, giải thưởng, tuyển dụng, hoặc hoạt động team. Trigger khi người dùng nói "viết thông báo [X]", "ra mắt dịch vụ mới", "ký hợp tác với [đối tác]", "đạt [cột mốc]", "tuyển dụng", "sự kiện [tên]", "thông báo nội bộ ra ngoài". Khác với insight hay tin công nghệ — bài tin công ty bám sát thông tin người dùng cung cấp, không tự suy diễn hay thêm thắt. Claude hỏi lại nếu thiếu thông tin cốt lõi — không viết bằng thông tin giả định.
---

# Skill: Viết Bài Tin Công Ty — TaaS

## Mục tiêu

Tạo bài thông báo công ty vừa đủ thông tin, vừa có góc nhìn làm rõ **ý nghĩa với người đọc bên ngoài** — không phải bản tóm tắt nội bộ, không phải press release cứng nhắc.

Người đọc là khách hàng tiềm năng, đối tác, ứng viên, hoặc cộng đồng tech — họ không quan tâm đến thành tích của công ty, họ quan tâm đến **điều này có nghĩa gì với họ**.

Bài đọc xong phải trả lời được: *"Tin này liên quan đến tôi như thế nào?"*

---

## Nguyên tắc cốt lõi — KHÁC với 3 loại bài còn lại

> **Tin công ty không được tự suy diễn.** Đây là loại bài duy nhất trong hệ thống mà thông tin từ người dùng là nguồn duy nhất — Claude không được bổ sung thông tin từ web, không tự thêm chi tiết, không phỏng đoán số liệu chưa được xác nhận.

| Loại bài khác | Tin công ty |
|---|---|
| Research web để bổ sung data | Chỉ dùng thông tin người dùng cung cấp |
| Thêm góc nhìn bên ngoài | Góc nhìn duy nhất: từ công ty |
| Có thể viết khi thiếu data | Dừng và hỏi nếu thiếu thông tin cốt lõi |
| Độ dài 1000-2500 chữ | Ngắn gọn: 800-1000 chữ |

---

## Auto-detect và xử lý thiếu thông tin

### Detect loại tin từ yêu cầu

| Từ khóa người dùng dùng | Loại tin | Template dùng |
|---|---|---|
| "ra mắt", "launch", "giới thiệu dịch vụ" | `ra-mat` | Section 3A |
| "ký hợp tác", "partnership", "đối tác mới" | `hop-tac` | Section 3B |
| "đạt X khách hàng", "X năm thành lập", "cột mốc" | `cot-moc` | Section 3C |
| "giải thưởng", "được công nhận", "top X" | `giai-thuong` | Section 3D |
| "tuyển dụng", "mở rộng team", "đang tìm" | `tuyen-dung` | Section 3E |
| "sự kiện", "hội thảo", "tham gia", "tổ chức" | `su-kien` | Section 3F |

### Thông tin bắt buộc — hỏi lại nếu thiếu

Trước khi viết, Claude PHẢI có đủ các thông tin sau. **Nếu thiếu bất kỳ mục nào → hỏi trực tiếp, không tự điền:**

| Thông tin | Tại sao cần |
|---|---|
| **Sự kiện / tin tức cụ thể là gì?** | Nội dung chính của bài |
| **Ngày/thời điểm xảy ra hoặc có hiệu lực** | Tính chính xác, tránh gây nhầm lẫn |
| **Ý nghĩa với khách hàng / thị trường** | Không có → bài chỉ là thông báo nội bộ |
| **Quote từ leadership** *(nếu có)* | Tăng credibility, thêm human element |
| **Bước tiếp theo / CTA** | Người đọc biết phải làm gì sau khi đọc |

> Nếu người dùng chưa cung cấp quote → hỏi: *"Bạn có câu quote từ CEO/CTO/người phụ trách muốn đưa vào không? Quote giúp bài bớt corporate và thêm human hơn nhiều."*

---

## Cấu trúc bài viết

### Tiêu đề

Format tốt nhất cho tin công ty B2B:

| Dạng | Ví dụ |
|---|---|
| Sự kiện + ý nghĩa | "TaaS Việt Nam Ra Mắt Dịch Vụ AI-Assisted Testing — Rút Ngắn Thời Gian Regression 60%" |
| Cột mốc + con số | "100 Khách Hàng Doanh Nghiệp Trong 2 Năm — Và Những Gì Chúng Tôi Học Được" |
| Partnership + benefit | "Hợp Tác Với [Đối Tác] Để Mở Rộng Năng Lực Testing Tự Động Cho Thị Trường SEA" |
| Giải thưởng + context | "Top 10 QA Outsourcing Provider Đông Nam Á 2025 — Điều Này Có Nghĩa Gì Với Bạn" |

Tránh:
- "[Tên công ty] Tự Hào Thông Báo..." ❌ — corporate cliché
- "Tin Vui: Chúng Tôi Vừa..." ❌ — không có thông tin trong tiêu đề
- Tiêu đề chỉ là tên sự kiện, không có ý nghĩa ❌

---

### 1. Lead — 80-100 chữ đầu

**Trả lời 3 câu hỏi trong đoạn đầu tiên:** Cái gì? Khi nào? Tại sao quan trọng với người đọc?

Không mở đầu bằng:
- Tên công ty + "tự hào thông báo" ❌
- Lịch sử công ty ❌
- Định nghĩa về ngành ❌

Mở đầu bằng:
- Sự kiện + ý nghĩa trực tiếp với reader
- Con số cụ thể nếu có
- Vấn đề mà tin này giải quyết

Ví dụ tốt:
> "Từ tháng 4/2026, khách hàng TaaS sẽ có thêm lựa chọn AI-Assisted Testing trong gói dịch vụ — giảm thời gian chạy regression suite từ 8 tiếng xuống còn dưới 3 tiếng mà không cần thay đổi test case hiện có."

---

### 2. Chi tiết sự kiện — theo loại tin (phần chính, 200-300 chữ)

#### 3A — Ra mắt dịch vụ / sản phẩm
```
H2: [Tên dịch vụ] là gì và hoạt động như thế nào
  → Mô tả cụ thể: làm được gì, không làm được gì
  → Khác biệt so với cách làm cũ / giải pháp hiện tại

H2: Phù hợp với team như thế nào
  → Use case cụ thể: ai nên dùng, giai đoạn nào của dự án
  → Điều kiện để dùng được (tech stack, quy mô, v.v.)

H2: Bắt đầu như thế nào
  → Các bước cụ thể: đăng ký / liên hệ / thử nghiệm
  → Timeline: onboarding mất bao lâu
```

#### 3B — Partnership / hợp tác
```
H2: [Đối tác] là ai và tại sao partnership này có ý nghĩa
  → Giới thiệu đối tác ngắn gọn (1-2 câu, không copy từ website họ)
  → Điểm tương đồng về mission / thị trường / khách hàng

H2: Partnership này mang lại gì cho khách hàng
  → Benefit cụ thể: dịch vụ mới, vùng phủ mới, năng lực mới
  → Timeline: khi nào có hiệu lực

H2: Bước tiếp theo
  → Khách hàng hiện tại cần làm gì
  → Khách hàng mới liên hệ như thế nào
```

#### 3C — Cột mốc tăng trưởng
```
H2: Con số và ý nghĩa đằng sau
  → Không chỉ nêu con số — giải thích tại sao con số này có ý nghĩa
  → So sánh timeline: đạt được trong bao lâu

H2: Điều chúng tôi học được trên hành trình này
  → 2-3 bài học thực tế — honest, không phải PR speak
  → Điều làm đúng + điều làm lại sẽ khác

H2: Hướng tiếp theo
  → Mục tiêu cụ thể tiếp theo là gì
  → Điều này có nghĩa gì với khách hàng
```

#### 3D — Giải thưởng / công nhận
```
H2: Giải thưởng này là gì và tiêu chí xét chọn
  → Tổ chức nào trao, tiêu chí cụ thể
  → Không chỉ nói "uy tín" — explain tại sao tiêu chí này có giá trị

H2: Điều này phản ánh điều gì trong cách chúng tôi làm việc
  → Kết nối giải thưởng với quy trình / giá trị cụ thể
  → Ví dụ thực tế từ dự án hoặc khách hàng

H2: Ý nghĩa với khách hàng và đối tác
  → Tại sao điều này quan trọng với người đang cân nhắc hợp tác
```

#### 3E — Tuyển dụng / mở rộng team
```
H2: Chúng tôi đang tìm ai và tại sao ngay bây giờ
  → Vị trí cụ thể, lý do mở rộng (growth, new service, market)
  → Không phải JD đầy đủ — chỉ capture được người phù hợp

H2: Làm việc ở đây như thế nào
  → 2-3 điều thực sự khác biệt, không phải "môi trường năng động"
  → Ví dụ cụ thể từ cách team làm việc hàng ngày

H2: Cách ứng tuyển
  → Link, email, hoặc quy trình cụ thể
  → Timeline phản hồi
```

#### 3F — Sự kiện / hội thảo
```
H2: Sự kiện này là gì và ai nên tham dự
  → Format: online/offline, thời lượng, số lượng
  → Ai sẽ benefit nhất từ việc tham dự

H2: Nội dung chính
  → Agenda hoặc topic chính — đủ cụ thể để người đọc quyết định có nên tham dự
  → Speaker / người trình bày nếu có

H2: Đăng ký và thông tin thực tế
  → Link đăng ký, deadline, chi phí (nếu có)
  → Địa điểm / link online
```

---

### 3. Quote từ leadership *(nếu có)*

Format chuẩn:

```html
<blockquote>
  "[Quote cụ thể — phản ánh suy nghĩ thật, không phải PR template.
  Nên đề cập đến khách hàng, thị trường, hoặc team — không phải
  tự khen về công ty]"
  <cite>— [Tên], [Chức danh], [Tên công ty]</cite>
</blockquote>
```

Ví dụ quote tốt:
> *"Sau 18 tháng thử nghiệm với 12 khách hàng pilot, chúng tôi thấy AI-Assisted Testing chỉ thực sự hiệu quả khi team đã có test coverage tốt làm nền. Đó là lý do chúng tôi bundle nó với gói audit quy trình — không phải bán tool đơn lẻ."*
> — CTO, [Tên công ty]

Quote cần tránh:
> *"Chúng tôi rất vui mừng và tự hào khi ra mắt dịch vụ mới này..."* ❌ — không có thông tin

---

### 4. Ý nghĩa với người đọc — "Điều này có nghĩa gì với bạn" (80-100 chữ)

Phần này bắt buộc — và phải **cụ thể theo từng nhóm reader**:

```
Nếu bạn là khách hàng hiện tại   → [hành động / benefit cụ thể]
Nếu bạn đang cân nhắc hợp tác    → [thông tin liên quan đến quyết định của họ]
Nếu bạn là ứng viên              → [điều này nói lên gì về môi trường làm việc]
```

Không viết chung: *"Đây là bước tiến quan trọng của chúng tôi trong hành trình..."* ❌

---

### 5. CTA — Bước tiếp theo (40-60 chữ)

Một CTA duy nhất, rõ ràng, không pushy:

```html
<!-- Ví dụ cho ra mắt dịch vụ -->
<p>Bạn muốn thử AI-Assisted Testing cho dự án hiện tại?
<a href="/lien-he">Đặt lịch demo 30 phút</a> —
chúng tôi sẽ chạy thử trên test suite thực của bạn trước khi quyết định.</p>

<!-- Ví dụ cho tuyển dụng -->
<p>Xem chi tiết vị trí và gửi CV tại <a href="/tuyen-dung">[link]</a>.
Phản hồi trong vòng 5 ngày làm việc.</p>

<!-- Ví dụ cho sự kiện -->
<p><a href="/dang-ky-su-kien">Đăng ký tham dự</a> — còn [X] chỗ.
Deadline đăng ký: [ngày].</p>
```

---

## Quy tắc viết

**PHẢI:**
- Dùng **thông tin người dùng cung cấp** — không tự thêm chi tiết không được xác nhận
- Tiêu đề có **ý nghĩa cụ thể** — không chỉ là tên sự kiện
- Có phần **"điều này có nghĩa gì với bạn"** — bắt buộc với mọi loại tin
- Có **CTA duy nhất** ở cuối — rõ ràng, không nhiều lựa chọn cùng lúc
- Ngôi **"chúng tôi"** cho công ty, **"bạn"** cho reader
- Độ dài: **400-600 chữ** — tin công ty phải ngắn gọn, không đọc như báo cáo

**TRÁNH:**
- Mở đầu bằng tên công ty + "tự hào thông báo" hoặc "hân hạnh giới thiệu"
- Dùng thông tin không được người dùng xác nhận — dù chỉ là chi tiết nhỏ
- Quote chỉ toàn lời khen về công ty — phải có nội dung thực sự
- Liệt kê tính năng dài mà không nói benefit với reader
- Từ bị cấm: "tự hào", "hân hạnh", "đánh dấu bước ngoặt", "tiên phong",
  "hành trình", "sứ mệnh", "tầm nhìn", "đẳng cấp", "chuyên nghiệp hàng đầu"

---

## Checklist trước khi xuất bài

```
✅ Nguồn tin   : Tất cả thông tin đều từ người dùng cung cấp, không tự thêm?
✅ Tiêu đề     : Có ý nghĩa cụ thể, không chỉ là tên sự kiện?
✅ Lead        : 80 chữ đầu trả lời được Cái gì? Khi nào? Tại sao quan trọng?
✅ Ý nghĩa     : Có phần giải thích "điều này có nghĩa gì với reader" không?
✅ Quote       : Nếu có quote — có nội dung thực sự, không chỉ là lời khen?
✅ CTA         : Có đúng 1 CTA rõ ràng ở cuối không?
✅ Độ dài      : Bài có nằm trong 400-600 chữ không?
```

Nếu bất kỳ mục nào ✗ → sửa trước khi xuất bài.

---

## Format output cuối

Xuất bài dưới dạng HTML với:
- `<h2>` cho các section chính — tối đa 2-3 H2 trong toàn bài
- `<strong>` cho số liệu, tên dịch vụ, tên đối tác, ngày tháng quan trọng
- `<blockquote>` + `<cite>` cho quote leadership
- `<ul>` cho danh sách benefit hoặc tính năng — tối đa 4-5 items
- `<a href>` cho CTA — một link duy nhất ở cuối bài
- Internal link sang 1 case study hoặc bài tin công nghệ liên quan *(nếu tự nhiên)*
- Ghi rõ số chữ ước tính ở cuối

## Tags Ghost
`tin-cong-ty`
