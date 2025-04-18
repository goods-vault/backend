import httpx
from exceptions import ProductNotExists
from settings import settings
from utils import get_head

URL = "https://be-rich.gs1ru.org/api/gtin-search/public"
HEADERS = {
    "content-type": "application/json",
    "cookie": f"captcha_token={settings.gs1.captcha_token.get_secret_value()}",
}


class GS1RUClient:
    def __init__(self):
        self.url = URL
        self.headers = HEADERS

    async def get_product(self, code: str):
        async with httpx.AsyncClient(headers=self.headers) as client:
            response = await client.post(self.url, json={"gtin": code})
            response.raise_for_status()
            response = response.json()
            if settings.debug:
                print(f"Response for code {code}:", response)

        if response["noInfo"]:
            raise ProductNotExists()

        image = get_head(response, "productImageUrl")
        return {
            "gtin": get_head(response, "gtin"),
            "brand": get_head(response, "brandName"),
            "title": get_head(response, "productDescription", default="").capitalize(),
            "image": None if image in ["Маркировка", "/images/placeholder.png"] else image,
            "net_content": {
                "unit": get_head(response, "netContent", "unitCode"),
                "value": get_head(response, "netContent"),
            },
            "category": get_head(response, "gpcCategory", "code", "").lstrip("GPCCLBRK_"),
            "updated_at": get_head(response, "licenseInfo", "dateUpdated"),
        }
