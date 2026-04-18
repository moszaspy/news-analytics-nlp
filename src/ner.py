#NER(Named Entity Recognition) คือการระบุและจำแนกชื่อเฉพาะในข้อความ เช่น ชื่อคน สถานที่ องค์กร เป็นต้น
#ในที่นี้เราจะใช้ spaCy ซึ่งเป็นไลบรารีสำหรับการประมวลผลภาษาธรรมชาติ (NLP) ที่มีความสามารถในการทำ NER ได้อย่างมีประสิทธิภาพ
import spacy
import pandas as pd
from collections import Counter

# โหดล model
nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    """
    ฟังก์ชันนี้จะรับข้อความและคืนค่าชื่อเฉพาะที่ถูกระบุในข้อความนั้น
    """
    if not isinstance(text, str) or text.strip() =="":
        return []
    
    doc = nlp(text)
    persons = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            #ทำความสะอาดชื่อ เช่น ลบช่องว่างส่วนเกิน
            name = ent.text.strip()
            name = name.replace("'s", "").replace("’s", "").strip() # ลบ 's ทุก format

            # กรองชื่อที่ไม่ต้องการออก
            if len(name) < 2: # ชื่อสั้นเกินไป
                continue
            if name.islower(): # ชื่อที่เป็นตัวพิมพ์เล็กทั้งหมด
                continue
            if len(name.split()) > 4: # ชื่อที่ยาวเกินไป
                continue

            persons.append(name)
    return persons

def run_ner(df):
    """
    รัน NER กับทุกบทความใน DataFrame และนับจำนวนชื่อเฉพาะที่ถูกระบุ
    """
    print("กำลังสกัดชื่อบุคคลจากบทความ...")

    df["persons"] = df["content"].apply(extract_entities)
    df['Persons_count'] = df['persons'].apply(len)

    print(f" เสร็จเรียบร้อย")
    return df

def get_top_persons(df, top_n=10):
    """
    หาบุคคลที่ถูกระบุมากที่สุดในบทความ
    """
    all_persons = []
    for persons in df["persons"]:
        all_persons.extend(persons)

    counter = Counter(all_persons)
    
    # รวมชื่อที่ซ้ำกัน เช่น Trump และ Donald Trump → Donald Trump
    merged = {}
    for name, count in counter.items():
        # หาว่าชื่อนี้เป็น subset ของชื่ออื่นหรือไม่
        full_name = next(
            (n for n in counter if name in n and name != n),
            name
        )
        merged[full_name] = merged.get(full_name, 0) + count
    
    sorted_persons = sorted(merged.items(), key=lambda X:X[1], reverse=True)
    return sorted_persons[:top_n]

if __name__ == "__main__":
    df = pd.read_csv("D:/Data science/DataTest/ai_news_project/data/bbc_articles.csv")

    # รัน NER
    df = run_ner(df)

    # แสดงผลลัพธ์
    print("\nตัวอย่างชื่อบุคคลที่ถูกระบุในบทความ 10 อันดับแรก:")
    top_persons = get_top_persons(df)
    for person, count in top_persons:
        print(f"{person}: {count} ครั้ง")

    # บันทึกผลลัพธ์กลับไปยัง CSV
    df.to_csv("D:/Data science/DataTest/ai_news_project/data/bbc_articles_with_ner.csv", index=False)
    print("\n✅ บันทึกข้อมูลพร้อม NER เสร็จเรียบร้อย! ไฟล์ใหม่: bbc_articles_with_ner.csv")
