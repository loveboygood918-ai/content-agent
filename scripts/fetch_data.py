import os
import json
import time
import requests

APIFY_TOKEN = os.environ["APIFY_TOKEN"]
ACTOR_ID = "apify~instagram-scraper"

INPUT_PAYLOAD = {
    "addParentData": False,
    "directUrls": [
        "https://www.instagram.com/bhavinaistories/",
        "https://www.instagram.com/viral._.aistories/",
        "https://www.instagram.com/user_resl_me/",
        "https://www.instagram.com/relatable.exee/",
        "https://www.instagram.com/thezuvora/",
        "https://www.instagram.com/wondermakerfr/"
    ],
    "resultsLimit": 20,
    "resultsType": "posts"
}

def run_actor():
    url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/run-sync-get-dataset-items"
    params = {"token": APIFY_TOKEN}
    print("Starting Apify Instagram Scraper run...")
    resp = requests.post(url, params=params, json=INPUT_PAYLOAD, timeout=600)
    resp.raise_for_status()
    data = resp.json()
    print(f"Fetched {len(data)} items.")
    return data

def save_data(data):
    os.makedirs("dashboard", exist_ok=True)
    with open("dashboard/data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Saved to dashboard/data.json")

if __name__ == "__main__":
    items = run_actor()
    save_data(items)
