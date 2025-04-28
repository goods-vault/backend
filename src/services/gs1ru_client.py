import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import ProductNotExists, InvalidCaptchaToken
from models.utils.category import get_category_by_id
from settings import settings
from utils import get_head

URL = "https://be-rich.gs1ru.org/api/gtin-search/public"
HEADERS = {
    "content-type": "application/json",
    "cookie": f"captcha_token={settings.gs1.captcha_token.get_secret_value()}",
}


class GS1RUClient:
    def __init__(self, db: AsyncSession):
        self.url = URL
        self.headers = HEADERS
        self.db = db

    async def get_product(self, code: str):
        async with httpx.AsyncClient(headers=self.headers, timeout=settings.gs1.request_timeout) as client:
            response = await client.post(self.url, json={"gtin": code})
            data = response.json()
            if response.status_code == 403 and data.get("message") == "Неверный результат проверки Captcha":
                raise InvalidCaptchaToken()

            response.raise_for_status()
            if settings.debug:
                print(f"Response for code {code}:", data)

        if data["noInfo"]:
            raise ProductNotExists()

        image = get_head(data, "productImageUrl")
        category_id = get_head(data, "gpcCategory", "code", "").split("_")[1]
        return {
            "gtin": get_head(data, "gtin"),
            "brand": get_head(data, "brandName"),
            "title": get_head(data, "productDescription", default="").capitalize(),
            "image": None if image in ["Маркировка", "/images/placeholder.png"] else image,
            "net_content": {
                "unit": get_head(data, "netContent", "unitCode"),
                "value": get_head(data, "netContent"),
            },
            "category_id": category_id,
            "category": (await get_category_by_id(self.db, int(category_id))).title,
            "updated_at": get_head(data, "licenseInfo", "dateUpdated"),
        }
