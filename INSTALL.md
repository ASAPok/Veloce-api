# Installation Guide

## Install from PyPI

```bash
pip install veloce-api
```

## Install from source

```bash
git clone https://github.com/yourusername/veloce-api.git
cd veloce-api
pip install -e .
```

## Development Installation

```bash
pip install -e ".[dev]"
```

## Usage in Bot

To use this library in your Telegram bot:

1. Install the library:
```bash
cd G:\app-coding\Veloce\huinya-vpn-pedika
pip install -e G:\app-coding\Veloce\veloce-api
```

2. Update imports in your bot:
```python
from veloce import VeloceClient

client = VeloceClient("https://vpn.unfitshop.ru/api", "api_key")
await client.users.create_free("user123")
```

3. The library will be available globally after installation.

## Verify Installation

```bash
python -c "import veloce; print(f'Veloce API v{veloce.__version__} installed successfully!')"
```
