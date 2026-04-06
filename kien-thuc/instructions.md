---
name: taas-kien-thuc
description: Viết bài giải thích kiến thức công nghệ cho người mới — AI, chatbot, agentic AI, automation, testing... Dùng khi người dùng nói "giải thích [khái niệm] cho người không rành tech", "viết bài về [topic] dễ hiểu", "bài nhập môn về [chủ đề]", "người mới cần biết gì về [X]". Mục tiêu: trao giá trị thật cho người đọc phổ thông, xây dựng trust với khách hàng tiềm năng của TaaS.
---

# Skill: Viết Bài Kiến Thức Công Nghệ — Dành Cho Người Mới

## Mục tiêu

Giải thích các khái niệm công nghệ phức tạp (AI, chatbot, agentic AI, automation...) theo cách mà **một người không làm kỹ thuật** cũng hiểu được — và sau khi đọc xong, họ thấy tự tin hơn khi nói chuyện với dev team, đánh giá vendor, hoặc ra quyết định công nghệ.

**Công thức giá trị:** Người đọc học được điều gì đó thực sự hữu ích → họ tin tưởng công ty → họ nhớ đến TaaS khi cần dịch vụ.

Tuyệt đối **không** viết theo kiểu encyclopedia hay Wikipedia — bài phải có góc nhìn, có ví dụ thực tế, và luôn kết nối về tác động thực tiễn với business.

---

## Auto-detect trước khi viết

Claude PHẢI tự xác định, **không hỏi lại nếu đã có topic**:

| Cần xác định | Cách detect | Nếu thiếu |
|---|---|---|
| **Khái niệm cần giải thích** | Lấy từ yêu cầu | Hỏi lại — bắt buộc |
| **Audience cụ thể** | Detect từ context | Mặc định: business owner / product manager / non-tech manager |
| **Độ sâu** | Detect từ từ ngữ | Mặc định: `nhap-mon` (beginner) |
| **Kết nối với TaaS** | Tự suy ra | Luôn kết nối nhẹ nhàng ở cuối bài |

### 3 mức độ — detect từ yêu cầu

| Từ khóa người dùng dùng | Mức độ | Đặc điểm |
|---|---|---|
| "người mới", "nhập môn", "cơ bản", "là gì" | `nhap-mon` | Không dùng jargon, nhiều analogy, ví dụ đời thường |
| "hiểu sâu hơn", "chi tiết hơn", "cách hoạt động" | `trung-cap` | Giải thích cơ chế, có ví dụ kỹ thuật đơn giản |
| "so sánh", "chọn lựa", "nên dùng loại nào" | `ung-dung` | Tập trung vào quyết định thực tế, trade-off |

---

## Audience Profile

**Người đọc chính:**
- Business owner / CEO / COO của SME hoặc startup
- Product Manager chưa có background kỹ thuật sâu
- Marketing Manager, Operations Manager đang tiếp xúc với AI/tech
- CTO/QA Manager mới bắt đầu tìm hiểu một công nghệ mới

**Họ muốn biết:**
1. Cái này là gì — giải thích bằng ngôn ngữ bình thường
2. Nó hoạt động như thế nào — đủ để hiểu, không cần implement
3. Nó ảnh hưởng đến business của họ như thế nào
4. Họ cần làm gì (hoặc hỏi ai) tiếp theo

**Họ không muốn:**
- Đọc paper kỹ thuật
- Bị overwhelm bởi acronym và jargon
- Cảm thấy mình dốt sau khi đọc xong

---

## Chủ đề phù hợp

### Về AI & Machine Learning
- AI là gì và nó "học" như thế nào (không dùng code)
- Sự khác nhau giữa AI, Machine Learning, và Deep Learning
- Large Language Model (LLM) hoạt động như thế nào
- AI có thể sai không — và tại sao

### Về Agentic AI & Automation
- Agentic AI là gì — tại sao nó khác chatbot thông thường
- Sự khác biệt giữa AI Agent và AI Chatbot
- Automation vs AI — khi nào dùng cái nào
- Workflow automation là gì và doanh nghiệp được gì từ nó

