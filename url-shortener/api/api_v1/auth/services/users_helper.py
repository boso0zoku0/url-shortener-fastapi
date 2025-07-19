from abc import ABC, abstractmethod


class AbstractUserHelper(ABC):

    @abstractmethod
    def get_user_password(self, username) -> str | None:
        pass

    """
    :param username - передали имя пользователя
    :return password - получили пароль этого пользователя если найден
    """

    @classmethod
    def check_passwords_match(cls, password_1, password_2) -> bool:
        return password_1 == password_2

    def validate_user_password(self, username, password) -> bool:
        """
        :param username - имя пользователя чей пароль проверить
        :param password - переданный пароль сверить с тем что с БД
        :return - True если совпадает, иначе False
        """
        password_db = self.get_user_password(username=username)
        if password_db is None:
            return False
        self.check_passwords_match(password_1=password_db, password_2=password)
        return True
