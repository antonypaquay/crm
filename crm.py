import re
import string
from tinydb import TinyDB, where
from pathlib import Path


class User:

    DB = TinyDB(Path(__file__).resolve().parent / "data.json", indent=4)

    def __init__(self, first_name: str, last_name: str, phone_number: str = "", address: str = ""):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address

    def __repr__(self):
        return f"User({self.first_name}, {self.last_name})"

    def __str__(self):
        return f"{self.full_name}\n{self.phone_number}\n{self.address}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def db_instance(self):
        return User.DB.get((where("first_name") == self.first_name) & (where("last_name") == self.last_name))

    def _checks(self):
        self._check_phone_number()
        self._check_names()

    def _check_phone_number(self):
        phone_number = re.sub(r"[+()\s]*", "", self.phone_number)
        if len(phone_number) < 10 or not phone_number.isdigit():
            raise ValueError(f"Phone number {phone_number} is invalid.")

    def _check_names(self):
        if not (self.first_name and self.last_name):
            raise ValueError("The first and last name cannot be empty.")
        special_characters = string.punctuation + string.digits

        for character in self.first_name + self.last_name:
            if character in special_characters:
                raise ValueError(f"Invalid name {self.full_name}")

    def save(self, validate_data: bool = False) -> int:
        if validate_data:
            self._checks()

        return User.DB.insert(self.__dict__)


def get_all_users():
    return [User(**user) for user in User.DB.all()]


if __name__ == "__main__":
    martin = User.db_instance('Manon', 'Gaillard')
    print(martin)
    # from faker import Faker
    # fake = Faker(locale="fr_FR")

    # for _ in range(5):
    #     user = User(first_name=fake.first_name(),
    #                 last_name=fake.last_name(),
    #                 phone_number=fake.phone_number(),
    #                 address=fake.address())
    #     print(user.save(True))
    #     print("-" * 10)
