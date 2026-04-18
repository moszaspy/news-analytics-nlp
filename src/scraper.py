import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

def get_bbc_articles(max_articles=20):
    """
    ดึงข่าวจาก BBC News หมวด World
    """

    base_url = "https://www.bbc.com/news/world"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36)"
    }
    print(f"🔍 กำลังดึงข้อมูลจาก BBC News")

    # ดึง HTML จากหน้าเว็บหลัก
    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # ค้นหาลิงก์ข่าว
    articles = []
    links = soup.find_all("a", href=True)

    news_links = []
    for link in links:
        href = link["href"]
        if "/news/articles/" in href:
            full_url = "https://www.bbc.com" + href if href.startswith("/") else href
            if full_url not in news_links:
                news_links.append(full_url)

    
    print(f"found all links: {len(news_links)} links")

    # เข้าไปอ่านแต่ละข่าว
    for i, url in enumerate(news_links[:max_articles]):
        try:
            print(f"กำลังอ่านข่าวที่ {i+1}: {url}")

            res = requests.get(url, headers=headers)
            article_soup = BeautifulSoup(res.text, "html.parser")

            # ดึง title
            title_tag = article_soup.find("h1")
            title = title_tag.text.strip() if title_tag else "No Title"

            # ดึง content
            paragraphs = article_soup.find_all("p")
            content = " ".join([p.get_text(strip=True) for p in paragraphs])

            articles.append({
                "url": url,
                "title": title,
                "content": content,
                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            time.sleep(1) # หลีกเลี่ยงการส่งคำขอเร็วเกินไป
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการดึงข่าว: {e}")
            continue
    return pd.DataFrame(articles)


if __name__ == "__main__":
    df = get_bbc_articles(max_articles=20)
    
    if len(df) > 0:
        df.to_csv("D:/Data science/DataTest/ai_news_project/data/bbc_articles.csv", index=False)
        print(f"\n✅ บันทึกข้อมูลเสร็จ! ได้ {len(df)} บทความ")
        print(df[["title", "scraped_at"]].head())
    else:
        print("❌ ไม่ได้ข้อมูลเลย มีปัญหาในฟังก์ชัน")



import pandas as pd

df = pd.read_csv("D:/Data science/DataTest/ai_news_project/data/bbc_articles.csv")

print(f"จำนวนบทความ: {len(df)}")
print(f"\nคอลัมน์: {df.columns.tolist()}")
print(f"\nตัวอย่าง title:")
print(df["title"].head())
print(f"\nตัวอย่าง content (100 ตัวอักษรแรก):")
print(df["content"].head().str[:100])
print(f"\nมี content ว่างเปล่าไหม: {df['content'].isna().sum()} บทความ")