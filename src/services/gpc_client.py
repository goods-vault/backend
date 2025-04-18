import httpx

BASE_URL = "https://gpc-api.gs1.org/api/browser"
HEADERS = {
    "referer": "https://gpc-browser.gs1.org/",
}
# TODO: get publicationId from /api/browser/publication?languageId=5 API endpoint instead of hardcoding it
PUBLICATION_ID = 66


class GPCClient:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = HEADERS

    async def fetch(self, endpoint: str) -> list:
        url = f"{self.base_url}/{endpoint}"
        params = {"publicationId": str(PUBLICATION_ID)}

        async with httpx.AsyncClient(headers=self.headers, params=params) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()["result"]
