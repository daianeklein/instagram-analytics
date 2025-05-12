from apify_client import ApifyClient
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import os
import json

def fetch_and_save_posts():
    load_dotenv()

    api_token = os.getenv("API_APIFY")
    actor_id = os.getenv("ACTOR_ID")

    if not api_token or not actor_id:
        raise ValueError("Missing API_APIFY or ACTOR_ID in .env file")

    # output
    date_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    current_path = Path(__file__)
    data_dir = current_path.parents[2] / "data/raw"
    data_dir.mkdir(parents=True, exist_ok=True)

    output_path = data_dir / f"instagram_{date_str}.json"

    client = ApifyClient(api_token)
    run_input = {
        "username": ["ladygaga"],
        "resultsLimit": 2,
    }

    run = client.actor(actor_id).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    # Save results to file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(items)} posts to {output_path}")

if __name__ == '__main__':
    fetch_and_save_posts()
