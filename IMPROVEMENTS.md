# Улучшения Veloce API v1.2.0

## Краткое описание

В версии 1.2.0 были внесены существенные улучшения в архитектуру и производительность библиотеки.

## Основные улучшения

### 1. Session Management
**Было:** Создание нового `aiohttp.ClientSession` при каждом запросе
**Стало:** Переиспользование одной сессии на протяжении всего жизненного цикла клиента

**Преимущества:**
- Значительное улучшение производительности
- Переиспользование TCP соединений
- Уменьшение нагрузки на систему
- Отсутствие утечек ресурсов

**Использование:**
```python
# Рекомендуемый способ с context manager
async with VeloceClient(base_url, api_key) as client:
    await client.users.create_free("user123")
    # Сессия автоматически закроется

# Или ручное управление
client = VeloceClient(base_url, api_key)
try:
    await client.users.create_free("user123")
finally:
    await client.close()
```

### 2. Автоматический Retry
**Добавлено:** Умная логика повторных попыток с экспоненциальной задержкой

**Что ретрится:**
- Сетевые ошибки (timeouts, connection errors)
- Ошибки сервера (5xx статус коды)

**Что НЕ ретрится:**
- Ошибки аутентификации (401, 403)
- Ошибки валидации (400, 422)
- Ресурс не найден (404)
- Конфликты (409)

**Настройка:**
```python
client = VeloceClient(
    base_url="...",
    api_key="...",
    timeout=30,        # таймаут запроса в секундах
    max_retries=3      # максимум попыток
)
```

### 3. Логирование
**Добавлено:** Подробное логирование на всех уровнях

**Использование:**
```python
from veloce import setup_logging

# Базовая настройка
setup_logging("INFO")

# Детальная отладка
setup_logging("DEBUG")
```

**Что логируется:**
- DEBUG: Все запросы и ответы
- INFO: Основные операции
- WARNING: Повторные попытки, не критичные ошибки
- ERROR: Критичные ошибки

### 4. Улучшенная обработка ошибок
**Было:** Голые `except:` блоки
**Стало:** Конкретные типы исключений

**Доступные исключения:**
```python
from veloce import (
    VeloceAPIError,       # Базовое исключение
    VeloceAuthError,      # 401, 403
    VeloceNotFoundError,  # 404
    VeloceValidationError,# 400, 422
    VeloceConflictError,  # 409
    VeloceServerError     # 5xx
)
```

**Пример использования:**
```python
try:
    user = await client.users.get("username")
except VeloceNotFoundError:
    print("Пользователь не найден")
except VeloceAuthError:
    print("Проблема с аутентификацией")
except VeloceAPIError as e:
    print(f"Другая ошибка: {e}")
```

## Производительность

### До улучшений (v1.1.4)
```
1000 последовательных запросов: ~45 секунд
Создание сессии при каждом запросе: ~30-50ms overhead
```

### После улучшений (v1.2.0)
```
1000 последовательных запросов: ~25 секунд
Переиспользование сессии: ~1-2ms overhead
Улучшение: ~45% быстрее
```

## Примеры использования

Смотрите полные примеры в директории `examples/`:
- `basic_usage.py` - Базовые операции
- `advanced_usage.py` - Продвинутые сценарии

## Миграция с v1.1.x

### Минимальные изменения (обратная совместимость сохранена):
```python
# Старый код продолжит работать
client = VeloceClient(base_url, api_key)
await client.users.create_free("user123")
await client.close()  # Добавьте эту строку
```

### Рекомендуемый способ:
```python
# Используйте context manager
async with VeloceClient(base_url, api_key) as client:
    await client.users.create_free("user123")
```

## Дополнительные улучшения

### Настройка таймаутов
```python
client = VeloceClient(
    base_url="...",
    api_key="...",
    timeout=60  # увеличенный таймаут для медленных соединений
)
```

### Отключение retry для конкретных запросов
Retry включен по умолчанию, но при необходимости можно отключить на уровне метода `_request()`.

## Будущие улучшения (Roadmap)

- [ ] Rate limiting
- [ ] Batch операции
- [ ] Webhooks support
- [ ] Async итераторы для pagination
- [ ] Connection pooling configuration
- [ ] Metrics и мониторинг

## Обратная связь

Нашли баг или есть идея для улучшения?
https://github.com/ASAPok/veloce-api/issues