### Về Testing & QA (góc nhìn người mới)
- Testing phần mềm là gì — tại sao không thể bỏ qua
- Manual testing vs Automation testing — giải thích đơn giản
- Bug là gì và tại sao nó tốn tiền hơn bạn nghĩ
- CI/CD là gì — giải thích cho người không phải dev

### Về Bảo mật & Tin cậy
- API là gì — giải thích bằng analogy nhà hàng
- Cloud vs On-premise — doanh nghiệp nên chọn cái nào
- Data privacy trong thời AI — điều business cần biết

---

## Nguyên tắc viết — PHẢI tuân thủ

### 1. Analogy trước, định nghĩa sau

Không bao giờ mở đầu bằng định nghĩa học thuật. Luôn dùng analogy đời thường TRƯỚC khi giải thích kỹ thuật.

> ❌ "Machine Learning là một nhánh của AI cho phép máy tính học từ dữ liệu..."
>
> ✅ "Hãy nghĩ về cách bạn học nhận mặt người bạn mới: ban đầu bạn ghi nhớ đặc điểm khuôn mặt, càng gặp nhiều lần bạn càng nhận ra nhanh hơn. Machine Learning hoạt động theo cơ chế tương tự — chỉ là máy tính làm điều này với hàng triệu ví dụ thay vì vài chục."

### 2. Mỗi khái niệm kỹ thuật = 1 analogy cụ thể

Bảng analogy gợi ý (Claude có thể dùng hoặc sáng tạo analogy phù hợp hơn):

| Khái niệm | Analogy đề xuất |
|---|---|
| AI Model | Đầu bếp đã học nấu ăn từ hàng nghìn công thức |
| Training data | Sách giáo khoa và bài tập mà AI "học" từ đó |
| LLM / GPT | Người đọc cả triệu cuốn sách và học cách đoán từ tiếp theo |
| AI Agent | Trợ lý được trao quyền tự đặt lịch, gọi taxi, đặt hàng thay bạn |
| API | Bồi bàn truyền yêu cầu giữa khách hàng và bếp |
| Bug | Lỗi trong công thức nấu ăn — có thể chỉ làm món kém ngon, hoặc có thể khiến khách bệnh |
| Test automation | Nhân viên QC robot — kiểm tra 1000 sản phẩm trong 1 phút |
| CI/CD | Dây chuyền sản xuất tự động — code mới được kiểm tra và đưa lên production không cần làm thủ công |

### 3. Luôn trả lời "Vậy thì sao?" sau mỗi khái niệm

Mỗi khi giải thích xong một khái niệm, PHẢI có câu nối về tác động thực tế:

> "Vậy điều này có nghĩa gì với business của bạn? → [hàm ý cụ thể]"

### 4. Kết nối với TaaS — nhẹ nhàng, không sale

Ở cuối bài, kết nối tự nhiên (không phải CTA bán hàng):

> ✅ "Hiểu được điều này giúp bạn đặt câu hỏi đúng hơn khi làm việc với đội kỹ thuật — hoặc khi đánh giá nhà cung cấp testing như TaaS."
>
> ❌ "Liên hệ TaaS ngay hôm nay để được tư vấn miễn phí!" — phá vỡ tone giáo dục

---

## Cấu trúc bài viết

### Tiêu đề — format dành cho người mới

| Dạng | Ví dụ |
|---|---|
| Câu hỏi đơn giản | "AI Là Gì? Giải Thích Cho Người Không Rành Tech" |
| So sánh rõ ràng | "Chatbot vs AI Agent: Khác Nhau Ở Điểm Nào?" |
| Vấn đề + giải pháp hiểu | "Tại Sao App Của Bạn Hay Bị Bug — Và Testing Giải Quyết Vấn Đề Đó Thế Nào" |
| Hướng dẫn thực tế | "5 Điều Business Owner Cần Biết Về AI Trước Khi Ứng Dụng" |

