# TRON API

Этот проект предоставляет API для работы с кошельками TRON.

## Запуск тестов
Для запуска тестов выполните команду в корневой папке:
```sh
pytest
```

## Основные эндпоинты

### Получение информации о кошельке
**POST** `localhost:8000/tron/wallet_info`

**Тело запроса (JSON):**
```json
{
    "address": "..."
}
```

**Пример использования (cURL):**
```sh
curl -X POST "http://localhost:8000/tron/wallet_info" \
     -H "Content-Type: application/json" \
     -d '{"address": "TXYZ..."}'
```

---

### Получение логов кошелька
**GET** `localhost:8000/tron/wallet_logs?skip=0&limit=10`

**Пример использования (cURL):**
```sh
curl -X GET "http://localhost:8000/tron/wallet_logs?skip=0&limit=10"
```

## Установка и запуск
1. Убедитесь, что у вас установлен Python и зависимости.
2. Запустите сервер командой:
   ```sh
   uvicorn main:app --reload
   ```
3. API будет доступно по адресу `http://localhost:8000`. 

---

## Структура `.env` файла
Создайте файл `.env` в корневой директории и добавьте следующие переменные окружения:
```ini
DB_HOST=
DB_PORT=
DB_USER=
DB_PASSWORD=
DB_NAME=

TRON_API_KEY=
TRON_ADDRESS=
```

---

