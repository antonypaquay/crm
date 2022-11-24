from crm import User
import pytest
from tinydb import TinyDB, table
from tinydb.storages import MemoryStorage


@pytest.fixture
def setup_db():
    User.DB = TinyDB(storage=MemoryStorage)


@pytest.fixture
def user(setup_db):
    u = User(
        first_name="Patrick",
        last_name="Martin",
        address="24 Rue du moulin, 1400 Nivelles",
        phone_number="0476232323")

    u.save()
    return u


def test_first_name(user):
    assert user.first_name == "Patrick"


def test_full_name(user):
    assert user.full_name == "Patrick Martin"


def test_exists(user):
    assert user.exists() is True


def test_not_exists(setup_db):
    u = User(
        first_name="Patrick",
        last_name="Martin",
        address="24 Rue du moulin, 1400 Nivelles",
        phone_number="0476232323")
    assert u.exists() is False


def test_db_instance(user):
    assert isinstance(user.db_instance, table.Document)
    assert user.db_instance["first_name"] == "Patrick"
    assert user.db_instance["last_name"] == "Martin"
    assert user.db_instance["address"] == "24 Rue du moulin, 1400 Nivelles"
    assert user.db_instance["phone_number"] == "0476232323"


def test_not_db_instance(setup_db):
    u = User(
        first_name="Patrick",
        last_name="Martin",
        address="24 Rue du moulin, 1400 Nivelles",
        phone_number="0476232323")
    assert u.db_instance is None


def test__check_phone_number(setup_db):
    user_good = User(
        first_name="Antoine",
        last_name="Dupond",
        address="24 Rue du moulin, 1400 Nivelles",
        phone_number="0476232323")
    user_bad = User(
        first_name="Antoine",
        last_name="Dupond",
        address="24 Rue du moulin, 1400 Nivelles",
        phone_number="abdda")

    with pytest.raises(ValueError) as err:
        user_bad._check_phone_number()

    assert "invalid" in str(err.value)

    user_good.save(validate_data=True)
    assert user_good.exists() is True


def test__check_names_empty(setup_db):
    user_bad = User(
        first_name="",
        last_name="",
        address="24 Rue du moulin, 1400 Nivelles",
        phone_number="0476232323")

    with pytest.raises(ValueError) as err:
        user_bad._check_names()

    assert "The first and last name cannot be empty." in str(err.value)


def test__check_names_invalid_characters(setup_db):
    user_bad = User(
        first_name="Patrick#*#",
        last_name="%*¨£$",
        address="24 Rue du moulin, 1400 Nivelles",
        phone_number="0476232323")

    with pytest.raises(ValueError) as err:
        user_bad._check_names()

    assert "Invalid name" in str(err.value)


def test_delete(setup_db):
    user_test = User(
        first_name="Sebastian",
        last_name="Carlos",
        address="24 Rue du moulin, 1400 Nivelles",
        phone_number="0476232323")
    user_test.save()
    first = user_test.delete()
    second = user_test.delete()
    assert len(first) > 0
    assert isinstance(first, list)
    assert len(second) == 0
    assert isinstance(second, list)


def test_save(setup_db):
    user_test = User(
        first_name="Sebastian",
        last_name="Carlos",
        address="24 Rue du moulin, 1400 Nivelles",
        phone_number="0476232323")
    user_test_dup = User(
        first_name="Sebastian",
        last_name="Carlos",
        address="24 Rue du moulin, 1400 Nivelles",
        phone_number="0476232323")
    first = user_test.save()
    second = user_test_dup.save()
    assert isinstance(first, int)
    assert isinstance(second, int)
    assert first > 0
    assert second == -1

