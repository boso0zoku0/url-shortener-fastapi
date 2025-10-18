import secrets
from abc import ABC, abstractmethod


class AbstractTokenHelper(ABC):

    @abstractmethod
    def token_exists(self, token: str) -> bool:
        pass

    @abstractmethod
    def add_token(self, token: str) -> None:
        pass

    @abstractmethod
    def get_all_tokens(self) -> list[str]:
        pass

    @abstractmethod
    def delete_token(self, token: str) -> None:
        """
        :param token: удалить токен
        :return: None
        """

    def generate_token(self) -> str:
        return secrets.token_urlsafe(16)

    def generate_and_save_token(self) -> str:
        token = self.generate_token()
        self.add_token(token)
        return token
