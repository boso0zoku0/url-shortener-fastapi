import secrets
from abc import ABC, abstractmethod


class AbstractTokenHelper(ABC):

    @abstractmethod
    def token_exists(self, token) -> bool:
        pass

    @abstractmethod
    def add_token(self, token) -> None:
        pass

    @abstractmethod
    def get_all_tokens(self) -> list[str]:
        pass

    @abstractmethod
    def delete_token(self, token) -> None:
        """
        :param token: удалить токен
        :return: None
        """

    @classmethod
    def generate_token(cls):
        return secrets.token_urlsafe(16)

    def generate_and_save_token(self):
        generate = self.generate_token()
        self.add_token(generate)
