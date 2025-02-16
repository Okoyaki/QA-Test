import requests
import random

BASE_URL = "https://qa-internship.avito.com/api/1"

# Генерируем уникальный sellerID
seller_id = random.randint(111111, 999999)


def test_create_item():
    """Тест создания объявления"""
    payload = {
        "title": "test",
        "description": "test",
        "price": 1000,
        "sellerId": seller_id
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(f"{BASE_URL}/item", json=payload, headers=headers)
    
    assert response.status_code == 200, f"Ошибка: {response.text}"
    
    json_data = response.json()

    global item_id
    item_id = json_data['status'].split()[-1]


def test_get_item_by_id():
    """Тест получения объявления по ID"""
    response = requests.get(f"{BASE_URL}/item/{item_id}")
    
    assert response.status_code == 200, f"Ошибка: {response.text}"
    
    json_data = response.json()[0]

    assert json_data["id"] == item_id, "ID в ответе не совпадает с ожидаемым"
    assert json_data["sellerId"] == seller_id, "sellerId в ответе не совпадает с ожидаемым"


def test_get_items_by_seller():
    """Тест получения всех объявлений по sellerID"""
    response = requests.get(f"{BASE_URL}/{seller_id}/item")
    
    assert response.status_code == 200, f"Ошибка: {response.text}"
    
    json_data = response.json()[0]
    print(json_data)
    assert isinstance(json_data, dict), "Ответ должен быть словарем"
    assert json_data["name"] == item_id, "Созданное объявление не найдено в словаре"


def test_get_item_statistics():
    """Тест получения статистики по объявлению"""
    response = requests.get(f"{BASE_URL}/statistic/{item_id}")
    
    assert response.status_code == 200, f"Ошибка: {response.text}"
    
    json_data = response.json()[0]
    print(json_data)
    assert "viewCount" in json_data, "Ответ не содержит поле 'views'"
    assert isinstance(json_data["viewCount"], int), "Поле 'views' должно быть числом"