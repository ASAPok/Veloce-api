# Публикация на PyPI

## Предварительные Требования

1. **Аккаунт на PyPI:**
   - Зарегистрируйся на https://pypi.org/
   - Настрой 2FA (двухфакторную аутентификацию)
   - Создай API token в https://pypi.org/manage/account/token/

2. **Установи инструменты:**
   ```bash
   pip install --upgrade build twine
   ```

## Шаг 1: Подготовка

Проверь что всё корректно:

```bash
cd G:\app-coding\Veloce\veloce-api\Veloce-api

# Проверь версию в pyproject.toml
cat pyproject.toml | findstr version

# Проверь что всё установлено
pip install -e .
python -c "import veloce; print(veloce.__version__)"
```

## Шаг 2: Сборка Пакета

```bash
# Очисти старые сборки
rm -rf build/ dist/ *.egg-info

# Собери пакет
python -m build
```

Это создаст:
- `dist/veloce-api-1.0.0.tar.gz` (source distribution)
- `dist/veloce_api-1.0.0-py3-none-any.whl` (wheel)

## Шаг 3: Проверка Пакета

```bash
# Проверь пакет twine
twine check dist/*
```

Должно показать: `Checking dist/veloce-api-1.0.0.tar.gz: PASSED`

## Шаг 4: Тестовая Публикация (TestPyPI)

Сначала протестируй на TestPyPI:

```bash
# Загрузи на TestPyPI
twine upload --repository testpypi dist/*
```

Введи username: `__token__`
И твой TestPyPI API token

Проверь: https://test.pypi.org/project/veloce-api/

Установи из TestPyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ veloce-api
```

## Шаг 5: Публикация на PyPI

Если всё работает, загружай на настоящий PyPI:

```bash
# Загрузи на PyPI
twine upload dist/*
```

Введи username: `__token__`
И твой PyPI API token

## Шаг 6: Проверка

Проверь на PyPI: https://pypi.org/project/veloce-api/

Установи из PyPI:
```bash
pip install veloce-api
```

Протестируй:
```bash
python -c "from veloce import VeloceClient; print('OK')"
```

## Обновление Версии

Для публикации новой версии:

1. Обнови версию в `pyproject.toml`:
   ```toml
   version = "1.0.1"
   ```

2. Обнови версию в `veloce/__init__.py`:
   ```python
   __version__ = "1.0.1"
   ```

3. Добавь запись в `CHANGELOG.md`

4. Повтори шаги 2-5

## Автоматизация через GitHub Actions

Создай `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

Добавь `PYPI_API_TOKEN` в secrets репозитория.

## Полезные Команды

```bash
# Проверка без загрузки
twine check dist/*

# Удалить версию (нельзя после публикации!)
# Можно только через веб-интерфейс PyPI

# Просмотр информации о пакете
pip show veloce-api

# Установка конкретной версии
pip install veloce-api==1.0.0
```

## Troubleshooting

**Ошибка: "File already exists"**
- Нельзя перезаписать уже опубликованную версию
- Обнови версию и загрузи заново

**Ошибка: "Invalid or non-existent authentication"**
- Проверь API token
- Username должен быть `__token__`, не твоё имя

**Ошибка: "MANIFEST файлы не включены"**
- Проверь `MANIFEST.in`
- Используй `python -m build` вместо `python setup.py sdist`

## После Публикации

1. **Создай GitHub Release:**
   - Tag: `v1.0.0`
   - Title: `Veloce API v1.0.0`
   - Description: Скопируй из CHANGELOG.md

2. **Обнови README badges:**
   ```markdown
   ![PyPI](https://img.shields.io/pypi/v/veloce-api)
   ![Python](https://img.shields.io/pypi/pyversions/veloce-api)
   ![License](https://img.shields.io/pypi/l/veloce-api)
   ```

3. **Объяви в социальных сетях:**
   - Telegram канал
   - Reddit (r/Python)
   - Twitter

## 🔗 Ссылки

- **PyPI**: https://pypi.org/project/veloce-api/
- **Source Code**: https://github.com/ASAPok/veloce-api
- **Issue Tracker**: https://github.com/ASAPok/veloce-api/issues
- **Veloce Panel**: https://github.com/ASAPok/veloce