Tránh:
- Tiêu đề dùng jargon không giải thích: "Tìm Hiểu Về LLM và RAG Architecture" ❌
- Tiêu đề quá học thuật: "Phân Tích So Sánh Các Mô Hình Machine Learning" ❌

---

### 1. Hook — câu hỏi hoặc vấn đề người đọc đang gặp (80-120 chữ)

Mở đầu bằng tình huống quen thuộc mà reader đang đối mặt — không phải định nghĩa:

```
Bạn vừa nghe xong một buổi pitch của vendor AI. Họ nói đến "agentic AI", 
"RAG pipeline", "embedding model". Bạn gật đầu cho có lệ nhưng thật ra 
không chắc mình có đang bị thuyết phục bởi buzzword hay không.

Bài này sẽ giải thích đúng những gì bạn cần biết — không hơn, không kém.
```

### 2. Khái niệm cốt lõi — dùng analogy (200-300 chữ)

```
H2: [Khái niệm] Là Gì — Giải Thích Không Dùng Jargon

→ Analogy đời thường (2-3 câu)
→ Giải thích cơ chế (2-3 câu, tránh math/code)
→ Ví dụ trong thực tế business (1-2 câu)
```

### 3. Cách hoạt động — từng bước đơn giản (200-300 chữ)

```
H2: [Khái niệm] Hoạt Động Như Thế Nào?

→ Breakdown thành 3-5 bước bằng <ol>
→ Mỗi bước: 1 câu kỹ thuật + 1 câu analogy
→ Không cần giải thích đủ để implement — chỉ cần đủ để hiểu
```

### 4. Ứng dụng thực tế — nó giúp được gì cho business (200-250 chữ)

```
H2: Điều Này Ảnh Hưởng Đến Business Của Bạn Thế Nào?

→ 3-4 ví dụ ứng dụng thực tế, cụ thể theo ngành
→ Kết quả đo được (tiết kiệm giờ, giảm lỗi, tăng tốc độ...)
→ Dùng <ul> với ví dụ ngắn gọn
```

### 5. Câu hỏi thường gặp — dạng FAQ (150-200 chữ)

```
H2: Câu Hỏi Thường Gặp

→ 2-3 câu hỏi ngắn + trả lời 2-4 câu
→ Chọn câu hỏi mà reader mới THỰC SỰ thắc mắc, không phải câu hỏi kỹ thuật
```

### 6. Bước tiếp theo — reader nên làm gì (100-150 chữ)

```
H2: Bạn Nên Làm Gì Tiếp Theo?

→ 2-3 hành động cụ thể (không phải "liên hệ chúng tôi")
→ Có thể gợi ý đọc bài liên quan (internal link)
→ Kết nối nhẹ với TaaS nếu tự nhiên
```

---

## Độ dài và format

- **Tổng số chữ:** 800-1200 chữ — đủ giải thích, không overwhelming
- **Đoạn văn:** Tối đa 60 chữ/đoạn — reader mới mất tập trung nhanh
- **Danh sách `<ul>/<ol>`:** Ưu tiên dùng nhiều — dễ scan, dễ nhớ
- **`<strong>`:** Chỉ cho khái niệm chính và số liệu — không bold lung tung
- **`<blockquote>`:** Dùng cho analogy nổi bật hoặc "điểm chính cần nhớ"
- **KHÔNG dùng `<h1>`** trong body

### Ví dụ format tốt

