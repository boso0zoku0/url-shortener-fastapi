class ShortUrlBaseError(Exception):
    """
    Base exception for short url CRUD actions
    """


class ShortUrlAlreadyExists(ShortUrlBaseError):
    """
    Raised on short url creation if such slug already exists
    """
