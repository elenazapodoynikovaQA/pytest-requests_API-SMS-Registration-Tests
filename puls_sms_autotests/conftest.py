import pytest
import time

def generate_unique_phone():
    timestamp = int(time.time())
    return f"7962{timestamp % 1000000:06d}"

def generate_unique_email():
    timestamp = int(time.time())
    return f"katya{timestamp}@mail.ru"

@pytest.fixture(scope="module")
def registered_user():
    return {
        "phone": generate_unique_phone(),
        "email": generate_unique_email(),
        "password": "Zap83wer%%"
    }
