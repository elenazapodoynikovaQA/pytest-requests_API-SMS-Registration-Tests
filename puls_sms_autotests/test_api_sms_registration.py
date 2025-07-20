import requests

BASE_URL = "https://upjet-back.dev.sandakov.space"
REGISTER_URL = f"{BASE_URL}/api/auth/register"
CONFIRM_URL = f"{BASE_URL}/api/auth/verify/phone/confirm"
COMPLETE_URL = f"{BASE_URL}/api/auth/register/complete"
LOGIN_URL = f"{BASE_URL}/api/auth/login"

# 1. Регистрация от начала до конца
def test_sms_registration_flow(registered_user):
    print(f"\n Регистрируем нового пользователя:")
    print(f"   Телефон: {registered_user['phone']}")
    print(f"   Email: {registered_user['email']}")

# Шаг 1 — отправка формы
    user_data = {
        "first_name": "Катя",
        "last_name": "К",
        "phone": registered_user["phone"],
        "email": registered_user["email"],
        "password": registered_user["password"],
        "password_confirmation": registered_user["password"]
    }

    response = requests.post(REGISTER_URL, json=user_data)
    assert response.status_code == 200
    token = response.json()["data"]
    print(f"   Получен промежуточный токен: {token[:30]}...")

# Шаг 2 — подтверждение СМС
    sms_payload = {
        "phone": registered_user["phone"],
        "code": "54321"
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    confirm_response = requests.post(CONFIRM_URL, json=sms_payload, headers=headers)
    assert confirm_response.status_code == 200
    assert confirm_response.json()["status"] == "success"
    print("   Подтверждение СМС прошло успешно")

# Шаг 3 — завершение регистрации
    complete_payload = {
        "date_of_birth": "1982-07-08T00:00:00+11:00",
        "country_id": 177,
        "city_id": 6711,
        "gender": "female"
    }

    complete_response = requests.post(COMPLETE_URL, json=complete_payload, headers=headers)
    assert complete_response.status_code == 200
    assert complete_response.json()["status"] == "success"
    print("   Регистрация завершена успешно!\n")


#  2. Повторная регистрация → 422
def test_duplicate_registration_returns_422(registered_user):
    print(f"\n Повторная регистрация с email: {registered_user['email']}")

    user_data = {
        "first_name": "Катя",
        "last_name": "Копия",
        "phone": registered_user["phone"],
        "email": registered_user["email"],
        "password": registered_user["password"],
        "password_confirmation": registered_user["password"]
    }

    response = requests.post(REGISTER_URL, json=user_data)
    print(f"   Ответ: {response.status_code}")
    print(f"   Тело: {response.json()}")

    assert response.status_code == 422
    print("   Повторная регистрация отклонена\n")


#  3. Успешный вход
def test_login_with_valid_phone_and_password(registered_user):
    print(f"\n Вход по телефону: {registered_user['phone']}")

    payload = {
        "phone": registered_user["phone"],
        "password": registered_user["password"]
    }

    response = requests.post(LOGIN_URL, json=payload)
    print(f"   Ответ от login: {response.status_code}, {response.json()}")

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    print("   Вход успешен\n")


#  4. Ошибка при неверном телефоне
def test_login_with_invalid_phone_and_valid_password(registered_user):
    fake_phone = "79998887766"
    print(f"\n Вход с фейковым телефоном: {fake_phone}")

    payload = {
        "phone": fake_phone,
        "password": registered_user["password"]
    }

    response = requests.post(LOGIN_URL, json=payload)
    print(f"   Ответ: {response.status_code}, тело: {response.json()}")

    assert response.status_code == 401
    print("   Логин с неверным телефоном корректно отклонён\n")
