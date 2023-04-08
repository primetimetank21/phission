# type: ignore
# pylint: disable=missing-timeout
import requests
import json
import os
from dotenv import load_dotenv

# API Docs: https://www.ipqualityscore.com/documentation/malicious-url-scanner-api/overview
# Malicious Datasets to test with:
#   - https://www.kaggle.com/datasets/shashwatwork/web-page-phishing-detection-dataset
#   - https://research.aalto.fi/en/datasets/phishstorm-phishing-legitimate-url-dataset
#   - https://www.trendmicro.com/vinfo/us/threat-encyclopedia/malicious-url


def detect_phish(url, api_key):
    api_url = f"https://ipqualityscore.com/api/json/url/{api_key}/{url}"
    res = requests.get(api_url)

    print(res.status_code)
    save_response(res)


def save_response(res):
    res_json = json.dumps(res.json(), indent=4)
    with open("response.json", "w", encoding="utf-8") as f:
        f.write(res_json)


def main():
    load_dotenv()

    # url = "vamoaestudiarmedicina.blogspot.com/"
    url = "goalgoof.com"
    api_key = os.environ.get("IPQS_API_KEY")

    detect_phish(url, api_key)


if __name__ == "__main__":
    main()
