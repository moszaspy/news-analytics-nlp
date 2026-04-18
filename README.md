My personal information
| **Name** | Chinatip Boonnarong (ชินาธิป บุญณรงค์) |
| **University** | Prince of Songkla University (มหาวิทยาลัยสงขลานครินทร์) |
| **Bachelor's Degree** | Faculty of Science, Applied Biochemistry |
| **Master's Degree** | Data Science (in progress) |
| **GitHub** | https://github.com/moszaspy |

## 📁 Project Structure
news-analytics-nlp/
│
├── data/
├── src/
│   ├── scraper.py
│   ├── ner.py
│   ├── sentiment.py
│   └── dashboard.py
└── requirements.txt

# 📰 News Analytics NLP Pipeline

แอปพลิเคชัน NLP แบบครบวงจรที่ดึงข้อมูลจากบทความข่าว แยกข้อมูลบุคคลสำคัญโดยใช้การระบุชื่อเอนทิตี (NER) วิเคราะห์ความรู้สึก และแสดงข้อมูลเชิงลึกผ่านแดชบอร์ดแบบโต้ตอบ
---

## 🗺️ System Architecture

BBC News Website
↓
[Web Scraping] - ใช้ requests  ทำหน้าที่ส่งคำขอ HTTP เพื่อดึงโค้ด HTML มาจากเว็บ + BeautifulSoup ทำหน้าที่แปลง (Parse) โค้ด HTML นั้นให้เป็นโครงสร้างที่ค้นหาและดึงข้อมูลเฉพาะส่วนที่ต้องการได้ง่าย
↓
[Named Entity Recognition] - ใช้ spaCy ซึ่งเป็นไลบรารีสำหรับการประมวลผลภาษาธรรมชาติ (NLP) 
↓
[Sentiment Analysis] - RoBERTa (cardiffnlp/twitter-roberta-base-sentiment-latest)
↓
[Dashboard & Visualization] - Streamlit เพื่อสร้างเว็บแอปพลิเคชันข้อมูลแบบโต้ตอบได้อย่างรวดเร็ว + Plotly เป็นไลบรารีสร้างกราฟที่โต้ตอบได้

---

## ⚙️ Technical Solution & Algorithm

### 1. Web Scraping
- Library: `requests`, `BeautifulSoup4`
- Source: BBC News World (https://www.bbc.com/news/world)
- Extracts: URL ของบทความ, ชื่อเรื่อง, เนื้อหา, วันที่และเวลาพิมพ์

### 2. Named Entity Recognition (NER)
- Model: `spaCy en_core_web_sm` (Small Language Model)
- Target: เฉพาะบุคคลเท่านั้น (PERSON entities only)
- Post-processing:
  - ลบคำต่อท้ายแสดงความเป็นเจ้าของ (`'s`)
  - กรองชื่อที่สั้นกว่า 2 ตัวอักษร
  - Filter all-lowercase tokens
  - รวมชื่อบางส่วน (เช่น Trump → Donald Trump)

### 3. Sentiment Analysis
- Model: `cardiffnlp/twitter-roberta-base-sentiment-latest`
- Labels: `positive` / `negative` / `neutral`
- Input: เนื้อหาบทความ (ตัดทอนเหลือ 1,000 ตัวอักษร)
- Output: sentiment label + confidence score

### 4. Visualization Dashboard
- Framework: `Streamlit`
- Charts: `Plotly`
- Features:
  - KPI cards (total articles, positive, negative, neutral)
  - Sentiment distribution pie chart
  - Top 10 most mentioned persons bar chart
  - ฮิสโตแกรมแสดงความรู้สึกต่อคน
  - ตารางข้อมูลบทความที่สามารถกรองได้

---

## 🚀 How to Run

### 1. Install dependencies (ติดตั้งส่วนประกอบที่จำเป็น)
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Scrape news articles ( Scrape news articles )
```bash
python src/scraper.py
```

### 3. Run NER
```bash
python src/ner.py
```

### 4. Run Sentiment Analysis
```bash
python src/sentiment.py
```

### 5. Launch Dashboard
```bash
streamlit run src/dashboard.py
```

▶️ Push README ขึ้น GitHub
git add README.md
git commit -m "add README with system design and developer info"
git push origin main
