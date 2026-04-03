#!/usr/bin/env python3
"""Script to create a health check cron job via WebSocket."""
import asyncio
import json
import sys

try:
    import websockets
except ImportError:
    print("Installing websockets...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "websockets"])
    import websockets

ACCESS_KEY = "my_secret_api_key"
WS_URL = "ws://10.93.26.140:42002/ws/chat?access_key=my_secret_api_key"


async def create_health_check():
    """Connect to WebSocket and create a health check cron job."""
    headers = {
        "X-Access-Key": ACCESS_KEY,
    }
    
    try:
        async with websockets.connect(WS_URL) as ws:
            print("Connected to WebSocket")
            
            # Wait for initial message
            msg = await ws.recv()
            print(f"Received: {msg[:200]}...")
            
            # Send message to create health check
            health_check_msg = {
                "type": "message",
                "content": "Create a health check for this chat that runs every 15 minutes. Each run should check for backend errors in the last 15 minutes, inspect a trace if needed, and post a short summary here. If there are no recent errors, say the system looks healthy. Use your cron tool."
            }
            
            await ws.send(json.dumps(health_check_msg))
            print("Sent health check request")
            
            # Wait for response
            for _ in range(30):
                try:
                    response = await asyncio.wait_for(ws.recv(), timeout=60)
                    print(f"Response: {response[:300]}...")
                    
                    # Check if it's the final response
                    try:
                        data = json.loads(response)
                        if data.get("type") == "message" and "health" in data.get("content", "").lower():
                            print("\n✓ Health check created successfully!")
                            return True
                    except:
                        pass
                except asyncio.TimeoutError:
                    print("Timeout waiting for response")
                    break
            
            print("\n✓ Request sent to agent")
            return True
            
    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(create_health_check())
    sys.exit(0 if success else 1)
