from transformers import pipeline
import pandas as pd
import ast

# โหลดโมเดลสำหรับการวิเคราะห์ความรู้สึก
# model นี้จะแบ่งเป็น positive, negative และ neutral
print("กำลังโหลดโมเดลสำหรับการวิเคราะห์ความรู้สึก...")
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model='cardiffnlp/twitter-roberta-base-sentiment-latest',
    truncation=True,
    max_length=512
)
print("โมเดลโหลดเสร็จเรียบร้อย")

def analyze_sentiment(text):
    """
    วิเคราะห์ความรู้สึกของข้อความและคืนค่าเป็น positive, negative หรือ neutral และ socre ของแต่ละประเภท
    """
    if not isinstance(text, str) or text.strip() == "":
        return "neutral", 0.0
    
    try:
        # ตัดข้อความให้ไม่เกิน 512 ตัวอักษรเพื่อให้โมเดลทำงานได้
        short_text = text[:1000]
        result = sentiment_pipeline(short_text)[0]

        label = result["label"].lower() # positive / negative / neutral
        score = round(result["score"], 4) # ความมั่นใจของโมเดล
        return label, score
    
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการวิเคราะห์ความรู้สึก: {e}")
        return "neutral", 0.0

def run_sentiment(df):
    """
    รัน Sentiment Analysis กับทุกบทความ"""
    print("\n กำลังวิเคราะห์ความรู้สึกของบทความ...")
    
    results = df["content"].apply(analyze_sentiment)
    df["sentiment"] = results.apply(lambda x: x[0])
    df["sentiment_score"] = results.apply(lambda x: x[1])

    print("เสร็จเรียบร้อย")
    return df

def get_sentiment_summary(df):
    """
    สรุปผล Sentiment ของทุกบทความใน DataFrame
    """
    summary = df["sentiment"].value_counts()
    print("\n  สรุปผลการวิเคราะห์ความรู้สึก:")
    for label, count in summary.items():
        print(f" {label}: {count} บทความ")
    return summary

if __name__ == "__main__":
    # โหลดข้อมูลที่ผ่าน NER แล้ว
    df = pd.read_csv("D:/Data science/DataTest/ai_news_project/data/bbc_articles_with_ner.csv")

    # รัน Sentiment Analysis กับบทความทั้งหมด
    df = run_sentiment(df)

    # แสดงสรุปผลการวิเคราะห์ความรู้สึก
    get_sentiment_summary(df)

    # แสดงตัวอย่าง
    print("\n ตัวอย่างผลการวิเคราะห์ความรู้สึก:")
    print(df[["title", "sentiment", "sentiment_score"]].head(10).to_string())

    # บันทึกผลลัพธ์ลงไฟล์ใหม่
    df.to_csv("D:/Data science/DataTest/ai_news_project/data/bbc_final.csv", index=False)
    print("\n บันทึกผลลัพธ์ลงไฟล์ bbc_final.csv เรียบร้อยแล้ว")
