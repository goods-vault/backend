class ProductNotExists(Exception):
    """Товара нет в базе данных GS1 Russia"""

class InvalidCaptchaToken(Exception):
    """Невалидный или истёкший капча-токен"""
