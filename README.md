# Veloce API - Python Client Library

[![PyPI version](https://img.shields.io/pypi/v/veloce-api.svg)](https://pypi.org/project/veloce-api/)
[![Python versions](https://img.shields.io/pypi/pyversions/veloce-api.svg)](https://pypi.org/project/veloce-api/)
[![License](https://img.shields.io/pypi/l/veloce-api.svg)](https://pypi.org/project/veloce-api/)
[![Downloads](https://pepy.tech/badge/veloce-api)](https://pepy.tech/project/veloce-api)

**English** | **[Русский](README_RU.md)**

Official Python client library for [Veloce VPN Panel](https://github.com/yourusername/veloce) management API.

## ✨ Features

- 🚀 **Complete API Coverage** - All Veloce Panel endpoints
- 🔄 **Async/Await** - Full asynchronous support
- 🛡️ **Type Safe** - Pydantic models and type hints
- 🔁 **Auto Retry** - Exponential backoff on failures
- 🎯 **Easy to Use** - Intuitive API design
- 📦 **Free & Paid Tiers** - Automatic tier management
- 🔑 **API Key Auth** - Secure authentication
- 📊 **Comprehensive** - Users, nodes, system, inbounds, and more

## 📦 Installation

```bash
pip install veloce-api
```

## 🚀 Quick Start

```python
from veloce import VeloceClient

# Initialize client
client = VeloceClient(
    base_url="https://your-panel.com/api",
    api_key="your_api_key"
)

# Create free tier user
url = await client.users.create_free("username123")
print(f"Subscription URL: {url}")

# Extend subscription
await client.users.extend_subscription("username123", days=30)

# Get user info
user = await client.users.get("username123")
print(f"Status: {user['status']}, Expire: {user['expire']}")
```

## 📚 API Modules

### Users (`client.users`)
Complete user management with free/paid tier support:
```python
# Create users
await client.users.create_free("user123")
await client.users.create_paid("user456", days=30)

# Manage subscriptions
await client.users.extend_subscription("user123", days=30)
await client.users.get_subscription_url("user123")

# User operations
await client.users.list(offset=0, limit=10, status="active")
await client.users.ban("user123")
await client.users.reset_traffic("user123")
```

### System (`client.system`)
System statistics and operations:
```python
# Get stats
stats = await client.system.get_stats()
print(f"Total users: {stats['total_user']}")
print(f"Active: {stats['users_active']}")

# Manage core
await client.system.restart_core()
config = await client.system.get_core_config()
```

### Nodes (`client.nodes`)
Node management:
```python
# List nodes
nodes = await client.nodes.list()

# Node operations
await client.nodes.create(node_data)
await client.nodes.update(node_id, node_data)
await client.nodes.reconnect(node_id)
```

### Admin (`client.admin`)
Admin operations:
```python
# Authentication
token = await client.admin.login("username", "password")

# Management
await client.admin.create("newadmin", "password", is_sudo=True)
await client.admin.delete("oldadmin")
```

### And More!
- **Inbounds** (`client.inbounds`) - Inbound configuration
- **Core** (`client.core`) - Core statistics and control
- **API Keys** (`client.api_keys`) - API key management

## 🔧 Advanced Usage

### Error Handling
```python
from veloce.exceptions import VeloceNotFoundError, VeloceAuthError

try:
    user = await client.users.get("nonexistent")
except VeloceNotFoundError:
    print("User not found")
except VeloceAuthError:
    print("Invalid API key")
```

### Type Safety with Pydantic
```python
from veloce.models import UserResponse

user = await client.users.get("user123")
# user is typed as Dict, or use Pydantic model:
user_model = UserResponse(**user)
print(user_model.username)
```

### Custom Retry Configuration
```python
from veloce.retry import retry_on_error

@retry_on_error(max_retries=5, base_delay=2.0)
async def robust_operation():
    return await client.users.get("user123")
```

## 📖 Documentation

- [Installation Guide](INSTALL.md)
- [Publishing to PyPI](PUBLISHING.md)
- [Changelog](CHANGELOG.md)
- [Full API Documentation](https://veloce-api.readthedocs.io)

## 💻 Development

```bash
# Clone repository
git clone https://github.com/yourusername/veloce-api.git
cd veloce-api

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Type checking
mypy veloce

# Format code
black veloce
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **PyPI**: https://pypi.org/project/veloce-api/
- **Documentation**: https://veloce-api.readthedocs.io
- **Source Code**: https://github.com/yourusername/veloce-api
- **Issue Tracker**: https://github.com/yourusername/veloce-api/issues
- **Veloce Panel**: https://github.com/yourusername/veloce

## 🌟 Support

If you find this project useful, please give it a ⭐️!

For questions and support, please [open an issue](https://github.com/yourusername/veloce-api/issues).
