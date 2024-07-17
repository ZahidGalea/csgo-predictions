from base64 import b64decode
import requests
import time

HLTV_BASE_URL = "https://www.hltv.org"


def request(url):
    MAX_RETRIES = 2

    for i in range(MAX_RETRIES + 1):
        try:
            api_response = requests.post(
                "https://api.zyte.com/v1/extract",
                auth=("", ""),
                json={
                    "url": url,
                    "httpResponseBody": True,
                },
            )

            http_response_body: str = b64decode(
                api_response.json()["httpResponseBody"]
            ).decode("utf-8")

            return http_response_body

        except Exception as e:
            if i == MAX_RETRIES:  # Si se ha alcanzado el máximo de reintentos
                print("EXCEPTION OCCURRED on api request")
                raise e
            else:
                print(f"Attempt {i+1} failed. Retrying...")
                time.sleep(3)