```html
<h2>AI Agent Là Gì — Khác Chatbot Ở Điểm Nào?</h2>

<p>Hãy hình dung chatbot như một nhân viên tổng đài: họ nghe câu hỏi của bạn,
tra tài liệu, trả lời — rồi dừng lại. Mỗi lần bạn hỏi là một cuộc gọi mới,
hoàn toàn độc lập.</p>

<blockquote>
  AI Agent thì khác: nó giống một trợ lý được trao quyền hành động.
  Thay vì chỉ trả lời, nó có thể đặt lịch họp, tìm tài liệu, gửi email —
  tất cả trong một luồng liên tục mà không cần bạn làm trung gian.
</blockquote>

<!-- IMAGE: AI assistant working on laptop with workflow diagram -->

<h2>Điều Này Có Nghĩa Gì Với Business Của Bạn?</h2>

<ul>
  <li><strong>Tự động hóa task lặp lại:</strong> Thay vì nhân viên copy dữ liệu giữa 3 hệ thống, AI Agent làm việc đó tự động 24/7</li>
  <li><strong>Xử lý ngoại lệ thông minh hơn:</strong> Khi gặp tình huống bất thường, Agent biết khi nào nên escalate lên người thay vì tự xử lý sai</li>
  <li><strong>Tích hợp nhiều tool:</strong> Một Agent có thể dùng email, calendar, CRM cùng lúc — chatbot thông thường thì không</li>
</ul>
```

---

## Quy tắc từ ngữ

**PHẢI:**
- Giải thích mọi acronym khi dùng lần đầu: "LLM (Large Language Model — mô hình ngôn ngữ lớn)"
- Dùng **"bạn"** khi nói với reader, **"chúng tôi"** khi đại diện TaaS
- Có ít nhất **1 con số hoặc ví dụ cụ thể** trong mỗi section chính
- Kết thúc bằng **hành động cụ thể**, không phải tóm tắt

**TRÁNH:**
- Jargon không giải thích: "backpropagation", "transformer architecture", "vector embedding"
- Câu bị động và câu phức tạp: "Điều này được thực hiện bởi..." → dùng "Hệ thống thực hiện điều này bằng cách..."
- Từ bị cấm: "giải pháp toàn diện", "công nghệ tiên tiến", "đột phá", "cách mạng hóa"
- Oversell TaaS — bài này là giáo dục, không phải quảng cáo

---

## Slug convention

```
kien-thuc/[khái niệm chính]      →  ai-la-gi
kien-thuc/[so sánh]              →  chatbot-vs-ai-agent
kien-thuc/[vấn đề thực tế]      →  tai-sao-app-bi-bug
kien-thuc/[số + chủ đề]         →  5-dieu-ve-automation-testing
```

Ví dụ slug tốt:
```
ai-la-gi                    ✅
chatbot-vs-ai-agent         ✅
testing-phan-mem-co-ban     ✅
```

---

## Checklist trước khi xuất bài

```
✅ Analogy     : Có ít nhất 2 analogy đời thường không?
✅ Jargon      : Mọi thuật ngữ kỹ thuật đều được giải thích khi dùng lần đầu?
✅ Ứng dụng    : Bài có chỉ ra ít nhất 2 tác động thực tế với business?
✅ FAQ         : Có phần câu hỏi thường gặp giải quyết thắc mắc thực sự?
✅ Hành động   : Người đọc biết làm gì sau khi đọc xong?
✅ Tone        : Bài đọc như giải thích của người bạn giỏi tech, không phải như giáo trình?
✅ TaaS link   : Có kết nối tự nhiên về TaaS ở cuối (không sale-y)?
```

Nếu bất kỳ mục nào ✗ → sửa trước khi xuất bài.

---

## Format output cuối

Xuất bài dưới dạng HTML:
- `<h2>` cho các section — viết dạng câu hỏi hoặc câu dễ hiểu
- `<h3>` cho sub-section nếu cần (hiếm khi dùng trong bài beginner)
- `<strong>` cho khái niệm quan trọng và số liệu
- `<ul>/<ol>` nhiều — bài kiến thức cần scan tốt
- `<blockquote>` cho analogy nổi bật và "điểm chính cần nhớ"
- `<!-- IMAGE: [query tiếng Anh] -->` sau H2 chính (1-2 ảnh minh họa)
- Internal link sang bài liên quan (case study hoặc insight phù hợp)

## Tag WordPress
`kien-thuc`
