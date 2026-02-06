# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-02-06

### Added
- Context manager support for automatic session cleanup (`async with VeloceClient()`)
- Persistent HTTP session management for improved performance
- Automatic retry logic with exponential backoff for network errors
- Comprehensive logging support throughout the library
- `setup_logging()` utility function for easy logging configuration
- Timeout configuration option (default: 30 seconds)
- Max retries configuration option (default: 3 attempts)
- Example scripts in `examples/` directory

### Improved
- Better error handling with specific exception types
- All bare `except` blocks replaced with specific exception handling
- Enhanced type hints coverage
- More detailed debug logging for requests and responses
- Retry logic for server errors (5xx) and network failures
- Session is now shared across all requests instead of creating new sessions

### Fixed
- Session leaks from creating new `ClientSession` on every request
- Improved JSON parsing error handling
- Better exception propagation in user API methods

### Changed
- `VeloceClient.__init__()` now accepts `timeout` and `max_retries` parameters
- All API errors now properly logged with appropriate log levels
- `_request()` method now uses persistent session

## [1.1.4] - 2026-01-31

### Fixed
- Reverted `proxies` payload to use empty dict `{"vless": {}}` instead of passing empty string flow
- `flow=""` may cause validation errors if backend expects Enum value or no field

## [1.1.3] - 2026-01-31

### Fixed
- `create_free()` now properly checks if user exists before deciding to create or update
- Previously it blindly tried update after failed create, causing 404 errors

## [1.1.2] - 2026-01-31

### Fixed
- `create_free()` was sending invalid `status="free"` to API (API only accepts "active" or "on_hold")
- Changed to `status="active"` - Free Tier is determined by `expire=1`, not by status field

## [1.0.0] - 2026-01-25

### Added
- Initial release
- Complete API coverage for Veloce Panel
- User management (CRUD, free/paid tiers, subscriptions)
- Admin operations (authentication, management)
- Node management (CRUD, usage stats)
- System operations (stats, inbounds, core control)
- Inbound configuration management
- Core statistics and control
- API keys management
- Pydantic models for type safety
- Retry logic with exponential backoff
- Custom exception classes
- Async/await support throughout
- Comprehensive documentation

### Features
- Lazy-loaded API modules for better performance
- Type hints for IDE autocomplete
- Error handling with descriptive exceptions
- Free tier and paid tier user support
- Automatic inbound switching based on subscription status
