import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import pandas as pd
from datetime import datetime

def parse_timestamp(timestamp: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    """
    Convert timestamp ISO into formatted date and time.
    """
    if not timestamp:
        return None, None
    
    try:
        dt = datetime.fromisoformat(timestamp.replace("Z", ""))
        return dt.strftime("%d-%m-%Y"), dt.strftime("%H:%M")
    except ValueError:
        print(f"Error processing timestamp: {timestamp}")
        return None, None

def extract_post_data(posts: List[Dict]) -> pd.DataFrame:
    """
    Extract relevant data from Instagram posts.
    """
    records = []
    
    for post in posts:
        record = {
            "post_id": post.get("id"),
            "caption": post.get("caption", ""),
            "likes_count": post.get("likesCount", 0),
            "media_url": post.get("imageUrl") or post.get("videoUrl", ""),
            "date": None,
            "time": None
        }
        
        record["date"], record["time"] = parse_timestamp(post.get("timestamp"))
        records.append(record)
    
    return pd.DataFrame(records)


def process_instagram_data(input_path: Path, output_path: Path) -> pd.DataFrame:
    """
    Process Instagram data from JSON to CSV.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_path}")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(input_path, "r", encoding="utf-8") as file:
        posts = json.load(file)
    
    df = extract_post_data(posts)
    df.to_csv(output_path, sep=";", index=False, encoding="utf-8")
    
    print(f"File saved: {output_path}")
    print("\nDataframe sample:")
    print(df.head())
    
    return df


def main(input_file: Optional[Path] = None, output_file: Optional[Path] = None):
    """
    Main function to process Instagram data.
    """
    # If no input file is provided, use the most recent JSON in the raw data directory
    if input_file is None:
        current_path = Path.cwd()
        base_dir = current_path.parents[2]
        data_dir = base_dir / "data" / "raw"
        
        # Find the most recent JSON file
        json_files = list(data_dir.glob("instagram_*.json"))
        if not json_files:
            print("No Instagram JSON files found in the raw data directory.")
            return
        
        input_file = max(json_files, key=lambda f: f.stat().st_mtime)
    
    if output_file is None:
        output_dir = input_file.parent.parent / "processed"
        output_file = output_dir / f"{input_file.stem}_processed.csv"
    
    process_instagram_data(input_file, output_file)


if __name__ == "__main__":
    main()