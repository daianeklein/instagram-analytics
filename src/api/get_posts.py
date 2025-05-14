import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import os
import json
from apify_client import ApifyClient

# Add the src directory to the Python path
current_path = Path(__file__).resolve()
src_dir = current_path.parent / 'src'
sys.path.insert(0, str(src_dir))

def fetch_and_save_posts(instagram_profile: str):
    """
    Fetch Instagram posts using Apify API and save to JSON file.
    """
    load_dotenv()

    api_token = os.getenv('API_APIFY')
    actor_id = os.getenv('ACTOR_ID')

    if not api_token or not actor_id:
        raise ValueError('Missing API_APIFY or ACTOR_ID in .env file')

    date_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    data_dir = current_path.parents[2] / 'data' / 'raw'
    data_dir.mkdir(parents=True, exist_ok=True)

    output_path = data_dir / f'instagram_{instagram_profile}_{date_str}.json'

    # Configure Apify client
    client = ApifyClient(api_token)
    
    run_input = {
        'username': [instagram_profile],
        'resultsLimit': 5,  
    }

    run = client.actor(actor_id).call(run_input=run_input)
    items = list(client.dataset(run['defaultDatasetId']).iterate_items())

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    print(f'Saved {len(items)} posts to {output_path}')
    
    return output_path


def main(instagram_profile: str = None):
    """
    Main function to run the Instagram data fetching process.
    """
    if not instagram_profile:
        instagram_profile = input("Enter the Instagram profile to fetch: ").strip()
    try:
        output_file = fetch_and_save_posts(instagram_profile)
        print(f"Data successfully fetched and saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
