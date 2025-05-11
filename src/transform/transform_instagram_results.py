import pandas as pd
from datetime import datetime
import json

def extract_post_data(posts: list) -> pd.DataFrame:
    records = []

    for post in posts:
        post_id = post.get("id")
        caption = post.get("caption", "")
        likes = post.get("likesCount")
        timestamp = post.get("timestamp")

        # Formatação da data e hora
        if timestamp:
            dt = datetime.fromisoformat(timestamp.replace("Z", ""))
            date_str = dt.strftime("%d-%m-%Y")
            time_str = dt.strftime("%H:%M")
        else:
            date_str = None
            time_str = None

        records.append({
            "post_id": post_id,
            "caption": caption,
            "likes_count": likes,
            "date": date_str,
            "time": time_str
        })
    return pd.DataFrame(records)

path = 'instagram_ladygaga_2025-05-11_20-05-03.json'
with open(path, "r") as f:
    raw_data = json.load(f)

df = extract_post_data(raw_data)
print(df.head())
