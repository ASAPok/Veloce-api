"""
Advanced usage examples for Veloce API
"""

import asyncio
import os
from datetime import datetime
from veloce import VeloceClient
from veloce.utils import setup_logging
from veloce.exceptions import VeloceAPIError


async def batch_user_creation():
    """Create multiple users efficiently"""
    setup_logging("INFO")

    async with VeloceClient(
        base_url=os.getenv("VELOCE_URL", "https://your-panel.com/api"),
        api_key=os.getenv("VELOCE_API_KEY", "your_api_key")
    ) as client:
        usernames = [f"user{i}" for i in range(1, 11)]

        for username in usernames:
            try:
                url = await client.users.create_free(username)
                print(f"Created {username}: {url}")
            except VeloceAPIError as e:
                print(f"Failed to create {username}: {e}")


async def monitor_system():
    """Monitor system statistics"""
    setup_logging("INFO")

    async with VeloceClient(
        base_url=os.getenv("VELOCE_URL"),
        api_key=os.getenv("VELOCE_API_KEY")
    ) as client:
        while True:
            try:
                stats = await client.system.get_stats()

                print(f"\n=== System Stats at {datetime.now()} ===")
                print(f"Total users: {stats['total_user']}")
                print(f"Active users: {stats['users_active']}")
                print(f"Incoming bandwidth: {stats['incoming_bandwidth']:,} bytes")
                print(f"Outgoing bandwidth: {stats['outgoing_bandwidth']:,} bytes")
                print(f"Incoming speed: {stats['incoming_bandwidth_speed']:,} bytes/s")
                print(f"Outgoing speed: {stats['outgoing_bandwidth_speed']:,} bytes/s")

                await asyncio.sleep(10)

            except KeyboardInterrupt:
                print("\nMonitoring stopped")
                break
            except VeloceAPIError as e:
                print(f"Error fetching stats: {e}")
                await asyncio.sleep(5)


async def user_lifecycle():
    """Complete user lifecycle management"""
    setup_logging("INFO")

    async with VeloceClient(
        base_url=os.getenv("VELOCE_URL"),
        api_key=os.getenv("VELOCE_API_KEY")
    ) as client:
        username = "demo_user"

        # 1. Create free user
        print(f"Creating free user: {username}")
        url = await client.users.create_free(username)
        print(f"Subscription URL: {url}")

        # 2. Check user info
        user = await client.users.get(username)
        print(f"User status: {user['status']}")
        print(f"Free tier: {user['expire'] == 1}")

        # 3. Upgrade to paid
        print(f"\nUpgrading to paid subscription (30 days)")
        url = await client.users.extend_subscription(username, days=30)
        print(f"New URL: {url}")

        # 4. Get usage stats
        usage = await client.users.get_usage(username)
        print(f"\nUsage stats:")
        print(f"Used traffic: {usage['used_traffic']:,} bytes")
        print(f"Data limit: {usage['data_limit']}")
        print(f"Expire: {usage['expire']}")

        # 5. Reset traffic
        print("\nResetting traffic")
        await client.users.reset_traffic(username)

        # 6. Extend subscription
        print("Extending subscription by 7 days")
        await client.users.extend_subscription(username, days=7)

        # 7. Ban user temporarily
        print("\nBanning user")
        await client.users.ban(username)

        user = await client.users.get(username)
        print(f"User status after ban: {user['status']}")

        # 8. Unban user
        print("\nUnbanning user")
        await client.users.unban(username)

        user = await client.users.get(username)
        print(f"User status after unban: {user['status']}")


async def node_management():
    """Manage nodes"""
    setup_logging("INFO")

    async with VeloceClient(
        base_url=os.getenv("VELOCE_URL"),
        api_key=os.getenv("VELOCE_API_KEY")
    ) as client:
        # List all nodes
        nodes = await client.nodes.list()
        print(f"Total nodes: {len(nodes)}")

        for node in nodes:
            print(f"\nNode: {node['name']}")
            print(f"  Address: {node['address']}:{node['port']}")
            print(f"  Status: {node['status']}")
            print(f"  Coefficient: {node['usage_coefficient']}")

            # Get node usage
            usage = await client.nodes.get_usage(node['id'])
            if usage:
                print(f"  Uplink: {usage.get('uplink', 0):,} bytes")
                print(f"  Downlink: {usage.get('downlink', 0):,} bytes")


async def api_key_management():
    """Manage API keys (requires admin privileges)"""
    setup_logging("INFO")

    async with VeloceClient(
        base_url=os.getenv("VELOCE_URL"),
        api_key=os.getenv("VELOCE_API_KEY")
    ) as client:
        # List existing keys
        keys = await client.api_keys.list()
        print(f"Existing API keys: {len(keys)}")

        for key in keys:
            print(f"- {key['name']} (ID: {key['id']}, Active: {key['is_active']})")

        # Create new key
        new_key = await client.api_keys.create("test_key")
        if new_key:
            print(f"\nNew API key created:")
            print(f"ID: {new_key['id']}")
            print(f"Name: {new_key['name']}")
            print(f"Key: {new_key['key']}")
            print("IMPORTANT: Save this key, it won't be shown again!")


if __name__ == "__main__":
    # Choose which example to run
    import sys

    if len(sys.argv) < 2:
        print("Usage: python advanced_usage.py <example>")
        print("Examples: batch, monitor, lifecycle, nodes, apikeys")
        sys.exit(1)

    example = sys.argv[1].lower()

    if example == "batch":
        asyncio.run(batch_user_creation())
    elif example == "monitor":
        asyncio.run(monitor_system())
    elif example == "lifecycle":
        asyncio.run(user_lifecycle())
    elif example == "nodes":
        asyncio.run(node_management())
    elif example == "apikeys":
        asyncio.run(api_key_management())
    else:
        print(f"Unknown example: {example}")
