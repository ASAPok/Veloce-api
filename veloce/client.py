"""
Main Veloce API Client
"""

import aiohttp
import asyncio
import logging
from typing import Dict, Any, Optional, Tuple

from .exceptions import (
    VeloceAPIError,
    VeloceAuthError,
    VeloceNotFoundError,
    VeloceValidationError,
    VeloceConflictError,
    VeloceServerError
)


logger = logging.getLogger(__name__)


class VeloceClient:
    """
    Main client for Veloce Panel API

    Usage with context manager (recommended):
        >>> async with VeloceClient("https://panel.com/api", "api_key") as client:
        ...     await client.users.create_free("user123")
        ...     await client.nodes.list()

    Or manual session management:
        >>> client = VeloceClient("https://panel.com/api", "api_key")
        >>> await client.users.create_free("user123")
        >>> await client.close()
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: int = 30,
        max_retries: int = 3
    ):
        """
        Initialize Veloce API client

        Args:
            base_url: Base URL of panel (e.g. https://panel.com/api)
            api_key: API key for authentication
            timeout: Request timeout in seconds (default: 30)
            max_retries: Maximum number of retry attempts (default: 3)
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.max_retries = max_retries

        # Session management
        self._session: Optional[aiohttp.ClientSession] = None
        self._owns_session = True

        # Lazy load API modules
        self._users_api = None
        self._admin_api = None
        self._nodes_api = None
        self._inbounds_api = None
        self._system_api = None
        self._api_keys_api = None
        self._core_api = None

    async def __aenter__(self):
        """Context manager entry"""
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        await self.close()

    async def _ensure_session(self) -> aiohttp.ClientSession:
        """Ensure aiohttp session exists"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(timeout=self.timeout)
            self._owns_session = True
        return self._session

    async def close(self):
        """Close aiohttp session"""
        if self._session and not self._session.closed and self._owns_session:
            await self._session.close()
            self._session = None
    
    @property
    def users(self):
        """User management API"""
        if self._users_api is None:
            from .api.users import UsersAPI
            self._users_api = UsersAPI(self)
        return self._users_api
    
    @property
    def admin(self):
        """Admin operations API"""
        if self._admin_api is None:
            from .api.admin import AdminAPI
            self._admin_api = AdminAPI(self)
        return self._admin_api
    
    @property
    def nodes(self):
        """Node management API"""
        if self._nodes_api is None:
            from .api.nodes import NodesAPI
            self._nodes_api = NodesAPI(self)
        return self._nodes_api
    
    @property
    def inbounds(self):
        """Inbound configuration API"""
        if self._inbounds_api is None:
            from .api.inbounds import InboundsAPI
            self._inbounds_api = InboundsAPI(self)
        return self._inbounds_api
    
    @property
    def system(self):
        """System information API"""
        if self._system_api is None:
            from .api.system import SystemAPI
            self._system_api = SystemAPI(self)
        return self._system_api
    
    @property
    def api_keys(self):
        """API keys management"""
        if self._api_keys_api is None:
            from .api.api_keys import APIKeysAPI
            self._api_keys_api = APIKeysAPI(self)
        return self._api_keys_api
    
    @property
    def core(self):
        """Core statistics API"""
        if self._core_api is None:
            from .api.core import CoreAPI
            self._core_api = CoreAPI(self)
        return self._core_api
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with API key"""
        return {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        retry: bool = True
    ) -> Tuple[int, Dict[str, Any]]:
        """
        Make HTTP request to API with automatic retry logic

        Args:
            method: HTTP method
            endpoint: API endpoint
            json_data: JSON body
            params: Query parameters
            retry: Enable retry logic for transient errors

        Returns:
            Tuple of (status_code, response_data)

        Raises:
            VeloceAPIError: On API errors
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()
        session = await self._ensure_session()

        last_exception = None
        retries = self.max_retries if retry else 1

        for attempt in range(retries):
            try:
                logger.debug(f"[Attempt {attempt + 1}/{retries}] {method} {endpoint}")

                async with session.request(
                    method,
                    url,
                    json=json_data,
                    params=params,
                    headers=headers
                ) as resp:
                    try:
                        response_data = await resp.json()
                    except aiohttp.ContentTypeError:
                        response_data = {}
                    except Exception as e:
                        logger.warning(f"Failed to parse JSON response: {e}")
                        response_data = {}

                    logger.debug(f"Response {resp.status} from {endpoint}")

                    # Handle errors
                    if resp.status == 401:
                        raise VeloceAuthError(
                            "Authentication failed. Check API key.",
                            status_code=401,
                            response=response_data
                        )
                    elif resp.status == 403:
                        raise VeloceAuthError(
                            "Permission denied",
                            status_code=403,
                            response=response_data
                        )
                    elif resp.status == 404:
                        raise VeloceNotFoundError(
                            "Resource not found",
                            status_code=404,
                            response=response_data
                        )
                    elif resp.status == 409:
                        raise VeloceConflictError(
                            "Resource already exists",
                            status_code=409,
                            response=response_data
                        )
                    elif resp.status in (400, 422):
                        raise VeloceValidationError(
                            response_data.get("detail", "Validation error"),
                            status_code=resp.status,
                            response=response_data
                        )
                    elif resp.status >= 500:
                        # Server errors are retryable
                        error = VeloceServerError(
                            "Server error",
                            status_code=resp.status,
                            response=response_data
                        )
                        if attempt < retries - 1:
                            last_exception = error
                            delay = min(2 ** attempt, 60)
                            logger.warning(f"Server error, retrying in {delay}s...")
                            await asyncio.sleep(delay)
                            continue
                        raise error

                    return resp.status, response_data

            except (VeloceAuthError, VeloceNotFoundError, VeloceConflictError,
                    VeloceValidationError):
                # These errors are not retryable
                raise
            except VeloceServerError:
                # Already handled above
                raise
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                # Network errors are retryable
                last_exception = e
                if attempt < retries - 1:
                    delay = min(2 ** attempt, 60)
                    logger.warning(f"Network error, retrying in {delay}s: {e}")
                    await asyncio.sleep(delay)
                    continue
                logger.error(f"HTTP client error after {retries} attempts: {e}")
                raise VeloceAPIError(f"HTTP request failed: {e}")
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise VeloceAPIError(f"Request failed: {e}")

        # Should not reach here, but just in case
        if last_exception:
            raise VeloceAPIError(f"Request failed after {retries} attempts: {last_exception}")
        raise VeloceAPIError(f"Request failed after {retries} attempts")
    
    async def health_check(self) -> bool:
        """
        Check if API is accessible

        Returns:
            True if healthy, False otherwise
        """
        try:
            await self._request("GET", "/admin")
            return True
        except VeloceAuthError:
            # Auth error means API is working but credentials are wrong
            return True
        except VeloceAPIError as e:
            logger.warning(f"Health check failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during health check: {e}")
            return False
