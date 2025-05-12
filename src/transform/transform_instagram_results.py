import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import pandas as pd
from datetime import datetime

def parse_timestamp(timestamp: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    """
    Convert timestamp ISO into datetime.
    """
    if not timestamp:
        return None, None
    
    try:
        dt = datetime.fromisoformat(timestamp.replace("Z", ""))
        return dt.strftime("%d-%m-%Y"), dt.strftime("%H:%M")
    except ValueError:
        print(f"Erro ao processar timestamp: {timestamp}")
        return None, None


def extract_post_data(posts: List[Dict]) -> pd.DataFrame:
    """
    Extract data from JSON output.
    """
    records = []
    
    for post in posts:
        record = {
            "post_id": post.get("id"),
            "caption": post.get("caption", ""),
            "likes_count": post.get("likesCount", 0),
            "date": None,
            "time": None
        }
        
        record["date"], record["time"] = parse_timestamp(post.get("timestamp"))
        
        records.append(record)
    
    return pd.DataFrame(records)


def process_instagram_data(input_path: Path, output_path: Path) -> None:
    """
    Process data and save into CSV
    """

    if not input_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {input_path}")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(input_path, "r", encoding="utf-8") as file:
        posts = json.load(file)
    
    df = extract_post_data(posts)
    df.to_csv(output_path, sep=";", index=False, encoding="utf-8")
    
    print(f"File saved: {output_path}")
    print("\nDataframe sample:")
    print(df.head())

def main():
    # Dir setup
    current_path = Path(__file__)
    base_dir = current_path.parents[2]
    data_dir = base_dir / "data" / "raw"
    output_dir = base_dir / "data" / "processed"
    
    input_filename = "instagram_ladygaga_2025-05-11_20-05-03.json"
    input_path = data_dir / input_filename
    output_path = output_dir / "processed.csv"
    
    process_instagram_data(input_path, output_path)

if __name__ == "__main__":
    main()