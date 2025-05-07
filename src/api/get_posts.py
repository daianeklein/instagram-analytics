import os
import json
from datetime import datetime
from dotenv import load_dotenv
from apify_client import ApifyClient

class InstagramScraper:
    def __init__(self, api_key, actor_id, username, result_limit=5, output_dir="data"):
        self.client = ApifyClient(api_key)
        self.actor_id = actor_id
        self.username = username
        self.result_limit = result_limit
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def run_actor(self):
        run_input = {
            'username' : [self.username],
            'resultsLimit': self.result_limit}

        self.run = self.client.actor(self.actor_id).call(run_input=run_input)

    def fetch_data(self):
        return list(self.client.dataset(self.run['defaultDatasetId']).iterate_items())
    
    def save_to_json(self, data):
        date_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_path = os.path.join(self.output_dir, f"instagram_ladygaga_{date_str}.json")

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"Arquivo salvo em: {output_path}")

if __name__ == '__main__':
    load_dotenv()

    scraper = InstagramScraper(
        api_key=os.getenv('API_APIFY'),
        actor_id=os.getenv('ACTOR_ID'),
        username='ladygaga',
        result_limit=2)
    
    scraper.run_actor()
    data = scraper.fetch_data()
    scraper.save_to_json(data)
