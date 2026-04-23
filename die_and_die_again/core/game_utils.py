
from faker import Faker


fake = Faker()


def random_first_name(gender: str = None) -> str:
    """
    Generate a random first name.

    :param gender: 'male', 'female', or None for any
    :return: name string
    """
    if gender is None:
        return fake.first_name()

    gender = gender.lower()

    if gender == "male":
        return fake.first_name_male()
    elif gender == "female":
        return fake.first_name_female()
    else:
        raise ValueError("gender must be 'male', 'female', or None")

