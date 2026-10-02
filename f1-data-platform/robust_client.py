import time
import logging
import requests

class RobustClient:
    def __init__(
            self,
            base_url: str,
            max_retries: int = 3,
            timeout: int = 30,
    ):
        self.base_url = base_url
        self.max_retries = max_retries
        self.timeout = timeout
    def get_season(self, season: int):
        url = f"{self.base_url}/{season}.json"

        for attempt in range(self.max_retries):
            try: 
                response = requests.get(
                    url,
                    timeout=self.timeout
                )
                if response.status_code in (
                    429,  # Too Many Requests
                    500,  # Internal Server Error
                    502,  # Bad Gateway
                    503,  # Service Unavailable
                    504,  # Gateway Timeout
                ):
                    raise requests.HTTPError(
                        f"Retryable error: {response.status_code}"
                    )
                response.raise_for_status()
                return response.json()
            except (
                requests.ConnectionError,
                requests.Timeout,
                requests.HTTPError,
            ) as error:
                if attempt == self.max_retries -1:
                    raise

                delay = 2 ** attempt

                print(
                    f"Request failed with error: {error}. Retrying in {delay} seconds..."
                
                )
                time.sleep(delay)