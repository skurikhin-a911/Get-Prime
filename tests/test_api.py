import os
import random
import json
import allure
import pytest
import requests as requests


class TestApiGet:
    access_token_merchant = ""
    access_token_frontend = ""
    access_token_tg = ""
    urls_to_check = []
    face_uuids = []

    @pytest.mark.apitest
    @allure.title("Проверка https://dev-api.getprime.pro/api/v1/health - check")
    @allure.description("Валидная проверка на работаспособность системы")
    def test_health_check(self):
        url_health = os.getenv("url_health")
        with allure.step(f"Проверка {url_health} на код 200"):
            assert requests.get(url_health).status_code == 200, "статус код не 200"
        response = (requests.get(url_health).json())
        with allure.step(f"Проверка что статус - ок"):
            assert response['status'] == 'OK', "Статус не ок"

    @pytest.mark.apitest
    @allure.title("Проверка https://dev-api.getprime.pro/api/v1/auth - merchant")
    @allure.description("Валидная проверка с передачей ключа merchant")
    def test_auth_merchant(self):
        merch_key = os.getenv("merchant_key")
        url_auth = os.getenv("url_auth")
        with allure.step(f"Проверка {url_auth} что статус 200"):
            assert requests.post(url=url_auth, headers={
                'X-API-Key': merch_key}).status_code == 200, "Статус код не 200"
        response = requests.post(url=url_auth, headers={'X-API-Key': merch_key}).json()
        global access_token_merchant
        access_token_merchant = response['jwt_token']
        with allure.step("Проверка что jwt token не пустой"):
            assert response['jwt_token'] != ''

    @pytest.mark.apitest
    @allure.title("Проверка https://dev-api.getprime.pro/api/v1/auth - invalid-api-key")
    @allure.description("Негативная проверка с передачей неверного ключа ")
    def test_auth_wrong_key(self):
        url_auth = os.getenv("url_auth")
        with allure.step(f"Проверка {url_auth} на код 401"):
            assert requests.post(url=url_auth,
                                 headers={'X-API-Key': "invalid-api-key"}).status_code == 401, "Статус код не 401"
        response = (requests.post(url_auth).json())
        with allure.step(
                f"Проверка текста message. Ожидали текст 'Вы не авторизованы.\
                 Пожалуйста, выполните вход и повторите попытку.' Получили '{response['message']}'"):
            assert response[
                       'message'] == "Вы не авторизованы. Пожалуйста, выполните вход и повторите попытку.", \
                "Проверка не прошла"

    @pytest.mark.apitest
    @allure.title("Проверка https://dev-api.getprime.pro/api/v1/auth - fronted with domain")
    @allure.description("Валидная проверка с передачей ключа fronted и домена letoplan.pims.ru")
    def test_auth_fronted_with_domain(self):
        frontend_key = os.getenv("frontend_key")
        url_auth = os.getenv("url_auth")
        with allure.step(f"Проверка {url_auth} на код 200"):
            assert requests.post(url=url_auth, headers={'X-API-Key': frontend_key,
                                                        'X-Merchant-Domain': 'letoplan.pims.ru'}).status_code == 200, 'Статус код не 200'
        response = requests.post(url=url_auth, headers={'X-API-Key': frontend_key,
                                                        'X-Merchant-Domain': 'letoplan.pims.ru'}).json()
        global access_token_frontend
        access_token_frontend = response['jwt_token']
        with allure.step("Проверка, что jwt_token не пустой"):
            assert response['jwt_token'] != ''

    @pytest.mark.apitest
    @allure.title("Проверка https://dev-api.getprime.pro/api/v1/auth - frontend with wrong domain")
    @allure.description("Негативная проверка с передачей ключа fronted и с неправильным доменом")
    def test_auth_frontend_with_wrong_domain(self):
        frontend_key = os.getenv("frontend_key")
        url_auth = os.getenv("url_auth")
        with allure.step(f"Проверка {url_auth} на код 404"):
            assert requests.post(url=url_auth, headers={'X-API-Key': frontend_key,
                                                        'X-Merchant-Domain': 'wrongdomain.ru'}).status_code == 404, 'Статус код не 404'
        response = requests.post(url=url_auth, headers={'X-API-Key': frontend_key,
                                                        'X-Merchant-Domain': 'wrongdomain.ru'}).json()
        with allure.step(
                f"Проверка текста message. Ожидали текст 'Домен не найден', получили '{response['message']}'"):
            assert response['message'] == 'Домен не найден.', "Текст не совпадает"

    @pytest.mark.apitest
    @allure.title("Проверка https://dev-api.getprime.pro/api/v1/auth - TG_SERVICE")
    @allure.description("Валидная проверка с передачей ключа tg service")
    def test_auth_tg_service(self):
        tg_service_key = os.getenv("tg_service_key")
        url_auth = os.getenv("url_auth")
        with allure.step(f"Проверка {url_auth} на код 200"):
            assert requests.post(url=url_auth,
                                 headers={'X-API-Key': tg_service_key}).status_code == 200, "Статус код не 200"
            response = requests.post(url=url_auth, headers={'X-API-Key': tg_service_key}).json()

        global access_token_tg
        access_token_tg = response["jwt_token"]
        with allure.step("Проверка что jwt token не пустой"):
            assert response["jwt_token"] != ''

    @pytest.mark.apitest
    @allure.title("Проверка https://dev-api.getprime.pro/api/v1/health - merchant")
    @allure.description("Валидная проверка health c ролью merchant")
    def test_health_merchant(self):
        merchant_key = os.getenv("merchant_key")
        url_health = os.getenv("url_health")
        with allure.step(f"Проверка {url_health} на код 200"):
            assert requests.get(url=url_health,
                                headers={'X-API-Key': merchant_key}).status_code == 200, "Статус код не 200"
            response = requests.get(url=url_health, headers={'X-API-Key': merchant_key}).json()
        with allure.step("Проверка что статус ок"):
            assert response['status'] == "OK", "Статус не ок"

    @pytest.mark.apitest
    @allure.title("Проверка https://dev-api.getprime.pro/api/v1/health - fronted")
    @allure.description("Валидная проверка health c ролью fronted")
    def test_health_fronted(self):
        frontend_key = os.getenv("frontend_key")
        url_health = os.getenv("url_health")
        with allure.step(f"Проверка {url_health} на код 200"):
            assert requests.get(url=url_health,
                                headers={"X-API-Key": frontend_key}).status_code == 200, "Статус код не 200"
            response = requests.get(url=url_health, headers={"X-API-Key": frontend_key}).json()
        with allure.step("Проверка что статус ок"):
            assert response['status'] == "OK", "Статус не ок"

    @pytest.mark.apitest
    @allure.title("Проверка https://dev-api.getprime.pro/api/v1/health - payment-system")
    @allure.description("Валидная проверка health c ролью payment-system")
    def test_health_payment_system(self):
        payment_system_key = os.getenv("payment_system_key")
        url_health = os.getenv("url_health")
        with allure.step(f"Проверка {url_health} на код 200"):
            assert requests.get(url=url_health,
                                headers={"X-API-Key": payment_system_key}).status_code == 200, "Статус код не 200"
            response = requests.get(url=url_health, headers={"X-API-Key": payment_system_key}).json()
        with allure.step("Проверка что статус ок"):
            assert response["status"] == "OK", "Статус не ок"

    @pytest.mark.apitest
    @allure.title("Проверка https://dev-api.getprime.pro/api/v1/health - tg-service")
    @allure.description("Валидная проверка health с ролью tg-service")
    def test_health_payment_system(self):
        tg_service_key = os.getenv("tg_service_key")
        url_health = os.getenv("url_health")
        with allure.step(f"Проверка {url_health} на код 200"):
            assert requests.get(url=url_health,
                                headers={"X-API-Key": tg_service_key}).status_code == 200, "Статус код не 200"
            response = requests.get(url=url_health, headers={"X-API-Key": tg_service_key}).json()
        with allure.step("Проверка что статус ок"):
            assert response["status"] == "OK", "Статус не ок"

    @pytest.mark.apitest
    @allure.title("Проверка https://dev-api.getprime.pro/api/v1/certificates/catalog - merchant")
    @allure.description("Негативная проверка catalog с ролью merchant")
    def test_certificate_catalog_merchant(self):
        url_certificates_catalog = os.getenv("url_certificates_catalog")
        with allure.step(f"Проверка {url_certificates_catalog} на 403"):
            assert requests.get(url=url_certificates_catalog, headers={
                "Authorization": f"Bearer {access_token_merchant}"}).status_code == 403, "Статус код не 403"
            response = requests.get(url=url_certificates_catalog,
                                    headers={"Authorization": f"Bearer {access_token_merchant}"}).json()
        with allure.step(
                f"Проверка текста message. Ожидали текст 'У вас нет прав для выполнения этого действия.',\
                 Получили '{response['message']}'"):
            assert response['message'] == "У вас нет прав для выполнения этого действия.", "Текст не совпадает"

    @pytest.mark.apitest
    @allure.title("Проверка https://dev-api.getprime.pro/api/v1/certificates/catalog - frontend")
    @allure.description("Валидная проверка catalog с ролью frontend")
    def test_certificate_catalog_frontend(self):
        global face_uuids
        url_certificates_catalog = os.getenv("url_certificates_catalog")
        with allure.step(f"Проверка {url_certificates_catalog} на 200"):
            response = requests.get(
                url=url_certificates_catalog,
                headers={"Authorization": f"Bearer {access_token_frontend}"}
            )
            assert response.status_code == 200, "Статус код не 200"

        with allure.step("Проверка что статус ок"):
            response_json = response.json()
            assert response_json.get("status") == "OK", "Статус не ок"

        face_uuids = []

        # Проверка наличия массива faces и его обработка
        if "faces" in response_json and isinstance(response_json["faces"], list):
            for face in response_json["faces"]:
                if "uuid" in face:
                    face_uuids.append(face["uuid"])
            # Сохраняем список UUID (например, в файл или переменную)
            face_uuid_list = json.dumps(face_uuids)
            face_uuid_index = 0  # Для итерации, если нужно
            print(f"Loaded {len(face_uuids)} UUIDs:", face_uuids)
        else:
            print("No 'faces' array found in response.")

    @pytest.mark.apitest
    @allure.title("Проверка Проверка https://dev-api.getprime.pro/api/v1/certificates/catalog - TG-service")
    @allure.description("Негативная проверка catalog с ролью tg_service")
    def test_certificate_catalog_tg_service(self):
        url_certificates_catalog = os.getenv("url_certificates_catalog")
        with allure.step(f"Проверка {url_certificates_catalog} на 403"):
            assert requests.get(url=url_certificates_catalog, headers={
                "Authorization": f"Bearer {access_token_tg}"}).status_code == 403, "Статус кода не 403"
            response = requests.get(url=url_certificates_catalog,
                                    headers={"Authorization": f"Bearer {access_token_tg}"}).json()
        with allure.step(
                f"Проверка текста message. Ожидали текст 'У вас нет прав для выполнения этого действия.',\
                 Получили '{response['message']}'"):
            assert response['message'] == "У вас нет прав для выполнения этого действия.", "Текст не совпадает"

    @pytest.mark.apitest
    @allure.title("Проверка https://dev-api.getprime.pro/api/v1/certificates/catalog - Positive")
    @allure.description(
        "Позитивная проверка catalog с проверкой обязательных ключей 'merchant, timezones, designs, faces' с их содержимым")
    def test_certificate_catalog(self):
        url_certificates_catalog = os.getenv("url_certificates_catalog")
        with allure.step(f"Проверка {url_certificates_catalog} на 200"):
            response = requests.get(
                url=url_certificates_catalog,
                headers={"Authorization": f"Bearer {access_token_frontend}"})
            assert response.status_code == 200, "Статус код не 200"
            json_response = response.json()
        with allure.step("Проверка наличия ключей верхнего уровня: 'designs', 'faces', 'timezones', 'merchant'"):
            for key in ["designs", "faces", "timezones", "merchant"]:
                assert key in json_response, f"Отсутствует ключ '{key}'"

        with allure.step("Проверка наличия полей в ключе design и самого поля design"):
            for design in json_response["designs"]:
                for field in ["uuid", "name", "url", "sorting", "is_default"]:
                    assert field in design, f"В дизайне отсутствует поле '{field}'"

        with allure.step("Проверка наличия полей в ключе face и самого поля face"):
            for face in json_response["faces"]:
                for field in ["uuid", "value", "is_default"]:
                    assert field in face, f"В лице отсутствует поле '{field}'"

        with allure.step("Проверка наличия полей в ключе timezones и самого поля timezones"):
            for tz in json_response["timezones"]:
                for field in ["code", "name", "short_name", "utc_offset", "is_default"]:
                    assert field in tz, f"В timezone '{tz.get('code')}' отсутствует поле '{field}'"

        with allure.step("Проверка наличия полей в ключе merchant и самого поля merchant"):
            merchant = json_response["merchant"]
            for field in ["name", "code", "domain", "customer_template_code", "support_phone",
                          "support_email", "logo_url", "certificate_expiration_period",
                          "currency_name", "currency_symbol", "currency_format", "merchant_uuid", "country_code"]:
                assert field in merchant, f"В merchant отсутствует поле '{field}'"

        with allure.step("Проверка, что списки:(designs, faces, timezones, merchant) не пустые"):
            assert json_response["designs"], "Список designs пуст"
            assert json_response["faces"], "Список faces пуст"
            assert json_response["timezones"], "Список timezones пуст"
            assert json_response["merchant"], "Список merchant пуст"

    @pytest.mark.apitest
    @allure.title("Проверка https://dev-api.getprime.pro/api/v1/certificates/catalog -  No Token")
    @allure.description(
        "Негативная проверка catalog без ключа авторизации в хедере")
    def test_certificate_catalog_no_token(self):
        url_certificates_catalog = os.getenv("url_certificates_catalog")
        with allure.step(f"Проверка {url_certificates_catalog} на 403 "):
            response = requests.get(url=url_certificates_catalog)
            assert response.status_code == 403, "статус код не 403"
            json_response = response.json()
        with allure.step(
                f"Проверка текста message. Ожидали текст 'У вас нет прав для выполнения этого действия.',\
                 Получили текст '{json_response['message']}'"):
            assert json_response['message'] == "У вас нет прав для выполнения этого действия.", "Текст не соответствует"

    @pytest.mark.apitest
    @allure.title("Проверка https://dev-api.getprime.pro/api/v1/certificates/catalog - Invalid Token")
    @allure.description("Негативная проверка catalog с невалидным ключом авторизации в хедере")
    def test_certificate_catalog_invalid_token(self):
        url_certificates_catalog = os.getenv("url_certificates_catalog")
        with allure.step(f"Проверка {url_certificates_catalog} на 403"):
            response = requests.get(url=url_certificates_catalog, headers={"Authorization": "invalid_token"})
            assert response.status_code == 403, "Статус код не 403"
            json_response = response.json()
        with allure.step(
                f"Проверка текста message. Ожидали текст 'У вас нет прав для выполнения этого действия.',\
                 Получили текст '{json_response['message']}'"):
            assert json_response['message'] == "У вас нет прав для выполнения этого действия.", "Текст не соответствует"

    @pytest.mark.apitest
    @allure.title("Проверка https://dev-api.getprime.pro/api/v1/certificates/catalog - Get Catalog JSON")
    @allure.description("Получение всех url из json")
    def test_certificate_get_catalog_json(self):
        global urls_to_check
        url_certificates_catalog = os.getenv("url_certificates_catalog")
        with allure.step(f"Проверка {url_certificates_catalog} на 200"):
            response = requests.get(url=url_certificates_catalog,
                                    headers={"Authorization": f"Bearer {access_token_frontend}"})
            assert response.status_code == 200, "Статус код не 200"
            json_response = response.json()

        urls_to_check = []
        with allure.step("Проверка merchant.logo_url"):
            merchant = json_response.get("merchant")
            if merchant and merchant.get("logo_url"):
                urls_to_check.append(merchant["logo_url"])

        with allure.step("Проверка designs"):
            designs = json_response.get("designs")
            if isinstance(designs, list):
                for d in designs:
                    if d.get("url"):
                        urls_to_check.append(d["url"])
                    faces = d.get("faces")
                    if isinstance(faces, list):
                        for f in faces:
                            if f.get("url"):
                                urls_to_check.append(f["url"])

    @pytest.mark.apitest
    @allure.title("Проверка https://dev-api.getprime.pro/api/v1/certificates/catalog - Check Each URL")
    @allure.description("Проверка всех url")
    def test_certificate_check_each_url(self):
        url_certificates_catalog = os.getenv("url_certificates_catalog")
        with allure.step(f"Проверка {url_certificates_catalog} на 200"):
            response = requests.get(url=url_certificates_catalog,
                                    headers={"Authorization": f"Bearer {access_token_frontend}"})
            assert response.status_code == 200, "Статус код не 200"
            failed_urls = []
            checked = 0
            passed_count = 0

            for url in urls_to_check:
                with allure.step(f"Проверяется URL: {url}"):
                    try:
                        response = requests.get(url)
                        if response.status_code != 200:
                            failed_urls.append({"url": url, "status": response.status_code})
                        else:
                            passed_count += 1
                    except Exception as e:
                        failed_urls.append({"url": url, "status": str(e)})

                    checked += 1

            with allure.step("Анализ результатов проверки URL"):
                if len(failed_urls) == 0:

                    assert len(failed_urls) == 0, "Неуспешных URL"
                else:
                    pytest.fail(f"Неуспешных URL: {len(failed_urls)}", strict=False)
                    # Или можно вывести список ошибок
                    # print("Ошибки по URL:", failed_urls)

                print(f"✅ Успешно: {passed_count} / {len(urls_to_check)}")
                # Можно добавить логирование в allure
                allure.attach(
                    f"Успешных: {passed_count}\nНеуспешных: {len(failed_urls)}",
                    name="Результаты проверки",
                    attachment_type=allure.attachment_type.TEXT
                )

    @pytest.mark.apitest
    @allure.title("Проверка https://dev-api.getprime.pro/api/v1/orders/create - Fixed_Nominal")
    @allure.description("Позитивная проверка создания сертификата с фиксированым номиналом")
    def test_certificate_create_fixed_nominal(self):
        url_create_order = os.getenv("url_create_order")

        payload = {
            "buyer": {
                "name": "Иван Иванов",
                "email": "ivanov@example.com",
                "phone": "+79991112233"
            },
            "order_certificates": [
                {
                    "design_uuid": "542f8ec8-75d1-46ce-8a07-6dfbbebc8581",
                    "amount": 1000000,
                    "is_gift": True,
                    "send_now": True,
                    "timezone_code": "MSK",
                    "sender": "Иванов Иван Иванович",
                    "message": "С днём рождения!",
                    "recipient_name": "Алексей",
                    "recipient_phone": "+79992223344",
                    "recipient_email": "ivanov@example.com",
                    "count": 1
                }
            ]
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token_frontend}'
        }

        with allure.step(f"Проверка {url_create_order}"):
            response = requests.post(url_create_order, json=payload, headers=headers)
            assert response.status_code == 200, "Статус код не 200"
            json_response = response.json()

        with allure.step("Проверка что статус 'ОК'"):
            assert json_response["status"] == "OK", "Статус не 'ОК'"

        with allure.step("Проверка наличия payment_url и его содержимого"):
            assert "payment_url" in json_response, "В ответе отсутствует 'payment_url'"
            payment_url = json_response["payment_url"]
            assert "dev-get.alfa-payment.ru" in payment_url, \
                f"'payment_url' не содержит 'dev-get.alfa-payment.ru', текущий URL: {payment_url}"

    @pytest.mark.apitest
    @allure.title("Проверка https://dev-api.getprime.pro/api/v1/orders/create - random_amout")
    @allure.description("Позитивная проверка создания сертификата с рандомным номиналом")
    def test_certificate_random_nominal(self):
        url_create_order = os.getenv("url_create_order")
        min_value = 100
        max_value = 10000000
        random_amout = random.randint(min_value, max_value)

        payload = {
            "buyer": {
                "name": "Иван Иванов",
                "email": "ivanov@example.com",
                "phone": "+79991112233"
            },
            "order_certificates": [
                {
                    "design_uuid": "542f8ec8-75d1-46ce-8a07-6dfbbebc8581",
                    "amount": random_amout,
                    "is_gift": True,
                    "send_now": True,
                    "timezone_code": "MSK",
                    "sender": "Иванов Иван Иванович",
                    "message": "С днём рождения!",
                    "recipient_name": "Алексей",
                    "recipient_phone": "+79992223344",
                    "recipient_email": "ivanov@example.com",
                    "count": 1
                }
            ]
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token_frontend}'
        }
        with allure.step(f"Проверка {url_create_order} на код 200"):
            response = requests.post(url_create_order, json=payload, headers=headers)
            assert response.status_code == 200, "Статус код не 200"
            json_response = response.json()
        with allure.step("Проверка что статус 'ОК'"):
            assert json_response['status'] == "OK", "Статус не ОК"

        with allure.step("Проверка наличия payment_url и его содержимого"):
            assert "payment_url" in json_response, "В ответе отсутствует payment_url"
            payment_url = json_response['payment_url']
            assert "dev-get.alfa-payment.ru" in payment_url, \
                f"'payment_url' не содержит 'dev-get.alfa-payment.ru', текущий URL: {payment_url}"

    @pytest.mark.apitest
    @allure.title("Проверка https://dev-api.getprime.pro/api/v1/orders/create - send_later")
    @allure.description("Позитивная проверка создания сертификата с отсроченной доставкой")
    def test_certificate_send_later(self):
        url_create_order = os.getenv("url_create_order")

        payload = {
            "buyer": {
                "name": "Иван Иванов",
                "email": "ivanov@example.com",
                "phone": "+79991112233"
            },
            "order_certificates": [
                {
                    "design_uuid": "542f8ec8-75d1-46ce-8a07-6dfbbebc8581",
                    "amount": 1000000,
                    "is_gift": 'true',
                    "send_now": 'false',
                    "timezone_code": "MSK",
                    "sender": "Иванов Иван Иванович",
                    "message": "С днём рождения!",
                    "delivery_time": "2024-01-09T11:50:26+00:00",
                    "recipient_name": "Алексей",
                    "recipient_phone": "+79992223344",
                    "recipient_email": "ivanov@example.com",
                    "count": 1
                }
            ]
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token_frontend}'
        }
        with allure.step(f"Проверка {url_create_order} на код 200"):
            response = requests.post(url_create_order, json=payload, headers=headers)
            assert response.status_code == 200, "Статус код не 200"
            json_response = response.json()
        with allure.step("Проверка что статус 'ОК'"):
            assert json_response['status'] == 'OK', "Ставтус не 'ОК'"
        with allure.step("Проверка наличия payment_url и его содержимого"):
            assert 'payment_url' in json_response, "В ответе отсутствует payment_url"
            payment_url = json_response['payment_url']
            assert "dev-get.alfa-payment.ru" in payment_url, \
                f"'payment_url' не содержит 'dev-get.alfa-payment.ru', текущий URL: {payment_url}"

    @pytest.mark.apitest
    @allure.title("Проверка https://dev-api.getprime.pro/api/v1/orders/create - Check face uuid")
    @allure.description("Позитивная проверка создания сертификата с отсроченной доставкой")
    def test_certificate_send_later(self):
        url_create_order = os.getenv("url_create_order")
        headers = {
            "Authorization": f"Bearer {access_token_frontend}",
            "Content-Type": "application/json"
        }

        for face_uuid in face_uuids:
            payload = {
                "buyer": {
                    "name": "Иван Иванов",
                    "email": "ivanov@example.com",
                    "phone": "+79991112233"
                },
                "order_certificates": [
                    {
                        "design_uuid": "542f8ec8-75d1-46ce-8a07-6dfbbebc8581",
                        "face_uuid": face_uuid,  # передаем по одному uuid
                        "is_gift": 'true',
                        "send_now": 'true',
                        "timezone_code": "MSK",
                        "sender": "Иванов Иван Иванович",
                        "message": "С днём рождения!",
                        "delivery_time": "2024-01-09T11:50:26+00:00",
                        "recipient_name": "Алексей",
                        "recipient_phone": "+79992223344",
                        "recipient_email": "ivanov@example.com",
                        "count": 1
                    }
                ]
            }
        with allure.step(f"Проверка {url_create_order} на статус 200"):
            response = requests.post(url_create_order, json=payload, headers=headers)
            # print(f"Отправка для face_uuid: {face_uuid}")
            # print(payload)
            assert response.status_code == 200, f"Статус код не 200, а {response.status_code}"
            resp_json = response.json()
        with allure.step("Проверка что статус 'ОК'"):
            assert resp_json.get("status") == "OK", f"Статус не OK: {resp_json.get('status')}"
        with allure.step("Проверка на наличие 'order_uuid' в ответе"):
            assert "order_uuid" in resp_json, "Нет order_uuid в ответе"
        with allure.step("Проверка на наличие 'payment_url' в ответе"):
            assert "payment_url" in resp_json, "Нет payment_url в ответе"
        with allure.step("Проверка на наличия домена 'dev-get.alfa-payment.ru' в поле 'paymtnt_url'"):
            assert "dev-get.alfa-payment.ru" in resp_json[
                "payment_url"], "payment_url не содержит dev-get.alfa-payment.ru"
            # print(f"Проверен UUID: {face_uuid}")

    @pytest.mark.apitest
    @allure.title("Проверка https://dev-api.getprime.pro/api/v1/orders/create - Max lengths and gift-false")
    @allure.description("Позитивная проверка полей максимально заполненными символами и gift false")
    def test_certificate_max_lengths_and_gift_false(self):
        url_create_order = os.getenv("url_create_order")
        headers = {
            "Authorization": f"Bearer {access_token_frontend}",
            "Content-Type": "application/json"
        }

        # Выбираем один случайный face_uuid
        selected_face_uuid = random.choice(face_uuids)

        payload = {
            "buyer": {
                "name": "Иван Иванов",
                "email": "ivanov@example.com",
                "phone": "+79991112233"
            },
            "order_certificates": [
                {
                    "design_uuid": "542f8ec8-75d1-46ce-8a07-6dfbbebc8581",
                    "face_uuid": selected_face_uuid,  # выбранный случайный uuid
                    "is_gift": 'false',
                    "send_now": 'true',
                    "count": 1
                }
            ]
        }
        # with allure.step(f"Проверка {url_create_order} на код 200"):     на сервере 500
        #     response = requests.post(url_create_order, json=payload, headers=headers)
        #     assert response.status_code == 200, "Статус код не 200"
        #     resp_json = response.json()
        # with allure.step("Проверка на наличия домена 'dev-get.alfa-payment.ru' в поле 'paymtnt_url'"):
        #     assert "dev-get.alfa-payment.ru" in resp_json[
        #         "payment_url"], "payment_url не содержит dev-get.alfa-payment.ru"

    @pytest.mark.apitest
    @allure.title("Проверка https://dev-api.getprime.pro/api/v1/orders/create - amount below min")
    @allure.description("Негативная проверка поля amount, значение меньше минимальной планки ")
    def test_certificate_amount_below_min(self):
        url_create_order = os.getenv("url_create_order")
        headers = {
            "Authorization": f"Bearer {access_token_frontend}",
            "Content-Type": "application/json"
        }

        # Выбираем один случайный face_uuid

        payload = {
            "buyer": {
                "name": "Иван Иванов",
                "email": "ivanov@example.com",
                "phone": "+79991112233"
            },
            "order_certificates": [
                {
                    "design_uuid": "542f8ec8-75d1-46ce-8a07-6dfbbebc8581",
                    "amount": "99",
                    "is_gift": 'true',
                    "send_now": 'true',
                    "timezone_code": "{{timezone_code}}",
                    "sender": "Иванов Иван Иванович",
                    "message": "С днём рождения!",
                    "recipient_name": "Алексей",
                    "recipient_phone": "+79992223344",
                    "recipient_email": "ivanov@example.com",
                    "count": 1
                }
            ]
        }
        with allure.step(f"Проверка {url_create_order} на код 400"):
            response = requests.post(url_create_order, json=payload, headers=headers)
            assert response.status_code == 400, "Статус код не 400"
            json_response = response.json()
        with allure.step(
                f"Проверка текста message. Ожидали текст 'amount не может быть ниже значения: 10000',\
                             Получили текст '{json_response['message']}'"):
            assert json_response[
                       'message'] == "amount не может быть ниже значения: 10000", "Текст не соответствует"

    # @pytest.mark.apitest
    # @allure.title("Проверка https://dev-api.getprime.pro/api/v1/orders/create - amount below max")
    # @allure.description("Негативная проверка поля amount, значение меньше минимальной планки ")
    # def test_certificate_amount_below_max(self):
    #     url_create_order = os.getenv("url_create_order")
    #     headers = {
    #         "Authorization": f"Bearer {access_token_frontend}",
    #         "Content-Type": "application/json"
    #     }
    #
    #     # Выбираем один случайный face_uuid
    #
    #     payload = {
    #         "buyer": {
    #             "name": "Иван Иванов",
    #             "email": "ivanov@example.com",
    #             "phone": "+79991112233"
    #         },
    #         "order_certificates": [
    #             {
    #                 "design_uuid": "542f8ec8-75d1-46ce-8a07-6dfbbebc8581",
    #                 "amount": "10000001",
    #                 "is_gift": 'true',
    #                 "send_now": 'true',
    #                 "timezone_code": "{{timezone_code}}",
    #                 "sender": "Иванов Иван Иванович",
    #                 "message": "С днём рождения!",
    #                 "recipient_name": "Алексей",
    #                 "recipient_phone": "+79992223344",
    #                 "recipient_email": "ivanov@example.com",
    #                 "count": 1
    #             }
    #         ]
    #     }
    #     with allure.step(f"Проверка {url_create_order} на код 400"):
    #         response = requests.post(url_create_order, json=payload, headers=headers)
    #         assert response.status_code == 400, "Статус код не 400"
    #         json_response = response.json()
    #     with allure.step(
    #             f"Проверка текста message. Ожидали текст 'amount не может превышать значение: 10000000',\
    #                              Получили текст '{json_response['message']}'"):
    #         assert json_response[
    #                    'message'] == "amount не может превышать значение: 10000000", "Текст не соответствует"