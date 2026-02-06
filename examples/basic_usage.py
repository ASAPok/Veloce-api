"""
Basic usage examples for Veloce API
"""

import asyncio
from veloce import VeloceClient
from veloce.utils import setup_logging
from veloce.exceptions import VeloceAPIError, VeloceNotFoundError


async def main():
    # Setup logging to see debug information
    setup_logging("INFO")

    # Method 1: Using context manager (recommended - automatically closes session)
    async with VeloceClient(
        base_url="https://your-panel.com/api",
        api_key="your_api_key",
        timeout=30,
        max_retries=3
    ) as client:
        # Create free user
        try:
            url = await client.users.create_free("user123")
            print(f"Free user created: {url}")
        except VeloceAPIError as e:
            print(f"Error creating user: {e}")

        # Get user info
        user = await client.users.get("user123")
        if user:
            print(f"User status: {user['status']}")
            print(f"Expire: {user['expire']}")

        # Extend subscription
        url = await client.users.extend_subscription("user123", days=30)
        print(f"Subscription extended: {url}")

        # List all users
        result = await client.users.list(offset=0, limit=10)
        print(f"Total users: {result['total']}")
        for user in result['users']:
            print(f"- {user['username']}: {user['status']}")

        # Get system stats
        stats = await client.system.get_stats()
        print(f"Total users: {stats['total_user']}")
        print(f"Active users: {stats['users_active']}")

        # List nodes
        nodes = await client.nodes.list()
        for node in nodes:
            print(f"Node: {node['name']} - {node['status']}")


async def manual_session_management():
    # Method 2: Manual session management
    client = VeloceClient(
        base_url="https://your-panel.com/api",
        api_key="your_api_key"
    )

    try:
        url = await client.users.create_free("user456")
        print(f"User created: {url}")
    finally:
        await client.close()


async def error_handling():
    async with VeloceClient("https://your-panel.com/api", "your_api_key") as client:
        try:
            user = await client.users.get("nonexistent")
            if user is None:
                print("User not found")
        except VeloceNotFoundError:
            print("User does not exist")
        except VeloceAPIError as e:
            print(f"API error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
