import httpx


class GreenhouseClient:
    BASE_URL = "https://boards-api.greenhouse.io/v1/boards"

    def __init__(self):
        self.client = httpx.Client(timeout=30)

    def fetch_jobs(self, board_token: str):
        url = f"{self.BASE_URL}/{board_token}/jobs?content=true"

        response = self.client.get(url)

        response.raise_for_status()

        return response.json()

    def close(self):
        self.client.close()
