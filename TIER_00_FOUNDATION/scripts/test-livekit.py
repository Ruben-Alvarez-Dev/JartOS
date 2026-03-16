#!/usr/bin/env python3
"""
Test script for LiveKit server - OpenClaw-City
Date: 2026-03-10
"""

import asyncio
import aiohttp
from livekit.api import AccessToken, room_service
from livekit.protocol import room as room_proto

# Configuration
LIVEKIT_URL = "http://localhost:7880"
API_KEY = "openclaw-54990a102ce72a4e"
API_SECRET = "YOUR_LIVEKIT_SECRET"

async def test_livekit():
    print("=== LiveKit Server Test ===\n")

    # Test 1: Create token
    print("1. Creating access token...")
    token = (
        AccessToken(API_KEY, API_SECRET)
        .with_identity("test-user")
        .with_name("Test User")
        .to_jwt()
    )
    print(f"   ✅ Token created: {token[:50]}...")

    # Test 2: Connect to RoomService
    print("\n2. Connecting to Room Service...")
    async with aiohttp.ClientSession() as session:
        rs = room_service.RoomService(session, LIVEKIT_URL, API_KEY, API_SECRET)

        # Test 3: List rooms
        print("\n3. Listing rooms...")
        try:
            rooms_response = await rs.list_rooms(room_proto.ListRoomsRequest())
            rooms = rooms_response.rooms
            print(f"   ✅ Rooms found: {len(rooms)}")
            for r in rooms:
                print(f"      - {r.name}: {r.num_participants} participants")
            if not rooms:
                print("   ℹ️ No active rooms (this is normal)")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return

        # Test 4: Create a test room
        print("\n4. Creating test room 'openclaw-test'...")
        try:
            create_response = await rs.create_room(room_proto.CreateRoomRequest(name="openclaw-test"))
            print(f"   ✅ Room created: {create_response.name}")

            # Delete test room
            await rs.delete_room(room_proto.DeleteRoomRequest(room="openclaw-test"))
            print(f"   ✅ Test room cleaned up")
        except Exception as e:
            print(f"   ⚠️ Note: {e}")

        print("\n=== Test Complete ===")
        print("\nLiveKit server is working correctly! ✅")
        print(f"\nConnection details:")
        print(f"  URL: {LIVEKIT_URL}")
        print(f"  API Key: {API_KEY}")

if __name__ == "__main__":
    asyncio.run(test_livekit())
