import os
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

API_APIFY = os.getenv('API_APIFY')
client = ApifyClient(API_APIFY)

# Prepare the Actor input
run_input = {
    "username": ["ladygaga"],
    "resultsLimit": 1,
}

# Run the Actor and wait for it to finish
run = client.actor("nH2AHrwxeTRJoN5hX").call(run_input=run_input)

# Fetch and print Actor results from the run's dataset (if there are any)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)