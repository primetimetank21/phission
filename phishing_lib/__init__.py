# pylint: disable=missing-timeout,broad-exception-caught

import requests
import json
import os
from dotenv import load_dotenv

# API Docs: https://www.ipqualityscore.com/documentation/malicious-url-scanner-api/overview
# Malicious Datasets to test with:
#   - https://www.kaggle.com/datasets/shashwatwork/web-page-phishing-detection-dataset
#   - https://research.aalto.fi/en/datasets/phishstorm-phishing-legitimate-url-dataset
#   - https://www.trendmicro.com/vinfo/us/threat-encyclopedia/malicious-url


def detect_phish(url, api_key) -> requests.Response:
    api_url = f"https://ipqualityscore.com/api/json/url/{api_key}/{url}"

    try:
        res = requests.get(api_url)
        if not res.ok:
            res = {}

    except Exception as e:
        print(f"Error in detect_phish(): {e}")
        res = {}

    return res


def save_response(res):
    res_json = json.dumps(res.json(), indent=4)
    with open("response.json", "w", encoding="utf-8") as f:
        f.write(res_json)


def get_IPQS(url: str) -> dict:
    load_dotenv()

    # url = "vamoaestudiarmedicina.blogspot.com/"
    # url = "goalgoof.com"
    api_key = os.environ.get("IPQS_API_KEY")

    score = detect_phish(url, api_key)
    if score:
        save_response(score)
        score = score.json()

    return score
