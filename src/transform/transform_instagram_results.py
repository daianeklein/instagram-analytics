# src/transform/instagram_transformer.py

import pandas as pd
from typing import List, Dict
from datetime import datetime

class InstagramPostTransformer:
    def __init__(self, raw_data: List[Dict]):
        self.raw_data = raw_data

    def transform(self) -> pd.DataFrame:
        transformed_data = []

        for post in self.raw_data:
            post_id = post.get("id")
            caption = post.get("caption")
            comments_count = post.get("commentsCount")
            likes_count = post.get("likesCount")
            timestamp = post.get("timestamp")

            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace("Z", ""))
                    date_str = dt.strftime("%d-%m-%Y")
                    time_str = dt.strftime("%H:%M:%S")
                except ValueError:
                    date_str = None
                    time_str = None
            else:
                date_str = None
                time_str = None

            transformed_data.append({
                "post_id": post_id,
                "caption": caption,
                "comments_count": comments_count,
                "likes_count": likes_count,
                "date": date_str,
                "time": time_str
            })

        return pd.DataFrame(transformed_data)
    
if __name__ == '__main__':
    import json

    with open('/Users/daianeklein/Documents/DS/instagram-analytics/data/raw/instagram_ladygaga_2025-05-07_19-00-00.json', 'r') as file:
        data = json.load(file)

        transformer = InstagramPostTransformer(data)
        df_transformed = transformer.transform()
        print(df_transformed)

