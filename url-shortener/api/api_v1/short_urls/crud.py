from schemas.short_url import ShortUrl
import random

SHORT_URLS = [
    ShortUrl(id=random.randint(0, 10), target_url="http://google.com", slug="google"),
    ShortUrl(id=random.randint(0, 10), target_url="http://yandex.ru", slug="yandex"),
]
